#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 2 변화추적 run.md 생성 — 2026-08-26 (10일 임계, staock_update, /재분석실행 10 10).
신규 v{N} _content.json vs 직전 v{N-1} (timeline.json max-v) read-only 비교.
출력: analysis/_reanalysis_runs/20260826_run.md
"""
import json, os, glob, re

TODAY = "2026-08-26"
THRESHOLD = 10
OUT = "analysis/_reanalysis_runs/20260826_run.md"

# ticker -> (folder, name_kr, next_v)
PLAN = {
    "000720": ("현대건설", "현대건설", 7),
    "052690": ("한전기술", "한전기술", 7),
    "JEPI": ("JPMorganEquityPremiumIncome", "JEPI", 7),
    "LQD": ("iSharesInvestmentGradeCorpBond", "LQD", 7),
    "MLM": ("MartinMarietta", "마틴마리에타", 8),
    "MUFG": ("Mitsubishi", "미쓰비시UFJ", 14),
    "NEE": ("NextEraEnergy", "넥스트에라에너지", 8),
    "NKE": ("Nike", "나이키", 13),
    "O": ("RealtyIncome", "리얼티인컴", 7),
    "OKLO": ("Oklo", "오클로", 7),
}
GRADE_RANK = {"강력매도": 0, "매도": 1, "중립": 2, "매수": 3, "강력매수": 4}
CUR = {"KRW": "₩", "USD": "$"}


def find_timeline(ticker):
    for f in glob.glob("analysis/_history/*timeline.json"):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("ticker") == ticker:
            return d
    return None


def fmt(v, sym=""):
    if v is None:
        return "N/A"
    if isinstance(v, (int, float)):
        return f"{sym}{v:,.0f}" if abs(v) >= 100 else f"{sym}{v:,.2f}"
    return f"{sym}{v}"


def main():
    rows = []
    up, down = [], []
    fragile_lines = []
    skipped = []
    for tk, (folder, kr, nv) in PLAN.items():
        cpath = f"analysis/{tk}_{folder}_v{nv}/_content.json"
        dpath = f"analysis/{tk}_{folder}_v{nv}/data.json"
        if not os.path.exists(cpath):
            skipped.append((tk, "_content.json 없음"))
            continue
        c = json.load(open(cpath, encoding="utf-8"))
        d = json.load(open(dpath, encoding="utf-8")) if os.path.exists(dpath) else {}
        cur = CUR.get(d.get("meta", {}).get("currency", "USD"), "$")
        new_score = c.get("score")
        new_grade = c.get("grade")
        new_tp = (c.get("confidence") or {}).get("target_mid")

        tl = find_timeline(tk)
        prev = None
        if tl and tl.get("history"):
            prev = max(tl["history"], key=lambda h: h.get("v", 0))
        prev_date = prev.get("date") if prev else "N/A"
        prev_score = prev.get("score") if prev else None
        prev_grade = prev.get("grade") if prev else None
        prev_tp = prev.get("target_price") if prev else None

        delta = ""
        if isinstance(new_score, (int, float)) and isinstance(prev_score, (int, float)):
            dd = round(new_score - prev_score)
            delta = f"{dd:+d}"
        ci = (c.get("confidence") or {}).get("ci_pct", "")

        rows.append(
            f"| {tk} | {kr} | {prev_date} | {THRESHOLD}일 | {prev_score} | {new_score} | {delta} | "
            f"{prev_grade or 'N/A'} | {new_grade} | {prev_tp or 'N/A'} | {fmt(new_tp, cur)} | conf {ci} |"
        )

        # grade change
        pr = GRADE_RANK.get(prev_grade)
        nr = GRADE_RANK.get(new_grade)
        if pr is not None and nr is not None:
            if nr > pr:
                up.append(f"- 🟢 {tk} ({kr}): {prev_grade} → {new_grade} (스코어 {prev_score}→{new_score})")
            elif nr < pr:
                down.append(f"- 🔴 {tk} ({kr}): {prev_grade} → {new_grade} (스코어 {prev_score}→{new_score})")

        # fragile
        fa = c.get("fragile_assumptions") or []
        if fa:
            first = fa[0]
            if isinstance(first, (list, tuple)) and len(first) >= 2:
                fragile_lines.append(f"- **{tk}**: {first[0]} — _반증 시_: {first[1]}")

    lines = []
    lines.append(f"# 재분석 실행 결과 — {TODAY} (10일런)\n")
    lines.append(f"**명령**: `/재분석실행 10 10` (임계 10일 / 상한 10종) · launchd **staock_update** 슬롯 (10일런)\n")
    lines.append("**검출**: timeline.json max-v date 기준 20종이 10일+ 경과(08-16 코호트). "
                 "ANTHROPIC(비상장·비표준, 91일) standing 제외. 7일런(cap 10/일)이 ~146종 유니버스를 "
                 "10일 내 다 못 덮어 새어나온 오버플로 코호트 → 알파벳 정렬 상위 10종 BLIND 재분석.\n")
    lines.append("**BLIND**: 분석가 10종 병렬(Agent), 이전 v·HTML·timeline 미참조. "
                 "데이터 yfinance 단일계열(WebSearch 미바인딩) — confidence 하향 반영.\n")
    lines.append("| 티커 | 종목명 | 이전 분석일 | 경과 | 이전 스코어 | 신규 스코어 | Δ | 이전 등급 | 신규 등급 | 이전 목표가 | 신규 목표가 | 비고 |")
    lines.append("| ---- | ------ | ----------- | ---- | ----------- | ----------- | - | --------- | --------- | ----------- | ----------- | ---- |")
    lines.extend(rows)
    lines.append("\n## 등급 변경 종목\n")
    lines.append("### 🟢 등급 상승 (비중 확대 검토)")
    lines.extend(up if up else ["- 없음"])
    lines.append("\n### 🔴 등급 하락 (매도 검토 권고)")
    lines.extend(down if down else ["- 없음"])
    lines.append("\n## 스킵된 종목\n")
    lines.extend([f"- {tk}: {why}" for tk, why in skipped] if skipped else ["- 없음"])
    lines.append("\n## 약한 가정 (분석가가 명시한 핵심 1개씩)\n")
    lines.extend(fragile_lines if fragile_lines else ["- N/A"])
    lines.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ run.md 작성 — {OUT} ({len(rows)}종, 상승 {len(up)} 하락 {len(down)} 스킵 {len(skipped)})")


if __name__ == "__main__":
    main()
