#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-22 (10일 임계, 상한 10, staock_update 슬롯)
대상 3종 (timeline 사각지대 교정으로 신규 검출, 모두 2026-06-12 분석 → 40일 경과):
  QUAL v2, SGOV v2, VEA v2 (모두 ETF)
- 기존 v 접미사 없는 폴더 → _v1 리네임 완료 (etf.md 단독 구조, ETF 파이프라인 산출물)
- ANTHROPIC(56일)·SPACEX(41일) 은 비상장·비표준 standing 제외.
- 각 종목 analysis/{ticker}_{folder}_v2/ 생성 + data.json 작성 (fetch_price.py 호출).
- 분석 _content.json 은 후속 BLIND 분석가가 작성.
"""
import json, os, subprocess, sys

TODAY = "2026-07-22"
YYYYMMDD = "20260722"
THRESHOLD = 10

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "QUAL": ("QUAL", "iSharesMSCIQuality",       "iShares MSCI USA 퀄리티 팩터 ETF", 2, "2026-06-12", "팩터 ETF-퀄리티(ROE·부채·이익안정성) 대형주", "ETF"),
    "SGOV": ("SGOV", "iShares0-3MonthTreasury",  "iShares 0-3개월 미국채 ETF",       2, "2026-06-12", "채권 ETF-초단기 미국채(현금성·듀레이션 0.1년)", "ETF"),
    "VEA":  ("VEA",  "VanguardDevelopedMarkets", "뱅가드 선진국(미국제외) ETF",      2, "2026-06-12", "글로벌 주식 ETF-선진국 미국제외(유럽·일본 중심)", "ETF"),
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
        out_dir = f"analysis/{disp}_{folder}_v{nv}"
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
            d["prev_version_date"] = prev_date
            d["sector"] = sector
            d["name_kr"] = kr
            os.makedirs(out_dir, exist_ok=True)
            with open(f"{out_dir}/data.json", "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            print(f"[{disp}] OK — {cur}{d['current_price']} / ATR {d['atr_14']} ({d.get('atr_pct')}%) → {out_dir}/data.json")
            ok.append(disp)
        except Exception as e:
            print(f"  X {disp}: FAILED — {e}")
            fail.append(disp)
    print(f"\n=== 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
