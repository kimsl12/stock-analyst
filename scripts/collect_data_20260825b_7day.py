#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 데이터 수집 — 2026-08-25 (7일 임계, stock_update-2 슬롯, /재분석실행 7 20→10).
검출: timeline.json max-v date 기준 61종이 7일+ 경과. ANTHROPIC(비상장·비표준, 90일) standing 제외.
경과일 desc 상위(10일, 08-15 재분석분) 코호트 중 스킬 정렬(경과 desc → 종목명 desc/asc) 상위 10종.
yfinance 단일계열(WebSearch 미바인딩)로 리치 data.json 생성 → analysis/{ticker}_{folder}_v{nv}/data.json.
한국 6자리 티커는 .KS 접미사로 조회하되, 저장 ticker/폴더는 원 코드 유지.
로직은 20260824b 검증본 재사용, PLAN 만 08-15 10일 코호트 10종으로 교체.
"""
import json, os, sys, datetime
import yfinance as yf

TODAY = "2026-08-25"
RUN = "20260825b_7day"
THRESHOLD = 7

# ticker -> (folder, name_kr, next_v, prev_v, prev_date)
PLAN = {
    "000660": ("SK하이닉스",           "SK하이닉스",             9,  8,  "2026-08-15"),
    "035420": ("NAVER",               "NAVER",                 14, 13, "2026-08-15"),
    "066570": ("LG전자",              "LG전자",                11, 10, "2026-08-15"),
    "BWXT":   ("BWXTechnologies",     "BWX테크놀로지스",        8,  7,  "2026-08-15"),
    "CCJ":    ("Cameco",              "카메코",                 8,  7,  "2026-08-15"),
    "CEG":    ("ConstellationEnergy", "컨스텔레이션에너지",     12, 11, "2026-08-15"),
    "DUK":    ("DukeEnergy",          "듀크에너지",             8,  7,  "2026-08-15"),
    "ETN":    ("Eaton",               "이튼",                   12, 11, "2026-08-15"),
    "KTOS":   ("KratosDefense",       "크라토스디펜스",         13, 12, "2026-08-15"),
    "MLSS":   ("MilestoneScientific", "마일스톤사이언티픽",     13, 12, "2026-08-15"),
}


def yf_symbol(ticker):
    """한국 6자리 숫자 코드는 .KS(코스피) 접미사. 그 외 미국 티커는 그대로."""
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
    price = g(info, "currentPrice", "regularMarketPrice")
    if price is None and hist is not None and len(hist):
        price = round(float(hist["Close"].iloc[-1]), 2)
    prev_close = g(info, "regularMarketPreviousClose", "previousClose")
    lo52 = g(info, "fiftyTwoWeekLow")
    hi52 = g(info, "fiftyTwoWeekHigh")
    atr = calc_atr(hist)
    mcap = g(info, "marketCap")
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

    dy = g(info, "dividendYield")
    if dy is not None:
        dy_pct = round(dy, 2) if dy > 1 else round(dy * 100, 2)
    else:
        dy_pct = None

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
            "beta": g(info, "beta"),
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
        "quarterly_income_bn": qi,
        "sector": g(info, "sector"),
        "industry": g(info, "industry"),
        "longName": g(info, "longName", "shortName"),
        "exchange": g(info, "exchange", "fullExchangeName"),
        "currency": g(info, "currency"),
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
            print(f"[{ticker}] OK v{nv} {out['meta']['currency']}{q['current_price']} ({out['meta']['price_as_of']}) "
                  f"PE={out['valuation']['trailingPE']} mcap={q['marketCap']} -> {out_dir}/data.json")
            ok.append(ticker)
        except Exception as e:
            print(f"  X {ticker}: EXC {e}")
            fail.append(ticker)
    print(f"\n=== 수집 완료 — 성공 {len(ok)} / 실패 {len(fail)} ===")
    if fail:
        print("실패:", ", ".join(fail))


if __name__ == "__main__":
    main()
