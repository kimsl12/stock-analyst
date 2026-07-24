#!/usr/bin/env python3
"""
재분석 데이터 수집 — 2026-07-25 (10일 임계, staock_update 슬롯, /재분석실행 10 10)
대상 6종 (경과일 desc, 10일 코호트 = 2026-07-15 분석분, 7일 런 일일 cap 으로 새어나온 백로그):
  052690 v4(한전기술), BWXT v5, DUK v5, LQD v4(ETF), MLSS v10, PLTR v11
- ANTHROPIC 비상장·비표준 standing 제외. 크립토(QuantTrader 별도) 제외.
- 각 종목 analysis/{ticker}_{folder}_v{nv}/ 생성 + data.json 작성 (fetch_price.py 호출).
- 052690.KS 는 최신 바(2026-07-24) Close=NaN(미정산) → history 폴백으로 재계산.
- 분석 _content.json 은 후속 BLIND 분석가가 작성.
- 중앙 generator(reanalysis_generate_20260725.py)가 data.json+_content.json 으로 6MD+scorecard+HTML.
"""
import json, os, subprocess, sys, math

TODAY = "2026-07-25"
YYYYMMDD = "20260725"
THRESHOLD = 10

# display_ticker -> (fetch_ticker, folder_name, kr_name, next_v, prev_v_date, sector, asset_type)
PLAN = {
    "052690": ("052690.KS", "한전기술",                       "한전기술(KEPCO E&C)",      4, "2026-07-15", "원자력-엔지니어링/원전설계·SMR·해외수주(체코·중동)", "주식"),
    "BWXT":   ("BWXT",       "BWXTechnologies",               "BWX테크놀로지스",          5, "2026-07-15", "원자력-방산/해군원자로·SMR·의료동위원소·정부계약", "주식"),
    "DUK":    ("DUK",        "DukeEnergy",                    "듀크에너지",               5, "2026-07-15", "유틸리티-전력/규제유틸·전력수요증가·데이터센터", "주식"),
    "LQD":    ("LQD",        "iSharesInvestmentGradeCorpBond", "iShares 투자등급 회사채 ETF", 4, "2026-07-15", "채권-투자등급회사채/듀레이션·크레딧스프레드·금리", "ETF"),
    "MLSS":   ("MLSS",       "MilestoneScientific",           "마일스톤사이언티픽",       10, "2026-07-15", "헬스케어-의료기기/컴퓨터제어약물주입·마이크로캡", "주식"),
    "PLTR":   ("PLTR",       "Palantir",                      "팔란티어",                 11, "2026-07-15", "기술-소프트웨어/데이터분석·AIP·정부·상업AI", "주식"),
}

CUR_MAP = {"USD": "$", "KRW": "₩"}


def _is_bad(v):
    return v is None or (isinstance(v, float) and math.isnan(v)) or v == 0


def history_fallback(fetch_ticker):
    """fetch_price 가 NaN 반환 시 yfinance history 로 종가/ATR 재계산."""
    import yfinance as yf, pandas as pd
    t = yf.Ticker(fetch_ticker)
    h = t.history(period="6mo", auto_adjust=False).dropna(subset=["Close"])
    if len(h) < 20:
        raise RuntimeError(f"{fetch_ticker}: history 부족 ({len(h)}행)")
    hi, lo, cl = h["High"], h["Low"], h["Close"]
    pc = cl.shift(1)
    tr = pd.concat([(hi - lo), (hi - pc).abs(), (lo - pc).abs()], axis=1).max(axis=1)
    atr = float(tr.rolling(14).mean().iloc[-1])
    price = float(cl.iloc[-1])
    last_date = str(h.index[-1].date())
    win = h.tail(252)
    return {
        "current_price": round(price, 2),
        "prev_close": round(float(cl.iloc[-2]), 2),
        "atr_14": round(atr, 2),
        "atr_pct": round(atr / price * 100, 2),
        "high_52w": round(float(win["High"].max()), 2),
        "low_52w": round(float(win["Low"].min()), 2),
        "stop_loss_2atr": round(price - 2 * atr, 2),
        "target_3atr": round(price + 3 * atr, 2),
        "date": last_date,
    }


def fetch(fetch_ticker):
    out = subprocess.run([sys.executable, "scripts/fetch_price.py", fetch_ticker],
                         capture_output=True, text=True, timeout=240).stdout
    if "JSON_OUTPUT_START" not in out:
        raise RuntimeError(f"{fetch_ticker}: JSON 마커 없음")
    block = out.split("JSON_OUTPUT_START", 1)[1].split("JSON_OUTPUT_END", 1)[0].strip()
    d = json.loads(block)[0]
    # NaN → JSON 은 NaN 토큰을 문자열로 안 담으므로 json.loads 시 float('nan') 가능
    if _is_bad(d.get("current_price")) or _is_bad(d.get("atr_14")):
        fb = history_fallback(fetch_ticker)
        d.update(fb)
        d["_fallback"] = "history_recompute (fetch_price NaN)"
    return d


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    for disp in only:
        fetch_ticker, folder, kr, nv, prev_date, sector, atype = PLAN[disp]
        try:
            d = fetch(fetch_ticker)
            if _is_bad(d.get("current_price")) or _is_bad(d.get("atr_14")):
                raise RuntimeError(f"가격/ATR 누락(폴백 후에도): {d.get('current_price')}/{d.get('atr_14')}")
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
            fb = " [폴백]" if d.get("_fallback") else ""
            print(f"[{disp}] OK v{nv} {cur}{d['current_price']} ATR {cur}{d['atr_14']} ({d['atr_pct']}%) "
                  f"손절 {cur}{d.get('stop_loss_2atr')} 목표 {cur}{d.get('target_3atr')} date={d['date']}{fb} -> {out_dir}/")
            ok.append(disp)
        except Exception as e:
            print(f"  X {disp}: FAILED — {e}")
            fail.append(disp)
    print(f"\n=== 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
