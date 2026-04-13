#!/usr/bin/env python3
"""
fetch_price.py — 실시간 주가 + ATR(14) 수집 스크립트

사용법:
    python scripts/fetch_price.py 010120          # 한국 종목 (6자리)
    python scripts/fetch_price.py SNDK            # 미국 종목 (알파벳)
    python scripts/fetch_price.py 000660 AAPL     # 복수 종목

출력: JSON (stdout) + analysis/{ticker}_price.md (파일)
"""

import sys
import json
from datetime import datetime, timedelta


def is_korean_ticker(ticker: str) -> bool:
    return ticker.isdigit() and len(ticker) == 6


def fetch_korean(ticker: str) -> dict:
    """pykrx로 한국 주식 데이터 수집"""
    from pykrx import stock as krx

    today = datetime.now()
    start = (today - timedelta(days=40)).strftime("%Y%m%d")
    end = today.strftime("%Y%m%d")

    df = krx.get_market_ohlcv(start, end, ticker)
    if df.empty:
        return {"error": f"No data for {ticker}", "ticker": ticker}

    df = df.tail(30)
    latest = df.iloc[-1]

    # ATR(14) 계산
    atr = _calc_atr(df, period=14)

    current_price = int(latest["종가"])
    name = krx.get_market_ticker_name(ticker)

    # 52주 고저
    start_52w = (today - timedelta(days=365)).strftime("%Y%m%d")
    df_52w = krx.get_market_ohlcv(start_52w, end, ticker)
    high_52w = int(df_52w["고가"].max()) if not df_52w.empty else None
    low_52w = int(df_52w["저가"].min()) if not df_52w.empty else None

    # 시가총액 — yfinance 보조 사용 (pykrx 시가총액 API 불안정)
    try:
        import yfinance as yf
        info = yf.Ticker(f"{ticker}.KS").info
        market_cap = info.get("marketCap")
        if not market_cap:
            info = yf.Ticker(f"{ticker}.KQ").info
            market_cap = info.get("marketCap")
    except Exception:
        market_cap = None

    return {
        "ticker": ticker,
        "name": name,
        "market": "KRX",
        "currency": "KRW",
        "current_price": current_price,
        "prev_close": int(df.iloc[-2]["종가"]) if len(df) >= 2 else None,
        "change_pct": round((current_price / int(df.iloc[-2]["종가"]) - 1) * 100, 2) if len(df) >= 2 else None,
        "high_52w": high_52w,
        "low_52w": low_52w,
        "market_cap": market_cap,
        "market_cap_str": _format_krw(market_cap) if market_cap else None,
        "volume": int(latest["거래량"]),
        "atr_14": int(round(atr)) if atr else None,
        "atr_pct": round(atr / current_price * 100, 2) if atr else None,
        "stop_loss_2atr": int(current_price - 2 * atr) if atr else None,
        "target_3atr": int(current_price + 3 * atr) if atr else None,
        "date": latest.name.strftime("%Y-%m-%d"),
        "fetch_time": datetime.now().isoformat(),
    }


def fetch_us(ticker: str) -> dict:
    """yfinance로 미국/글로벌 주식 데이터 수집"""
    import yfinance as yf

    stock = yf.Ticker(ticker)
    hist = stock.history(period="3mo")
    if hist.empty:
        return {"error": f"No data for {ticker}", "ticker": ticker}

    hist = hist.tail(30)
    latest = hist.iloc[-1]

    atr = _calc_atr_yf(hist, period=14)
    current_price = round(float(latest["Close"]), 2)

    info = stock.info or {}
    name = info.get("shortName", info.get("longName", ticker))
    market_cap = info.get("marketCap")

    hist_52w = stock.history(period="1y")
    high_52w = round(float(hist_52w["High"].max()), 2) if not hist_52w.empty else None
    low_52w = round(float(hist_52w["Low"].min()), 2) if not hist_52w.empty else None

    return {
        "ticker": ticker,
        "name": name,
        "market": info.get("exchange", "US"),
        "currency": info.get("currency", "USD"),
        "current_price": current_price,
        "prev_close": round(float(hist.iloc[-2]["Close"]), 2) if len(hist) >= 2 else None,
        "change_pct": round((current_price / float(hist.iloc[-2]["Close"]) - 1) * 100, 2) if len(hist) >= 2 else None,
        "high_52w": high_52w,
        "low_52w": low_52w,
        "market_cap": market_cap,
        "market_cap_str": _format_usd(market_cap) if market_cap else None,
        "volume": int(latest["Volume"]),
        "atr_14": round(atr, 2) if atr else None,
        "atr_pct": round(atr / current_price * 100, 2) if atr else None,
        "stop_loss_2atr": round(current_price - 2 * atr, 2) if atr else None,
        "target_3atr": round(current_price + 3 * atr, 2) if atr else None,
        "date": hist.index[-1].strftime("%Y-%m-%d"),
        "fetch_time": datetime.now().isoformat(),
    }


