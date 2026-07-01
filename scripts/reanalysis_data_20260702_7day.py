#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-02 (7일 임계, 상한 10, stock_update-2 슬롯)
대상 10종 (8~9일 stale, 2026-06-23~24 분석분):
  DIS v8, C v8, CAT v8, BRKB v8, BAC v8, BABA v8, AZN v8, ASML v8, V v8, VRT v6

각 종목 analysis/{ticker}_{folder}_v{nv}/ 생성 + price_seed.json 작성 (fetch_price.py 호출).
분석 .md + scorecard 는 후속 BLIND 분석가가 작성.
ANTHROPIC(36일, 비상장·비표준) 은 standing 제외 — 후보 아님.
"""
import json, os, subprocess, sys

TODAY = "2026-07-02"
YYYYMMDD = "20260702"
THRESHOLD = 7

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "DIS":  ("DIS",   "Disney",              "월트디즈니",           8, "2026-06-23", "커뮤니케이션서비스/미디어·엔터·스트리밍(DTC)·테마파크", "주식"),
    "C":    ("C",     "Citigroup",           "씨티그룹",             8, "2026-06-23", "금융/글로벌 유니버설 뱅크", "주식"),
    "CAT":  ("CAT",   "Caterpillar",         "캐터필러",             8, "2026-06-23", "산업재/건설·광산·에너지 중장비", "주식"),
    "BRKB": ("BRK-B", "BerkshireHathaway",   "버크셔해서웨이(B)",    8, "2026-06-23", "금융/보험·복합 지주", "주식"),
    "BAC":  ("BAC",   "BankOfAmerica",       "뱅크오브아메리카",     8, "2026-06-23", "금융/대형 상업은행", "주식"),
    "BABA": ("BABA",  "Alibaba",             "알리바바",             8, "2026-06-23", "중국 기술/이커머스·클라우드·AI", "주식"),
    "AZN":  ("AZN",   "AstraZeneca",         "아스트라제네카",       8, "2026-06-23", "헬스케어/제약(종양·희귀질환·심혈관)", "주식"),
    "ASML": ("ASML",  "ASML",                "ASML홀딩",             8, "2026-06-23", "반도체 장비/EUV 노광 독점", "주식"),
    "V":    ("V",     "Visa",                "비자",                 8, "2026-06-23", "금융/글로벌 결제 네트워크", "주식"),
    "VRT":  ("VRT",   "VertivHoldings",      "버티브홀딩스",         6, "2026-06-23", "산업재/데이터센터 인프라(전력·열관리)", "주식"),
}

CUR_MAP = {"USD": "$", "KRW": "₩"}


def fetch(fetch_ticker):
    out = subprocess.run([sys.executable, "scripts/fetch_price.py", fetch_ticker],
                         capture_output=True, text=True, timeout=120).stdout
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
            d["ticker"] = disp  # display ticker (BRKB 등 정규화)
            d["currency"] = cur
            d["metadata"] = {
                "ticker": disp,
                "fetch_ticker": fetch_ticker,
                "company_name": d.get("name"),
                "company_name_ko": kr,
                "analysis_date": TODAY,
                "analysis_version": f"v{nv}",
                "analysis_mode": "BLIND_reanalysis",
                "asset_type": atype,
                "sector": sector,
                "prev_version_date": prev_date,
            }
            d["reanalysis_meta"] = {
                "version": f"v{nv}",
                "previous_version": f"v{nv-1}",
                "blind_mode": True,
                "previous_files_read": 0,
                "reanalysis_date": TODAY,
                "threshold_days": THRESHOLD,
                "session_run": YYYYMMDD,
            }
            out_dir = f"analysis/{disp}_{folder}_v{nv}"
            os.makedirs(out_dir, exist_ok=True)
            with open(f"{out_dir}/price_seed.json", "w", encoding="utf-8") as f:
                json.dump([d], f, ensure_ascii=False, indent=2)
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
