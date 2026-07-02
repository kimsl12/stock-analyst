#!/usr/bin/env python3
"""
재분석 자동 실행 — 2026-07-03 (7일 임계, 상한 10, stock_update-2 슬롯)
대상 10종 (9일 stale, 06-24 배치):
  AVGO v9, ASTS v8, AMZN v8, AMAT v9, AGG v7, ABBV v7,
  035720 카카오 v8, 034020 두산에너빌리티 v8, 012450 한화에어로스페이스 v8, 010120 LSELECTRIC v9
- BLIND: general-purpose 에이전트가 _content.json 작성 (이전 v·HTML·timeline 미참조)
- 가격: analysis/{folder}_v{N}/data.json (사전 fetch_price.py 수집, 종가 2026-07-02)
- 출력: 종목당 6개 MD + scorecard + HTML 리포트
- 회차 보고: analysis/_reanalysis_runs/20260703_run_7day.md (메인이 별도 작성)
- 제외: ANTHROPIC (비상장·비표준, standing 제외)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from report_template import generate_report

TODAY = "2026-07-03"
YYYYMMDD = "20260703"
RUN_MD = "20260703_run_7day"
THRESHOLD = 7

# ticker -> (folder_name, name_kr, next_v, prev_v_date)
PLAN = {
    "AVGO":   ("Broadcom",                   "브로드컴",             9, "2026-06-24"),
    "ASTS":   ("ASTSpaceMobile",             "AST스페이스모바일",    8, "2026-06-24"),
    "AMZN":   ("Amazon",                     "아마존",               8, "2026-06-24"),
    "AMAT":   ("AppliedMaterials",           "어플라이드머티어리얼즈", 9, "2026-06-24"),
    "AGG":    ("iSharesCoreUSAggregateBond", "iShares 미국종합채권", 7, "2026-06-24"),
    "ABBV":   ("AbbVie",                     "애브비",               7, "2026-06-24"),
    "035720": ("카카오",                      "카카오",               8, "2026-06-24"),
    "034020": ("두산에너빌리티",              "두산에너빌리티",       8, "2026-06-24"),
    "012450": ("한화에어로스페이스",          "한화에어로스페이스",   8, "2026-06-24"),
    "010120": ("LSELECTRIC",                 "LS일렉트릭",           9, "2026-06-24"),
}


def _fmt(v):
    if isinstance(v, (int, float)):
        return f"{v:,}"
    return str(v)


def make_md_files(ticker, folder, kr, nv, prev_date, c, d):
    out_dir = f"analysis/{ticker}_{folder}_v{nv}"
    cur = d.get("currency", "$")
    prevv = nv - 1

    company_md = f"""# {kr} ({ticker}) — 기업개요 & Moat (BLIND v{nv} 재분석)

> **재분석 모드**: BLIND v{nv} (이전 v{prevv} 절대 read 안 함)
> **재분석 일자**: {TODAY}
> **데이터 기준일**: {d.get('date')}

## Executive Summary

{c['summary']}

## Moat 평가: {c['moat_rating']}

{c['moat_details']}

## 산업 위치 + 경쟁 우위

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

## 가격 정보 ({d.get('date')} 기준)

