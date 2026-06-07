#!/usr/bin/env python3
"""재분석 자동 실행 — 2026-06-08 (10일 임계, 회차) — 10종 data.json 일괄 생성

대상: GLD v5, MUU v2, MU v5, PEP v5, PG v5, RSP v5, SAP v5, SCHD v5, TTE v5, TXN v5
fetch_price.py 라이브 가격(직전 미국 종가) + metadata 결합 → 각 v{N}/data.json 저장.
ANTHROPIC(비상장)은 선정 단계 제외, 11위 TXN 편입 (과거 회차 선례 동일).
"""
import json, os, subprocess, sys
from datetime import datetime

TODAY = "2026-06-08"

# ticker -> (folder, name_ko, name_en, next_v, asset_type, sector, prev_date)
PLAN = {
    "GLD":  ("SPDRGoldShares",          "SPDR 골드셰어",        "SPDR Gold Shares",                5, "ETF",  "Commodity / Gold",                       "2026-05-27"),
    "MUU":  ("DirexionDailyMU2X",       "Direxion MU 2X 레버리지 ETF", "Direxion Daily MU Bull 2X Shares", 2, "ETF",  "Leveraged / Semiconductor (Micron 2X)",  "2026-05-27"),
    "MU":   ("Micron",                  "마이크론 테크놀로지",   "Micron Technology, Inc.",          5, "주식", "Semiconductors / Memory (DRAM·HBM·NAND)", "2026-05-27"),
    "PEP":  ("PepsiCo",                 "펩시코",               "PepsiCo, Inc.",                    5, "주식", "Consumer Staples / Beverages & Snacks",  "2026-05-27"),
    "PG":   ("PG",                      "프록터앤갬블",         "The Procter & Gamble Company",     5, "주식", "Consumer Staples / Household Products",   "2026-05-27"),
    "RSP":  ("InvescoSP500EqualWeight", "인베스코 S&P500 동일가중 ETF", "Invesco S&P 500 Equal Weight ETF", 5, "ETF",  "US Equity / Equal Weight S&P500",        "2026-05-27"),
    "SAP":  ("SAP",                     "SAP",                  "SAP SE (ADR)",                     5, "주식", "Technology / Enterprise Software (ERP·Cloud)", "2026-05-27"),
    "SCHD": ("SchwabUSDividendEquity",  "슈왑 미국 배당주 ETF", "Schwab US Dividend Equity ETF",    5, "ETF",  "US Equity / Dividend",                   "2026-05-27"),
    "TTE":  ("TotalEnergies",           "토탈에너지스",         "TotalEnergies SE (ADR)",           5, "주식", "Energy / Integrated Oil & Gas",          "2026-05-27"),
    "TXN":  ("TexasInstruments",        "텍사스 인스트루먼츠",  "Texas Instruments Incorporated",   5, "주식", "Semiconductors / Analog",                "2026-05-27"),
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
    print(f"=== data.json 생성 — {TODAY} — {len(tickers)}종 ===\n")
    results = fetch_batch(tickers)
    # results: dict ticker -> price dict (또는 list)
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
