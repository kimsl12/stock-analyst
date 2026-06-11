#!/usr/bin/env python3
"""
check_house_view.py — 하우스 뷰 명제의 기계 판정 가능 반증 조건 매일 평가

입력: knowledge-base/market/house_view.md 의 ```json fence (checks 배열)
        { id, metric, op, threshold, consecutive_days, meaning }
      metric: US10Y(^TNX/10) | WTI(CL=F) | GOLD(GC=F) | BTC(BTC-USD) | VIX(^VIX) | SP500(^GSPC) | FG
출력: 조건 도달 시 notify.sh 알림 (KST 일별 디듀프 — portfolio_watch 와 상태 파일 공유)
      + stdout 전체 평가표

도달 의미: 해당 명제는 다음 브리핑에서 "반증됨" 처리 + 개정 로그 작성 의무 (house_view.md 권한 매트릭스).

사용:
    python3 scripts/check_house_view.py            # 평가 + 알림
    python3 scripts/check_house_view.py --dry-run  # 알림·상태 기록 없이 평가만
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HV_MD = ROOT / "knowledge-base/market/house_view.md"
FG_JSON = ROOT / "knowledge-base/market/fear_greed.json"
STATE_JSON = ROOT / "scripts/launchd/.watch_state.json"
NOTIFY = ROOT / "scripts/notify.sh"

KST = timezone(timedelta(hours=9))
DRY_RUN = "--dry-run" in sys.argv

SYMBOLS = {"US10Y": "^TNX", "WTI": "CL=F", "GOLD": "GC=F", "BTC": "BTC-USD", "VIX": "^VIX", "SP500": "^GSPC"}
OPS = {"<": lambda a, b: a < b, ">": lambda a, b: a > b, "<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b}


def load_checks() -> list:
    text = HV_MD.read_text()
    m = re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    if not m:
        print("[house_view] 기계 검사 JSON fence 없음 — 종료")
        sys.exit(0)
    return json.loads(m.group(1)).get("checks", [])


def closes_for(metric: str, days: int):
    """최근 종가 시리즈 (오름차순 날짜). FG 는 단일값 리스트."""
    if metric == "FG":
        try:
            d = json.loads(FG_JSON.read_text())
            v = d.get("value") or d.get("score")
            return [float(v)] if v is not None else []
        except Exception:
            return []
    import yfinance as yf

    sym = SYMBOLS.get(metric)
    if not sym:
        return []
    h = yf.Ticker(sym).history(period=f"{max(days + 7, 12)}d")
    vals = [float(x) for x in h["Close"].dropna().tolist()]
    if metric == "US10Y" and vals and vals[-1] > 20:
        vals = [v / 10.0 for v in vals]  # ^TNX 가 수익률×10 스케일로 반환되는 환경만 보정
    return vals


def main() -> None:
    checks = load_checks()
    if not checks:
        print("[house_view] 등록된 기계 검사 없음")
        return

    state = {}
    if STATE_JSON.exists():
        try:
            state = json.loads(STATE_JSON.read_text())
        except Exception:
            state = {}
    today = datetime.now(KST).strftime("%Y-%m-%d")

    print(f"[house_view] 반증 조건 평가 — {today} ({len(checks)}건)")
    triggered = []
    for c in checks:
        n = int(c.get("consecutive_days", 1))
        vals = closes_for(c["metric"], n)
        if len(vals) < n:
            print(f"  {c['id']:4} {c['metric']:6} 데이터 부족 — 스킵")
            continue
        op = OPS[c["op"]]
        thr = float(c["threshold"])
        window = vals[-n:]
        hit = all(op(v, thr) for v in window)
        cur = window[-1]
        mark = "도달" if hit else "미달"
        print(f"  {c['id']:4} {c['metric']:6} 현재 {cur:,.2f} {c['op']} {thr:,.2f} (연속 {n}일) → {mark}")
        if hit:
            triggered.append(c)
            key = f"hv:{c['id']}"
            if state.get(key) == today:
                print(f"       (디듀프) {c['id']} 오늘 이미 알림")
                continue
            state[key] = today
            if not DRY_RUN:
                subprocess.run(
                    ["bash", str(NOTIFY), f"하우스 뷰 반증 조건 도달: {c['id']}",
                     f"{c['meaning']} (현재 {cur:,.2f}) — 다음 브리핑에서 명제 개정 의무", "high"],
                    check=False,
                )
            print(f"       [알림] {c['meaning']}")

    if not DRY_RUN:
        STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
        STATE_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    print(f"[house_view] 완료 — 도달 {len(triggered)}건")


if __name__ == "__main__":
    main()
