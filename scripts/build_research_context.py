#!/usr/bin/env python3
"""
build_research_context.py — 종목별 리서치 KB 발췌 자동 배달 (v3.40 ①)

배경: 리서치 KB 132건 축적에 종목분석 인용 7건 (5.3%, 반도체 0건) — 분석가가
"찾아 읽어야" 하는 구조가 소비를 죽임 (2026-07-23 실측). 이 스크립트가 티커의
섹터에 해당하는 리서치 발췌를 분석 폴더에 배달해 "받는" 구조로 역전한다.

동작:
  1. algo-trading/data/sector_map.json 으로 티커 → 엔진 섹터 → 리서치 섹터(최대 2) 매핑
  2. knowledge-base/research/{sector}/ 의 _meta.md thesis + 최신 아이템 프론트매터
     (citation 완성 라인 + key_finding) 발췌
  3. analysis/{폴더}/research_context.md 저장 — 분석가는 citation 라인을 그대로 복사 인용

사용:
    python3 scripts/build_research_context.py NVDA                      # 최신 분석 폴더 자동 탐색
    python3 scripts/build_research_context.py NVDA --dir analysis/NVDA_NVIDIA_v6
    python3 scripts/build_research_context.py 005380 --stdout           # 파일 없이 출력만

게이트 연동 (②): research_context.md 존재 시 scorecard 는 📄 인용 1건 이상 또는
research_skip_reason 명기 의무 — scripts/check_research_citation.py 가 기계 검증.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "knowledge-base/research"
SECTOR_MAP = ROOT / "algo-trading/data/sector_map.json"
ANALYSIS = ROOT / "analysis"

KST = timezone(timedelta(hours=9))
MAX_SECTORS = 2
MAX_ITEMS_PER_SECTOR = 4

# 엔진 11종 섹터 → 리서치 KB 10섹터 (우선순위 순)
ENGINE_TO_RESEARCH = {
    "Tech": ["semiconductor", "tech_platform"],
    "Energy": ["energy"],
    "Utilities": ["energy"],
    "Healthcare": ["biotech"],
    "Financials": ["fintech", "macro"],
    "Industrials": ["industrials", "defense"],
    "Materials": ["industrials"],
    "Discretionary": ["consumer"],
    "Staples": ["consumer"],
    "Gold": ["macro"],
    "REIT": ["macro"],
}

# 티커 단위 강제 매핑 (엔진 섹터가 뭉뚱그리는 케이스)
TICKER_OVERRIDES = {
    # 반도체 (Tech 중 semiconductor 우선)
    **{t: ["semiconductor"] for t in (
        "NVDA AMD TSM ASML AMAT LRCX MU QCOM AVGO INTC TXN MRVL SNDK STX ANET "
        "SOXX SOXL SOXS 000660 005930 009150".split()
    )},
    # 플랫폼/소프트웨어
    **{t: ["tech_platform"] for t in "META GOOGL MSFT ORCL NOW SAP CRM ADBE IBM PLTR NFLX AMZN BABA 035420 035720".split()},
    # 자동차
    **{t: ["auto"] for t in "TSLA TM 005380".split()},
    # 방산
    **{t: ["defense", "industrials"] for t in "KTOS BA RKLB LUNR ASTS 012450".split()},
    # 바이오/헬스
    **{t: ["biotech"] for t in "LLY NVO ABBV MRK JNJ AZN NVS UNH ISRG TMO 207940 068270".split()},
}


def load_engine_sector(ticker: str):
    try:
        m = json.loads(SECTOR_MAP.read_text()).get("map", {})
        return (m.get(ticker) or {}).get("sector")
    except Exception:
        return None


def research_sectors(ticker: str) -> list:
    if ticker in TICKER_OVERRIDES:
        cands = list(TICKER_OVERRIDES[ticker])
    else:
        eng = load_engine_sector(ticker)
        cands = list(ENGINE_TO_RESEARCH.get(eng, [])) if eng else []
    if not cands:
        cands = ["macro"]  # 광범위 ETF·미상 → 매크로
    # 실존 + 아이템 보유 섹터만
    out = []
    for s in cands:
        d = RESEARCH / s
        if d.is_dir() and any(f.name != "_meta.md" for f in d.glob("*.md")):
            out.append(s)
    return out[:MAX_SECTORS]


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n([\s\S]*?)\n---", text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        kv = re.match(r"^(\w[\w_]*):\s*(.+)$", line.strip())
        if kv:
            out[kv.group(1)] = kv.group(2).strip().strip('"')
    return out


def sector_block(sector: str) -> str:
    d = RESEARCH / sector
    lines = [f"## 섹터: {sector}"]

    # thesis (있으면)
    meta = d / "_meta.md"
    if meta.exists():
        tm = re.search(r"##\s*현재 thesis[\s\S]*?\n\n- \*\*([^*]+)\*\*:\s*([^\n]+)", meta.read_text())
        if tm:
            lines.append(f"\n**현재 thesis — {tm.group(1)}**: {tm.group(2)}")

    # 아이템 최신순
    items = []
    for f in d.glob("*.md"):
        if f.name.startswith("_"):
            continue
        fm = parse_frontmatter(f.read_text())
        date = fm.get("date_collected") or fm.get("date_published") or "0000-00-00"
        items.append((date, f, fm))
    items.sort(key=lambda x: x[0], reverse=True)

    # L3 분기 Deep Dive 포인터 (HTML 파싱 대신 경로 안내 — S1 요약·S8 종목 매트릭스 섹션 참조)
    l3 = sorted((ROOT / "reports/research").glob(f"{sector}_*.html")) if (ROOT / "reports/research").is_dir() else []
    if l3:
        lines.append(f"\n**L3 분기 Deep Dive**: {l3[-1].relative_to(ROOT)} — 필요 시 Read 해 S1 Executive Summary + S8 종목 영향 매트릭스만 발췌 (전문 인용 금지)")

    lines.append("")
    for date, f, fm in items[:MAX_ITEMS_PER_SECTOR]:
        cit = fm.get("citation") or f"📄 [{fm.get('source_type','자료')}] {fm.get('source','?')} ({date[:7]}) — \"{fm.get('title', f.stem)}\""
        finding = fm.get("key_finding", "")
        rel = f.relative_to(ROOT)
        lines.append(f"- {cit}")
        if finding:
            lines.append(f"  - 핵심: {finding}")
        lines.append(f"  - 원문: {rel}")
    return "\n".join(lines)


def find_latest_dir(ticker: str):
    cands = sorted(
        (p for p in ANALYSIS.iterdir() if p.is_dir() and p.name.startswith(f"{ticker}_")),
        key=lambda p: int(re.search(r"_v(\d+)$", p.name).group(1)) if re.search(r"_v(\d+)$", p.name) else 0,
    )
    return cands[-1] if cands else None


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("사용법: build_research_context.py {TICKER} [--dir analysis/…] [--stdout]")
        return 1
    ticker = args[0]
    to_stdout = "--stdout" in sys.argv
    out_dir = None
    if "--dir" in sys.argv:
        out_dir = Path(sys.argv[sys.argv.index("--dir") + 1])
        if not out_dir.is_absolute():
            out_dir = ROOT / out_dir

    sectors = research_sectors(ticker)
    if not sectors:
        print(f"[research_context] {ticker}: 매핑되는 리서치 섹터 없음 — 컨텍스트 미생성 (게이트 미적용, 정상)")
        return 0

    body = [
        f"# Research KB 컨텍스트 — {ticker}",
        f"> 생성: {datetime.now(KST).strftime('%Y-%m-%d %H:%M KST')} · 섹터 {', '.join(sectors)} · build_research_context.py 자동 배달",
        "> **인용 규약**: 아래 `📄 …` citation 라인을 그대로 복사해 인용 (형식 SSOT: knowledge-base/research/_citation_format.md).",
        "> 분석 논지와 무관하면 스코어카드에 `research_skip_reason: <사유 1줄>` 명기 — 미인용·미사유는 검증 게이트에서 실패.",
        "",
    ]
    for s in sectors:
        body.append(sector_block(s))
        body.append("")
    text = "\n".join(body)

    if to_stdout:
        print(text)
        return 0

    if out_dir is None:
        out_dir = find_latest_dir(ticker)
    if out_dir is None or not out_dir.is_dir():
        print(f"[research_context] {ticker}: 분석 폴더 미발견 — --dir 지정 필요")
        return 1
    (out_dir / "research_context.md").write_text(text)
    n_items = text.count("📄")
    print(f"[research_context] {ticker}: 섹터 {', '.join(sectors)} · 발췌 {n_items}건 → {out_dir.relative_to(ROOT)}/research_context.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
