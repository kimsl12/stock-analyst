#!/usr/bin/env python3
"""Phase 2 변화추적 run.md 조립 — 2026-07-17 (7일 슬롯). 신규는 _content.json/data.json 실측, 이전은 scorecard.md 본문 실측."""
import json

RUN_MD = "analysis/_reanalysis_runs/20260717_run_7day.md"

# ticker -> (folder, name_kr, new_v)
PLAN = [
    ("TM","Toyota","도요타",8), ("TMUS","TMobile","T-모바일",10),
    ("TQQQ","ProSharesUltraProQQQ","프로셰어즈 나스닥100 3배",10),
    ("TSM","TSMC","TSMC",9), ("TTE","TotalEnergies","토탈에너지스",9),
    ("TXN","TexasInstruments","텍사스인스트루먼트",9),
    ("VOO","VanguardSP500","뱅가드 S&P500",9),
    ("035420","NAVER","네이버",10), ("066570","LG전자","LG전자",7),
    ("CEG","ConstellationEnergy","컨스텔레이션에너지",8),
]

# 이전 v{N-1} scorecard.md 본문 실측값
OLD = {
    "TM":   {"pv":7,"date":"2026-07-07","score":74.2,"grade":"매수","tp":"$215 (Base)"},
    "TMUS": {"pv":9,"date":"2026-07-07","score":71.8,"grade":"매수","tp":"$206 (3ATR)"},
    "TQQQ": {"pv":9,"date":"2026-07-07","score":42.4,"grade":"매도","tp":"산정불가(레버리지)"},
    "TSM":  {"pv":8,"date":"2026-07-07","score":73.7,"grade":"매수","tp":"$525 (Base)"},
    "TTE":  {"pv":8,"date":"2026-07-07","score":68.0,"grade":"매수","tp":"$84 (펀더)"},
    "TXN":  {"pv":8,"date":"2026-07-07","score":67.7,"grade":"매수","tp":"$315 (펀더12M)"},
    "VOO":  {"pv":8,"date":"2026-07-07","score":77.6,"grade":"매수","tp":"$725 (Base)"},
    "035420":{"pv":9,"date":"2026-07-08","score":60.0,"grade":"중립","tp":"₩225,000"},
    "066570":{"pv":6,"date":"2026-07-08","score":64.0,"grade":"중립","tp":"₩232,000"},
    "CEG":  {"pv":7,"date":"2026-07-08","score":71.0,"grade":"매수","tp":"$278"},
}

GRANK = {"강력매수":5,"매수":4,"보유":3,"중립":3,"비중축소":2,"매도":1,"강력매도":0}


def fmt_tp(cur, v):
    if cur == "₩":
        return f"₩{int(round(v)):,}"
    return f"${v:,.0f}" if v >= 100 else f"${v:,.1f}"


rows = []
up, down, keep = [], [], []
for t, folder, kr, nv in PLAN:
    c = json.load(open(f"analysis/{t}_{folder}_v{nv}/_content.json", encoding="utf-8"))
    d = json.load(open(f"analysis/{t}_{folder}_v{nv}/data.json", encoding="utf-8"))
    o = OLD[t]
    cur = d.get("currency", "$")
    ns, ng = c["score"], c["grade"]
    conf = c.get("confidence", {})
    new_tp = fmt_tp(cur, conf.get("target_mid", 0))
    cp = d.get("current_price")
    cp_s = fmt_tp(cur, cp)
    delta = round(ns - o["score"], 1)
    dr = GRANK.get(ng, 3) - GRANK.get(o["grade"], 3)
    if o["grade"] == ng:
        chg = "유지"; keep.append(t)
    elif dr > 0:
        chg = f"🟢 {o['grade']}→{ng}"; up.append((t, kr, o["grade"], ng, c))
    else:
        chg = f"🔴 {o['grade']}→{ng}"; down.append((t, kr, o["grade"], ng, c))
    ds = f"+{delta}" if delta >= 0 else f"{delta}"
    rows.append((t, kr, o, nv, o["date"], ns, ng, ds, new_tp, cp_s, cur))

# 경과일: 2026-07-17 - date
from_dates = {"2026-07-07":10, "2026-07-08":9}

