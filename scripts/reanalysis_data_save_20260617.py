#!/usr/bin/env python3
"""재분석 자동 실행 — 2026-06-17 (7일 임계, 상한 20→10 클램핑) — 10종 data.json 일괄 생성

대상: timeline.json 최신 v 날짜 기준 7일+ 경과 60종 중 경과일 상위 10종.
최우선 ANTHROPIC(21일)은 비상장·비표준(가격 fetch 불가) standing 제외 → 상장 9일 경과 배치 10종.
fetch_price 통화코드(USD/KRW) → 심볼($/₩) 변환 후 저장.
"""
import json, os, subprocess, sys
from datetime import datetime

TODAY = "2026-06-17"
YYYYMMDD = "20260617"
THRESHOLD = 7

# ticker -> (folder, kr_name, next_v, prev_v_date, sector)
PLAN = {
    "010120": ("LSELECTRIC",                "LS일렉트릭",      7, "2026-06-08", "산업재 / 전력기기·전력인프라"),
    "012450": ("한화에어로스페이스",        "한화에어로스페이스", 6, "2026-06-08", "방산 / 항공우주·엔진"),
    "034020": ("두산에너빌리티",            "두산에너빌리티",  6, "2026-06-08", "유틸리티/산업재 / 원자력·SMR·발전설비"),
    "035720": ("카카오",                    "카카오",          6, "2026-06-08", "커뮤니케이션 / 인터넷 플랫폼"),
    "ABBV":   ("AbbVie",                    "애브비",          5, "2026-06-08", "헬스케어 / 제약·바이오"),
    "AGG":    ("iSharesCoreUSAggregateBond","iShares 미국종합채권 ETF", 5, "2026-06-08", "채권 ETF / 미국 종합채권"),
    "AMAT":   ("AppliedMaterials",          "어플라이드 머티어리얼즈", 7, "2026-06-08", "기술 / 반도체 장비(WFE)"),
    "AMZN":   ("Amazon",                    "아마존",          6, "2026-06-08", "경기소비재 / e커머스·클라우드(AWS)"),
    "ASTS":   ("ASTSpaceMobile",            "AST 스페이스모바일", 6, "2026-06-08", "커뮤니케이션 / 위성통신(D2C)"),
    "AVGO":   ("Broadcom",                  "브로드컴",        7, "2026-06-08", "기술 / 반도체·AI ASIC·인프라SW"),
}

CUR_MAP = {"USD": "$", "KRW": "₩"}


def fetch_batch(tickers):
    proc = subprocess.run(
        ["python3", "scripts/fetch_price.py"] + tickers,
        capture_output=True, text=True
    )
    out = proc.stdout
    start = out.find("JSON_OUTPUT_START")
    end = out.find("JSON_OUTPUT_END")
    if start == -1 or end == -1:
        print("ERROR: JSON markers missing", file=sys.stderr)
        print(proc.stderr[-500:], file=sys.stderr)
        sys.exit(1)
    json_text = out[start + len("JSON_OUTPUT_START"):end].strip()
    return json.loads(json_text)


def main():
    all_tickers = list(PLAN.keys())
    data_list = fetch_batch(all_tickers)
    data_by_t = {d["ticker"]: d for d in data_list}

    ok, fail = [], []
    for ticker, (folder, kr, nv, prev_date, sector) in PLAN.items():
        d = data_by_t.get(ticker)
        if d is None:
            print(f"⚠️ {ticker}: fetch 실패")
            fail.append(ticker)
            continue
        # 통화 코드 → 심볼
        code = d.get("currency", "USD")
        d["currency"] = CUR_MAP.get(code, code)
        # 메타 보강
        d["metadata"] = {
            "ticker": ticker,
            "company_name": d.get("name", folder),
            "company_name_ko": kr,
            "analysis_date": TODAY,
            "analysis_version": f"v{nv}",
            "analysis_mode": "BLIND_reanalysis",
            "asset_type": "ETF" if "ETF" in sector else "주식",
            "sector": sector,
            "currency": d["currency"],
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
        print(f"✅ {ticker}: {d['currency']}{d.get('current_price')} (기준 {d.get('date')}) → {out_dir}/data.json")
        ok.append(ticker)

    print(f"\n=== data.json 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))
        sys.exit(2)


if __name__ == "__main__":
    main()
