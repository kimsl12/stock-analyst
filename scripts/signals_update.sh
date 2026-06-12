#!/usr/bin/env bash
#
# signals_update.sh — 알고 매매 엔진용 시그널 일일 빌드 (매일 KST 15:25)
#
# 계약 (algo-trading/algo_engine_handoff.md): 엔진이 매일 15:40 에
# algo-trading/data/{stock_scores,macro_regime,earnings_calendar}.json 을 읽음.
# 그 전에 빌드 완료돼야 함. 신호가 stale 하면 엔진 신선도 게이트가 매매 전면 차단
# (2026-05-19~06-12 24일간 그 상태였음 — 스케줄 자체가 없었던 게 원인).
#
# 동작: git pull → build_signals.mjs → 산출물 sanity 검증 → commit + push → 실패 시 알림
#
# 설치:
#   cp scripts/launchd/com.stockanalyst.signals.plist ~/Library/LaunchAgents/
#   launchctl load ~/Library/LaunchAgents/com.stockanalyst.signals.plist
#
# 수동 테스트: bash scripts/signals_update.sh
#

set -euo pipefail

PROJECT_ROOT="/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
NOTIFY="$PROJECT_ROOT/scripts/notify.sh"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }
notify_fail() { bash "$NOTIFY" "매매 시그널 빌드 실패" "$1" high || true; }

log "=== signals 일일 빌드 시작 ==="

if [ ! -d "$PROJECT_ROOT" ]; then
  osascript -e 'display notification "외장 SSD 미마운트 — 시그널 빌드 불가 (엔진 게이트가 매매 차단함)" with title "매매 시그널 빌드 실패"' || true
  exit 1
fi
cd "$PROJECT_ROOT"

# git pull — 헤드리스 환경 행 방지: 자격증명 프롬프트 차단 + 120초 타임아웃
# (2026-06-12 첫 테스트에서 pull 이 무한 대기 → 15:40 엔진 점검을 넘겨버릴 뻔한 사고)
export GIT_TERMINAL_PROMPT=0
git pull --rebase --autostash origin main 2>&1 &
PULL_PID=$!
PULL_OK=1
for _ in $(seq 1 24); do
  kill -0 "$PULL_PID" 2>/dev/null || break
  sleep 5
done
if kill -0 "$PULL_PID" 2>/dev/null; then
  kill "$PULL_PID" 2>/dev/null || true
  PULL_OK=0
fi
wait "$PULL_PID" 2>/dev/null || PULL_OK=0
if [ "$PULL_OK" -eq 0 ]; then
  log "WARN: git pull 실패/타임아웃 — 로컬 분석 데이터로 빌드 진행 (신호 생성이 우선)"
  notify_fail "signals git pull 실패 — 로컬 데이터로 빌드 진행함"
fi

# 신규 분석 티커의 섹터 증분 조회 (캐시 완비 시 즉시 no-op) [v2.1]
python3 scripts/build_sector_map.py --missing-only 2>&1 | tail -1 || log "WARN: sector_map 갱신 실패 — 기존 맵 사용"

if ! node algo-trading/build_signals.mjs 2>&1; then
  log "ERROR: build_signals 실패"
  notify_fail "build_signals.mjs 실패 — 신호 stale, 15:40 엔진 점검 전 수동 복구 필요"
  exit 1
fi

# sanity: 오늘 날짜 + 최소 종목 수
TODAY=$(TZ=Asia/Seoul date '+%Y-%m-%d')
GEN=$(python3 -c "import json; print(json.load(open('algo-trading/data/stock_scores.json'))['generated_at'][:10])" 2>/dev/null || echo "")
TOTAL=$(python3 -c "import json; print(json.load(open('algo-trading/data/stock_scores.json'))['total_count'])" 2>/dev/null || echo "0")
if [ "$GEN" != "$TODAY" ] || [ "$TOTAL" -lt 50 ]; then
  log "ERROR: sanity 실패 (generated=$GEN, total=$TOTAL)"
  notify_fail "시그널 sanity 실패 (generated=$GEN, total=$TOTAL) — 산출물 검증 필요"
  exit 1
fi
log "sanity OK (generated=$GEN, total=$TOTAL)"

# commit + push (provenance — 엔진은 로컬 파일을 읽으므로 push 실패해도 신호는 유효)
git add algo-trading/data/
if git diff --cached --quiet; then
  log "변경 없음 — commit 스킵"
else
  ELIG=$(python3 -c "import json; print(json.load(open('algo-trading/data/stock_scores.json'))['eligible_count'])" 2>/dev/null || echo "?")
  git commit -m "chore(signals): 매매 시그널 일일 빌드 ${TODAY} — eligible ${ELIG}종 (launchd)" || true
  git push origin main 2>&1 || { log "WARN: push 실패 — 로컬 신호는 유효"; notify_fail "시그널 push 실패 (로컬 신호는 유효 — 다음 회차 재시도)"; }
fi

log "=== 완료 (total=$TOTAL) ==="
exit 0
