#!/usr/bin/env bash
# 브리핑 커밋·푸시 스크립트
#
# 목적: briefing-lead 워크플로 마지막 단계(자동 commit/push)를 스크립트로 고정.
#       권한 정책으로 main 직접 푸시가 차단될 때를 대비해 feature branch + PR 폴백을 내장.
#
# 사용법:
#   scripts/briefing_commit.sh <type> [YYYYMMDD]
#
#   예) scripts/briefing_commit.sh evening 20260421
#       scripts/briefing_commit.sh morning
#       scripts/briefing_commit.sh weekly 20260418
#
# 동작:
#   1. 지정된 브리핑 관련 파일들을 stage
#   2. commit (이미 커밋된 상태면 skip)
#   3. main 직접 push 시도 → 성공 시 종료
#   4. 실패 시 feature branch(briefing/{type}-{date})로 전환, push, gh pr create

set -euo pipefail

# ── 인자 파싱 ─────────────────────────────────────────
TYPE="${1:-}"
DATE="${2:-$(date +%Y%m%d)}"

if [[ -z "$TYPE" ]]; then
    echo "Usage: $0 <type> [YYYYMMDD]" >&2
    echo "  type: morning | evening | weekly | crypto | rebalancing | model_portfolio | global_intelligence | performance_review | user_portfolio" >&2
    exit 64
fi

# ── 리포지토리 루트 이동 ─────────────────────────────
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# ── 한국어 강제 안전망 [v3.30] — 발행 직전 매핑 자동 치환 (generator 가 건너뛰었어도 여기서 잡힘)
HTML_FILE="reports/briefing/${TYPE}_${DATE}.html"
if [[ -f "$HTML_FILE" ]]; then
    if ! python3 scripts/check_korean.py --fix "$HTML_FILE"; then
        echo "[warn] 한국어 검증 FAIL (영어 산문 잔존) — 발행은 진행, 알림 발송"
        bash scripts/notify.sh "한국어 검증 실패" "${TYPE}_${DATE} 매핑 외 영어 잔존 — 본문 재작성 필요" || true
    fi
fi

# ── 확신 라벨 게이트 [v3.36] — 역캘리브레이션 교정 (실측: 높음 14.3% < 중간 60.0%)
#    확신 높음 남발 + 반증 트리거 누락을 발행 시점에 기계 검사 (briefing-lead §확신 라벨 산정 룰)
if ! python3 scripts/check_confidence.py; then
    echo "[warn] 확신 라벨 게이트 FAIL — 발행은 진행, 알림 발송"
    bash scripts/notify.sh "확신 라벨 게이트 실패" "${TYPE}_${DATE} 확신 높음 남발/반증 트리거 누락 — 산정 체크리스트 재적용 필요" || true
fi

# ── 처방 → 목표 비중 동기화 [v3.37] — /내포트폴리오 산출물의 "## 목표 비중" 블록을
#    portfolio_targets.json 에 반영 (드리프트 감시·웹 표시가 처방을 자동 추종)
if [[ "$TYPE" == "user_portfolio" ]]; then
    if ! python3 scripts/sync_portfolio_targets.py; then
        echo "[warn] 목표 비중 동기화 실패 (검증 거부) — 발행은 진행, 알림 발송"
        bash scripts/notify.sh "목표 비중 동기화 실패" "${TYPE}_${DATE} 목표 비중 블록 검증 거부 — 기존 targets 유지" || true
    fi
fi

# ── 스테이지 ─────────────────────────────────────────
echo "→ staging briefing artifacts ($TYPE $DATE)"
git add \
    "reports/briefing/" \
    "scripts/portfolio_targets.json" \
    "knowledge-base/portfolio/" \
    "knowledge-base/market/" \
    "knowledge-base/_index.md" \
    "knowledge-db/market/" \
    "knowledge-db/performance/" \
    2>/dev/null || true

