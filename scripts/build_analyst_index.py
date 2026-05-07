#!/usr/bin/env python3
"""
Analyst Reports 인덱스 자동 생성기.

reports/analyst/items/*/meta.json 을 모두 읽어 reports/analyst/index.html 을 갱신.
deploy_cloudflare.sh 가 deploy 직전 호출하는 것을 가정.

사용:
    python3 scripts/build_analyst_index.py
"""
from __future__ import annotations

import html
import json
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYST_DIR = REPO / "reports" / "analyst"
ITEMS_DIR = ANALYST_DIR / "items"
INDEX_PATH = ANALYST_DIR / "index.html"


def load_items() -> list[dict]:
    items: list[dict] = []
    if not ITEMS_DIR.exists():
        return items
    for sub in sorted(ITEMS_DIR.iterdir()):
        if not sub.is_dir():
            continue
        meta_path = sub / "meta.json"
        if not meta_path.exists():
            continue
        try:
            with meta_path.open(encoding="utf-8") as f:
                meta = json.load(f)
        except json.JSONDecodeError as exc:
            print(f"[warn] invalid meta.json: {sub.name} ({exc})", file=sys.stderr)
            continue
        meta["_dir"] = sub.name
        items.append(meta)
    items.sort(key=lambda m: (m.get("date", ""), m.get("item_id", "")), reverse=True)
    return items


def fmt_target(meta: dict) -> str:
    name = meta.get("target_name") or meta.get("target") or ""
    code = meta.get("target") or ""
    if name and code and name != code:
        return f"{html.escape(name)} <span class=\"code\">{html.escape(code)}</span>"
    return html.escape(name or code)


def fmt_price(meta: dict) -> str:
    tp = meta.get("target_price")
    cur = meta.get("target_currency") or ""
    prior = meta.get("prior_target_price")
    if tp is None:
        return ""
    pieces = [f"TP {cur}{tp}".strip()]
    if prior:
        delta = ""
        try:
            d = float(tp) - float(prior)
            sign = "+" if d > 0 else ""
            delta = f" ({sign}{d:g} vs prior {prior})"
        except (TypeError, ValueError):
            delta = f" (prior {prior})"
        pieces.append(delta)
    return "".join(pieces)


RATING_KO = {
    "Buy": "매수", "Strong Buy": "적극 매수", "Hold": "보유",
    "Sell": "매도", "Strong Sell": "적극 매도",
    "Overweight": "비중확대", "Underweight": "비중축소",
    "Equal Weight": "중립", "Neutral": "중립",
    "Bullish": "강세", "Bearish": "약세", "N/A": "평가 없음",
}


def rating_ko(rating: str) -> str:
    return RATING_KO.get(rating, rating) if rating else ""


def render_card(meta: dict) -> str:
    item_dir = meta["_dir"]
    summary_href = f"items/{item_dir}/summary.html"
    title = html.escape(meta.get("title") or meta.get("item_id", ""))
    source = html.escape(meta.get("source_full") or meta.get("source") or "")
    date = html.escape(meta.get("date") or "")
    rating = meta.get("rating") or ""
    rating_class = ""
    rl = rating.lower()
    if rl in ("buy", "overweight", "strong buy", "bullish"):
        rating_class = "buy"
    elif rl in ("sell", "underweight", "strong sell", "bearish"):
        rating_class = "sell"
    elif rl in ("hold", "equal weight", "neutral"):
        rating_class = "hold"
    rating_html = (
        f'<span class="rating {rating_class}">{html.escape(rating_ko(rating))}</span>'
        if rating else ""
    )
    target_html = fmt_target(meta)
    price_html = html.escape(fmt_price(meta))
    bullets = meta.get("summary_bullets") or []
    bullet_html = ""
    if bullets:
        first = html.escape(str(bullets[0]))
        bullet_html = f'<p class="lead">{first}</p>'

    return (
        f'<a class="card" href="{summary_href}">'
        f'<div class="row1">'
        f'<span class="src">{source}</span>'
        f'<span class="date">{date}</span>'
        f'</div>'
        f'<div class="row2">'
        f'<span class="target">{target_html}</span>'
        f'{rating_html}'
        f'</div>'
        f'<div class="row3">{title}</div>'
        f'{bullet_html}'
        + (f'<div class="tp">{price_html}</div>' if price_html else "")
        + '</a>'
    )


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Analyst Reports</title>
<style>
:root{{--bg:#0F1923;--card:#1A2733;--text:#E8EAED;--sub:#9AA0A6;--blue:#42A5F5;--buy:#26A69A;--sell:#EF5350;--hold:#FFA726;--border:#2D3A45}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:24px;max-width:1200px;margin:0 auto}}
h1{{font-size:24px;margin-bottom:4px}}
.sub{{color:var(--sub);font-size:14px;margin-bottom:20px}}
.back{{display:inline-block;color:var(--blue);font-size:13px;margin-bottom:16px;text-decoration:none}}
.back:hover{{text-decoration:underline}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:14px;text-decoration:none;color:var(--text);transition:border-color 0.2s,transform 0.1s}}
.card:hover{{border-color:var(--blue);transform:translateY(-1px)}}
.row1{{display:flex;justify-content:space-between;font-size:12px;color:var(--sub);margin-bottom:8px}}
.row1 .src{{font-weight:600;color:var(--blue)}}
.row2{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}}
.row2 .target{{font-size:15px;font-weight:600}}
.row2 .target .code{{color:var(--sub);font-size:12px;margin-left:4px}}
.rating{{font-size:11px;padding:2px 8px;border-radius:10px;background:#2D3A45}}
.rating.buy{{background:rgba(38,166,154,0.2);color:var(--buy)}}
.rating.sell{{background:rgba(239,83,80,0.2);color:var(--sell)}}
.rating.hold{{background:rgba(255,167,38,0.2);color:var(--hold)}}
.row3{{font-size:13px;color:var(--text);line-height:1.4;margin-bottom:6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.lead{{font-size:12px;color:var(--sub);line-height:1.4;margin-top:4px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.tp{{font-size:11px;color:var(--sub);margin-top:6px;font-family:ui-monospace,Menlo,monospace}}
.empty{{color:var(--sub);font-size:14px;padding:40px;text-align:center}}
.count{{color:var(--sub);font-size:13px}}
@media(max-width:700px){{body{{padding:12px}}}}
</style>
</head>
<body>
<a class="back" href="../../">← 메인으로</a>
<h1>Analyst Reports</h1>
<p class="sub">애널리스트 리포트 모음 · 총 <span class="count">{count}</span>건 · 마지막 갱신 {updated}</p>
<div class="grid">
{cards}
</div>
</body>
</html>
"""


def main() -> int:
    items = load_items()
    if items:
        cards = "\n".join(render_card(m) for m in items)
    else:
        cards = '<div class="empty">아직 리포트가 없습니다. <code>reports/analyst/incoming/</code> 에 PDF 를 드롭하거나 <code>/애널리스트스크랩</code> 을 실행하세요.</div>'
    updated = datetime.now().strftime("%Y-%m-%d %H:%M KST")
    INDEX_PATH.write_text(
        HTML_TEMPLATE.format(count=len(items), updated=updated, cards=cards),
        encoding="utf-8",
    )
    print(f"[ok] wrote {INDEX_PATH} ({len(items)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
