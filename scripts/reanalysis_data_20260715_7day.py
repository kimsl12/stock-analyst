#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-15 (7일 임계, 상한 20→10 클램핑, stock_update-2 슬롯)
대상 10종 (9일 stale, 2026-07-06 분석분 코호트):
  HOOD v9, INTC v9, SOXS v9(ETF 3x), NVS v10, LUNR v9, SOXL v9(ETF 3x),
  MS v10, IONQ v9, SNDK v11, IBM v8
- 8 개별주 + 2 레버리지 ETF(SOXS/SOXL, 트레이딩 도구 적합도 프레이밍).
- ANTHROPIC(49일, 비상장·비표준) standing 제외 — 후보 아님.
- 각 종목 analysis/{disp}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출).
- 분석 _content.json 은 후속 BLIND 분석가(general-purpose)가 작성.
- 중앙 generator(reanalysis_generate_20260715_7day.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys

TODAY = "2026-07-15"
YYYYMMDD = "20260715"
THRESHOLD = 7

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "HOOD": ("HOOD", "Robinhood",              "로빈후드",              9,  "2026-07-06", "금융-핀테크/증권·크립토 브로커리지·자산관리", "주식"),
    "INTC": ("INTC", "Intel",                  "인텔",                  9,  "2026-07-06", "기술-반도체/CPU·파운드리(IDM)·AI 가속기", "주식"),
    "SOXS": ("SOXS", "Direxion3xSemiBear",     "디렉시온 반도체 3배 베어", 9,  "2026-07-06", "반도체 레버리지(인버스 3x)", "ETF"),
    "NVS":  ("NVS",  "Novartis",               "노바티스",              10, "2026-07-06", "헬스케어-제약/혁신신약·순수 제약 전환", "주식"),
    "LUNR": ("LUNR", "IntuitiveMachines",      "인튜이티브머신스",      9,  "2026-07-06", "산업재-우주/달탐사 착륙선·우주 서비스", "주식"),
    "SOXL": ("SOXL", "Direxion3xSemiconductor", "디렉시온 반도체 3배 불", 9,  "2026-07-06", "반도체 레버리지(3x)", "ETF"),
    "MS":   ("MS",   "MorganStanley",          "모건스탠리",            10, "2026-07-06", "금융-투자은행/자산관리(WM)·트레이딩·IB", "주식"),
    "IONQ": ("IONQ", "IonQ",                   "아이온큐",              9,  "2026-07-06", "기술-양자컴퓨팅/트랩드이온 하드웨어", "주식"),
    "SNDK": ("SNDK", "Sandisk",                "샌디스크",              11, "2026-07-06", "기술-반도체/NAND 플래시·스토리지", "주식"),
    "IBM":  ("IBM",  "IBM",                    "IBM",                   8,  "2026-07-06", "기술-IT서비스/하이브리드 클라우드·AI·양자", "주식"),
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
