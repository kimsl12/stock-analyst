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

set -euo pipefail

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

# 2. 원격 최신화 (unstaged changes 자동 stash 처리, v3.22 P1-10 fail-fast)
log "git pull --rebase --autostash origin main"
if ! git pull --rebase --autostash origin main 2>&1; then
  log "ERROR: git pull 실패 — 누적 충돌 위험 (silent state corruption 방지). deploy 중단."
  exit 1
fi

# 3. daily_pick.json + kb.json 재빌드 (past 필터 매일 재계산 — economic_calendar 등)
log "build_daily_pick.mjs + build_kb.mjs 실행"
cd web || { log "ERROR: web/ cd 실패"; exit 0; }
if ! node scripts/build_daily_pick.mjs 2>&1; then
  log "ERROR: build_daily_pick 실패 — deploy 중단 (silent corruption 차단)"
  exit 1
fi
# kb.json 은 .gitignore (vercel 컨테이너 안 매 deploy 시 재빌드 정상). 로컬 검증용 빌드.
if ! node scripts/build_kb.mjs 2>&1; then
  log "WARN: build_kb 실패 — 로컬 kb.json stale 가능성 (본서버는 vercel 빌드 시 재계산)"
fi
cd "$PROJECT_ROOT" || exit 0

# 4. 변경 있는지 확인 (daily_pick.json 또는 KB 본문 신규 변경)
KB_CHANGED=$(git status --porcelain knowledge-base/market/ 2>/dev/null | wc -l | tr -d ' ')
if git diff --quiet web/src/data/daily_pick.json && [ "$KB_CHANGED" -eq 0 ]; then
  log "변경 없음 — commit/deploy 스킵 (어제 픽 유지 + KB 본문 무변경)"
  log "=== 완료 (skip) ==="
  exit 0
fi
if git diff --quiet web/src/data/daily_pick.json && [ "$KB_CHANGED" -gt 0 ]; then
  log "daily_pick 무변경이나 KB 본문 ${KB_CHANGED}건 변경 감지 — vercel deploy 강제 (본서버 past 필터 재계산용)"
  # daily_pick commit 없이 deploy 만
  log "vercel --prod --yes (KB 본문 트리거)"
  vercel --prod --yes 2>&1 | tail -5
  log "bash scripts/deploy_cloudflare.sh (KB 본문 트리거)"
  bash scripts/deploy_cloudflare.sh 2>&1 | tail -3
  log "=== 완료 (KB-only deploy) ==="
  exit 0
fi

# 5. 메타 추출
PICK_DATE=$(jq -r '.pick_date' web/src/data/daily_pick.json 2>/dev/null || echo "unknown")
PICK_TICKER=$(jq -r '.pick.ticker // "none"' web/src/data/daily_pick.json 2>/dev/null)
PICK_SCORE=$(jq -r '.pick.score // 0' web/src/data/daily_pick.json 2>/dev/null)
PICK_GRADE=$(jq -r '.pick.grade // "-"' web/src/data/daily_pick.json 2>/dev/null)
log "갱신 감지: $PICK_DATE / $PICK_TICKER / $PICK_SCORE $PICK_GRADE"

# 6. commit + push
git add web/src/data/daily_pick.json
if ! git commit -m "chore(daily_pick): 자동 갱신 ${PICK_DATE} — ${PICK_TICKER} ${PICK_SCORE}점 ${PICK_GRADE} (launchd)"; then
  log "ERROR: git commit 실패"
  exit 0
fi

log "git push origin main"
if ! git push origin main 2>&1; then
  log "ERROR: git push 실패 — 다음 회차에 재시도"
  exit 0
fi

# 7. deploy 두 채널
log "vercel --prod --yes"
if vercel --prod --yes 2>&1; then
  log "Vercel 배포 완료"
else
  log "WARN: Vercel 배포 실패"
fi

log "bash scripts/deploy_cloudflare.sh"
if bash scripts/deploy_cloudflare.sh 2>&1; then
  log "Cloudflare 배포 완료"
else
  log "WARN: Cloudflare 배포 실패"
fi

log "=== 완료 ($PICK_TICKER ${PICK_SCORE}점) ==="
exit 0
