#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-06-27 (10일 임계, 상한 10, staock_update 슬롯)
대상 10종 (10일 stale, 2026-06-17 분석분 v6/v3/v5/v7):
  PEP v7, PG v7, MU v7, MUU v4, ORCL v6, META v8, NVO v7, GLD v7, MA v7, MRK v7

각 종목 analysis/{ticker}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출).
_content.json 은 후속 BLIND 분석 에이전트가 작성.
ANTHROPIC(31일, 비상장·비표준) 은 standing 제외 — 후보 아님.
"""
import json, os, subprocess, sys

TODAY = "2026-06-27"
YYYYMMDD = "20260627"
PREV_DATE = "2026-06-17"
THRESHOLD = 10

# ticker -> (folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "PEP":  ("PepsiCo",            "펩시코",                        7, PREV_DATE, "필수소비재/음료·스낵", "주식"),
    "PG":   ("PG",                 "프록터앤드갬블(P&G)",            7, PREV_DATE, "필수소비재/생활용품", "주식"),
    "MU":   ("Micron",             "마이크론",                      7, PREV_DATE, "반도체/메모리(DRAM·HBM·NAND)", "주식"),
    "MUU":  ("DirexionDailyMU2X",  "디렉시온 마이크론 2배 레버리지 ETF", 4, PREV_DATE, "반도체/메모리 2x 레버리지(MU 기초)", "레버리지 ETF"),
    "ORCL": ("Oracle",             "오라클",                        6, PREV_DATE, "기술/엔터프라이즈 SW·클라우드(OCI)·AI인프라", "주식"),
    "META": ("Meta",               "메타플랫폼스",                   8, PREV_DATE, "커뮤니케이션서비스/소셜미디어·디지털광고·AI", "주식"),
    "NVO":  ("NovoNordisk",        "노보노디스크",                   7, PREV_DATE, "헬스케어/제약(GLP-1·당뇨·비만)", "주식"),
    "GLD":  ("SPDRGoldShares",     "SPDR 골드 셰어즈",               7, PREV_DATE, "원자재 / 금 현물", "ETF"),
    "MA":   ("Mastercard",         "마스터카드",                    7, PREV_DATE, "금융/결제 네트워크", "주식"),
    "MRK":  ("Merck",              "머크",                          7, PREV_DATE, "헬스케어/제약(종양·백신·면역)", "주식"),
}

CUR_MAP = {"USD": "$", "KRW": "₩"}


def fetch(ticker):
    out = subprocess.run([sys.executable, "scripts/fetch_price.py", ticker],
                         capture_output=True, text=True, timeout=120).stdout
    if "JSON_OUTPUT_START" not in out:
        raise RuntimeError(f"{ticker}: JSON 마커 없음")
    block = out.split("JSON_OUTPUT_START", 1)[1]
    block = block.split("JSON_OUTPUT_END", 1)[0].strip()
    arr = json.loads(block)
    return arr[0]


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    for ticker in only:
        folder, kr, nv, prev_date, sector, atype = PLAN[ticker]
        try:
            d = fetch(ticker)
            if d.get("current_price") in (None, 0) or d.get("atr_14") in (None, 0):
                raise RuntimeError(f"가격/ATR 누락: {d}")
            cur = CUR_MAP.get(d.get("currency", "USD"), d.get("currency"))
            d["currency"] = cur
            d["metadata"] = {
                "ticker": ticker,
                "company_name": d.get("name"),
                "company_name_ko": kr,
                "analysis_date": TODAY,
                "analysis_version": f"v{nv}",
                "analysis_mode": "BLIND_reanalysis",
                "asset_type": atype,
                "sector": sector,
                "currency": cur,
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
            out_dir = f"analysis/{ticker}_{folder}_v{nv}"
            os.makedirs(out_dir, exist_ok=True)
            with open(f"{out_dir}/data.json", "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            print(f"[{ticker}] OK v{nv} {cur}{d['current_price']} ATR {cur}{d['atr_14']} ({d['atr_pct']}%) date={d['date']} -> {out_dir}/data.json")
            ok.append(ticker)
        except Exception as e:
            print(f"  X {ticker}: FAILED — {e}")
            fail.append(ticker)
    print(f"\n=== 데이터 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
