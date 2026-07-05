#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-06 (7일 임계, 상한 20→10 클램핑, stock_update-2 슬롯)
대상 10종 (8~9일 stale, 2026-06-27/28 분석분 배치):
  COST v9, COIN v9, BHP v9, ADBE v9, 329180 v9, 466100 v8, 009150 v8, ANET v7, CVX v9, 005930 v8

각 종목 analysis/{disp}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출, dict 형식).
분석 _content.json 은 후속 BLIND 분석가(general-purpose)가 작성.
ANTHROPIC(40일, 비상장·비표준) 은 standing 제외 — 후보 아님.
중앙 generator(reanalysis_generate_20260706_7day.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys

TODAY = "2026-07-06"
YYYYMMDD = "20260706"
THRESHOLD = 7

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "COST":   ("COST",   "Costco",         "코스트코",       9, "2026-06-27", "임의소비재-유통/창고형 회원제 소매(멤버십)", "주식"),
    "COIN":   ("COIN",   "Coinbase",       "코인베이스",     9, "2026-06-27", "금융-크립토 거래소/커스터디·스테이킹·USDC", "주식"),
    "BHP":    ("BHP",    "BHPGroup",       "BHP그룹",        9, "2026-06-27", "소재-광업/철광석·구리·석탄(호주 대형 자원)", "주식"),
    "ADBE":   ("ADBE",   "Adobe",          "어도비",         9, "2026-06-27", "기술-소프트웨어/크리에이티브·디지털미디어·AI(Firefly)", "주식"),
    "329180": ("329180", "HD현대중공업",   "HD현대중공업",   9, "2026-06-27", "산업재-조선/상선·해양플랜트·특수선(방산)", "주식"),
    "466100": ("466100", "클로봇",         "클로봇",         8, "2026-06-27", "기술-로보틱스/자율주행 로봇 SW·솔루션", "주식"),
    "009150": ("009150", "삼성전기",       "삼성전기",       8, "2026-06-27", "기술-전자부품/MLCC·패키지기판·카메라모듈", "주식"),
    "ANET":   ("ANET",   "AristaNetworks", "아리스타네트웍스", 7, "2026-06-27", "기술-네트워킹/데이터센터 스위칭·AI 네트워크", "주식"),
    "CVX":    ("CVX",    "Chevron",        "셰브론",         9, "2026-06-28", "에너지-통합/석유·가스 상하류·화학", "주식"),
    "005930": ("005930", "삼성전자",       "삼성전자",       8, "2026-06-28", "기술-반도체/메모리·파운드리·가전(DX)", "주식"),
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
