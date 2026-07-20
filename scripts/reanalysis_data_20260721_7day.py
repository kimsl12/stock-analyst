#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-21 (7일 임계, 상한 20→10 클램핑, stock_update-2 슬롯)
대상 10종 (경과일 desc, 동률 티커 desc, ANTHROPIC 비상장 standing 제외):
  8일(2026-07-13 코호트): PEP v9, ORCL v8, LIN v2, JNJ v9, ISRG v2, HSBC v9, HD v9, GS v10, GOOGL v9, GLD v9(ETF)
- 오늘 오전 10일 슬롯(staock_update)이 ABBV 1종 처리 완료 → 본 회차는 8일 코호트 상위 10종.
- 각 종목 analysis/{disp}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출).
- 분석 _content.json 은 후속 BLIND 분석가(general-purpose)가 작성.
- 중앙 generator(reanalysis_generate_20260721_7day.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys

TODAY = "2026-07-21"
YYYYMMDD = "20260721"
THRESHOLD = 7

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "PEP":   ("PEP",  "PepsiCo",           "펩시코",              10, "2026-07-13", "필수소비재-음료/스낵·글로벌 F&B", "주식"),
    "ORCL":  ("ORCL", "Oracle",            "오라클",              9,  "2026-07-13", "기술-엔터프라이즈SW/OCI·AI 데이터센터·DB", "주식"),
    "LIN":   ("LIN",  "Linde",             "린데",                3,  "2026-07-13", "소재-산업가스/수소·전자소재·장기계약", "주식"),
    "JNJ":   ("JNJ",  "JohnsonJohnson",    "존슨앤드존슨",        10, "2026-07-13", "헬스케어-제약/메드텍·이노베이티브메디슨", "주식"),
    "ISRG":  ("ISRG", "IntuitiveSurgical", "인튜이티브서지컬",    3,  "2026-07-13", "헬스케어-의료기기/로봇수술(다빈치)·소모품", "주식"),
    "HSBC":  ("HSBC", "HSBC",              "HSBC",                10, "2026-07-13", "금융-글로벌은행/아시아 중심·자산관리", "주식"),
    "HD":    ("HD",   "HomeDepot",         "홈디포",              10, "2026-07-13", "경기소비재-주택개량 리테일/Pro·주택시장", "주식"),
    "GS":    ("GS",   "GoldmanSachs",      "골드만삭스",          11, "2026-07-13", "금융-투자은행/트레이딩·IB·자산운용", "주식"),
    "GOOGL": ("GOOGL","Alphabet",          "알파벳",              10, "2026-07-13", "기술-인터넷플랫폼/검색·클라우드·Gemini AI", "주식"),
    "GLD":   ("GLD",  "SPDRGoldShares",    "SPDR 골드 셰어즈",    10, "2026-07-13", "원자재-금 현물 ETF(인플레·안전자산 헤지)", "ETF"),
}

CUR_MAP = {"USD": "$", "KRW": "₩"}


def fetch(fetch_ticker):
    out = subprocess.run([sys.executable, "scripts/fetch_price.py", fetch_ticker],
                         capture_output=True, text=True, timeout=180).stdout
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
    print(f"\n=== 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
