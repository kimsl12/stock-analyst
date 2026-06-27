#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-06-28 (7일 임계, 상한 10, stock_update-2 슬롯)
대상 10종 (9일 stale, 2026-06-19 분석분):
  009150 삼성전기 v7, 329180 HD현대중공업 v8, 466100 클로봇 v7, ADBE v8, ANET v6,
  BHP v8, COIN v8, COST v8, HOOD v7, IONQ v7

각 종목 analysis/{ticker}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출).
_content.json 은 후속 BLIND 분석 에이전트가 작성.
ANTHROPIC(32일, 비상장·비표준) 은 standing 제외 — 후보 아님.
"""
import json, os, subprocess, sys

TODAY = "2026-06-28"
YYYYMMDD = "20260628"
PREV_DATE = "2026-06-19"
THRESHOLD = 7

# ticker -> (folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "009150": ("삼성전기",        "삼성전기",          7, PREV_DATE, "IT/전자부품 (MLCC·반도체 패키지기판·카메라모듈)", "주식"),
    "329180": ("HD현대중공업",    "HD현대중공업",      8, PREV_DATE, "조선/방산 (상선·해양·엔진)", "주식"),
    "466100": ("클로봇",          "클로봇",            7, PREV_DATE, "로보틱스/자동화 (서비스로봇·자율주행 SW)", "주식"),
    "ADBE":   ("Adobe",           "어도비",            8, PREV_DATE, "기술/소프트웨어 (크리에이티브·디지털미디어·AI)", "주식"),
    "ANET":   ("AristaNetworks",  "아리스타 네트웍스", 6, PREV_DATE, "기술/네트워킹 하드웨어 (데이터센터 스위칭·AI 네트워크)", "주식"),
    "BHP":    ("BHPGroup",        "BHP 그룹",          8, PREV_DATE, "소재/광업 (철광석·구리·니켈)", "주식"),
    "COIN":   ("Coinbase",        "코인베이스",        8, PREV_DATE, "금융/크립토 거래소", "주식"),
    "COST":   ("Costco",          "코스트코",          8, PREV_DATE, "필수소비재/창고형 소매", "주식"),
    "HOOD":   ("Robinhood",       "로빈후드",          7, PREV_DATE, "금융/핀테크 (리테일 브로커리지·크립토)", "주식"),
    "IONQ":   ("IonQ",            "아이온큐",          7, PREV_DATE, "기술/양자컴퓨팅 (이온트랩)", "주식"),
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
