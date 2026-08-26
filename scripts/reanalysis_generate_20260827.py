#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 HTML/MD 생성 — 2026-08-27 (10일 임계, 상한 10, staock_update 슬롯, /재분석실행 10 10).
08-17 코호트(10일) 중 티커 오름차순 상위 10종 (ANTHROPIC 비상장 standing 제외).
7일런(cap 10/일)이 ~147종 유니버스를 10일 내 다 못 덮어 새어나온 오버플로 코호트.
- BLIND: 분석가(Agent 10종 병렬)가 _content.json 작성 (이전 v·HTML·timeline 미참조)
- 가격/펀더멘털: analysis/{folder}_v{N}/data.json (collect_data_20260827_10day.py, yfinance 리치 수집)
- extra_kpis(정량 KPI 표)는 data.json에서 메인이 중앙 주입 → 숫자 전사 오류 차단
- 통화 인식(KRW/USD): 컨센 평균목표·FCF 등 심볼 자동 · 한국 티커는 D/E·FCF 스케일 혼동 방지 위해 억제
- 배당수익률: 실측 유효 티커만 표기(0<dyp<=8 게이트) → yfinance 스케일 아티팩트 차단
- 출력: 종목당 6개 MD + HTML 리포트.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from report_template import generate_report

TODAY = "2026-08-27"
YYYYMMDD = "20260827"
RUN_MD = "20260827_run"
THRESHOLD = 10

CUR_SYMBOL = {"KRW": "₩", "USD": "$"}

# ticker -> (folder, name_kr, name_en, next_v, prev_date)
PLAN = {
    "010120": ("LSELECTRIC",                 "LS일렉트릭",           "LS Electric",                        15, "2026-08-17"),
    "012450": ("한화에어로스페이스",          "한화에어로스페이스",   "Hanwha Aerospace",                   14, "2026-08-17"),
    "034020": ("두산에너빌리티",              "두산에너빌리티",       "Doosan Enerbility",                  14, "2026-08-17"),
    "035720": ("카카오",                      "카카오",               "Kakao",                              14, "2026-08-17"),
    "AGG":    ("iSharesCoreUSAggregateBond", "AGG",                 "iShares Core US Aggregate Bond ETF", 13, "2026-08-17"),
    "AMAT":   ("AppliedMaterials",           "어플라이드머티리얼즈", "Applied Materials",                  15, "2026-08-17"),
    "ASML":   ("ASML",                       "ASML",                "ASML Holding",                       14, "2026-08-17"),
    "ASTS":   ("ASTSpaceMobile",             "AST스페이스모바일",    "AST SpaceMobile",                    14, "2026-08-17"),
    "AVGO":   ("Broadcom",                   "브로드컴",             "Broadcom",                           15, "2026-08-17"),
    "AZN":    ("AstraZeneca",                "아스트라제네카",       "AstraZeneca",                        14, "2026-08-17"),
}

KR_TICKERS = {"010120", "012450", "034020", "035720"}
# 배당수익률 실측 유효 티커만 표기 — 게이트(0<dyp<=8)로 yfinance 스케일 아티팩트 차단
KEEP_DIV = {"AZN", "AVGO", "AMAT", "ASML", "AGG"}


def _cur(d):
    return CUR_SYMBOL.get(d.get("meta", {}).get("currency", "USD"), "$")


def _fmt(v):
    if isinstance(v, (int, float)):
        return f"{v:,}"
    return str(v)


def _pct(v):
    return f"{v*100:.1f}%" if isinstance(v, (int, float)) else "N/A"


