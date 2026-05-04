#!/usr/bin/env python3
"""
build_manifest.py — reports/ 디렉토리 스캔 → web/src/data/manifest.json + web/public/reports/ 복사

PLAN.md §8.3, §10.3 기반.

수행:
1. reports/ 와 reports/briefing/ 모든 *.html 파일 스캔
2. 파일명 패턴으로 type/ticker/date/title 추출
3. web/src/data/manifest.json 생성 (Astro가 빌드 시 import)
4. web/public/reports/ 로 HTML 전량 복사 (Vercel이 정적 서빙)

사용법:
    cd web && python scripts/build_manifest.py
    또는 npm run build (prebuild hook이 자동 호출)
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# 경로
# ---------------------------------------------------------------------------
WEB_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = WEB_DIR.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
OUTPUT_JSON = WEB_DIR / "src" / "data" / "manifest.json"
PUBLIC_REPORTS = WEB_DIR / "public" / "reports"

# ---------------------------------------------------------------------------
# 분류 규칙
# ---------------------------------------------------------------------------
# 한국 ETF prefix (있으면 type='etf')
KR_ETF_PREFIXES = {
    "KODEX", "TIGER", "ACE", "RISE", "SOL", "HANARO",
    "ARIRANG", "PLUS", "KOSEF", "KIWOOM", "KBSTAR", "FOCUS",
}

# briefing 파일명 prefix → 표준 type
BRIEFING_TYPE: dict[str, str] = {
    "morning": "morning",
    "evening": "evening",
    "weekly": "weekly",
    "crypto": "crypto",
    "user_portfolio": "user_portfolio",
    "global_intelligence": "global_intelligence",
    "model_portfolio": "model_portfolio",
    "rebalancing_user": "rebalancing",
    "rebalancing": "rebalancing",
    "daily_briefing": "daily_briefing",  # legacy
}

# 복사 시 제외 패턴
COPY_IGNORE = shutil.ignore_patterns(
    "*.md", ".DS_Store", "._*", ".gitkeep", "*.json"
)


# ---------------------------------------------------------------------------
# 파일명 파서
# ---------------------------------------------------------------------------
RE_BRIEFING = re.compile(r"^([a-z_]+)_(\d{8})\.html$")
RE_STOCK = re.compile(r"^([0-9A-Z][0-9A-Za-z]*)_(.+)_(\d{8})\.html$")


def fmt_date(yyyymmdd: str) -> str:
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}"


def parse_briefing(filename: str) -> dict | None:
    m = RE_BRIEFING.match(filename)
    if not m:
        return None
    raw_type, date_str = m.groups()
    btype = BRIEFING_TYPE.get(raw_type)
    if not btype:
        return None
    return {"type": btype, "ticker": None, "name": None, "date": fmt_date(date_str)}


def parse_stock(filename: str) -> dict | None:
    m = RE_STOCK.match(filename)
    if not m:
        return None
    ticker, name, date_str = m.groups()
    is_etf = ticker.upper() in KR_ETF_PREFIXES
    return {
        "type": "etf" if is_etf else "stock_analysis",
        "ticker": ticker,
        "name": name,
        "date": fmt_date(date_str),
    }


# ---------------------------------------------------------------------------
# HTML title 추출 (첫 8KB만)
# ---------------------------------------------------------------------------
RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def extract_title(html_path: Path) -> str | None:
    try:
        with html_path.open("r", encoding="utf-8", errors="replace") as f:
            chunk = f.read(8192)
    except OSError:
        return None
    m = RE_TITLE.search(chunk)
    if not m:
        return None
    return re.sub(r"\s+", " ", m.group(1)).strip() or None


# ---------------------------------------------------------------------------
# 매니페스트 빌드
# ---------------------------------------------------------------------------
def build_items() -> tuple[list[dict], list[str]]:
    items: list[dict] = []
    warnings: list[str] = []

    if not REPORTS_DIR.exists():
        warnings.append(f"reports/ 미발견: {REPORTS_DIR}")
        return items, warnings

    # 1. reports/briefing/*.html
    briefing_dir = REPORTS_DIR / "briefing"
    if briefing_dir.exists():
        for path in sorted(briefing_dir.glob("*.html")):
            meta = parse_briefing(path.name)
            if not meta:
                warnings.append(f"미인식 briefing 파일명: {path.name}")
                continue
            items.append(
                {
                    **meta,
                    "filename": path.name,
                    "url_path": f"/reports/briefing/{path.name}",
                    "size_bytes": path.stat().st_size,
                    "title": extract_title(path),
                }
            )

    # 2. reports/*.html (루트 = 종목분석/ETF)
    for path in sorted(REPORTS_DIR.glob("*.html")):
        meta = parse_stock(path.name)
        if not meta:
            warnings.append(f"미인식 stock 파일명: {path.name}")
            continue
        items.append(
            {
                **meta,
                "filename": path.name,
                "url_path": f"/reports/{path.name}",
                "size_bytes": path.stat().st_size,
                "title": extract_title(path),
            }
        )

    # 정렬: date desc → filename
    items.sort(key=lambda x: (x["date"], x["filename"]), reverse=True)
    return items, warnings


# ---------------------------------------------------------------------------
# reports/ → web/public/reports/ 복사
# ---------------------------------------------------------------------------
def copy_reports() -> int:
    if not REPORTS_DIR.exists():
        return 0
    if PUBLIC_REPORTS.exists():
        shutil.rmtree(PUBLIC_REPORTS)
    PUBLIC_REPORTS.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(REPORTS_DIR, PUBLIC_REPORTS, ignore=COPY_IGNORE)
    # 복사된 HTML 개수 카운트
    return sum(1 for _ in PUBLIC_REPORTS.rglob("*.html"))


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------
def main() -> int:
    items, warnings = build_items()
    if not items:
        print("WARN: 인덱싱된 리포트 0건 — reports/ 확인 필요", file=sys.stderr)

    # 복사
    copied = copy_reports()

    # manifest.json 출력
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "count": len(items),
        "by_type": _count_by_type(items),
        "items": items,
    }
    OUTPUT_JSON.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 결과 보고
    rel = OUTPUT_JSON.relative_to(PROJECT_ROOT)
    print(f"OK: manifest 생성 ({len(items)} items, {copied} HTMLs copied) → {rel}")
    if warnings:
        print(f"  ({len(warnings)} warnings)", file=sys.stderr)
        for w in warnings[:10]:
            print(f"  WARN: {w}", file=sys.stderr)
        if len(warnings) > 10:
            print(f"  ... ({len(warnings) - 10} more)", file=sys.stderr)
    return 0


def _count_by_type(items: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for it in items:
        out[it["type"]] = out.get(it["type"], 0) + 1
    return out


if __name__ == "__main__":
    sys.exit(main())
