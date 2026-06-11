#!/usr/bin/env python3
"""
analyst_lookup.py — 애널리스트 아카이브에서 특정 티커 관련 최근 항목 조회

reports/analyst/items/*/meta.json 을 스캔하여 target/tags/title 매칭 항목을
날짜 내림차순 마크다운으로 출력. 종목분석 Phase 0-C (data-collector) 가
수집 패키지에 "애널리스트 아카이브" 섹션으로 포함하는 용도.

사용:
    python3 scripts/analyst_lookup.py NVDA              # 기본: 최근 90일, 최대 5건
    python3 scripts/analyst_lookup.py NVDA --days 180 --limit 10
    python3 scripts/analyst_lookup.py 005930            # 한국 종목

매칭 규칙 (우선순위):
    1. meta.target == 티커 (정확)
    2. meta.tags 에 티커 소문자 포함
    3. meta.title 에 티커 단어 포함
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ITEMS_DIR = ROOT / "reports/analyst/items"


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("사용: python3 scripts/analyst_lookup.py TICKER [--days 90] [--limit 5]")
        sys.exit(1)
    ticker = args[0].upper()

    def opt(name: str, default: int) -> int:
        if name in sys.argv:
            return int(sys.argv[sys.argv.index(name) + 1])
        return default

    days = opt("--days", 90)
    limit = opt("--limit", 5)
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    matches = []
    for meta_path in ITEMS_DIR.glob("*/meta.json"):
        try:
            meta = json.loads(meta_path.read_text())
        except Exception:
            continue
        date = meta.get("date") or ""
        if date < cutoff:
            continue
        target = (meta.get("target") or "").upper()
        tags = [str(t).lower() for t in (meta.get("tags") or [])]
        title = meta.get("title") or ""
        if target == ticker:
            rank = 0
        elif ticker.lower() in tags:
            rank = 1
        elif re.search(rf"\b{re.escape(ticker)}\b", title, re.IGNORECASE):
            rank = 2
        else:
            continue
        matches.append((rank, date, meta))

    matches.sort(key=lambda x: (x[0], x[1]), reverse=False)
    # 날짜 내림차순 우선, 정확 매칭 우선
    matches.sort(key=lambda x: x[1], reverse=True)
    matches.sort(key=lambda x: x[0])
    matches = matches[:limit]

    if not matches:
        print(f"## 애널리스트 아카이브 — {ticker}\n\n최근 {days}일 내 관련 항목 없음.")
        return

    print(f"## 애널리스트 아카이브 — {ticker} (최근 {days}일, {len(matches)}건)\n")
    for _, date, m in matches:
        rating = m.get("rating") or "N/A"
        tp = m.get("target_price")
        tp_str = f" · TP {m.get('target_currency', '')} {tp}" if tp else ""
        bullets = m.get("summary_bullets") or []
        first = f" — {bullets[0]}" if bullets else ""
        print(f"- **{date}** [{m.get('source_full', m.get('source', '?'))}] {m.get('title', '')}")
        print(f"  - 의견: {rating}{tp_str}{first}")
        print(f"  - 항목: reports/analyst/items/{m.get('item_id', '')}/ · 출처: {m.get('source_url', '-')}")


if __name__ == "__main__":
    main()
