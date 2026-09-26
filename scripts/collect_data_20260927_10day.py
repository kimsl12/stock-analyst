#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 데이터 수집 — 2026-09-27 (10일 임계, staock_update 슬롯, /재분석실행 10 10).
검출: timeline.json max-v date 기준 10일+ 경과 (진실 소스).
  09-17 배치(10일 경과) 10종 + ANTHROPIC(비상장·비표준 123일, standing 제외).
상한 10종 — 09-17 배치 10종 전부 (7일 슬롯 일일 cap 초과분이 정확히 10일에 누출).
대상 10종: STX SMR SCHD RSP QQQ QLD QCOM PM PEP NOW (전부 미국 상장).
yfinance 단일계열(WebSearch 미바인딩)로 리치 data.json 생성. 09-26 스크립트 재사용.
배당수익률 스케일 함정: divY>5% 종목은 회차 종료 전 dividendRate/price 대조 필수."""
import json, os, sys, datetime
import yfinance as yf

TODAY = "2026-09-27"
RUN = "20260927_10day"
THRESHOLD = 10

# ticker -> (folder(name만), name_kr, next_v, prev_v, prev_date)
PLAN = {
    "STX":  ("Seagate",                 "시게이트",           17, 16, "2026-09-17"),
    "SMR":  ("NuScalePower",            "뉴스케일파워",       15, 14, "2026-09-17"),
    "SCHD": ("SchwabUSDividendEquity",  "슈왑미국배당ETF",    16, 15, "2026-09-17"),
    "RSP":  ("InvescoSP500EqualWeight", "인베스코S&P동일가중", 16, 15, "2026-09-17"),
    "QQQ":  ("InvescoQQQ",              "인베스코QQQ",        16, 15, "2026-09-17"),
    "QLD":  ("ProSharesUltraQQQ",       "프로셰어즈2xQQQ",    15, 14, "2026-09-17"),
    "QCOM": ("Qualcomm",                "퀄컴",               10,  9, "2026-09-17"),
    "PM":   ("PhilipMorris",            "필립모리스",         17, 16, "2026-09-17"),
    "PEP":  ("PepsiCo",                 "펩시코",             17, 16, "2026-09-17"),
    "NOW":  ("ServiceNow",              "서비스나우",         10,  9, "2026-09-17"),
}

YF_MAP = {}  # 전종목 미국 상장 — 오버라이드 불요


def yf_symbol(ticker):
    if ticker in YF_MAP:
        return YF_MAP[ticker]
    if ticker.isdigit() and len(ticker) == 6:
        return f"{ticker}.KS"
    return ticker


def calc_atr(hist, period=14):
    if hist is None or len(hist) < 2:
        return None
    h = hist.tail(period + 1)
    trs = []
    prev_close = None
    for _, row in h.iterrows():
        hi, lo, cl = row["High"], row["Low"], row["Close"]
        if hi != hi or lo != lo or cl != cl:  # NaN guard
            continue
        if prev_close is None:
            trs.append(hi - lo)
        else:
            trs.append(max(hi - lo, abs(hi - prev_close), abs(lo - prev_close)))
        prev_close = cl
    if not trs:
        return None
    return round(sum(trs[-period:]) / min(period, len(trs)), 4)


def g(info, *keys):
    for k in keys:
        v = info.get(k)
        if v is not None:
            return v
    return None


def bn(x):
    return round(x / 1e9, 3) if x is not None else None


def _safe(df, row, col):
    try:
        v = df.loc[row, col]
        return v if v == v else None
    except Exception:
        return None


def collect(ticker):
    t = yf.Ticker(yf_symbol(ticker))
    info = t.info or {}
    hist = t.history(period="1mo")
    # KR nan 방어 — High/Low/Close 모두 결측인 행 제거 (마지막 행 nan → ATR nan 방지)
    if hist is not None and len(hist):
        hist = hist.dropna(subset=["High", "Low", "Close"])
    price = g(info, "currentPrice", "regularMarketPrice")
    if price is None and hist is not None and len(hist):
        price = round(float(hist["Close"].iloc[-1]), 2)
    prev_close = g(info, "regularMarketPreviousClose", "previousClose")
    lo52 = g(info, "fiftyTwoWeekLow")
    hi52 = g(info, "fiftyTwoWeekHigh")
    atr = calc_atr(hist)
    mcap = g(info, "marketCap", "totalAssets")
    ebitda = g(info, "ebitda")
    total_cash = g(info, "totalCash")
    total_debt = g(info, "totalDebt")
    ev_ebitda = None
    if mcap and ebitda and ebitda != 0:
        ev = mcap + (total_debt or 0) - (total_cash or 0)
        ev_ebitda = round(ev / ebitda, 2)
    range_pos = None
    if lo52 and hi52 and hi52 != lo52 and price:
        range_pos = round((price - lo52) / (hi52 - lo52) * 100)
    stop2 = round(price - 2 * atr, 2) if (price and atr) else None
    netdebt = None
    if total_debt is not None and total_cash is not None:
        netdebt = total_debt - total_cash

    qi = {}
    try:
        qis = t.quarterly_income_stmt
        if qis is not None and not qis.empty:
            cols = list(qis.columns)[:5]
            for c in cols:
                key = str(c)[:10]
                def pick(row):
                    try:
                        val = qis.loc[row, c]
                        return bn(float(val)) if val == val else None
                    except Exception:
                        return None
                qi[key] = {
                    "Total Revenue": pick("Total Revenue"),
                    "Operating Income": pick("Operating Income"),
                    "Net Income": pick("Net Income"),
                    "Diluted EPS": (lambda v: round(float(v), 2) if v is not None and v == v else None)(
                        _safe(qis, "Diluted EPS", c)),
                }
    except Exception as e:
        qi = {"error": str(e)}

    # 배당수익률 — 스케일 함정 방어: dividendRate/price 로 교차 검증도 병기
    dy = g(info, "dividendYield", "yield")
    div_rate = g(info, "dividendRate", "trailingAnnualDividendRate")
    dy_from_rate = round(div_rate / price * 100, 2) if (div_rate and price) else None
    if dy is not None:
        dy_pct = round(dy, 2) if dy > 1 else round(dy * 100, 2)
    else:
        dy_pct = dy_from_rate

    quote_type = g(info, "quoteType", "typeDisp")

    exp = g(info, "annualReportExpenseRatio", "netExpenseRatio")
    etf = {
        "quoteType": quote_type,
        "expense_ratio_pct": (round(exp * 100, 3) if (exp is not None and exp < 1) else exp),
        "totalAssets": g(info, "totalAssets"),
        "navPrice": g(info, "navPrice"),
        "ytdReturn": g(info, "ytdReturn"),
        "threeYearAvgReturn": g(info, "threeYearAverageReturn"),
        "category": g(info, "category"),
    }

    return {
        "quote": {
            "current_price": price,
            "prev_close": prev_close,
            "fiftyTwoWeekLow": lo52,
            "fiftyTwoWeekHigh": hi52,
            "range_position_pct": range_pos,
            "marketCap": mcap,
            "sharesOutstanding": g(info, "sharesOutstanding"),
            "volume": g(info, "volume", "regularMarketVolume"),
            "atr_14": atr,
            "atr_pct": round(atr / price * 100, 2) if (atr and price) else None,
            "stop_loss_2atr": stop2,
            "beta": g(info, "beta", "beta3Year"),
        },
        "valuation": {
            "trailingPE": g(info, "trailingPE"),
            "forwardPE": g(info, "forwardPE"),
            "trailingEps": g(info, "trailingEps"),
            "forwardEps": g(info, "forwardEps"),
            "pegRatio": g(info, "trailingPegRatio", "pegRatio"),
            "priceToBook": g(info, "priceToBook"),
            "priceToSalesTrailing12Months": g(info, "priceToSalesTrailing12Months"),
            "ebitda": ebitda,
            "ev_ebitda_approx": ev_ebitda,
            "enterpriseToRevenue": g(info, "enterpriseToRevenue"),
            "dividendYield_pct": dy_pct,
            "dividendRate": div_rate,
            "dividendYield_from_rate_pct": dy_from_rate,
        },
        "profitability": {
            "grossMargins": g(info, "grossMargins"),
            "operatingMargins": g(info, "operatingMargins"),
            "profitMargins": g(info, "profitMargins"),
            "returnOnEquity": g(info, "returnOnEquity"),
        },
        "growth": {
            "totalRevenue_ttm": g(info, "totalRevenue"),
            "revenueGrowth_yoy": g(info, "revenueGrowth"),
            "earningsGrowth_yoy": g(info, "earningsGrowth"),
        },
        "balance_sheet": {
            "totalCash": total_cash,
            "totalDebt": total_debt,
            "netDebt_approx": netdebt,
            "debtToEquity": g(info, "debtToEquity"),
            "freeCashflow_ttm": g(info, "freeCashflow"),
            "operating_cashflow": g(info, "operatingCashflow"),
        },
        "consensus": {
            "targetMeanPrice": g(info, "targetMeanPrice"),
            "targetHighPrice": g(info, "targetHighPrice"),
            "targetLowPrice": g(info, "targetLowPrice"),
            "targetMedianPrice": g(info, "targetMedianPrice"),
            "recommendationMean": g(info, "recommendationMean"),
            "recommendationKey": g(info, "recommendationKey"),
            "numberOfAnalystOpinions": g(info, "numberOfAnalystOpinions"),
        },
        "holders": {
            "heldPercentInsiders": g(info, "heldPercentInsiders"),
            "heldPercentInstitutions": g(info, "heldPercentInstitutions"),
            "shortPercentOfFloat": g(info, "shortPercentOfFloat"),
            "shortRatio": g(info, "shortRatio"),
        },
        "moving_avg": {
            "fiftyDayAverage": g(info, "fiftyDayAverage"),
            "twoHundredDayAverage": g(info, "twoHundredDayAverage"),
        },
        "etf": etf,
        "quarterly_income_bn": qi,
        "sector": g(info, "sector"),
        "industry": g(info, "industry"),
        "longName": g(info, "longName", "shortName"),
        "exchange": g(info, "exchange", "fullExchangeName"),
        "currency": g(info, "currency"),
        "quote_type": quote_type,
        "price_date": str(hist.index[-1])[:10] if (hist is not None and len(hist)) else TODAY,
    }


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    ok, fail = [], []
    now = datetime.datetime.now().isoformat(timespec="seconds")
    for ticker in only:
        folder, kr, nv, pv, pdate = PLAN[ticker]
        out_dir = f"analysis/{ticker}_{folder}_v{nv}"
        os.makedirs(out_dir, exist_ok=True)
        try:
            c = collect(ticker)
            if c["quote"]["current_price"] is None:
                print(f"  X {ticker}: no price")
                fail.append(ticker); continue
            out = {
                "meta": {
                    "name": c.pop("longName") or kr,
                    "ticker": ticker,
                    "name_ko": kr,
                    "exchange": c.pop("exchange"),
                    "currency": c.pop("currency") or "USD",
                    "quote_type": c.get("quote_type"),
                    "reanalysis_version": f"v{nv} (BLIND — 이전 미참조)",
                    "collected_at": now,
                    "price_as_of": c.pop("price_date"),
                    "prev_version": f"v{pv}",
                    "prev_version_date": pdate,
                    "threshold_days": THRESHOLD,
                    "session_run": RUN,
                    "data_source": "yfinance 단일계열, WebSearch 미바인딩",
                },
                **c,
            }
            with open(f"{out_dir}/data.json", "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
            q = out["quote"]
            v = out["valuation"]
            print(f"[{ticker}] OK v{nv} {out['meta']['currency']}{q['current_price']} ({out['meta']['price_as_of']}) "
                  f"type={out['meta']['quote_type']} PE={v['trailingPE']} fwdPE={v['forwardPE']} "
                  f"mcap={q['marketCap']} atr={q['atr_14']} tgtMean={out['consensus']['targetMeanPrice']} "
                  f"divY={v['dividendYield_pct']}(rate={v['dividendYield_from_rate_pct']}) -> {out_dir}/data.json")
            ok.append(ticker)
        except Exception as e:
            print(f"  X {ticker}: EXC {e}")
            fail.append(ticker)
    print(f"\n=== 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
