#!/usr/bin/env python3
"""
scoreboard.py — 분석 유니버스 상대평가 (등급 쿼터제의 결정적 기반)

analysis/_history/*_timeline.json 의 종목별 최신 종합점수를 모아
주어진 점수의 백분위와 등급 쿼터 판정을 출력한다.

등급 쿼터 (v3.27, 2026-06-11):
    강력매수  = 유니버스 상위 5% 이내  (+ 변형 논지 보유 — 논지는 scorecard-strategist 가 판단)
    매수      = 상위 25% 이내
    중립      = 그 외
    매도 검토 = 하위 15%

사용:
    python3 scripts/scoreboard.py                     # 유니버스 분포만 출력
    python3 scripts/scoreboard.py 76                  # 76점의 백분위 + 쿼터 판정
    python3 scripts/scoreboard.py 76 --exclude NVDA   # 자기 종목 제외 (BLIND 재분석용 — 필수)

scorecard-strategist 가 등급 부여 직전에 호출 (Phase 3). 점수가 timeline 에 없으면
scorecard.md 의 "종합점수 N/100" 패턴 폴백 파싱으로 유니버스를 보강한다.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / "analysis/_history"

QUOTA = [
    (5, "강력매수 가능 (상위 5% 이내 — 단, 변형 논지 필수)"),
    (25, "매수 가능 (상위 25% 이내)"),
    (85, "중립 권장 (쿼터 미달 — 매수 등급 부여 금지)"),
    (100, "매도 검토 (하위 15%)"),
]

SCORE_RE = re.compile(r"종합\s*점수\D{0,8}(\d{1,3}(?:\.\d+)?)\s*/\s*100")


def universe(exclude: str | None) -> dict:
    scores = {}
    for f in HISTORY.glob("*_timeline.json"):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        ticker = d.get("ticker")
        if not ticker or (exclude and ticker.upper() == exclude.upper()):
            continue
        hist = d.get("history") or []
        if not hist:
            continue
        last = hist[-1]
        score = last.get("score")
        if score is None and last.get("scorecard_path"):
            sc = ROOT / last["scorecard_path"]
            if sc.exists():
                m = SCORE_RE.search(sc.read_text(errors="ignore"))
                if m:
                    score = float(m.group(1))
        if score is not None:
            scores[ticker] = float(score)
    return scores


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    exclude = None
    if "--exclude" in sys.argv:
        exclude = sys.argv[sys.argv.index("--exclude") + 1]

    scores = universe(exclude)
    vals = sorted(scores.values(), reverse=True)
    n = len(vals)
    if n < 10:
        print(f"[scoreboard] 유니버스 {n}종 — 10종 미만이라 상대평가 불가 (절대점수 등급 유지)")
        return

    import statistics

    p25 = vals[max(0, int(n * 0.25) - 1)]
    p5 = vals[max(0, int(n * 0.05) - 1)]
    p85 = vals[min(n - 1, int(n * 0.85) - 1)]
    print(f"[scoreboard] 유니버스 {n}종 (자기 종목 제외: {exclude or '없음'})")
    print(f"  평균 {statistics.mean(vals):.1f} / 중앙값 {statistics.median(vals):.1f}")
    print(f"  쿼터 경계: 강력매수 ≥ {p5:.1f} (상위 5%) / 매수 ≥ {p25:.1f} (상위 25%) / 매도 검토 ≤ {p85:.1f} (하위 15%)")

    if args:
        score = float(args[0])
        above = sum(1 for v in vals if v > score)
        pct = above / n * 100  # 상위 N%
        rank = above + 1
        if pct >= 85:
            v = QUOTA[3][1]
        elif pct > 25:
            v = QUOTA[2][1]
        elif pct > 5:
            v = QUOTA[1][1]
        else:
            v = QUOTA[0][1]
        print(f"  입력 {score}점 → 상위 {pct:.1f}% ({rank}/{n}위)")
        print(f"  쿼터 판정: {v}")


if __name__ == "__main__":
    main()
