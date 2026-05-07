#!/usr/bin/env bash
# Cloudflare Pages 배포 스크립트
# GitHub Actions 차단(Ticket 4287825) 대응 — gh-pages 우회
# 사용: bash scripts/deploy_cloudflare.sh

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$REPO_ROOT"

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
mkdir -p "$DEPLOY_DIR/reports" "$DEPLOY_DIR/reports/briefing" "$DEPLOY_DIR/reports/analyst/items"

# 2. HTML 복사 (nullglob 으로 빈 디렉토리 대응)
shopt -s nullglob
stock_files=(reports/*.html)
brief_files=(reports/briefing/*.html)
shopt -u nullglob

if [ ${#stock_files[@]} -gt 0 ]; then
  cp -f "${stock_files[@]}" "$DEPLOY_DIR/reports/"
fi
if [ ${#brief_files[@]} -gt 0 ]; then
  cp -f "${brief_files[@]}" "$DEPLOY_DIR/reports/briefing/"
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
"$PYTHON" "$SCRIPT_DIR/build_analyst_index.py"
# build_analyst_index 가 reports/analyst/index.html 을 갱신하므로 deploy_dir 에도 복사
if [ -f "reports/analyst/index.html" ]; then
  cp -f reports/analyst/index.html "$DEPLOY_DIR/reports/analyst/" 2>/dev/null || true
fi

echo "==> 메인 인덱스 생성 (3컬럼)"
"$PYTHON" "$SCRIPT_DIR/build_main_index.py" "$DEPLOY_DIR"

# 6. 통계
stock_count=$(find "$DEPLOY_DIR/reports" -maxdepth 1 -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
brief_count=$(find "$DEPLOY_DIR/reports/briefing" -maxdepth 1 -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
analyst_count=$(find "$DEPLOY_DIR/reports/analyst/items" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
echo "==> 패키지 준비 완료: 종목 ${stock_count}개 + 브리핑 ${brief_count}개 + 애널리스트 ${analyst_count}건"

# 7. wrangler 배포
cd "$REPO_ROOT"
TIMESTAMP=$(date '+%Y%m%d_%H%M')
echo "==> wrangler pages deploy 실행 (commit: $TIMESTAMP)"
wrangler pages deploy "$DEPLOY_DIR" \
  --project-name="$PROJECT_NAME" \
  --branch=main \
  --commit-message="manual sync $TIMESTAMP"

echo ""
echo "==> 배포 완료"
echo "    https://${PROJECT_NAME}.pages.dev/"
