#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 변화 추적 — 2026-09-28 (7일 슬롯, stock_update-2).
이전 값: analysis/_history/{ticker}_*_timeline.json 의 max-v(=v{N-1}) 항목 (진실 소스).
신규 값: analysis/{folder}_v{N}/_report_data.json (Phase 1b BLIND 산출).
출력: analysis/_reanalysis_runs/20260928_7day_run.md (변화표 + 등급변경 + 약한가정).
※ 이전 scorecard.md 를 읽지 않고 timeline 메타만 사용 → BLIND 무결성 유지."""
import json, glob, os, re

ROOT = "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
TODAY = "2026-09-28"

# ticker -> (folder(name만), next_v, name_kr)
PLAN = {
    "VMC":  ("VulcanMaterials",          12, "벌컨머티리얼즈"),
    "SOXS": ("Direxion3xSemiBear",       17, "Direxion 3x 반도체 인버스"),
    "T":    ("ATT",                      17, "AT&T"),
    "SOXL": ("Direxion3xSemiconductor",  17, "Direxion 3x 반도체"),
    "VOO":  ("VanguardSP500",            17, "뱅가드 S&P500"),
    "TTE":  ("TotalEnergies",            17, "토탈에너지스"),
    "TSM":  ("TSMC",                     17, "TSMC"),
    "TXN":  ("TexasInstruments",         17, "텍사스인스트루먼트"),
    "TMUS": ("TMobile",                  18, "T모바일"),
    "SNDK": ("Sandisk",                  19, "샌디스크"),
}

GRADE_RANK = {"강력매도": 0, "매도": 1, "중립": 2, "매수": 3, "강력매수": 4}


def norm_grade(g):
    if not g:
        return ""
    # 구체적(긴) 등급 먼저 — "매수"가 "강력매수"의 부분문자열이므로 순서 중요
    for k in ["강력매수", "강력매도", "매수", "매도", "중립"]:
        if k in g:
            return k
    return g.strip()


def prev_from_timeline(ticker):
    hits = glob.glob(f"{ROOT}/analysis/_history/{ticker}_*_timeline.json")
    if not hits:
        return None
    d = json.load(open(hits[0], encoding="utf-8"))
    hist = d.get("history", [])
    if not hist:
        return None
    latest = max(hist, key=lambda h: h.get("v", 0))
    return {
        "v": latest.get("v"),
        "date": latest.get("date"),
        "score": latest.get("score"),
        "grade": norm_grade(latest.get("grade")),
        "target": latest.get("target_price"),
    }


def new_from_report(folder, nv):
    p = f"{ROOT}/analysis/{folder}_v{nv}/_report_data.json"
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    tp = d.get("target_price")
    cur = d.get("currency", "$")
    return {
        "score": d.get("score"),
        "grade": norm_grade(d.get("grade")),
        "target": f"{cur}{tp}" if tp is not None else None,
        "custom": d.get("custom_sections", []),
    }


def main():
    rows, up, down, fragile, missing = [], [], [], [], []
    for tk, (folder, nv, kr) in PLAN.items():
        full = f"{tk}_{folder}"
        prev = prev_from_timeline(tk)
        new = new_from_report(full, nv)
        if new is None:
            missing.append(tk)
            continue
        ps = prev["score"] if prev else None
        ns = new["score"]
        delta = (ns - ps) if (isinstance(ns, (int, float)) and isinstance(ps, (int, float))) else None
        pg = prev["grade"] if prev else ""
        ng = new["grade"]
        rows.append((tk, kr, prev["date"] if prev else "?", ps, ns, delta, pg, ng,
                     prev["target"] if prev else "?", new["target"]))
        if pg and ng and GRADE_RANK.get(ng, 2) > GRADE_RANK.get(pg, 2):
            up.append((tk, pg, ng))
        elif pg and ng and GRADE_RANK.get(ng, 2) < GRADE_RANK.get(pg, 2):
            down.append((tk, pg, ng))
        # 약한 가정 추출
        for s in new["custom"]:
            if "약한 가정" in s.get("title", ""):
                txt = re.sub(r"<[^>]+>", " ", s.get("content", "")).strip()
                txt = re.sub(r"\s+", " ", txt)
                fragile.append((tk, txt[:400]))

    lines = [f"# 재분석 실행 결과 — {TODAY} (7일 슬롯 · stock_update-2)", ""]
    lines.append(f"**대상**: {len(rows)}종 (7일+ 경과 상위 10, 09-19 배치)  ·  **스킵**: {len(missing)}종  ·  **모드**: BLIND (이전 미참조)")
    lines.append("")
    lines.append("| 티커 | 종목명 | 이전 분석일 | 이전 점수 | 신규 점수 | Δ | 이전 등급 | 신규 등급 | 이전 목표가 | 신규 목표가 |")
    lines.append("| ---- | ------ | ----------- | --------- | --------- | - | --------- | --------- | ----------- | ----------- |")
    for tk, kr, pd_, ps, ns, dl, pg, ng, pt, nt in rows:
        dls = f"{dl:+d}" if isinstance(dl, int) else (f"{dl:+.0f}" if isinstance(dl, float) else "–")
        gchg = "→" if pg == ng else f"→ **{ng}**"
        lines.append(f"| {tk} | {kr} | {pd_} | {ps} | {ns} | {dls} | {pg} | {gchg if pg!=ng else ng} | {pt} | {nt} |")
    lines.append("")
    lines.append("## 등급 변경")
    lines.append("")
    if up:
        for tk, a, b in up:
            lines.append(f"- 🟢 **{tk}**: {a} → {b} (상향)")
    if down:
        for tk, a, b in down:
            lines.append(f"- 🔴 **{tk}**: {a} → {b} (하향)")
    if not up and not down:
        lines.append("- 등급 변경 없음")
    lines.append("")
    if missing:
        lines.append("## 스킵된 종목")
        lines.append("")
        for tk in missing:
            lines.append(f"- {tk}: _report_data.json 미생성")
        lines.append("")
    lines.append("## 약한 가정 (분석가 명시)")
    lines.append("")
    for tk, txt in fragile:
        lines.append(f"- **{tk}**: {txt}")
    lines.append("")

    out = f"{ROOT}/analysis/_reanalysis_runs/{TODAY.replace('-','')}_7day_run.md"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"[OK] {out}")
    print(f"  행 {len(rows)} / 상향 {len(up)} / 하향 {len(down)} / 스킵 {len(missing)}")
    for tk, kr, pd_, ps, ns, dl, pg, ng, pt, nt in rows:
        print(f"  {tk:5s} {ps}->{ns} ({pg}->{ng}) tp {pt}->{nt}")


if __name__ == "__main__":
    main()
