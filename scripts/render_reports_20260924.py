#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 v{N} HTML 리포트 생성 — 2026-09-24 (/재분석실행 7 20→cap10, stock_update-2 7일 슬롯).
각 폴더의 _report_data.json 을 읽어 report_template.generate_report 로 HTML 생성.
출력: reports/{ticker}_{folder}_20260924.html
정규화 가드: target_price/stop_loss/atr/score/current_price 를 숫자로 강제(에이전트 문자열 드리프트 방어).
"""
import json, os, sys, re
ROOT = "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
sys.path.insert(0, ROOT)
from report_template import generate_report

DATE = "20260924"
# ticker -> (folder(name만), next_v)
PLAN = {
    "V":    ("Visa",                  17),
    "TSLA": ("Tesla",                 17),
    "TQQQ": ("ProSharesUltraProQQQ",  17),
    "TIP":  ("iSharesTIPS",           17),
    "IWM":  ("iSharesRussell2000",    17),
    "GEV":  ("GEVernova",             15),
    "DIA":  ("SPDRDJIA",              17),
    "BRKB": ("BerkshireHathaway",     17),
    "BAC":  ("BankOfAmerica",         17),
    "BABA": ("Alibaba",               17),
}

NUM_KEYS = ("target_price", "stop_loss", "atr", "score", "current_price", "low52", "high52", "market_cap")


def _to_num(v):
    if v is None or isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        m = re.search(r"-?[\d,]+\.?\d*", v.replace(",", ""))
        if m:
            try:
                f = float(m.group())
                return int(f) if f == int(f) else f
            except Exception:
                return v
    return v


def normalize(data):
    for k in NUM_KEYS:
        if k in data:
            data[k] = _to_num(data[k])
    si = data.get("scorecard_items")
    if isinstance(si, list):
        data["scorecard_items"] = [[it[0], _to_num(it[1])] if isinstance(it, list) and len(it) == 2 else it for it in si]
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
            data = normalize(json.load(open(rd_path, encoding="utf-8")))
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
