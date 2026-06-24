#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-06-25 (7일 임계, 상한 20→10 클램핑, stock_update-2 슬롯)
대상 10종 (9일 stale, 2026-06-16 분석분):
  AVGO v8, ASTS v7, AMZN v7, AMAT v8, AGG v6, ABBV v6,
  035720 v7, 034020 v7, 012450 v7, 010120 v8

각 종목 analysis/{ticker}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출).
_content.json 은 후속 BLIND 분석 에이전트가 작성.
"""
import json, os, subprocess, sys

TODAY = "2026-06-25"
YYYYMMDD = "20260625"

# ticker -> (folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "AVGO":   ("Broadcom",                   "브로드컴",            8, "2026-06-16", "기술 / 반도체·AI ASIC·인프라SW", "주식"),
    "ASTS":   ("ASTSpaceMobile",             "AST스페이스모바일",   7, "2026-06-16", "통신 / 위성 직접연결(D2D)·우주", "주식"),
    "AMZN":   ("Amazon",                     "아마존",              7, "2026-06-16", "기술 / 이커머스·클라우드(AWS)·광고", "주식"),
    "AMAT":   ("AppliedMaterials",           "어플라이드머티리얼즈", 8, "2026-06-16", "기술 / 반도체 장비(WFE)", "주식"),
    "AGG":    ("iSharesCoreUSAggregateBond", "iShares미국종합채권",  6, "2026-06-16", "채권 ETF / 미국 투자등급 종합채권", "ETF"),
    "ABBV":   ("AbbVie",                     "애브비",              6, "2026-06-16", "헬스케어 / 제약(면역·신경·종양)", "주식"),
    "035720": ("카카오",                     "카카오",              7, "2026-06-16", "기술 / 플랫폼·핀테크·콘텐츠·AI", "주식"),
    "034020": ("두산에너빌리티",             "두산에너빌리티",      7, "2026-06-16", "산업재 / 원자력·SMR·발전설비", "주식"),
    "012450": ("한화에어로스페이스",         "한화에어로스페이스",  7, "2026-06-16", "방산 / 지상방산·항공엔진·우주", "주식"),
    "010120": ("LSELECTRIC",                 "LS일렉트릭",          8, "2026-06-16", "산업재 / 전력기기·자동화·전력인프라", "주식"),
}

CUR_MAP = {"USD": "$", "KRW": "₩"}


def fetch(ticker):
    out = subprocess.run([sys.executable, "scripts/fetch_price.py", ticker],
                         capture_output=True, text=True, timeout=120).stdout
    # JSON_OUTPUT_START ... JSON_OUTPUT_END 블록 추출
    if "JSON_OUTPUT_START" not in out:
        raise RuntimeError(f"{ticker}: JSON 마커 없음")
    block = out.split("JSON_OUTPUT_START", 1)[1]
    block = block.split("JSON_OUTPUT_END", 1)[0].strip()
    arr = json.loads(block)
    return arr[0]


def main():
    ok, fail = [], []
    for ticker, (folder, kr, nv, prev_date, sector, atype) in PLAN.items():
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
                "threshold_days": 7,
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
    print(f"\n=== data.json 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
