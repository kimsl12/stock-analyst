#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 v{N} HTML 리포트 생성 — 2026-09-28 (/재분석실행 7 20→cap10, stock_update-2 슬롯).
각 폴더의 _report_data.json 을 읽어 report_template.generate_report 로 HTML 생성.
출력: reports/{ticker}_{folder}_20260928.html
중앙 정규화: 숫자 필드(current_price·market_cap·high52·low52·atr·stop_loss·target_price·score)를
  float/int 로 강제 coerce(문자열·$₩,% strip). BLIND 에이전트가 문자열로 써도 렌더 ValueError 방지.
"""
import json, os, re, sys
ROOT = "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
sys.path.insert(0, ROOT)
from report_template import generate_report

DATE = "20260928"
# ticker -> (folder(name만), next_v)
PLAN = {
    "VMC":  ("VulcanMaterials",          12),
    "SOXS": ("Direxion3xSemiBear",       17),
    "T":    ("ATT",                      17),
    "SOXL": ("Direxion3xSemiconductor",  17),
    "VOO":  ("VanguardSP500",            17),
    "TTE":  ("TotalEnergies",            17),
    "TSM":  ("TSMC",                     17),
    "TXN":  ("TexasInstruments",         17),
    "TMUS": ("TMobile",                  18),
    "SNDK": ("Sandisk",                  19),
}

NUM_FIELDS = ["current_price", "market_cap", "high52", "low52", "atr", "stop_loss", "target_price"]


def _coerce_num(v):
    if v is None or isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        s = re.sub(r"[,$₩%\s]", "", v)
        s = re.sub(r"[A-Za-z].*$", "", s)  # 'x' 등 접미사 제거
        try:
            f = float(s)
            return int(f) if f.is_integer() else f
        except ValueError:
            return None
    return v


def normalize(data):
    for k in NUM_FIELDS:
        if k in data:
            data[k] = _coerce_num(data[k])
    # score: 숫자 우선(문자열도 template가 str()로 처리하나 통일)
    if "score" in data and isinstance(data["score"], str):
        n = _coerce_num(data["score"])
        if n is not None:
            data["score"] = n
    # scorecard_items 점수 float
    fixed = []
    for item in data.get("scorecard_items", []):
        if isinstance(item, (list, tuple)) and len(item) == 2:
            n = _coerce_num(item[1])
            fixed.append([item[0], n if n is not None else item[1]])
        else:
            fixed.append(item)
    if fixed:
        data["scorecard_items"] = fixed
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
                  f"score={data.get('score')} grade={data.get('grade')} tp={data.get('target_price')} cp={data.get('current_price')}")
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
