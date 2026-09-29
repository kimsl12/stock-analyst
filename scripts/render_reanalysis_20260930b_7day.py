#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 v{N} 중앙 HTML 렌더 — 2026-09-30b (/재분석실행 7 20→cap10, stock_update-2 슬롯).
정규화 완료된 각 폴더 _report_data.json 을 report_template.generate_report 로 렌더.
report-generator 서브에이전트 자체 commit/deploy 회피 위해 메인이 중앙 렌더."""
import json, os, sys

ROOT = "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
sys.path.insert(0, ROOT)
from report_template import generate_report

DATE = "20260930"
# ticker -> (folder(name만), next_v)
PLAN = {
    "000660": ("SK하이닉스",         13),
    "000720": ("현대건설",           11),
    "035420": ("NAVER",             18),
    "052690": ("한전기술",           11),
    "066570": ("LG전자",            15),
    "BWXT":   ("BWXTechnologies",   12),
    "LLY":    ("EliLilly",          18),
    "LUNR":   ("IntuitiveMachines", 17),
    "LVMUY":  ("LVMH",              18),
    "MA":     ("Mastercard",        17),
}


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    for tk in only:
        folder, nv = PLAN[tk]
        d = f"{ROOT}/analysis/{tk}_{folder}_v{nv}"
        rp = f"{d}/_report_data.json"
        out = f"{ROOT}/reports/{tk}_{folder}_{DATE}.html"
        if not os.path.exists(rp):
            print(f"❌ {tk}: _report_data.json 없음")
            fail.append(tk); continue
        try:
            data = json.load(open(rp, encoding="utf-8"))
            generate_report(data, out)
            sz = os.path.getsize(out)
            print(f"[{tk}] OK v{nv} score={data.get('score')} grade={data.get('grade')} tp={data.get('target_price')} -> reports/{tk}_{folder}_{DATE}.html ({sz//1024}KB)")
            ok.append(tk)
        except Exception as e:
            print(f"❌ {tk}: 렌더 실패 {e}")
            fail.append(tk)
    print(f"\n=== 렌더 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