# ── 커밋 (있으면) ─────────────────────────────────────
if git diff --cached --quiet; then
    echo "[info] stage된 변경 없음 → 기존 로컬 커밋만 push 시도"
else
    DATE_FMT="${DATE:0:4}-${DATE:4:2}-${DATE:6:2}"
    git commit -m "feat(briefing): ${TYPE} 브리핑 ${DATE_FMT}"
    echo "[ok] 커밋 완료: $(git rev-parse --short HEAD)"
fi

# ── Push 전략: main 직접 시도 → 실패 시 feature branch + PR ─
CUR_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ "$CUR_BRANCH" == "main" ]]; then
    echo "→ 1차: main 직접 push 시도"
    if git push origin main 2>&1 | tee /tmp/briefing-push-main.log; then
        echo "[ok] main push 성공 — $(git rev-parse --short HEAD)"
        # 브리핑 발행 알림 (macOS 알림센터)
        bash "$REPO_ROOT/scripts/notify.sh" "브리핑 발행: ${TYPE}" \
            "${DATE} ${TYPE} 브리핑 push 완료 — 배포 후 사이트 반영" || true
        exit 0
    fi

    echo "[warn] main push 실패 → feature branch + PR 폴백"
    BRANCH="briefing/${TYPE}-${DATE}"

    # 이미 해당 브랜치가 있으면 -N 접미 추가
    if git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
        N=1
        while git rev-parse --verify "${BRANCH}-${N}" >/dev/null 2>&1; do
            N=$((N+1))
        done
        BRANCH="${BRANCH}-${N}"
    fi

    echo "→ feature branch 생성: $BRANCH"
    git checkout -b "$BRANCH"
    git push -u origin "$BRANCH"

    if command -v gh >/dev/null 2>&1; then
        echo "→ PR 생성"
        gh pr create \
            --base main \
            --head "$BRANCH" \
            --title "feat(briefing): ${TYPE} 브리핑 ${DATE}" \
            --body "$(cat <<EOF
자동 생성된 ${TYPE} 브리핑 리포트 (${DATE}).

main 직접 푸시가 권한 정책으로 차단되어 feature branch + PR 경로로 전환됨.

## 산출물
- reports/briefing/${TYPE}_${DATE}.html
- knowledge-base/_index.md (최근 핵심 인사이트 append)
- knowledge-base/market/ + knowledge-db/market/ (시장 데이터)

## 리뷰 포인트
- debate-card / contrarian-card 1건 이상 포함 여부
- 13F 시차 경고 보존 여부
- 4종 모델 포트폴리오 방향 누락 없음 여부

🤖 Generated via scripts/briefing_commit.sh
EOF
)"
        echo "[ok] PR 생성 완료"
        gh pr view --web 2>/dev/null || true
    else
        echo "[warn] gh CLI 없음 — 브랜치만 push됨. PR은 수동 생성 필요:"
        echo "    https://github.com/$(git config --get remote.origin.url | sed -E 's|.*github\.com[:/]([^/]+/[^/.]+).*|\1|')/compare/main...${BRANCH}"
    fi

    # main 복귀
    git checkout main
else
    # 이미 feature branch 위에 있음 → 단순 push
    echo "→ 현재 branch: $CUR_BRANCH (feature branch 모드)"
    git push -u origin "$CUR_BRANCH"

    if command -v gh >/dev/null 2>&1; then
        # PR 존재 여부 확인, 없으면 생성
        if ! gh pr view --json number >/dev/null 2>&1; then
            gh pr create \
                --base main \
                --head "$CUR_BRANCH" \
                --title "feat(briefing): ${TYPE} 브리핑 ${DATE}" \
                --body "자동 생성된 ${TYPE} 브리핑 리포트 (${DATE})."
        else
            echo "[info] 이미 PR 존재 → 커밋만 추가됨"
        fi
    fi
fi

echo "[done] 완료"
