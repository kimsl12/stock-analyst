#!/bin/bash
#
# daily_pick_update.sh — DailyPick 위젯 매일 KST 자정 자동 갱신
#
# 동작:
#   1. 외장 SSD 마운트 확인
#   2. git pull (원격 최신)
#   3. build_daily_pick.mjs 재실행 → web/src/data/daily_pick.json
#   4. 변경 있으면 commit + push + Vercel + Cloudflare deploy
#   5. 변경 없으면 skip (어제 픽 그대로)
#
# launchd 등록:
#   cp scripts/launchd/com.stockanalyst.daily-pick.plist ~/Library/LaunchAgents/
#   launchctl load ~/Library/LaunchAgents/com.stockanalyst.daily-pick.plist
#
# 수동 테스트:
#   bash scripts/daily_pick_update.sh
#

set -uo pipefail

PROJECT_ROOT="/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
LOG="$PROJECT_ROOT/scripts/launchd/daily-pick.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "=== daily_pick 자동 갱신 시작 ==="

# 1. 외장 SSD 마운트 확인
if [ ! -d "$PROJECT_ROOT" ]; then
  log "ERROR: 프로젝트 폴더 미존재 (외장 SSD 미마운트 가능성). 중단."
  exit 1
fi

cd "$PROJECT_ROOT" || { log "ERROR: cd 실패"; exit 1; }

# 2. 사전 git 상태 — 다른 변경 없어야 함 (충돌 회피)
if ! git diff --quiet HEAD; then
  log "WARN: 작업 트리에 미커밋 변경 있음 — daily_pick.json 외 다른 변경은 보존 (stash 안 함)"
fi

# 3. 원격 최신화
log "git pull --rebase origin main"
if ! git pull --rebase origin main 2>&1 | tee -a "$LOG" | tail -3; then
  log "WARN: git pull 실패 — local 그대로 진행"
fi

# 4. daily_pick.json 재빌드
log "build_daily_pick.mjs 실행"
cd web || { log "ERROR: web/ cd 실패"; exit 1; }
if ! node scripts/build_daily_pick.mjs 2>&1 | tee -a "$LOG" | tail -3; then
  log "ERROR: build_daily_pick 실패 — deploy 스킵"
  exit 1
fi
cd "$PROJECT_ROOT" || exit 1

# 5. 변경 있는지 확인
if git diff --quiet web/src/data/daily_pick.json; then
  log "변경 없음 — commit/deploy 스킵 (어제 픽 유지 가능성)"
  log "=== 완료 (skip) ==="
  exit 0
fi

# 6. 메타 추출
PICK_DATE=$(jq -r '.pick_date' web/src/data/daily_pick.json 2>/dev/null || echo "unknown")
PICK_TICKER=$(jq -r '.pick.ticker // "none"' web/src/data/daily_pick.json 2>/dev/null)
PICK_SCORE=$(jq -r '.pick.score // 0' web/src/data/daily_pick.json 2>/dev/null)
PICK_GRADE=$(jq -r '.pick.grade // "-"' web/src/data/daily_pick.json 2>/dev/null)
log "갱신 감지: $PICK_DATE / $PICK_TICKER / $PICK_SCORE $PICK_GRADE"

# 7. commit + push
git add web/src/data/daily_pick.json
if ! git commit -m "chore(daily_pick): 자동 갱신 ${PICK_DATE} — ${PICK_TICKER} ${PICK_SCORE}점 ${PICK_GRADE} (launchd)"; then
  log "ERROR: git commit 실패"
  exit 1
fi

log "git push origin main"
if ! git push origin main 2>&1 | tee -a "$LOG" | tail -3; then
  log "ERROR: git push 실패 — deploy 스킵 (다음 회차에 재시도)"
  exit 1
fi

# 8. deploy 두 채널
log "vercel --prod --yes"
if vercel --prod --yes 2>&1 | tee -a "$LOG" | tail -3; then
  log "Vercel 배포 완료"
else
  log "WARN: Vercel 배포 실패"
fi

log "bash scripts/deploy_cloudflare.sh"
if bash scripts/deploy_cloudflare.sh 2>&1 | tee -a "$LOG" | tail -3; then
  log "Cloudflare 배포 완료"
else
  log "WARN: Cloudflare 배포 실패"
fi

log "=== 완료 ($PICK_TICKER ${PICK_SCORE}점) ==="
