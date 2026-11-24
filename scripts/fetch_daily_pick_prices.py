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

    symbols = {}
    kq_retry = []
    for key, sym in sym_of.items():
        series = first.get(sym)
        if series is not None:
            symbols[key] = dict(symbol=sym, **series)
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
                symbols[key] = dict(symbol=sym, **series)
            else:
                warn("가격 없음: %s (.KS/.KQ 모두 빈 응답)" % key)

    total = len(sym_of)
    missing_bench = [b for b in BENCH if b not in symbols]
    os.makedirs(OUT_DIR, exist_ok=True)
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "symbols": symbols,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, allow_nan=False)

    if missing_bench:
        print("[fail] 벤치마크 누락: " + ", ".join(missing_bench), file=sys.stderr)
        sys.exit(1)
    print("[ok] prices: %d/%d symbols" % (len(symbols), total))


if __name__ == "__main__":
    main()
