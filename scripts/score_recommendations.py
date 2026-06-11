#!/usr/bin/env python3
"""
score_recommendations.py — 추천 성과 자동 채점 (결정적 스크립트, LLM 불필요)

입력:  knowledge-db/performance/2026_recommendations.md (append-only 추천 기록)
출력:  knowledge-db/performance/auto_scoring.json  (+ 요약 md fence 콘솔 출력)

동작:
  1. 추천 표 파싱 (제안일 | 모듈 | 카테고리 | 대상 | 방향 | 시간축 | 확신 | ... | status)
  2. 카테고리 종목/ETF/토큰 행에서 티커 추출 (대상 컬럼 선두 토큰 또는 괄호 안)
  3. yfinance 배치 조회 — 제안일 종가(기준가) + 최신 종가
  4. 방향 부호 반영 수익률 (Bull=+, Bear=−, 중립=절대값 추적만)
  5. 분류 (참고 지표 — 최종 해석은 /성과리뷰 에이전트):
       signed_return ≥ +3%  → hit
       signed_return ≤ −3%  → miss
       그 외               → flat
     단, 시간축 최소 경과 미달 시 "early" (단기 30일 / 중기 90일 / 장기 180일)

사용:
    python3 scripts/score_recommendations.py            # 채점 + json 저장
    python3 scripts/score_recommendations.py --dry-run  # 저장 없이 요약만

소비처: /성과리뷰 Step 0, /주간리포트 C-9 — 본 json 을 먼저 읽고 해석에 집중.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REC_MD = ROOT / "knowledge-db/performance/2026_recommendations.md"
OUT_JSON = ROOT / "knowledge-db/performance/auto_scoring.json"

KST = timezone(timedelta(hours=9))
DRY_RUN = "--dry-run" in sys.argv

HIT_THRESHOLD = 3.0  # ±3%
MIN_DAYS = {"단기": 30, "중기": 90, "장기": 180}

# 토큰 → yfinance 심볼
TOKEN_MAP = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "XRP": "XRP-USD"}


def extract_ticker(target: str, category: str) -> str | None:
    """대상 컬럼에서 티커 추출. 실패 시 None (= 측정 불가)."""
    target = target.strip()
    # 1. 선두 토큰이 티커 형태 (미국 1~5자 대문자 / 한국 6자리)
    m = re.match(r"^([A-Z]{1,5}|\d{6})(?:\s|$|\b)", target)
    cand = None
    if m:
        cand = m.group(1)
    else:
        # 2. 괄호 안 단일 티커 "(GLD/IAU)" → 첫 항목
        m2 = re.search(r"\(([A-Z]{1,5}(?:/[A-Z]{1,5})*)\)", target)
        if m2:
            cand = m2.group(1).split("/")[0]
    if not cand:
        return None
    if category == "토큰":
        return TOKEN_MAP.get(cand)
    if cand.isdigit():
        return f"{cand}.KS"  # 한국 종목 — KOSPI 우선 (KQ 미스는 측정 불가 처리)
    return cand


def parse_rows() -> list:
    rows = []
    for line in REC_MD.read_text().splitlines():
        if not re.match(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|", line):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 10:
            continue
        date, module, category, target, direction, horizon, confidence = cols[0:7]
        status = cols[9]
        rows.append(
            {
                "date": date,
                "module": module,
                "category": category,
                "target": target,
                "direction": direction,
                "horizon": horizon,
                "confidence": confidence,
                "status": status,
            }
        )
    return rows


def direction_sign(direction: str):
    d = direction.strip()
    if d.startswith("Bull"):
        return 1
    if d.startswith("Bear"):
        return -1
    return 0  # 중립 등


def main() -> None:
    rows = parse_rows()
    priceable = []
    for r in rows:
        if r["category"] not in ("종목", "ETF", "토큰"):
            r["skip_reason"] = "비가격 카테고리 (자산군/시나리오/이벤트)"
            continue
        t = extract_ticker(r["target"], r["category"])
        if not t:
            r["skip_reason"] = "티커 추출 실패"
            continue
        r["yf_ticker"] = t
        priceable.append(r)

    tickers = sorted({r["yf_ticker"] for r in priceable})
    min_date = min((r["date"] for r in priceable), default=None)
    print(f"[scoring] 전체 {len(rows)}행 / 가격 측정 대상 {len(priceable)}행 / 티커 {len(tickers)}종")

    closes = {}
    if tickers and min_date:
        import yfinance as yf

        start = (datetime.strptime(min_date, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
        data = yf.download(tickers, start=start, progress=False, group_by="ticker", threads=True)
        for t in tickers:
            try:
                s = data[t]["Close"].dropna() if len(tickers) > 1 else data["Close"].dropna()
                if len(s):
                    closes[t] = s
            except Exception:
                pass

    today = datetime.now(KST).date()
    results = []
    for r in priceable:
        s = closes.get(r["yf_ticker"])
        if s is None or not len(s):
            r["skip_reason"] = "가격 데이터 없음"
            continue
        # 제안일 이후 첫 거래일 종가 = 기준가
        rec_date = r["date"]
        base = s[s.index >= rec_date]
        if not len(base):
            r["skip_reason"] = "제안일 이후 거래일 없음"
            continue
        base_price = float(base.iloc[0])
        cur_price = float(s.iloc[-1])
        raw_ret = (cur_price / base_price - 1) * 100
        sign = direction_sign(r["direction"])
        signed = raw_ret * sign if sign != 0 else None

        elapsed = (today - datetime.strptime(rec_date, "%Y-%m-%d").date()).days
        min_days = MIN_DAYS.get(r["horizon"], 30)
        if sign == 0:
            verdict = "untracked(중립)"
        elif elapsed < min_days:
            verdict = "early"
        elif signed >= HIT_THRESHOLD:
            verdict = "hit"
        elif signed <= -HIT_THRESHOLD:
            verdict = "miss"
        else:
            verdict = "flat"

        results.append(
            {
                **{k: r[k] for k in ("date", "module", "category", "target", "direction", "horizon", "confidence", "status")},
                "ticker": r["yf_ticker"],
                "base_price": round(base_price, 2),
                "current_price": round(cur_price, 2),
                "raw_return_pct": round(raw_ret, 2),
                "signed_return_pct": round(signed, 2) if signed is not None else None,
                "elapsed_days": elapsed,
                "verdict": verdict,
            }
        )

    classified = [x for x in results if x["verdict"] in ("hit", "miss", "flat")]
    hits = sum(1 for x in classified if x["verdict"] == "hit")
    misses = sum(1 for x in classified if x["verdict"] == "miss")

    payload = {
        "generated_at": datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "doc": "결정적 자동 채점 — 기준가=제안일 이후 첫 거래일 종가, 임계 ±3%, 시간축 최소 경과(30/90/180일) 미달은 early. 해석·교훈 도출은 /성과리뷰 에이전트 책임.",
        "total_rows": len(rows),
        "priced_rows": len(results),
        "skipped_rows": len(rows) - len(results),
        "summary": {
            "hit": hits,
            "miss": misses,
            "flat": sum(1 for x in classified if x["verdict"] == "flat"),
            "early": sum(1 for x in results if x["verdict"] == "early"),
            "hit_rate_pct": round(hits / (hits + misses) * 100, 1) if (hits + misses) else None,
        },
        "results": results,
    }

    if not DRY_RUN:
        OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        print(f"[scoring] 저장: {OUT_JSON.relative_to(ROOT)}")

    sm = payload["summary"]
    print(
        f"[scoring] 판정 가능 {hits + misses + sm['flat']}건 — hit {hits} / miss {misses} / flat {sm['flat']}"
        f" / early {sm['early']} | 적중률 {sm['hit_rate_pct']}%"
    )


if __name__ == "__main__":
    main()
