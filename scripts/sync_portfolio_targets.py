#!/usr/bin/env python3
"""
sync_portfolio_targets.py — /내포트폴리오 처방 → portfolio_targets.json 자동 동기화 (v3.37)

배경: 처방(lead_user_portfolio_*.md)은 사람이 읽는 액션("SGOV +5주")으로만 말하고
기계가 읽는 목표 비중이 없어, 드리프트 감시(portfolio_watch)·웹 표시가 처방과 단절돼 있었다.
(실사고: 6/27 처방이 알고 엔진이 이미 청산한 SGOV·QUAL 추가 매수를 권고 — 처방↔현실↔감시 3중 단절)

동작:
  1. analysis/briefing/lead_user_portfolio_*.md 최신 파일에서 "## 목표 비중" 표 파싱
     | 티커 | 목표 비중(%) | 근거 |  (briefing-lead §/내포트폴리오 Phase 3 의무 블록)
  2. 검증: 티커 형식 / 3종 이상 / 합계 95~105
  3. scripts/portfolio_targets.json 갱신 (threshold 유지 + provenance 기록)
  → 이후 watchdog 드리프트 알림 + /portfolio "목표 vs 실제" 표시가 처방 기준을 자동 추종

블록이 없으면 no-op (구형 산출물 호환 — 기존 targets 유지).

사용:
    python3 scripts/sync_portfolio_targets.py             # 최신 lead 자동 탐색
    python3 scripts/sync_portfolio_targets.py --dry-run
    python3 scripts/sync_portfolio_targets.py --file {md} # 특정 파일 (테스트)
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEAD_DIR = ROOT / "analysis/briefing"
TARGETS_JSON = ROOT / "scripts/portfolio_targets.json"

KST = timezone(timedelta(hours=9))
TICKER_RE = re.compile(r"^[A-Z0-9]{1,6}(\.[A-Z]{1,2})?$")


def find_latest_lead() -> Path | None:
    files = sorted(LEAD_DIR.glob("lead_user_portfolio_*.md"))
    return files[-1] if files else None


def parse_targets_block(md: str) -> dict[str, float] | None:
    """'## 목표 비중' 섹션의 표 → {티커: 비중}. 섹션 없으면 None."""
    m = re.search(r"^##+\s*(?:\d+\.\s*)?목표\s*비중[\s\S]+?(?=^## |\Z)", md, re.M)
    if not m:
        return None
    targets: dict[str, float] = {}
    for line in m.group(0).splitlines():
        row = re.match(r"^\|\s*\*?\*?([A-Z0-9.]{1,9})\*?\*?\s*\|\s*\*?\*?([\d.]+)\s*%?\*?\*?\s*\|", line)
        if not row:
            continue
        ticker, pct = row.group(1), float(row.group(2))
        if TICKER_RE.match(ticker) and 0 < pct <= 100:
            targets[ticker] = pct
    return targets or None


def main() -> int:
    dry = "--dry-run" in sys.argv
    src = Path(sys.argv[sys.argv.index("--file") + 1]) if "--file" in sys.argv else find_latest_lead()
    if not src or not src.exists():
        print("[sync_targets] lead_user_portfolio_*.md 없음 — 기존 targets 유지")
        return 0

    targets = parse_targets_block(src.read_text())
    if targets is None:
        print(f"[sync_targets] {src.name} 에 '## 목표 비중' 블록 없음 — 기존 targets 유지 (구형 산출물)")
        return 0

    # 검증
    total = sum(targets.values())
    if len(targets) < 3:
        print(f"[sync_targets] ❌ 티커 {len(targets)}종 (<3) — 동기화 거부, 기존 유지")
        return 1
    if not (95 <= total <= 105):
        print(f"[sync_targets] ❌ 합계 {total:.1f}% (95~105 이탈) — 동기화 거부, 기존 유지")
        return 1

    prev = json.loads(TARGETS_JSON.read_text()) if TARGETS_JSON.exists() else {}
    out = {
        "_doc": "리밸런싱 드리프트 감시 목표 비중 (%). 토스 주식 보유분만 정규화 (현금·ISA·크립토 제외). /내포트폴리오 처방의 '## 목표 비중' 블록에서 sync_portfolio_targets.py 가 자동 동기화 — 수동 편집분은 다음 처방 실행 시 덮어써짐.",
        "threshold_pct_point": prev.get("threshold_pct_point", 5),
        "seeded_at": datetime.now(KST).strftime("%Y-%m-%d"),
        "source": src.name,
        "targets": dict(sorted(targets.items(), key=lambda kv: -kv[1])),
    }

    diff = {
        t: (prev.get("targets", {}).get(t), v)
        for t, v in targets.items()
        if prev.get("targets", {}).get(t) != v
    }
    removed = [t for t in prev.get("targets", {}) if t not in targets]
    print(f"[sync_targets] {src.name} → {len(targets)}종 합계 {total:.1f}%")
    for t, (old, new) in diff.items():
        print(f"  {t}: {old if old is not None else '신규'} → {new}")
    for t in removed:
        print(f"  {t}: 제거 (감시 제외)")

    if dry:
        print("[sync_targets] --dry-run — 저장 안 함")
        return 0
    TARGETS_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"[sync_targets] 저장 완료 → {TARGETS_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
