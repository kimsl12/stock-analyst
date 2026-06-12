#!/usr/bin/env python3
"""
build_sector_map.py — 매매 엔진용 종목 섹터 맵 구축 (algo-trading/data/sector_map.json)

엔진 요청 (2026-06-12): stock_scores.json 에 sector 필드 — 레짐별 비우호 섹터 차단용
(예: Stagflation 레짐에서 Tech 차단). 엔진 분류 체계 11종으로 정규화:
    Tech / Discretionary / Financials / Utilities / Staples / Energy /
    Materials / Industrials / Gold / Healthcare / REIT
광범위 인덱스·채권 ETF 는 null (= 엔진 "섹터 미상 → 중립 통과" — 의도된 동작).

소스: yfinance (US: GICS sector / KRX: {티커}.KS) + ETF 수동 오버라이드 표.
캐시: 한 번 조회한 티커는 재조회 안 함 (섹터는 사실상 불변) — --refresh 로 강제 갱신.

사용:
    python3 scripts/build_sector_map.py                 # 전체 (캐시 미스만 조회)
    python3 scripts/build_sector_map.py --missing-only  # 동일 (별칭 — signals_update 가 매일 호출)
    python3 scripts/build_sector_map.py --refresh       # 전체 재조회
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / "analysis/_history"
OUT = ROOT / "algo-trading/data/sector_map.json"

KST = timezone(timedelta(hours=9))

# GICS(yfinance) → 엔진 분류 11종
GICS_MAP = {
    "Technology": "Tech",
    "Communication Services": "Tech",  # GOOGL/META — 레짐 반응이 Tech 와 동행
    "Consumer Cyclical": "Discretionary",
    "Consumer Defensive": "Staples",
    "Financial Services": "Financials",
    "Basic Materials": "Materials",
    "Real Estate": "REIT",
    "Healthcare": "Healthcare",
    "Energy": "Energy",
    "Industrials": "Industrials",
    "Utilities": "Utilities",
}

# ETF·특수 종목 수동 오버라이드 (yfinance ETF 는 sector 미제공)
# null = 광범위 인덱스/채권 — 엔진이 "중립 통과" 처리 (의도)
ETF_OVERRIDES = {
    "BRKB": "Financials",  # yfinance 심볼은 BRK-B — 직접 매핑 (Berkshire)
    "GLD": "Gold", "IAU": "Gold",
    "SLV": "Materials",
    "QQQ": "Tech", "TQQQ": "Tech", "SOXX": "Tech", "SOXL": "Tech", "SOXS": "Tech",
    "XLE": "Energy",
    "VOO": None, "SPY": None, "RSP": None, "DIA": None, "IWM": None,
    "VEA": None, "EWY": None, "USMV": None, "QUAL": None, "VIG": None,
    "SCHD": None, "JEPI": None, "JEPQ": None,
    "AGG": None, "TLT": None, "TIP": None, "SGOV": None,
}


def universe() -> list:
    tickers = []
    for f in HISTORY.glob("*_timeline.json"):
        try:
            tl = json.loads(f.read_text())
        except Exception:
            continue
        t = tl.get("ticker")
        if t and (tl.get("history") or []):
            tickers.append(str(t))
    return sorted(set(tickers))


def fetch_sector(ticker: str):
    """yfinance 조회 → (엔진 라벨 | None, 원시 라벨, 소스)."""
    import yfinance as yf

    if ticker.upper() in ETF_OVERRIDES:
        return ETF_OVERRIDES[ticker.upper()], "ETF override", "manual"

    symbols = [f"{ticker}.KS", f"{ticker}.KQ"] if ticker.isdigit() else [ticker]
    for sym in symbols:
        try:
            info = yf.Ticker(sym).info or {}
            raw = info.get("sector")
            qt = info.get("quoteType", "")
            if not raw and qt == "ETF":
                return None, f"ETF ({info.get('category', '미분류')})", "yfinance"
            if raw:
                return GICS_MAP.get(raw), raw, "yfinance"
        except Exception:
            continue
    return None, None, "miss"


def main() -> None:
    refresh = "--refresh" in sys.argv

    cache = {}
    if OUT.exists() and not refresh:
        try:
            cache = json.loads(OUT.read_text()).get("map", {})
        except Exception:
            cache = {}

    tickers = universe()
    todo = [t for t in tickers if t not in cache]
    print(f"[sector_map] 유니버스 {len(tickers)}종 / 캐시 {len(cache)} / 조회 대상 {len(todo)}")

    for i, t in enumerate(todo):
        sector, raw, source = fetch_sector(t)
        cache[t] = {"sector": sector, "sector_raw": raw, "source": source}
        mark = sector or ("통과(null)" if source != "miss" else "미상")
        print(f"  [{i+1}/{len(todo)}] {t:8} → {mark}" + (f" ({raw})" if raw and raw != "ETF override" else ""))

    mapped = sum(1 for v in cache.values() if v.get("sector"))
    nul = sum(1 for v in cache.values() if v.get("sector") is None and v.get("source") != "miss")
    miss = sum(1 for v in cache.values() if v.get("source") == "miss")
    OUT.write_text(json.dumps({
        "generated_at": datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST"),
        "doc": "엔진 분류 11종 (Tech/Discretionary/Financials/Utilities/Staples/Energy/Materials/Industrials/Gold/Healthcare/REIT). null = 광범위 인덱스·채권 → 엔진 중립 통과.",
        "map": dict(sorted(cache.items())),
    }, ensure_ascii=False, indent=2) + "\n")
    print(f"[sector_map] 저장 — 섹터 확정 {mapped} / 의도적 null {nul} / 미상 {miss} → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
