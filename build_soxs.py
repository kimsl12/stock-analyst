# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, os.getcwd())
from report_template import generate_report

with open("analysis/SOXS_Direxion3xSemiBear/soxs_payload.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# JSON은 tuple을 지원하지 않으므로 list를 tuple로 변환 (report_template 호환)
if "extra_kpis" in data:
    data["extra_kpis"] = [tuple(x) for x in data["extra_kpis"]]
if "scorecard_items" in data:
    data["scorecard_items"] = [tuple(x) for x in data["scorecard_items"]]
if "sectors" in data:
    data["sectors"] = [tuple(x) for x in data["sectors"]]

p = generate_report(data, "reports/SOXS_Direxion3xSemiBear_20260415.html")
print("OK: " + str(p))
