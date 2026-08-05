#!/usr/bin/env python3
"""_content.json 스키마 정규화 (2026-08-06 10일 회차, /재분석실행 10 10, staock_update) — 멱등.
consensus/risks/scorecard/fragile/confidence 표준화 + 필수 키 보증 (generator KeyError 방지)."""
import json, os

PLAN = {
    "TSM": "TSMC_v11", "TXN": "TexasInstruments_v11", "TTE": "TotalEnergies_v11",
    "TMUS": "TMobile_v12", "TM": "Toyota_v10", "CEG": "ConstellationEnergy_v10",
    "CCJ": "Cameco_v6", "052690": "한전기술_v5", "035420": "NAVER_v12", "000720": "현대건설_v5",
}
SEPS = ["—", "–", "·", ":", "：", " - "]

STR_DEFAULTS = {
    "summary": "요약 정보 미상 (정규화 fallback).",
    "moat_rating": "중간",
    "moat_details": "해자 상세 미상.",
    "sector": "미분류",
    "category": "중립",
    "financial": "재무 분석 미상.",
    "valuation": "밸류에이션 미상.",
    "business": "사업/산업 분석 미상.",
    "momentum": "모멘텀 미상.",
    "strategy": "전략 미상.",
    "risk_summary": "리스크 종합 미상.",
    "per": "N/A",
    "asset_type": "주식",
}


def norm_consensus(cons):
    if isinstance(cons, str):
        return [["컨센서스", cons.strip()]]
    if isinstance(cons, dict):
        return [[str(k), str(v)] for k, v in cons.items()]
    rows = []
    for r in cons or []:
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
    for r in risks or []:
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
    while len(out) < 3:
        out.append({"name": f"기타 리스크 {len(out)+1}", "level": "중",
                    "impact": "중", "desc": "분석 본문 참조."})
    return out


def norm_scorecard(items):
    rows = []
    for r in items or []:
        if isinstance(r, (list, tuple)) and len(r) >= 2:
            rows.append([str(r[0]), float(r[1])])
        elif isinstance(r, dict):
            name = r.get("name") or r.get("항목") or r.get("item") or (list(r.values())[0] if r else "항목")
            score = r.get("score", r.get("점수", r.get("value", 0)))
            rows.append([str(name), float(score)])
    if rows and any(s > 10 for _, s in rows):
        rows = [[n, round(s / 10, 1)] for n, s in rows]
    if len(rows) > 10:
        rows = rows[:10]
    while len(rows) < 10:
        rows.append([f"항목{len(rows)+1}", 5.0])
    return rows


def norm_fragile(fr):
    out = []
    for r in fr or []:
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
    while len(out) < 3:
        out.append([f"핵심 가정 {len(out)+1}", "반증 시 스코어·등급 하방 리스크"])
    return out[:3]


def norm_confidence(conf, cur_price):
    def num(v, fallback):
        if isinstance(v, (int, float)):
            return v
        if isinstance(v, str):
            cleaned = "".join(ch for ch in v if ch.isdigit() or ch == ".")
            try:
                return float(cleaned) if cleaned else fallback
            except ValueError:
                return fallback
        return fallback
    if not isinstance(conf, dict):
        conf = {}
    mid = num(conf.get("target_mid"), cur_price)
    lo = num(conf.get("target_low"), mid * 0.85)
    hi = num(conf.get("target_high"), mid * 1.15)
    lo, mid, hi = sorted([lo, mid, hi])
    for k, v in (("target_low", lo), ("target_mid", mid), ("target_high", hi)):
        conf[k] = int(round(v)) if v >= 1000 else round(v, 2)
    conf.setdefault("ci_pct", "±15%")
    conf.setdefault("score_band", "±6pt")
    return conf


def main():
    ok, miss = [], []
    for t, suf in PLAN.items():
        p = f"analysis/{t}_{suf}/_content.json"
        if not os.path.exists(p):
            print(f"⏸ {t}: 파일 없음"); miss.append(t); continue
        d = json.load(open(p, encoding="utf-8"))
        d["consensus"] = norm_consensus(d.get("consensus", []))
        d["risks"] = norm_risks(d.get("risks", []))
        d["scorecard_items"] = norm_scorecard(d.get("scorecard_items", []))
        d["fragile_assumptions"] = norm_fragile(d.get("fragile_assumptions", []))
        dp = f"analysis/{t}_{suf}/data.json"
        cur_price = json.load(open(dp, encoding="utf-8")).get("current_price", 0)
        d["confidence"] = norm_confidence(d.get("confidence"), cur_price)
        if isinstance(d.get("score"), str):
            d["score"] = float("".join(ch for ch in d["score"] if ch.isdigit() or ch == ".") or 0)
        d["score"] = round(float(d.get("score", 0)))
        g = str(d.get("grade", "")).strip()
        if g not in ("강력매수", "매수", "중립", "매도", "강력매도"):
            for cand in ("강력매수", "강력매도", "매수", "매도", "중립"):
                if cand in g:
                    d["grade"] = cand; break
            else:
                d["grade"] = "중립"
        for k, dv in STR_DEFAULTS.items():
            if not d.get(k) or not str(d.get(k)).strip():
                d[k] = dv
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        ok.append(t)
        print(f"✅ {t}: consensus {len(d['consensus'])}행 · risks {len(d['risks'])}개 · "
              f"scorecard {len(d['scorecard_items'])}개 · fragile {len(d['fragile_assumptions'])}개 · "
              f"score {d.get('score')} {d.get('grade')} · TP {d['confidence']['target_mid']}")
    print(f"\n=== 정규화 완료 — 성공 {len(ok)} / 누락 {len(miss)} ===")
    if miss:
        print("누락:", ", ".join(miss))


if __name__ == "__main__":
    main()
