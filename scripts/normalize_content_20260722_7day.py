#!/usr/bin/env python3
"""_content.json 스키마 정규화 (2026-07-22 7일 회차) — consensus/risks/scorecard/fragile/confidence 표준화. 멱등."""
import json, os

PLAN = {
    "005380": "현대차_v3", "005930": "삼성전자_v10", "009150": "삼성전기_v10",
    "207940": "삼성바이오로직스_v3", "329180": "HD현대중공업_v11", "466100": "클로봇_v10",
    "AAPL": "Apple_v3", "ADBE": "Adobe_v11", "AMD": "AMD_v3", "ANET": "AristaNetworks_v9",
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


def norm_confidence(conf, cur_price):
    """target_* 를 숫자로 강제. 통화기호·콤마 제거. 순서 보정."""
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
    for t, suf in PLAN.items():
        p = f"analysis/{t}_{suf}/_content.json"
        if not os.path.exists(p):
            print(f"⏸ {t}: 파일 없음"); continue
        d = json.load(open(p, encoding="utf-8"))
        d["consensus"] = norm_consensus(d.get("consensus", []))
        d["risks"] = norm_risks(d.get("risks", []))
        d["scorecard_items"] = norm_scorecard(d.get("scorecard_items", []))
        d["fragile_assumptions"] = norm_fragile(d.get("fragile_assumptions", []))
        dp = f"analysis/{t}_{suf}/data.json"
        cur_price = json.load(open(dp, encoding="utf-8")).get("current_price", 0)
        d["confidence"] = norm_confidence(d.get("confidence"), cur_price)
        if isinstance(d.get("score"), str):
            d["score"] = float("".join(ch for ch in d["score"] if ch.isdigit() or ch == "."))
        g = str(d.get("grade", "")).strip()
        if g not in ("강력매수", "매수", "중립", "매도", "강력매도"):
            for cand in ("강력매수", "강력매도", "매수", "매도", "중립"):
                if cand in g:
                    d["grade"] = cand; break
            else:
                d["grade"] = "중립"
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"✅ {t}: consensus {len(d['consensus'])}행 · risks {len(d['risks'])}개 · "
              f"scorecard {len(d['scorecard_items'])}개 · fragile {len(d['fragile_assumptions'])}개 · "
              f"score {d.get('score')} {d.get('grade')} · TP {d['confidence']['target_mid']}")


if __name__ == "__main__":
    main()
