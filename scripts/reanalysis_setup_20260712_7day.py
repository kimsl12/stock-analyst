#!/usr/bin/env python3
"""
재분석 setup — 2026-07-12 (7일 임계, 상한 20→10 클램핑, stock_update-2 슬롯)
fetch_price.py 로 10종 실시간 가격 수집 → analysis/{ticker}_{folder}_v{N}/data.json 생성.
_content.json 은 BLIND general-purpose 에이전트가 별도 작성.
제외: ANTHROPIC (비상장·비표준, standing 제외).
"""
import json, os, subprocess, sys

TODAY = "2026-07-12"
RUN = "20260712"
THRESHOLD = 7

# ticker -> (folder, name_kr, next_v, prev_v_date, asset_type, sector)
PLAN = {
    "UNP":  ("UnionPacific",   "유니온퍼시픽",         9, "2026-07-02", "주식", "산업재-철도/화물운송"),
    "USMV": ("iSharesMinVol",  "iShares 미국 최소변동성", 9, "2026-07-03", "ETF", "팩터 ETF-최소변동성(Min Vol)"),
    "UNH":  ("UnitedHealth",   "유나이티드헬스",       2, "2026-07-03", "주식", "헬스케어-매니지드케어/건강보험"),
    "TMO":  ("ThermoFisher",   "써모피셔사이언티픽",   2, "2026-07-03", "주식", "헬스케어-생명과학 도구/진단"),
    "SPGI": ("SPGlobal",       "S&P글로벌",            2, "2026-07-03", "주식", "금융-신용평가/지수/시장데이터"),
    "QCOM": ("Qualcomm",       "퀄컴",                 2, "2026-07-03", "주식", "반도체-모바일 SoC/무선/라이선싱"),
    "NOW":  ("ServiceNow",     "서비스나우",           2, "2026-07-03", "주식", "소프트웨어-엔터프라이즈 워크플로우/SaaS"),
    "NFLX": ("Netflix",        "넷플릭스",             2, "2026-07-03", "주식", "커뮤니케이션-스트리밍/미디어"),
    "MELI": ("MercadoLibre",   "메르카도리브레",       2, "2026-07-03", "주식", "임의소비재-이커머스/핀테크(중남미)"),
    "LNG":  ("CheniereEnergy", "셰니에르에너지",       2, "2026-07-03", "주식", "에너지-LNG 수출/인프라"),
}


def main():
    tickers = list(PLAN.keys())
    print(f"=== setup {TODAY} — fetch {len(tickers)}종 ===")
    res = subprocess.run(["python3", "scripts/fetch_price.py"] + tickers,
                         capture_output=True, text=True)
    text = res.stdout
    if "JSON_OUTPUT_START" not in text:
        print("FETCH FAILED\n", res.stdout[-2000:], res.stderr[-2000:])
        sys.exit(1)
    raw = text.split("JSON_OUTPUT_START", 1)[1].split("JSON_OUTPUT_END", 1)[0].strip()
    arr = json.loads(raw)
    by = {d["ticker"]: d for d in arr}

    for tk, (folder, kr, nv, prevdate, atype, sector) in PLAN.items():
        d = dict(by[tk])
        if d.get("currency") == "USD":
            d["currency"] = "$"
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
            "session_run": RUN,
            "sector": sector,
            "company_name_ko": kr,
            "prev_version_date": prevdate,
        }
        outdir = f"analysis/{tk}_{folder}_v{nv}"
        os.makedirs(outdir, exist_ok=True)
        with open(f"{outdir}/data.json", "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"[{tk}] v{nv} {outdir}  price={d.get('current_price')} atr={d.get('atr_14')} "
              f"stop={d.get('stop_loss_2atr')} target={d.get('target_3atr')} "
              f"52w={d.get('low_52w')}~{d.get('high_52w')} mcap={d.get('market_cap_str')}")


if __name__ == "__main__":
    main()
