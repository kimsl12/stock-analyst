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
#   11. 데일리픽 성적표 신선도(2일) + 논지 판정 대기(14일)
#   12. 브리핑 발행 점검 (앱 스케줄 생존 카나리아)
#   13. 점수 이력 원장 append
#   14. 목표 비중 동기화 지연(10일)
#
# 알림: scripts/notify.sh (macOS 알림센터)
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

# 10. 본서버 배포 신선도 (로컬 pick_date vs 배포 사이트 — 8/13~25 12일 동결 무감지 사고 재발 차단) [v3.41]
DEPLOYED_PICK=$(curl -s -m 15 "https://stock-analyst-jungwon1.vercel.app/" 2>/dev/null | grep -oE 'data-pick-date="[^"]*"' | head -1 | cut -d'"' -f2)
LOCAL_PICK=$(jq -r '.pick_date // ""' web/src/data/daily_pick.json 2>/dev/null)
if [ -z "$DEPLOYED_PICK" ]; then
  log "WARN: 본서버 pick_date 추출 실패 (네트워크/마크업 변경?)"
elif [ -n "$LOCAL_PICK" ] && [ "$DEPLOYED_PICK" != "$LOCAL_PICK" ]; then
  # 하루 이상 괴리만 경고 (빌드 진행 중 수 분 괴리는 정상)
  if [ "$DEPLOYED_PICK" \< "$(TZ=Asia/Seoul date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d 'yesterday' '+%Y-%m-%d')" ]; then
    log "WARN: 본서버 동결 의심 — 배포 $DEPLOYED_PICK vs 로컬 $LOCAL_PICK"
    notify_warn "본서버 사이트 동결 의심 (배포 ${DEPLOYED_PICK} vs 로컬 ${LOCAL_PICK}) — vercel ls 로 배포 Error 확인 필요" high
  else
    log "OK: 본서버 신선도 허용 범위 (배포 $DEPLOYED_PICK)"
  fi
else
  log "OK: 본서버 신선 ($DEPLOYED_PICK)"
fi

# 11. 데일리픽 성적표 신선도 + 논지 판정 대기 (eval 경로는 DAILY_PICK_EVAL_JSON 로 override 가능 — 테스트용)
EVAL_JSON="${DAILY_PICK_EVAL_JSON:-web/src/data/daily_pick_eval.json}"
EVAL_STATE=$(python3 - "$EVAL_JSON" <<'PY' 2>/dev/null || echo ""
import json, sys
from datetime import date, datetime, timedelta, timezone
today = datetime.now(timezone(timedelta(hours=9))).date()
d = json.load(open(sys.argv[1]))
gen = (d.get("generated_at") or "")[:10]
old = ((d.get("pending") or {}).get("oldest_unjudged_date") or "")[:10]
gen_age = (today - date.fromisoformat(gen)).days if gen else -1
old_age = (today - date.fromisoformat(old)).days if old else 0
print(gen or "-", gen_age, old or "-", old_age)
PY
)
if [ -z "$EVAL_STATE" ]; then
  log "WARN: daily_pick_eval.json 읽기 실패"
  notify_warn "데일리픽 성적표 파일 읽기 실패 — eval.json 확인" high
else
  read -r EVAL_GEN EVAL_GEN_AGE EVAL_OLD EVAL_OLD_AGE <<< "$EVAL_STATE"
  if [ "$EVAL_GEN_AGE" -lt 0 ] || [ "$EVAL_GEN_AGE" -gt 2 ]; then
    log "WARN: 데일리픽 성적표 stale (generated_at=$EVAL_GEN)"
    notify_warn "데일리픽 성적표 미갱신 (generated_at=${EVAL_GEN})" high
  else
    log "OK: 데일리픽 성적표 신선 ($EVAL_GEN)"
  fi
  if [ "$EVAL_OLD_AGE" -gt 14 ]; then
    log "WARN: 논지 판정 대기 ${EVAL_OLD_AGE}일 (oldest=$EVAL_OLD)"
    notify_warn "데일리픽 논지 판정 대기 14일 초과 — 토요일 /성과리뷰 확인"
  else
    log "OK: 논지 판정 대기 정상 (oldest=$EVAL_OLD)"
  fi
fi

# 12. 브리핑 발행 점검 — 앱 스케줄 생존 카나리아 (2026-10-29~11-02 앱 스케줄 4일 공백 무감지 재발 차단)
#     06:40 회차: 전일 이브닝 / 10:30 회차: 당일 모닝(09:03 스케줄). 일간 브리핑을 중단하면 이 단계 제거.
if (( 10#$(TZ=Asia/Seoul date '+%H') >= 10 )); then
  BRIEF_FILE="reports/briefing/morning_$(TZ=Asia/Seoul date '+%Y%m%d').html"
  BRIEF_LABEL="오늘 모닝 브리핑"
else
  BRIEF_FILE="reports/briefing/evening_$(TZ=Asia/Seoul date -v-1d '+%Y%m%d' 2>/dev/null || date -d 'yesterday' '+%Y%m%d').html"
  BRIEF_LABEL="전일 이브닝 브리핑"
fi
if [ -f "$BRIEF_FILE" ]; then
  log "OK: ${BRIEF_LABEL} 발행 확인 ($BRIEF_FILE)"
else
  log "WARN: ${BRIEF_LABEL} 미발행 ($BRIEF_FILE 없음)"
  notify_warn "${BRIEF_LABEL} 미발행 — Claude 앱 스케줄 중단 의심 (앱 실행·로그인 상태 확인)" high
fi

# 13. 점수 이력 원장 append (timeline 은 종목당 최근 3건만 보존 → 과거 점수 유실 차단. 멱등)
if [ -f scripts/score_ledger.py ]; then
  if python3 scripts/score_ledger.py append 2>&1 | tail -2; then
    log "OK: score_ledger append 완료"
  else
    log "WARN: score_ledger append 실패"
    notify_warn "점수 이력 원장 append 실패 — scripts/score_ledger.py 확인"
  fi
fi

# 14. 목표 비중 동기화 지연 (/내포트폴리오 주 1회 → 10일 초과 시 드리프트 감시가 옛 목표 기준으로 도는 상태.
#     8/29~11/25 88일 미동기화 무감지 재발 차단)
TGT_AGE=$(python3 - <<'PY' 2>/dev/null || echo ""
import json, re
from datetime import date, datetime, timedelta, timezone
d = json.load(open("scripts/portfolio_targets.json"))
m = re.search(r"(\d{8})", d.get("source") or "")
s = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}" if m else (d.get("seeded_at") or "")[:10]
today = datetime.now(timezone(timedelta(hours=9))).date()
print(s, (today - date.fromisoformat(s)).days)
PY
)
if [ -z "$TGT_AGE" ]; then
  log "WARN: portfolio_targets.json 기준일 읽기 실패"
else
  read -r TGT_DATE TGT_DAYS <<< "$TGT_AGE"
  if [ "$TGT_DAYS" -gt 10 ]; then
    log "WARN: 목표 비중 ${TGT_DAYS}일 미동기화 (기준 $TGT_DATE)"
    notify_warn "포트폴리오 목표 비중 ${TGT_DAYS}일 미동기화 (기준 ${TGT_DATE}) — /내포트폴리오 실행 필요"
  else
    log "OK: 목표 비중 동기화 정상 (기준 $TGT_DATE, ${TGT_DAYS}일 전)"
  fi
fi

log "=== watchdog 완료 ==="
exit 0
