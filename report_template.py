#!/usr/bin/env python3
"""
report_template.py - 종목분석 HTML 리포트 생성 모듈
report-generator가 데이터 딕셔너리를 넘기면 HTML 파일을 생성한다.

사용법:
  from report_template import generate_report
  generate_report(data, output_path="reports/AAPL_Apple_20260406.html")
"""
import os, sys, json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from chart_templates import (
        radar_chart, bar_chart, line_chart,
        risk_heatmap, price_range_bar,
        donut_chart, etf_performance_chart
    )
    CHARTS = True
except ImportError:
    CHARTS = False

CSS = """
:root{--bg:#0F1923;--card:#1A2733;--text:#E8EAED;--sub:#9AA0A6;--buy:#26A69A;--sell:#EF5350;--warn:#FFA726;--blue:#42A5F5;--border:#2D3A45}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:16px;max-width:900px;margin:0 auto;font-size:16px;line-height:1.6}
.header{text-align:center;padding:24px 0;border-bottom:2px solid var(--border);margin-bottom:20px}
.header h1{font-size:28px;margin-bottom:4px}
.meta{color:var(--sub);font-size:14px}
.badge{display:inline-block;padding:4px 12px;border-radius:12px;font-size:13px;font-weight:600;margin:4px}
.b-buy{background:rgba(38,166,154,0.2);color:var(--buy)}
.b-sell{background:rgba(239,83,80,0.2);color:var(--sell)}
.b-hold{background:rgba(255,167,38,0.2);color:var(--warn)}
.b-score{background:rgba(66,165,245,0.15);color:var(--blue)}
.sec{background:var(--card);border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid var(--border)}
.sec h2{font-size:18px;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border)}
.sec h3{font-size:15px;color:var(--blue);margin:14px 0 8px}
.kg{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:12px 0}
.ki{background:rgba(255,255,255,0.03);padding:12px;border-radius:8px;text-align:center}
.ki .kl{font-size:12px;color:var(--sub);margin-bottom:2px}
.ki .kv{font-size:20px;font-weight:700}
.up{color:var(--buy)}.dn{color:var(--sell)}.nt{color:var(--warn)}
table{width:100%;border-collapse:collapse;margin:10px 0;font-size:14px}
th{background:rgba(255,255,255,0.05);padding:8px 10px;text-align:left;font-weight:600;border-bottom:1px solid var(--border)}
td{padding:7px 10px;border-bottom:1px solid rgba(255,255,255,0.03)}
tr:hover{background:rgba(255,255,255,0.02)}
.sc{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}
.sb,.tb{padding:14px;border-radius:10px;text-align:center}
.sb{background:rgba(239,83,80,0.1);border:1px solid var(--sell)}
.tb{background:rgba(38,166,154,0.1);border:1px solid var(--buy)}
.sb .sp{font-size:22px;font-weight:700;color:var(--sell)}
.tb .tp{font-size:22px;font-weight:700;color:var(--buy)}
.sl{font-size:12px;color:var(--sub)}
.cb{margin:14px 0;text-align:center}
.mw{display:inline-block;padding:4px 10px;border-radius:8px;font-size:13px;font-weight:600;background:rgba(38,166,154,0.2);color:var(--buy)}
.mn{display:inline-block;padding:4px 10px;border-radius:8px;font-size:13px;font-weight:600;background:rgba(66,165,245,0.2);color:var(--blue)}
.ri{padding:8px 12px;margin:6px 0;border-radius:8px;border-left:3px solid var(--warn)}
.rh{border-left-color:var(--sell);background:rgba(239,83,80,0.05)}
.rm{border-left-color:var(--warn);background:rgba(255,167,38,0.05)}
.rl{border-left-color:var(--buy);background:rgba(38,166,154,0.05)}
.disc{font-size:12px;color:var(--sub);text-align:center;padding:20px;margin-top:20px;border-top:1px solid var(--border)}
.dl-bar{position:sticky;top:0;z-index:99;background:var(--card);border-bottom:1px solid var(--border);padding:8px 16px;display:flex;justify-content:flex-end;gap:8px;margin:-16px -16px 16px}
.dl-btn{background:var(--blue);color:#fff;border:none;padding:6px 16px;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:4px}
.dl-btn:hover{opacity:0.85}
.dl-btn svg{width:14px;height:14px;fill:currentColor}
@media print{.dl-bar{display:none}}
@media(max-width:600px){.kg{grid-template-columns:repeat(2,1fr)}.sc{grid-template-columns:1fr}body{padding:10px;font-size:15px}.header h1{font-size:22px}}
"""

