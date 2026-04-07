#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F-10 마이그레이션 스크립트 — knowledge-db/market/*.jsonl → 연도별 4종 .md

명세 (briefing_pipeline.md §4 / market-data-collector.md):
    knowledge-db/market/
    ├── 2026_daily_prices.md         ← snapshot 행
    ├── 2026_economic_indicators.md  ← calendar 행
    ├── 2026_correlation_log.md      ← (correlation-monitor 갱신, 본 스크립트는 헤더만)
    └── 2026_guru_changes.md         ← guru_13f 행

사용법:
    python scripts/migrate_market_jsonl_to_md.py

동작:
    1. knowledge-db/market/*.jsonl 전부 읽어 type 별 분류
    2. 연도별로 4종 .md 파일에 표 행으로 append (없으면 헤더부터 생성)
    3. 처리한 .jsonl 은 knowledge-db/market/_archive/ 로 이동
    4. confidence: none / value: null 인 행도 보존 (수집 실패 이력)

재실행 안전성: 같은 (date, key) 행이 이미 .md 에 있으면 skip.
"""
from __future__ import annotations

import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MARKET_DIR = REPO_ROOT / "knowledge-db" / "market"
ARCHIVE_DIR = MARKET_DIR / "_archive"

FILES = {
    "daily_prices": MARKET_DIR / "2026_daily_prices.md",
    "economic_indicators": MARKET_DIR / "2026_economic_indicators.md",
    "guru_changes": MARKET_DIR / "2026_guru_changes.md",
    "correlation_log": MARKET_DIR / "2026_correlation_log.md",
}

HEADERS = {
    "daily_prices": (
        "| 일자 | 카테고리 | 키 | 종가/현재 | 일간 변동률 | 단위 | 출처 | 수집시각 | Alert |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
    ),
    "economic_indicators": (
        "| 발표일자 | 지역 | 지표 | 컨센서스 | 실제 | 서프라이즈 | 시장 반응 | 출처 |\n"
        "|---|---|---|---|---|---|---|---|\n"
    ),
    "guru_changes": (
        "| 갱신일 | 투자자 | 종목 | 분기 | 포지션일 | 공시일 | 액션 | 이전 비중 | 새 비중 | 출처 |\n"
        "|---|---|---|---|---|---|---|---|---|---|\n"
    ),
    "correlation_log": (
        "| 갱신일 | 페어 | 90D 상관 | Z-score | Alert | 출처 |\n"
        "|---|---|---|---|---|---|\n"
    ),
}

WRITERS = {
    "daily_prices": "market-data-collector",
    "economic_indicators": "market-data-collector",
    "guru_changes": "market-data-collector",
    "correlation_log": "correlation-monitor",
}

READERS = "briefing-lead, global-macro-analyst, correlation-monitor, briefing-report-generator"


def frontmatter(kind: str, year: int) -> str:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    return (
        f"---\n"
        f"file: {year}_{kind}\n"
        f"year: {year}\n"
        f"created: {today}\n"
        f"write_owner: {WRITERS[kind]}\n"
        f"read_owners: [{READERS}]\n"
        f"type: time_series\n"
        f"---\n\n"
        f"> **쓰기 권한:** {WRITERS[kind]}\n"
        f"> **읽기 권한:** {READERS}\n"
        f"> **목적:** {year}년 시장 {kind.replace('_', ' ')} 시계열 영구 축적 (append-only).\n"
        f"> **마이그레이션:** {today} `scripts/migrate_market_jsonl_to_md.py` 로 기존 .jsonl 변환.\n\n"
        f"# {year} {kind.replace('_', ' ').title()}\n\n"
    )


def fmt(v) -> str:
    """null/None → '—', 그 외는 문자열."""
    if v is None or v == "":
        return "—"
    return str(v)


def row_daily(rec: dict) -> str:
    return (
        f"| {fmt(rec.get('date'))} "
        f"| {fmt(rec.get('category'))} "
        f"| {fmt(rec.get('key'))} "
        f"| {fmt(rec.get('value'))} "
        f"| {fmt(rec.get('change_pct') or rec.get('change_bp'))} "
        f"| {fmt(rec.get('unit'))} "
        f"| {fmt(rec.get('source'))} "
        f"| {fmt(rec.get('captured_at'))} "
        f"| {fmt(rec.get('note') or rec.get('alert'))} |\n"
    )


def row_calendar(rec: dict) -> str:
    return (
        f"| {fmt(rec.get('event_date') or rec.get('date'))} "
        f"| {fmt(rec.get('region'))} "
        f"| {fmt(rec.get('indicator'))} "
        f"| {fmt(rec.get('consensus'))} "
        f"| {fmt(rec.get('actual'))} "
        f"| {fmt(rec.get('importance'))} "
        f"| {fmt(rec.get('note'))} "
        f"| {fmt(rec.get('source'))} |\n"
    )


def row_guru(rec: dict) -> str:
    return (
        f"| {fmt(rec.get('date'))} "
        f"| {fmt(rec.get('investor'))} "
        f"| {fmt(rec.get('ticker'))} "
        f"| {fmt(rec.get('quarter'))} "
        f"| {fmt(rec.get('position_date'))} "
        f"| {fmt(rec.get('disclosure_date'))} "
        f"| {fmt(rec.get('action'))} "
        f"| {fmt(rec.get('prev_weight'))} "
        f"| {fmt(rec.get('new_weight'))} "
        f"| {fmt(rec.get('source') or rec.get('note'))} |\n"
    )


TYPE_MAP = {
    "snapshot": ("daily_prices", row_daily),
    "calendar": ("economic_indicators", row_calendar),
    "guru_13f": ("guru_changes", row_guru),
}


def parse_year(rec: dict) -> int:
    raw = rec.get("date") or rec.get("event_date") or rec.get("week_of") or ""
    try:
        return int(str(raw)[:4])
    except (TypeError, ValueError):
        return datetime.utcnow().year


def load_existing_keys(path: Path) -> set[str]:
    """이미 파일에 있는 행의 (1열|3열) 시그니처 set 반환 — 중복 방지."""
    if not path.exists():
        return set()
    keys = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|") and "---" not in line and "일자" not in line and "발표일자" not in line and "갱신일" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 3:
                keys.add(f"{cells[0]}|{cells[2]}")
    return keys


def main() -> int:
    if not MARKET_DIR.exists():
        print(f"[error] not found: {MARKET_DIR}", file=sys.stderr)
        return 1

    jsonl_files = sorted(MARKET_DIR.glob("*.jsonl"))
    if not jsonl_files:
        print("[info] no .jsonl to migrate.")
        return 0

    # type → year → list[row_str]
    buckets: dict[str, dict[int, list[str]]] = defaultdict(lambda: defaultdict(list))
    skipped_changelog = 0

    for jf in jsonl_files:
        for ln, raw in enumerate(jf.read_text(encoding="utf-8").splitlines(), 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                rec = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"[warn] {jf.name}:{ln} JSON 파싱 실패 — {e}", file=sys.stderr)
                continue
            t = rec.get("type")
            if t == "changelog":
                skipped_changelog += 1
                continue
            mapped = TYPE_MAP.get(t)
            if not mapped:
                print(f"[warn] {jf.name}:{ln} unknown type={t} skipped", file=sys.stderr)
                continue
            kind, row_fn = mapped
            year = parse_year(rec)
            buckets[kind][year].append(row_fn(rec))

    # write to .md (append, 중복 제거)
    written = 0
    for kind, by_year in buckets.items():
        for year, rows in by_year.items():
            target = MARKET_DIR / f"{year}_{kind}.md"
            existing_keys = load_existing_keys(target)

            if not target.exists():
                target.write_text(frontmatter(kind, year) + HEADERS[kind], encoding="utf-8")

            with target.open("a", encoding="utf-8") as f:
                for r in rows:
                    cells = [c.strip() for c in r.strip("\n").strip("|").split("|")]
                    sig = f"{cells[0]}|{cells[2]}" if len(cells) >= 3 else r
                    if sig in existing_keys:
                        continue
                    f.write(r)
                    existing_keys.add(sig)
                    written += 1

    # correlation_log: 빈 헤더 파일만 생성 (correlation-monitor 가 추후 갱신)
    for year in {y for by_year in buckets.values() for y in by_year}:
        target = MARKET_DIR / f"{year}_correlation_log.md"
        if not target.exists():
            target.write_text(frontmatter("correlation_log", year) + HEADERS["correlation_log"], encoding="utf-8")

    # archive 처리한 .jsonl
    ARCHIVE_DIR.mkdir(exist_ok=True)
    moved = 0
    for jf in jsonl_files:
        dest = ARCHIVE_DIR / jf.name
        shutil.move(str(jf), str(dest))
        moved += 1

    print(f"[ok] rows written: {written}")
    print(f"[ok] changelog skipped: {skipped_changelog}")
    print(f"[ok] jsonl archived: {moved} → {ARCHIVE_DIR.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
