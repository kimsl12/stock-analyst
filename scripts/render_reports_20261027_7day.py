#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 v{N} HTML 리포트 생성 — 2026-10-27 (재분석실행 7 20, stock_update-2 7일 슬롯).
각 폴더의 _report_data.json 을 읽어 normalize 가드 적용 후 report_template.generate_report 로 HTML 생성.
출력: reports/{ticker}_{folder}_20261027.html
normalize 가드: scorecard_items>10 → /10 · score 0~100정수 · custom_sections body→content · risks 기본값 · extra_kpis dict→pair · date 2026-10-26 강제."""
import json, os, sys
ROOT = "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
sys.path.insert(0, ROOT)
from report_template import generate_report

DATE = "20261027"
# ticker -> (folder(name만), next_v)
PLAN = {
    "000660": ("SK하이닉스",       16),
    "000720": ("현대건설",         14),
    "035420": ("NAVER",            21),
    "052690": ("한전기술",         14),
    "066570": ("LG전자",           18),
    "AXP":    ("AmericanExpress",  13),
    "BA":     ("Boeing",           20),
    "BHP":    ("BHPGroup",         21),
    "BKNG":   ("Booking",          13),
    "BLK":    ("BlackRock",        20),
}


def _fix_score(s):
    try:
        s = float(s)
    except Exception:
        return 0.0
    if s > 10:          # 0~100 오입력 → /10
        s = round(s / 10, 1)
    if s > 10:
        s = 10.0
    if s < 0:
        s = 0.0
    return s


def _parse_cap(v):
    """market_cap 문자열("$1.79T","$45.3B(총자산)") → 숫자. report_template._fmtcap 은 숫자만 처리."""
    if v is None or isinstance(v, (int, float)):
        return v
    s = str(v)
    import re
    m = re.search(r"([0-9][0-9,\.]*)\s*([TBM억]?)", s)
    if not m:
        return v
    try:
        num = float(m.group(1).replace(",", ""))
    except Exception:
        return v
    suf = m.group(2)
    mult = {"T": 1e12, "B": 1e9, "M": 1e6, "억": 1e8, "": 1.0}.get(suf, 1.0)
    return num * mult


def normalize(data):
    """schema drift 멱등 교정."""
    if "market_cap" in data:
        data["market_cap"] = _parse_cap(data.get("market_cap"))
    items = data.get("scorecard_items") or []
    fixed = []  # report_template 은 [name, score] 쌍 리스트를 기대 (for n, s in sc_items)
    for it in items:
        if isinstance(it, dict):
            name = it.get("name") or it.get("label") or ""
            fixed.append([str(name), _fix_score(it.get("score"))])
        elif isinstance(it, (list, tuple)) and len(it) >= 2:
            fixed.append([str(it[0]), _fix_score(it[1])])
    if fixed:
        data["scorecard_items"] = fixed
    sc = data.get("score")
    try:
        data["score"] = int(round(float(sc)))
    except Exception:
        pass
    for sec in data.get("custom_sections", []) or []:
        if isinstance(sec, dict) and not sec.get("content") and sec.get("body"):
            sec["content"] = sec["body"]
    # date 2026-10-27 강제(에이전트가 다른 날짜로 썼을 수 있음 — run-date 컨벤션 일치)
    data["date"] = "2026-10-27"
    # extra_kpis dict → [label,value] pair 강제 (report_template 은 pair 언패킹)
    ek = data.get("extra_kpis") or []
    fixed_ek = []
    for it in ek:
        if isinstance(it, dict):
            fixed_ek.append([str(it.get("label") or it.get("name") or ""), str(it.get("value") or it.get("val") or "")])
        elif isinstance(it, (list, tuple)) and len(it) >= 2:
            fixed_ek.append([str(it[0]), str(it[1])])
    if ek:
        data["extra_kpis"] = fixed_ek
    for r in data.get("risks", []) or []:
        if isinstance(r, dict):
            r.setdefault("level", "중간")
            r.setdefault("impact", "—")
            r.setdefault("desc", "")
            r.setdefault("name", "")
    return data


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    for tk in only:
        folder, nv = PLAN[tk]
        rd_path = f"{ROOT}/analysis/{tk}_{folder}_v{nv}/_report_data.json"
        if not os.path.exists(rd_path):
            print(f"  X {tk}: _report_data.json 없음 ({rd_path})")
            fail.append(tk); continue
        try:
            data = json.load(open(rd_path, encoding="utf-8"))
            data = normalize(data)
            out = f"{ROOT}/reports/{tk}_{folder}_{DATE}.html"
            generate_report(data, out)
            sz = os.path.getsize(out)
            print(f"[{tk}] OK -> reports/{tk}_{folder}_{DATE}.html ({sz:,} bytes) "
                  f"score={data.get('score')} grade={data.get('grade')} tp={data.get('target_price')}")
            ok.append(tk)
        except Exception as e:
            import traceback
            print(f"  X {tk}: EXC {e}")
            traceback.print_exc()
            fail.append(tk)
    print(f"\n=== 리포트 생성 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))
        sys.exit(1)


if __name__ == "__main__":
    main()
