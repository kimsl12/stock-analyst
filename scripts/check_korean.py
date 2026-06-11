#!/usr/bin/env python3
"""
check_korean.py — 리포트 한국어 강제 검증 + 자동 치환 (v3.30, 2026-06-11)

reference/korean_translation_rules.md 의 v3.22 검증 파이프라인을 스크립트화.
기존에는 에이전트가 40줄 bash/perl 스니펫을 매번 베껴 실행해야 해서 스킵·오실행이
잦았다 (한국어 룰 미준수의 실원인). 이제 한 줄 실행 + 매핑 치환은 기계가 직접 수행.

사용:
    python3 scripts/check_korean.py reports/briefing/morning_20260611.html         # 검증만
    python3 scripts/check_korean.py --fix reports/briefing/morning_20260611.html   # 매핑 자동 치환 후 검증

검증 항목 (v3.22 룰 동일):
    1. 매핑 사전 영어 표현 잔류 (korean_translation_rules.md 의 표를 파싱 — SSOT 유지)
    2. 본문 한글 비중 ≥ 80% (예외: 고유명사 대문자 시작 단어 / 표준 약어 / 경로·슬러그)

--fix 동작:
    text 노드(태그 밖)에서만 매핑 사전 영어 → 한글 치환 (긴 키 우선, 단어 경계).
    script/style 블록·태그 속성은 건드리지 않음. 치환 후 재검증 결과 출력.

종료 코드: 0 = PASS / 1 = FAIL (재출력·재호출 판단용)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_MD = ROOT / "reference/korean_translation_rules.md"

# v3.22 표준 약어 (룰 md 의 ABBR 목록과 동일 — 분모 제외 대상)
ABBR = (
    "ETF|PER|PBR|ROE|EPS|ATR|RSI|FCF|DCF|EBITDA|YoY|QoQ|MoM|WoW|GDP|CPI|PCE|FOMC|GPU|ASIC|"
    "TAM|SAM|NAV|AUM|TER|NIM|OPM|HBM|NAND|DRAM|CAPEX|PDF|SOTP|MACD|EBIT|ROIC|API|SaaS|IPO|"
    "BPS|VIX|NYSE|NASDAQ|WACC|FCFF|FCFE|Moat|MOAT|FX|TIPS|PMI|ISM|JOLTS|WTI|OPEC|EU|UN|NATO|"
    "ESG|AI|DC|SOX|HV\\d*|R:R|KST|UTC|HTML|KB|TP|NFP|DXY|BTC|ETH|SOL|USD|KRW|GM|D-\\d+|Q\\d"
)

EXTRA_KEYWORDS = ["approximately", "significantly", "Take Profit", "Stop Loss"]


def load_mapping() -> list:
    """korean_translation_rules.md 의 '## 매핑 사전' 표 파싱 → [(영어, 한글), ...] 긴 키 우선."""
    text = RULES_MD.read_text()
    m = re.search(r"## 매핑 사전.*?(?=\n## [^#])", text, re.DOTALL)
    if not m:
        sys.exit("[check_korean] FATAL: 매핑 사전 섹션 파싱 실패 — korean_translation_rules.md 확인")
    pairs = []
    for line in m.group(0).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] in ("영어", "") or set(cells[0]) <= {"-", " "}:
            continue
        ko = re.sub(r"\s*[(（].*$", "", cells[1]).strip()  # 괄호 주석 제거
        if not ko:
            continue
        for en in [k.strip() for k in cells[0].split(" / ")]:
            if en and re.search(r"[A-Za-z]", en):
                pairs.append((en, ko))
    if len(pairs) < 10:
        sys.exit(f"[check_korean] FATAL: 매핑 {len(pairs)}건만 파싱 — 표 형식 변경 의심")
    pairs.sort(key=lambda x: -len(x[0]))  # 긴 키 우선 (Strong Buy 가 Buy 보다 먼저)
    return pairs


def extract_body_text(html: str) -> str:
    """v3.22 파이프라인: body 추출 → script/style/style 속성/태그/엔티티 제거."""
    m = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
    body = m.group(1) if m else html
    body = re.sub(r"<script\b[^>]*>.*?</script>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<style\b[^>]*>.*?</style>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'\s+style="[^"]*"', "", body, flags=re.DOTALL)
    body = re.sub(r'\s+title="[^"]*"', "", body, flags=re.DOTALL)
    body = re.sub(r"<[^>]*>", "", body)
    body = re.sub(r"&[a-z]+;|&#\d+;", " ", body)
    return body


def find_violations(text: str, mapping: list) -> list:
    out = []
    for en, ko in mapping + [(k, "") for k in EXTRA_KEYWORDS]:
        if re.search(r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])", text):
            out.append(en)
    return out


def korean_ratio(text: str):
    """예외 제거 후 한글 문자 비중. (한글+라틴) 100자 미만이면 None (측정 불가 — 통과)."""
    t = re.sub(r"\S*/\S*", " ", text)  # 경로
    t = re.sub(r"\S+\.(md|html|json|py|mjs|sh|js|css)\b", " ", t, flags=re.IGNORECASE)
    t = re.sub(r"\b[a-z]+_[a-z_]+\b", " ", t, flags=re.IGNORECASE)  # 슬러그
    t = re.sub(r"\b(?:%s)\b" % ABBR, " ", t)  # 표준 약어
    t = re.sub(r"\b[A-Z][a-zA-Z]+\b", " ", t)  # 고유명사 (대문자 시작)
    k = len(re.findall(r"[가-힣]", t))
    total = k + len(re.findall(r"[A-Za-z]", t))
    if total <= 100:
        return None
    return k / total * 100


def fix_html(html: str, mapping: list):
    """text 노드에서만 매핑 치환. script/style 블록은 통째로 보존."""
    # script/style 블록 보호
    protected = []

    def protect(m):
        protected.append(m.group(0))
        return f"\x00P{len(protected) - 1}\x00"

    work = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", protect, html, flags=re.DOTALL | re.IGNORECASE)

    changed = 0

    def fix_text(m):
        nonlocal changed
        seg = m.group(0)
        for en, ko in mapping:
            seg2 = re.sub(r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])", ko, seg)
            if seg2 != seg:
                changed += 1
                seg = seg2
        return seg

    # 태그 사이 텍스트 (>...<) 만 치환
    work = re.sub(r"(?<=>)[^<>\x00]+(?=<)", fix_text, work)
    work = re.sub(r"\x00P(\d+)\x00", lambda m: protected[int(m.group(1))], work)
    return work, changed


def report(path: Path, mapping: list) -> bool:
    html = path.read_text(encoding="utf-8", errors="ignore")
    text = extract_body_text(html)
    vios = find_violations(text, mapping)
    ratio = korean_ratio(text)
    ok = not vios and (ratio is None or ratio >= 80)
    print(f"[check_korean] {path.name}")
    print(f"  매핑 잔류: {len(vios)}건" + (f" — {', '.join(vios[:12])}" if vios else ""))
    print(f"  한글 비중: {f'{ratio:.1f}%' if ratio is not None else '측정 불가 (표본 부족 — 통과)'} (기준 80%)")
    print(f"  결과: {'PASS' if ok else 'FAIL'}")
    return ok


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_fix = "--fix" in sys.argv
    if not args:
        sys.exit("사용: python3 scripts/check_korean.py [--fix] <리포트.html> [추가파일...]")

    mapping = load_mapping()
    all_ok = True
    for arg in args:
        path = Path(arg) if Path(arg).is_absolute() else ROOT / arg
        if not path.exists():
            print(f"[check_korean] 파일 없음: {arg}")
            all_ok = False
            continue
        if do_fix:
            html = path.read_text(encoding="utf-8", errors="ignore")
            fixed, changed = fix_html(html, mapping)
            if changed:
                path.write_text(fixed, encoding="utf-8")
                print(f"[check_korean] --fix: {path.name} 매핑 치환 {changed}개 세그먼트 적용")
            else:
                print(f"[check_korean] --fix: {path.name} 치환 대상 없음")
        if not report(path, mapping):
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
