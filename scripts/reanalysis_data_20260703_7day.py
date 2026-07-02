#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-03 (7일 임계, 상한 10, stock_update-2 슬롯)
대상 10종 (9일 stale, 2026-06-24 분석분 / 06-24 배치):
  AVGO v9, ASTS v8, AMZN v8, AMAT v9, AGG v7, ABBV v7,
  035720 카카오 v8, 034020 두산에너빌리티 v8, 012450 한화에어로스페이스 v8, 010120 LSELECTRIC v9

각 종목 analysis/{disp}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출, dict 형식).
분석 _content.json 은 후속 BLIND 분석가(general-purpose)가 작성.
ANTHROPIC(37일, 비상장·비표준) 은 standing 제외 — 후보 아님.
중앙 generator(reanalysis_generate_20260703_7day.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys

TODAY = "2026-07-03"
YYYYMMDD = "20260703"
THRESHOLD = 7

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "AVGO":   ("AVGO",   "Broadcom",                   "브로드컴",             9, "2026-06-24", "정보기술-반도체/AI ASIC·네트워킹·인프라SW(VMware)", "주식"),
    "ASTS":   ("ASTS",   "ASTSpaceMobile",             "AST스페이스모바일",    8, "2026-06-24", "통신서비스/위성-스마트폰 직접연결(D2D)", "주식"),
    "AMZN":   ("AMZN",   "Amazon",                     "아마존",               8, "2026-06-24", "임의소비재/이커머스·클라우드(AWS)·광고", "주식"),
    "AMAT":   ("AMAT",   "AppliedMaterials",           "어플라이드머티어리얼즈", 9, "2026-06-24", "정보기술-반도체장비/증착·식각·이온주입", "주식"),
    "AGG":    ("AGG",    "iSharesCoreUSAggregateBond", "iShares 미국종합채권", 7, "2026-06-24", "채권 ETF/미국 투자등급 종합채권", "ETF"),
    "ABBV":   ("ABBV",   "AbbVie",                     "애브비",               7, "2026-06-24", "헬스케어/제약(면역·종양·신경·미용)", "주식"),
    "035720": ("035720", "카카오",                      "카카오",               8, "2026-06-24", "커뮤니케이션서비스/플랫폼·핀테크·콘텐츠·AI", "주식"),
    "034020": ("034020", "두산에너빌리티",              "두산에너빌리티",       8, "2026-06-24", "산업재/발전설비·원자력(SMR)·풍력·수소", "주식"),
    "012450": ("012450", "한화에어로스페이스",          "한화에어로스페이스",   8, "2026-06-24", "산업재-방산/지상방산·항공엔진·우주", "주식"),
    "010120": ("010120", "LSELECTRIC",                 "LS일렉트릭",           9, "2026-06-24", "산업재/전력기기·자동화·배전(데이터센터 전력)", "주식"),
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
            d["ticker"] = disp            # display ticker
            d["fetch_ticker"] = fetch_ticker
            d["currency"] = cur           # 심볼로 변환 ($/₩)
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
            # generator 는 data.json 을 dict 로 로드 → dict 로 저장
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
