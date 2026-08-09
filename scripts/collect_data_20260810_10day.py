#!/usr/bin/env python3
"""재분석 데이터 수집 — 2026-08-10 (10일 임계, staock_update 슬롯, /재분석실행 10 10).
07-31 코호트 상장 10종(정확히 10일 경과). ANTHROPIC(75일) 비상장·비표준 standing 제외.
fetch_price 로 종가 수집 → analysis/{ticker}_{folder}_v{nv}/data.json + reanalysis 메타.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from fetch_price import fetch_us, fetch_korean, is_korean_ticker

TODAY = "2026-08-10"
RUN = "20260810_10day"
THRESHOLD = 10

# ticker -> (folder(이름만), name_kr, next_v, prev_v, prev_date, sector)
PLAN = {
    "WMT":  ("Walmart",       "월마트",       12, 11, "2026-07-31", "필수소비재-대형 리테일/옴니채널(광고·멤버십)"),
    "V":    ("Visa",          "비자",         12, 11, "2026-07-31", "금융-결제 네트워크(카드 레일·크로스보더)"),
    "VZ":   ("Verizon",       "버라이즌",     12, 11, "2026-07-31", "통신-대형 이동통신(무선·브로드밴드)"),
    "TSLA": ("Tesla",         "테슬라",       12, 11, "2026-07-31", "자동차-전기차/에너지·자율주행(FSD·로보택시)"),
    "TIP":  ("iSharesTIPS",   "아이셰어즈 물가연동국채 ETF", 12, 11, "2026-07-31", "ETF-미국 물가연동국채(TIPS)"),
    "STX":  ("Seagate",       "시게이트",     12, 11, "2026-07-31", "기술-저장장치(HDD·니어라인/AI 데이터)"),
    "SMR":  ("NuScalePower",  "뉴스케일파워", 10, 9,  "2026-07-31", "산업재-원자력/SMR(소형모듈원자로)"),
    "DIS":  ("Disney",        "디즈니",       12, 11, "2026-07-31", "커뮤니케이션-미디어/엔터(스트리밍·테마파크)"),
    "C":    ("Citigroup",     "씨티그룹",     12, 11, "2026-07-31", "금융-글로벌 대형은행(트랜잭션·트레이딩)"),
    "CAT":  ("Caterpillar",   "캐터필러",     12, 11, "2026-07-31", "산업재-건설/광산 중장비(에너지·인프라)"),
}

ETF_SET = {"TIP"}
FETCH_TICKER = {}  # yfinance 심볼 매핑 (필요 시)


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    for ticker in only:
        folder, kr, nv, pv, pdate, sector = PLAN[ticker]
        out_dir = f"analysis/{ticker}_{folder}_v{nv}"
        os.makedirs(out_dir, exist_ok=True)
        try:
            fetch_sym = FETCH_TICKER.get(ticker, ticker)
            d = fetch_korean(ticker) if is_korean_ticker(ticker) else fetch_us(fetch_sym)
            if "error" in d:
                print(f"  X {ticker}: {d['error']}")
                fail.append(ticker); continue
            d["ticker"] = ticker
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
                json.dump(d, f, ensure_ascii=False, indent=2, default=float)
            print(f"[{ticker}] OK v{nv} — {d.get('currency','$')}{d.get('current_price')} "
                  f"ATR {d.get('atr_14')} ({d.get('atr_pct')}%) 52w {d.get('low_52w')}~{d.get('high_52w')} "
                  f"기준일 {d.get('date')}")
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