def build_extra_kpis(ticker, d, c, nv):
    """data.json(신 스키마) 에서 정량 KPI 표를 중앙 주입. 통화 인식."""
    kpis = []
    cur = _cur(d)
    q = d.get("quote") or {}
    val = d.get("valuation") or {}
    prof = d.get("profitability") or {}
    grw = d.get("growth") or {}
    bal = d.get("balance_sheet") or {}
    cons = d.get("consensus") or {}
    cp = q.get("current_price")

    def add(label, v):
        if v is not None and v != "":
            kpis.append([label, v])

    if val.get("forwardPE") is not None and val["forwardPE"] > 0:
        add("선행 PER", f"{val['forwardPE']:.1f}x")
    if val.get("priceToBook") is not None:
        add("P/B", f"{val['priceToBook']:.2f}x")
    if val.get("pegRatio") is not None:
        add("PEG", f"{val['pegRatio']:.2f}")
    if prof.get("returnOnEquity") is not None:
        add("ROE", _pct(prof["returnOnEquity"]))
    if prof.get("grossMargins") is not None and not (ticker == "035420"):  # NAVER GM=1.0 아티팩트
        add("매출총이익률", _pct(prof["grossMargins"]))
    if prof.get("operatingMargins") is not None:
        add("영업이익률", _pct(prof["operatingMargins"]))
    if prof.get("profitMargins") is not None:
        add("순이익률", _pct(prof["profitMargins"]))
    if grw.get("revenueGrowth_yoy") is not None:
        add("매출성장(YoY)", _pct(grw["revenueGrowth_yoy"]))
    # 배당수익률 — KEEP_DIV 만 (나머지 아티팩트)
    dyp = val.get("dividendYield_pct")
    if dyp is not None and ticker in KEEP_DIV and 0 < dyp <= 8:
        add("배당수익률", f"{dyp:.2f}%")
    if q.get("beta") is not None:
        add("베타", f"{q['beta']:.2f}")
    # 부채/자본 — 한국 티커는 스케일 혼동으로 억제
    if bal.get("debtToEquity") is not None and ticker not in KR_TICKERS:
        add("부채/자본", f"{bal['debtToEquity']:.1f}%")
    # FCF — 한국(KRW)은 스케일 심볼 혼동으로 억제, 미국만 표기
    if bal.get("freeCashflow_ttm") and ticker not in KR_TICKERS:
        fcf = bal["freeCashflow_ttm"]
        add("FCF(TTM)", f"{cur}{fcf/1e9:.1f}B")

    tmean = cons.get("targetMeanPrice")
    if tmean and cp:
        add("컨센 평균목표", f"{cur}{_fmt(round(tmean,2))} ({(tmean/cp-1)*100:+.1f}%)")
    if cons.get("recommendationKey") and cons["recommendationKey"] != "none":
        rk = cons["recommendationKey"]
        rm = cons.get("recommendationMean")
        add("컨센 투자의견", f"{rk}" + (f" ({rm:.2f})" if rm else ""))
    if cons.get("numberOfAnalystOpinions"):
        add("애널리스트 수", f"{cons['numberOfAnalystOpinions']}명")

    add("재분석", f"v{nv} BLIND")
    return kpis


