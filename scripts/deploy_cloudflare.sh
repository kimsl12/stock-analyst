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

echo "==> Cloudflare Pages 배포 시작"
echo "    repo:       $REPO_ROOT"
echo "    deploy_dir: $DEPLOY_DIR"
echo "    project:    $PROJECT_NAME"

# 1. 임시 디렉토리 초기화
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR/reports" "$DEPLOY_DIR/reports/briefing"

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

# 3. 테스트 파일 정리
rm -f "$DEPLOY_DIR"/reports/*_test.html 2>/dev/null || true

# 4. .nojekyll (호환성)
touch "$DEPLOY_DIR/.nojekyll"

# 5. index.html 생성
cd "$DEPLOY_DIR"
cat > index.html <<'INDEXEOF'
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Stock Analyst Reports</title>
<style>
:root{--bg:#0F1923;--card:#1A2733;--text:#E8EAED;--sub:#9AA0A6;--blue:#42A5F5;--buy:#26A69A;--border:#2D3A45}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:24px;max-width:1100px;margin:0 auto}
h1{font-size:24px;margin-bottom:4px}
.sub{color:var(--sub);font-size:14px;margin-bottom:20px}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline;opacity:0.85}
.columns{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start}
.col h2{font-size:16px;margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid var(--border);color:var(--sub)}
.col-stock h2{color:var(--blue)}
.col-brief h2{color:var(--buy)}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:12px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;transition:border-color 0.2s}
.card:hover{border-color:var(--blue)}
.card .name{font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .date{color:var(--sub);font-size:12px;flex-shrink:0;margin-left:8px}
.count{color:var(--sub);font-size:13px;margin-left:8px}
@media(max-width:700px){.columns{grid-template-columns:1fr}body{padding:12px}}
</style>
</head>
<body>
<h1>Stock Analyst Reports</h1>
<p class="sub">AI 종합 분석 리포트 — Cloudflare Pages 자동 배포</p>
<div class="columns">
<div class="col col-stock">
<h2>종목 분석</h2>
INDEXEOF

# 종목 카드 (날짜 내림차순)
for f in $(ls reports/*.html 2>/dev/null | while read fp; do
  d=$(basename "$fp" | grep -oE '[0-9]{8}' | head -1)
  echo "${d:-00000000} $fp"
done | sort -k1,1rn | awk '{print $2}'); do
  fname=$(basename "$f")
  fdate=$(echo "$fname" | grep -oE '[0-9]{8}' | head -1)
  dispdate=""
  if [ -n "$fdate" ]; then
    dispdate="${fdate:0:4}-${fdate:4:2}-${fdate:6:2}"
  fi
  dispname=$(echo "$fname" | sed 's/\.html$//')
  echo "<div class=\"card\"><a class=\"name\" href=\"$f\">$dispname</a><span class=\"date\">$dispdate</span></div>" >> index.html
done

echo '</div><div class="col col-brief"><h2>브리핑</h2>' >> index.html

# 브리핑 카드
if ls reports/briefing/*.html 1>/dev/null 2>&1; then
  for f in $(ls reports/briefing/*.html 2>/dev/null | while read fp; do
    d=$(basename "$fp" | grep -oE '[0-9]{8}' | head -1)
    echo "${d:-00000000} $fp"
  done | sort -k1,1rn | awk '{print $2}'); do
    fname=$(basename "$f")
    dispname=$(echo "$fname" | sed 's/\.html//' | sed 's/_/ /g')
    echo "<div class=\"card\"><a class=\"name\" href=\"$f\">$dispname</a></div>" >> index.html
  done
else
  echo '<p style="color:var(--sub);font-size:13px">브리핑 리포트가 없습니다.</p>' >> index.html
fi

echo '</div></div></body></html>' >> index.html

# 6. 통계 출력
stock_count=$(ls reports/*.html 2>/dev/null | wc -l | tr -d ' ')
brief_count=$(ls reports/briefing/*.html 2>/dev/null | wc -l | tr -d ' ')
echo "==> 패키지 준비 완료: 종목 ${stock_count}개 + 브리핑 ${brief_count}개"

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
