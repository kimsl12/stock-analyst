#!/usr/bin/env python3
"""_content.json 스키마 정규화 (2026-07-17 재분석) — consensus/risks 표준화. 멱등."""
import json, os

PLAN = {
    "TM": "Toyota_v8", "TMUS": "TMobile_v10", "TQQQ": "ProSharesUltraProQQQ_v10",
    "TSM": "TSMC_v9", "TTE": "TotalEnergies_v9", "TXN": "TexasInstruments_v9",
    "VOO": "VanguardSP500_v9", "035420": "NAVER_v10", "066570": "LG전자_v7",
    "CEG": "ConstellationEnergy_v8",
}
SEPS = ["—", "–", "·", ":", "：", " - "]


def norm_consensus(cons):
    if isinstance(cons, str):
        return [["컨센서스", cons.strip()]]
    if isinstance(cons, dict):
        return [[str(k), str(v)] for k, v in cons.items()]
    rows = []
    for r in cons:
        if isinstance(r, (list, tuple)):
            if len(r) >= 2:
                rows.append([str(r[0]), str(r[1])])
            elif len(r) == 1:
                rows.append(["항목", str(r[0])])
        elif isinstance(r, dict):
            items = list(r.items())
            if "label" in r and "value" in r:
                rows.append([str(r["label"]), str(r["value"])])
            elif len(items) >= 2:
                rows.append([str(items[0][1]), str(items[1][1])])
            elif items:
                rows.append([str(items[0][0]), str(items[0][1])])
        elif isinstance(r, str):
            done = False
            for sep in SEPS:
                if sep in r:
                    k, v = r.split(sep, 1)
                    rows.append([k.strip(), v.strip()])
                    done = True
                    break
            if not done:
                rows.append(["항목", r.strip()])
    return rows or [["컨센서스", "N/A"]]


def norm_risks(risks):
    out = []
    for r in risks:
        if isinstance(r, dict):
            name = (r.get("name") or r.get("title") or r.get("요인") or r.get("리스크")
                    or (list(r.values())[0] if r else "리스크"))
            desc = (r.get("desc") or r.get("detail") or r.get("상세") or r.get("설명")
                    or r.get("영향") or "")
            level = r.get("level") or r.get("수준") or "중"
            impact = r.get("impact") or "중"
            if isinstance(impact, str) and len(impact) > 6 and not desc:
                desc, impact = impact, "중"
            if isinstance(impact, str) and len(impact) > 6:
                impact = "중"
            if isinstance(level, str) and len(level) > 6:
                level = "중"
            out.append({"name": str(name).strip(), "level": str(level).strip(),
                        "impact": str(impact).strip(), "desc": str(desc).strip()})
        elif isinstance(r, str):
            name, desc = r, r
            for sep in SEPS:
                if sep in r:
                    name, desc = r.split(sep, 1)
                    break
            out.append({"name": name.strip()[:80], "level": "중", "impact": "중",
                        "desc": desc.strip()})
    return out


def norm_scorecard(items):
    rows = []
    for r in items:
        if isinstance(r, (list, tuple)) and len(r) >= 2:
            rows.append([str(r[0]), float(r[1])])
        elif isinstance(r, dict):
            name = r.get("name") or r.get("항목") or r.get("item") or (list(r.values())[0] if r else "항목")
            score = r.get("score", r.get("점수", r.get("value", 0)))
            rows.append([str(name), float(score)])
    # 스케일 정규화: 어느 항목이든 10 초과면 /100 스케일로 보고 전체 /10
    if rows and any(s > 10 for _, s in rows):
        rows = [[n, round(s / 10, 1)] for n, s in rows]
    return rows


def norm_fragile(fr):
    out = []
    for r in fr:
        if isinstance(r, (list, tuple)):
            if len(r) >= 2:
                out.append([str(r[0]), str(r[1])])
            elif len(r) == 1:
                out.append([str(r[0]), "반증 시 스코어·등급 하방 리스크"])
        elif isinstance(r, dict):
            a = r.get("assumption") or r.get("가정") or (list(r.values())[0] if r else "")
            im = (r.get("impact") or r.get("영향") or r.get("반증 시 영향")
                  or "반증 시 스코어·등급 하방 리스크")
            out.append([str(a), str(im)])
        elif isinstance(r, str):
            assumption, impact = r.strip(), ""
            for sep in ["—", "–", " - ", "→"]:
                if sep in r:
                    assumption, impact = r.split(sep, 1)
                    break
            out.append([assumption.strip(), impact.strip() or "반증 시 스코어·등급 하방 리스크"])
    return out


def main():
    for t, suf in PLAN.items():
        p = f"analysis/{t}_{suf}/_content.json"
        if not os.path.exists(p):
            print(f"⏸ {t}: 파일 없음"); continue
        d = json.load(open(p, encoding="utf-8"))
        d["consensus"] = norm_consensus(d.get("consensus", []))
        d["risks"] = norm_risks(d.get("risks", []))
        d["scorecard_items"] = norm_scorecard(d.get("scorecard_items", []))
        d["fragile_assumptions"] = norm_fragile(d.get("fragile_assumptions", []))
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"✅ {t}: consensus {len(d['consensus'])}행 · risks {len(d['risks'])}개 · "
              f"scorecard {len(d['scorecard_items'])}개 · fragile {len(d['fragile_assumptions'])}개")


if __name__ == "__main__":
    main()