def make_md_files(ticker, folder, kr, nv, prev_date, c, d):
    out_dir = f"analysis/{ticker}_{folder}_v{nv}"
    cur = _cur(d)
    q = d.get("quote") or {}
    prevv = nv - 1
    price = q.get("current_price")
    atr = q.get("atr_14")
    atr_pct = q.get("atr_pct")
    lo52 = q.get("fiftyTwoWeekLow")
    hi52 = q.get("fiftyTwoWeekHigh")
    stop2 = q.get("stop_loss_2atr")
    pdate = d.get("meta", {}).get("price_as_of", "2026-08-26")
    conf = c["confidence"]

    company_md = f"""# {kr} ({ticker}) — 기업개요 & Moat (BLIND v{nv} 재분석)

> **재분석 모드**: BLIND v{nv} (이전 v{prevv} 절대 read 안 함)
> **재분석 일자**: {TODAY} · **데이터 기준일**: {pdate}

## Executive Summary

{c['summary']}

## Moat 평가: {c['moat_rating']}

{c['moat_details']}

## 산업 위치 + 종합

- **섹터**: {c['sector']}
- **카테고리**: {c['category']}
- **종합 등급**: {c['grade']} (스코어 {c['score']}/100)
"""

    financial_md = f"""# {kr} ({ticker}) — 재무 분석 (BLIND v{nv})

> **BLIND 모드 — 이전 v{prevv} read 0건**

## 최근 실적 + 재무 상태

{c['financial']}

## 밸류에이션

{c['valuation']}

## 가격 정보 ({pdate} 기준)

- 현재가 {cur}{_fmt(price)} / ATR(14) {cur}{_fmt(atr)} ({atr_pct}%)
- 52주 범위 {cur}{_fmt(lo52)} ~ {cur}{_fmt(hi52)}
- 손절(2ATR) {cur}{_fmt(stop2)} / 목표(base) {cur}{_fmt(conf['target_mid'])}
- 상세 data.json 참조
"""

    business_md = f"""# {kr} ({ticker}) — 사업/산업 분석 (BLIND v{nv})

> **BLIND 모드 — 이전 v{prevv} read 0건**

## 산업 동향 + 경쟁 구도 + 메가트렌드

{c['business']}
"""

    momentum_md = f"""# {kr} ({ticker}) — 모멘텀 + 컨센서스 (BLIND v{nv})

> **BLIND 모드 — 이전 v{prevv} read 0건**

## 최근 모멘텀 + 컨센서스 + 수급

{c['momentum']}

## 컨센서스 표

| 항목 | 값 |
|------|-----|
""" + "\n".join(f"| {k} | {v} |" for k, v in c['consensus']) + "\n"

    risk_md = f"""# {kr} ({ticker}) — 리스크 분석 (BLIND v{nv})

> **BLIND 모드 — 이전 v{prevv} read 0건**

## 주요 리스크

"""
    for r in c['risks']:
        risk_md += f"""### {r['name']} ({r['level']})

- **영향**: {r['impact']}
- **상세**: {r['desc']}

"""
    risk_md += f"""## 리스크 종합

{c['risk_summary']}
"""

    sc_md = f"""# {kr} ({ticker}) — 종합 스코어카드 (BLIND v{nv})

> **재분석 v{nv}** — 이전 v{prevv} 비교 미포함 (Phase 2 reanalysis_runs/{RUN_MD}.md 참조)
> **BLIND 모드 — 이전 v{prevv} read 0건**

## 종합 평가

- **종합점수 = {c['score']}/100**
- **투자 등급: {c['grade']}**
- **카테고리**: {c['category']}
- **목표가**: {cur}{_fmt(conf['target_mid'])}

## 10항목 스코어카드

| # | 항목 | 점수 | 가중 |
|---|------|------|------|
"""
    for i, (n, s) in enumerate(c['scorecard_items'], 1):
        sc_md += f"| {i} | {n} | {float(s):.1f}/10 | 10% |\n"

    sc_md += f"""
## 손절가 / 목표가

- **손절가 = 현재가 − 2×ATR14 = {cur}{_fmt(stop2)}**
- **목표가(base) = {cur}{_fmt(conf['target_mid'])}**

## 투자 전략

{c['strategy']}

## §Confidence Interval (95% CI)

- **목표가 범위**: {cur}{_fmt(conf['target_low'])} ~ {cur}{_fmt(conf['target_high'])} (중심 {cur}{_fmt(conf['target_mid'])}, {conf['ci_pct']})
- **스코어 ±밴드**: {conf['score_band']} (가정 변경 시 변동 폭)
- **시나리오 분기**: 강세 {cur}{_fmt(conf['target_high'])} / 기본 {cur}{_fmt(conf['target_mid'])} / 약세 {cur}{_fmt(conf['target_low'])}

## §약한 가정 3개 (Most Fragile Assumptions)

"""
    for i, (assumption, impact) in enumerate(c['fragile_assumptions'], 1):
        sc_md += f"{i}. **{assumption}** — _반증 시 영향_: {impact}\n"

    sc_md += f"""
---

> 본 스코어카드는 **{TODAY} BLIND 재분석 v{nv}**입니다.
> 이전 v{prevv} ({prev_date}) 와의 차이는 `analysis/_reanalysis_runs/{RUN_MD}.md` 비교표 참조.
"""

    files = {
        f"{out_dir}/company.md": company_md,
        f"{out_dir}/financial.md": financial_md,
        f"{out_dir}/business.md": business_md,
        f"{out_dir}/momentum.md": momentum_md,
        f"{out_dir}/risk.md": risk_md,
        f"{out_dir}/scorecard.md": sc_md,
    }
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return out_dir


