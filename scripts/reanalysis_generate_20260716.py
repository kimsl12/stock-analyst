#!/usr/bin/env python3
"""
재분석 HTML 생성 — 2026-07-16 (staock_update 슬롯, 10일 임계, 상한 10종)

이번 회차는 BLIND 분석 에이전트가 v폴더에 6개 .md 를 직접 작성했다 (기존 _content.json 패턴 아님).
따라서 md 본문을 HTML 로 변환해 custom_sections 로 싣고, 필수 필드는 data.json + scorecard grep 으로 채운다.

- 이미 존재하는 HTML 은 건너뛴다 (report-generator 에이전트가 만든 것 보존).
- 사용법: python3 scripts/reanalysis_generate_20260716.py [TICKER ...]
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from report_template import generate_report

TODAY = "2026-07-16"
YYYYMMDD = "20260716"

# ticker -> (folder, name_kr, next_v, asset_type)
PLAN = {
    "000660": ("SK하이닉스", "SK하이닉스", 5, "주식"),
    "000720": ("현대건설", "현대건설", 3, "주식"),
    "052690": ("한전기술", "한전기술", 3, "주식"),
    "BWXT": ("BWXTechnologies", "BWX테크놀로지스", 4, "주식"),
    "CCJ": ("Cameco", "카메코", 4, "주식"),
    "DUK": ("DukeEnergy", "듀크에너지", 4, "주식"),
    "JEPI": ("JPMorganEquityPremiumIncome", "JPM에퀴티프리미엄인컴", 3, "ETF"),
    "LQD": ("iSharesInvestmentGradeCorpBond", "iShares투자등급회사채", 3, "ETF"),
    "MLM": ("MartinMarietta", "마틴마리에타", 4, "주식"),
    "NEE": ("NextEraEnergy", "넥스트에라에너지", 4, "주식"),
}

SECTION_TITLES = [
    ("company.md", "§ 기업개요 &amp; 해자 (Moat)"),
    ("financial.md", "§ 재무 분석 &amp; 밸류에이션"),
    ("business.md", "§ 산업 &amp; 경쟁구도"),
    ("momentum.md", "§ 모멘텀 &amp; 수급"),
    ("risk.md", "§ 리스크 (Devil's Advocate)"),
    ("scorecard.md", "§ 종합 스코어카드"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md_to_html(md):
    """마크다운 → HTML. 표·제목·볼드·리스트·인용·코드 처리."""
    # 포매터 훅이 단독 `~` 를 `~~` 로 중복시킨 오염을 복구한다. 진짜 취소선은 `~~text~~` 쌍이다.
    #  - 범위 표기(`3~5%`, `2027말~2028`): 앞이 단어 문자 → 하이픈으로
    #  - 근사 표기(`~9.6%`, `~8.3년`): 앞이 공백/행두 → 물결 하나로
    md = re.sub(r"(?<=[\w가-힣%\)])~~(?=[\w가-힣$₩\-−])", "-", md)
    md = re.sub(r"(?<![\w가-힣~])~~(?=[\d$₩])", "~", md)

    lines = md.split("\n")
    out = []
    i = 0
    in_code = False
    while i < len(lines):
        ln = lines[i]

        # 코드 펜스
        if ln.strip().startswith("```"):
            if not in_code:
                out.append("<pre style='background:rgba(127,127,127,.12);padding:10px;border-radius:6px;overflow-x:auto'><code>")
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            out.append(esc(ln))
            i += 1
            continue

        # 표 (| a | b | 다음 줄이 |---|---|)
        if ln.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            hdr = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table><thead><tr>"]
            for h in hdr:
                t.append("<th>{}</th>".format(inline(h)))
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join("<td>{}</td>".format(inline(c)) for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        # 제목
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            lv = min(len(m.group(1)) + 1, 6)
            out.append("<h{lv} style='margin:14px 0 6px'>{txt}</h{lv}>".format(lv=lv, txt=inline(m.group(2))))
            i += 1
            continue

        # 인용 — 연속 `>` 줄을 모아 내부를 재귀 파싱한다 (인용 안에 표가 오는 경우가 있다)
        if ln.strip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append(
                "<blockquote style='border-left:3px solid var(--accent,#6aa9ff);padding-left:10px;margin:8px 0;opacity:.9'>{}</blockquote>".format(
                    md_to_html("\n".join(buf))
                )
            )
            continue

        # 리스트
        if re.match(r"^\s*[-*]\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append("<li>{}</li>".format(inline(re.sub(r"^\s*[-*]\s+", "", lines[i]))))
                i += 1
            out.append("<ul style='margin:6px 0 6px 18px'>" + "".join(items) + "</ul>")
            continue
        if re.match(r"^\s*\d+\.\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append("<li>{}</li>".format(inline(re.sub(r"^\s*\d+\.\s+", "", lines[i]))))
                i += 1
            out.append("<ol style='margin:6px 0 6px 18px'>" + "".join(items) + "</ol>")
            continue

        # 수평선
        if re.match(r"^\s*---+\s*$", ln):
            out.append("<hr style='border:0;border-top:1px solid rgba(127,127,127,.3);margin:12px 0'>")
            i += 1
            continue

        if ln.strip() == "":
            out.append("")
        else:
            out.append("<p style='margin:6px 0'>{}</p>".format(inline(ln)))
        i += 1

    return "\n".join(out)


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code style='background:rgba(127,127,127,.15);padding:1px 4px;border-radius:3px'>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def parse_scorecard(text):
    score = grade = tp = None
    m = re.search(r"\*\*종합 점수:\s*([0-9.]+)\s*/\s*100\*\*", text)
    if m:
        score = float(m.group(1))
        if score == int(score):
            score = int(score)
    m = re.search(r"\*\*투자 등급:\s*(강력매수|강력매도|매수|매도|중립)\*\*", text)
    if m:
        grade = m.group(1)
    m = re.search(r"\*\*목표주가:\s*([₩$][0-9,\.]+)\*\*", text)
    if m:
        tp = m.group(1)
    return score, grade, tp


def build(ticker):
    folder, kr, nv, atype = PLAN[ticker]
    vdir = "analysis/{}_{}_v{}".format(ticker, folder, nv)
    out_path = "reports/{}_{}_{}.html".format(ticker, folder, YYYYMMDD)

    if os.path.exists(out_path):
        print("  ⏭ {}: 이미 존재 — 건너뜀 ({} bytes)".format(ticker, os.path.getsize(out_path)))
        return None

    d = json.load(open("{}/data.json".format(vdir), encoding="utf-8"))
    sc_text = open("{}/scorecard.md".format(vdir), encoding="utf-8").read()
    score, grade, tp = parse_scorecard(sc_text)
    if score is None or grade is None:
        raise ValueError("scorecard 파싱 실패: score={} grade={}".format(score, grade))

    cur = d.get("currency", "$")
    prevv = nv - 1

    sections = [{
        "title": "§ 재분석 v{} 안내".format(nv),
        "content": (
            "<p><strong>재분석 v{nv} (이전 v{pv} 비교 미포함)</strong> — 본 리포트는 BLIND 모드로 작성됐다. "
            "분석가는 이전 v1~v{pv} 산출물·리포트·timeline 을 일절 참조하지 않고 현재 데이터에서 독립 추론했다. "
            "이전 회차와의 변화 비교는 <code>analysis/_reanalysis_runs/{ymd}_run.md</code> 의 변화표가 담당한다.</p>"
            "<p style='opacity:.85'>데이터 기준일 {date} · 데이터 소스 yfinance 단일 "
            "(본 슬롯은 WebSearch 미바인딩 — 미확인 항목은 본문에 '추정/불확실'로 명시했고 confidence 를 하향했다).</p>"
        ).format(nv=nv, pv=prevv, ymd=YYYYMMDD, date=d.get("date")),
    }]

    for fname, title in SECTION_TITLES:
        p = "{}/{}".format(vdir, fname)
        if not os.path.exists(p):
            continue
        sections.append({"title": title, "content": md_to_html(open(p, encoding="utf-8").read())})

    data = {
        "ticker": ticker,
        "name": kr if kr == folder else "{} ({})".format(kr, folder),
        "date": YYYYMMDD,
        "score": score,
        "grade": grade,
        "current_price": d["current_price"],
        "currency": cur,
        "market_cap": d.get("market_cap"),
        "low52": d.get("low_52w"),
        "high52": d.get("high_52w"),
        "asset_type": atype,
        "stop_loss": d.get("stop_loss_2atr"),
        "target_price": d.get("target_3atr"),
        "atr": d.get("atr_14"),
        "extra_kpis": [
            ("등급", grade),
            ("재분석", "v{} BLIND".format(nv)),
            ("펀더멘털 목표가", tp or "N/A"),
        ],
        "custom_sections": sections,
    }
    generate_report(data, output_path=out_path)
    print("  ✅ {}: {} ({:,} bytes) — {}점 {} TP {}".format(
        ticker, out_path, os.path.getsize(out_path), score, grade, tp))
    return out_path


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    print("=== 재분석 HTML 생성 — {} (10일 임계, 상한 10종) ===\n".format(TODAY))
    ok, skip, fail = [], [], []
    for t in only:
        try:
            r = build(t)
            (ok if r else skip).append(t)
        except Exception as e:
            print("  ❌ {}: {}".format(t, e))
            fail.append(t)
    print("\n=== 생성 {} / 건너뜀 {} / 실패 {} ===".format(len(ok), len(skip), len(fail)))
    if fail:
        print("실패:", ", ".join(fail))
        sys.exit(1)


if __name__ == "__main__":
    main()
