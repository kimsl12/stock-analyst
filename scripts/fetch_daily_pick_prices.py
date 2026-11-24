# -*- coding: utf-8 -*-
"""데일리픽 성적표용 가격 캐시 수집기.

원장(web/src/data/daily_pick_ledger.json)의 티커 + 벤치마크(^GSPC, ^KS11)의
일봉(시가/고가/종가)을 yfinance 로 받아 analysis/_daily_pick/prices.json 에 저장한다.
키는 원장 ticker (벤치마크는 심볼 그대로). 날짜는 거래소 현지 날짜.
벤치마크 2개 중 하나라도 없으면 exit 1.
"""
import json
import math
import os
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import yfinance as yf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "web", "src", "data", "daily_pick_ledger.json")
OUT_DIR = os.path.join(ROOT, "analysis", "_daily_pick")
OUT = os.path.join(OUT_DIR, "prices.json")
BENCH = ["^GSPC", "^KS11"]


def warn(msg):
    print("[warn] " + msg, file=sys.stderr)


def to_symbol(ticker, market, suffix=".KS"):
    if market == "KRX" or (ticker.isdigit() and len(ticker) == 6):
        return ticker + suffix
    return ticker


def session_open(market, last_date, now=None):
    """마지막 바 날짜가 거래소 현지 오늘이고 장이 아직 안 닫혔으면 True (미완성 바).
    US: 뉴욕 16:15 이후 마감 / KRX: 서울 15:45 이후 마감."""
    now = now or datetime.now(timezone.utc)
    if market == "KRX":
        local, close = now.astimezone(ZoneInfo("Asia/Seoul")), (15, 45)
    else:
        local, close = now.astimezone(ZoneInfo("America/New_York")), (16, 15)
    if local.strftime("%Y-%m-%d") != last_date:
        return False
    return (local.hour, local.minute) < close


def drop_open_bar(series, market, now=None):
    """진행 중인 당일 바 제거. 남는 바가 없으면 None."""
    if series is None or not series["dates"]:
        return series
    if session_open(market, series["dates"][-1], now):
        series = {k: v[:-1] for k, v in series.items()}
    return series if series["dates"] else None


def extract(df, sym, multi):
    """download 결과에서 심볼별 시리즈 추출. 비면 None."""
    try:
        sub = df[sym] if multi else df
    except KeyError:
        return None
    if sub is None or len(sub) == 0:
        return None
    sub = sub.dropna(subset=["Close"])
    if len(sub) == 0:
        return None
    dates, o, h, c = [], [], [], []
    for idx, row in sub.iterrows():
        cl = float(row["Close"])
        op = float(row["Open"]) if row["Open"] == row["Open"] else cl
        hi = float(row["High"]) if row["High"] == row["High"] else cl
        if any(math.isnan(x) or math.isinf(x) for x in (op, hi, cl)):
            continue
        dates.append(idx.strftime("%Y-%m-%d"))
        o.append(op)
        h.append(hi)
        c.append(cl)
    if not dates:
        return None
    return {"dates": dates, "open": o, "high": h, "close": c}


def download(symbols, start, end):
    """심볼 리스트 -> {symbol: series|None}"""
    if not symbols:
        return {}
    df = yf.download(
        symbols, start=start, end=end, auto_adjust=False, progress=False,
        group_by="ticker", threads=True,
    )
    multi = hasattr(df.columns, "nlevels") and df.columns.nlevels > 1
    result = {}
    for s in symbols:
        if multi:
            result[s] = extract(df, s, True)
        else:
            result[s] = extract(df, s, False) if len(symbols) == 1 else None
    return result


def main():
    with open(LEDGER, encoding="utf-8") as f:
        ledger = json.load(f)
    rows = ledger["rows"] if isinstance(ledger, dict) else ledger

    tickers = {}  # ticker -> market
    for r in rows:
        tickers.setdefault(r["ticker"], r.get("market"))
    min_date = min(r["date"] for r in rows)
    start = (datetime.strptime(min_date, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    end = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    # 원장 ticker -> 1차 심볼
    sym_of = {t: to_symbol(t, m) for t, m in tickers.items()}
    for b in BENCH:
        sym_of[b] = b

    first = download(list(dict.fromkeys(sym_of.values())), start, end)
    bench_market = {"^GSPC": "US", "^KS11": "KRX"}
    mkt_of = dict(tickers, **bench_market)

    fetched = {}
    kq_retry = []
    for key, sym in sym_of.items():
        series = first.get(sym)
        if series is not None:
            fetched[key] = (sym, series)
        elif sym.endswith(".KS"):
            kq_retry.append(key)
        else:
            warn("가격 없음: %s (%s)" % (key, sym))

    if kq_retry:
        kq_syms = [sym_of[k][:-3] + ".KQ" for k in kq_retry]
        second = download(kq_syms, start, end)
        for key, sym in zip(kq_retry, kq_syms):
            series = second.get(sym)
            if series is not None:
                fetched[key] = (sym, series)
            else:
                warn("가격 없음: %s (.KS/.KQ 모두 빈 응답)" % key)

    # 진행 중인 당일 바 제거 (장 마감 전 라이브 바를 종가로 저장 방지)
    symbols = {}
    for key, (sym, series) in fetched.items():
        series = drop_open_bar(series, mkt_of.get(key), None)
        if series is not None:
            symbols[key] = dict(symbol=sym, **series)

    # 벤치마크 누락 시 기존 캐시를 건드리지 않고 종료
    missing_bench = [b for b in BENCH if b not in symbols]
    if missing_bench:
        print("[fail] 벤치마크 누락: " + ", ".join(missing_bench), file=sys.stderr)
        sys.exit(1)

    # 이번에 실패한 종목은 기존 캐시 항목 승계
    prior = {}
    try:
        with open(OUT, encoding="utf-8") as f:
            prior = json.load(f).get("symbols", {})
    except (OSError, ValueError):
        pass
    for key in sym_of:
        if key not in symbols and key in prior:
            symbols[key] = prior[key]
            warn("이전 캐시 승계(stale): %s" % key)

    os.makedirs(OUT_DIR, exist_ok=True)
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "symbols": symbols,
    }
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, allow_nan=False)
    os.replace(tmp, OUT)
    print("[ok] prices: %d/%d symbols" % (len(symbols), len(sym_of)))


if __name__ == "__main__":
    main()
