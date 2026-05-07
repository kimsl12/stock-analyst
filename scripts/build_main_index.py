#!/usr/bin/env python3
"""
Stock Analyst 메인 사이트 index.html 생성기 (3컬럼).

입력 디렉토리:
  reports/*.html              → 종목 분석 컬럼
  reports/briefing/*.html     → 브리핑 컬럼
  reports/analyst/items/*/    → 애널리스트 리포트 컬럼 (최근 N개)

deploy_cloudflare.sh 가 호출. 패키지 디렉토리 (예: /tmp/cf-deploy) 를 인자로 받아
그 위치에서 파일들을 스캔하고 거기 index.html 을 작성한다.

사용:
    python3 scripts/build_main_index.py /tmp/cf-deploy
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

DATE_RE = re.compile(r"(\d{8})")
ANALYST_RECENT = 12  # 메인 컬럼 표시 개수


def date_from_filename(name: str) -> str:
    m = DATE_RE.search(name)
    return m.group(1) if m else "00000000"


def disp_date(yyyymmdd: str) -> str:
    if not yyyymmdd or yyyymmdd == "00000000" or len(yyyymmdd) != 8:
        return ""
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}"


def scan_stock_reports(deploy_root: Path) -> list[tuple[str, str, str]]:
    """returns sorted [(href, dispname, dispdate), ...]"""
    out: list[tuple[str, str, str]] = []
    for f in (deploy_root / "reports").glob("*.html"):
        if f.name == "index.html":
            continue
        d = date_from_filename(f.name)
        out.append((d, f"reports/{f.name}", f.stem))
    out.sort(key=lambda x: x[0], reverse=True)
    return [(href, name, disp_date(d)) for d, href, name in out]


def scan_briefings(deploy_root: Path) -> list[tuple[str, str]]:
    """returns sorted [(href, dispname), ...]"""
    bd = deploy_root / "reports" / "briefing"
    if not bd.exists():
        return []
    out: list[tuple[str, str]] = []
    for f in bd.glob("*.html"):
        d = date_from_filename(f.name)
        out.append((d, f"reports/briefing/{f.name}", f.stem.replace("_", " ")))
    out.sort(key=lambda x: x[0], reverse=True)
    return [(href, name) for _, href, name in out]


def scan_analyst_items(deploy_root: Path, limit: int) -> tuple[list[dict], int]:
    """returns (recent_items, total_count)"""
    items_dir = deploy_root / "reports" / "analyst" / "items"
    if not items_dir.exists():
        return [], 0
    metas: list[dict] = []
    for sub in items_dir.iterdir():
        if not sub.is_dir():
            continue
        mp = sub / "meta.json"
        if not mp.exists():
            continue
        try:
            with mp.open(encoding="utf-8") as f:
                meta = json.load(f)
            meta["_dir"] = sub.name
            metas.append(meta)
        except json.JSONDecodeError:
            continue
    metas.sort(key=lambda m: (m.get("date", ""), m.get("item_id", "")), reverse=True)
    return metas[:limit], len(metas)


def render_stock_column(rows: list[tuple[str, str, str]]) -> str:
    if not rows:
        return '<p class="empty">종목 분석 리포트가 없습니다.</p>'
    pieces = []
    for href, name, dispdate in rows:
        pieces.append(
            f'<div class="card"><a class="name" href="{html.escape(href)}">{html.escape(name)}</a>'
            f'<span class="date">{html.escape(dispdate)}</span></div>'
        )
    return "\n".join(pieces)


def render_brief_column(rows: list[tuple[str, str]]) -> str:
    if not rows:
        return '<p class="empty">브리핑 리포트가 없습니다.</p>'
    pieces = []
    for href, name in rows:
        pieces.append(
            f'<div class="card"><a class="name" href="{html.escape(href)}">{html.escape(name)}</a></div>'
        )
    return "\n".join(pieces)


def render_analyst_column(items: list[dict], total: int) -> str:
    if not items:
        return (
            '<p class="empty">애널리스트 리포트가 아직 없습니다.<br>'
            '<a href="reports/analyst/index.html">전체 페이지 →</a></p>'
        )
    pieces = []
    for m in items:
        item_dir = m["_dir"]
        href = f"reports/analyst/items/{item_dir}/summary.html"
        source = m.get("source_full") or m.get("source") or ""
        target = m.get("target_name") or m.get("target") or ""
        date = m.get("date") or ""
        rating = m.get("rating") or ""
        rating_cls = ""
        rl = rating.lower()
        if rl in ("buy", "overweight", "strong buy"):
            rating_cls = " buy"
        elif rl in ("sell", "underweight", "strong sell"):
            rating_cls = " sell"
        elif rl in ("hold", "equal weight", "neutral"):
            rating_cls = " hold"
        rating_html = (
            f'<span class="rating{rating_cls}">{html.escape(rating)}</span>' if rating else ""
        )
        pieces.append(
            '<div class="card">'
            f'<a class="name" href="{html.escape(href)}">'
            f'<span class="src">{html.escape(source)}</span> · '
            f'<b>{html.escape(target)}</b>'
            "</a>"
            f'<span class="meta">{html.escape(date)} {rating_html}</span>'
            "</div>"
        )
    if total > len(items):
        pieces.append(
            f'<div class="more"><a href="reports/analyst/index.html">전체 {total}건 보기 →</a></div>'
        )
    else:
        pieces.append(
            '<div class="more"><a href="reports/analyst/index.html">애널리스트 페이지 →</a></div>'
        )
    return "\n".join(pieces)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Stock Analyst Reports</title>
<style>
:root{{--bg:#0F1923;--card:#1A2733;--text:#E8EAED;--sub:#9AA0A6;--blue:#42A5F5;--buy:#26A69A;--sell:#EF5350;--hold:#FFA726;--accent:#7C4DFF;--border:#2D3A45}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:24px;max-width:1400px;margin:0 auto}}
h1{{font-size:24px;margin-bottom:4px}}
.sub{{color:var(--sub);font-size:14px;margin-bottom:20px}}
a{{color:var(--blue);text-decoration:none}}
a:hover{{text-decoration:underline;opacity:0.85}}
.columns{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;align-items:start}}
.col h2{{font-size:16px;margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid var(--border);color:var(--sub)}}
.col-stock h2{{color:var(--blue)}}
.col-brief h2{{color:var(--buy)}}
.col-analyst h2{{color:var(--accent)}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:12px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;transition:border-color 0.2s;gap:8px}}
.card:hover{{border-color:var(--blue)}}
.card .name{{font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--text)}}
.card .date{{color:var(--sub);font-size:12px;flex-shrink:0}}
.col-analyst .card{{flex-direction:column;align-items:flex-start}}
.col-analyst .card .name{{display:block;width:100%}}
.col-analyst .card .name .src{{color:var(--accent);font-size:12px;font-weight:700}}
.col-analyst .card .meta{{margin-top:4px;color:var(--sub);font-size:11px;display:flex;gap:8px;align-items:center}}
.col-analyst .rating{{font-size:10px;padding:1px 7px;border-radius:9px;background:#2D3A45}}
.col-analyst .rating.buy{{background:rgba(38,166,154,0.2);color:var(--buy)}}
.col-analyst .rating.sell{{background:rgba(239,83,80,0.2);color:var(--sell)}}
.col-analyst .rating.hold{{background:rgba(255,167,38,0.2);color:var(--hold)}}
.more{{margin-top:8px;font-size:13px}}
.empty{{color:var(--sub);font-size:13px;padding:8px 4px}}
.foot{{margin-top:24px;padding-top:14px;border-top:1px solid var(--border);font-size:11px;color:var(--sub);font-family:ui-monospace,Menlo,monospace}}
@media(max-width:1000px){{.columns{{grid-template-columns:1fr 1fr}}.col-analyst{{grid-column:1/-1}}}}
@media(max-width:700px){{.columns{{grid-template-columns:1fr}}body{{padding:12px}}.col-analyst{{grid-column:auto}}}}
</style>
</head>
<body>
<h1>Stock Analyst Reports</h1>
<p class="sub">AI 종합 분석 리포트 · Cloudflare Pages 자동 배포</p>
<div class="columns">
<div class="col col-stock"><h2>종목 분석 ({stock_count})</h2>
{stock_html}
</div>
<div class="col col-brief"><h2>브리핑 ({brief_count})</h2>
{brief_html}
</div>
<div class="col col-analyst"><h2>애널리스트 리포트 ({analyst_count})</h2>
{analyst_html}
</div>
</div>
<p class="foot">갱신: {updated}</p>
</body>
</html>
"""


def main(deploy_root: Path) -> int:
    stock = scan_stock_reports(deploy_root)
    brief = scan_briefings(deploy_root)
    analyst, analyst_total = scan_analyst_items(deploy_root, ANALYST_RECENT)

    body = HTML_TEMPLATE.format(
        stock_count=len(stock),
        brief_count=len(brief),
        analyst_count=analyst_total,
        stock_html=render_stock_column(stock),
        brief_html=render_brief_column(brief),
        analyst_html=render_analyst_column(analyst, analyst_total),
        updated=datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    )
    out = deploy_root / "index.html"
    out.write_text(body, encoding="utf-8")
    print(f"[ok] wrote {out} (stock={len(stock)} brief={len(brief)} analyst={analyst_total})")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: build_main_index.py <deploy_root>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(Path(sys.argv[1])))
