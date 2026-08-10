#!/usr/bin/env python3
"""재분석 데이터 수집 — 2026-08-11 (7일 임계, stock_update-2 슬롯, /재분석실행 7 20→cap10).
08-02 코호트 상장 10종(정확히 9일 경과). ANTHROPIC(76일) 비상장·비표준 standing 제외.
크립토(QuantTrader 별도) 제외. 당일 10일 런(staock_update)이 08-01 코호트 10종 선처리.
fetch_price 로 종가 수집 → analysis/{ticker}_{folder}_v{nv}/data.json + reanalysis 메타.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from fetch_price import fetch_us, fetch_korean, is_korean_ticker

TODAY = "2026-08-11"
RUN = "20260811b_7day"
THRESHOLD = 7

# ticker -> (folder, name_kr, next_v, prev_v, prev_date, sector)
PLAN = {
    "005380": ("현대차",            "현대차",           5,  4,  "2026-08-02", "자동차-완성차/전동화"),
    "005930": ("삼성전자",          "삼성전자",         12, 11, "2026-08-02", "기술-반도체/메모리·파운드리"),
    "009150": ("삼성전기",          "삼성전기",         12, 11, "2026-08-02", "기술-전자부품(MLCC/반도체기판)"),
    "207940": ("삼성바이오로직스",  "삼성바이오로직스", 5,  4,  "2026-08-02", "헬스케어-바이오의약품 CDMO"),
    "329180": ("HD현대중공업",      "HD현대중공업",     13, 12, "2026-08-02", "산업재-조선/방산"),
    "AAPL":   ("Apple",             "애플",             5,  4,  "2026-08-02", "기술-소비자 하드웨어/서비스"),
    "ABBV":   ("AbbVie",            "애브비",           11, 10, "2026-08-02", "헬스케어-제약(면역/신경/에스테틱)"),
    "ADBE":   ("Adobe",             "어도비",           13, 12, "2026-08-02", "기술-소프트웨어(크리에이티브/디지털미디어)"),
    "AMD":    ("AMD",               "AMD",              5,  4,  "2026-08-02", "기술-반도체(CPU/GPU/AI가속기)"),
    "ANET":   ("AristaNetworks",    "아리스타네트웍스", 11, 10, "2026-08-02", "기술-데이터센터 네트워킹"),
}

ETF_SET = set()  # 본 회차 ETF 없음


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    for ticker in only:
        folder, kr, nv, pv, pdate, sector = PLAN[ticker]
        out_dir = f"analysis/{ticker}_{folder}_v{nv}"
        os.makedirs(out_dir, exist_ok=True)
        try:
            d = fetch_korean(ticker) if is_korean_ticker(ticker) else fetch_us(ticker)
            if "error" in d:
                print(f"  X {ticker}: {d['error']}")
                fail.append(ticker); continue
            d["asset_type"] = "ETF" if ticker in ETF_SET else "주식"
            d["analysis_date"] = TODAY
            d["analysis_version"] = f"v{nv}"
            d["reanalysis"] = {
                "version": f"v{nv}",
                "previous_version": f"v{pv}",
                "blind_mode": True,
                "previous_files_read": 0,
                "reanalysis_date": TODAY,
                "threshold_days": THRESHOLD,
                "session_run": RUN,
                "sector": sector,
                "company_name_ko": kr,
                "prev_version_date": pdate,
            }
            with open(f"{out_dir}/data.json", "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            print(f"  OK {ticker} v{nv}: {d.get('currency','$')}{d.get('current_price')} "
                  f"(52w {d.get('low_52w')}~{d.get('high_52w')}, ATR {d.get('atr_14')} {d.get('atr_pct')}%)")
            ok.append(ticker)
        except Exception as e:
            print(f"  X {ticker}: {e}")
            fail.append(ticker)
    print(f"\n=== 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
