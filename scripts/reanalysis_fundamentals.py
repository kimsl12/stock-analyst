#!/usr/bin/env python3
"""
reanalysis_fundamentals.py — BLIND 재분석용 펀더멘털 일괄 수집 (yfinance)
사용법: python3 scripts/reanalysis_fundamentals.py INTC
출력: info 핵심 + 최근 분기 손익 + 애널리스트 목표가/투자의견 (stdout, 사람이 읽는 요약).
WebSearch 미바인딩 슬롯 대비 — 이 스크립트 1회 호출로 재무/컨센서스 확보.
"""
import sys, json
import warnings
warnings.filterwarnings("ignore")

t = sys.argv[1]
import yfinance as yf
tk = yf.Ticker(t)
info = tk.info or {}

def g(*keys):
    for k in keys:
        v = info.get(k)
        if v not in (None, ""):
            return v
    return None

print(f"===== {t} — yfinance 펀더멘털 =====")
print(f"이름: {g('longName','shortName')}")
print(f"섹터/산업: {g('sector')} / {g('industry')}")
print(f"현재가: {g('currentPrice','regularMarketPrice','navPrice')}  시총: {g('marketCap')}")
print(f"PER(trailing/forward): {g('trailingPE')} / {g('forwardPE')}")
print(f"PBR: {g('priceToBook')}  PSR: {g('priceToSalesTrailing12Months')}")
print(f"EPS(trailing/forward): {g('trailingEps')} / {g('forwardEps')}")
print(f"매출(TTM): {g('totalRevenue')}  매출성장(YoY): {g('revenueGrowth')}")
print(f"이익성장(YoY): {g('earningsGrowth')}  분기매출성장: {g('revenueQuarterlyGrowth')}")
print(f"영업이익률: {g('operatingMargins')}  순이익률: {g('profitMargins')}  총이익률: {g('grossMargins')}")
print(f"ROE: {g('returnOnEquity')}  ROA: {g('returnOnAssets')}")
print(f"부채/자본: {g('debtToEquity')}  총현금: {g('totalCash')}  총부채: {g('totalDebt')}")
print(f"FCF: {g('freeCashflow')}  영업CF: {g('operatingCashflow')}")
print(f"배당수익률: {g('dividendYield')}  배당성향: {g('payoutRatio')}")
print(f"베타: {g('beta')}  52주변동: {g('52WeekChange')}")
print(f"애널리스트 투자의견: {g('recommendationKey')} (mean {g('recommendationMean')}, {g('numberOfAnalystOpinions')}인)")
print(f"목표가 평균/저/고: {g('targetMeanPrice')} / {g('targetLowPrice')} / {g('targetHighPrice')}  (현재가 대비)")
print(f"배당/ETF 여부·운용사: quoteType={g('quoteType')}  category={g('category')}  운용보수={g('annualReportExpenseRatio')}")

# 최근 분기 손익
try:
    qf = tk.quarterly_income_stmt
    if qf is not None and not qf.empty:
        print("\n----- 최근 분기 손익 (열=분기, 단위 원자료) -----")
        rows = ["Total Revenue", "Operating Income", "Net Income", "Gross Profit", "Basic EPS", "Diluted EPS"]
        cols = list(qf.columns)[:5]
        header = "지표\t" + "\t".join(str(c)[:10] for c in cols)
        print(header)
        for r in rows:
            if r in qf.index:
                vals = []
                for c in cols:
                    v = qf.loc[r, c]
                    try:
                        vals.append(f"{float(v):,.0f}" if abs(float(v)) >= 1000 else f"{float(v):.2f}")
                    except Exception:
                        vals.append("-")
                print(f"{r}\t" + "\t".join(vals))
except Exception as e:
    print(f"(분기 손익 조회 실패: {e})")

# 애널리스트 목표가 상세
try:
    apt = tk.analyst_price_targets
    if apt:
        print(f"\n----- analyst_price_targets -----\n{apt}")
except Exception:
    pass
