#!/usr/bin/env bash
#
# algo_portfolio_sync.sh — 알고 매매 보유·체결 변경 → 웹사이트 자동 반영 (매일 KST 16:15)
#
# 계약 (algo-trading/algo_engine_handoff.md §9): 엔진이 체결 직후 + 매일 15:40 런 종료 시
# algo-trading/data/algo_holdings.json 을 덮어씀. 이 스크립트는 그 파일의 변경을 감지해
# commit → push → Vercel + Cloudflare 배포 → /portfolio "알고 자동매매" 섹션 갱신.
#
# 호출 경로 2곳 (둘 다 idempotent — 변경 없으면 조용히 종료):
#   1. launchd com.stockanalyst.algo-sync (16:15 — 엔진 15:40 매매 직후)
#   2. automation_watchdog.sh 9단계 (06:40 / 10:30 — 장중 긴급 체결 잔여분)
#
# 수동 테스트: bash scripts/algo_portfolio_sync.sh
#

set -uo pipefail

PROJECT_ROOT="/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
NOTIFY="$PROJECT_ROOT/scripts/notify.sh"
HOLDINGS_FILE="algo-trading/data/algo_holdings.json"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }
notify_fail() { bash "$NOTIFY" "알고 보유 동기화 실패" "$1" "${2:-default}" || true; }

log "=== algo 보유 동기화 시작 ==="

if [ ! -d "$PROJECT_ROOT" ]; then
  osascript -e 'display notification "외장 SSD 미마운트 — 알고 보유 동기화 불가" with title "알고 보유 동기화 실패"' || true
  exit 1
fi
cd "$PROJECT_ROOT" || exit 1

# 변경 감지 — 엔진이 새로 쓴 게 없으면 즉시 종료 (watchdog 호출 시 대부분 이 경로)
if git diff --quiet -- "$HOLDINGS_FILE" && [ -z "$(git ls-files --others --exclude-standard -- "$HOLDINGS_FILE")" ]; then
  log "변경 없음 — 종료"
  exit 0
fi

# git pull — 헤드리스 행 방지 (자격증명 프롬프트 차단 + 120초 타임아웃, signals_update 와 동일 패턴)
export GIT_TERMINAL_PROMPT=0
git pull --rebase --autostash origin main 2>&1 &
PULL_PID=$!
for _ in $(seq 1 24); do
  kill -0 "$PULL_PID" 2>/dev/null || break
  sleep 5
done
if kill -0 "$PULL_PID" 2>/dev/null; then
  kill "$PULL_PID" 2>/dev/null || true
  log "WARN: git pull 타임아웃 — 로컬 상태로 진행"
fi
wait "$PULL_PID" 2>/dev/null || log "WARN: git pull 실패 — 로컬 상태로 진행"

# 커밋 메시지용 요약 (jq 없는 환경 대비 python3)
POS_COUNT=$(python3 -c "import json; print(len(json.load(open('$HOLDINGS_FILE')).get('positions') or []))" 2>/dev/null || echo "?")
LAST_TRADE=$(python3 -c "
import json
t = (json.load(open('$HOLDINGS_FILE')).get('trades') or [])
print(f\"{t[0]['action']} {t[0]['ticker']}\" if t else '체결 없음')" 2>/dev/null || echo "?")
TODAY=$(TZ=Asia/Seoul date '+%Y-%m-%d')

git add "$HOLDINGS_FILE"
if git diff --cached --quiet; then
  log "스테이징 후 변경 없음 (pull 로 동기화됨) — 종료"
  exit 0
fi
if ! git commit -m "chore(algo): 알고 매매 보유 반영 ${TODAY} — 포지션 ${POS_COUNT}건, 최근 ${LAST_TRADE} (launchd)"; then
  log "ERROR: git commit 실패"
  notify_fail "algo_holdings commit 실패 — 사이트 미반영" high
  exit 1
fi

# push 실패는 비치명 (다음 회차/세션 재시도 + watchdog 미푸시 감지) — 배포는 로컬 파일 기준이라 진행
if ! git push origin main 2>&1; then
  log "WARN: git push 실패 — 로컬 커밋 유지, 배포는 진행"
  notify_fail "algo 보유 push 실패 — 배포는 진행됨, 커밋은 다음 회차 push"
fi

# deploy — Cloudflare 미러 (풀사이트 패키징, 2026-06-12 전환 — 플래그 기간 주채널)
# → Vercel (timeout 가드: 플래그 기간 Blocked + 좀비 행 실측, 해제 후 자동 복구)
log "bash scripts/deploy_cloudflare.sh"
if bash scripts/deploy_cloudflare.sh 2>&1; then
  log "Cloudflare 배포 완료"
  bash "$NOTIFY" "알고 매매 보유 반영" "포지션 ${POS_COUNT}건, 최근 ${LAST_TRADE} — 미러 /portfolio 갱신 완료" || true
else
  log "WARN: Cloudflare 배포 실패"
  notify_fail "알고 보유 미러 배포 실패 — 사이트 미반영 (단독 재실행 가능)" high
fi

log "vercel --prod --yes (timeout 160s)"
if timeout 160 vercel --prod --yes < /dev/null 2>&1; then
  log "Vercel 배포 완료"
else
  log "WARN: Vercel 배포 실패/타임아웃 — 플래그 기간 예상 동작 (해제 후 자동 복구)"
fi

log "=== 완료 (포지션 ${POS_COUNT}건) ==="
exit 0
