#!/usr/bin/env python3
"""
재분석 회차2 (2026-06-07, 7일 임계) — 가격 수집 + data.json 생성 prep
대상 10종 (전원 2026-05-27 분석, 11일 경과):
  035420 NAVER, 066570 LG전자, ASML, AZN, BABA, BAC, BRKB, C, CAT, DIS
- fetch_price.py 라이브 가격(2026-06-05 종가) → analysis/{folder}_v{N}/data.json
- _content.json 은 종목별 BLIND 에이전트가 별도 작성
"""
import json, os, subprocess, sys
from datetime import datetime

TODAY = "2026-06-07"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ticker -> (fetch_symbol, folder, name_kr, next_v, prev_date, sector, asset_type)
PLAN = {
    "035420": ("035420", "035420_NAVER", "NAVER", 5, "2026-05-27", "Communication Services / Internet", "주식"),
    "066570": ("066570", "066570_LG전자", "LG전자", 2, "2026-05-27", "Technology / Consumer Electronics", "주식"),
    "ASML":   ("ASML", "ASML_ASML", "ASML", 5, "2026-05-27", "Technology / Semiconductor Equipment", "주식"),
    "AZN":    ("AZN", "AZN_AstraZeneca", "아스트라제네카", 5, "2026-05-27", "Healthcare / Pharmaceuticals", "주식"),
    "BABA":   ("BABA", "BABA_Alibaba", "알리바바", 5, "2026-05-27", "Consumer Discretionary / E-commerce", "주식"),
    "BAC":    ("BAC", "BAC_BankOfAmerica", "뱅크오브아메리카", 5, "2026-05-27", "Financials / Diversified Banks", "주식"),
    "BRKB":   ("BRK-B", "BRKB_BerkshireHathaway", "버크셔 해서웨이 B", 5, "2026-05-27", "Financials / Multi-Sector Holdings", "주식"),
    "C":      ("C", "C_Citigroup", "씨티그룹", 5, "2026-05-27", "Financials / Diversified Banks", "주식"),
    "CAT":    ("CAT", "CAT_Caterpillar", "캐터필러", 5, "2026-05-27", "Industrials / Construction Machinery", "주식"),
    "DIS":    ("DIS", "DIS_Disney", "디즈니", 5, "2026-05-27", "Communication Services / Entertainment", "주식"),
}


def fetch(symbol):
    out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "fetch_price.py"), symbol],
                         capture_output=True, text=True, cwd=ROOT)
    lines = out.stdout.splitlines()
    try:
        s = lines.index("JSON_OUTPUT_START")
        e = lines.index("JSON_OUTPUT_END")
        data = json.loads("\n".join(lines[s+1:e]))
        return data[0] if isinstance(data, list) else data
    except Exception as ex:
        print(f"  ⚠️ {symbol} JSON 파싱 실패: {ex}")
        print("STDERR:", out.stderr[-300:])
        return None


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    for tk in only:
        symbol, folder, kr, nv, prev_date, sector, asset = PLAN[tk]
        p = fetch(symbol)
        if not p or "current_price" not in p:
            print(f"  ❌ {tk}: 가격 수집 실패")
            fail.append(tk); continue
        cur = "$" if p.get("currency") in ("USD", "$") else ("₩" if symbol.isdigit() else p.get("currency", "$"))
        data = {
            "metadata": {
                "ticker": tk,
                "company_name": p.get("name"),
                "company_name_ko": kr,
                "analysis_date": TODAY,
                "analysis_version": f"v{nv}",
                "analysis_mode": "BLIND_reanalysis",
                "asset_type": asset,
                "sector": sector,
                "currency": cur,
                "prev_version_date": prev_date,
            },
            "currency": cur,
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
            "fetch_time": p.get("fetch_time"),
            "market_cap_str": p.get("market_cap_str"),
        }
        out_dir = os.path.join(ROOT, "analysis", f"{folder}_v{nv}")
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "data.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[{tk}] ✅ v{nv} data.json — {cur}{data['current_price']} (기준 {data['date']}, mc {data['market_cap_str']})")
        ok.append(tk)
    print(f"\n=== prep 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
