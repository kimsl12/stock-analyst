#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-17 (7일 임계, 상한 20→10 클램핑, stock_update-2 슬롯)
대상 10종 (경과일 desc, 동률 알파벳순, ANTHROPIC 비상장 standing 제외):
  10일(2026-07-07 코호트): TM v8, TMUS v10, TQQQ v10(ETF 3x), TSM v9, TTE v9, TXN v9, VOO v9(ETF)
  9일(2026-07-08 코호트, 알파벳 상위 3): 035420 NAVER v10, 066570 LG전자 v7, CEG v8
- 오늘 오전 10일 슬롯(staock_update)이 MSFT 등 10종 처리 완료 → 본 회차는 그 다음 오래된 배치.
- 각 종목 analysis/{disp}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출).
- 한국(035420·066570)은 6자리 티커 그대로 → fetch_price.py 가 pykrx 자동 처리.
- 분석 _content.json 은 후속 BLIND 분석가(general-purpose)가 작성.
- 중앙 generator(reanalysis_generate_20260717_7day.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys

TODAY = "2026-07-17"
YYYYMMDD = "20260717"
THRESHOLD = 7

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "TM":     ("TM",     "Toyota",               "도요타",              8,  "2026-07-07", "경기소비재-자동차/HEV·BEV·수소·글로벌 완성차", "주식"),
    "TMUS":   ("TMUS",   "TMobile",              "T-모바일",            10, "2026-07-07", "통신서비스-무선통신/5G·포스트페이드·광대역", "주식"),
    "TQQQ":   ("TQQQ",   "ProSharesUltraProQQQ", "프로셰어즈 나스닥100 3배", 10, "2026-07-07", "나스닥100 레버리지(3x, 트레이딩 도구)", "ETF"),
    "TSM":    ("TSM",    "TSMC",                 "TSMC",                9,  "2026-07-07", "기술-반도체/파운드리·첨단노드 독점", "주식"),
    "TTE":    ("TTE",    "TotalEnergies",        "토탈에너지스",        9,  "2026-07-07", "에너지-통합석유가스/LNG·재생에너지 전환", "주식"),
    "TXN":    ("TXN",    "TexasInstruments",     "텍사스인스트루먼트",  9,  "2026-07-07", "기술-반도체/아날로그·임베디드(산업·차량)", "주식"),
    "VOO":    ("VOO",    "VanguardSP500",        "뱅가드 S&P500",       9,  "2026-07-07", "미국 대형주 인덱스(S&P500, 코어 보유)", "ETF"),
    "035420": ("035420", "NAVER",                "네이버",              10, "2026-07-08", "기술-인터넷플랫폼/AI·커머스·핀테크·콘텐츠", "주식"),
    "066570": ("066570", "LG전자",               "LG전자",              7,  "2026-07-08", "경기소비재-가전/전장(VS)·B2B·HVAC", "주식"),
    "CEG":    ("CEG",    "ConstellationEnergy",  "컨스텔레이션에너지",  8,  "2026-07-08", "유틸리티-전력/원자력·AI 데이터센터 전력공급", "주식"),
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
            print(f"[{disp}] X FAILED — {e}")
            fail.append(disp)
    print(f"\n=== 데이터 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
