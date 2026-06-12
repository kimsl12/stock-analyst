#!/usr/bin/env bash
#
# automation_watchdog.sh — 자동화 상태 점검 + 포트폴리오 감시 (매일 KST 06:40 / 10:30)
#
# 점검 항목:
#   1. 외장 SSD 마운트
#   2. daily_pick.json 신선도 (pick_date == 오늘 KST — 00:05 launchd 성공 여부 사후 검증)
#   3. git 미푸시 커밋 (push 실패 잔존 감지 — 사이트 stale)
#   4. holdings_health.json 재생성 (최신 분석 반영)
#   5. portfolio_watch.py — 손절/목표가 도달 + 리밸런싱 드리프트 알림
#
# 알림: scripts/notify.sh (macOS 알림센터 + NTFY_TOPIC 설정 시 폰 푸시)
# 로그: scripts/launchd/watchdog.log
#
# 설치:
#   cp scripts/launchd/com.stockanalyst.watchdog.plist ~/Library/LaunchAgents/
#   launchctl load ~/Library/LaunchAgents/com.stockanalyst.watchdog.plist
#
# 수동 테스트:
#   bash scripts/automation_watchdog.sh
#

set -uo pipefail

PROJECT_ROOT="/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
NOTIFY="$PROJECT_ROOT/scripts/notify.sh"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

notify_warn() {
  bash "$NOTIFY" "자동화 watchdog" "$1" "${2:-default}" || true
}

log "=== watchdog 시작 ==="

# 1. 마운트 확인 (미마운트면 알림 불가 항목 없이 종료 — osascript 는 동작)
if [ ! -d "$PROJECT_ROOT" ]; then
  osascript -e 'display notification "외장 SSD 미마운트 — 자동화 전체 중단 상태" with title "자동화 watchdog"' || true
  exit 1
fi
cd "$PROJECT_ROOT" || exit 1

# 2. daily_pick 신선도 (KST 오늘 == pick_date)
TODAY_KST=$(TZ=Asia/Seoul date '+%Y-%m-%d')
PICK_DATE=$(jq -r '.pick_date // "unknown"' web/src/data/daily_pick.json 2>/dev/null || echo "unknown")
if [ "$PICK_DATE" != "$TODAY_KST" ]; then
  log "WARN: daily_pick stale — pick_date=$PICK_DATE, today=$TODAY_KST"
  notify_warn "DailyPick 미갱신 감지 — pick_date=$PICK_DATE (오늘 $TODAY_KST). daily-pick.log 확인 필요" high
else
  log "OK: daily_pick 신선 ($PICK_DATE)"
fi

# 3. 미푸시 커밋 감지 (push 실패 잔존 → 사이트 stale)
git fetch origin main --quiet 2>/dev/null || log "WARN: git fetch 실패 (오프라인?)"
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
if [ "$AHEAD" -gt 0 ]; then
  log "WARN: 미푸시 커밋 ${AHEAD}건"
  notify_warn "미푸시 커밋 ${AHEAD}건 — 사이트 미반영 상태. git push 필요" high
else
  log "OK: 원격 동기 상태"
fi

# 4. holdings_health 재생성 (분석 최신화 반영 — 실패해도 기존 파일로 5번 진행)
if node web/scripts/build_holdings_health.mjs 2>&1; then
  log "OK: holdings_health 재생성"
else
  log "WARN: build_holdings_health 실패 — 기존 데이터로 감시 진행"
  notify_warn "holdings_health 재생성 실패 — 감시는 기존 데이터로 진행"
fi

# 5. 손절/목표가 + 드리프트 감시 (스크립트 내부에서 자체 알림·디듀프)
if python3 scripts/portfolio_watch.py 2>&1 | grep -v "FutureWarning\|warnings.warn\|NotOpenSSL"; then
  log "OK: portfolio_watch 완료"
else
  log "WARN: portfolio_watch 실패"
  notify_warn "portfolio_watch 실행 실패 — 손절/목표가 감시 미수행" high
fi

# 6. 일일 레짐 분류 (전환 시 스크립트가 자체 알림) [v3.28]
if python3 scripts/regime_classifier.py 2>&1 | grep -v "FutureWarning\|warnings.warn\|NotOpenSSL"; then
  log "OK: regime_classifier 완료"
else
  log "WARN: regime_classifier 실패 — 브리핑은 직전 regime.json 사용"
fi

# 7. 하우스 뷰 반증 조건 평가 (도달 시 스크립트가 자체 알림) [v3.28]
if python3 scripts/check_house_view.py 2>&1 | grep -v "FutureWarning\|warnings.warn\|NotOpenSSL"; then
  log "OK: check_house_view 완료"
else
  log "WARN: check_house_view 실패"
fi

# 8. 매매 시그널 신선도 (stock_scores.json — 엔진 게이트가 stale 신호로 전면 차단되는 사고 방지) [v3.33]
SIG_GEN=$(python3 -c "import json; print(json.load(open('algo-trading/data/stock_scores.json'))['generated_at'][:10])" 2>/dev/null || echo "")
YESTERDAY=$(TZ=Asia/Seoul date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d 'yesterday' '+%Y-%m-%d')
if [ -z "$SIG_GEN" ]; then
  log "WARN: stock_scores.json 읽기 실패"
  notify_warn "매매 시그널 파일 읽기 실패 — signals.log 확인" high
elif [ "$SIG_GEN" \< "$YESTERDAY" ]; then
  log "WARN: 매매 시그널 stale (generated=$SIG_GEN)"
  notify_warn "매매 시그널 stale (${SIG_GEN}) — 15:25 launchd 실패 의심, 엔진 매매 차단 중" high
else
  log "OK: 매매 시그널 신선 ($SIG_GEN)"
fi

# 9. 알고 매매 보유 동기화 + 신선도 (장중 긴급 체결 잔여분 웹 반영) [v3.34]
if bash scripts/algo_portfolio_sync.sh 2>&1; then
  log "OK: algo_portfolio_sync 완료"
else
  log "WARN: algo_portfolio_sync 실패"
  notify_warn "algo_portfolio_sync 실행 실패 — 알고 보유 웹 반영 누락 가능" high
fi
# 엔진 live 인데 2일+ 무보고 → 엔진 쪽 장애 의심 (not_live/paused 는 정상이므로 침묵)
ALGO_STATE=$(python3 -c "
import json
d = json.load(open('algo-trading/data/algo_holdings.json'))
print(d.get('engine_status',''), (d.get('generated_at') or '')[:10])" 2>/dev/null || echo "")
if [ -n "$ALGO_STATE" ]; then
  ALGO_STATUS=$(echo "$ALGO_STATE" | cut -d' ' -f1)
  ALGO_GEN=$(echo "$ALGO_STATE" | cut -d' ' -f2)
  TWO_DAYS_AGO=$(TZ=Asia/Seoul date -v-2d '+%Y-%m-%d' 2>/dev/null || date -d '2 days ago' '+%Y-%m-%d')
  if [ "$ALGO_STATUS" = "live" ] && [ -n "$ALGO_GEN" ] && [ "$ALGO_GEN" \< "$TWO_DAYS_AGO" ]; then
    log "WARN: 알고 엔진 무보고 (status=live, generated=$ALGO_GEN)"
    notify_warn "알고 엔진 보유 보고 ${ALGO_GEN} 이후 중단 — 엔진 쪽 점검 필요" high
  else
    log "OK: 알고 보유 보고 상태 정상 (status=$ALGO_STATUS, generated=$ALGO_GEN)"
  fi
fi

log "=== watchdog 완료 ==="
exit 0
