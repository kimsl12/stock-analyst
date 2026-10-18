#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
글로벌 인텔리전스 (MODULE G) md -> HTML 조립기 (2026-10-18 일요일 예약 실행)
- briefing-report-generator 대용량 토큰 초과 사망 우회: 메인 직접 조립 (프로젝트 메모리)
- CSS/JS 는 reference/briefing_css.html 에서 추출, 본문은 lead 종합 + global-macro-analyst 마크다운 변환
- debate-card / contrarian-card h2 는 전용 컬러 카드 div 로 래핑
"""
import re, json, html, pathlib

ROOT   = pathlib.Path("/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트")
LEAD   = ROOT / "analysis/briefing/lead_global_intelligence_20261018.md"
MACRO  = ROOT / "analysis/briefing/global_macro_20261018.md"
CSSF   = ROOT / "reference/briefing_css.html"
REG    = ROOT / "knowledge-base/market/regime.json"
OUT    = ROOT / "reports/briefing/global_intelligence_20261018.html"
DATE   = "2026-10-18"

# ---------- 1. CSS / JS 추출 (상단 주석 placeholder 오염 제거 후) ----------
cssraw = CSSF.read_text(encoding="utf-8")
cssraw = re.sub(r"^\s*<!--.*?-->", "", cssraw, count=1, flags=re.S)
STYLE  = re.search(r"<style>.*?</style>", cssraw, re.S).group(0)
SCRIPT = re.search(r"<script>.*?</script>", cssraw, re.S).group(0)
assert len(STYLE) > 5000 and len(SCRIPT) > 200, f"CSS/JS 추출 실패: STYLE={len(STYLE)} SCRIPT={len(SCRIPT)}"

# ---------- 2. 본문 마크다운 조립 (lead 종합 + analyst G-0~ citations) ----------
def strip_front(t):
    return re.sub(r"^---\n.*?\n---\n", "", t, count=1, flags=re.S)

def from_first_h2(t):
    i = t.find("\n## ")
    return t[i+1:] if i != -1 else t

lead = from_first_h2(strip_front(LEAD.read_text(encoding="utf-8")))
# lead 의 '매크로 위험 등급' 섹션은 analyst 상세 표가 대신 → HTML 에서 제거(중복 방지)
cut = lead.find("\n## 매크로 위험 등급")
if cut != -1:
    lead = lead[:cut]

macro = from_first_h2(MACRO.read_text(encoding="utf-8"))

body_md = "# GI\n\n" + lead.strip() + "\n\n---\n\n" + macro.strip()
first = body_md.find("\n## ")
body_md = body_md[first+1:]

# ---------- 3. 인라인 포맷 ----------
def inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"\[([^\]]+?)\]\((https?://[^)]+?)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"`([^`]+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"~~(.+?)~~", r"<del>\1</del>", t)
    t = re.sub(r"(?<![\*\w])\*(?!\*)(\S.*?\S|\S)\*(?!\*)", r"<em>\1</em>", t)
    return t

def is_table_row(l): return ("|" in l) and (l.strip().startswith("|") or l.count("|") >= 2)
def is_sep_row(l):   return bool(re.fullmatch(r"[\s|:\-]+", l)) and "-" in l

lines = body_md.split("\n")
out = []
i = 0
sec_open = False
def close_sec():
    global sec_open
    if sec_open:
        out.append("</div>")
        sec_open = False

RAWSTART = re.compile(r'^\s*<')

while i < len(lines):
    line = lines[i]
    s = line.strip()

    if s == "":
        i += 1; continue
    if re.fullmatch(r"-{3,}", s):
        i += 1; continue

    # 원시 HTML passthrough
    if RAWSTART.match(line):
        while i < len(lines) and lines[i].strip() != "":
            out.append(lines[i]); i += 1
        continue

    # 헤더 — debate/contrarian 은 전용 카드 div
    if s.startswith("## "):
        close_sec()
        title = s[3:].strip()
        cls = "sec"
        if "debate-card" in title:
            cls = "debate-card"
        elif "contrarian-card" in title:
            cls = "contrarian-card"
        out.append('<div class="%s"><h2>%s</h2>' % (cls, inline(title)))
        sec_open = True
        i += 1; continue
    if s.startswith("### "):
        out.append("<h3>%s</h3>" % inline(s[4:].strip())); i += 1; continue
    if s.startswith("#### "):
        out.append("<h4>%s</h4>" % inline(s[5:].strip())); i += 1; continue

    # 테이블
    if is_table_row(line):
        tbl = []
        while i < len(lines) and is_table_row(lines[i]):
            tbl.append(lines[i]); i += 1
        def cells(row):
            r = row.strip()
            if r.startswith("|"): r = r[1:]
            if r.endswith("|"):  r = r[:-1]
            return [c.strip() for c in r.split("|")]
        sep_idx = next((k for k,r in enumerate(tbl) if is_sep_row(r)), None)
        out.append('<div style="overflow-x:auto"><table>')
        if sep_idx is not None:
            for h in tbl[:sep_idx]:
                out.append("<tr>" + "".join("<th>%s</th>" % inline(c) for c in cells(h)) + "</tr>")
            data = tbl[sep_idx+1:]
        else:
            data = tbl
        for r in data:
            out.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in cells(r)) + "</tr>")
        out.append("</table></div>")
        continue

    # 블록쿼트
    if s.startswith(">"):
        buf = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
            i += 1
        inner = "<br>".join(inline(b) if b.strip() != "" else "" for b in buf)
        out.append('<div class="deepdive" style="border-left:3px solid var(--highlight);background:var(--card2);padding:10px 14px;margin:12px 0;border-radius:6px;font-size:14px">%s</div>' % inner)
        continue

    # 리스트
    if re.match(r"^\s*[-*]\s+", line):
        items = []
        while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
            items.append(re.sub(r"^\s*[-*]\s+", "", lines[i])); i += 1
        out.append("<ul style='padding-left:20px;margin:8px 0'>" + "".join("<li>%s</li>" % inline(it) for it in items) + "</ul>")
        continue
    if re.match(r"^\s*\d+\.\s+", line):
        items = []
        while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
            items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i])); i += 1
        out.append("<ol style='padding-left:22px;margin:8px 0'>" + "".join("<li>%s</li>" % inline(it) for it in items) + "</ol>")
        continue

    # 문단
    para = []
    start_i = i
    def _is_block_start(cur):
        cs2 = cur.strip()
        return (cs2 == "" or re.match(r"^#{1,6}\s", cs2) or cs2.startswith(">")
                or re.match(r"^\s*[-*]\s+", cur) or re.match(r"^\s*\d+\.\s+", cur)
                or RAWSTART.match(cur) or is_table_row(cur) or re.fullmatch(r"-{3,}", cs2))
    while i < len(lines) and not _is_block_start(lines[i]):
        para.append(lines[i].strip()); i += 1
    if para:
        out.append("<p>%s</p>" % inline(" ".join(para)))
    elif i == start_i:
        out.append("<p>%s</p>" % inline(lines[i].strip())); i += 1

close_sec()
BODY = "\n".join(out)

# ---------- 4. 헤더 + meta-box ----------
reg = json.loads(REG.read_text(encoding="utf-8"))
regime_strip = reg.get("strip_html", "")
regime_line = (
    "<strong>리스크오프 2일째</strong> — 추세 하락(MA20 −1.03%) · VIX 20.0(중·금 +21%) · "
    "10Y 5.10%(−12bp·2007래권 5%+ 고착) · 2Y 4.77% · 10Y-2Y +0.35(커브 플래트닝·베어 스티프닝 반전) · "
    "BEI 2.35% · HY 3.23%(+8bp 재확대) · F&amp;G 17.9(극단공포·1주 전 46.5) · 크립토 F&amp;G 53 · "
    "금 $4,181(리스크오프에도 홀딩·HV5) · WTI $99/$110(+10% WoW·HV4) · DXY 121.6(2개월래+ 최강) · "
    "BTC $82.0K(V자 회복·NASDAQ↔BTC −1.65σ 탈동조 HV6) → 가중치 <strong>하락장</strong>"
)

HEADER = f'''<div class="header">
<h1>🌐 글로벌 인텔리전스 (MODULE G) — {DATE} (일)</h1>
<div class="meta">메인 스레드 직접 조립 (generator 토큰 초과 우회) · global-macro-analyst(mode=full) 작성 · {DATE} 21:1x KST · 일요일 예약 실행</div>
<div class="meta" style="margin-top:4px">레짐: {regime_line}</div>
{regime_strip}
</div>

<div class="sec meta-box"><div>작성: global-macro-analyst (mode=full, 주간 예약 실행) + 메인 스레드 종합 레이어</div><div>데이터 기준: knowledge-base/macro/ 8파일(10/17~10/18 주간 KB 점검 fresh) + market/ (regime 10/18·correlation 10/18·economic_calendar·surprise_index·prediction_markets) + fred_snapshot.json(10/18 20:36) + 이번 주 lead(10/17 weekly·10/17~10/18 evening) + research KB(macro·energy·semiconductor L2)</div><div>휴장 맥락: 주말 전면 휴장 48시간째(미·한·아시아·프리마켓 없음·미 선물 KST 월 07:00 재개장 대기). 지수·FX·원자재·금리는 10/16(금) 확정 종가 승계, 크립토만 라이브. 다음 거래일 = 월요일 10/19(한국 재개장)</div><div>웹검색: 보조 1회(Bessent–He/APEC — real-world 2025 오염 확인 → 방향만 교차 확증·KB SSOT 우선). --skip-collect(KB 신선도 충분)</div><div style="color:var(--warning);margin-top:6px">⚠️ 본 문서는 관찰·해석·시나리오 목적이며 매수·매도·비중조정 추천이 아님. 셧다운 D+17 데이터 블랙아웃 — 9월 CPI/고용 공식 미발표(단일 수치 단정 금지)·dovish_reflex 가드(시뮬 2026=매파)·prediction_markets stale·13F 시차 경고 적용</div></div>
'''

TOGGLE = '''<div style="position:sticky;top:0;z-index:99;background:var(--card);border-bottom:1px solid var(--border);padding:8px 16px;display:flex;justify-content:flex-end">
<button onclick="toggleTheme()" style="background:transparent;color:var(--text);border:1px solid var(--border);padding:6px 16px;border-radius:8px;font-size:13px;cursor:pointer;font-family:inherit">
<span id="theme-icon">☀️</span> <span id="theme-label">라이트 모드</span></button></div>'''

full = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>글로벌 인텔리전스 (MODULE G) — {DATE}</title>
{STYLE}
</head>
<body>

{TOGGLE}

{HEADER}
{BODY}

{SCRIPT}
</body>
</html>
'''

OUT.write_text(full, encoding="utf-8")
print("WROTE", OUT, len(full), "bytes")
print("sections(h2):", BODY.count('<div class="sec"') + BODY.count('<div class="debate-card"') + BODY.count('<div class="contrarian-card"'))
print("tables:", BODY.count("<table>"), "debate:", BODY.count('class="debate-card"'), "contrarian:", BODY.count('class="contrarian-card"'))
