#!/usr/bin/env python3
"""
재분석 변화 추적 — 2026-06-28 (Phase 2, 7일 런 stock_update-2)
신규 v{N} _content.json vs 직전 v{N-1} scorecard.md 비교 → analysis/_reanalysis_runs/20260628_run_7day.md
read-only 비교 (분석 영향 없음).
"""
import json, os, re

TODAY = "2026-06-28"
RUN_MD = "analysis/_reanalysis_runs/20260628_run_7day.md"
ELAPSED = "9일"

# ticker, folder, kr, next_v, prev_v_date
PLAN = [
    ("009150", "삼성전기",        "삼성전기",          7, "2026-06-19"),
    ("329180", "HD현대중공업",    "HD현대중공업",      8, "2026-06-19"),
    ("466100", "클로봇",          "클로봇",            7, "2026-06-19"),
    ("ADBE",   "Adobe",           "어도비",            8, "2026-06-19"),
    ("ANET",   "AristaNetworks",  "아리스타 네트웍스", 6, "2026-06-19"),
    ("BHP",    "BHPGroup",        "BHP 그룹",          8, "2026-06-19"),
    ("COIN",   "Coinbase",        "코인베이스",        8, "2026-06-19"),
    ("COST",   "Costco",          "코스트코",          8, "2026-06-19"),
    ("HOOD",   "Robinhood",       "로빈후드",          7, "2026-06-19"),
    ("IONQ",   "IonQ",            "아이온큐",          7, "2026-06-19"),
]

GRADE_ORDER = {"강력매도": 0, "매도": 1, "중립": 2, "매수": 3, "강력매수": 4}


def parse_old(path):
    if not os.path.exists(path):
        return None, None, None
    txt = open(path, encoding="utf-8").read()
    score = grade = tp = None
    m = re.search(r"종합 점수\*?\*?:?\s*([0-9]+)\s*/\s*100", txt)
    if m: score = int(m.group(1))
    m = re.search(r"투자 등급\*?\*?:?\s*(강력매수|매수|중립|매도|강력매도)", txt)
    if m: grade = m.group(1)
    m = re.search(r"목표가 범위\*?\*?:?\s*.*?중심\s*([₩$]?[0-9,\.]+)", txt)
    if m: tp = m.group(1).rstrip(",.")
    return score, grade, tp


def fmt_tp(v, cur):
    if isinstance(v, (int, float)):
        return f"{cur}{v:,.0f}" if v >= 100 else f"{cur}{v}"
    return str(v)


rows = []
grade_up, grade_down = [], []
fragile_all = []

for ticker, folder, kr, nv, prev_date in PLAN:
    cdir = f"analysis/{ticker}_{folder}_v{nv}"
    c = json.load(open(f"{cdir}/_content.json", encoding="utf-8"))
    d = json.load(open(f"{cdir}/data.json", encoding="utf-8"))
    cur = d.get("currency", "$")
    new_score = c["score"]
    new_grade = c["grade"]
    new_tp = fmt_tp(c["confidence"]["target_mid"], cur)

    old_score, old_grade, old_tp = parse_old(f"analysis/{ticker}_{folder}_v{nv-1}/scorecard.md")
    d_score = (new_score - old_score) if (old_score is not None) else None
    d_str = f"{d_score:+d}" if d_score is not None else "—"

    chg = "—"
    if old_grade and new_grade and old_grade != new_grade:
        if GRADE_ORDER.get(new_grade, 2) > GRADE_ORDER.get(old_grade, 2):
            chg = "🟢 상승"; grade_up.append((ticker, kr, old_grade, new_grade, c))
        else:
            chg = "🔴 하락"; grade_down.append((ticker, kr, old_grade, new_grade, c))

    rows.append({
        "ticker": ticker, "kr": kr, "nv": nv, "prev_date": prev_date,
        "old_score": old_score if old_score is not None else "—",
        "new_score": new_score, "d": d_str,
        "old_grade": old_grade or "—", "new_grade": new_grade, "chg": chg,
        "old_tp": old_tp or "—", "new_tp": new_tp,
    })
    fragile_all.append((ticker, kr, c["fragile_assumptions"]))

# ── run.md 작성
lines = []
lines.append(f"# 재분석 실행 결과 — {TODAY}")
lines.append("")
lines.append(f"**임계 기준:** 7일 / 상한 10종 (stock_update-2 슬롯) | **처리:** 성공 10 / 스킵 0")
lines.append("**모드:** BLIND 재분석 (각 종목 이전 v{N-1} read 0건 — 독립 판단). 대상: 9일 경과 2026-06-19 분석분 10종.")
lines.append("> ANTHROPIC(32일, 비상장·비표준)은 standing 제외. 동일일 01:00 10일 런이 06-18 코호트 10종을 선처리, 본 7일 런은 06-19 코호트 10종 처리.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 1. 변화 요약 표")
lines.append("")
lines.append("| 티커 | 종목명 | 이전 v / 분석일 | 경과 | 이전 스코어 | 신규 스코어 | Δ | 이전 등급 | 신규 등급 | 등급 변경 | 이전 목표가(중심) | 신규 목표가(중심) |")
lines.append("| ---- | ------ | --------------- | ---- | ----------- | ----------- | --- | --------- | --------- | --------- | ----------------- | ----------------- |")
for r in rows:
    lines.append(f"| {r['ticker']} | {r['kr']} | v{r['nv']-1} / {r['prev_date']} | {ELAPSED} | {r['old_score']} | {r['new_score']} | {r['d']} | {r['old_grade']} | {r['new_grade']} | {r['chg']} | {r['old_tp']} | {r['new_tp']} |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 2. 등급 변경 종목")
lines.append("")
lines.append(f"### 🟢 상승 ({len(grade_up)}종)")
lines.append("")
if grade_up:
    for ticker, kr, og, ng, c in grade_up:
        lines.append(f"- **{ticker} ({kr})**: {og} → {ng} — {c['summary'][:120]}…")
else:
    lines.append("- 없음")
lines.append("")
lines.append(f"### 🔴 하락 ({len(grade_down)}종)")
lines.append("")
if grade_down:
    for ticker, kr, og, ng, c in grade_down:
        lines.append(f"- **{ticker} ({kr})**: {og} → {ng} — {c['summary'][:120]}…")
else:
    lines.append("- 없음")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 3. 약한 가정 (각 종목 애널리스트 명시 — 반증 모니터링)")
lines.append("")
for ticker, kr, fa in fragile_all:
    lines.append(f"**{ticker} ({kr})**")
    for i, (a, impact) in enumerate(fa, 1):
        lines.append(f"{i}. {a} — _반증 시:_ {impact}")
    lines.append("")
lines.append("---")
lines.append("")
lines.append("## 4. 스킵 종목")
lines.append("")
lines.append("- 없음 (10종 전량 성공)")
lines.append("")
lines.append(f"> 본 회차는 **{TODAY} BLIND 재분석**입니다. 각 종목 신규 v는 이전 버전을 참조하지 않은 독립 산출이며,")
lines.append("> 위 비교표는 사후 read-only 대조입니다 (분석 자체에 영향 없음).")

os.makedirs(os.path.dirname(RUN_MD), exist_ok=True)
with open(RUN_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"run.md 작성 완료: {RUN_MD}")
print(f"등급 상승 {len(grade_up)}종 / 하락 {len(grade_down)}종")
for r in rows:
    print(f"  {r['ticker']:7} {r['old_score']}→{r['new_score']} ({r['d']}) {r['old_grade']}→{r['new_grade']} {r['chg']} | TP {r['old_tp']}→{r['new_tp']}")
