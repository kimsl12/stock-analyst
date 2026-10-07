#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_report_data.json 중앙 normalize 가드 — 2026-10-08 재분석 10일런 (BLIND 에이전트 산출 후 렌더 직전).
멱등. 각 _report_data.json 을 data.json 실측과 대조해 스키마 드리프트 교정:
  1) scorecard_items 스케일(값>10 → /10, 10항목 보장, 숫자화)
  2) 숫자 필드(current_price·market_cap·atr·stop_loss·high52·low52) 문자열→숫자, 누락 시 data.json 승계
  3) target_price 문자열→숫자
  4) score 0~100 정수 보장
교정 내역을 stdout 로그로 출력."""
import json, os, re, sys

ROOT = "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
PLAN = {
    "ORCL": ("Oracle",                  17),
    "QUAL": ("iSharesMSCIQuality",      10),
    "SGOV": ("iShares0-3MonthTreasury", 10),
    "SNDK": ("Sandisk",                 20),
    "SOXL": ("Direxion3xSemiconductor", 18),
    "SOXS": ("Direxion3xSemiBear",      18),
    "SPGI": ("SPGlobal",                11),
    "T":    ("ATT",                     18),
    "TLT":  ("iSharesTreasury",         18),
    "TMO":  ("ThermoFisher",            11),
}


def to_num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        m = re.search(r"-?[\d,]+\.?\d*", v.replace(",", ""))
        if m:
            try:
                return float(m.group().replace(",", ""))
            except Exception:
                return None
    return None


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    for tk in only:
        folder, nv = PLAN[tk]
        d_path = f"{ROOT}/analysis/{tk}_{folder}_v{nv}/data.json"
        rd_path = f"{ROOT}/analysis/{tk}_{folder}_v{nv}/_report_data.json"
        if not os.path.exists(rd_path):
            print(f"  X {tk}: _report_data.json 없음")
            continue
        data = json.load(open(d_path, encoding="utf-8")) if os.path.exists(d_path) else {}
        rd = json.load(open(rd_path, encoding="utf-8"))
        q = data.get("quote", {})
        fixes = []

        # 1) scorecard_items 스케일 + 숫자화 (0~10 보장)
        items = rd.get("scorecard_items", [])
        new_items = []
        scaled = False
        for it in items:
            try:
                name, sc = it[0], it[1]
            except Exception:
                continue
            scn = to_num(sc)
            if scn is None:
                scn = 5
            if scn > 10:
                scn = round(scn / 10)
                scaled = True
            scn = max(0, min(10, int(round(scn))))
            new_items.append([name, scn])
        if new_items:
            rd["scorecard_items"] = new_items
        if scaled:
            fixes.append("scorecard_items 0~100→0~10 스케일 교정")

        # 2) 숫자 필드 문자열→숫자, 누락 시 data.json 승계
        num_map = {
            "current_price": q.get("current_price"),
            "market_cap": q.get("marketCap"),
            "atr": q.get("atr_14"),
            "stop_loss": q.get("stop_loss_2atr"),
            "high52": q.get("fiftyTwoWeekHigh"),
            "low52": q.get("fiftyTwoWeekLow"),
        }
        for key, fallback in num_map.items():
            cur = rd.get(key)
            n = to_num(cur)
            if n is None:
                n = fallback
                if n is not None:
                    fixes.append(f"{key} 누락 → data.json 승계({n})")
            elif not isinstance(cur, (int, float)):
                fixes.append(f"{key} 문자열→숫자({n})")
            rd[key] = n

        # target_price 문자열→숫자
        tp = rd.get("target_price")
        tpn = to_num(tp)
        if tpn is not None and not isinstance(tp, (int, float)):
            fixes.append(f"target_price 문자열→숫자({tpn})")
            rd["target_price"] = tpn

        # 3) score 0~100 정수
        s = to_num(rd.get("score"))
        if s is not None:
            if s <= 10:
                s = s * 10
                fixes.append("score 0~10→0~100 교정")
            rd["score"] = int(round(max(0, min(100, s))))

        # 4) thesis dict 보장 (report_template.thesis_block 은 dict{claim,...} 기대)
        #    에이전트가 산문 문자열로 쓰면 {claim, grade_line} 으로 coerce (멱등).
        th = rd.get("thesis")
        if isinstance(th, str):
            rd["thesis"] = {
                "claim": th,
                "grade_line": f"{rd.get('grade','')} ({rd.get('score','')}점 / 100)",
            }
            fixes.append("thesis 문자열→dict coerce")
        elif isinstance(th, dict) and not th.get("grade_line"):
            th["grade_line"] = f"{rd.get('grade','')} ({rd.get('score','')}점 / 100)"
            rd["thesis"] = th

        json.dump(rd, open(rd_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        items_str = ",".join(str(x[1]) for x in rd.get("scorecard_items", []))
        fix_str = (" | 교정: " + "; ".join(fixes)) if fixes else " | 교정 없음"
        print(f"[{tk}] score={rd.get('score')} grade={rd.get('grade')} tp={rd.get('target_price')} "
              f"items=[{items_str}]{fix_str}")


if __name__ == "__main__":
    main()
