#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-22 (7일 임계, 상한 20→10 클램핑, stock_update-2 슬롯)
대상 10종 (경과일 desc, 9일 코호트=2026-07-13 분석분 상위 10종):
  005380 v3, 005930 v10, 009150 v10, 207940 v3, 329180 v11, 466100 v10,
  AAPL v3, ADBE v11, AMD v3, ANET v9
- ANTHROPIC(56일) 비상장·비표준 standing 제외. SPACEX 동일.
- 오늘 01:00 10일 슬롯(staock_update)이 QUAL/SGOV/VEA 3종 처리 완료 → 본 회차는 9일 코호트.
- 각 종목 analysis/{ticker}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출).
- 분석 _content.json 은 후속 BLIND 분석가가 작성.
- 중앙 generator(reanalysis_generate_20260722_7day.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys

TODAY = "2026-07-22"
YYYYMMDD = "20260722"
THRESHOLD = 7

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "005380": ("005380", "현대차",             "현대차",             3,  "2026-07-13", "경기소비재-완성차/전동화·미국현지생산·제네시스", "주식"),
    "005930": ("005930", "삼성전자",           "삼성전자",           10, "2026-07-13", "기술-반도체/메모리(HBM)·파운드리·MX", "주식"),
    "009150": ("009150", "삼성전기",           "삼성전기",           10, "2026-07-13", "기술-전자부품/MLCC·패키지기판·카메라모듈", "주식"),
    "207940": ("207940", "삼성바이오로직스",   "삼성바이오로직스",   3,  "2026-07-13", "헬스케어-바이오CDMO/위탁생산·에피스분할", "주식"),
    "329180": ("329180", "HD현대중공업",       "HD현대중공업",       11, "2026-07-13", "산업재-조선/상선·특수선·엔진기계", "주식"),
    "466100": ("466100", "클로봇",             "클로봇",             10, "2026-07-13", "기술-로봇SW/실내자율주행·물류로봇", "주식"),
    "AAPL":   ("AAPL",   "Apple",              "애플",               3,  "2026-07-13", "기술-소비자하드웨어/아이폰·서비스·실리콘", "주식"),
    "ADBE":   ("ADBE",   "Adobe",              "어도비",             11, "2026-07-13", "기술-크리에이티브SW/구독·생성형AI(Firefly)", "주식"),
    "AMD":    ("AMD",    "AMD",                "AMD",                3,  "2026-07-13", "기술-반도체/CPU·GPU(MI시리즈)·데이터센터", "주식"),
    "ANET":   ("ANET",   "AristaNetworks",     "아리스타네트웍스",   9,  "2026-07-13", "기술-네트워크장비/데이터센터스위칭·AI백엔드", "주식"),
}

CUR_MAP = {"USD": "$", "KRW": "₩"}


def fetch(fetch_ticker):
    out = subprocess.run([sys.executable, "scripts/fetch_price.py", fetch_ticker],
                         capture_output=True, text=True, timeout=240).stdout
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
