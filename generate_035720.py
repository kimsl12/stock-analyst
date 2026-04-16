import sys, os

_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _root)

_tmpl = os.path.join(_root, 'report_template.py')
if not os.path.exists(_tmpl):
    raise FileNotFoundError('report_template.py not found: ' + _tmpl)

from report_template import generate_report
import json

# Load data from external JSON
with open(os.path.join(_root, 'kakao_report_data.json'), encoding='utf-8') as f:
    data = json.load(f)

# Convert lists to tuples where needed
data['extra_kpis'] = [tuple(x) for x in data['extra_kpis']]
data['scorecard_items'] = [tuple(x) for x in data['scorecard_items']]

output_path = os.path.join(_root, 'reports', '035720_카카오_20260416.html')
generate_report(data, output_path)
