#!/usr/bin/env python3
"""
check_research_citation.py — 리서치 KB 인용 기계 게이트 (v3.40 ②)

규칙 (게이트 없는 의무는 안 지켜진다 — 2026-06-08 v3.23 실패 교훈):
  - analysis/{폴더}/research_context.md 가 **없으면** → 게이트 미적용 (PASS, 리서치 미배달)
  - 있으면 scorecard.md 는 둘 중 하나를 반드시 충족:
      (a) 📄 인용 1건 이상 (citation 라인 복사)
      (b) `research_skip_reason: <사유>` 명기 (미인용도 합법 — 단 사유가 데이터로 남아야 함)
  - 둘 다 없으면 FAIL (exit 1)

사용:
    python3 scripts/check_research_citation.py analysis/NVDA_NVIDIA_v6
    python3 scripts/check_research_citation.py --all-recent 7   # 최근 7일 스코어카드 일괄
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANALYSIS = ROOT / "analysis"


def check_dir(d: Path) -> tuple:
    """(status, message) — status: PASS | SKIP_OK | FAIL | NA"""
    ctx = d / "research_context.md"
    sc = d / "scorecard.md"
    if not ctx.exists():
        return ("NA", f"{d.name}: research_context.md 없음 — 게이트 미적용")
    if not sc.exists():
        return ("FAIL", f"{d.name}: research_context 존재하나 scorecard.md 없음")
    text = sc.read_text()
    n_cite = len(re.findall(r"📄\s*\[", text))
    if n_cite > 0:
        return ("PASS", f"{d.name}: 리서치 인용 {n_cite}건 ✅")
    m = re.search(r"research_skip_reason\s*[:：]\s*(.+)", text)
    if m:
        return ("SKIP_OK", f"{d.name}: 미인용 — 사유 명기 ✅ ({m.group(1).strip()[:60]})")
    return ("FAIL", f"{d.name}: ❌ research_context 배달됐는데 인용 0건 + skip_reason 없음 — citation 라인 복사 또는 research_skip_reason 명기 필요")


def main() -> int:
    if "--all-recent" in sys.argv:
        days = int(sys.argv[sys.argv.index("--all-recent") + 1])
        cutoff = time.time() - days * 86400
        dirs = [
            d for d in ANALYSIS.iterdir()
            if d.is_dir() and not d.name.startswith("_") and d.name != "briefing"
            and (d / "scorecard.md").exists() and (d / "scorecard.md").stat().st_mtime >= cutoff
        ]
    else:
        args = [a for a in sys.argv[1:] if not a.startswith("--")]
        if not args:
            print("사용법: check_research_citation.py {analysis/폴더} 또는 --all-recent {일수}")
            return 1
        p = Path(args[0])
        dirs = [p if p.is_absolute() else ROOT / p]

    fails = 0
    counts = {"PASS": 0, "SKIP_OK": 0, "FAIL": 0, "NA": 0}
    for d in sorted(dirs):
        status, msg = check_dir(d)
        counts[status] += 1
        if status == "FAIL":
            fails += 1
        print(f"[{status:7}] {msg}")
    if len(dirs) > 1:
        print(f"\n합계: 인용 {counts['PASS']} / 사유스킵 {counts['SKIP_OK']} / 실패 {counts['FAIL']} / 미적용 {counts['NA']}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
