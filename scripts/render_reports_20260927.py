#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 v{N} HTML 리포트 생성 — 2026-09-27 (/재분석실행 10 10, staock_update 슬롯).
각 폴더의 _report_data.json 을 읽어 report_template.generate_report 로 HTML 생성.
출력: reports/{ticker}_{folder}_20260927.html
"""
import json, os, sys
ROOT = "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
sys.path.insert(0, ROOT)
from report_template import generate_report

DATE = "20260927"
# ticker -> (folder(name만), next_v)
PLAN = {
    "STX":  ("Seagate",                 17),
    "SMR":  ("NuScalePower",            15),
    "SCHD": ("SchwabUSDividendEquity",  16),
    "RSP":  ("InvescoSP500EqualWeight", 16),
    "QQQ":  ("InvescoQQQ",              16),
    "QLD":  ("ProSharesUltraQQQ",       15),
    "QCOM": ("Qualcomm",                10),
    "PM":   ("PhilipMorris",            17),
    "PEP":  ("PepsiCo",                 17),
    "NOW":  ("ServiceNow",              10),
}


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
