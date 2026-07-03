#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-04 (7일 임계, 상한 20→10 클램핑, stock_update-2 슬롯)
대상 10종 (8~9일 stale, 2026-06-25/26 분석분 배치):
  USMV v8, BA v8, BLK v8, GE v8, GLD v8, GOOGL v8, GS v9, HD v8, HSBC v8, JNJ v8

각 종목 analysis/{disp}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출, dict 형식).
분석 _content.json 은 후속 BLIND 분석가(general-purpose)가 작성.
ANTHROPIC(38일, 비상장·비표준) 은 standing 제외 — 후보 아님.
중앙 generator(reanalysis_generate_20260704_7day.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys

TODAY = "2026-07-04"
YYYYMMDD = "20260704"
THRESHOLD = 7

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "USMV":  ("USMV",  "iSharesMinVol",   "iShares 미국 최소변동성 ETF", 8, "2026-06-25", "ETF/미국 저변동성 우량주(MSCI USA Min Vol)", "ETF"),
    "BA":    ("BA",    "Boeing",          "보잉",                        8, "2026-06-26", "산업재-항공/상용기·방산·서비스", "주식"),
    "BLK":   ("BLK",   "BlackRock",       "블랙록",                      8, "2026-06-26", "금융-자산운용/ETF(iShares)·Aladdin·대체투자", "주식"),
    "GE":    ("GE",    "GEAerospace",     "GE에어로스페이스",            8, "2026-06-26", "산업재-항공/항공엔진·서비스(LEAP)", "주식"),
    "GLD":   ("GLD",   "SPDRGoldShares",  "SPDR 골드셰어즈 ETF",         8, "2026-06-26", "원자재 ETF/금 현물(SPDR Gold)", "ETF"),
    "GOOGL": ("GOOGL", "Alphabet",        "알파벳",                      8, "2026-06-26", "커뮤니케이션서비스/검색·광고·클라우드·AI(Gemini)", "주식"),
    "GS":    ("GS",    "GoldmanSachs",    "골드만삭스",                  9, "2026-06-26", "금융-투자은행/트레이딩·IB·자산운용", "주식"),
    "HD":    ("HD",    "HomeDepot",       "홈디포",                      8, "2026-06-26", "임의소비재-유통/주택개선 소매", "주식"),
    "HSBC":  ("HSBC",  "HSBC",            "HSBC",                        8, "2026-06-26", "금융-은행/글로벌 상업·투자은행(아시아 중심)", "주식"),
    "JNJ":   ("JNJ",   "JohnsonJohnson",  "존슨앤드존슨",                8, "2026-06-26", "헬스케어/제약·의료기기·소비자건강", "주식"),
}

CUR_MAP = {"USD": "$", "KRW": "₩"}


def fetch(fetch_ticker):
    out = subprocess.run([sys.executable, "scripts/fetch_price.py", fetch_ticker],
                         capture_output=True, text=True, timeout=150).stdout
    if "JSON_OUTPUT_START" not in out:
        raise RuntimeError(f"{fetch_ticker}: JSON 마커 없음")
    block = out.split("JSON_OUTPUT_START", 1)[1]
    block = block.split("JSON_OUTPUT_END", 1)[0].strip()
    arr = json.loads(block)
    return arr[0]


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    for disp in only:
        fetch_ticker, folder, kr, nv, prev_date, sector, atype = PLAN[disp]
        try:
            d = fetch(fetch_ticker)
            if d.get("current_price") in (None, 0) or d.get("atr_14") in (None, 0):
                raise RuntimeError(f"가격/ATR 누락: {d}")
            cur = CUR_MAP.get(d.get("currency", "USD"), d.get("currency"))
            d["ticker"] = disp
            d["fetch_ticker"] = fetch_ticker
            d["currency"] = cur
            d["asset_type"] = atype
            d["analysis_date"] = TODAY
            d["analysis_version"] = f"v{nv}"
            d["reanalysis"] = {
                "version": f"v{nv}",
                "previous_version": f"v{nv-1}",
                "blind_mode": True,
                "previous_files_read": 0,
                "reanalysis_date": TODAY,
                "threshold_days": THRESHOLD,
                "session_run": YYYYMMDD,
                "sector": sector,
                "company_name_ko": kr,
                "prev_version_date": prev_date,
            }
            out_dir = f"analysis/{disp}_{folder}_v{nv}"
            os.makedirs(out_dir, exist_ok=True)
            with open(f"{out_dir}/data.json", "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            print(f"[{disp}] OK v{nv} {cur}{d['current_price']} ATR {cur}{d['atr_14']} ({d['atr_pct']}%) "
                  f"손절 {cur}{d.get('stop_loss_2atr')} 목표 {cur}{d.get('target_3atr')} date={d['date']} -> {out_dir}/")
            ok.append(disp)
        except Exception as e:
            print(f"  X {disp}: FAILED — {e}")
            fail.append(disp)
    print(f"\n=== 데이터 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
