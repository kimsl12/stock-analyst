#!/usr/bin/env python3
"""재분석 데이터 수집 — 2026-08-01 (10일 임계, staock_update 슬롯, /재분석실행 10 10)
07-18 코호트 5종 (VIG·TLT·VRT·XOM·VST) + 07-20 코호트 5종 (TMO·QCOM·NOW·NFLX·MELI).
ANTHROPIC 비상장·비표준 standing 제외. 크립토(QuantTrader 별도) 제외.
fetch_price 로 종가 수집 → analysis/{ticker}_{folder}_v{nv}/data.json + reanalysis 메타.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from fetch_price import fetch_us, fetch_korean, is_korean_ticker

TODAY = "2026-08-01"
RUN = "20260801_10day"
THRESHOLD = 10

# ticker -> (folder, name_kr, next_v, prev_v, prev_date, sector)
PLAN = {
    "VIG":  ("VanguardDividendAppreciation", "뱅가드배당성장ETF", 9,  8,  "2026-07-18", "ETF-미국 배당성장주"),
    "TLT":  ("iSharesTreasury",              "아이셰어스20년국채", 11, 10, "2026-07-18", "ETF-미국 장기국채"),
    "VRT":  ("VertivHoldings",               "버티브홀딩스",       9,  8,  "2026-07-18", "기술-데이터센터 인프라/열관리"),
    "XOM":  ("ExxonMobil",                   "엑슨모빌",           11, 10, "2026-07-18", "에너지-통합 석유메이저"),
    "VST":  ("VistraCorp",                   "비스트라",           9,  8,  "2026-07-18", "유틸리티-발전/원자력"),
    "TMO":  ("ThermoFisher",                 "써모피셔사이언티픽", 4,  3,  "2026-07-20", "헬스케어-생명과학 장비/진단"),
    "QCOM": ("Qualcomm",                     "퀄컴",               4,  3,  "2026-07-20", "반도체-모바일/엣지 AP"),
    "NOW":  ("ServiceNow",                   "서비스나우",         4,  3,  "2026-07-20", "소프트웨어-엔터프라이즈 워크플로우/AI"),
    "NFLX": ("Netflix",                      "넷플릭스",           4,  3,  "2026-07-20", "미디어-글로벌 스트리밍"),
    "MELI": ("MercadoLibre",                 "메르카도리브레",     4,  3,  "2026-07-20", "이커머스-중남미 마켓플레이스/핀테크"),
}

ETF_SET = {"VIG", "TLT"}


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    for ticker in only:
        folder, kr, nv, pv, pdate, sector = PLAN[ticker]
        out_dir = f"analysis/{ticker}_{folder}_v{nv}"
        os.makedirs(out_dir, exist_ok=True)
        try:
            d = fetch_korean(ticker) if is_korean_ticker(ticker) else fetch_us(ticker)
            if "error" in d:
                print(f"  X {ticker}: {d['error']}")
                fail.append(ticker); continue
            d["asset_type"] = "ETF" if ticker in ETF_SET else "주식"
            d["analysis_date"] = TODAY
            d["analysis_version"] = f"v{nv}"
            d["reanalysis"] = {
                "version": f"v{nv}",
                "previous_version": f"v{pv}",
                "blind_mode": True,
                "previous_files_read": 0,
                "reanalysis_date": TODAY,
                "threshold_days": THRESHOLD,
                "session_run": RUN,
                "sector": sector,
                "company_name_ko": kr,
                "prev_version_date": pdate,
            }
            with open(f"{out_dir}/data.json", "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            print(f"[{ticker}] OK v{nv} — {d.get('currency','$')}{d.get('current_price')} "
                  f"ATR {d.get('atr_14')} ({d.get('atr_pct')}%) 52w {d.get('low_52w')}~{d.get('high_52w')}")
            ok.append(ticker)
        except Exception as e:
            print(f"  X {ticker}: EXC {e}")
            import traceback; traceback.print_exc()
            fail.append(ticker)
    print(f"\n=== 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
