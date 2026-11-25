# -*- coding: utf-8 -*-
"""
check_data_blackout.py — '데이터 블랙아웃' 전제 게이트 (2026-11-25)

배경: "미 정부 셧다운으로 9·10월 고용·물가 지표 미발표(데이터 블랙아웃)" 전제가 KB·브리핑에
수 주간 승계됐으나, FRED 스냅샷에는 해당 월 관측이 이미 들어 있었다
(analysis/_audit/briefing_audit.md §2-1). 지표 발표 여부는 fred_snapshot.json 관측일로 판정한다.

동작: FRED 핵심 계열(UNRATE·PAYEMS·CPIAUCSL·PCEPILFE)의 최신 관측월이 정상 발표 주기에 맞는데
      대상 파일에 미발표·블랙아웃·셧다운발 지연을 현재 사실로 쓴 줄이 있으면 WARN
      (건수 + 최대 5줄 인용 + 계열별 관측일).
제외: '정정'·'폐기'·'[미검증' 이 든 줄, 그리고 `blackout-check: ignore` ~ `blackout-check: end`
      사이의 줄 (마크다운은 `<!-- blackout-check: ignore -->`, YAML frontmatter 는 `# blackout-check: ignore`).
      연준 위원 발언 금지 기간('FOMC 블랙아웃')·전력 블랙아웃은 다른 뜻이라 세지 않는다.

종료 코드: 기본 0 (경고만 — 자동화에 차단 게이트를 끼우지 않는다). --strict 면 경고 시 2.
사용:
    python3 scripts/check_data_blackout.py <파일...>
    python3 scripts/check_data_blackout.py --strict analysis/briefing/lead_evening_20261124.md
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

SNAPSHOT = Path(__file__).resolve().parent.parent / "knowledge-base/macro/fred_snapshot.json"

# 계열별 정상 발표 주기: (기준일, 시차 개월). 매월 기준일 이후면 "시차"개월 전 관측이, 이전이면 그보다
# 한 달 더 전 관측이 FRED 에 있어야 정상 (고용 = 익월 첫 금요일, CPI = 익월 10~15일, PCE = 익월 말).
# 월 1일 관측 기준 경과일로는 고용 ~70일·CPI ~75일·PCE ~95일 이내에 해당한다.
# 실제로 발표가 밀리면(진짜 블랙아웃) 이 기준에 못 미쳐 게이트가 판정을 보류한다.
RELEASE = {"UNRATE": (10, 1), "PAYEMS": (10, 1), "CPIAUCSL": (16, 1), "PCEPILFE": (5, 2)}

EXEMPT = ("정정", "폐기", "[미검증")
IGNORE_ON, IGNORE_OFF = "blackout-check: ignore", "blackout-check: end"
MAX_QUOTES = 5

# 데이터 블랙아웃이 아닌 '블랙아웃' — 연준 발언 금지 기간, 전력 블랙아웃
OTHER_SENSE = re.compile(
    r"(?:FOMC|Fed|연준)(?:(?!셧다운|데이터|지표)[^|\n]){0,30}?블랙아웃"
    r"|(?<!셧다운 )(?<!데이터 )블랙아웃\s*(?:기간|~?\s*\d{1,2}/\d{1,2}\s*개시)"
    r"|(?:전력|전력망|정전)[^|\n]{0,6}?블랙아웃"
)
# 셧다운 주장: 지속 일수(N일째·D+N)·미발표, 또는 지표·데이터 발표가 밀렸다는 서술.
# "셧다운 → 조달 집행 지연" 같은 일반 지연·가정 시나리오는 데이터 주장이 아니라 세지 않는다.
SHUT = r"셧다운(?!\s*(?:회피|리스크|우려|가능성|시한|데드라인|무관))"
CLAIM = re.compile(
    r"블랙아웃"
    rf"|{SHUT}[^|\n]{{0,30}}?(?:미발표|깜깜이|일째|D\+\d)"
    rf"|{SHUT}[^|\n]{{0,30}}?(?:지표|데이터|발표|통계|보고서|BLS|BEA|EIA)[^|\n]{{0,12}}?(?:지연|연기|중단|공백|부재)"
    r"|미발표[^|\n]{0,10}?셧다운"
)
# "9·10월 CPI/NFP 미발표" 처럼 특정 월 지표가 안 나왔다는 주장 → 그 월 관측이 FRED 에 있으면 모순
MONTH_CLAIM = re.compile(r"(?<![\d/.])(\d{1,2})(?:[·,~](\d{1,2}))?월((?:(?!\d월)[^\n]){0,30}?)미발표")
INDICATOR = re.compile(r"CPI|PCE|NFP|BLS|고용|실업률|물가|지표")
# FRED 계열은 미국 지표만 판정 가능 — 다른 나라 지표·한국 통계명이 앞에 있으면 월 주장 판정에서 뺀다
NON_US = re.compile(r"한국|국내|통계청|한은|금통위|관세청|고용동향|산업활동|코스피|중국|일본|유로|독일|영국")


def month_back(today, months):
    y, m = today.year, today.month - months
    if m <= 0:
        y, m = y - 1, m + 12
    return date(y, m, 1)


def load_observed():
    """핵심 계열의 최신 관측일 {id: date}. 스냅샷이 없거나 계열이 빠지면 None."""
    try:
        series = json.loads(SNAPSHOT.read_text(encoding="utf-8"))["series"]
        found = {s["id"]: date.fromisoformat(s["date"]) for s in series if s.get("id") in RELEASE}
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return {k: found[k] for k in RELEASE} if len(found) == len(RELEASE) else None


def is_publishing_normally(observed, today):
    for sid, (day, lag) in RELEASE.items():
        if observed[sid] < month_back(today, lag if today.day >= day else lag + 1):
            return False
    return True


def month_claim_hit(text, observed, today):
    """'N월 … 미발표' 가 FRED 에 이미 있는 월을 가리키면 그 매치를 돌려준다."""
    for m in MONTH_CLAIM.finditer(text):
        ctx = m.group(3)
        if not INDICATOR.search(ctx) or NON_US.search(text[max(0, m.start() - 40):m.end()]):
            continue
        only_pce = "PCE" in ctx and not re.search(r"CPI|NFP|BLS|고용|실업률", ctx)
        obs = observed["PCEPILFE"] if only_pce else min(observed[k] for k in ("UNRATE", "PAYEMS", "CPIAUCSL"))
        for g in (m.group(1), m.group(2)):
            if g and 1 <= int(g) <= 12:
                mm = int(g)
                ref = date(today.year if mm <= today.month else today.year - 1, mm, 1)
                if ref <= obs:
                    return m
    return None


def scan(path, observed, today):
    """파일에서 블랙아웃 주장 줄 [(줄번호, 인용)] 을 찾는다."""
    hits, ignoring = [], False
    for no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if IGNORE_ON in line:
            ignoring = True
            continue
        if IGNORE_OFF in line:
            ignoring = False
            continue
        if ignoring or any(k in line for k in EXEMPT):
            continue
        text = OTHER_SENSE.sub("", line)
        m = CLAIM.search(text) or month_claim_hit(text, observed, today)
        if m:
            a, b = max(0, m.start() - 40), min(len(text), m.end() + 60)
            hits.append((no, ("…" if a else "") + text[a:b].strip() + ("…" if b < len(text) else "")))
    return hits


def main():
    ap = argparse.ArgumentParser(description="FRED 는 발표가 이어지는데 '미발표·블랙아웃'을 쓴 줄을 경고")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--strict", action="store_true", help="경고가 있으면 exit 2")
    args = ap.parse_args()

    today = date.today()
    observed = load_observed()
    if observed is None:
        print("[blackout-check] 건너뜀 — fred_snapshot.json 을 읽지 못했거나 핵심 계열 누락")
        return 0
    obs_txt = " · ".join(f"{k} {v.isoformat()}" for k, v in observed.items())
    if not is_publishing_normally(observed, today):
        print(f"[blackout-check] 판정 보류 — FRED 핵심 계열이 정상 발표 주기보다 늦음(실제 지연 가능): {obs_txt}")
        return 0

    results = []
    for f in args.files:
        p = Path(f)
        if p.is_file():  # 없는 파일은 건너뜀 (브리핑 종류에 따라 lead/HTML 한쪽만 있을 수 있음)
            hits = scan(p, observed, today)
            if hits:
                results.append((f, hits))

    total = sum(len(h) for _, h in results)
    if total == 0:
        print(f"[blackout-check] OK — 미발표·블랙아웃 주장 0줄 (FRED 관측: {obs_txt})")
        return 0

    print(f"[blackout-check] WARN — FRED 는 지표 발표가 이어지는데 미발표·블랙아웃·셧다운발 지연 주장 {total}줄")
    print(f"  FRED 최신 관측: {obs_txt}")
    quoted = 0
    for f, hits in results:
        print(f"  {f}: {len(hits)}줄")
        for no, quote in hits:
            if quoted < MAX_QUOTES:
                print(f"    L{no}: {quote}")
                quoted += 1
    if total > quoted:
        print(f"    (외 {total - quoted}줄 생략)")
    print("  → 발표 여부는 fred_snapshot.json 관측일로 판정. 과거 이력이면 '정정'·'폐기' 표기 또는 blackout-check: ignore 블록 처리.")
    return 2 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
