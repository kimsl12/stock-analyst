#!/usr/bin/env python3
"""재분석 데이터 수집 — 2026-08-09 (7일 임계, stock_update-2 슬롯, /재분석실행 7 20 → cap 10).
07-31 코호트 10종(9일 경과, 티커 asc 상위 10). ANTHROPIC(74일) 비상장·비표준 standing 제외.
당일 10일 런은 정상 0종(임계 10일+ 유일종 ANTHROPIC 제외) → 무겹침.
fetch_price 로 종가 수집 → analysis/{ticker}_{folder}_v{nv}/data.json + reanalysis 메타.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from fetch_price import fetch_us, fetch_korean, is_korean_ticker

TODAY = "2026-08-09"
RUN = "20260809_7day"
THRESHOLD = 7

# ticker -> (folder(이름만), name_kr, next_v, prev_v, prev_date, sector)
PLAN = {
    "010120": ("LSELECTRIC",                 "LS일렉트릭",                  13, 12, "2026-07-31", "산업재-전력기기/전력인프라(변압기·전력망)"),
    "012450": ("한화에어로스페이스",          "한화에어로스페이스",          12, 11, "2026-07-31", "산업재-방산/항공우주(엔진·지상장비)"),
    "034020": ("두산에너빌리티",              "두산에너빌리티",              12, 11, "2026-07-31", "산업재-발전설비/원자력(SMR·대형원전)"),
    "035720": ("카카오",                      "카카오",                      12, 11, "2026-07-31", "기술-인터넷 플랫폼/핀테크·콘텐츠"),
    "AGG":    ("iSharesCoreUSAggregateBond",  "아이셰어즈 미국종합채권 ETF", 11, 10, "2026-07-31", "ETF-미국 투자등급 종합채권"),
    "AMAT":   ("AppliedMaterials",            "어플라이드머티어리얼즈",      13, 12, "2026-07-31", "기술-반도체 장비(증착·식각·이온주입)"),
    "ASTS":   ("ASTSpaceMobile",              "AST스페이스모바일",           12, 11, "2026-07-31", "통신-위성 직접통신(D2C)"),
    "AVGO":   ("Broadcom",                    "브로드컴",                    13, 12, "2026-07-31", "기술-반도체/인프라SW(AI ASIC·네트워킹)"),
    "BAC":    ("BankOfAmerica",               "뱅크오브아메리카",            12, 11, "2026-07-31", "금융-대형은행(상업·투자은행)"),
    "BRKB":   ("BerkshireHathaway",           "버크셔해서웨이",              12, 11, "2026-07-31", "금융-복합기업/보험(자본배분)"),
}

ETF_SET = {"AGG"}
FETCH_TICKER = {"BRKB": "BRK-B"}  # yfinance 심볼 매핑 (data.json ticker 는 원본 유지)


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
            d["ticker"] = ticker  # 원본 티커 유지 (BRK-B → BRKB)
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
