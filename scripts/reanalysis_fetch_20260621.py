#!/usr/bin/env python3
"""
재분석 data.json 수집 — 2026-06-21 (stock_update-2 슬롯, 7일 임계, 상한 20→10 클램핑)
대상 10종: NKE v6, MSTR v7, MRVL v7, KO v6, IWM v7, GEV v5, ETN v5, DIA v7, CVX v7, 005930 v6
- fetch_price.py 의 fetch_us/fetch_korean 직접 호출 → 종가 데이터 수집
- analysis/{ticker}_{folder}_v{nv}/data.json 작성 (BLIND _meta 포함)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_price import fetch_us, fetch_korean, is_korean_ticker

TODAY = "2026-06-21"

# ticker -> (folder_name, name_kr, next_v, prev_date)
PLAN = {
    "NKE":    ("Nike",                 "나이키",            6, "2026-06-12"),
    "MSTR":   ("Strategy",             "스트래티지",        7, "2026-06-12"),
    "MRVL":   ("MarvellTechnology",    "마벨테크놀로지",    7, "2026-06-12"),
    "KO":     ("CocaCola",             "코카콜라",          6, "2026-06-12"),
    "IWM":    ("iSharesRussell2000",   "iShares러셀2000",   7, "2026-06-12"),
    "GEV":    ("GEVernova",            "GE버노바",          5, "2026-06-12"),
    "ETN":    ("Eaton",                "이튼",              5, "2026-06-12"),
    "DIA":    ("SPDRDJIA",             "SPDR다우존스",      7, "2026-06-12"),
    "CVX":    ("Chevron",              "셰브론",            7, "2026-06-12"),
    "005930": ("삼성전자",             "삼성전자",          6, "2026-06-12"),
}


def norm_currency(cur):
    return {"USD": "$", "KRW": "₩"}.get(cur, cur)


def main():
    ok, fail = [], []
    for ticker, (folder, kr, nv, prev_date) in PLAN.items():
        out_dir = f"analysis/{ticker}_{folder}_v{nv}"
        os.makedirs(out_dir, exist_ok=True)
        try:
            d = fetch_korean(ticker) if is_korean_ticker(ticker) else fetch_us(ticker)
            if not d or "current_price" not in d or d.get("current_price") in (None, 0):
                raise ValueError(f"빈 응답/가격 없음: {d}")
            d["currency"] = norm_currency(d.get("currency", "$"))
            prevv = nv - 1
            d["_meta"] = {
                "ticker": ticker,
                "name_kr": kr,
                "analysis_mode": f"reanalysis_v{nv}_BLIND",
                "analysis_date": TODAY,
                "data_source": "fetch_price.py (yfinance/pykrx) " + TODAY + " + knowledge-base + 공개지식(date_cutoff 2026-01)",
                "blind_note": f"이전 v1~v{prevv} 분석/리포트/timeline 미참조 — 현재 데이터에서 독립 추론",
            }
            with open(f"{out_dir}/data.json", "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            cur = d["currency"]
            print(f"[{ticker}] OK v{nv}  {cur}{d['current_price']}  ATR14={d.get('atr_14')}  "
                  f"손절={d.get('stop_loss_2atr')} 목표={d.get('target_3atr')}  ({d.get('date')})")
            ok.append(ticker)
        except Exception as e:
            print(f"  X {ticker}: FETCH FAILED — {e}")
            fail.append(ticker)
    print(f"\n=== fetch 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
