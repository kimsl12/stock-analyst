#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 v{N} HTML 리포트 생성 — 2026-10-14 (7일 임계, stock_update-2 슬롯, /재분석실행 7 20).
각 폴더의 _report_data.json 을 normalize(스케일 가드) 후 report_template.generate_report 로 HTML 생성.
출력: reports/{ticker}_{folder}_20261013.html
normalize 가드:
  - scorecard_items 점수가 10 초과면 /10 (0~100 드리프트 교정) + [0,10] clamp
  - target_price 문자열($ , 포함) → 숫자
  - score 정수 0~100 보정
  - extra_kpis / risks 스키마 코어션
"""
import json, os, sys, re
ROOT = "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
sys.path.insert(0, ROOT)
from report_template import generate_report

DATE = "20261014"
# ticker -> (folder(name만), next_v)
PLAN = {
    "466100": ("클로봇",                      19),
    "ADBE":   ("Adobe",                       20),
    "009150": ("삼성전기",                     19),
    "005380": ("현대차",                       12),
    "010120": ("LSELECTRIC",                   20),
    "AGG":    ("iSharesCoreUSAggregateBond",   18),
    "VIG":    ("VanguardDividendAppreciation", 17),
    "207940": ("삼성바이오로직스",              12),
    "VRT":    ("VertivHoldings",               17),
    "ABBV":   ("AbbVie",                       18),
}


def _num(x):
    if isinstance(x, (int, float)):
        return x
    if isinstance(x, str):
        m = re.search(r"-?[\d,]+\.?\d*", x.replace(",", ""))
        if m:
            try:
                return float(m.group().replace(",", ""))
            except Exception:
                return None
    return None


def normalize(data):
    notes = []
    # scorecard_items 스케일 가드
    items = data.get("scorecard_items", []) or []
    fixed = []
    mx = 0
    for it in items:
        try:
            name, sc = it[0], it[1]
        except Exception:
            continue
        s = _num(sc)
        if s is None:
            s = 0
        mx = max(mx, s)
        fixed.append([name, s])
    if mx > 10:  # 0~100 드리프트 → /10
        notes.append(f"scorecard_items 0~100 드리프트 감지(max={mx}) → /10 교정")
        fixed = [[n, round(s / 10, 1)] for n, s in fixed]
    # clamp [0,10]
    fixed = [[n, max(0, min(10, s))] for n, s in fixed]
    # 정수화(소수점 .0 이면 int)
    fixed = [[n, int(s) if float(s).is_integer() else s] for n, s in fixed]
    data["scorecard_items"] = fixed

    # target_price 숫자화
    tp = data.get("target_price")
    tpn = _num(tp)
    if tpn is not None:
        data["target_price"] = int(tpn) if float(tpn).is_integer() else round(tpn, 2)
        if not isinstance(tp, (int, float)):
            notes.append(f"target_price 문자열→숫자({tp!r}→{data['target_price']})")

    # score 정수 0~100
    sc = _num(data.get("score"))
    if sc is not None:
        data["score"] = int(round(sc))

    # extra_kpis 코어션: dict{label,value[,desc]} 또는 비2튜플 → [label, value]
    ek = data.get("extra_kpis", []) or []
    ek_fixed = []
    ek_drift = False
    for x in ek:
        if isinstance(x, dict):
            ek_fixed.append([x.get("label", x.get("name", "")), x.get("value", "")])
            ek_drift = True
        elif isinstance(x, (list, tuple)):
            if len(x) == 2:
                ek_fixed.append([x[0], x[1]])
            elif len(x) > 2:
                ek_fixed.append([x[0], x[1]]); ek_drift = True
            elif len(x) == 1:
                ek_fixed.append([x[0], ""]); ek_drift = True
    if ek_drift:
        notes.append("extra_kpis 스키마 드리프트 → [label,value] 코어션")
    data["extra_kpis"] = ek_fixed

    # risks 코어션: 문자열 → {name, level, impact, desc}
    rk = data.get("risks", []) or []
    rk_fixed = []
    rk_drift = False
    for r in rk:
        if isinstance(r, dict):
            rk_fixed.append(r)
        elif isinstance(r, str):
            if ":" in r:
                nm, ds = r.split(":", 1)
            elif "：" in r:
                nm, ds = r.split("：", 1)
            else:
                nm, ds = (r[:24], r)
            rk_fixed.append({"name": nm.strip(), "level": "중간", "impact": "—", "desc": ds.strip()})
            rk_drift = True
    if rk_drift:
        notes.append("risks 문자열 → dict 코어션")
    data["risks"] = rk_fixed

    return data, notes


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
            data, notes = normalize(data)
            if notes:
                with open(rd_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            out = f"{ROOT}/reports/{tk}_{folder}_{DATE}.html"
            generate_report(data, out)
            sz = os.path.getsize(out)
            nstr = (" | NORM:" + "; ".join(notes)) if notes else ""
            print(f"[{tk}] OK -> reports/{tk}_{folder}_{DATE}.html ({sz:,} bytes) "
                  f"score={data.get('score')} grade={data.get('grade')} tp={data.get('target_price')} "
                  f"items_max={max((s for _,s in data.get('scorecard_items',[])), default='NA')}{nstr}")
            ok.append(tk)
        except Exception as e:
            import traceback
            print(f"  X {tk}: EXC {e}")
            traceback.print_exc()
            fail.append(tk)
    print(f"\n=== 리포트 생성 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
