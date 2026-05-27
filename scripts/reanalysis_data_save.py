#!/usr/bin/env python3
"""재분석 2026-05-28 — 10종 data.json 일괄 생성"""
import json, os, subprocess, sys
from datetime import datetime

TICKERS = [
    ("WMT", "Walmart"),
    ("V", "Visa"),
    ("VZ", "Verizon"),
    ("T", "ATT"),
    ("TXN", "TexasInstruments"),
    ("TTE", "TotalEnergies"),
    ("SCHD", "SchwabUSDividendEquity"),
    ("SAP", "SAP"),
    ("PG", "PG"),
    ("PEP", "PepsiCo"),
]

# fetch_price 호출 후 JSON 캡처
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
        sys.exit(1)
    json_text = out[start + len("JSON_OUTPUT_START"):end].strip()
    return json.loads(json_text)


def main():
    all_tickers = [t for t, _ in TICKERS]
    data_list = fetch_batch(all_tickers)
    data_by_t = {d["ticker"]: d for d in data_list}

    for ticker, name in TICKERS:
        d = data_by_t.get(ticker)
        if d is None:
            print(f"⚠️ {ticker}: fetch 실패")
            continue
        out_dir = f"analysis/{ticker}_{name}_v4"
        os.makedirs(out_dir, exist_ok=True)
        # 보강: 회차 메타
        d["reanalysis_meta"] = {
            "version": "v4",
            "previous_version": "v3",
            "blind_mode": True,
            "previous_files_read": 0,
            "reanalysis_date": "2026-05-28",
            "threshold_days": 14,
            "session_run": "20260528"
        }
        with open(f"{out_dir}/data.json", "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"✅ {ticker}: data.json → {out_dir}/")


if __name__ == "__main__":
    main()
