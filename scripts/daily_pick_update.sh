#!/usr/bin/env bash
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
NOTIFY="$PROJECT_ROOT/scripts/notify.sh"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

notify_fail() {
  bash "$NOTIFY" "DailyPick 자동화 실패" "$1" high || true
}

log "=== daily_pick 자동 갱신 시작 ==="

# 1. 외장 SSD 마운트 확인
if [ ! -d "$PROJECT_ROOT" ]; then
  log "ERROR: 프로젝트 폴더 미존재 (외장 SSD 미마운트 가능성). 중단."
  exit 1
fi

cd "$PROJECT_ROOT" || { log "ERROR: cd 실패"; exit 1; }

# 2. 원격 최신화
#    [2026-06-15] 런타임 산출물(fetch/build 가 매번 재생성하는 git-tracked JSON)을 pull 전 정리.
#    이들이 로컬·원격 양쪽에서 동시 변경돼 autostash pop 충돌 → 6/12~ launchd 연속 중단 사고
#    (로그 "작업 폴더를 정방향 진행할 수 없습니다"). step 3 빌드가 어차피 재생성하므로 폐기 안전.
git checkout -- web/src/data/ \
  knowledge-base/macro/fred_snapshot.json \
  knowledge-base/market/fear_greed.json \
  knowledge-base/market/regime.json \
  knowledge-base/portfolio/insider_signals.json 2>/dev/null || true

export GIT_TERMINAL_PROMPT=0
log "git pull --rebase --autostash origin main (timeout 120s)"
if ! timeout 120 git pull --rebase --autostash origin main 2>&1; then
  # 충돌/타임아웃 — 진행 중 rebase·stash 잔재 정리 후 로컬 데이터로 계속 (픽은 로컬 analysis/ 기반
  # 결정적 생성, 최종 push 가 원격 동기화). signals_update.sh·algo_portfolio_sync.sh 와 동일 패턴.
  log "WARN: git pull 실패/타임아웃 — 작업트리 복구 후 로컬 데이터로 빌드 계속"
  git rebase --abort 2>/dev/null || true
  git checkout -- web/src/data/ knowledge-base/ 2>/dev/null || true
  notify_fail "daily_pick git pull 실패 — 로컬 데이터로 진행 (다음 회차 재동기화)"
fi

# 3. daily_pick.json + kb.json 재빌드 (past 필터 매일 재계산 — economic_calendar 등)
log "build_daily_pick.mjs + build_kb.mjs 실행"
cd web || { log "ERROR: web/ cd 실패"; exit 0; }
if ! node scripts/build_daily_pick.mjs 2>&1; then
  log "ERROR: build_daily_pick 실패 — deploy 중단 (silent corruption 차단)"
  notify_fail "build_daily_pick.mjs 실패 — 오늘 픽 미갱신"
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
# [v3.32] 로테이션 이력 동반 커밋 — 미커밋 시 Vercel 컨테이너 재빌드마다 픽이 굴러가는 버그
git add web/src/data/daily_pick.json web/src/data/daily_pick_history.json
if ! git commit -m "chore(daily_pick): 자동 갱신 ${PICK_DATE} — ${PICK_TICKER} ${PICK_SCORE}점 ${PICK_GRADE} (launchd)"; then
  log "ERROR: git commit 실패"
  notify_fail "git commit 실패 — 픽은 생성됐으나 미발행"
  exit 0
fi

log "git push origin main"
if ! git push origin main 2>&1; then
  log "ERROR: git push 실패 — 다음 회차에 재시도"
  notify_fail "git push 실패 — 사이트 미반영 (다음 회차 재시도)"
  exit 0
fi

# 7. deploy 두 채널
# [2026-06-12] timeout 가드 — GitHub 플래그 기간 Vercel Blocked + 행 실측 (행이 Cloudflare 단계를 막음)
log "vercel --prod --yes (timeout 160s)"
if timeout 160 vercel --prod --yes < /dev/null 2>&1; then
  log "Vercel 배포 완료"
else
  log "WARN: Vercel 배포 실패"
  notify_fail "Vercel 배포 실패 — 본서버 stale 가능성"
fi

log "bash scripts/deploy_cloudflare.sh"
if bash scripts/deploy_cloudflare.sh 2>&1; then
  log "Cloudflare 배포 완료"
else
  log "WARN: Cloudflare 배포 실패"
  notify_fail "Cloudflare 배포 실패 — 미러 stale (단독 재실행 가능)"
fi

log "=== 완료 ($PICK_TICKER ${PICK_SCORE}점) ==="
exit 0
