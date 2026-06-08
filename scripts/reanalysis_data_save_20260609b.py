#!/usr/bin/env python3
"""재분석 자동 실행 — 2026-06-09 회차2 (7일 임계, 상한 10) — 10종 data.json 일괄 생성

대상: ORCL v4, 012450 v5, ABBV v4, AGG v4, AMAT v6, AMZN v5, ASTS v5, AVGO v6, BLK v5, GOOGL v5
fetch_price.py 라이브 가격(직전 미국 종가 / 한국 종가) + metadata 결합 → 각 v{N}/data.json 저장.
오늘 1회차(10일 임계 10종)에 이어 7일 임계로 7~9일 경과분 검출. IBM(8일, 11위)은 다음 회차 이월.
ANTHROPIC(비상장, 13일)은 선정 단계 제외(비표준 스코어카드) — 1회차 선례 동일.
"""
import json, os, subprocess, sys
from datetime import datetime

TODAY = "2026-06-09"

# ticker -> (folder, name_ko, name_en, next_v, asset_type, sector, prev_date)
PLAN = {
    "ORCL":   ("Oracle",                     "오라클",                 "Oracle Corporation",                  4, "주식", "Technology / Enterprise Software·Cloud (OCI)",          "2026-05-31"),
    "012450": ("한화에어로스페이스",            "한화에어로스페이스",      "Hanwha Aerospace Co., Ltd.",          5, "주식", "Industrials / Defense·Aerospace",                      "2026-06-01"),
    "ABBV":   ("AbbVie",                     "애브비",                 "AbbVie Inc.",                         4, "주식", "Healthcare / Pharmaceuticals (Immunology)",            "2026-06-01"),
    "AGG":    ("iSharesCoreUSAggregateBond", "iShares 미국종합채권 ETF", "iShares Core U.S. Aggregate Bond ETF", 4, "ETF", "ETF / US Aggregate Bond (Fixed Income)",               "2026-06-01"),
    "AMAT":   ("AppliedMaterials",           "어플라이드 머티어리얼즈",  "Applied Materials, Inc.",             6, "주식", "Technology / Semiconductor Equipment",                 "2026-06-01"),
    "AMZN":   ("Amazon",                     "아마존",                 "Amazon.com, Inc.",                    5, "주식", "Consumer Discretionary / E-commerce·Cloud (AWS)",      "2026-06-01"),
    "ASTS":   ("ASTSpaceMobile",             "AST 스페이스모바일",      "AST SpaceMobile, Inc.",               5, "주식", "Communication Services / Satellite Direct-to-Cell",    "2026-06-01"),
    "AVGO":   ("Broadcom",                   "브로드컴",               "Broadcom Inc.",                       6, "주식", "Technology / Semiconductor·Infra Software (AI ASIC)",  "2026-06-01"),
    "BLK":    ("BlackRock",                  "블랙록",                 "BlackRock, Inc.",                     5, "주식", "Financials / Asset Management",                        "2026-06-01"),
    "GOOGL":  ("Alphabet",                   "알파벳",                 "Alphabet Inc.",                       5, "주식", "Communication Services / Internet·AI·Cloud",           "2026-06-01"),
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
    print(f"=== data.json 생성 — {TODAY} 회차2 (7일 임계) — {len(tickers)}종 ===\n")
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
