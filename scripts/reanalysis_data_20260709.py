#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-09 (10일 임계, 상한 10, staock_update 슬롯)
대상 10종 (10~11일 stale, 2026-06-28/29 분석분 백로그):
  LRCX v7, KO v8, JPM v7, IWM v9, GEV v7, STX v9, SMR v7, SLV v8, RKLB v8, QQQ v8

각 종목 analysis/{disp}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출, dict 형식).
분석 _content.json 은 후속 BLIND 분석가(general-purpose)가 작성.
ANTHROPIC(43일, 비상장·비표준) 은 standing 제외 — 후보 아님.
중앙 generator(reanalysis_generate_20260709.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys

TODAY = "2026-07-09"
YYYYMMDD = "20260709"
THRESHOLD = 10

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "LRCX": ("LRCX", "LamResearch",        "램리서치",       7, "2026-06-28", "기술-반도체장비/식각·증착 WFE(파운드리·메모리 capex)", "주식"),
    "KO":   ("KO",   "CocaCola",           "코카콜라",       8, "2026-06-28", "필수소비재-음료/탄산·비탄산 글로벌 브랜드", "주식"),
    "JPM":  ("JPM",  "JPMorgan",           "JP모건",         7, "2026-06-28", "금융-은행/IB·소비자금융·자산관리(대형 유니버설뱅크)", "주식"),
    "IWM":  ("IWM",  "iSharesRussell2000", "iShares 러셀2000", 9, "2026-06-28", "ETF-미국 소형주 지수(러셀2000, 경기민감)", "ETF"),
    "GEV":  ("GEV",  "GEVernova",          "GE버노바",       7, "2026-06-28", "산업재-전력장비/가스터빈·그리드·풍력(전력화 수혜)", "주식"),
    "STX":  ("STX",  "Seagate",            "시게이트",       9, "2026-06-29", "기술-스토리지/대용량 HDD(HAMR)·니어라인", "주식"),
    "SMR":  ("SMR",  "NuScalePower",       "뉴스케일파워",   7, "2026-06-29", "산업재-원자력/SMR(소형모듈원자로)", "주식"),
    "SLV":  ("SLV",  "iSharesSilver",      "iShares 실버",   8, "2026-06-29", "ETF-은 현물(산업금속+귀금속 이중성)", "ETF"),
    "RKLB": ("RKLB", "RocketLab",          "로켓랩",         8, "2026-06-29", "산업재-우주/소형발사체(Electron·Neutron)·위성", "주식"),
    "QQQ":  ("QQQ",  "InvescoQQQ",         "인베스코 QQQ",   8, "2026-06-29", "ETF-나스닥100 지수(대형 기술주 집중)", "ETF"),
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
