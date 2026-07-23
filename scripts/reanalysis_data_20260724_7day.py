#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-24 (7일 임계, 상한 20→10 클램핑, stock_update-2 슬롯)
대상 10종 (경과일 desc, 10일 코호트=2026-07-14 분석분, 오늘 01:00 10일 슬롯이 처리 못 한 백로그):
  HOOD v10, INTC v10, LUNR v10, META v11, IONQ v10,
  LVMUY v11, MA v10, LLY v11, MRK v10, IBM v9
- 오늘 01:00 10일 슬롯(staock_update)이 SNDK/T/MUU/NVO/MS/NVS/MU/PG/SOXL/SOXS 10종 처리 완료.
  7일 런 일일 cap(10종)으로 새어나온 나머지 10일 코호트 → 본 회차 정상 재분석 (dual_schedule 설계대로).
- ANTHROPIC 비상장·비표준 standing 제외. 크립토(QuantTrader 별도) 제외.
- 각 종목 analysis/{ticker}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출).
- 분석 _content.json 은 후속 BLIND 분석가가 작성.
- 중앙 generator(reanalysis_generate_20260724_7day.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys

TODAY = "2026-07-24"
YYYYMMDD = "20260724"
THRESHOLD = 7

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "HOOD":  ("HOOD",  "Robinhood",         "로빈후드",           10, "2026-07-14", "금융-핀테크/증권중개·크립토·옵션·현금관리", "주식"),
    "INTC":  ("INTC",  "Intel",             "인텔",               10, "2026-07-14", "기술-반도체/CPU·파운드리(IFS)·데이터센터", "주식"),
    "LUNR":  ("LUNR",  "IntuitiveMachines", "인튜이티브머신스",   10, "2026-07-14", "산업재-우주/달착륙선·NASA CLPS·우주인프라", "주식"),
    "META":  ("META",  "Meta",              "메타플랫폼스",       11, "2026-07-14", "기술-소셜미디어/디지털광고·생성형AI·Reality Labs", "주식"),
    "IONQ":  ("IONQ",  "IonQ",              "아이온큐",           10, "2026-07-14", "기술-양자컴퓨팅/트랩드이온·클라우드양자", "주식"),
    "LVMUY": ("LVMUY", "LVMH",              "루이비통모엣헤네시", 11, "2026-07-14", "경기소비재-명품/패션·주류·화장품·리테일", "주식"),
    "MA":    ("MA",    "Mastercard",        "마스터카드",         10, "2026-07-14", "금융-결제네트워크/카드·크로스보더·B2B결제", "주식"),
    "LLY":   ("LLY",   "EliLilly",          "일라이릴리",         11, "2026-07-14", "헬스케어-제약/GLP-1비만·당뇨·알츠하이머", "주식"),
    "MRK":   ("MRK",   "Merck",             "머크",               10, "2026-07-14", "헬스케어-제약/키트루다·백신·종양학", "주식"),
    "IBM":   ("IBM",   "IBM",               "IBM",                9,  "2026-07-14", "기술-엔터프라이즈IT/하이브리드클라우드·watsonx AI·컨설팅", "주식"),
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