def make_html_report(ticker, folder, kr, name_en, nv, prev_date, c, d):
    cur = _cur(d)
    q = d.get("quote") or {}
    conf = c["confidence"]
    prevv = nv - 1
    report_data = {
        "ticker": ticker,
        "name": f"{name_en} — 재분석 v{nv} (이전 비교 미포함)",
        "date": TODAY,
        "score": c["score"],
        "grade": c.get("grade_label") or c["grade"],
        "current_price": q.get("current_price"),
        "currency": cur,
        "market_cap": q.get("marketCap"),
        "per": c.get("per", "N/A"),
        "low52": q.get("fiftyTwoWeekLow"),
        "high52": q.get("fiftyTwoWeekHigh"),
        "asset_type": c.get("asset_type", "주식"),
        "stop_loss": q.get("stop_loss_2atr"),
        "target_price": conf.get("target_mid"),
        "atr": q.get("atr_14"),
        "executive_summary": c["summary"],
        "company_overview": c["summary"],
        "moat_rating": c["moat_rating"],
        "moat_details": c["moat_details"],
        "financial_analysis": c["financial"],
        "valuation": c["valuation"],
        "momentum": c["momentum"],
        "business_analysis": c["business"],
        "scorecard_items": [(n, float(s)) for n, s in c["scorecard_items"]],
        "risks": c["risks"],
        "risk_summary": c["risk_summary"],
        "strategy": c["strategy"],
        "thesis": c.get("thesis"),
        "consensus_table": {
            "headers": ["항목", "값"],
            "rows": [[k, v] for k, v in c["consensus"]]
        },
        "extra_kpis": build_extra_kpis(ticker, d, c, nv),
        "custom_sections": [
            {
                "title": "§ Confidence Interval (95% CI)",
                "content": (
                    f"**목표가 범위**: {cur}{_fmt(conf['target_low'])} ~ {cur}{_fmt(conf['target_high'])}"
                    f" (중심 {cur}{_fmt(conf['target_mid'])}, {conf['ci_pct']})\n\n"
                    f"**스코어 ±밴드**: {conf['score_band']}\n\n"
                    f"**시나리오 분기**:\n"
                    f"- 강세: {cur}{_fmt(conf['target_high'])}\n"
                    f"- 기본: {cur}{_fmt(conf['target_mid'])}\n"
                    f"- 약세: {cur}{_fmt(conf['target_low'])}"
                )
            },
            {
                "title": "§ 약한 가정 3개 (Most Fragile Assumptions)",
                "content": "\n\n".join([
                    f"**{i+1}. {assum}**\n\n반증 시 영향: {impact}"
                    for i, (assum, impact) in enumerate(c['fragile_assumptions'])
                ])
            },
            {
                "title": f"재분석 메타 (v{nv} BLIND)",
                "content": (
                    f"- **재분석 회차**: v{nv} (이전 v{prevv}, {prev_date})\n"
                    f"- **모드**: BLIND (이전 v{prevv} read 0건, 구조적 앵커링 차단)\n"
                    f"- **임계**: {THRESHOLD}일 (상한 10종, staock_update 슬롯, {TODAY})\n"
                    f"- **데이터**: yfinance 단일계열({d.get('meta',{}).get('price_as_of','2026-08-26')} 종가)\n"
                    f"- **회차 보고**: `analysis/_reanalysis_runs/{RUN_MD}.md`"
                )
            }
        ]
    }
    output_path = f"reports/{ticker}_{folder}_{YYYYMMDD}.html"
    generate_report(report_data, output_path=output_path)
    return output_path


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    print(f"=== 재분석 생성 — {TODAY} ({THRESHOLD}일, 상한 10) BLIND — {len(only)}종 ===\n")
    ok, fail = [], []
    for ticker in only:
        folder, kr, name_en, nv, prev_date = PLAN[ticker]
        cpath = f"analysis/{ticker}_{folder}_v{nv}/_content.json"
        dpath = f"analysis/{ticker}_{folder}_v{nv}/data.json"
        if not os.path.exists(cpath):
            print(f"  ⏸ {ticker}: _content.json 없음 — SKIP")
            fail.append(ticker)
            continue
        try:
            c = json.load(open(cpath, encoding="utf-8"))
            d = json.load(open(dpath, encoding="utf-8"))
            make_md_files(ticker, folder, kr, nv, prev_date, c, d)
            html = make_html_report(ticker, folder, kr, name_en, nv, prev_date, c, d)
            print(f"[{ticker}] OK v{nv} score {c['score']} {c['grade']} MD(6)+HTML: {html}")
            ok.append(ticker)
        except Exception as e:
            print(f"  X {ticker}: FAILED — {e}")
            import traceback; traceback.print_exc()
            fail.append(ticker)
    print(f"\n=== 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
