#!/usr/bin/env python3
"""재분석 데이터 수집 — 2026-08-10 (7일 임계, stock_update-2 슬롯, /재분석실행 7 20→cap10).
08-01 코호트 상장 10종(정확히 9일 경과, 티커 알파벳순 tiebreak). ANTHROPIC(75일) 비상장·비표준 standing 제외.
ETF(TLT·USMV·VIG)·잔여 9일종은 익일 롤링 런으로 이월(윈도우 내 유지).
fetch_price 로 종가 수집 → analysis/{ticker}_{folder}_v{nv}/data.json + reanalysis 메타.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from fetch_price import fetch_us, fetch_korean, is_korean_ticker

TODAY = "2026-08-10"
RUN = "20260810b_7day"
THRESHOLD = 7

# ticker -> (folder(이름만), name_kr, next_v, prev_v, prev_date, sector)
PLAN = {
    "466100": ("클로봇",         "클로봇",         12, 11, "2026-08-01", "로봇-자율주행SW/서비스로봇(물류·안내)"),
    "AMZN":   ("Amazon",         "아마존",         12, 11, "2026-08-01", "인터넷-이커머스/클라우드(AWS·광고)"),
    "GOOGL":  ("Alphabet",       "알파벳",         12, 11, "2026-08-01", "인터넷-검색/광고/클라우드/AI(제미나이)"),
    "GS":     ("GoldmanSachs",   "골드만삭스",     13, 12, "2026-08-01", "금융-투자은행/트레이딩/자산운용"),
    "LNG":    ("CheniereEnergy", "셰니에르에너지", 5,  4,  "2026-08-01", "에너지-LNG 수출/인프라"),
    "MELI":   ("MercadoLibre",   "메르카도리브레", 5,  4,  "2026-08-01", "이커머스-중남미 마켓플레이스/핀테크"),
    "NFLX":   ("Netflix",        "넷플릭스",       5,  4,  "2026-08-01", "미디어-글로벌 스트리밍"),
    "NOW":    ("ServiceNow",     "서비스나우",     5,  4,  "2026-08-01", "소프트웨어-엔터프라이즈 워크플로우/AI"),
    "PEP":    ("PepsiCo",        "펩시코",         12, 11, "2026-08-01", "필수소비재-음료/스낵"),
    "QCOM":   ("Qualcomm",       "퀄컴",           5,  4,  "2026-08-01", "반도체-모바일/엣지 AP"),
}

ETF_SET = set()
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