def _tbl(headers, rows):
    h = "".join("<th>{}</th>".format(x) for x in headers)
    b = ""
    for r in rows:
        b += "<tr>" + "".join("<td>{}</td>".format(c) for c in r) + "</tr>"
    return "<table><thead><tr>{}</tr></thead><tbody>{}</tbody></table>".format(h, b)

def _kpi(label, value):
    return '<div class="ki"><div class="kl">{}</div><div class="kv">{}</div></div>'.format(label, value)

def _fmtprice(val, cur="$"):
    if val is None: return "N/A"
    return "{}{:,.2f}".format(cur, val)

def _fmtcap(val, cur="$"):
    if val is None: return "N/A"
    if val >= 1e12: return "{}{:.2f}T".format(cur, val/1e12)
    if val >= 1e9: return "{}{:.1f}B".format(cur, val/1e9)
    if val >= 1e8: return "{:.1f}억".format(val/1e8)
    return "{}{:,.0f}".format(cur, val)

def generate_report(data, output_path=None):
    """
    data keys:
      필수: ticker, name, date, score, grade, current_price, currency
      KPI: market_cap, per, low52, high52, extra_kpis=[(label,val),...]
      손절: stop_loss, target_price, atr
      스코어: scorecard_items=[(name,score), ...]
      개요: executive_summary, company_overview, moat_rating, moat_details
      재무: financials_table={headers,rows}, financial_analysis
           revenue_data, op_income_data, fin_years, fin_unit, estimates_from
      밸류: valuation, valuation_table={headers,rows}
      모멘텀: momentum, consensus_table={headers,rows}
      산업: business_analysis, competition_table={headers,rows}
      리스크: risks=[{name,level,impact,desc},...], risk_summary
      전략: strategy
      ETF: asset_type="ETF", sectors=[(name,pct),...], etf_performance={periods,etf,index,etf_name,index_name}
      커스텀: custom_sections=[{title,content},...]
    """
    if output_path is None:
        t = data.get("ticker","X")
        n = data.get("name","X")
        d = data.get("date", datetime.now().strftime("%Y%m%d"))
        output_path = "reports/{}_{}_{}html".format(t, n, d)
    
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    cur = data.get("currency","$")
    parts = []
    
    # Header
    grade = data.get("grade","N/A")
    gc = "b-buy" if "buy" in str(grade).lower() or "매수" in str(grade) else ("b-sell" if "sell" in str(grade).lower() or "매도" in str(grade) else "b-hold")
    parts.append('<div class="header"><h1>{} ({})</h1><div class="meta">{} 종합 분석 리포트 | {}</div><div style="margin-top:8px"><span class="badge {}">{}</span> <span class="badge b-score">{}/100</span></div></div>'.format(
        data.get("name",""), data.get("ticker",""), data.get("asset_type","주식"), data.get("date",""), gc, grade, data.get("score","N/A")))
    
    # KPI
    kpis = [
        _kpi("현재가", _fmtprice(data.get("current_price"), cur)),
        _kpi("시가총액", _fmtcap(data.get("market_cap"), cur)),
        _kpi("PER", str(data.get("per","N/A"))),
        _kpi("52주 범위", "{}~{}".format(_fmtprice(data.get("low52"), cur), _fmtprice(data.get("high52"), cur))),
    ]
    for label, val in data.get("extra_kpis", []):
        kpis.append(_kpi(label, val))
    parts.append('<div class="sec"><h2>핵심 지표</h2><div class="kg">{}</div></div>'.format("".join(kpis)))
    
    # Executive Summary
    es = data.get("executive_summary","")
    if es:
        parts.append('<div class="sec"><h2>Executive Summary</h2><p>{}</p></div>'.format(es))
    
    # Stop Loss
    sl = data.get("stop_loss")
    tg = data.get("target_price")
    cp = data.get("current_price", 0)
    atr = data.get("atr")
    if sl and tg and cp:
        slp = (sl - cp) / cp * 100
        tgp = (tg - cp) / cp * 100
        chart = ""
        if CHARTS and data.get("low52") and data.get("high52"):
            try: chart = '<div class="cb">{}</div>'.format(price_range_bar(data["low52"], data["high52"], cp, sl, tg, cur))
            except: pass
        parts.append('<div class="sec"><h2>손절/목표가 (ATR 기반)</h2><div class="sc"><div class="sb"><div class="sl">손절가 (ATR 2x)</div><div class="sp">{}{:,.2f}</div><div class="dn" style="font-size:13px">{:+.1f}%</div></div><div class="tb"><div class="sl">목표가 (R:R 1:2)</div><div class="tp">{}{:,.2f}</div><div class="up" style="font-size:13px">{:+.1f}%</div></div></div>{}<p style="color:var(--sub);font-size:13px;text-align:center">ATR(14): {}{} | R:R 1:2</p></div>'.format(
            cur, sl, slp, cur, tg, tgp, chart, cur, "{:.2f}".format(atr) if atr else "N/A"))
    
    # Scorecard
    sc_items = data.get("scorecard_items", [])
    if sc_items:
        chart = ""
        if CHARTS:
            try: chart = '<div class="cb">{}</div>'.format(radar_chart(sc_items))
            except: pass
        rows = [[n, "{:.1f}".format(s), "/10"] for n, s in sc_items]
        parts.append('<div class="sec"><h2>스코어카드</h2>{}{}<p style="text-align:right;font-weight:700;margin-top:8px">종합: {}/100</p></div>'.format(
            chart, _tbl(["항목","점수","만점"], rows), data.get("score","N/A")))
    
    # Company Overview
    ov = data.get("company_overview","")
    moat = data.get("moat_rating","")
    if ov or moat:
        mc = "mw" if "Wide" in str(moat) else "mn"
        mb = '<span class="{}">{}</span>'.format(mc, moat) if moat else ""
        md = data.get("moat_details","")
        parts.append('<div class="sec"><h2>기업개요 & Moat {}</h2><p>{}</p>{}</div>'.format(
            mb, ov, "<h3>Moat 상세</h3><p>{}</p>".format(md) if md else ""))
    
    # Financials
    ft = data.get("financials_table")
    fa = data.get("financial_analysis","")
    if ft or fa:
        tbl = _tbl(ft["headers"], ft["rows"]) if ft else ""
        chart = ""
        if CHARTS and data.get("revenue_data") and data.get("op_income_data"):
            try: chart = '<div class="cb">{}</div>'.format(bar_chart(data.get("fin_years",[]), data["revenue_data"], data["op_income_data"], data.get("fin_unit","조원"), data.get("estimates_from")))
            except: pass
        parts.append('<div class="sec"><h2>재무분석</h2>{}{}{}</div>'.format(
            chart, tbl, "<h3>분석</h3><p>{}</p>".format(fa) if fa else ""))
    
    # Valuation
    vt = data.get("valuation_table")
    va = data.get("valuation","")
    if vt or va:
        tbl = _tbl(vt["headers"], vt["rows"]) if vt else ""
        parts.append('<div class="sec"><h2>밸류에이션</h2>{}{}</div>'.format(tbl, "<p>{}</p>".format(va) if va else ""))
    
    # Momentum
    mm = data.get("momentum","")
    ct = data.get("consensus_table")
    if mm or ct:
        tbl = _tbl(ct["headers"], ct["rows"]) if ct else ""
        parts.append('<div class="sec"><h2>모멘텀 & 컨센서스</h2>{}{}</div>'.format("<p>{}</p>".format(mm) if mm else "", tbl))
    
    # Business
    ba = data.get("business_analysis","")
    bt = data.get("competition_table")
    if ba or bt:
        tbl = _tbl(bt["headers"], bt["rows"]) if bt else ""
        parts.append('<div class="sec"><h2>산업 & 경쟁구도</h2>{}{}</div>'.format("<p>{}</p>".format(ba) if ba else "", tbl))
    
    # ETF specific
    if data.get("asset_type") == "ETF":
        sectors = data.get("sectors", [])
        perf = data.get("etf_performance")
        if CHARTS and sectors:
            try: parts.append('<div class="sec"><h2>섹터 배분</h2><div class="cb">{}</div></div>'.format(donut_chart(sectors)))
            except: pass
        if CHARTS and perf:
            try: parts.append('<div class="sec"><h2>수익률 비교</h2><div class="cb">{}</div></div>'.format(
                etf_performance_chart(perf["periods"], perf["etf"], perf["index"], perf.get("etf_name","ETF"), perf.get("index_name","Index"))))
            except: pass
    
    # Risks
    risks = data.get("risks", [])
    rs = data.get("risk_summary","")
    if risks or rs:
        ritems = ""
        rtuples = []
        for r in risks:
            nm = r.get("name","")
            lv = r.get("level","중")
            im = r.get("impact","중")
            ds = r.get("desc","")
            cls = "rh" if lv=="고" or im=="고" else ("rm" if lv=="중" else "rl")
            ritems += '<div class="ri {}"><strong>{}</strong> (발생: {}, 영향: {})<br><span style="color:var(--sub);font-size:13px">{}</span></div>'.format(cls, nm, lv, im, ds)
            rtuples.append((nm, lv, im))
        chart = ""
        if CHARTS and rtuples:
            try: chart = '<div class="cb">{}</div>'.format(risk_heatmap(rtuples))
            except: pass
        parts.append('<div class="sec"><h2>리스크 분석</h2>{}{}{}</div>'.format(
            "<p>{}</p>".format(rs) if rs else "", chart, ritems))
    
    # Strategy
    st = data.get("strategy","")
    if st:
        parts.append('<div class="sec"><h2>매매 전략</h2><p>{}</p></div>'.format(st))
    
    # Custom sections
    for sec in data.get("custom_sections", []):
        parts.append('<div class="sec"><h2>{}</h2>{}</div>'.format(sec.get("title",""), sec.get("content","")))
    
    # Disclaimer
    parts.append('<div class="disc">이 리포트는 AI가 자동 생성한 참고 자료이며, 투자 권유가 아닙니다.<br>투자 결정은 본인의 판단과 책임 하에 이루어져야 합니다.<br>생성일: {} | 종목분석 에이전트 v3.0</div>'.format(
        data.get("date", datetime.now().strftime("%Y-%m-%d"))))

    # Download bar (sticky top)
    fname = os.path.basename(output_path) if output_path else "report.html"
    dl_bar = (
        '<div class="dl-bar">'
        '<button class="dl-btn" onclick="downloadReport()" title="HTML 다운로드">'
        '<svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zm7-18v12.17l3.59-3.58L17 12l-5 5-5-5 1.41-1.41L12 14.17V2z"/></svg>'
        '다운로드'
        '</button>'
        '<button class="dl-btn" style="background:var(--border)" onclick="window.print()" title="PDF 인쇄">'
        '<svg viewBox="0 0 24 24"><path d="M19 8h-1V3H6v5H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zM8 5h8v3H8V5zm8 14H8v-4h8v4zm2-4v-2H6v2H4v-4c0-.55.45-1 1-1h14c.55 0 1 .45 1 1v4h-2z"/></svg>'
        'PDF'
        '</button>'
        '</div>'
    )
    dl_script = (
        '<script>'
        'function downloadReport(){{'
        'var a=document.createElement("a");'
        'a.href="data:text/html;charset=utf-8,"+encodeURIComponent(document.documentElement.outerHTML);'
        'a.download="{}";'
        'a.click();'
        '}}'
        '</script>'
    ).format(fname)

    body = dl_bar + "\n" + "\n".join(parts) + "\n" + dl_script
    
    html = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>""".format(title="{} ({}) 종합 분석".format(data.get("name",""), data.get("ticker","")), css=CSS, body=body)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    size = os.path.getsize(output_path)
    print("리포트 생성 완료: {} ({:,} bytes)".format(output_path, size))
    return output_path


if __name__ == "__main__":
    test = {
        "ticker": "AAPL", "name": "Apple", "date": "2026-04-06",
        "asset_type": "주식", "score": 78.5, "grade": "Buy",
        "current_price": 234.50, "market_cap": 3.57e12,
        "per": "33.2x", "low52": 169.21, "high52": 260.10, "currency": "$",
        "stop_loss": 215.30, "target_price": 272.90, "atr": 9.60,
        "executive_summary": "Apple은 서비스 고성장과 AI 전략으로 안정적 실적 유지 중.",
        "scorecard_items": [("Moat",8),("수익성",9),("성장성",6),("재무",9),("밸류",5),("모멘텀",7),("배당",4),("리스크",8),("산업",7),("경영",9)],
        "company_overview": "Apple Inc.는 글로벌 테크 기업으로 iPhone, Mac, 서비스 사업을 운영.",
        "moat_rating": "Wide Moat",
        "risks": [
            {"name":"중국 매출 의존","level":"중","impact":"고","desc":"매출 19%가 중국"},
            {"name":"AI 경쟁 심화","level":"중","impact":"중","desc":"Google/Samsung AI 확대"},
        ],
        "strategy": "현재가 기준 Hold. $220 이하 진입 시 매수 매력 상승.",
    }
    p = generate_report(test, "/tmp/test_report.html")
    with open(p) as f: lines = len(f.readlines())
    print("줄 수: {}".format(lines))
