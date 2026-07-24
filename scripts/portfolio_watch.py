#!/usr/bin/env python3
"""
portfolio_watch.py — 보유 종목 감시 (손절/목표가 도달 + 리밸런싱 드리프트)

입력:
    web/src/data/holdings_health.json   (build_holdings_health.mjs 산출물 — 수량·손절·목표가)
    scripts/portfolio_targets.json      (티커별 목표 비중 — 사용자 편집 파일)
    yfinance 실시간(지연) 종가          (배치 1회 조회)

알림 (scripts/notify.sh 경유 — macOS 알림센터):
    [high]    현재가 ≤ 손절가          → "손절선 도달"
    [default] 현재가 ≥ 목표가          → "목표가 도달"
    [default] 현재가 ≤ 손절가 × 1.02   → "손절선 2% 이내 접근"
    [default] |실제 비중 − 목표 비중| > 임계(기본 5%p) → "리밸런싱 드리프트"

디듀프: scripts/launchd/.watch_state.json — 같은 알림 키는 KST 기준 하루 1회.

사용:
    python3 scripts/portfolio_watch.py            # 감시 + 알림
    python3 scripts/portfolio_watch.py --dry-run  # 알림 없이 stdout 만

launchd: scripts/automation_watchdog.sh 가 매일 호출.
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEALTH_JSON = ROOT / "web/src/data/holdings_health.json"
TARGETS_JSON = ROOT / "scripts/portfolio_targets.json"
STATE_JSON = ROOT / "scripts/launchd/.watch_state.json"
NOTIFY = ROOT / "scripts/notify.sh"

KST = timezone(timedelta(hours=9))
DRY_RUN = "--dry-run" in sys.argv


def today_kst() -> str:
    return datetime.now(KST).strftime("%Y-%m-%d")


def load_state() -> dict:
    if STATE_JSON.exists():
        try:
            return json.loads(STATE_JSON.read_text())
        except Exception:
            return {}
    return {}


def save_state(state: dict) -> None:
    STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATE_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def notify(title: str, body: str, priority: str = "default", *, state: dict, key: str) -> None:
    """하루 1회 디듀프 후 notify.sh 호출."""
    if state.get(key) == today_kst():
        print(f"  (디듀프) {title}: {body}")
        return
    state[key] = today_kst()
    print(f"  [알림:{priority}] {title}: {body}")
    if not DRY_RUN:
        subprocess.run(["bash", str(NOTIFY), title, body, priority], check=False)


def fetch_prices(tickers: list) -> dict:
    """yfinance 배치 조회 — {ticker: 최근 종가}. 실패 티커는 누락."""
    import yfinance as yf

    out = {}
    data = yf.download(tickers, period="5d", progress=False, group_by="ticker", threads=True)
    for t in tickers:
        try:
            closes = data[t]["Close"].dropna() if len(tickers) > 1 else data["Close"].dropna()
            if len(closes):
                out[t] = round(float(closes.iloc[-1]), 2)
        except Exception:
            pass
    return out


def main() -> None:
    if not HEALTH_JSON.exists():
        print("[watch] holdings_health.json 없음 — build_holdings_health.mjs 먼저 실행")
        sys.exit(1)

    health = json.loads(HEALTH_JSON.read_text())
    holdings = health.get("holdings", [])
    tickers = [h["ticker"] for h in holdings if h.get("qty")]
    if not tickers:
        print("[watch] 보유 종목 없음")
        return

    prices = fetch_prices(tickers)
    missing = [t for t in tickers if t not in prices]
    if missing:
        print(f"[watch] 가격 조회 실패 (스킵): {', '.join(missing)}")

    state = load_state()

    # ── 1. 손절/목표가 도달 ──────────────────────────────
    print(f"[watch] 손절/목표가 점검 — {today_kst()}")
    for h in holdings:
        t = h["ticker"]
        a = h.get("analysis") or {}
        price = prices.get(t)
        if price is None:
            continue
        stop, target = a.get("stop_loss"), a.get("target_price")
        line = f"{t:5} ${price}"
        if stop:
            line += f" | 손절 ${stop}"
        if target:
            line += f" | 목표 ${target}"
        print(f"  {line}")

        if stop and price <= stop:
            notify(
                f"손절선 도달: {t}",
                f"현재 ${price} ≤ 손절 ${stop} (분석 v{a.get('v')}, {a.get('date')})",
                "high",
                state=state,
                key=f"stop_hit:{t}",
            )
        elif stop and price <= stop * 1.02:
            notify(
                f"손절선 접근: {t}",
                f"현재 ${price} — 손절 ${stop} 대비 {((price / stop) - 1) * 100:+.1f}%",
                "default",
                state=state,
                key=f"stop_near:{t}",
            )
        if target and price >= target:
            notify(
                f"목표가 도달: {t}",
                f"현재 ${price} ≥ 목표 ${target} (분석 v{a.get('v')}, {a.get('date')})",
                "default",
                state=state,
                key=f"target_hit:{t}",
            )

    # ── 2. 리밸런싱 드리프트 ─────────────────────────────
    if TARGETS_JSON.exists():
        cfg = json.loads(TARGETS_JSON.read_text())
        targets = cfg.get("targets", {})
        threshold = float(cfg.get("threshold_pct_point", 5))
        values = {
            h["ticker"]: h["qty"] * prices[h["ticker"]]
            for h in holdings
            if h.get("qty") and h["ticker"] in prices
        }
        total = sum(values.values())
        if total > 0 and targets:
            print(f"[watch] 드리프트 점검 (임계 {threshold}%p, 주식 보유분 정규화 기준)")
            drifted = []
            for t, v in sorted(values.items(), key=lambda x: -x[1]):
                actual = v / total * 100
                tgt = targets.get(t)
                if tgt is None:
                    continue
                drift = actual - float(tgt)
                print(f"  {t:5} 실제 {actual:5.1f}% / 목표 {tgt:5.1f}% / 괴리 {drift:+5.1f}%p")
                if abs(drift) > threshold:
                    drifted.append(f"{t} {drift:+.1f}%p (실제 {actual:.1f}%)")
            if drifted:
                notify(
                    "리밸런싱 드리프트",
                    f"목표 비중 이탈 {len(drifted)}종: " + " · ".join(drifted),
                    "default",
                    state=state,
                    key="drift:" + ",".join(sorted(d.split()[0] for d in drifted)),
                )
    else:
        print("[watch] portfolio_targets.json 없음 — 드리프트 점검 스킵")

    if not DRY_RUN:
        save_state(state)  # dry-run 은 디듀프 상태 미기록 (실알림 차단 방지)
    print("[watch] 완료")


if __name__ == "__main__":
    main()
