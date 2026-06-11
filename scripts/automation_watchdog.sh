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

log "=== watchdog 완료 ==="
exit 0