def _calc_atr(df, period=14):
    """pykrx DataFrame용 ATR 계산"""
    if len(df) < period + 1:
        return None
    highs = df["고가"].values
    lows = df["저가"].values
    closes = df["종가"].values
    trs = []
    for i in range(1, len(df)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    if len(trs) < period:
        return None
    return sum(trs[-period:]) / period


def _calc_atr_yf(df, period=14):
    """yfinance DataFrame용 ATR 계산"""
    if len(df) < period + 1:
        return None
    highs = df["High"].values
    lows = df["Low"].values
    closes = df["Close"].values
    trs = []
    for i in range(1, len(df)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    if len(trs) < period:
        return None
    return sum(trs[-period:]) / period


def _format_krw(value):
    if value >= 1e12:
        return f"{value / 1e12:.1f}조원"
    elif value >= 1e8:
        return f"{value / 1e8:.0f}억원"
    return f"{value:,}원"


def _format_usd(value):
    if value >= 1e12:
        return f"${value / 1e12:.2f}T"
    elif value >= 1e9:
        return f"${value / 1e9:.1f}B"
    elif value >= 1e6:
        return f"${value / 1e6:.0f}M"
    return f"${value:,.0f}"


def generate_price_md(data: dict) -> str:
    """주가 데이터를 마크다운 형식으로 변환"""
    if "error" in data:
        return f"# {data['ticker']} 주가 수집 실패\n\n오류: {data['error']}\n"

    currency_sym = "W" if data["currency"] == "KRW" else "$"
    price_fmt = f"{data['current_price']:,}" if data["currency"] == "KRW" else f"{data['current_price']}"

    lines = [
        f"# {data['name']} ({data['ticker']}) 실시간 주가",
        f"",
        f"수집 시각: {data['fetch_time']}",
        f"데이터 기준일: {data['date']}",
        f"",
        f"## 주가",
        f"- 현재가: {currency_sym}{price_fmt}",
        f"- 전일비: {data['change_pct']:+.2f}%" if data.get("change_pct") else "",
        f"- 52주 고가: {currency_sym}{data['high_52w']:,}" if data.get("high_52w") else "",
        f"- 52주 저가: {currency_sym}{data['low_52w']:,}" if data.get("low_52w") else "",
        f"- 시가총액: {data.get('market_cap_str', 'N/A')}",
        f"- 거래량: {data['volume']:,}",
        f"",
        f"## ATR 기반 손절/목표가",
        f"- ATR(14): {currency_sym}{data['atr_14']:,}" if data.get("atr_14") else "- ATR(14): N/A",
        f"- ATR 변동성: {data['atr_pct']}%" if data.get("atr_pct") else "",
        f"- 손절가 (2x ATR): {currency_sym}{data['stop_loss_2atr']:,}" if data.get("stop_loss_2atr") else "",
        f"- 목표가 (3x ATR): {currency_sym}{data['target_3atr']:,}" if data.get("target_3atr") else "",
    ]
    return "\n".join(line for line in lines if line is not None)


# === 시장 지수 일괄 수집 (--market 모드) [v1.1] ===

MARKET_TICKERS = {
    # 미국 지수
    "^GSPC": "S&P 500",
    "^IXIC": "NASDAQ",
    "^DJI": "Dow Jones",
    "^VIX": "VIX",
    # 아시아 지수
    "^KS11": "KOSPI",
    "^KQ11": "KOSDAQ",
    "^N225": "Nikkei 225",
    "^HSI": "Hang Seng",
    # 환율/원자재/금
    "DX-Y.NYB": "DXY (Dollar Index)",
    "GC=F": "Gold Futures",
    "CL=F": "WTI Crude Oil",
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    # 채권
    "^TNX": "US 10Y Yield",
    "^TYX": "US 30Y Yield",
    # 환율
    "KRW=X": "USD/KRW",
    "JPY=X": "USD/JPY",
    "CNY=X": "USD/CNY",
}


def fetch_market_snapshot() -> list:
    """시장 지수 일괄 수집 → daily_snapshot.md 갱신용"""
    import yfinance as yf

    results = []
    for ticker, name in MARKET_TICKERS.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            if hist.empty:
                results.append({"ticker": ticker, "name": name, "error": "No data"})
                continue

            latest = hist.iloc[-1]
            prev = hist.iloc[-2] if len(hist) >= 2 else None
            price = round(float(latest["Close"]), 2)
            change = round((price / float(prev["Close"]) - 1) * 100, 2) if prev is not None else None

            results.append({
                "ticker": ticker,
                "name": name,
                "price": price,
                "change_pct": change,
                "date": hist.index[-1].strftime("%Y-%m-%d"),
            })
        except Exception as e:
            results.append({"ticker": ticker, "name": name, "error": str(e)})

    return results


def generate_snapshot_md(results: list) -> str:
    """시장 스냅샷을 daily_snapshot.md 형식으로 변환"""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "---",
        f"updated: {today}",
        f"valid_until: {(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')}",
        "category: market",
        "collection_status: SUCCESS",
        "confidence: high",
        f"last_synced_from_db: {today}",
        "---",
        "",
        "# Daily Market Snapshot",
        "",
        f"## CURRENT ({today})",
        "",
        "### 미국 지수",
        "| 지수 | 종가 | 등락률 | 기준일 |",
        "|------|------|--------|--------|",
    ]

    sections = {
        "미국 지수": ["^GSPC", "^IXIC", "^DJI", "^VIX"],
        "아시아 지수": ["^KS11", "^KQ11", "^N225", "^HSI"],
        "환율": ["DX-Y.NYB", "KRW=X", "JPY=X", "CNY=X"],
        "원자재/금": ["GC=F", "CL=F"],
        "채권 수익률": ["^TNX", "^TYX"],
        "크립토": ["BTC-USD", "ETH-USD"],
    }

    lookup = {r["ticker"]: r for r in results}
    first_section = True

    for section_name, tickers in sections.items():
        if not first_section:
            lines.append(f"\n### {section_name}")
            lines.append("| 항목 | 종가 | 등락률 | 기준일 |")
            lines.append("|------|------|--------|--------|")
        first_section = False

        for t in tickers:
            r = lookup.get(t, {})
            if "error" in r:
                lines.append(f"| {r.get('name', t)} | N/A | N/A | N/A |")
            else:
                chg = f"{r['change_pct']:+.2f}%" if r.get("change_pct") is not None else "N/A"
                lines.append(f"| {r['name']} | {r['price']:,.2f} | {chg} | {r.get('date', 'N/A')} |")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("사용법:")
        print("  python scripts/fetch_price.py <ticker> [<ticker2> ...]  # 개별 종목")
        print("  python scripts/fetch_price.py --market                  # 시장 지수 일괄")
        print("  python scripts/fetch_price.py --market --save           # 시장 지수 + KB 저장")
        sys.exit(1)

    # --market 모드: 시장 지수 일괄 수집
    if "--market" in sys.argv:
        print("Fetching market snapshot...")
        results = fetch_market_snapshot()

        success = sum(1 for r in results if "error" not in r)
        fail = sum(1 for r in results if "error" in r)
        print(f"\nCollected: {success}/{len(results)} (failed: {fail})")

        md_content = generate_snapshot_md(results)
        print(f"\n{md_content}")

        if "--save" in sys.argv:
            import os
            kb_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                   "knowledge-base", "market", "daily_snapshot.md")
            with open(kb_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"\nSaved to {kb_path}")

        print(f"\n{'='*50}")
        print("JSON_OUTPUT_START")
        print(json.dumps(results, ensure_ascii=False, indent=2))
        print("JSON_OUTPUT_END")
        return

    # 개별 종목 모드
    tickers = [t for t in sys.argv[1:] if not t.startswith("--")]
    results = []

    for ticker in tickers:
        try:
            if is_korean_ticker(ticker):
                data = fetch_korean(ticker)
            else:
                data = fetch_us(ticker)
            results.append(data)
            print(f"\n{'='*50}")
            print(generate_price_md(data))
        except Exception as e:
            error_data = {"ticker": ticker, "error": str(e)}
            results.append(error_data)
            print(f"\n[ERROR] {ticker}: {e}", file=sys.stderr)

    print(f"\n{'='*50}")
    print("JSON_OUTPUT_START")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print("JSON_OUTPUT_END")


if __name__ == "__main__":
    main()
