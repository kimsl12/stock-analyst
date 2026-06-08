#!/usr/bin/env python3
"""재분석 자동 실행 — 2026-06-09 (10일 임계, 상한 10) — 10종 data.json 일괄 생성

대상: MA v5, MRK v5, NVO v5, LLY v6, LVMUY v6, META v6, PLTR v6, SNDK v7, SOXX v3, VOO v5
fetch_price.py 라이브 가격(직전 미국 종가) + metadata 결합 → 각 v{N}/data.json 저장.
ANTHROPIC(비상장, 13일)은 선정 단계 제외(비표준 스코어카드), 11위 VOO(11일) 편입 — 과거 회차 선례 동일.
"""
import json, os, subprocess, sys
from datetime import datetime

TODAY = "2026-06-09"

# ticker -> (folder, name_ko, name_en, next_v, asset_type, sector, prev_date)
PLAN = {
    "MA":    ("Mastercard",           "마스터카드",        "Mastercard Incorporated",         5, "주식", "Financials / Payment Networks", "2026-05-28"),
    "MRK":   ("Merck",                "머크",             "Merck & Co., Inc.",                5, "주식", "Healthcare / Pharmaceuticals", "2026-05-28"),
    "NVO":   ("NovoNordisk",          "노보노디스크",      "Novo Nordisk A/S (ADR)",           5, "주식", "Healthcare / Pharma (GLP-1·Diabetes)", "2026-05-28"),
    "LLY":   ("EliLilly",             "엘리 릴리",         "Eli Lilly and Company",            6, "주식", "Healthcare / Pharma (GLP-1·Obesity)", "2026-05-29"),
    "LVMUY": ("LVMH",                 "LVMH (ADR)",       "LVMH Moet Hennessy Louis Vuitton", 6, "주식", "Consumer Discretionary / Luxury Goods", "2026-05-29"),
    "META":  ("Meta",                 "메타 플랫폼스",      "Meta Platforms, Inc.",             6, "주식", "Communication Services / Social Media·AI", "2026-05-29"),
    "PLTR":  ("Palantir",             "팔란티어",          "Palantir Technologies Inc.",       6, "주식", "Technology / AI·Data Analytics Software", "2026-05-29"),
    "SNDK":  ("Sandisk",              "샌디스크",          "Sandisk Corporation",              7, "주식", "Technology / Semiconductor (NAND Memory)", "2026-05-29"),
    "SOXX":  ("iSharesSemiconductor", "iShares 반도체 ETF", "iShares Semiconductor ETF",        3, "ETF", "ETF / Semiconductor Sector", "2026-05-29"),
    "VOO":   ("VanguardSP500",        "뱅가드 S&P 500 ETF", "Vanguard S&P 500 ETF",             5, "ETF", "ETF / Large-Cap US Equity (Passive Index)", "2026-05-29"),
}


def fetch_batch(tickers):
    proc = subprocess.run(
        ["python3", "scripts/fetch_price.py"] + tickers,
        capture_output=True, text=True
    )
    out = proc.stdout
    start = out.find("JSON_OUTPUT_START")
    end = out.find("JSON_OUTPUT_END")
    if start == -1 or end == -1:
        print("ERROR: JSON markers missing", file=sys.stderr)
        print("STDOUT:", out[:2000], file=sys.stderr)
        print("STDERR:", proc.stderr[:2000], file=sys.stderr)
        sys.exit(1)
    json_text = out[start + len("JSON_OUTPUT_START"):end].strip()
    return json.loads(json_text)


def main():
    tickers = list(PLAN.keys())
    print(f"=== data.json 생성 — {TODAY} (10일 임계) — {len(tickers)}종 ===\n")
    results = fetch_batch(tickers)
    if isinstance(results, list):
        results = {r.get("ticker"): r for r in results}

    ok, fail = [], []
    for ticker in tickers:
        folder, name_ko, name_en, nv, asset_type, sector, prev_date = PLAN[ticker]
        p = results.get(ticker)
        if not p or p.get("error"):
            print(f"  ❌ {ticker}: 가격 수집 실패 — {p.get('error') if p else 'no data'}")
            fail.append(ticker)
            continue
        out_dir = f"analysis/{ticker}_{folder}_v{nv}"
        os.makedirs(out_dir, exist_ok=True)
        data = {
            "metadata": {
                "ticker": ticker,
                "company_name": name_en,
                "company_name_ko": name_ko,
                "analysis_date": TODAY,
                "analysis_version": f"v{nv}",
                "analysis_mode": "BLIND_reanalysis",
                "asset_type": asset_type,
                "sector": sector,
                "currency": p.get("currency", "$"),
                "prev_version_date": prev_date,
            },
            "currency": p.get("currency", "$"),
            "date": p.get("date"),
            "current_price": p.get("current_price"),
            "prev_close": p.get("prev_close"),
            "change_pct": p.get("change_pct"),
            "high_52w": p.get("high_52w"),
            "low_52w": p.get("low_52w"),
            "market_cap": p.get("market_cap"),
            "volume": p.get("volume"),
            "atr_14": p.get("atr_14"),
            "atr_pct": p.get("atr_pct"),
            "stop_loss_2atr": p.get("stop_loss_2atr"),
            "target_3atr": p.get("target_3atr"),
            "fetch_time": p.get("fetch_time", datetime.now().isoformat()),
            "market_cap_str": p.get("market_cap_str"),
        }
        with open(f"{out_dir}/data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[{ticker}] ✅ v{nv} data.json — {p.get('currency','$')}{p.get('current_price')} (ATR {p.get('atr_14')}, {p.get('date')})")
        ok.append(ticker)

    print(f"\n=== 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