- 현재가 {cur}{_fmt(d.get('current_price'))} / ATR(14) {cur}{_fmt(d.get('atr_14'))} ({d.get('atr_pct')}%)
- 52주 범위 {cur}{_fmt(d.get('low_52w'))} ~ {cur}{_fmt(d.get('high_52w'))}
- 손절(2ATR) {cur}{_fmt(d.get('stop_loss_2atr'))} / 목표(3ATR) {cur}{_fmt(d.get('target_3atr'))}
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

    conf = c['confidence']
    sc_md = f"""# {kr} ({ticker}) — 종합 스코어카드 (BLIND v{nv})

> **재분석 v{nv}** — 이전 v{prevv} 비교 미포함 (Phase 2 reanalysis_runs/{RUN_MD}.md 참조)
> **BLIND 모드 — 이전 v{prevv} read 0건**

## 종합 평가

- **종합 점수**: {c['score']}/100
- **투자 등급**: {c['grade']}
- **카테고리**: {c['category']}

## 10항목 스코어카드

| # | 항목 | 점수 | 가중 |
|---|------|------|------|
"""
    for i, (n, s) in enumerate(c['scorecard_items'], 1):
        sc_md += f"| {i} | {n} | {float(s):.1f}/10 | 10% |\n"

    sc_md += f"""
## 투자 전략

{c['strategy']}

## § Confidence Interval (95% CI)

- **목표가 범위**: {cur}{_fmt(conf['target_low'])} ~ {cur}{_fmt(conf['target_high'])} (중심 {cur}{_fmt(conf['target_mid'])}, {conf['ci_pct']})
- **스코어 ±밴드**: {conf['score_band']} (가정 변경 시 변동 폭)
- **시나리오 분기**:
  - **강세 시나리오**: 목표가 {cur}{_fmt(conf['target_high'])}
  - **기본 시나리오**: 목표가 {cur}{_fmt(conf['target_mid'])}
  - **약세 시나리오**: 목표가 {cur}{_fmt(conf['target_low'])}

## § 약한 가정 3개 (Most Fragile Assumptions)

본 결론을 뒤집을 수 있는 핵심 가정 3개:

"""
    for i, (assumption, impact) in enumerate(c['fragile_assumptions'], 1):
        sc_md += f"{i}. **{assumption}**\n   - 반증 시 영향: {impact}\n\n"

    sc_md += f"""## 카탈리스트 + 모니터링 포인트

분석 본문 참조. 핵심 KPI:
- {c['risks'][0]['name']}
- {c['risks'][1]['name']}

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


def make_html_report(ticker, folder, kr, nv, prev_date, c, d):
    cur = d.get("currency", "$")
    conf = c['confidence']
    prevv = nv - 1
    report_data = {
        "ticker": ticker,
        "name": f"{kr} ({folder})",
        "date": TODAY,
        "score": c["score"],
        "grade": c["grade"],
        "current_price": d["current_price"],
        "currency": cur,
        "market_cap": d.get("market_cap"),
        "per": c.get("per", "N/A"),
        "low52": d.get("low_52w"),
        "high52": d.get("high_52w"),
        "asset_type": c.get("asset_type", "주식"),
        "stop_loss": d.get("stop_loss_2atr"),
        "target_price": d.get("target_3atr"),
        "atr": d.get("atr_14"),
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
        "consensus_table": {
            "headers": ["항목", "값"],
            "rows": [[k, v] for k, v in c["consensus"]]
        },
        "extra_kpis": [
            ("등급", c["grade"]),
            ("재분석", f"v{nv} BLIND"),
        ],
        "custom_sections": [
            {
                "title": "§ Confidence Interval (95% CI)",
                "content": (
                    f"**목표가 범위**: {cur}{_fmt(conf['target_low'])} ~ {cur}{_fmt(conf['target_high'])}"
                    f" (중심 {cur}{_fmt(conf['target_mid'])}, {conf['ci_pct']})\n\n"
                    f"**스코어 ±밴드**: {conf['score_band']}\n\n"
                    f"**시나리오 분기**:\n"
                    f"- 강세 시나리오: {cur}{_fmt(conf['target_high'])}\n"
                    f"- 기본 시나리오: {cur}{_fmt(conf['target_mid'])}\n"
                    f"- 약세 시나리오: {cur}{_fmt(conf['target_low'])}"
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
                    f"- **모드**: BLIND (이전 v{prevv} read 0건)\n"
                    f"- **임계**: {THRESHOLD}일 (상한 10종, stock_update-2 슬롯, {TODAY})\n"
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
    print(f"=== 재분석 — {TODAY} ({THRESHOLD}일 임계, 상한 10) BLIND — {len(only)}종 ===\n")
    ok, fail = [], []
    for ticker in only:
        folder, kr, nv, prev_date = PLAN[ticker]
        cpath = f"analysis/{ticker}_{folder}_v{nv}/_content.json"
        dpath = f"analysis/{ticker}_{folder}_v{nv}/data.json"
        if not os.path.exists(cpath):
            print(f"  ⏸ {ticker}: _content.json 없음 — SKIP")
            fail.append(ticker)
            continue
        try:
            c = json.load(open(cpath, encoding="utf-8"))
            d = json.load(open(dpath, encoding="utf-8"))
            out_dir = make_md_files(ticker, folder, kr, nv, prev_date, c, d)
            html = make_html_report(ticker, folder, kr, nv, prev_date, c, d)
            print(f"[{ticker}] OK v{nv} MD(6) + HTML: {html}")
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
