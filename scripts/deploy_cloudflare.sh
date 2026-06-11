#!/usr/bin/env bash
# Cloudflare Pages 배포 스크립트
# GitHub Actions 차단(Ticket 4287825) 대응 — gh-pages 우회
# 사용: bash scripts/deploy_cloudflare.sh
#
# 인증 우선순위 (v3.22 — 2026-06-01):
#   1. CLOUDFLARE_API_TOKEN 환경변수 (이미 export 됐으면 그대로)
#   2. .env.local (REPO_ROOT) CLOUDFLARE_API_TOKEN= 한 줄 자동 source
#   3. wrangler OAuth (브라우저 로그인 — wrangler login 후 ~/.config/.wrangler/)
#   토큰 발급: https://dash.cloudflare.com/profile/api-tokens
#   필요 권한: Account → Cloudflare Pages:Edit

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$REPO_ROOT"

# .env.local 자동 로드 (CLOUDFLARE_API_TOKEN 등 — secret 파일은 외부 read 금지, source 만 수행)
if [ -f "$REPO_ROOT/.env.local" ] && [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
  set +u
  # shellcheck disable=SC1091
  source "$REPO_ROOT/.env.local"
  set -u
  [ -n "${CLOUDFLARE_API_TOKEN:-}" ] && echo "==> .env.local 에서 CLOUDFLARE_API_TOKEN 로드 완료"
fi

DEPLOY_DIR="/tmp/cf-deploy"
PROJECT_NAME="stock-analyst"

# venv 우선, 없으면 시스템 python3
PYTHON="$REPO_ROOT/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON=$(command -v python3)
fi

echo "==> Cloudflare Pages 배포 시작"
echo "    repo:       $REPO_ROOT"
echo "    deploy_dir: $DEPLOY_DIR"
echo "    project:    $PROJECT_NAME"
echo "    python:     $PYTHON"

# 1. 임시 디렉토리 초기화
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR/reports" "$DEPLOY_DIR/reports/briefing" "$DEPLOY_DIR/reports/research" "$DEPLOY_DIR/reports/analyst/items"

# 2. HTML 복사 (nullglob 으로 빈 디렉토리 대응)
shopt -s nullglob
stock_files=(reports/*.html)
brief_files=(reports/briefing/*.html)
research_files=(reports/research/*.html)
shopt -u nullglob

if [ ${#stock_files[@]} -gt 0 ]; then
  cp -f "${stock_files[@]}" "$DEPLOY_DIR/reports/"
fi
if [ ${#brief_files[@]} -gt 0 ]; then
  cp -f "${brief_files[@]}" "$DEPLOY_DIR/reports/briefing/"
fi
# 2.3 research L3 분기 Deep Dive (있을 때만) [v3.17 — 2026-05-12]
if [ ${#research_files[@]} -gt 0 ]; then
  cp -f "${research_files[@]}" "$DEPLOY_DIR/reports/research/"
fi

# 2.5 애널리스트 리포트 복사 (있을 때만)
if [ -d "reports/analyst/items" ]; then
  # items/{id}/* 모두 복사 (PDF, source.html, summary.html, meta.json)
  cp -r reports/analyst/items/. "$DEPLOY_DIR/reports/analyst/items/" 2>/dev/null || true
fi
if [ -f "reports/analyst/_schema.md" ]; then
  cp -f reports/analyst/_schema.md "$DEPLOY_DIR/reports/analyst/" 2>/dev/null || true
fi

# 3. 테스트 파일 정리
rm -f "$DEPLOY_DIR"/reports/*_test.html 2>/dev/null || true

# 4. .nojekyll
touch "$DEPLOY_DIR/.nojekyll"

# 5. 인덱스 갱신 (Python 스크립트로 분리)
echo "==> 애널리스트 인덱스 갱신"
# 출력을 deploy_dir 로 한정 — repo의 reports/analyst/index.html 은 건드리지 않음 (git 작업 트리 오염 방지)
"$PYTHON" "$SCRIPT_DIR/build_analyst_index.py" "$DEPLOY_DIR/reports/analyst/index.html"

echo "==> 메인 인덱스 생성 (3컬럼)"
"$PYTHON" "$SCRIPT_DIR/build_main_index.py" "$DEPLOY_DIR"

# 6. 통계
stock_count=$(find "$DEPLOY_DIR/reports" -maxdepth 1 -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
brief_count=$(find "$DEPLOY_DIR/reports/briefing" -maxdepth 1 -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
research_count=$(find "$DEPLOY_DIR/reports/research" -maxdepth 1 -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
analyst_count=$(find "$DEPLOY_DIR/reports/analyst/items" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
echo "==> 패키지 준비 완료: 종목 ${stock_count}개 + 브리핑 ${brief_count}개 + 리서치 ${research_count}건 + 애널리스트 ${analyst_count}건"

# 7. wrangler 배포 (1차 시도 실패 시 5초 대기 후 1회 재시도 — v3.22 P1-9)
cd "$REPO_ROOT"
TIMESTAMP=$(date '+%Y%m%d_%H%M')
echo "==> wrangler pages deploy 실행 (commit: $TIMESTAMP)"
if ! wrangler pages deploy "$DEPLOY_DIR" \
  --project-name="$PROJECT_NAME" \
  --branch=main \
  --commit-message="manual sync $TIMESTAMP"; then
  echo "==> wrangler 1차 실패 — 5초 대기 후 재시도"
  sleep 5
  wrangler pages deploy "$DEPLOY_DIR" \
    --project-name="$PROJECT_NAME" \
    --branch=main \
    --commit-message="manual sync $TIMESTAMP (retry)" || {
      echo "==> wrangler 2회 모두 실패 — Vercel 본서버는 영향 없음. 수동 재실행 필요:"
      echo "    bash scripts/deploy_cloudflare.sh"
      exit 1
    }
fi

echo ""
echo "==> 배포 완료"
echo "    https://${PROJECT_NAME}.pages.dev/"
