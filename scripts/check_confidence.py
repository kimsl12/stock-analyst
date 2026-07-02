#!/usr/bin/env python3
"""
check_confidence.py — 확신 라벨 기계 게이트 (v3.36, 2026-07-02)

배경: auto_scoring 실측 — 확신 "높음" 적중 14.3%(2/14) < "중간" 60.0%(9/16).
강한 단정일수록 못 맞추는 역캘리브레이션 → 확신 높음 남발을 커밋 단계에서 기계 검사.
(게이트 없는 명세 의무는 안 지켜진다 — 이 시스템의 반복 교훈)

검사 대상: knowledge-db/performance/2026_recommendations.md 의 최근 N일(기본 30) 행
  R1. 확신에 "높음" 포함 행 → 근거(1줄)에 반증/조건 트리거 표현 필수
      (반증|트리거|분기점|폐기|무효|하회|상회|이탈|돌파|손절 중 1개 이상)
  R2. 순수 "높음" 비율 ≤ 25% (표본 4행 미만이면 스킵)
  R3. auto_scoring.json by_confidence 역전(높음 < 중간, 높음 n≥10) 상태면
      신규 "높음" 행 존재 자체를 경고 (체크리스트 4번 항목 위반 가능성)

종료 코드: FAIL 있으면 1 (briefing_commit.sh 가 비치명 처리 + 알림), 없으면 0.
사용:
    python3 scripts/check_confidence.py            # 기본 30일 창
    python3 scripts/check_confidence.py --days 14
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REC_MD = ROOT / "knowledge-db/performance/2026_recommendations.md"
SCORING = ROOT / "knowledge-db/performance/auto_scoring.json"

KST = timezone(timedelta(hours=9))

# 근거 컬럼에서 인정하는 반증/조건 트리거 표현
TRIGGER_RE = re.compile(r"반증|트리거|분기점|폐기|무효|하회|상회|이탈|돌파|손절")
HIGH_PURE_RE = re.compile(r"^높음$")


def parse_rows(days: int) -> list[dict]:
    if not REC_MD.exists():
        return []
    cutoff = (datetime.now(KST) - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = []
    for line in REC_MD.read_text().splitlines():
        if not line.startswith("| 20"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 8:
            continue
        date = cols[0]
        if not re.match(r"\d{4}-\d{2}-\d{2}", date) or date < cutoff:
            continue
        rows.append({"date": date, "target": cols[3][:40], "confidence": cols[6], "reason": cols[7]})
    return rows


def main() -> int:
    days = 30
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])

    rows = parse_rows(days)
    fails: list[str] = []
    warns: list[str] = []

    # R1 — 높음 계열 행의 반증 트리거 필수
    high_like = [r for r in rows if "높음" in r["confidence"]]
    for r in high_like:
        if not TRIGGER_RE.search(r["reason"]):
            fails.append(
                f"R1 {r['date']} [{r['target']}] 확신 '{r['confidence']}' 인데 근거에 반증/조건 트리거 없음"
            )

    # R2 — 순수 "높음" 비율 cap 25%
    if len(rows) >= 4:
        pure_high = [r for r in rows if HIGH_PURE_RE.match(r["confidence"])]
        ratio = len(pure_high) / len(rows) * 100
        if ratio > 25:
            fails.append(
                f"R2 최근 {days}일 확신 '높음' 비율 {ratio:.0f}% ({len(pure_high)}/{len(rows)}) — cap 25% 초과, 체크리스트 재적용 필요"
            )

    # R3 — 역캘리브레이션 지속 중 신규 높음 경고
    if SCORING.exists() and high_like:
        try:
            bc = json.loads(SCORING.read_text())["breakdown"]["by_confidence"]
            h, m = bc.get("높음", {}), bc.get("중간", {})
            if (
                h.get("n", 0) >= 10
                and h.get("hit_rate_pct") is not None
                and m.get("hit_rate_pct") is not None
                and h["hit_rate_pct"] < m["hit_rate_pct"]
            ):
                warns.append(
                    f"R3 역캘리브레이션 지속 (높음 {h['hit_rate_pct']}% < 중간 {m['hit_rate_pct']}%) 인데 "
                    f"최근 {days}일 높음 계열 {len(high_like)}행 — 산정 체크리스트 4번(과거 캘리브레이션) 점검"
                )
        except Exception:
            pass

    print(f"[check_confidence] 최근 {days}일 제안 {len(rows)}행 / 높음 계열 {len(high_like)}행")
    for w in warns:
        print(f"  ⚠️ {w}")
    for f in fails:
        print(f"  ❌ {f}")
    if not fails and not warns:
        print("  ✅ 통과 — 확신 라벨 규율 유지")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
