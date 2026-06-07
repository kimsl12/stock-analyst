#!/usr/bin/env python3
"""재분석 자동 실행 — 2026-06-08 (회차 2, 7일 임계) — 10종 data.json 일괄 생성

대상: T v5, 010120 v6, 034020 v5, 035720 v5, BA v5, GE v5, GS v6, HD v5, HSBC v5, JNJ v5
fetch_price.py 라이브 가격(직전 미국/한국 종가) + metadata 결합 → 각 v{N}/data.json 저장.
ANTHROPIC(비상장)은 선정 단계 제외, 11위 JNJ 편입 (과거 회차 선례 동일).
"""
import json, os, subprocess, sys
from datetime import datetime

TODAY = "2026-06-08"

# ticker -> (folder, name_ko, name_en, next_v, asset_type, sector, prev_date)
PLAN = {
    "T":      ("ATT",            "AT&T",             "AT&T Inc.",                         5, "주식", "Communication Services / Telecom (Wireless·Fiber)", "2026-05-27"),
    "010120": ("LSELECTRIC",     "LS일렉트릭",        "LS Electric Co., Ltd.",             6, "주식", "Industrials / Electrical Equipment (전력기기·전력망)", "2026-05-28"),
    "034020": ("두산에너빌리티",  "두산에너빌리티",     "Doosan Enerbility Co., Ltd.",       5, "주식", "Industrials / Power & Nuclear (원자력·SMR·발전)", "2026-05-28"),
    "035720": ("카카오",          "카카오",            "Kakao Corp.",                       5, "주식", "Communication Services / Internet Platform", "2026-05-28"),
    "BA":     ("Boeing",         "보잉",              "The Boeing Company",                5, "주식", "Industrials / Aerospace & Defense", "2026-05-28"),
    "GE":     ("GEAerospace",    "GE 에어로스페이스",  "GE Aerospace",                      5, "주식", "Industrials / Aerospace (Jet Engines·Aftermarket)", "2026-05-28"),
    "GS":     ("GoldmanSachs",   "골드만삭스",         "The Goldman Sachs Group, Inc.",     6, "주식", "Financials / Investment Banking & Markets", "2026-05-28"),
    "HD":     ("HomeDepot",      "홈디포",            "The Home Depot, Inc.",              5, "주식", "Consumer Discretionary / Home Improvement Retail", "2026-05-28"),
    "HSBC":   ("HSBC",           "HSBC 홀딩스",        "HSBC Holdings plc (ADR)",           5, "주식", "Financials / Global Banking (Asia-focused)", "2026-05-28"),
    "JNJ":    ("JohnsonJohnson", "존슨앤드존슨",       "Johnson & Johnson",                 5, "주식", "Healthcare / Pharma & MedTech", "2026-05-28"),
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
    print(f"=== data.json 생성 — {TODAY} 회차2 — {len(tickers)}종 ===\n")
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
