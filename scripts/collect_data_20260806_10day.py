#!/usr/bin/env python3
"""재분석 데이터 수집 — 2026-08-06 (10일 임계, staock_update 슬롯, /재분석실행 10 10).
07-25 코호트 개별주 10종(12일 경과). SSD 언마운트 장애(07-26~29) + 이후 재분석 공백으로 백로그 누적,
07-25 분석분이 12일까지 경과 → 본 10일 임계 런이 정상 흡수. ANTHROPIC(71일) 비상장·비표준 standing 제외.
동일 12일 경과 16종 중 개별 기업 10종 우선(재분석 정보가치 우위), 광범위 지수 ETF 6종은 차기 회차.
fetch_price 로 종가 수집 → analysis/{ticker}_{folder}_v{nv}/data.json + reanalysis 메타.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from fetch_price import fetch_us, fetch_korean, is_korean_ticker

TODAY = "2026-08-06"
RUN = "20260806_10day"
THRESHOLD = 10

# ticker -> (folder(이름만), name_kr, next_v, prev_v, prev_date, sector)
PLAN = {
    "TSM":    ("TSMC",                "TSMC",              11, 10, "2026-07-25", "반도체-파운드리(AI 가속기 위탁생산)"),
    "TXN":    ("TexasInstruments",    "텍사스인스트루먼트", 11, 10, "2026-07-25", "반도체-아날로그/임베디드"),
    "TTE":    ("TotalEnergies",       "토탈에너지",         11, 10, "2026-07-25", "에너지-종합 석유·가스·재생"),
    "TMUS":   ("TMobile",             "T-모바일",           12, 11, "2026-07-25", "통신-무선"),
    "TM":     ("Toyota",              "토요타",             10,  9, "2026-07-25", "자동차-하이브리드/완성차"),
    "CEG":    ("ConstellationEnergy", "컨스텔레이션에너지", 10,  9, "2026-07-25", "유틸리티-원자력 발전(AI 데이터센터 PPA)"),
    "CCJ":    ("Cameco",              "카메코",              6,  5, "2026-07-25", "에너지-우라늄 채굴/농축"),
    "052690": ("한전기술",            "한전기술",            5,  4, "2026-07-25", "원자력-엔지니어링/설계(SMR)"),
    "035420": ("NAVER",              "NAVER",              12, 11, "2026-07-25", "인터넷-플랫폼/커머스/AI"),
    "000720": ("현대건설",            "현대건설",            5,  4, "2026-07-25", "건설-플랜트/원전/토목"),
}

ETF_SET = set()  # 전 종목 개별주


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
                json.dump(d, f, ensure_ascii=False, indent=2, default=float)
            print(f"[{ticker}] OK v{nv} — {d.get('currency','$')}{d.get('current_price')} "
                  f"ATR {d.get('atr_14')} ({d.get('atr_pct')}%) 52w {d.get('low_52w')}~{d.get('high_52w')}")
            ok.append(ticker)
        except Exception as e:
            print(f"  X {ticker}: EXC {e}")
            import traceback; traceback.print_exc()
            fail.append(ticker)
    print(f"\n=== 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