lines = []
lines.append("# 재분석 실행 결과 — 2026-07-17 (7일 슬롯)\n")
lines.append("**슬롯**: `stock_update-2` (임계 7일 / 상한 20종 → **10종으로 클램핑**) · **모드**: BLIND 재분석 (앵커링 편향 구조적 차단)")
lines.append("**데이터 소스**: 가격/ATR = fetch_price.py(yfinance/pykrx, 종가 2026-07-16). 펀더멘털 = 분석가 yfinance 실측(WebSearch 미바인딩 슬롯) → confidence 전반 보수.")
lines.append(f"**처리**: 성공 **10** / 스킵 **0** · **선정**: 경과일 desc, 동률 알파벳순, ANTHROPIC(비상장) standing 제외")
lines.append("**선행 회차**: 같은 날 오전 `staock_update`(10일 슬롯)이 MSFT·SPY 등 10종 완료 → 본 회차는 그 다음 오래된 배치(2026-07-07~08 코호트).\n")
lines.append("> **비교 기준**: 신규 점수·등급·목표가는 각 v{N} `_content.json`/`data.json` 실측. 이전 값은 v{N-1} `scorecard.md` **본문 실측값**(timeline 캐시 미사용). 목표가는 펀더멘털 중심(Base) 기준으로 통일.\n")
lines.append("---\n")
lines.append("## 1. 점수·등급·목표가 변화표\n")
lines.append("| 티커 | 종목명 | 이전(v/일자) | 신규(v/일자) | 경과 | 이전점수 | 신규점수 | Δ | 이전등급 | 신규등급 | 이전목표(중심) | 신규목표(중심) | 기준가(7/16) |")
lines.append("| ---- | ------ | ------------ | ------------ | ---- | -------- | -------- | --- | -------- | -------- | -------------- | -------------- | ------------ |")
for t, kr, o, nv, odate, ns, ng, ds, new_tp, cp_s, cur in rows:
    days = from_dates.get(odate, 9)
    chgmark = "" if o["grade"] == ng else ("🟢" if GRANK.get(ng,3) > GRANK.get(o["grade"],3) else "🔴")
    ng_disp = f"**{ng}** {chgmark}".strip() if chgmark else ng
    lines.append(f"| {t} | {kr} | v{o['pv']}·{odate} | v{nv}·2026-07-17 | {days}일 | {o['score']} | {ns} | {ds} | {o['grade']} | {ng_disp} | {o['tp']} | {new_tp} | {cp_s} |")

avg_delta = round(sum(ns - OLD[t]["score"] for t, _, _, _, _, ns, *_ in rows) / len(rows), 2)
n_up = sum(1 for _, _, _, _, _, ns, *_ in rows if ns - OLD[_[0] if False else 0]["score"] > 0) if False else None
raw_deltas = [ns - OLD[t]["score"] for t, _, _, _, _, ns, *_ in rows]
n_rise = sum(1 for x in raw_deltas if x > 0)
n_fall = sum(1 for x in raw_deltas if x < 0)
lines.append(f"\n평균 Δ **{avg_delta:+.2f}pt** (10종 단순평균) · 점수 상승 {n_rise}종 · 하락 {n_fall}종 · 등급변경 {len(up)+len(down)}종(🟢{len(up)}·🔴{len(down)}).\n")

lines.append("## 2. 등급 변경 종목\n")
lines.append(f"### 🟢 등급 상승 ({len(up)}종) — 비중 확대 검토")
if up:
    for t, kr, og, ng, c in up:
        lines.append(f"- **{t} ({kr})**: {og} → {ng} — {c['summary'][:160].rstrip()}…")
else:
    lines.append("- 없음")
lines.append(f"\n### 🔴 등급 하락 ({len(down)}종) — 비중 축소/보류 검토")
if down:
    for t, kr, og, ng, c in down:
        lines.append(f"- **{t} ({kr})**: {og} → {ng} — {c['summary'][:160].rstrip()}…")
else:
    lines.append("- 없음")
lines.append(f"\n### ⚪ 등급 유지 ({len(keep)}종)")
lines.append("- " + ", ".join(keep) + "\n")

lines.append("## 3. 스킵된 종목\n")
lines.append("- 없음 (10종 전원 완주).\n")

lines.append("## 4. 약한 가정 (분석가 명시 — 반증 모니터링 권고)\n")
for t, folder, kr, nv in PLAN:
    c = json.load(open(f"analysis/{t}_{folder}_v{nv}/_content.json", encoding="utf-8"))
    fa = c.get("fragile_assumptions", [])
    if fa:
        a, im = fa[0]
        lines.append(f"- **{t}**: {a[:110].rstrip()} → {im[:90].rstrip()}")
lines.append("")

lines.append("## 5. 방법론 노트\n")
lines.append("- **BLIND 구조적 분리**: 10종 각각 general-purpose 분석가가 이전 v·HTML·timeline 미참조 상태에서 data.json + KB + yfinance 실측만으로 독립 재산출. 등급 변경은 앵커링 보정이 아닌 현 데이터로부터의 독립 추론.")
lines.append("- **데이터 한계**: 스케줄 슬롯 WebSearch 미바인딩 → 펀더멘털은 yfinance(info·quarterly_income_stmt·analyst_price_targets) 실측. 한국주(NAVER·LG전자)는 yfinance 결측 보완 위해 공개 지식 보수 추정 병행, confidence 중간 이하.")
lines.append("- **매크로 앵커(2026-07-16)**: 미 레짐 중립 16일째·VIX 15.7·US10Y 4.55%·F&G 46.7 / 한국은행 2.50→2.75% 첫 인상·KOSPI -6.37% 반도체發 급락·USD/KRW 1,480원. 반도체 급락은 범용 DRAM·심리 축, HBM/AI 무손상 노이즈 의심(55%, 미확정)으로 반영.")
lines.append("")

body = "\n".join(lines)
open(RUN_MD, "w", encoding="utf-8").write(body)
print(f"작성 완료: {RUN_MD} ({len(body)} chars)")
print(f"평균 Δ {avg_delta:+.2f} · 상승 {n_rise} 하락 {n_fall} · 🟢{len(up)} 🔴{len(down)} 유지{len(keep)}")
