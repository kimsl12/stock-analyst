#!/usr/bin/env python3
"""
regime_classifier.py — 일일 시장 레짐 결정적 분류 (LLM 불필요)

입력: yfinance (^GSPC 60d, ^VIX 30d, ^TNX 30d) + knowledge-base/market/fear_greed.json
출력: knowledge-base/market/regime.json + stdout 요약. 레짐 전환 시 notify.sh 알림.

분류 기준 (고정 — 해석의 출발점을 매일 동일하게):
    추세    : SPX 종가 vs 20일 이동평균 (±1% 밴드 안 = 횡보)
    변동성  : VIX < 15 저 / 15~25 중 / > 25 고
    금리    : 10Y 현재 vs 20일 전 (±10bp 밴드 안 = 중립)
    위험선호: 추세 + VIX + Fear&Greed 합성 → 리스크온 / 중립 / 리스크오프
    가중치장: scorecard-strategist 의 3벌 세트 매핑 → 상승장 / 하락장 / 횡보장

소비처:
    briefing-lead   — 모든 브리핑 헤더에 레짐 표기 의무 (lead 직접 Read 허용 파일)
    scorecard-strategist — 10항목 가중치 3벌 세트 선택 (재량 → 본 출력)
    watchdog        — 매일 06:40 실행, 전환 시 알림

사용:
    python3 scripts/regime_classifier.py            # 분류 + 저장 + 전환 시 알림
    python3 scripts/regime_classifier.py --dry-run  # 저장·알림 없이 stdout 만
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "knowledge-base/market/regime.json"
FG_JSON = ROOT / "knowledge-base/market/fear_greed.json"
HISTORY = ROOT / "scripts/launchd/.regime_history.json"
NOTIFY = ROOT / "scripts/notify.sh"

KST = timezone(timedelta(hours=9))
DRY_RUN = "--dry-run" in sys.argv


def fetch_series():
    import yfinance as yf

    out = {}
    for key, sym, period in [("SPX", "^GSPC", "3mo"), ("VIX", "^VIX", "2mo"), ("TNX", "^TNX", "2mo")]:
        h = yf.Ticker(sym).history(period=period)
        closes = h["Close"].dropna()
        if len(closes) < 21:
            raise RuntimeError(f"{sym} 데이터 부족 ({len(closes)}일)")
        out[key] = closes
    return out


def read_fg():
    try:
        d = json.loads(FG_JSON.read_text())
        # 형식 변형 대비: 본 시스템 표준 {cnn: {score: N}} 우선, 구형 변형 폴백
        for path in (("cnn", "score"), ("value",), ("score",), ("fgi", "now", "value"), ("now", "value")):
            cur = d
            ok = True
            for k in path:
                if isinstance(cur, dict) and k in cur:
                    cur = cur[k]
                else:
                    ok = False
                    break
            if ok and isinstance(cur, (int, float)):
                return float(cur)
    except Exception:
        pass
    return None


def classify() -> dict:
    s = fetch_series()
    spx, vix, tnx = s["SPX"], s["VIX"], s["TNX"]

    spx_last = float(spx.iloc[-1])
    ma20 = float(spx.tail(20).mean())
    dev = (spx_last / ma20 - 1) * 100
    trend = "상승" if dev > 1.0 else ("하락" if dev < -1.0 else "횡보")

    vix_last = float(vix.iloc[-1])
    vol = "저" if vix_last < 15 else ("중" if vix_last <= 25 else "고")
    vix_5d = float(vix.iloc[-1] - vix.iloc[-6]) if len(vix) >= 6 else 0.0

    # ^TNX 스케일 자동 감지: 환경에 따라 수익률×10 (45.4) 또는 % 그대로 (4.54) 반환
    tnx_scale = 10.0 if float(tnx.iloc[-1]) > 20 else 1.0
    y10_last = float(tnx.iloc[-1]) / tnx_scale
    y10_20d = float(tnx.iloc[-21]) / tnx_scale if len(tnx) >= 21 else y10_last
    y10_chg_bp = (y10_last - y10_20d) * 100
    rate = "상승" if y10_chg_bp > 10 else ("하락" if y10_chg_bp < -10 else "중립")

    fg = read_fg()

    # 위험선호 합성 (-3 ~ +3)
    score = 0
    score += {"상승": 1, "횡보": 0, "하락": -1}[trend]
    score += {"저": 1, "중": 0, "고": -1}[vol]
    if fg is not None:
        score += 1 if fg > 55 else (-1 if fg < 45 else 0)
    risk = "리스크온" if score >= 2 else ("리스크오프" if score <= -2 else "중립")

    # scorecard 가중치 3벌 매핑
    if trend == "상승" and risk != "리스크오프":
        weight_set = "상승장"
    elif trend == "하락" or risk == "리스크오프":
        weight_set = "하락장"
    else:
        weight_set = "횡보장"

    return {
        "date": datetime.now(KST).strftime("%Y-%m-%d"),
        "risk_regime": risk,
        "trend": trend,
        "spx_vs_ma20_pct": round(dev, 2),
        "vol_regime": vol,
        "vix": round(vix_last, 1),
        "vix_5d_change": round(vix_5d, 1),
        "rate_direction": rate,
        "us10y_pct": round(y10_last, 2),
        "us10y_20d_change_bp": round(y10_chg_bp, 0),
        "fear_greed": fg,
        "weight_set": weight_set,
    }


def main() -> None:
    r = classify()

    # 연속일·전환 감지
    hist = []
    if HISTORY.exists():
        try:
            hist = json.loads(HISTORY.read_text())
        except Exception:
            hist = []
    prev = hist[-1] if hist else None
    changed = bool(prev and prev.get("risk_regime") != r["risk_regime"])
    streak = 1
    for h in reversed(hist):
        if h.get("risk_regime") == r["risk_regime"]:
            streak += 1
        else:
            break
    if prev and prev.get("date") == r["date"]:
        streak = max(1, streak - 1)  # 같은 날 재실행은 연속일 미가산
    r["streak_days"] = streak
    r["changed_today"] = changed
    r["summary_ko"] = (
        f"{r['risk_regime']} {streak}일째 — 추세 {r['trend']}(MA20 {r['spx_vs_ma20_pct']:+.1f}%) · "
        f"VIX {r['vix']}({r['vol_regime']}) · 10Y {r['us10y_pct']}%({r['rate_direction']}) · "
        f"F&G {r['fear_greed'] if r['fear_greed'] is not None else '—'} → 가중치 {r['weight_set']}"
    )

    print(f"[regime] {r['summary_ko']}")
    if changed:
        print(f"[regime] 전환: {prev['risk_regime']} → {r['risk_regime']}")

    if not DRY_RUN:
        if not hist or hist[-1].get("date") != r["date"]:
            hist.append({"date": r["date"], "risk_regime": r["risk_regime"]})
        else:
            hist[-1]["risk_regime"] = r["risk_regime"]
        HISTORY.parent.mkdir(parents=True, exist_ok=True)
        HISTORY.write_text(json.dumps(hist[-90:], ensure_ascii=False, indent=1))

        # [v3.29] 레짐 스트립 HTML — 브리핑 헤더용 (generator 가 그대로 붙여넣기)
        color_map = {"리스크온": "var(--up)", "리스크오프": "var(--down)"}
        cells = "".join(
            '<span class="rg-cell" style="background:{}" title="{} {}"></span>'.format(
                color_map.get(h.get("risk_regime"), "var(--neutral)"), h.get("date"), h.get("risk_regime")
            )
            for h in hist[-30:]
        )
        r["strip_html"] = (
            '<div class="regime-strip">{}<span class="rg-label">레짐 최근 {}일</span></div>'.format(
                cells, min(len(hist), 30)
            )
        )

        OUT_JSON.write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n")
        print(f"[regime] 저장: {OUT_JSON.relative_to(ROOT)}")
        if changed:
            subprocess.run(
                ["bash", str(NOTIFY), "시장 레짐 전환", f"{prev['risk_regime']} → {r['risk_regime']} | {r['summary_ko']}", "high"],
                check=False,
            )


if __name__ == "__main__":
    main()
