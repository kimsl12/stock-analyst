---
file: 2026_daily_prices
year: 2026
created: 2026-04-07
write_owner: market-data-collector
read_owners: [briefing-lead, global-macro-analyst, correlation-monitor, briefing-report-generator]
type: time_series
---

> **쓰기 권한:** market-data-collector
> **읽기 권한:** briefing-lead, global-macro-analyst, correlation-monitor, briefing-report-generator
> **목적:** 2026년 시장 daily prices 시계열 영구 축적 (append-only).
> **마이그레이션:** 2026-04-07 `scripts/migrate_market_jsonl_to_md.py` 로 기존 .jsonl 변환.

# 2026 Daily Prices

| 일자 | 카테고리 | 키 | 종가/현재 | 일간 변동률 | 단위 | 출처 | 수집시각 | Alert |
|---|---|---|---|---|---|---|---|---|
| 2026-04-07 | us_index | SP500 | — | — | point | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden — Yahoo Finance API 접근 불가 |
| 2026-04-07 | us_index | NASDAQ | — | — | point | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | us_index | DJIA | — | — | point | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | us_index | Russell2000 | — | — | point | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | us_index | VIX | — | — | index | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | asia_index | KOSPI | — | — | point | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | asia_index | KOSDAQ | — | — | point | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | asia_index | Nikkei225 | — | — | point | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | asia_index | ShanghaiComposite | — | — | point | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | asia_index | HangSeng | — | — | point | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | fx | USDKRW | — | — | KRW | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | commodity | WTI | — | — | USD/barrel | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | commodity | Gold | — | — | USD/oz | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | fx | DXY | — | — | index | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | bond | US10Y | — | — | percent | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | bond | US2Y | — | — | percent | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | bond | Spread2Y10Y | — | — | bp | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden — 계산값 산출 불가 |
| 2026-04-07 | crypto | BTC | — | — | USD | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden — CoinGecko 접근 불가 |
| 2026-04-07 | crypto | ETH | — | — | USD | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | crypto | SOL | — | — | USD | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | crypto | TotalMarketCap | — | — | USD | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden |
| 2026-04-07 | crypto | FearAndGreedIndex | — | — | index | N/A [수집실패: 네트워크 차단 환경] | 2026-04-07T00:00:00Z | 외부 네트워크 403 Forbidden — alternative.me 접근 불가 |
| 2026-04-17 | us_index | SP500 | 7041.28 | +0.26% | point | Yahoo Finance / CNBC [2026-04-16 종가] | 2026-04-17T18:00:00+09:00 | 04-17 공식 마감 미공시. 04-16 종가 사용. |
| 2026-04-17 | us_index | NASDAQ | 24102.70 | +0.36% | point | Yahoo Finance / CNBC [2026-04-16 종가] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | us_index | DJIA | 48578.72 | +0.24% | point | Yahoo Finance / CNBC [2026-04-16 종가] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | us_index | Russell2000 | 2713.66 | +0.30% | point | Yahoo Finance [2026-04-16 종가] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | us_index | VIX | 17.94 | -1.27% | index | Yahoo Finance [2026-04-16 종가] | 2026-04-17T18:00:00+09:00 | 17.94 — 소비심리 47.6 역대최저와 극단 괴리 |
| 2026-04-17 | asia_index | Nikkei225 | ~58930 | -1.0% | point | CNBC [2026-04-17 마감 추정] | 2026-04-17T18:00:00+09:00 | 04-17 -1% 수준 보도. 휴전 불확실 |
| 2026-04-17 | asia_index | SENSEX | 78497.56 | +0.65% | point | Goodreturns/Trading Economics [2026-04-17] | 2026-04-17T18:00:00+09:00 | 원유 하락 + 세계 성장 기대 |
| 2026-04-17 | asia_index | KOSPI | — | — | point | 미수집 — 마감치 미공시 | 2026-04-17T18:00:00+09:00 | 04-17 하락 출발 보도 |
| 2026-04-17 | asia_index | HangSeng | — | — | point | 미수집 | 2026-04-17T18:00:00+09:00 | 하락 출발 보도 |
| 2026-04-17 | fx | DXY | 98.19 | — | index | Trading Economics [2026-04-16] | 2026-04-17T18:00:00+09:00 | 3년래 최저권. 탈달러 구조화 |
| 2026-04-17 | fx | USDKRW | 1476.32 | — | KRW | Fed H.10 / PoundSterlingLive [2026-04-16] | 2026-04-17T18:00:00+09:00 | 1,400 초과 |
| 2026-04-17 | fx | USDJPY | 159.24 | +0.27% | JPY | [2026-04-17] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | commodity | WTI | 93.74 | — | USD/barrel | Investing.com / Trading Economics [2026-04-17] | 2026-04-17T18:00:00+09:00 | 이란 협상 기대 하방 지속. 4/16 종가 $94.62 |
| 2026-04-17 | commodity | Brent | 94.89 | -0.04% | USD/barrel | Trading Economics [2026-04-16] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | commodity | Gold | ~4800 | — | USD/oz | Bloomberg / Fortune [2026-04-17] | 2026-04-17T18:00:00+09:00 | $4,800 지지 테스트. $4,780 이탈 시 단기 약화 |
| 2026-04-17 | bond | US10Y | 4.31 | +0.65% | percent | FRED / Trading Economics [2026-04-17] | 2026-04-17T18:00:00+09:00 | 4거래일 연속 반등. 4.35% 임박 |
| 2026-04-17 | bond | US30Y | 4.93 | +0.80% | percent | [2026-04-16] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | crypto | BTC | ~75000 | +5.9% | USD | 247WallSt / CNBC [2026-04-17] | 2026-04-17T18:00:00+09:00 | 이란 협상 재개 기대. 리스크온 |
| 2026-04-17 | crypto | ETH | ~2377 | +8.6% | USD | 247WallSt [2026-04-17] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | crypto | SOL | ~87.6 | +6.3% | USD | 247WallSt [2026-04-17] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-18 | us_index | SP500 | 7126.06 | +1.20% | point | Yahoo Finance / CNBC [2026-04-18 종가 확정] | 2026-04-19T10:00:00+09:00 | 04-19 교차검증 완료. 신고가 기록 |
| 2026-04-18 | us_index | NASDAQ | 24468.48 | +1.52% | point | Yahoo Finance / CNBC [2026-04-18 종가 확정] | 2026-04-19T10:00:00+09:00 | NASDAQ 13일 연승 (1992년 이후 최장) |
| 2026-04-18 | us_index | DJIA | 49447.43 | +1.79% | point | Yahoo Finance / CNBC [2026-04-18 종가 확정] | 2026-04-19T10:00:00+09:00 | Dow 49,447 신고가 |
| 2026-04-18 | us_index | Russell2000 | 2776.90 | +2.11% | point | Yahoo Finance [2026-04-18 종가 확정] | 2026-04-19T10:00:00+09:00 | Russell 2000 신고가 |
| 2026-04-18 | us_index | VIX | 17.48 | -2.56% | index | Yahoo Finance [2026-04-18 종가 확정] | 2026-04-19T10:00:00+09:00 | 거짓 안정 5단계. 소비심리 47.6 괴리 30pt 역대급 |
| 2026-04-18 | asia_index | KOSPI | 6191.92 | -0.55% | point | DigitalToday / Seoul Economic Daily [2026-04-18 마감] | 2026-04-18T16:00:00+09:00 | 외인 차익실현. 신현승 4/21 취임 관망 |
| 2026-04-18 | asia_index | KOSDAQ | 1162.97 | +0.91% | point | DigitalToday [2026-04-18 마감] | 2026-04-18T16:00:00+09:00 | 외인 464.4억 + 기관 1.1조 순매수 |
| 2026-04-18 | asia_index | Nikkei225 | 58475.90 | -1.75% | point | CNBC [2026-04-18 마감] | 2026-04-18T16:00:00+09:00 | 호르무즈 소화 후 차익실현 |
| 2026-04-18 | asia_index | HangSeng | ~26130 | -1.01% | point | CNBC [2026-04-18 마감 추정] | 2026-04-18T16:30:00+09:00 | 종가 추정 (이전 26394 기준 -1.01%) |
| 2026-04-18 | asia_index | ShanghaiComposite | — | -0.17% | point | CNBC [2026-04-18 CSI300 기준] | 2026-04-18T16:00:00+09:00 | CSI300 -0.17% 소폭 하락 |
| 2026-04-18 | fx | DXY | 98.21 | +0.01% | index | Investing.com [2026-04-18 확정] | 2026-04-19T10:00:00+09:00 | 호르무즈 해소에도 반등 없음. 탈달러 구조적 약세 |
| 2026-04-18 | fx | USDKRW | ~1484 | — | KRW | PoundSterlingLive [2026-04-18] | 2026-04-18T20:00:00+09:00 | 1,400 초과 지속 |
| 2026-04-18 | fx | EURUSD | ~1.1370 | — | USD | Investing.com [2026-04-18] | 2026-04-18T20:00:00+09:00 | DXY 98선 유지 |
| 2026-04-18 | fx | USDJPY | ~159.40 | — | JPY | [2026-04-18 추정] | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | commodity | WTI | 83.85 | — | USD/barrel | TradingEconomics / Investing.com [2026-04-18] | 2026-04-19T10:00:00+09:00 | 호르무즈 완전개방 후 4일 -19%. $104→$83.85 |
| 2026-04-18 | commodity | Brent | 90.38 | — | USD/barrel | TradingEconomics [2026-04-18] | 2026-04-19T10:00:00+09:00 | WTI-Brent 스프레드 $6.5 |
| 2026-04-18 | commodity | Gold | 4878 | +0.6% | USD/oz | TradingEconomics / LiteFinance [2026-04-18] | 2026-04-19T10:00:00+09:00 | 신고가 갱신권. 구조적 Bull 재확정. DXY 하락에도 단절적 강세 |
| 2026-04-18 | commodity | Silver | 81.84 | +4%이상(주간) | USD/oz | TradingEconomics [2026-04-18] | 2026-04-19T10:00:00+09:00 | Gold 동조 + 산업수요. 1개월 고점 |
| 2026-04-18 | commodity | Copper | ~6.11 | — | USD/lbs | TradingEconomics [2026-04-18] | 2026-04-19T10:00:00+09:00 | Section 232 50% 관세 압력 |
| 2026-04-18 | bond | US10Y | ~4.27 | — | percent | TradingEconomics / FRED [2026-04-17 확인, 04-18 보합 추정] | 2026-04-19T10:00:00+09:00 | 4거래일 반등 추세. 4.35% 분기점 |
| 2026-04-18 | bond | US2Y | ~3.81 | — | percent | FRED [2026-04-10 공식] | 2026-04-19T10:00:00+09:00 | — |
| 2026-04-18 | bond | US30Y | ~4.88 | — | percent | [2026-04-17 기준 유지] | 2026-04-19T10:00:00+09:00 | — |
| 2026-04-18 | bond | Spread2Y10Y | ~+46 | — | bp | 계산값 (4.27%-3.81%=0.46%) | 2026-04-19T10:00:00+09:00 | 정상 구간(비역전). +46bp |
| 2026-04-18 | crypto | BTC | 77319 | +3.42% | USD | CoinGabbar [2026-04-18] | 2026-04-18T20:00:00+09:00 | 독립 강세 2일 연속. Gold 동시 상승 = 탈달러 쌍끌이 |
| 2026-04-18 | crypto | ETH | 2424.73 | +3.89% | USD | CoinGabbar [2026-04-18] | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | crypto | SOL | ~85.92 | -2.45% | USD | CoinGabbar [2026-04-18] | 2026-04-18T20:00:00+09:00 | Drift Protocol 익스플로잇 여파 |
| 2026-04-18 | crypto | TotalMarketCap | ~2.70T | +2.8% | USD | CoinGabbar [2026-04-18] | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | crypto | FearAndGreedIndex | 21~26 | — | index | alternative.me / BanklessTimes [2026-04-18] | 2026-04-18T20:00:00+09:00 | 소스별 혼재 (alt.me 21 vs CMC "Greed"). Extreme Fear 근접 |
| 2026-04-19 | crypto | BTC | 77305 | +1.0% | USD | CoinGabbar / CoinDesk [2026-04-19 주말] | 2026-04-19T10:00:00+09:00 | $77K대 안착 중. 주말 거래 |
| 2026-04-19 | crypto | ETH | 2423.71 | +3.86% | USD | CoinGabbar [2026-04-19 주말] | 2026-04-19T10:00:00+09:00 | — |
| 2026-04-19 | crypto | SOL | 86.57 | -3.29% | USD | CoinGabbar / OKX [2026-04-19 주말] | 2026-04-19T10:00:00+09:00 | — |
| 2026-04-19 | crypto | TotalMarketCap | ~2.70T | +2.8% | USD | CoinGabbar [2026-04-19 주말] | 2026-04-19T10:00:00+09:00 | BTC 도미넌스 ~57% |
| 2026-04-19 | crypto | FearAndGreedIndex | 21 | — | index | alternative.me [2026-04-19] | 2026-04-19T10:00:00+09:00 | Extreme Fear 근접 (기준선 25). 개선 중(전주 15→21) |
| 2026-04-20 | crypto | BTC | 77162 | +3.00% | USD | CoinGecko [2026-04-20 일요일 현재] | 2026-04-20T09:00:00+09:00 | $77K대 주말 유지. 독립 강세 4일 연속. 7일 +5.5% |
| 2026-04-20 | crypto | ETH | ~2370 | — | USD | CoinGecko 비율 추정 (SOL/ETH=0.03767) [2026-04-20] | 2026-04-20T09:00:00+09:00 | BTC 대비 소폭 약세 추정 |
| 2026-04-20 | crypto | SOL | ~85.02 | -4.8%(vs ETH) | USD | Investing.com / CoinMarketCap [2026-04-20] | 2026-04-20T09:00:00+09:00 | Drift 익스플로잇 여파 지속 |
| 2026-04-20 | crypto | TotalMarketCap | ~2.69T | — | USD | CoinGecko [2026-04-20] | 2026-04-20T09:00:00+09:00 | BTC 도미넌스 57.4% |
| 2026-04-20 | crypto | FearAndGreedIndex | 27 | — | index | alternative.me [2026-04-19~20] | 2026-04-20T09:00:00+09:00 | Fear 구간. 04-19 21에서 소폭 개선. 25(Extreme Fear) 기준선 상회 |
| 2026-04-20 | futures | SP500_Futures | 7103 | -0.32% | point | Investing.com [2026-04-20 일요일 프리마켓] | 2026-04-20T09:00:00+09:00 | 호르무즈 재봉쇄 + 나포 + 협상 결렬 초기 반영. 04-21 갭다운 예고 |
| 2026-04-20 | news | Hormuz_Status | CLOSED | — | — | CNN/NPR/Al Jazeera [2026-04-18~19] | 2026-04-20T09:00:00+09:00 | 04-17 개방→04-18 재봉쇄. 04-19 미 USS Spruance 이란 투스카 나포. 4/22 휴전 만료 D-2. 이란 2차 협상 거부 |
| 2026-04-21 | us_index | SP500 | 7109.14 | -0.24% | point | CNBC / Yahoo Finance [2026-04-21 close] | 2026-04-21T21:00:00-04:00 | NASDAQ 13일 연승 종료. VIX 거짓안정 해제 1단계 |
| 2026-04-21 | us_index | NASDAQ | 24404.39 | -0.26% | point | CNBC / Yahoo Finance [2026-04-21 close] | 2026-04-21T21:00:00-04:00 | 13일 연승 종료(1992년 이후 최장). 호르무즈 재봉쇄 반영 |
| 2026-04-21 | us_index | DJIA | 49442.56 | -0.01% | point | CNBC / Yahoo Finance [2026-04-21 close] | 2026-04-21T21:00:00-04:00 | 보합. Dow 상대 안정 |
| 2026-04-21 | us_index | Russell2000 | 2792.96 | +0.58% | point | Yahoo Finance [2026-04-21 close] | 2026-04-21T21:00:00-04:00 | 소형주 강세. Breadth 확대 신호 |
| 2026-04-21 | us_index | VIX | 18.98 | +8.58% | index | CNBC / CBOE [2026-04-21 close] | 2026-04-21T21:00:00-04:00 | ⚠️ 거짓안정 5단계→해제 1일차. 숏볼 해제 시작 |
| 2026-04-21 | asia_index | KOSPI | 6219.09 | +0.44% | point | CNBC Asia / Trading Economics [2026-04-21] | 2026-04-21T15:30:00+09:00 | 신현승 취임 안도 + 반도체 외인 매수. 장중 6355 사상최고 |
| 2026-04-21 | asia_index | Nikkei225 | 58825 | +0.60% | point | CNBC Asia [2026-04-21] | 2026-04-21T15:30:00+09:00 | AI주 강세 반등. 엔화 약세 수혜 |
| 2026-04-21 | asia_index | HangSeng | ~25900 | 소폭하락(추정) | point | 추정 [2026-04-21] | 2026-04-21T16:00:00+08:00 | 미중 무역 우려 재부각 |
| 2026-04-21 | fx | USDKRW | 1486 | +2원 | KRW | Investing.com / Bloomberg [2026-04-21] | 2026-04-21T21:00:00-04:00 | ⚠️ 1400 초과 지속. 호르무즈 재봉쇄 반영 |
| 2026-04-21 | fx | DXY | 98.19 | -0.02pt | index | Investing.com [2026-04-21] | 2026-04-21T21:00:00-04:00 | ⚠️ 구조적 약세. 호르무즈 재봉쇄에도 반등 없음 |
| 2026-04-21 | commodity | WTI | 87.88 | +6.4% | USD/barrel | TradingEconomics / Investing.com [2026-04-21] | 2026-04-21T21:00:00-04:00 | ⚠️ 호르무즈 재봉쇄 반영. 4/23 만료 결렬 시 $95~100+ |
| 2026-04-21 | commodity | Brent | 96.25 | +6.5% | USD/barrel | TradingEconomics [2026-04-21] | 2026-04-21T21:00:00-04:00 | 전쟁 디스카운트 재확대 |
| 2026-04-21 | commodity | Gold | 4820 | -1.0%(추정) | USD/oz | Investing.com / LiteFinance [2026-04-21] | 2026-04-21T21:00:00-04:00 | 단기 숨고르기. $4800 지지선 유지. 구조적 Bull 기조 변화 없음 |
| 2026-04-21 | bond | US10Y | ~4.25 | -2bp | percent | Federal Reserve H.15 / TradingEconomics [2026-04-20 확인] | 2026-04-21T21:00:00-04:00 | ⚠️ 반등 추세 지속. 4.35% 분기점 |
| 2026-04-21 | bond | US2Y | ~3.81 | — | percent | 추정 [유지] | 2026-04-21T21:00:00-04:00 | — |
| 2026-04-21 | bond | Spread2Y10Y | ~+44 | — | bp | 계산값 (4.25%-3.81%) | 2026-04-21T21:00:00-04:00 | 정상 구간(비역전) |
| 2026-04-21 | crypto | BTC | 75242 | -2.7% | USD | CoinGecko / Fortune [2026-04-20~21] | 2026-04-21T09:00:00+09:00 | 호르무즈 리스크오프. $77K 안착 실패 |
| 2026-04-21 | crypto | ETH | 2309 | -4.7%(추정) | USD | CoinGecko [2026-04-20~21] | 2026-04-21T09:00:00+09:00 | — |
| 2026-04-21 | crypto | SOL | 85.51 | 소폭변동 | USD | Coinbase [2026-04-21] | 2026-04-21T09:00:00+09:00 | — |
| 2026-04-21 | crypto | TotalMarketCap | ~2.60T | -3.5% | USD | 추정 [2026-04-20~21] | 2026-04-21T09:00:00+09:00 | BTC 도미넌스 57.4% |
| 2026-04-21 | crypto | FearAndGreedIndex | 54 | — | index | CMC Fear&Greed [2026-04-21] | 2026-04-21T09:00:00+09:00 | Greed 전환. 극공포(21)→탐욕(54) 급전환. 신뢰도 낮음 |
| 2026-04-22 | us_index | SP500 | 7064.01 | -0.63% | point | Schwab Market Update / Yahoo Finance [2026-04-21 close] | 2026-04-22T09:00:00+09:00 | Warsh 청문+Apple CEO+이란 불확실 3중 압박. 장 후 Trump 무기한 휴전 연장 발표 |
| 2026-04-22 | us_index | NASDAQ | 24259.96 | -0.59% | point | Schwab Market Update / Yahoo Finance [2026-04-21 close] | 2026-04-22T09:00:00+09:00 | 동반 하락. 야간 선물(NQ1) +0.4% 반등 |
| 2026-04-22 | us_index | DJIA | 49149.38 | -0.59% | point | Schwab Market Update [2026-04-21 close] | 2026-04-22T09:00:00+09:00 | -293pt |
| 2026-04-22 | us_index | VIX | 17.48 | -7.9%(추정) | index | CNBC / TheStreet [2026-04-21 close 추정] | 2026-04-22T09:00:00+09:00 | 이란 무기한 휴전 연장으로 재하락. 18.98→17.48 |
| 2026-04-22 | asia_index | KOSPI | 6388.47 | +2.72% | point | CNBC Asia / IBTimes [2026-04-21 KST close] | 2026-04-22T09:00:00+09:00 | ⚠️ 사상 최고 종가 신기록. 전고점 6307.27(2026-02-26) 돌파. SK하이닉스 +4.97% 120만원 |
| 2026-04-22 | asia_index | Nikkei225 | 59349.17 | +0.89% | point | CNBC Asia [2026-04-21 JST close] | 2026-04-22T09:00:00+09:00 | AI주 강세. Topix -0.18% (섹터 차별화) |
| 2026-04-22 | asia_index | HangSeng | ~25991 | +0.35%(잠정) | point | CNBC Asia [2026-04-21 HKT 막판] | 2026-04-22T09:00:00+09:00 | 장 막판 소폭 상승 |
| 2026-04-22 | asia_index | ShanghaiCSI300 | 4768 | +0.22% | point | CNBC Asia [2026-04-21 CST close] | 2026-04-22T09:00:00+09:00 | GDP +5.0% 서프라이즈 여진 |
| 2026-04-22 | fx | USDKRW | 1477.8 | -0.39% | KRW | PoundSterlingLive / Bloomberg [2026-04-21] | 2026-04-22T09:00:00+09:00 | 원화 강세. KOSPI 신기록+외인 매수 복합 |
| 2026-04-22 | fx | DXY | 98.3 | +0.11pt | index | Investing.com / TradingEconomics [2026-04-21] | 2026-04-22T09:00:00+09:00 | 소폭 회복. 구조적 약세 기조 유지 |
| 2026-04-22 | commodity | WTI | 86.18 | -1.9%(추정) | USD/barrel | Investing.com [2026-04-22 아시아 장중] | 2026-04-22T09:00:00+09:00 | 이란 무기한 휴전 연장 반영. $87.88→$86 |
| 2026-04-22 | commodity | Gold | 4782.14 | -0.81% | USD/oz | TradingEconomics [2026-04-21] | 2026-04-22T09:00:00+09:00 | $4800 지지선 이탈. 단기 숨고르기 지속 |
| 2026-04-22 | bond | US10Y | ~4.25 | 0bp | percent | CNBC / TradingEconomics [2026-04-21] | 2026-04-22T09:00:00+09:00 | Warsh 독립성 발언 후 안정 |
| 2026-04-22 | bond | US2Y | ~3.81 | — | percent | 추정 | 2026-04-22T09:00:00+09:00 | — |
| 2026-04-22 | bond | Spread2Y10Y | ~+44 | — | bp | 계산값 | 2026-04-22T09:00:00+09:00 | 정상 구간 유지 |
| 2026-04-22 | crypto | BTC | 75900 | +0.9%(04-21 9AM ET) | USD | Fortune / LatestLY [2026-04-21] | 2026-04-22T09:00:00+09:00 | $76K 저항선 재도전 중 |
| 2026-04-22 | crypto | ETH | 2309 | 보합 | USD | CoinGecko 추정 | 2026-04-22T09:00:00+09:00 | — |
| 2026-04-22 | crypto | SOL | 85.51 | 보합 | USD | CoinGecko 추정 | 2026-04-22T09:00:00+09:00 | — |
| 2026-04-22 | crypto | FearAndGreedIndex | 33 | -21pt(54→33) | index | feargreedmeter.com / CoinMarketCap [2026-04-22] | 2026-04-22T09:00:00+09:00 | ⚠️ Greed→Fear 급전환. 1일 -21pt = 크립토 심리 급속 훼손 |
| 2026-04-22 | news | Apple_CEO | Tim_Cook_Retire | — | — | Apple Newsroom / TechCrunch [2026-04-20] | 2026-04-22T09:00:00+09:00 | Tim Cook 9/1 Executive Chairman 전환. John Ternus(하드웨어 엔지니어링 SVP) CEO 내정. AAPL AI 전략 불확실 단기 압박 |
| 2026-04-22 | news | Iran_Ceasefire | INDEFINITE_EXTENDED | — | — | Yahoo Finance / TheStreet [2026-04-21 AH] | 2026-04-22T09:00:00+09:00 | Trump 이란 무기한 휴전 연장 발표(장 후). 이란 내부 분열로 협상 시간 필요. WTI 하락. ES1 +0.2% |
| 2026-04-22 | news | Warsh_Hearing | COMPLETED_INDEPENDENT | — | — | CNBC / CNN / PBS [2026-04-21] | 2026-04-22T09:00:00+09:00 | "독립성 필수"·"꼭두각시 아님". Tillis 반대(DOJ Powell수사 연계)로 인준 지연. 시장 안도 |
| 2026-04-22 | calendar | TSLA_Q1 | TBD | — | — | Benzinga / Electrek [예정] | 2026-04-22T09:00:00+09:00 | 04-22 장 후 발표. EPS 컨센 $0.33~$0.37. 인도 358K(컨센 miss). VIX 방향 결정자 |
| 2026-04-23 | us_index | SP500 | 7137.90 | +1.05% | point | Yahoo Finance / TheStreet [2026-04-22 close 확정] | 2026-04-23T09:00:00+09:00 | 사상 최고치 경신. 이란 휴전 연장 + TSLA Beat 기대. 반도체 주도 |
| 2026-04-23 | us_index | NASDAQ | 24657.57 | +1.64% | point | Yahoo Finance / TheStreet [2026-04-22 close 확정] | 2026-04-23T09:00:00+09:00 | 사상 최고치 경신. 반도체 섹터 주도 |
| 2026-04-23 | us_index | DJIA | 49490.03 | +0.69% | point | Yahoo Finance / TheStreet [2026-04-22 close 확정] | 2026-04-23T09:00:00+09:00 | +340.65pt |
| 2026-04-23 | us_index | Russell2000 | 미확인 | +0.82% | point | 24/7 Wall St. [2026-04-22] | 2026-04-23T09:00:00+09:00 | 소형주 리스크온 동참 |
| 2026-04-23 | us_index | VIX | ~20 | 소폭상승 추정 | index | 추정 [2026-04-22] | 2026-04-23T09:00:00+09:00 | WTI $92.96 급등 → 인플레 우려 반영. 정확 수치 미수집 |
| 2026-04-23 | asia_index | KOSPI | 6374.46 | -0.22% | point | CNBC Asia / FreePressJournal [2026-04-22 KST close] | 2026-04-23T09:00:00+09:00 | 전일 사상 최고(6388.47) 후 차익실현 |
| 2026-04-23 | asia_index | KOSDAQ | 미확인 | +0.18% | point | CNBC Asia [2026-04-22] | 2026-04-23T09:00:00+09:00 | 소폭 반등 |
| 2026-04-23 | asia_index | Nikkei225 | 59653.56 | +0.50% | point | CNBC Asia / FreePressJournal [2026-04-22 JST close] | 2026-04-23T09:00:00+09:00 | 미국 선물 강세 반영 |
| 2026-04-23 | asia_index | HangSeng | 미확인 | -1.19% | point | CNBC Asia [2026-04-22 HKT close] | 2026-04-23T09:00:00+09:00 | 유가 급등 인플레 우려 |
| 2026-04-23 | asia_index | ShanghaiCSI300 | 4799.62 | +0.66% | point | CNBC Asia [2026-04-22 CST close] | 2026-04-23T09:00:00+09:00 | 중국 내수 회복 기대 지속 |
| 2026-04-23 | fx | USDKRW | 1479.36 | -0.23% | KRW | PoundSterlingLive / Bloomberg [2026-04-22] | 2026-04-23T09:00:00+09:00 | 소폭 원화 강세. 1400 초과 지속 |
| 2026-04-23 | fx | DXY | ~98~99 추정 | 소폭상승추정 | index | 미수집 (추정) | 2026-04-23T09:00:00+09:00 | 유가 급등 + 미국 지수 신고가 복합. 정확 수치 미수집 |
| 2026-04-23 | commodity | WTI | 92.96 | +5.78(추정+3%+) | USD/barrel | Fortune / CNBC [2026-04-22 close 확정] | 2026-04-23T09:00:00+09:00 | ⚠️ 이란 호르무즈 선박 2척 나포 — 봉쇄 지속. $86→$92.96 급등 |
| 2026-04-23 | commodity | Brent | 101.91 | +3%+ | USD/barrel | CNBC / Oneindia [2026-04-22 close 확정] | 2026-04-23T09:00:00+09:00 | ⚠️ $100 돌파. 역사상 최대 공급 붕괴 지속 |
| 2026-04-23 | commodity | Gold | 4752.76 | +0.68% | USD/oz | RoboForex / Investing.com [2026-04-22] | 2026-04-23T09:00:00+09:00 | 이란 불확실 + 탈달러 수요 구조적 지지 |
| 2026-04-23 | bond | US10Y | ~4.30 | +5bp | percent | TradingEconomics / CNBC [2026-04-22] | 2026-04-23T09:00:00+09:00 | 유가 급등 → 인플레 기대 재상승. 4.25%→4.30% |
| 2026-04-23 | bond | US2Y | ~3.80 | — | percent | 추정 | 2026-04-23T09:00:00+09:00 | — |
| 2026-04-23 | bond | Spread2Y10Y | ~+50 | — | bp | 계산값 (4.30%-3.80%) | 2026-04-23T09:00:00+09:00 | 정상 구간(비역전) |
| 2026-04-23 | crypto | BTC | ~75640~78597 | 소폭변동 | USD | SpotedCrypto / CoinMarketCap [2026-04-22] | 2026-04-23T09:00:00+09:00 | $76K 저항선 구간 유지. 소스별 편차 |
| 2026-04-23 | crypto | ETH | ~2300 | 보합 추정 | USD | 추정 | 2026-04-23T09:00:00+09:00 | — |
| 2026-04-23 | crypto | SOL | ~80 | 소폭하락 추정 | USD | 추정 | 2026-04-23T09:00:00+09:00 | — |
| 2026-04-23 | crypto | TotalMarketCap | ~2.63T | — | USD | CoinMarketCap [2026-04-22] | 2026-04-23T09:00:00+09:00 | BTC 도미넌스 ~57.5% |
| 2026-04-23 | crypto | FearAndGreedIndex | 33 | 보합 | index | SpotedCrypto [2026-04-22] | 2026-04-23T09:00:00+09:00 | Fear 구간 안착. 59일 극단공포 탈출 후 Fear 구간 |
| 2026-04-23 | news | TSLA_Q1_Result | EPS_0.41_Beat | — | — | Electrek / CNBC / Investing.com [2026-04-22 AH] | 2026-04-23T09:00:00+09:00 | EPS $0.41(컨센 $0.37 Beat +10.8%), Rev $22.387B Beat, 마진 21.1%(+478bp). AH 초기+4%→Capex $25B 가이던스 후 +0.4% 수렴 |
| 2026-04-23 | news | Iran_Hormuz_Seizure | SHIPS_SEIZED_BLOCKADE_CONTINUES | — | — | NBC News / CNBC / Al Jazeera [2026-04-22] | 2026-04-23T09:00:00+09:00 | 이란 호르무즈 선박 2척 추가 나포. 휴전 연장에도 봉쇄 사실상 지속. WTI $92.96 급등 트리거 |
| 2026-04-24 | us_index | SP500 | 7108.40 | -0.41% | point | TheStreet / Yahoo Finance [2026-04-23 close] | 2026-04-24T09:00:00+09:00 | 소프트웨어 AI 충격(IBM -10.3%, ServiceNow -18%) 주도 조정. 사상 최고(7137.90) 대비 -0.41% |
| 2026-04-24 | us_index | NASDAQ | 24438.50 | -0.89% | point | TheStreet / Yahoo Finance [2026-04-23 close] | 2026-04-24T09:00:00+09:00 | 소프트웨어 섹터 전면 매도. TI +10% 반도체는 반등 |
| 2026-04-24 | us_index | DJIA | 49310.32 | -0.36% | point | TheStreet / Yahoo Finance [2026-04-23 close] | 2026-04-24T09:00:00+09:00 | -179.71pt |
| 2026-04-24 | us_index | Russell2000 | 미확인 | -0.98% | point | Investrade.com [2026-04-23] | 2026-04-24T09:00:00+09:00 | 소형주 낙폭 확대 |
| 2026-04-24 | us_index | VIX | ~20 | 소폭상승 | index | CNBC / Investrade [2026-04-23 추정] | 2026-04-24T09:00:00+09:00 | ⚠️ 20선 재근접. 소프트웨어 AI 불안 + 유가 상승 복합 |
| 2026-04-24 | asia_index | KOSPI | 6475.81 | +0.90% | point | TradingView / CNBC Asia [2026-04-23 KST close] | 2026-04-24T09:00:00+09:00 | 아시아 최강세. 반도체 + Q1 GDP 서프라이즈 기대 |
| 2026-04-24 | asia_index | KOSDAQ | 1174.31 | -0.58% | point | CNBC Asia [2026-04-23 KST close] | 2026-04-24T09:00:00+09:00 | 소형주 약세. KOSPI와 대비 |
| 2026-04-24 | asia_index | Nikkei225 | 59140.23 | -0.75% | point | CNBC Asia [2026-04-23 JST close] | 2026-04-24T09:00:00+09:00 | 소프트웨어 충격 반영 |
| 2026-04-24 | asia_index | HangSeng | 25915.20 | -0.95% | point | CNBC Asia / SCMP [2026-04-23 HKT close] | 2026-04-24T09:00:00+09:00 | 지정학 + 소프트웨어 이중 악재 |
| 2026-04-24 | asia_index | ShanghaiCSI300 | 4786.33 | -0.28% | point | SCMP / CNBC Asia [2026-04-23 CST close] | 2026-04-24T09:00:00+09:00 | 상대적 방어 |
| 2026-04-24 | fx | USDKRW | 1480.51 | +0.12% | KRW | PoundSterlingLive / TradingEconomics [2026-04-23] | 2026-04-24T09:00:00+09:00 | 소폭 원화 약세. 1400 초과 지속 |
| 2026-04-24 | fx | DXY | 98.725 | 소폭강세 | index | TradingEconomics / Gurufocus [2026-04-23] | 2026-04-24T09:00:00+09:00 | 이란 교착 → 안전자산 달러. 1주일래 고점 |
| 2026-04-24 | fx | EURUSD | 1.1698 | -0.06% | USD | PoundSterlingLive / TradingEconomics [2026-04-23] | 2026-04-24T09:00:00+09:00 | 달러 소폭 강세에 유로 약세 |
| 2026-04-24 | fx | USDJPY | 159.721 | +0.23% | JPY | PoundSterlingLive [2026-04-23] | 2026-04-24T09:00:00+09:00 | ⚠️ 엔화 약세 지속. BOJ 불확실 |
| 2026-04-24 | commodity | WTI | 94.14 | +1.26% | USD/barrel | TradingEconomics / FXDailyReport [2026-04-23 close] | 2026-04-24T09:00:00+09:00 | ⚠️ 4연속 상승. 이란 협상 교착. $95 근접 |
| 2026-04-24 | commodity | Brent | 103.38 | +1.44% | USD/barrel | Oneindia / Angle360ng [2026-04-23 close] | 2026-04-24T09:00:00+09:00 | ⚠️ $103 유지. 공급 위기 구조화 |
| 2026-04-24 | commodity | Gold | 4738.53 | -0.02% | USD/oz | Investing.com / Babypips [2026-04-23 close] | 2026-04-24T09:00:00+09:00 | 소폭 조정. DXY 98.7 강세에 단기 역풍. 구조적 Bull 유지 |
| 2026-04-24 | bond | US10Y | 4.30 | 0bp | percent | Federal Reserve H.15 / TradingEconomics [2026-04-23] | 2026-04-24T09:00:00+09:00 | 보합. 소프트웨어 충격 → 채권 안전자산 수요 상쇄 |
| 2026-04-24 | bond | US2Y | ~3.81 | +0bp | percent | TradingEconomics / FRED DGS2 [2026-04-22~23 추정] | 2026-04-24T09:00:00+09:00 | 04-22 3.81% 기준 |
| 2026-04-24 | bond | Spread2Y10Y | +49 | 계산값 | bp | 계산값 (4.30%-3.81%) | 2026-04-24T09:00:00+09:00 | 정상 구간(비역전) 유지 |
| 2026-04-24 | crypto | BTC | ~77900 | 보합~소폭상승 | USD | BlockchainMagazine / SpotedCrypto [2026-04-23] | 2026-04-24T09:00:00+09:00 | $77K 안착. 소프트웨어 충격에도 탈동조화 |
| 2026-04-24 | crypto | ETH | 2399 | +3.83% | USD | SpotedCrypto [2026-04-23] | 2026-04-24T09:00:00+09:00 | 알트코인 반등 선도 |
| 2026-04-24 | crypto | SOL | 미확인 | 소폭조정 | USD | 미수집 [KelpDAO 해킹 영향] | 2026-04-24T09:00:00+09:00 | $292M KelpDAO 해킹(북한 Lazarus) — SOL DeFi 리스크 부각 |
| 2026-04-24 | crypto | TotalMarketCap | ~2.71T | 소폭상승 | USD | SpotedCrypto / CoinMarketCap [2026-04-23] | 2026-04-24T09:00:00+09:00 | BTC 도미넌스 58.1% |
| 2026-04-24 | crypto | FearAndGreedIndex | 32~46 | 소폭개선 | index | 소스별 차이 [2026-04-23] | 2026-04-24T09:00:00+09:00 | Fear 구간 유지. 기관 ETF 수요가 하방 지지 |
| 2026-04-24 | crypto | BTC_ETF_Inflow_Daily | 335.8M | — | USD | TheBlock / CoinReporter [2026-04-23] | 2026-04-24T09:00:00+09:00 | 7거래일 연속 순유입. IBIT ~809,870 BTC(62% 점유). 7일 누계 $1.9B |
| 2026-04-24 | news | IBM_Q1_Result | EPS_1.91_Beat_Stock-10pct | — | — | CNBC / Benzinga [2026-04-23 AH] | 2026-04-24T09:00:00+09:00 | EPS $1.91(컨센 $1.81 Beat), Rev $15.92B(+9% YoY Beat). AI 성장 둔화 우려 → 주가 -10.3%. AI 불안 소프트웨어 섹터 매도 트리거 |
| 2026-04-24 | news | ServiceNow_Selloff | STOCK-18pct_AI_FEAR | — | — | CNBC / Yahoo Finance [2026-04-23] | 2026-04-24T09:00:00+09:00 | Beat에도 AI 대체 공포 + 이란 가이던스 → -18% 역대 최대. Salesforce -9.4%, Oracle -6%, Workday -9%, Adobe -7.4% 동반 |
| 2026-04-24 | news | Korea_Q1_GDP | PLUS1.7pct_5yr_HIGH | — | — | Korea Times / CNBC / RTTNews [2026-04-24 BOK 발표] | 2026-04-24T09:00:00+09:00 | +1.7% q/q (컨센 +0.9% 대비 +0.8%p 서프라이즈). 5.5년래 최고. 반도체 수출 +5.1% q/q 주도. YoY +3.6% |
| 2026-04-25 | us_index | SP500 | 7121 | +0.18% | point | Yahoo Finance / TheStreet [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | 신고가 경신. 반도체 AI 인프라 랠리(Intel Q1 +2800%) |
| 2026-04-25 | us_index | NASDAQ | ~24837 | +1.60% | point | Yahoo Finance [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | 신고가. Nvidia $5조 재탈환. Philly Sox 18일 연승(역대 최장) |
| 2026-04-25 | us_index | DJIA | 49230.71 | -0.16% | point | StockMarketWatch [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | -79.61pt. 반도체 집중도 낮은 전통 섹터 약세 |
| 2026-04-25 | us_index | Russell2000 | 미확인 | +0.65%추정 | point | Yahoo Finance 추정 [2026-04-24] | 2026-04-25T09:00:00+09:00 | 소형주 반등. 정확값 미수집 |
| 2026-04-25 | us_index | VIX | 18.63 | -3.52% | index | Yahoo Finance [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | 공포 완화. 단 18선 = 완전 안정 아님. FOMC 4/28-29 대기 |
| 2026-04-25 | asia_index | KOSPI | 6475.63 | flat | point | CNBC Asia [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | 전일 +0.90% 강세 후 숨고르기 |
| 2026-04-25 | asia_index | KOSDAQ | 1203.84 | +2.51% | point | CNBC Asia [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | 급반등. 바이오·소형기술주 강세 전환 |
| 2026-04-25 | asia_index | Nikkei225 | 59435 | +0.50% | point | TradingEconomics [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | 반도체 랠리 + 엔화 약세 방어막 |
| 2026-04-25 | asia_index | HangSeng | 미확인 | -0.16% | point | CNBC Asia [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | 소폭 하락. 이란 리스크 + 중국 모멘텀 부재 |
| 2026-04-25 | asia_index | CSI300 | 4769.37 | -0.35% | point | CNBC Asia [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | 중국 경기 모멘텀 단기 약화 |
| 2026-04-25 | fx | DXY | ~98.8 | 소폭강세 | index | TradingEconomics [2026-04-24] | 2026-04-25T09:00:00+09:00 | 이란 교착 안전자산 달러 수요. 주간 3주 만에 첫 상승 |
| 2026-04-25 | fx | USDKRW | 1475.19 | -0.44% | KRW | TradingEconomics [2026-04-24] | 2026-04-25T09:00:00+09:00 | 원화 강세. 한국 Q1 GDP 서프라이즈 + 반도체 수출 호조 반영 |
| 2026-04-25 | fx | USDJPY | 159.815 | +0.07% | JPY | TradingEconomics [2026-04-24] | 2026-04-25T09:00:00+09:00 | 엔화 약세 지속. BOJ 정책 불확실 |
| 2026-04-25 | commodity | WTI | 96.07 | 추정+2.05% | USD/barrel | Oneindia / Fortune [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | ⚠️ 5연속 상승. 트럼프 기뢰 격침 명령 + 이란 기뢰 미해제. $95 돌파 |
| 2026-04-25 | commodity | Brent | 105.63 | 추정+2.17% | USD/barrel | Oneindia [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | ⚠️ $105 돌파. 공급 리스크 구조화 |
| 2026-04-25 | commodity | Gold | 4723.60 | +0.54% | USD/oz | TradingEconomics [2026-04-24 close] | 2026-04-25T09:00:00+09:00 | $4,700 지지 재확인. 탈달러 구조적 수요 유지 |
| 2026-04-25 | bond | US10Y | 4.31 | +1bp | percent | Advisor Perspectives / TradingEconomics [2026-04-24] | 2026-04-25T09:00:00+09:00 | PMI Beat + 유가 상승 인플레 우려 소폭 반영 |
| 2026-04-25 | bond | US2Y | 3.78 | -3bp | percent | Advisor Perspectives / TradingEconomics [2026-04-24] | 2026-04-25T09:00:00+09:00 | 단기 인하 기대 소폭 유지 |
| 2026-04-25 | bond | Spread2Y10Y | +53 | — | bp | 계산값(4.31%-3.78%) | 2026-04-25T09:00:00+09:00 | 정상 구간(비역전) 유지. 전일 +49bp 대비 확대 |
| 2026-04-25 | crypto | BTC | ~78126 | 소폭상승 | USD | Yahoo Finance / CoinDesk [2026-04-24] | 2026-04-25T09:00:00+09:00 | $78K 안착. ETF 8일 연속 순유입. 탈동조화 유지 |
| 2026-04-25 | crypto | ETH | ~2352 | — | USD | Yahoo Finance [2026-04-24] | 2026-04-25T09:00:00+09:00 | $2,300선 지지 확인 |
| 2026-04-25 | crypto | SOL | ~85.95 | — | USD | Coinbase / Yahoo Finance [2026-04-24] | 2026-04-25T09:00:00+09:00 | KelpDAO 해킹 후 회복세 |
| 2026-04-25 | crypto | BTC_ETF_Monthly | 2.43B | — | USD | Invezz / CoinDesk [2026-04-24] | 2026-04-25T09:00:00+09:00 | 4월 누계 $2.43B(8일 연속). 3월 $1.32B 대비 +84%. IBIT 809,870 BTC |
| 2026-04-25 | crypto | FearAndGreedIndex | 39~60 | — | index | 소스별 차이 [2026-04-24] | 2026-04-25T09:00:00+09:00 | Fear→Neutral 전환 구간. 소스별 방법론 차이 |
| 2026-04-25 | calendar | USFlashPMI_Apr | Composite_52.0 | — | index | S&P Global [2026-04-24 발표] | 2026-04-25T09:00:00+09:00 | Beat 컨센 50.6. Mfg 54.0 / Svcs 51.3. Q2 모멘텀 확인. 단 입력비용 인플레 가속 경고 |
| 2026-04-25 | calendar | JoblessClaims_Apr18wk | 214000 | +6K | count | US DOL [2026-04-24 발표] | 2026-04-25T09:00:00+09:00 | 주간종료 4/18. 컨센 212K 소폭 상회. 계속청구 1,821K(+12K). 구조적 저실업 유지 |
| 2026-04-25 | news | Intel_Q1_Result | EPS_0.29_Beat2800pct | — | — | BusinessWire / Yahoo Finance [2026-04-23 AH] | 2026-04-25T09:00:00+09:00 | EPS $0.29(컨센 $0.01 대비 +2,800%). Rev $13.58B(컨센 $12.42B). INTC +24% $82.57. Philly Sox 18일 연승(역대 최장) |
| 2026-04-25 | news | GDP_Q1_Advance_Schedule | PENDING_APR30 | — | — | BEA.gov [공식 일정] | 2026-04-25T09:00:00+09:00 | GDP Q1 Advance + Core PCE 3월 모두 4/30 발표 예정. 4/25 발표 없음(당초 예상 오류 정정) |
| 2026-04-26 | us_index | SP500 | 7165.08 | +0.80% | point | NewsTribune / Jefferson City News-Tribune [2026-04-25 close] | 2026-04-26T09:00:00+09:00 | 신고가 재경신. 이란 평화회담 파키스탄 중재 기대 + 반도체 랠리 지속 |
| 2026-04-26 | us_index | NASDAQ | 24836.60 | +1.63% | point | NewsTribune [2026-04-25 close] | 2026-04-26T09:00:00+09:00 | 신고가. 주간 +1.5% |
| 2026-04-26 | us_index | DJIA | 49231 | +0.00% | point | NewsTribune [2026-04-25 close] | 2026-04-26T09:00:00+09:00 | 보합. 비기술 섹터 횡보. 주간 -0.4% |
| 2026-04-26 | us_index | Russell2000 | 2787 | +0.43% | point | Yahoo Finance [2026-04-24 close — 04-25 동기준] | 2026-04-26T09:00:00+09:00 | 소형주 동반 상승. 리스크온 |
| 2026-04-26 | us_index | VIX | ~18.71 | 소폭상승 | index | Yahoo Finance [2026-04-25 추정] | 2026-04-26T09:00:00+09:00 | ⚠️ 18선 대. FOMC 4/28-29 + GDP/PCE 4/30 이중 이벤트 대기 |
| 2026-04-26 | asia_index | KOSPI | ~6476 | 보합 | point | Korea Times / Seoul Economic Daily [2026-04-25] | 2026-04-26T09:00:00+09:00 | 소매투자자 KOSDAQ ETF→KOSPI 전환 흐름 |
| 2026-04-26 | asia_index | KOSDAQ | ~1204 | 고점권 | point | Seoul Economic Daily [2026-04-25] | 2026-04-26T09:00:00+09:00 | 2000년 8월 이후 최고. 닷컴버블 피크 1238.80 근접 |
| 2026-04-26 | asia_index | Nikkei225 | 59716 | +0.97% | point | CNBC Asia [2026-04-24 close] | 2026-04-26T09:00:00+09:00 | 반도체 랠리 + 엔화 약세 방어막. 60,000 목전 |
| 2026-04-26 | asia_index | HangSeng | 25978 | +0.24% | point | CNBC Asia [2026-04-24 close] | 2026-04-26T09:00:00+09:00 | 이란 협상 기대 소폭 반등 |
| 2026-04-26 | asia_index | ShanghaiComposite | ~4074 | -0.45% | point | CNBC Asia [2026-04-24 close] | 2026-04-26T09:00:00+09:00 | 중국 내수 모멘텀 단기 약화 |
| 2026-04-26 | fx | DXY | ~98.51 | 소폭약세 | index | TradingEconomics [2026-04-25] | 2026-04-26T09:00:00+09:00 | 이란 협상 기대 안전자산 수요 소폭 감소 |
| 2026-04-26 | fx | USDKRW | ~1476.67 | +1.48원 | KRW | PoundSterlingLive [2026-04-25] | 2026-04-26T09:00:00+09:00 | ⚠️ 1,400 초과. 1,475~1,480 구간 |
| 2026-04-26 | fx | EURUSD | ~1.1813 | 소폭강세 | USD | forex.com [2026-04-25] | 2026-04-26T09:00:00+09:00 | DXY 약세 반영. 주요 기술적 피벗 |
| 2026-04-26 | fx | USDJPY | ~159~160 | 횡보 | JPY | forex.com [2026-04-25] | 2026-04-26T09:00:00+09:00 | ⚠️ 엔화 약세 지속. 160 재진입 여부 관전 |
| 2026-04-26 | commodity | WTI | 94.88 | -1.24% | USD/barrel | Angle360ng / FXStreet [2026-04-25] | 2026-04-26T09:00:00+09:00 | ⚠️ 이란 평화회담 기대 하락. $96.07→$94.88. 주간 +14%. 협상 타결 시 $80~85 |
| 2026-04-26 | commodity | Brent | ~104.4 | 소폭하락 | USD/barrel | CNBC [2026-04-25] | 2026-04-26T09:00:00+09:00 | ⚠️ $104 유지. 협상 기대 반영 하락 |
| 2026-04-26 | commodity | Gold | ~4708.8 | -0.33% | USD/oz | Vietnam.vn / Barchart [2026-04-25 주말 기준] | 2026-04-26T09:00:00+09:00 | $4,700 지지선 재테스트. 주간 -2% 조정. 구조적 Bull 유지 |
| 2026-04-26 | commodity | Copper | ~5.61 | — | USD/lbs | CME Group [2026-04-25] | 2026-04-26T09:00:00+09:00 | -7.4% MoM. 글로벌 성장 우려 + 거래소 재고 증가 |
| 2026-04-26 | commodity | NaturalGas | ~2.52~2.56 | -3.6% | USD/MMBtu | TradingEconomics [2026-04-25] | 2026-04-26T09:00:00+09:00 | 2024년 10월 이후 최저. 온화한 날씨 + 저장 강건 |
| 2026-04-26 | bond | US10Y | ~4.33 | +2bp | percent | TradingEconomics / CNBC [2026-04-25] | 2026-04-26T09:00:00+09:00 | 리스크온 → 채권 소폭 매도. 4.35% 분기점 |
| 2026-04-26 | bond | US2Y | ~3.79 | +1bp | percent | TradingEconomics [2026-04-25] | 2026-04-26T09:00:00+09:00 | 보합~소폭 상승 |
| 2026-04-26 | bond | Spread2Y10Y | ~+54 | — | bp | 계산값(4.33%-3.79%) | 2026-04-26T09:00:00+09:00 | 정상 구간(비역전) 유지 |
| 2026-04-26 | crypto | BTC | ~77510~77779 | -0.57% | USD | CoinCodex [2026-04-25 주말] | 2026-04-26T09:00:00+09:00 | 주말 소폭 조정. 고래 270K BTC 월간 누적(2013년 이후 최대). 거래소 7년래 최저 |
| 2026-04-26 | crypto | ETH | 추정~2330~2350 | 소폭조정 | USD | 추정 [2026-04-25] | 2026-04-26T09:00:00+09:00 | $2,300선 지지 확인 |
| 2026-04-26 | crypto | SOL | 추정~85~86 | 보합 | USD | 추정 [2026-04-25] | 2026-04-26T09:00:00+09:00 | KelpDAO 해킹 후 회복세 유지 |
| 2026-04-26 | crypto | TotalMarketCap | ~2.58T | -0.07% | USD | CoinCodex [2026-04-25] | 2026-04-26T09:00:00+09:00 | BTC 도미넌스 ~58% |
| 2026-04-26 | news | Iran_PeaceTalks_Pakistan | ISLAMABAD_DIPLOMACY | — | — | CNBC / NewsTribune [2026-04-25] | 2026-04-26T09:00:00+09:00 | 이란 외교장관 아라그치 이슬라마바드 방문. 트럼프 특사 위트코프·쿠슈너 토요일 출발. WTI 리스크 프리미엄 소폭 해소 |
| 2026-04-26 | calendar | FOMC_Apr28-29 | HOLD_100pct | — | — | CME FedWatch / Kraken Blog [2026-04-25] | 2026-04-26T09:00:00+09:00 | 동결 100% 컨센서스. 파월 성명 톤 변화(closely monitoring) 여부 40% 확률이 핵심 |
| 2026-04-26 | calendar | BigTech_Earnings_Apr29 | MSFT_META_AMZN_GOOGL_QCOM | — | — | CNBC / Schwab [2026-04-25] | 2026-04-26T09:00:00+09:00 | 4/29 수요일 장후 동시 발표. MSFT EPS 컨센 $4.05(+17%)/Rev $81.37B. META EPS 컨센 $6.65/Rev $55.5B |
| 2026-04-26 | calendar | GDP_CorePCE_Apr30 | PENDING_08:30ET | — | — | BEA / TradingEconomics [2026-04-25] | 2026-04-26T09:00:00+09:00 | GDP Q1 Advance GDPNow +1.24%(04-21). Core PCE 3월 컨센 ~3.0%. 4/30 08:30 ET |
| 2026-04-26 | calendar | ECB_Apr30 | 25bp_CUT_CONSENSUS | — | — | CMC Markets [2026-04-25] | 2026-04-26T09:00:00+09:00 | 4/30 ECB 25bp 인하 컨센서스. Brent $104+ 에너지 인플레 변수 잔존 |
| 2026-04-26 | calendar | Apple_Earnings_Apr30 | AAPL_Q2FY26_PLUS_LLY_CAT | — | — | Schwab / CNBC [2026-04-25] | 2026-04-26T09:00:00+09:00 | 4/30 장후 AAPL Q2 FY26(Tim Cook 마지막 주요 발표). AI 전략 가이던스 관전 |
| 2026-04-27 | us_index | SP500_close_Apr25 | 7165.8 | +0.80% | point | CNBC / TheStreet [2026-04-25 close 확정] | 2026-04-27T09:00:00+09:00 | 신고가 재경신. 이란 협상 기대(취소 전) + Intel +24% + SOX 18일 연승 |
| 2026-04-27 | us_index | NASDAQ_close_Apr25 | 24837 | +1.60% | point | CNBC / TheStreet [2026-04-25 close 확정] | 2026-04-27T09:00:00+09:00 | 신고가. 반도체·기술주 주도. 주간 +1.5% |
| 2026-04-27 | us_index | DJIA_close_Apr25 | 49231 | -0.20% | point | CNBC / TheStreet [2026-04-25 close 확정] | 2026-04-27T09:00:00+09:00 | 보합~소폭 하락. 주간 -0.4% |
| 2026-04-27 | us_index | Russell2000_close_Apr25 | 2787 | +0.43% | point | Yahoo Finance [2026-04-25] | 2026-04-27T09:00:00+09:00 | 소형주 동반 상승 |
| 2026-04-27 | us_index | SOX_close_Apr24 | 10513.66 | +4.32% | point | Gurufocus / jianshiapp [2026-04-24 close] | 2026-04-27T09:00:00+09:00 | SOX 18거래일 연속 상승 역대 최장(1992년 이후). 200일선 편차 2000년 6월 이후 최고 = 단기 과매수 |
| 2026-04-27 | us_index | VIX_close_Apr25 | 18.71 | 소폭상승 | index | Yahoo Finance / CBOE [2026-04-25] | 2026-04-27T09:00:00+09:00 | ⚠️ 18선 대. FOMC 4/28-29 + GDP/PCE 4/30 이중 이벤트 대기 |
| 2026-04-27 | asia_index | Nikkei225 | 60537 | +1.38% | point | CNBC Asia [2026-04-27 종가] | 2026-04-27T16:00:00+09:00 | 역대 신고가. 60,000선 돌파 확인. 반도체·기술주 주도 |
| 2026-04-27 | asia_index | KOSPI | 6615.03 | +2.15% | point | CNBC Asia [2026-04-27 종가] | 2026-04-27T16:00:00+09:00 | 신고가 재경신. 반도체·방산 외인 매수 강세. 4월 글로벌 최강 수익률 |
| 2026-04-27 | asia_index | KOSDAQ_Apr25 | 1203.84 | +2.51% | point | AsiaBusinessDaily / CNBC Asia [2026-04-25 close] | 2026-04-27T09:00:00+09:00 | 25년래 최고. 2000년 닷컴버블 피크 1,238.80 근접 |
| 2026-04-27 | asia_index | HangSeng | 미확인 | -0.24% | point | CNBC Asia [2026-04-27 막판] | 2026-04-27T16:30:00+08:00 | 이란 협상 불확실 + 중국 모멘텀 부재 소폭 하락 |
| 2026-04-27 | asia_index | CSI300 | 4770.95 | 보합 | point | CNBC Asia [2026-04-27] | 2026-04-27T16:00:00+08:00 | 보합 |
| 2026-04-27 | asia_index | SENSEX | 79664 | +639(+0.82%) | point | Business Standard [2026-04-27 종가] | 2026-04-27T16:00:00+05:30 | 이란 신제안(호르무즈 재개방 조건) 기대 반등. 전일 76,664(-1.3%) 회복 |
| 2026-04-27 | fx | DXY | ~98.8 | 소폭강세 | index | AhaSignals / CNBC [2026-04-25 / 04-27] | 2026-04-27T09:00:00+09:00 | 이란 협상 결렬 → 안전자산 달러 소폭 반등. 구조적 약세 기조 유지 |
| 2026-04-27 | fx | USDKRW | ~1476.67 | 소폭변동 | KRW | PoundSterlingLive [2026-04-25] | 2026-04-27T09:00:00+09:00 | ⚠️ 1,400 초과 지속. KOSPI 신고가 → 외인 매수 → 1,470 방향 압력 |
| 2026-04-27 | fx | EURUSD | ~1.1729 | 소폭약세 | USD | Goodreturns / forex.com [2026-04-27] | 2026-04-27T09:00:00+09:00 | DXY 소폭 강세에 유로 약세 |
| 2026-04-27 | commodity | WTI | ~95~96 | 재급등+1~2% | USD/barrel | FXDailyReport / TheStreet [2026-04-27] | 2026-04-27T09:00:00+09:00 | ⚠️ 이란 협상 결렬(트럼프 위트코프·쿠슈너 방문 취소) → 재급등. 이란 신제안 보도로 $86→$95~96 변동성 |
| 2026-04-27 | commodity | Brent | ~107 | +3%이상 | USD/barrel | CNBC / Bloomberg [2026-04-27] | 2026-04-27T09:00:00+09:00 | ⚠️ $107 돌파. IEA "역대 최대 에너지 공급 충격" 경고 |
| 2026-04-27 | commodity | Gold | 4726.11 | +0.4%추정 | USD/oz | GoodReturns / BullionVault [2026-04-27 03:55 ET] | 2026-04-27T09:00:00+09:00 | $4,700선 회복. 이란 불확실 안전자산 수요 |
| 2026-04-27 | commodity | Silver | 76.47 | 소폭상승 | USD/oz | TradingEconomics [2026-04-27] | 2026-04-27T09:00:00+09:00 | $76선 회복. Gold 동조 |
| 2026-04-27 | bond | US10Y_Apr25 | 4.33 | +2bp | percent | Fed H.15 / TradingEconomics [2026-04-25] | 2026-04-27T09:00:00+09:00 | 5연속 상승. 이란 결렬 시 4.35%+ 가능 |
| 2026-04-27 | bond | US2Y_Apr22 | 3.789 | 참조 | percent | Fed H.15 [2026-04-22] | 2026-04-27T09:00:00+09:00 | 최신 확정값 04-22 기준 |
| 2026-04-27 | bond | US30Y_Apr22 | 4.927 | 참조 | percent | Fed H.15 [2026-04-22] | 2026-04-27T09:00:00+09:00 | 최신 확정값 04-22 기준 |
| 2026-04-27 | bond | Spread2Y10Y | ~+54 | — | bp | 계산값(4.33%-3.789%) | 2026-04-27T09:00:00+09:00 | 정상 구간(비역전) 유지 |
| 2026-04-27 | crypto | BTC | 79123.77 | +2.04% | USD | CoinGabbar [2026-04-27] | 2026-04-27T09:00:00+09:00 | $79K 돌파. 이란 재불확실에도 독립 강세 유지. ETF 연속 순유입 |
| 2026-04-27 | crypto | ETH | 2388.39 | +3.04% | USD | CoinGabbar [2026-04-27] | 2026-04-27T09:00:00+09:00 | $2,400 재도전 중 |
| 2026-04-27 | crypto | SOL | 87 | +1.96% | USD | CoinGabbar [2026-04-27] | 2026-04-27T09:00:00+09:00 | KelpDAO 해킹 여파 회복 완료 |
| 2026-04-27 | crypto | TotalMarketCap | 2.71T | +1.7% | USD | CoinGabbar [2026-04-27] | 2026-04-27T09:00:00+09:00 | BTC 도미넌스 58.2% / ETH 10.6% |
| 2026-04-27 | crypto | FearAndGreedIndex | 47 | +14pt(33→47) | index | alternative.me / CoinGabbar [2026-04-27] | 2026-04-27T09:00:00+09:00 | Neutral 전환. Fear→Neutral 2일 만에 회복. 주간 29→47 큰 폭 개선 |
| 2026-04-27 | news | Iran_Talks_STALLED | TRUMP_CANCELS_PAKISTAN | — | — | WashingtonPost / Bloomberg / NPR [2026-04-25] | 2026-04-27T09:00:00+09:00 | 트럼프 Truth Social: "위트코프·쿠슈너 방문 취소. 원하면 전화해라." WTI $94.88→$95~96+ 재급등 트리거 |
| 2026-04-27 | news | Iran_New_Proposal | HORMUZ_REOPEN_CONDITIONAL | — | — | Al Jazeera / CNBC [2026-04-27] | 2026-04-27T09:00:00+09:00 | 이란, 파키스탄 경유 신제안: 호르무즈 재개방 + 핵협상 지연(미 봉쇄 해제 선행). WTI $86→$95~96 재등락 |
| 2026-04-27 | news | CathieWood_Trade | AMD_SELL_AMZN_BUY | — | — | Gurufocus / TheStreet / TipRanks [2026-04-26] | 2026-04-27T09:00:00+09:00 | AMD 215,643주($75M) 매도(+25% 급등 차익실현). AMZN 280,450주($71.5M) 매수(빅테크 실적 전). 핵IPO(XE) 추가 |
| 2026-04-27 | news | Ackman_AMZN | PERSHING_AMZN_INITIATED | — | — | Nasdaq / InsiderMonkey [2026-04-27] | 2026-04-27T09:00:00+09:00 | Ackman AMZN 신규 포지션. P/E 27배 저평가 진입. Buffett·Wood와 공동 보유 |
| 2026-04-27 | news | Druckenmiller | ALPHABET_ADD_SANDISK_EXIT | — | — | InsiderMonkey [2026-04-27] | 2026-04-27T09:00:00+09:00 | Alphabet 비중 확대 + Sandisk 청산. AI 플랫폼 전략 집중 |
| 2026-04-28 | us_index | SP500 | 7137.90 | +1.05% | point | CNBC / TheStreet [2026-04-28 close] | 2026-04-28T21:00:00-04:00 | FOMC 1일차 시작. UPS/GM/GE Aerospace/HON 실적 Beat + 리스크온. WTI $98.97 = Core PCE 상방 압박 |
| 2026-04-28 | us_index | NASDAQ | 24663.80 | +0.90% | point | TheStreet [2026-04-28 close] | 2026-04-28T21:00:00-04:00 | — |
| 2026-04-28 | us_index | DJIA | 49141.93 | -0.05% | point | TheStreet [2026-04-28 close] | 2026-04-28T21:00:00-04:00 | 보합. 방산·물류 섹터 소폭 지지 |
| 2026-04-28 | us_index | Russell2000 | 2785.38 | +0.74% | point | TheStreet [2026-04-28 close] | 2026-04-28T21:00:00-04:00 | 소형주 강세 유지 |
| 2026-04-28 | us_index | VIX | 18.92 | -2.97% | index | CNBC / Yahoo Finance [2026-04-28 close] | 2026-04-28T21:00:00-04:00 | ⚠️ 19선 대. FOMC + 빅테크 4/29 앞두고 공포 완화 중 |
| 2026-04-28 | asia_index | KOSPI | 6690.90 | +0.75% | point | CNBC Asia [2026-04-29 KST close] | 2026-04-29T15:30:00+09:00 | 신고가 랠리 지속 |
| 2026-04-28 | asia_index | KOSDAQ | 1220.26 | +0.39% | point | CNBC Asia [2026-04-29 KST close] | 2026-04-29T15:30:00+09:00 | 2000년 닷컴 피크 1,238.80 근접 |
| 2026-04-28 | asia_index | Nikkei225 | 59917.46 | -1.02% | point | CNBC Asia [2026-04-29 JST close] | 2026-04-29T15:30:00+09:00 | 일본 공휴일 연휴 앞두고 차익실현 |
| 2026-04-28 | asia_index | HangSeng | 26111.84 | +1.68% | point | CNBC Asia [2026-04-29 HKT close] | 2026-04-29T16:30:00+08:00 | 홍콩 반등. 중국 내수 기대 |
| 2026-04-28 | fx | DXY | 98.70 | +0.08% | index | Investing.com / CNBC [2026-04-28] | 2026-04-28T21:00:00-04:00 | FOMC 앞 달러 소폭 강세 |
| 2026-04-28 | fx | USDKRW | 1478.28 | +0.36% | KRW | PoundSterlingLive [2026-04-28] | 2026-04-28T21:00:00-04:00 | ⚠️ 1,400 초과 지속 |
| 2026-04-28 | fx | USDJPY | 159.79 | +0.27% | JPY | TradingEconomics [2026-04-28] | 2026-04-28T21:00:00-04:00 | ⚠️ 엔화 약세 지속. BOJ 관망 |
| 2026-04-28 | commodity | WTI | 98.97 | +2.69% | USD/barrel | CNBC / Fortune [2026-04-28 close] | 2026-04-28T21:00:00-04:00 | ⚠️ $100 직전. 이란 신제안 제출(오만 경유). UAE OPEC 탈퇴 임박 조짐 |
| 2026-04-28 | commodity | Brent | 111.57 | +3.2% | USD/barrel | CNBC [2026-04-28 close] | 2026-04-28T21:00:00-04:00 | ⚠️ 3월래 최고. WTI-Brent 스프레드 확대 |
| 2026-04-28 | commodity | Gold | 4578.30 | -0.29% | USD/oz | Investing.com [2026-04-28 close] | 2026-04-28T21:00:00-04:00 | 소폭 조정. 구조적 Bull 유지 |
| 2026-04-28 | bond | US10Y | 4.35 | +0.32% | percent | CNBC / Fed H.15 [2026-04-28] | 2026-04-28T21:00:00-04:00 | ⚠️ 4.35% 분기점 접근. FOMC + 유가 상승 인플레 반영 |
| 2026-04-28 | bond | US30Y | 4.94 | -0.04% | percent | Fed H.15 [2026-04-28] | 2026-04-28T21:00:00-04:00 | — |
| 2026-04-28 | crypto | BTC | 77631.68 | +1.68% | USD | CoinGabbar [2026-04-28] | 2026-04-28T21:00:00-04:00 | $77K대 안착. ETF 순유입 지속 |
| 2026-04-28 | crypto | ETH | 2332.32 | +1.87% | USD | CoinGabbar [2026-04-28] | 2026-04-28T21:00:00-04:00 | $2,300선 지지 확인 |
| 2026-04-28 | news | FOMC_Day1 | HOLD_EXPECTED | — | — | Fed / CNBC [2026-04-28] | 2026-04-28T21:00:00-04:00 | FOMC 1일차 시작. 동결 100% 컨센서스. 파월 임기 5/15 만료 — 라스트 코멘트 효과 극대화 |
| 2026-04-28 | news | CB_Consumer_Confidence_Apr | DECLINED | — | — | Conference Board / Bloomberg [2026-04-28 10:00 ET] | 2026-04-28T21:00:00-04:00 | 4월 소비자신뢰 하락 확인. Michigan 49.8(사상 최저) 연동. 소비자 심리 악화 구조화 |
| 2026-04-29 | us_index | SP500 | 7135.95 | -0.04% | point | CNBC / TheStreet [2026-04-29 close] | 2026-04-29T21:00:00-04:00 | FOMC 동결(8-4 분열) + UAE OPEC 탈퇴 쇼크 상쇄. 빅테크 AH 혼조. Dow 부진 |
| 2026-04-29 | us_index | NASDAQ | 24673.24 | +0.04% | point | CNBC [2026-04-29 close] | 2026-04-29T21:00:00-04:00 | 보합. 빅테크 AH 낙폭이 장중 반영 전 |
| 2026-04-29 | us_index | DJIA | 48861.81 | -0.57% | point | CNBC [2026-04-29 close] | 2026-04-29T21:00:00-04:00 | -280.12pt. 유가 급등 + 산업재 부진 |
| 2026-04-29 | us_index | Russell2000 | 미확인 | -1.15% | point | TheStreet [2026-04-29 close] | 2026-04-29T21:00:00-04:00 | 최대 낙폭. 소형주 리스크오프 |
| 2026-04-29 | us_index | VIX | 미확인 | 소폭변동 | index | 추정 [2026-04-29] | 2026-04-29T21:00:00-04:00 | FOMC 동결 후 일시 완화. 빅테크 AH 반응 반영 전 |
| 2026-04-29 | asia_index | KOSPI | 6690.90 | +0.75% | point | CNBC Asia [2026-04-29 KST close] | 2026-04-29T15:30:00+09:00 | 신고가 지속. 반도체·방산 외인 매수 |
| 2026-04-29 | asia_index | KOSDAQ | 1220.26 | +0.39% | point | CNBC Asia [2026-04-29 KST close] | 2026-04-29T15:30:00+09:00 | — |
| 2026-04-29 | asia_index | Nikkei225 | CLOSED | — | point | CNBC Asia [2026-04-29] | 2026-04-29T09:00:00+09:00 | 일본 공휴일(Showa Day). 30일까지 휴장 |
| 2026-04-29 | asia_index | HangSeng | 26111.84 | +1.2% | point | CNBC Asia [2026-04-29 HKT close] | 2026-04-29T16:30:00+08:00 | CSI300 +1.1% 동반 강세. 4,810.35 |
| 2026-04-29 | fx | DXY | 98.86 | +0.23% | index | TradingEconomics [2026-04-29] | 2026-04-29T21:00:00-04:00 | FOMC 매파 신호 + 지정학 안전자산 달러 소폭 강세 |
| 2026-04-29 | fx | USDKRW | 미확인 | 소폭변동 | KRW | 미수집 [2026-04-29] | 2026-04-29T21:00:00-04:00 | ⚠️ 1,400 초과 기조 유지 추정 |
| 2026-04-29 | fx | USDJPY | 159.82 | +0.12% | JPY | TradingEconomics [2026-04-29] | 2026-04-29T21:00:00-04:00 | BOJ 동결 4회 연속. 엔화 약세 지속 |
| 2026-04-29 | commodity | WTI | 106.88 | +6.96% | USD/barrel | TradingEconomics / Fortune [2026-04-29 close] | 2026-04-29T21:00:00-04:00 | ⚠️ UAE OPEC 탈퇴 쇼크. $100 돌파. Brent $120 근접(6월 2022 이후 최고) |
| 2026-04-29 | commodity | Brent | ~120 | +7%+ | USD/barrel | Euronews / CNBC [2026-04-29 close] | 2026-04-29T21:00:00-04:00 | ⚠️ UAE OPEC 탈퇴 + 이란 봉쇄 복합 공급 쇼크. OPEC 글로벌 점유율 30% 하회 |
| 2026-04-29 | commodity | Gold | 4522.97 | -1.59% | USD/oz | TradingEconomics [2026-04-29 close] | 2026-04-29T21:00:00-04:00 | 달러 강세 역풍. 구조적 Bull 기조 유지 |
| 2026-04-29 | bond | US10Y | 4.42 | +7bp | percent | CNBC / Fed H.15 [2026-04-29] | 2026-04-29T21:00:00-04:00 | ⚠️ FOMC 매파 분열(8-4) + UAE 쇼크 → 인플레 기대 급등. 4.40%+ 돌파 |
| 2026-04-29 | bond | US2Y | 3.95 | +bp | percent | CNBC [2026-04-29] | 2026-04-29T21:00:00-04:00 | ⚠️ 3.95% 상회. FOMC 매파 분열 반영 |
| 2026-04-29 | bond | Spread2Y10Y | +47 | — | bp | 계산값(4.42%-3.95%) | 2026-04-29T21:00:00-04:00 | 정상 구간(비역전) 유지. 전일 대비 축소 |
| 2026-04-29 | crypto | BTC | 76224 | -1.80% | USD | CoinGecko / SpotedCrypto [2026-04-29] | 2026-04-29T21:00:00-04:00 | 리스크오프 + ETF -$263M 순유출(9일 연속 순유입 종료). Fidelity FBTC -$150M |
| 2026-04-29 | crypto | ETH | 2285 | -2.0%(추정) | USD | CoinGecko [2026-04-29] | 2026-04-29T21:00:00-04:00 | BTC 동반 조정 |
| 2026-04-29 | crypto | TotalMarketCap | 2.63T | — | USD | CoinGecko [2026-04-29] | 2026-04-29T21:00:00-04:00 | BTC 도미넌스 58% |
| 2026-04-29 | crypto | FearAndGreedIndex | 33 | -14pt(47→33) | index | SpotedCrypto / CoinMarketCap [2026-04-29] | 2026-04-29T21:00:00-04:00 | ⚠️ Fear 재진입. UAE OPEC 탈퇴 + FOMC 매파 분열 + ETF 유출 복합 |
| 2026-04-29 | news | FOMC_Apr29_Decision | HOLD_8-4_SPLIT | — | — | CNBC / CNN / PBS [2026-04-29 14:00 ET] | 2026-04-29T21:00:00-04:00 | 3.50~3.75% 동결. 찬성 8명, 반대 4명(1992년 이후 최다 이견). Miran 25bp 인하 지지, 나머지 3인 완화 편향 성명 반대. "Iran 전쟁 등 4대 공급 쇼크" 명시 |
| 2026-04-29 | news | Powell_FinalPressConf | STAY_AS_GOVERNOR | — | — | CNN / PBS / CNBC [2026-04-29 14:30 ET] | 2026-04-29T21:00:00-04:00 | 파월: "이것이 마지막 기자회견". 의장 임기 5/15 만료 후 Fed 이사로 잔류(이사 임기 2028-01까지). "법적 공격이 Fed 기관을 훼손할 위험" 발언 |
| 2026-04-29 | news | UAE_OPEC_Exit | SHOCK_OIL_SUPPLY | — | — | Al Jazeera / CNBC / Fortune [2026-04-28~29] | 2026-04-29T21:00:00-04:00 | UAE 4/28 OPEC+ 탈퇴 공식 발표(발효 5/1). OPEC 글로벌 점유율 30% 하회(최초). WTI +$7 / Brent $120 근접. 중동 공급 구조 재편 |
| 2026-04-29 | news | MSFT_Q3FY26 | EPS_4.27_BEAT | — | — | CNBC / Gurufocus / Shacknews [2026-04-29 AH] | 2026-04-29T22:00:00-04:00 | EPS $4.27(컨센 $4.06 Beat+5.2%). Rev $82.9B(컨센 $81.39B Beat). Azure +40%(컨센 +37% 상회). AI 연환산매출 $37B(+123%). Copilot 2천만 유료 시트. Q4 가이던스 소폭 하회 → AH 혼조 |
| 2026-04-29 | news | META_Q1 | EPS_7.31_CAPEX_UP | — | — | StockTitan / CNBC / SeekingAlpha [2026-04-29 AH] | 2026-04-29T22:00:00-04:00 | Rev $56.31B(컨센 $55.45B Beat, +33% YoY). EPS $7.31(컨센 $6.65 Beat). Q2 가이던스 $58~61B. CapEx $125~145B(기존 $115~135B 상향). AH -7% (CapEx 급등 실망) |
| 2026-04-29 | news | AMZN_Q1 | REV_181B_AWS_28PCT | — | — | StockTitan / CNBC [2026-04-29 AH] | 2026-04-29T22:00:00-04:00 | Rev $181.5B(컨센 $177.3B Beat, +17% YoY). EPS $2.78(컨센 $1.64 대폭 Beat). AWS $37.6B(+28% YoY, 컨센 +26% 상회). 광고 $17.24B(+24%). CapEx $43.2B(분기). AH 강세 |
| 2026-04-29 | news | GOOGL_Q1 | REV_109B_CLOUD_63PCT | — | — | 9to5Google / Yahoo Finance / CNBC [2026-04-29 AH] | 2026-04-29T22:00:00-04:00 | Rev $109.9B(+22% YoY). EPS $5.11(컨센 $2.62 대폭 Beat). Cloud $20.03B(+63%, 컨센 $18.4B 대폭 상회). CapEx $180~190B(기존 $175~185B 상향). Pichai: "수요 대비 컴퓨팅 부족". AH +4% |
| 2026-04-29 | news | Druckenmiller_META_Exit | SOLD_META_BOUGHT_AMZN_GOOGL | — | — | Motley Fool / Yahoo Finance [2026-04-24] | 2026-04-29T09:00:00-04:00 | Druckenmiller, META 전량 청산 + AMZN·GOOGL 대폭 추가. "클라우드 AI 자기강화 시스템" 논리. Q1 2026 13F 기준(3/31 포지션일, 공시 5/15) |
| 2026-04-30 | us_index | SP500 | 7209.01 | +1.02% | point | CNBC / TheStreet [2026-04-30 close 확정] | 2026-05-01T09:00:00+09:00 | 신고가. 7,200선 최초 돌파 종가. 4월 최강 월간 수익률(+9.3%) |
| 2026-04-30 | us_index | NASDAQ | 24892.31 | +0.89% | point | CNBC / TheStreet [2026-04-30 close 확정] | 2026-05-01T09:00:00+09:00 | 신고가 경신 |
| 2026-04-30 | us_index | DJIA | 49652.14 | +1.62% | point | CNBC / TheStreet [2026-04-30 close 확정] | 2026-05-01T09:00:00+09:00 | +790.33pt. LLY +9% + CAT +10% + GOOGL +9% 주도 |
| 2026-04-30 | us_index | VIX | 16.89 | -10.21% | index | CNBC / CBOE [2026-04-30 close 확정] | 2026-05-01T09:00:00+09:00 | AAPL·LLY·CAT Beat + 리스크온. 빠른 공포 해소 |
| 2026-04-30 | us_index | AAPL | 282.86 | — | USD | MarketBeat / Yahoo Finance [2026-04-30 정규장] | 2026-05-01T09:00:00+09:00 | 정규장 $267.78~$284.88 변동. Q2 FY26 AH +3% 추가 |
| 2026-04-30 | asia_index | KOSPI | 6598.87 | -1.38% | point | CNBC Asia [2026-04-30 KST close 확정] | 2026-05-01T09:00:00+09:00 | 장중 ATH 6,750 달성 후 급반전 종가. 차익실현 |
| 2026-04-30 | asia_index | KOSDAQ | 1192.35 | -2.29% | point | CNBC Asia [2026-04-30 KST close 확정] | 2026-05-01T09:00:00+09:00 | 소형주 차익실현 가속 |
| 2026-04-30 | asia_index | Nikkei225 | 59284.92 | -1.06% | point | CNBC Asia [2026-04-30 JST close 확정] | 2026-05-01T09:00:00+09:00 | 연휴(4/29 Showa Day) 복귀 후 차익실현 |
| 2026-04-30 | asia_index | HangSeng | 26112.00 | +1.68% | point | CNBC Asia [2026-04-30 HKT close 확정] | 2026-05-01T09:00:00+09:00 | 중국 기술주 반등 |
| 2026-04-30 | asia_index | CSI300 | 4108.00 | +0.71% | point | CNBC Asia [2026-04-30 CST close 확정] | 2026-05-01T09:00:00+09:00 | 노동절 연휴 전 소폭 강세 |
| 2026-04-30 | fx | DXY | 98.96 | +0.37% | index | TradingEconomics / AhaSignals [2026-04-30 close] | 2026-05-01T09:00:00+09:00 | FOMC 매파 분열 + ECB 동결 이중 매파. 3주 고점 |
| 2026-04-30 | fx | USDKRW | 1474.91 | — | KRW | PoundSterlingLive / Investing.com [2026-04-29~30] | 2026-05-01T09:00:00+09:00 | ⚠️ 1,400 초과 지속. 4/29 고점 1,486.95 |
| 2026-04-30 | fx | EURUSD | ~1.17 | — | USD | 추정 [ECB 동결 반영] | 2026-05-01T09:00:00+09:00 | ECB 동결(컨센 인하 뒤집음) 이후 약세 |
| 2026-04-30 | commodity | WTI | 109.41 | 급등 | USD/barrel | FXDailyReport / TradingEconomics [2026-04-30] | 2026-05-01T09:00:00+09:00 | ⚠️ UAE OPEC 탈퇴 5/1 발효 + 이란 봉쇄. $110 직전 |
| 2026-04-30 | commodity | Brent | ~120 | 유지 | USD/barrel | CNBC [2026-04-30] | 2026-05-01T09:00:00+09:00 | ⚠️ 이란 봉쇄 구조화 |
| 2026-04-30 | commodity | Gold | 4550.00 | -0.79% | USD/oz | TradingEconomics [2026-04-30] | 2026-05-01T09:00:00+09:00 | DXY 강세 역풍. 구조적 Bull 기조 유지 |
| 2026-04-30 | bond | US10Y | 4.43 | +8bp | percent | CNBC / Fed H.15 [2026-04-30] | 2026-05-01T09:00:00+09:00 | ⚠️ Core PCE 0.0% 둔화에도 UAE 쇼크 + FOMC 매파로 고착 |
| 2026-04-30 | bond | US2Y | 3.95 | 유지 | percent | CNBC [2026-04-30] | 2026-05-01T09:00:00+09:00 | FOMC 매파 반영 |
| 2026-04-30 | bond | US30Y | ~5.0 | 추정 | percent | 추정 [2026-04-30] | 2026-05-01T09:00:00+09:00 | — |
| 2026-04-30 | bond | Spread2Y10Y | +48 | — | bp | 계산값(4.43%-3.95%) | 2026-05-01T09:00:00+09:00 | 정상 구간(비역전) 유지 |
| 2026-04-30 | crypto | BTC | 76967.00 | 보합 | USD | Binance / CoinGecko [2026-04-29~30] | 2026-05-01T09:00:00+09:00 | ETF -$263M 순유출(4/29). 리스크오프 영향 |
| 2026-04-30 | crypto | ETH | 2313.00 | 보합 | USD | CoinGecko [2026-04-30] | 2026-05-01T09:00:00+09:00 | $2,300 지지선 확인 |
| 2026-04-30 | crypto | TotalMarketCap | 2.65T | — | USD | CoinGecko [2026-04-30] | 2026-05-01T09:00:00+09:00 | BTC 도미넌스 58.1% / ETH 10.5% |
| 2026-04-30 | crypto | FearAndGreedIndex | 26 | -7pt(33→26) | index | alternative.me / SpotedCrypto [2026-04-30] | 2026-05-01T09:00:00+09:00 | ⚠️ Extreme Fear(25) 1포인트 전. UAE+FOMC+ETF유출 복합 |
| 2026-04-30 | news | AAPL_Q2FY26 | EPS_2.01_Rev_111B_Beat | — | — | Apple Newsroom / 9to5Mac / GuruFocus [2026-04-30 AH] | 2026-05-01T09:00:00+09:00 | EPS $2.01(컨센 $1.94 Beat). Rev $111.18B(컨센 $109.66B Beat). iPhone $57B(+22%, 소폭 Miss). Services $30.98B(사상 최고). Greater China $20.5B(+28%). AH +3% |
| 2026-04-30 | news | AAPL_CEO_Transition | Cook_ExecChairman_Ternus_CEO | — | — | Apple Newsroom [2026-04-30] | 2026-05-01T09:00:00+09:00 | Tim Cook 9/1 Executive Chairman 전환 공식 확인. John Ternus CEO 내정. $100B 자사주 매입 + 배당 인상 + 순현금중립 목표 폐기 |
| 2026-04-30 | calendar | ECB_Apr30 | HOLD_2pct_Hawkish_Surprise | — | — | ECB / CNBC [2026-04-30 14:15 ET] | 2026-05-01T09:00:00+09:00 | 컨센 25bp 인하 뒤집고 2.0% 동결. 매파 서프라이즈. EUR/USD 약세 |
| 2026-04-30 | calendar | GDP_Q1_Advance | PLUS_2.3pct_Beat | — | — | BEA [2026-04-30 08:30 ET] | 2026-05-01T09:00:00+09:00 | 컨센 2.1%(GDPNow 1.2%) 대폭 상회. 침체 우려 후퇴 |
| 2026-04-30 | calendar | CorePCE_March | YoY_2.6pct_MoM_0.0pct | — | — | BEA [2026-04-30 08:30 ET] | 2026-05-01T09:00:00+09:00 | YoY 2.6%(컨센 3.0% 대폭 하회). MoM 0.0%(컨센 0.3% 급감). 골디락스 신호 |
| 2026-05-01 | asia_index | KOSPI_open | 6533.60 | -1.0%(추정) | point | Investing.com / TradingEconomics [2026-05-01 개장] | 2026-05-01T09:30:00+09:00 | 4/30 -1.38% 연속 조정. AAPL AH +3% 긍정 상쇄 |
| 2026-05-01 | fx | USDKRW_morning | 1474.91 | — | KRW | PoundSterlingLive [2026-04-29~30 참조] | 2026-05-01T09:30:00+09:00 | ⚠️ 5/1 아침 기준. 정확 수치 미수집 — 4/29 고점 1,486.95 참조 |
| 2026-05-01 | calendar | NFP_April | NOT_RELEASED | — | — | BLS [공식 일정] | 2026-05-01T09:00:00+09:00 | 4월 NFP는 2026-05-08(첫째 주 금요일) 발표 예정. 오늘 미발표. 3월 NFP +178K(4/3 발표) |
| 2026-05-01 | calendar | ISM_Mfg_PMI_April | PENDING_10AM_ET | — | — | ISM [예정 2026-05-01 10:00 ET] | 2026-05-01T09:00:00+09:00 | S&P Global Flash PMI 4월 54.0(강세 선행 지표). ISM 컨센 ~52.5. 3월 ISM 52.7 |
| 2026-05-01 | news | Ackman_PSUS_IPO | PSUS_IPO_FIRST_DAY_40.90 | — | — | CNBC [2026-04-29] | 2026-05-01T09:00:00+09:00 | PSUS 상장 첫날 $40.90(-18%, IPO가 $50 하회). $5B 모집(목표 $5~10B 하단). Berkshire 모델 추구. AMZN 비중 14% |
| 2026-05-01 | news | Buffett_vs_Ackman | AMZN_OPPOSITE_DIRECTION | — | — | Motley Fool [2026-04-27] | 2026-05-01T09:00:00+09:00 | Buffett AMZN 77% 감축(포트 0.1%). Ackman AMZN 65% 증량(포트 14%). 동일 종목 정반대 방향 |
| 2026-05-03 | crypto | BTC | 78803 | +0.6%± | USD | Fortune / SpotedCrypto [2026-05-03 EDT 기준] | 2026-05-04T09:00:00+09:00 | $76K~$79K 구간 횡보. $80K 저항 테스트 중. RSI 강세 다이버전스. BTC OI $61B(수개월 최고) |
| 2026-05-03 | crypto | FearAndGreedIndex | Greed | 개선 | index | Milk Road [2026-05-03] | 2026-05-04T09:00:00+09:00 | ✅ 5/3 Daily Greed 진입. 직전 5/1 기준 26(Fear) → 빅테크 실적 호조 촉매로 심리 급반전 |
| 2026-05-03 | crypto | BTC_ETF_Inflow_Monthly | 1600M | — | USD | Milk Road / BanklessTimes [2026-05-03] | 2026-05-04T09:00:00+09:00 | 4월 BTC ETF 순유입 $1.6B. 5월 $3B 목표 상향 가능성. BTC 선물 OI $61B |
| 2026-05-03 | crypto | TotalMarketCap | ~2.65T | — | USD | CoinGecko 추정 [2026-05-03] | 2026-05-04T09:00:00+09:00 | BTC 도미넌스 ~57.5%. ETH 시총 ~$233B |
| 2026-05-03 | news | Iran_ProjectFreedom | SHIPS_ESCORT_ANNOUNCED | — | — | CNBC / Washington Post / CNN [2026-05-03] | 2026-05-04T09:00:00+09:00 | Trump "Project Freedom" 발표 — 5/4(월)부터 억류 선박 안내 개시. 봉쇄 해소 아닌 구출 목적. 이란 의회 "휴전 위반 간주" 경고. WTI 5/4 선물 변동성 촉매 |
| 2026-05-03 | news | Warsh_Senate_Committee | APPROVED_13_11 | — | — | Al Jazeera / Yahoo Finance / CNBC [2026-04-29 확정] | 2026-05-04T09:00:00+09:00 | 상원 금융위원회 통과(13-11 당파표결 — 사상 첫 완전 당파). 5/11주 본회의 표결 예정. Fetterman(D-PA) 찬성 의향. 파월 5/15 만료 전 인준 가능 |
| 2026-05-04 | news | TrumpXi_Summit | BEIJING_MAY14_CONFIRMED | — | — | EconoTimes / US News / CNBC [2026-05-04 확인] | 2026-05-04T09:00:00+09:00 | Trump 5/14 베이징 방문 확정(8년만 첫 방중). 6차 파리 협상 "건설적". 희토류·대두·펜타닐 패키지. Section 301 공청회 5/5 겹침 — 관세 완화 vs 유지 분기점 |
| 2026-05-04 | us_index | SP500 | 7200.75 | -0.41% | point | TheStreet / BNN Bloomberg [2026-05-04 close 확정] | 2026-05-05T09:00:00+09:00 | ⚠️ 이란-UAE 교전 격화(미군 보트 7척 격침 / UAE 미사일 피격). Dow -1.13%(-557pt). WTI +4.4%($106.42) |
| 2026-05-04 | us_index | DJIA | 48941.90 | -1.13% | point | TheStreet / BNN Bloomberg [2026-05-04 close 확정] | 2026-05-05T09:00:00+09:00 | -557pt. 이란 교전 격화 최대 낙폭 |
| 2026-05-04 | asia_index | KOSPI | 6936.99 | +5.12% | point | Korea Herald / Bloomingbit [2026-05-04 종가 확정] | 2026-05-05T09:00:00+09:00 | 사상 최고가 확정. 외인 +3조194억원. 5/5 어린이날 휴장(→ 5/6 재개장) |
| 2026-05-04 | commodity | WTI | 106.42 | +4.39% | USD/barrel | CNBC / BNN Bloomberg [2026-05-04 close] | 2026-05-05T09:00:00+09:00 | ⚠️ 이란-UAE 교전 재급등. UAE 미사일 피격 + Fujairah 오일 허브 화재 |
| 2026-05-04 | commodity | Brent | 114.44 | +5.80% | USD/barrel | CNBC / BNN Bloomberg [2026-05-04 close] | 2026-05-05T09:00:00+09:00 | ⚠️ $110 재돌파. 이란-UAE 교전 격화 |
| 2026-05-05 | us_index | SP500_intraday | ~7286 | ~+1.2%(추정) | point | Yahoo Finance / CNBC [2026-05-05 장중 intraday] | 2026-05-05T14:00:00-04:00 | 이란 협상 낙관론(Trump 8pm ET 데드라인 + 이란 新제안). 전일 -0.41% 회복 중 |
| 2026-05-05 | us_index | NASDAQ_intraday | — | ~+2.0%(추정) | point | Yahoo Finance [2026-05-05 장중] | 2026-05-05T14:00:00-04:00 | 메가캡 기술주 주도 반등. 이란 협상 낙관 |
| 2026-05-05 | us_index | DJIA_intraday | — | ~+0.6%(추정) | point | Yahoo Finance [2026-05-05 장중] | 2026-05-05T14:00:00-04:00 | 전일 -1.13% 부분 회복 |
| 2026-05-05 | commodity | WTI_intraday | ~92 | ~-7%(추정) | USD/barrel | Yahoo Finance / CNBC [2026-05-05 장중] | 2026-05-05T14:00:00-04:00 | ⚠️→완화: 이란 협상 낙관론으로 급락. 오전 $107.42→장중 $92 |
| 2026-05-05 | commodity | Brent_intraday | ~96 | ~-4%(추정) | USD/barrel | Investing.com [2026-05-05 장중] | 2026-05-05T14:00:00-04:00 | ⚠️→완화: $107.42 오픈 → $96 급락. 이란 협상 기대 |
| 2026-05-05 | commodity | Brent_open | 107.42 | — | USD/barrel | Investing.com [2026-05-05 오픈] | 2026-05-05T09:30:00-04:00 | 5/5 오전 개장가. 이후 협상 낙관 급락 |
| 2026-05-05 | commodity | Gold_open | 4644.40 | 보합 | USD/oz | Investing.com [2026-05-05 오픈] | 2026-05-05T09:30:00-04:00 | $4,600선 유지. 이란 협상 낙관 시 헷지 수요 감소 |
| 2026-05-05 | fx | USDKRW | 1471.32 | 소폭변동 | KRW | TradingEconomics / Investing.com [2026-05-05] | 2026-05-05T09:00:00+09:00 | ⚠️ 1,400 초과. 범위 1,467.90~1,477.18. 이란 협상 타결 시 원화 강세 전환 가능 |
| 2026-05-05 | fx | DXY | 98.189 | +0.12% | index | TradingEconomics [2026-05-05] | 2026-05-05T09:00:00+09:00 | 98 구간 유지. 이란 협상 낙관 달러 약세 압력 |
| 2026-05-05 | bond | US10Y | ~4.42 | — | percent | CNBC / TradingEconomics [2026-05-05 추정] | 2026-05-05T09:00:00+09:00 | 4.5% 기준선 이하. 이란 협상 낙관 → 리스크온 → 소폭 상승 가능 |
| 2026-05-05 | bond | US2Y | 3.927 | — | percent | CNBC [2026-05-05 10:38 AM ET] | 2026-05-05T14:38:00-04:00 | FOMC 동결(3.50~3.75%) 반영 |
| 2026-05-05 | bond | Spread2Y10Y | ~+49~51 | — | bp | 계산값(추정) | 2026-05-05T09:00:00+09:00 | 정상 구간(비역전) 유지 |
| 2026-05-05 | crypto | BTC | ~79810 | 고가터치 | USD | Finance Magnates / SpotedCrypto [2026-05-04~05] | 2026-05-05T09:00:00+09:00 | 5/4 $80,393 터치(2026년 1/31 이후 최고). 이란 협상 낙관 리스크온 |
| 2026-05-05 | crypto | ETH | ~2302 | +0.84% | USD | Binance [2026-05-04] | 2026-05-05T09:00:00+09:00 | $2,300 지지선 유지 |
| 2026-05-05 | crypto | FearAndGreedIndex | 39 | 개선 중 | index | Milkroad.com [2026-05-04] | 2026-05-05T09:00:00+09:00 | Fear 구간. 5/3 Daily Greed 진입 후 조정. 이란 협상 낙관 시 Neutral 전환 가능 |
| 2026-05-05 | news | Iran_Military_Escalation | BOATS_SUNK_UAE_MISSILE | — | — | CBS News / NPR / CNBC [2026-05-04 확정] | 2026-05-05T09:00:00+09:00 | 5/4: 미군 이란 소형 보트 7척 격침(Admiral Brad Cooper). UAE 미사일 피격 보도 + Fujairah 오일 허브 화재. 최초 공식 교전 격화. |
| 2026-05-05 | news | Iran_Negotiation_Update | TRUMP_DEADLINE_8PM_ET | — | — | Yahoo Finance / The Hill / CNN [2026-05-05] | 2026-05-05T09:00:00+09:00 | Trump, 이란에 8pm ET 협상 데드라인 설정. 이란 30일 내 전쟁 종결 + 제재 해제 묶음 제안 전달. War Powers Act 60일 시계 논쟁(민주당 vs 백악관). |
| 2026-05-05 | news | KOSPI_Holiday | CHILDRENS_DAY_CLOSED | — | — | KRX / TradingHours.com [2026-05-05 확인] | 2026-05-05T09:00:00+09:00 | 5/5 어린이날 휴장. 5/6(수) 재개장. 이란 협상 진전 + WTI -7% 반응 예상 |
| 2026-05-05 | calendar | Section301_Hearing | USTR_EXCESS_CAPACITY_16NATIONS | — | — | USTR / Holland & Knight [2026-05-05] | 2026-05-05T09:00:00+09:00 | USTR, 중국·한국 등 16개국 제조업 과잉생산 조사 공청회. 목표 완료일 2026-07-24. Trump-Xi 5/14 정상회담 선행 이벤트 |
| 2026-05-05 | calendar | ISM_Services_PMI_April | PENDING_10AM_ET | — | — | ISM / FXStreet [2026-05-05 10:00 ET 발표 예정] | 2026-05-05T09:00:00+09:00 | 컨센 ~53%(3월 54%. 21개월 연속 확장). 결과 미확보 — 이브닝 갱신 필요 |
| 2026-05-05 | calendar | AMD_Q1_2026 | PENDING_AH_17:00ET | — | — | MarketBeat / StockTitan [2026-05-05 발표 예정] | 2026-05-05T09:00:00+09:00 | 컨센 EPS $1.30(+35% YoY) / Rev $9.84B(+32%). EPYC + Instinct AI GPU. NVIDIA 5/6 선행 지표 |
| 2026-05-06 | us_index | SP500 | 7365.12 | +1.46% | point | Yahoo Finance / TheStreet [2026-05-06 ET 16:00 종가] | 2026-05-07T05:00:00+09:00 | 신고가 경신. AMD 실적 호재 + 이란 협상 낙관 + WTI 급락 |
| 2026-05-06 | us_index | NASDAQ | 25838.94 | +2.02% | point | Yahoo Finance / TheStreet [2026-05-06 ET 16:00 종가] | 2026-05-07T05:00:00+09:00 | 신고가 경신. 반도체 섹터 주도 |
| 2026-05-06 | us_index | DJIA | 49910.59 | +1.24% | point | Yahoo Finance [2026-05-06 ET 16:00 종가] | 2026-05-07T05:00:00+09:00 | |
| 2026-05-06 | us_index | Russell2000 | 2886.77 | +1.47% | point | Yahoo Finance / TheStreet [2026-05-06 ET 16:00 종가] | 2026-05-07T05:00:00+09:00 | 신고가 경신 |
| 2026-05-06 | us_index | VIX | 17.39 | +0.06% | index | 247wallst.com [2026-05-06 ET 종가] | 2026-05-07T05:00:00+09:00 | 정상 구간 유지 |
| 2026-05-06 | asia_index | KOSPI | 7384.56 | +6.45% | point | ASIAE / KRX [2026-05-06 KST 종가] | 2026-05-06T15:30:00+09:00 | 사상 첫 7,000 돌파. 어린이날(5/5) 휴장 후 재개장 |
| 2026-05-06 | asia_index | KOSDAQ | 1210.17 | -0.29% | point | Investing.com [2026-05-06 KST 종가] | 2026-05-06T15:30:00+09:00 | |
| 2026-05-06 | asia_index | HangSeng | 26213.78 | +1.22% | point | Yahoo Finance [2026-05-06 HKT 종가] | 2026-05-06T16:00:00+08:00 | |
| 2026-05-06 | fx | USDKRW | 1451.71 | -1.17% | KRW | Trading Economics [2026-05-06 종가] | 2026-05-07T05:00:00+09:00 | ⚠️ 1,400 초과 유지. 이란 협상 진전 원화 강세 |
| 2026-05-06 | fx | USDJPY | 156.38 | -0.95% | JPY | Trading Economics [2026-05-06 종가] | 2026-05-07T05:00:00+09:00 | |
| 2026-05-06 | commodity | WTI | 91.54 | -10.5% | USD/barrel | Yahoo Finance / TheStreet [2026-05-06 ET 종가] | 2026-05-07T05:00:00+09:00 | ⚠️ 이란 MOU 협상 낙관 급락. 5/5 ~$102 → 5/6 $91.54 |
| 2026-05-06 | commodity | Brent | 102.22 | -6.96% | USD/barrel | Trading Economics [2026-05-06] | 2026-05-07T05:00:00+09:00 | ⚠️ 이란 협상 낙관 동반 급락 |
| 2026-05-06 | commodity | Gold | 4697.48 | +3.11% | USD/oz | Fortune.com [2026-05-06 종가] | 2026-05-07T05:00:00+09:00 | 중동 완화 우려 경감에도 금 강세 유지 |
| 2026-05-06 | bond | US10Y | 4.38 | -4bp | percent | Trading Economics [2026-05-06 ET 종가] | 2026-05-07T05:00:00+09:00 | |
| 2026-05-06 | crypto | BTC | 82320 | — | USD | Yahoo Finance [2026-05-06 ET 08:45 참조] | 2026-05-07T05:00:00+09:00 | 1월 이후 최고 수준 유지 |
| 2026-05-06 | crypto | ETH | 2407 | — | USD | Yahoo Finance [2026-05-06 ET 08:45 참조] | 2026-05-07T05:00:00+09:00 | |
| 2026-05-06 | news | AMD_Q1_FY2026 | REV_10.25B_EPS_1.37_BEAT | — | — | Shacknews / Seeking Alpha [2026-05-05 장후] | 2026-05-07T05:00:00+09:00 | Rev $10.25B(+38% YoY) vs $9.89B 컨센. EPS $1.37 vs $1.29. 주가 +16% |
| 2026-05-06 | news | ARM_Q4_FY2026 | REV_1.49B_EPS_0.60_BEAT | — | — | Shacknews / Investing.com [2026-05-06 장후] | 2026-05-07T05:00:00+09:00 | Rev $1.49B vs $1.47B 컨센. EPS $0.60 vs $0.58. 데이터센터 로열티 YoY 2배 |
| 2026-05-06 | news | NVIDIA_Earnings_Date | 20260520_AH | — | — | investor.nvidia.com / MarketBeat [확인] | 2026-05-07T05:00:00+09:00 | FY27 Q1 실적: 2026-05-20 장후 발표. 5/6 자체 발표 없음 (AMD 호재 동반 +5.5%) |
| 2026-05-06 | news | Iran_MOU_Negotiation | US_EPIC_FURY_CONCLUDED | — | — | Axios / CNN / Al Jazeera [2026-05-06] | 2026-05-07T05:00:00+09:00 | Rubio: Operation Epic Fury 종결. 14개항 MOU 협상 중. WTI -10.5% 급락 배경 |
| 2026-05-06 | calendar | ISM_Services_PMI_April | 53.6 | -0.4pp vs 3월 | index | ISM / prnewswire [2026-05-05] | 2026-05-07T05:00:00+09:00 | 22개월 연속 확장. 물가지수 70.7(2022 이후 최고). 고용 48.0(수축) |
| 2026-05-06 | calendar | ADP_Private_Payrolls_April | 109000 | +10K vs 컨센 99K | jobs | CNBC / prnewswire [2026-05-06] | 2026-05-07T05:00:00+09:00 | 1월 2025 이후 최강. 3월 62K로 하향 조정 |
| 2026-05-07 | us_index | SP500_futures | 7394.25 | +0.06% | point | Investing.com [2026-05-07 프리마켓 KST 오전] | 2026-05-07T04:00:00-04:00 | S&P 500 선물. 5/7 미국 정규장 개장 전 |
| 2026-05-07 | us_index | NASDAQ_futures | 28712.75 | -0.01% | point | Investing.com [2026-05-07 프리마켓 KST 오전] | 2026-05-07T04:00:00-04:00 | 혼조 출발. AMD·ARM 호재 소화 완료 |
| 2026-05-07 | asia_index | Nikkei225 | 62915.87 | +5.75% | point | CNBC / Reuters [2026-05-07 JST 종가] | 2026-05-07T15:30:00+09:00 | ⚠️ 사상 최고가. 황금연휴(4/29~5/6) 8거래일 공백 한꺼번에 반영. SoftBank +16.5% / Ibiden +17% / Tokyo Electron +9.2% / Advantest +7.8%. AI 랠리 캐치업 |
| 2026-05-07 | asia_index | KOSPI | ~7360 | -0.33% 추정 | point | CNBC / Seoul Economic Daily [2026-05-07 KST 장중] | 2026-05-07T15:30:00+09:00 | 오픈 7,499.07(+1.55%). 장중 차익실현. 5/6 종가 7,384.56 대비 소폭 조정. 2026 YTD +75% 세계 최강 수익률 |
| 2026-05-07 | asia_index | HangSeng | ~26597 | +1.47% | point | CNBC / SCMP [2026-05-07 HKT 장중/종가] | 2026-05-07T16:00:00+08:00 | 26,500선 회복. 중동 긴장 완화 + AI 기술주 반등 동조 |
| 2026-05-07 | fx | DXY | 98.03 | -0.01% | index | TradingEconomics [2026-05-07] | 2026-05-07T06:00:00-04:00 | 달러 약세 구조 지속. 이란 협상 진전 반영 |
| 2026-05-07 | fx | USDKRW | ~1440~1452 구간 | 소폭변동 | KRW | Investing.com / PoundSterlingLive [2026-05-06~07] | 2026-05-07T15:00:00+09:00 | ⚠️ 1,400 초과. 5/6 일중 저점 1,440.30(주간 최저). 이란 협상 + KOSPI 외인 유입 |
| 2026-05-07 | commodity | WTI | 95.66 | +4.50% (5/6 $91.54 대비) | USD/barrel | TradingEconomics [2026-05-07 장중] | 2026-05-07T10:00:00-04:00 | ⚠️ 5/6 협상 낙관 급락($91.54) 후 5/7 반등. 이란 협상 불확실 재확대. 48시간 내 응답 대기 |
| 2026-05-07 | commodity | Gold | 4710.76 | +0.28% 추정 | USD/oz | GoldPrice.org / TradingEconomics [2026-05-07 장중] | 2026-05-07T10:00:00-04:00 | 지정학 불확실에도 구조적 Bull 기조 유지. $4,700선 안착 |
| 2026-05-07 | bond | US10Y | ~4.42 | 유지 추정 | percent | 5/6 종가 기준 유지 (5/7 공식값 ET 장중 미수집) | 2026-05-07T15:56:00+09:00 | 5/6 ET 16:00 종가 4.42% 기준. 5/7 공식 종가 미수집 (ET 미마감) |
| 2026-05-07 | bond | US2Y | ~3.93 | 유지 추정 | percent | 추정 [5/6~7 연속성] | 2026-05-07T15:56:00+09:00 | — |
| 2026-05-07 | bond | Spread2Y10Y | ~+49 | — | bp | 계산값 (4.42%-3.93%) | 2026-05-07T15:56:00+09:00 | 정상 구간(비역전) 유지 |
| 2026-05-07 | crypto | BTC | ~82305 | 5/6 참조 | USD | Yahoo Finance [2026-05-06 ET 07:03 참조] | 2026-05-07T15:56:00+09:00 | 1월 31일 이후 최고. 이란 리스크온 + 크립토 법제화 기대 |
| 2026-05-07 | crypto | ETH | ~2412 | 5/6 참조 | USD | Yahoo Finance [2026-05-06 ET 07:03 참조] | 2026-05-07T15:56:00+09:00 | 4월 27일 이후 최고 |
| 2026-05-07 | news | Shell_Q1_2026 | ADJ_EARNINGS_6.9B | — | — | Shell IR / GlobeNewswire / StockTitan [2026-05-07 장전] | 2026-05-07T08:00:00-04:00 | 조정이익 $6.9B. CFFO $17.2B. 배당 5% 인상 $0.3906. $3B 자사주 매입. ARC Resources 인수(370 kboe/d 추가, 생산 CAGR +4%). 운전자본 유출 $11.2B (원자재 변동성 반영) |
| 2026-05-07 | news | McDonalds_Q1_2026 | PENDING_PREMARKET | — | — | CNBC / MarketBeat [2026-05-07 장전 예정] | 2026-05-07T15:56:00+09:00 | 컨센 EPS $2.75 / Rev $6.47B / SSS +3.7%. KST 15:56 수집 시점 공식 결과 미확인. Polymarket 77% Beat 예상 |
| 2026-05-07 | news | Jobless_Claims_Weekly | PENDING_08:30ET | — | — | DOL / Investing.com [2026-05-07 08:30 ET 예정] | 2026-05-07T15:56:00+09:00 | 컨센 ~205K (전주 189K 57년 최저). KST 15:56 = ET 07:56 — 발표 전. 실제 결과 미수집 |
| 2026-05-07 | news | Iran_Negotiations | ONE_PAGE_MOU_NEAR | — | — | Axios / Times of Israel / CNBC [2026-05-06~07] | 2026-05-07T09:00:00-04:00 | 미국, 이란 one-page MOU 초안 근접. 핵 모라토리엄 기간 12~15년 협상 중(미 20년 요구/이란 5년). 이란 고농축 우라늄 국외 반출 + IAEA 사찰 논의. 48시간 내 응답 대기. Trump 합의 불발 시 "훨씬 강도 높은 폭격" 재경고 |
| 2026-05-07 | news | Nikkei_Record_High | ATH_62915 | — | — | CNBC / Reuters [2026-05-07] | 2026-05-07T15:30:00+09:00 | 닛케이 사상 최고가 62,915.87. 황금연휴(4/29~5/6) 복귀 캐치업. SoftBank 비전펀드 AI 투자 재평가 + 반도체 전 종목 급등 |
| 2026-05-08 | us_index | SP500 | 7337.11 | -0.38% | point | CNBC / TheStreet [2026-05-08 ET 16:00 종가] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-08 | us_index | NASDAQ | 25806.20 | -0.13% | point | CNBC [2026-05-08 ET 16:00 종가] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-08 | us_index | DJIA | 49596.97 | -0.63% | point | CNBC [2026-05-08 ET 16:00 종가] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-08 | asia_index | KOSPI | 7498.00 | +0.11% | point | Seoul Econ Daily [2026-05-08 KST 15:30 종가] | 2026-05-09T10:00:00+09:00 | 4일 연속 상승. 사상 최고치 경신 |
| 2026-05-08 | asia_index | KOSDAQ | 1207.72 | +0.71% | point | Seoul Econ Daily [2026-05-08 KST 15:30 종가] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-08 | asia_index | Nikkei225 | 62713.65 | -0.19% | point | Yahoo Finance [2026-05-08 KST 15:30 종가] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-08 | bond | US10Y | 4.38 | -2bp | percent | Fed H.15 [2026-05-08 공식] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-08 | bond | US30Y | 4.95 | -0.38% | percent | Yahoo Finance [2026-05-08 ET 16:00] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-09 | us_index | SP500 | 7398.93 | +0.84% | point | CNBC [2026-05-09 ET 16:00 종가 / KST 2026-05-10 05:00] | 2026-05-09T10:00:00+09:00 | 사상 최고치. 6주 연속 상승. NFP +115K vs 컨센 +65K 골디락스 |
| 2026-05-09 | us_index | NASDAQ | 26247.08 | +1.71% | point | CNBC [2026-05-09 ET 16:00 종가 / KST 2026-05-10 05:00] | 2026-05-09T10:00:00+09:00 | 사상 최고치. 주간 +4.51% |
| 2026-05-09 | us_index | DJIA | 49609.16 | +0.02% | point | CNBC [2026-05-09 ET 16:00 종가 / KST 2026-05-10 05:00] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-09 | us_index | VIX | 17.19 | +0.64% | index | Yahoo Finance [2026-05-09 ET 16:00 종가] | 2026-05-09T10:00:00+09:00 | 20 미만 유지 (위험선호 구간) |
| 2026-05-09 | fx | DXY | 97.84 | -0.42% | index | Investing.com [2026-05-09 ET 종가] | 2026-05-09T10:00:00+09:00 | 10주 최저. 강한 NFP에도 달러 약세 (에너지 충격 반영) |
| 2026-05-09 | fx | USDKRW | 1461.48 | +1.18% | KRW | Yahoo Finance [2026-05-09 ET 종가] | 2026-05-09T10:00:00+09:00 | ⚠️ 1400 상회 유지 |
| 2026-05-09 | fx | USDJPY | 156.62 | +0.07% | JPY | Yahoo Finance [2026-05-09 ET 종가] | 2026-05-09T10:00:00+09:00 | 155.76~157.90 주간 레인지 |
| 2026-05-09 | commodity | WTI | 95.42 | +0.64% | USD/barrel | Investing.com [2026-05-09 ET 종가] | 2026-05-09T10:00:00+09:00 | $95 유지. 이란 협상 불확실 지속 |
| 2026-05-09 | commodity | Gold | 4720.40 | +0.44% | USD/oz | GoldPrice.org [2026-05-09 ET 종가] | 2026-05-09T10:00:00+09:00 | $4,700선 안착 |
| 2026-05-09 | crypto | BTC | 80263.61 | +0.10% | USD | Yahoo Finance [2026-05-09 KST 수집] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-09 | crypto | ETH | 2313.26 | +0.27% | USD | Yahoo Finance [2026-05-09 KST 수집] | 2026-05-09T10:00:00+09:00 | — |
| 2026-05-09 | macro | NFP_April2026 | 115000 | — | jobs | BLS [2026-05-09 08:30 ET 발표] | 2026-05-09T10:00:00+09:00 | 컨센 +65K 대폭 상회. 실업률 4.3% 유지. 헬스케어·운송·소매 주도. 골디락스 해석 |
| 2026-05-09 | us_index | VIX_corrected | 17.08 | -1.78% | index | Alain Guillot / TheStreet [2026-05-08 ET 16:00 종가] | 2026-05-10T20:00:00+09:00 | 5/9 이전 기록(17.19)은 5/8 중간값. 5/8 ET 16:00 공식 종가 17.08. 20 미만 안정 구간 |
| 2026-05-09 | asia_index | HangSeng | 26626.28 | +1.57% | point | Yahoo Finance [2026-05-09 HKT 16:00 종가] | 2026-05-10T20:00:00+09:00 | 이란 협상 낙관 + 중국 기술주 강세 |
| 2026-05-09 | asia_index | ShanghaiComposite | 4180.09 | +0.48% | point | Yahoo Finance [2026-05-09 CST 15:00 종가] | 2026-05-10T20:00:00+09:00 | 중국 경기 모멘텀 소폭 강화 |
| 2026-05-09 | asia_index | SENSEX | 77344 | -0.64% | point | Goodreturns [2026-05-09 IST 15:30 종가] | 2026-05-10T20:00:00+09:00 | Bajaj Finance(-1.88%) / HDFC Bank(-1.86%) / Axis Bank(-1.76%) 주도 하락. Titan Company(+4.86%) 강세 |
| 2026-05-09 | bond | US2Y | 3.90 | — | percent | ETF Trends / Advisor Perspectives [2026-05-08 ET 종가] | 2026-05-10T20:00:00+09:00 | 5/8 ET 종가. NFP 강건에도 소폭 하락 — 임금 +0.2% 하회 반영 |
| 2026-05-09 | bond | Spread2Y10Y | +48 | — | bp | 계산값(4.38%-3.90%) | 2026-05-10T20:00:00+09:00 | 정상 구간(비역전) 유지. 장단기 스프레드 안정 |
| 2026-05-09 | commodity | Gold_corrected | 4715.85 | +0.63% | USD/oz | Trading Economics [2026-05-08 ET 종가] | 2026-05-10T20:00:00+09:00 | 5/8 ET 16:00 공식 종가. $4,700선 안착 |
| 2026-05-09 | crypto | FearAndGreedIndex | 49 | — | index | Milkroad [2026-05-09] | 2026-05-10T20:00:00+09:00 | Fear 구간(50 미만). 직전 38(Fear). 암호화폐 심리 소폭 개선 중 |
| 2026-05-09 | crypto | BTC_ETF_Monthly | 2440M | — | USD | Yahoo Finance [2026-05 누계] | 2026-05-10T20:00:00+09:00 | 미국 spot BTC ETF 4월 유입 $2.44B — 10월 2025 이후 최대. 기관 수요 재확인 |
| 2026-05-09 | macro | NFP_April_Breakdown | Health37K_Transport30K_Retail22K | — | jobs | BLS [2026-05-08 08:30 ET] | 2026-05-10T20:00:00+09:00 | 업종별: 헬스케어 +37K / 운송·창고 +30K / 소매 +22K. 연방정부 -9K / 정보 -13K / 제조 -2K. K자형 노동시장 공식화 |
| 2026-05-14 | crypto | BTC | 81351.38 | +2.62% | USD | yfinance [2026-05-14 KST 수집 / fetch_price.py] | 2026-05-15T05:18:26+09:00 | $81K 재진입. NASDAQ 디커플링 완화 진행 |
| 2026-05-14 | crypto | ETH | 2294.01 | +1.61% | USD | yfinance [2026-05-14 KST 수집] | 2026-05-15T05:18:27+09:00 | $2,300 임박. BTC 대비 상대 약세 지속 |
| 2026-05-14 | crypto | SOL | 92.69 | +1.76% | USD | yfinance [2026-05-14 KST 수집] | 2026-05-15T05:18:28+09:00 | 알트 약세 흐름 유지. 52w 저점 $68.69 대비 회복 중 |
| 2026-05-14 | crypto | BNB | 679.31 | +1.18% | USD | yfinance [2026-05-14 KST 수집] | 2026-05-15T05:18:29+09:00 | 안정 횡보 + MiCA 2.0 대응 |
| 2026-05-14 | crypto | DOGE | 0.12 | +6.47% | USD | yfinance [2026-05-14 KST 수집] | 2026-05-15T05:18:30+09:00 | 변동성 확대 — 밈 사이클 일시 반등 |
| 2026-05-14 | crypto | LINK | 10.61 | +3.90% | USD | yfinance [2026-05-14 KST 수집] | 2026-05-15T05:18:32+09:00 | DeFi 모멘텀 안정. CCIP·RWA 내러티브 |
| 2026-05-14 | crypto | FearAndGreedIndex | 34 | — | index | alternative.me [2026-05-14] | 2026-05-15T05:18:22+09:00 | Fear 구간. 직전 42(Fear), 1주 47(Neutral) → 8p 하락. BTC ETF 유입 둔화 + Warsh 불확실성 반영 |
| 2026-05-18 | us_index | SP500 | 7403.05 | -0.07% | point | TheStreet/CNBC [2026-05-18 ET 16:00 종가] | 2026-05-19T09:00:00+09:00 | 2거래일 연속 하락. 테크섹터 -1.1% 주도. 다우만 +0.32% 방어 |
| 2026-05-18 | us_index | NASDAQ | 26090.73 | -0.51% | point | TheStreet/CNBC [2026-05-18 ET 16:00 종가] | 2026-05-19T09:00:00+09:00 | Seagate -7% Micron -6% 반도체 급락 |
| 2026-05-18 | us_index | DJIA | 49686.12 | +0.32% | point | TheStreet/CNBC [2026-05-18 ET 16:00 종가] | 2026-05-19T09:00:00+09:00 | 가치주 방어. 기술주 약세 속 나홀로 상승 |
| 2026-05-18 | us_index | VIX | 18.43 | -3.31% | index | FRED VIXCLS / Yahoo Finance [2026-05-18] | 2026-05-19T09:00:00+09:00 | 20 미만 유지. 이란 공격 연기 소식으로 점차 완화 |
| 2026-05-18 | bond | US10Y | 4.63 | +4bp est | % | TheStreet [2026-05-18 ET — "hits highest in a year"] | 2026-05-19T09:00:00+09:00 | ⚠️ 연중 최고. 2025년 이후 1년 만. CPI 3.8%+PPI 상회+이란 에너지 충격 구조화 |
| 2026-05-18 | bond | US30Y | 5.13 | +2bp est | % | TheStreet [2026-05-18 ET — "highest in nearly a decade"] | 2026-05-19T09:00:00+09:00 | ⚠️ 10년래 최고. 장기 인플레 기대 재점화 |
| 2026-05-18 | fx | DXY | 99.30 | +0.09% | index | FXStreet/DealPlexus [2026-05-18] | 2026-05-19T09:00:00+09:00 | 이란발 인플레 달러 강세. 월중 최강 수준 |
| 2026-05-18 | fx | USDJPY | 158.90 | +0.11% | JPY | TradingEconomics [2026-05-18] | 2026-05-19T09:00:00+09:00 | 엔화 약세 지속. BOJ 개입 경계선 160 접근 |
| 2026-05-18 | commodity | WTI | 106.22 | +0.76% | USD/barrel | TradingEconomics [2026-05-18 ET 종가] | 2026-05-19T09:00:00+09:00 | ⚠️ $100 상단 고착. 이란전쟁 공급 차질 지속 |
| 2026-05-19 | us_index | SP500 | 7353.61 | -0.67% | point | CNBC/TheStreet [2026-05-19 ET 16:00 종가] | 2026-05-20T09:10:00+09:00 | 3거래일 연속 하락. 10Y 4.687% 급등이 성장주 밸류에이션 압박 |
| 2026-05-19 | us_index | NASDAQ | 25870.71 | -0.84% | point | CNBC/TheStreet [2026-05-19 ET 16:00 종가] | 2026-05-20T09:10:00+09:00 | 반도체 섹터 주도 하락. 금리 급등 = 성장주 멀티플 압박 |
| 2026-05-19 | us_index | DJIA | 49363.88 | -0.65% | point | CNBC/TheStreet [2026-05-19 ET 16:00 종가] | 2026-05-20T09:10:00+09:00 | 전 섹터 동반 하락 -322pt. 전날 방어 효과 소멸 |
| 2026-05-19 | us_index | Russell2000 | — | ~-1.29% | point | Bloomberg [2026-05-19 장중 관측] | 2026-05-20T09:10:00+09:00 | 소형주 상대 약세. 금리 민감도 높아 대형주보다 낙폭 큼 |
| 2026-05-19 | us_index | VIX | ~18.0 | 소폭상승 | index | 추정 [2026-05-19 ET 종가] | 2026-05-20T09:10:00+09:00 | 18~20 구간 유지. 공포 임계치(20) 미도달 |
| 2026-05-19 | bond | US10Y | 4.687 | +5.7bp | % | TheStreet [2026-05-19 ET 장중 고점] | 2026-05-20T09:10:00+09:00 | ⚠️ 16개월래 최고. S&P 3연속 하락 직격 원인 |
| 2026-05-19 | bond | US30Y | 5.19 | +6bp est | % | Bloomberg/247wallst [2026-05-19 ET 장중] | 2026-05-20T09:10:00+09:00 | ⚠️ 19년래(2007년) 최고 수준 일시 돌파 |
| 2026-05-19 | bond | US2Y | ~4.09 | — | % | FRED DGS2 [2026-05-15 최근] | 2026-05-20T09:10:00+09:00 | FRED 5/15 관측값. 5/19 확정치 미수집 |
| 2026-05-19 | fx | DXY | ~99.0 | 하락 | index | TradingEconomics [2026-05-19] | 2026-05-20T09:10:00+09:00 | 미-이란 협상 진전 소식 → 달러 약세. 100 하향 이탈 |
| 2026-05-19 | fx | USDKRW | ~1500 | 변동성 | KRW | Investing.com [2026-05-19~20] | 2026-05-20T09:10:00+09:00 | 1,489.93~1,509.70 범위. 1,500 상단 박스권 |
| 2026-05-19 | commodity | WTI | 104.36 | -0.02% | USD/barrel | FXDailyReport [2026-05-19 ET 종가] | 2026-05-20T09:10:00+09:00 | 이란 협상 진전 소식 → 소폭 하락. $100 이상 고착 구조 유지 |
| 2026-05-19 | commodity | Copper | 6.25 | -0.43% | USD/lb | TradingEconomics [2026-05-19 ET 종가] | 2026-05-20T09:10:00+09:00 | ⚠️ 중국 소매판매·산업생산 예상 하회 → 수요 우려. 2주 내 저점 |
| 2026-05-19 | crypto | BTC | 76565 | -0.6% | USD | Yahoo Finance [2026-05-19 ET 09:30] | 2026-05-20T09:10:00+09:00 | 5/1 이후 최저 개장. 미-이란 결과 관망 |
| 2026-05-19 | crypto | ETH | 2116.81 | 보합 | USD | Fortune [2026-05-19 ET 17:02] | 2026-05-20T09:10:00+09:00 | 4/7 이후 최저 개장가. BTC 대비 상대 약세 지속 |
| 2026-05-19 | crypto | FearAndGreedIndex_CNN | 61 | — | index | CNN Fear&Greed [2026-05-19] | 2026-05-20T09:10:00+09:00 | 탐욕(Greed) 구간. 주식 F&G는 크립토 F&G(34 Fear)와 디커플 |
| 2026-05-20 | asia_index | KOSPI | 7425.66 | 개장기준 | point | CNBC Asia [2026-05-20 KST 09:00 개장] | 2026-05-20T09:10:00+09:00 | 미국 3연속 하락 속 개장. 이란 리스크 완화 상쇄 효과 |
| 2026-05-20 | asia_index | KOSDAQ | 1122.57 | 개장기준 | point | CNBC Asia [2026-05-20 KST 09:00 개장] | 2026-05-20T09:10:00+09:00 | D-1 대비 개장 소폭 강세 추정 |
| 2026-05-19 | asia_index | Nikkei225 | 60550.59 | — | point | Investtech Morning Report [2026-05-19 JST 종가] | 2026-05-20T09:10:00+09:00 | 5/20 장 진행 중 (KST 09:10 기준) |
| 2026-05-19 | asia_index | HangSeng | 25962.73 | — | point | Investtech Morning Report [2026-05-19 HKT 종가] | 2026-05-20T09:10:00+09:00 | 5/20 장 진행 중 (KST 09:10 기준) |
| 2026-05-19 | asia_index | ShanghaiComposite | 4169.54 | — | point | Investtech Morning Report [2026-05-19 CST 종가] | 2026-05-20T09:10:00+09:00 | 소매판매·산업생산 예상 하회 배경. 5/20 장 진행 중 |
| 2026-06-02 | us_index | SP500 | 7599.96 | +0.26% | point | CNBC/TheStreet [2026-06-01 ET 16:00 종가] | 2026-06-02T20:05:00+09:00 | D-1 종가. NVDA 신칩+ISM 54.0 → NASDAQ 27K 첫 돌파 신고가 |
| 2026-06-02 | us_index | NASDAQ | 27086.81 | +0.42% | point | CNBC/TheStreet [2026-06-01 ET 16:00 종가] | 2026-06-02T20:05:00+09:00 | D-1 종가. 27K 첫 돌파 사상 최고 |
| 2026-06-02 | us_index | DJIA | 51078.88 | +0.09% | point | CNBC/TheStreet [2026-06-01 ET 16:00 종가] | 2026-06-02T20:05:00+09:00 | D-1 종가 |
| 2026-06-02 | us_index | VIX | 16.05 | +1.84% | index | WebSearch 추정 [2026-06-02] | 2026-06-02T20:05:00+09:00 | 신고가 랠리에도 VIX 상승 = 하방 헤지 수요 증가 |
| 2026-06-02 | asia_index | KOSPI | 8801.49 | +0.15% | point | Investing.com/bloomingbit [2026-06-02 KST 15:30 종가] | 2026-06-02T20:05:00+09:00 | 사상 최고 신고가 |
| 2026-06-02 | asia_index | KOSDAQ | 1026.03 | -2.29% | point | Investing.com [2026-06-02 KST 15:30 종가] | 2026-06-02T20:05:00+09:00 | 5일 연속 하락. KOSPI-KOSDAQ 괴리 2.44%p |
| 2026-06-02 | asia_index | Nikkei225 | 66934.33 | — | point | 전일 수치 유지 (6/2 확인 미완) | 2026-06-02T20:05:00+09:00 | 미확인 — 재검증 필요 |
| 2026-06-02 | asia_index | HangSeng | 25757.04 | +1.41% | point | Google Finance/Investing.com [2026-06-02 HKT 종가] | 2026-06-02T20:05:00+09:00 | |
| 2026-06-02 | asia_index | ShanghaiComposite | — | — | point | 미수집 | 2026-06-02T20:05:00+09:00 | 웹검색 미확인 |
| 2026-06-02 | asia_index | SENSEX | 73937.37 | -0.44% | point | BusinessUpturn [2026-06-02 개장기준] | 2026-06-02T20:05:00+09:00 | 개장기준 — 종가 미확인 |
| 2026-06-02 | fx | USDKRW | 1518.82 | +0.33% | KRW | Wise/TradingEconomics [2026-06-02] | 2026-06-02T20:05:00+09:00 | ⚠️ 1400 초과. 수출 최고에도 이란 에너지 비용 압박 |
| 2026-06-02 | fx | USDJPY | 159.69 | +0.02% | JPY | TradingEconomics [2026-06-02] | 2026-06-02T20:05:00+09:00 | |
| 2026-06-02 | fx | DXY | 99.19 | +0.14% | pt | TradingEconomics [2026-06-02] | 2026-06-02T20:05:00+09:00 | 이란 재긴장 안전자산 수요 |
| 2026-06-02 | commodity | WTI | 92.08 | +1.38% | USD/barrel | Barchart/CNBC [2026-06-02] | 2026-06-02T20:05:00+09:00 | 이란 협상 중단 재선언. 범위 91.51~92.64 |
| 2026-06-02 | commodity | Brent | 93.71 | — | USD/barrel | CNBC [참조값, 5/28 기준] | 2026-06-02T20:05:00+09:00 | 정확한 6/2 수치 미수집 |
| 2026-06-02 | commodity | Gold | 4514.15 | -1.90% | USD/oz | Barchart/TradingEcon [2026-06-02] | 2026-06-02T20:05:00+09:00 | 전일 4534→4514. DXY 반등 압박 |
| 2026-06-02 | commodity | Copper | 6.56 | +0.57% | USD/lb | TradingEconomics [2026-06-02] | 2026-06-02T20:05:00+09:00 | 칠레 4월 생산 23년래 최저 공급 우려 |
| 2026-06-02 | bond | US10Y | 4.51 | +6bp | % | WebSearch [2026-06-02] | 2026-06-02T20:05:00+09:00 | ⚠️ 4.5% 초과. 베어 스티프닝 재가속 |
| 2026-06-02 | bond | US2Y | 4.04 | +5bp | % | WebSearch [2026-06-01 마감] | 2026-06-02T20:05:00+09:00 | |
| 2026-06-02 | bond | US30Y | 5.02 | — | % | WebSearch 추정 [2026-06-02] | 2026-06-02T20:05:00+09:00 | 30Y 5% 고착 지속 |
| 2026-06-02 | bond | Spread2Y10Y | 0.47 | — | %p | 계산값 (4.51-4.04) | 2026-06-02T20:05:00+09:00 | 정상 수익률 곡선 유지 |
| 2026-06-02 | crypto | BTC | 72800 | 약보합 | USD | FXStreet/CoinGecko추정 [2026-06-02 KST 20:05] | 2026-06-02T20:05:00+09:00 | $73K 하회 시 $70K 재테스트 우려 |
| 2026-06-02 | crypto | ETH | 1980 | — | USD | FXStreet [2026-06-02] | 2026-06-02T20:05:00+09:00 | $2,000 지지선 테스트 |
| 2026-06-02 | crypto | SOL | 80 | — | USD | FXStreet [2026-06-02] | 2026-06-02T20:05:00+09:00 | $115M 유입 SOL 상대 견조 |
| 2026-06-02 | us_index | SP500 | 7609.78 | +0.13% | point | TheStreet [6/2 ET 16:00 종가 = KST 6/3 05:00] | 2026-06-03T09:11:00+09:00 | 7,600 첫 돌파 신고가 |
| 2026-06-02 | us_index | NASDAQ | 27093.00 | +0.03% | point | TheStreet [6/2 ET 16:00 종가] | 2026-06-03T09:11:00+09:00 | 신고가 |
| 2026-06-02 | us_index | DJIA | 51307.79 | +0.45% | point | TheStreet [6/2 ET 16:00 종가] | 2026-06-03T09:11:00+09:00 | |
| 2026-06-02 | us_index | Russell2000 | — | — | point | 미수집 | 2026-06-03T09:11:00+09:00 | 웹검색 미확인 |
| 2026-06-02 | us_index | VIX | 15.5 | — | index | 추정 (FRED 5/28=15.74, 6/1=16.05 사이) | 2026-06-03T09:11:00+09:00 | 직접 수치 미확인 — 추정값 |
| 2026-06-02 | fx | DXY | 99.09 | -0.11% | pt | TradingEcon [6/2 ET 종가] | 2026-06-03T09:11:00+09:00 | 이란 소강 달러 소폭 후퇴 |
| 2026-06-02 | commodity | WTI | 91.97 | -0.20% | USD/barrel | TradingEcon/Fortune [6/2 ET 종가] | 2026-06-03T09:11:00+09:00 | 전일 급등 후 이란 소강 되돌림 |
| 2026-06-02 | commodity | Brent | 94.58 | -0.42% | USD/barrel | TradingEcon [6/2 ET 종가] | 2026-06-03T09:11:00+09:00 | |
| 2026-06-02 | commodity | Gold | 4494.61 | +0.21% | USD/oz | TradingEcon [6/2 ET 종가] | 2026-06-03T09:11:00+09:00 | $4,500 재근접 |
| 2026-06-02 | bond | US10Y | 4.46 | -5bp | % | TradingEcon [6/2 ET 종가] | 2026-06-03T09:11:00+09:00 | 장중 4.51% 고점 후 마감 후퇴 |
| 2026-06-02 | bond | US2Y | 4.03 | -1bp | % | TradingEcon [6/2 ET 종가] | 2026-06-03T09:11:00+09:00 | |
| 2026-06-02 | bond | Spread2Y10Y | 0.43 | — | %p | 계산값 (4.46-4.03) | 2026-06-03T09:11:00+09:00 | |
| 2026-06-03 | crypto | BTC | 72661 | -1.0% | USD | milkroad/CoinGecko추정 [6/3 KST 09:11] | 2026-06-03T09:11:00+09:00 | |
| 2026-06-03 | crypto | ETH | 1977 | -0.90% | USD | CoinGecko추정 [6/3 KST 09:11] | 2026-06-03T09:11:00+09:00 | |
| 2026-06-03 | crypto | SOL | 82.44 | -0.80% | USD | CoinGecko/Coinbase [6/3 KST 09:11] | 2026-06-03T09:11:00+09:00 | |
| 2026-06-03 | asia_index | KOSPI | 8801.49 | +0.15% | point | Investing.com/BusinessKorea [6/3 KST 15:30] | 2026-06-03T20:10:00+09:00 | 역대 최고 신고가 — 삼성전자+3.15% SK스퀘어+6.13% AI반도체 견인 |
| 2026-06-03 | asia_index | KOSDAQ | — | — | point | 미수집 — 6/2 1026.03 참조 | 2026-06-03T20:10:00+09:00 | 6/3 종가 웹검색 미확인 |
| 2026-06-03 | asia_index | Nikkei225 | 68634 | +2.94% | point | AP/News4Jax [6/3 일본장 오후] | 2026-06-03T20:10:00+09:00 | 68,000 첫 돌파 신고가 — 도쿄일렉트론+13.4% |
| 2026-06-03 | asia_index | HangSeng | 25597 | -1.73% | point | CNBC Asia [6/3] | 2026-06-03T20:10:00+09:00 | WTI급등·이란 지정학 반영 하락 |
| 2026-06-03 | asia_index | Shanghai | 4069 | -0.20% | point | CNBC Asia [6/3] | 2026-06-03T20:10:00+09:00 | 소폭 하락 |
| 2026-06-03 | fx | USDKRW | 1527.34 | +0.67% | KRW | exchange-rates.org/TradingEcon [6/3] | 2026-06-03T20:10:00+09:00 | ⚠️ 1,400 초과 — 이란 교착+WTI$95 복합 원화 약세 가속 |
| 2026-06-03 | fx | USDJPY | 160.0 | +0.2% | JPY | AP/Reuters [6/3] | 2026-06-03T20:10:00+09:00 | 160엔 일시 돌파 — 엔화 역대급 약세 재진입 |
| 2026-06-03 | commodity | WTI | 95.0 | +3.2% | USD/barrel | Investing.com/OilpriceAPI [6/3 ET 프리마켓] | 2026-06-03T20:10:00+09:00 | ⚠️ 이란 핵협상 단절+미군 Qeshm공습 — 3일연속 상승 |
| 2026-06-03 | commodity | Gold | 4457 | -0.74% | USD/oz | 150currency.com/TradingEcon [6/3 ET 05:57] | 2026-06-03T20:10:00+09:00 | $4,500 하향 이탈 — 달러강세 압박 |
| 2026-06-03 | bond | US10Y | 4.45 | 0bp | % | TradingEcon/FRED폴백 [6/3 프리마켓] | 2026-06-03T20:10:00+09:00 | WTI$95 인플레 재가속 압박 — 4.45% 고착 |
| 2026-06-03 | bond | US2Y | 4.03 | 0bp | % | 6/2 종가 유지 [추정] | 2026-06-03T20:10:00+09:00 | |
| 2026-06-03 | bond | Spread2Y10Y | 0.42 | — | %p | 계산값 (4.45-4.03) | 2026-06-03T20:10:00+09:00 | |
| 2026-06-03 | us_index | SP500_futures | -0.10% | — | pct | Benzinga/Reuters [6/3 ET 07:00 프리마켓] | 2026-06-03T20:10:00+09:00 | ⚠️ 프리마켓 추정 — 정규장 종가 아님 |
| 2026-06-03 | crypto | BTC | 67089 | -6.0% | USD | Yahoo Finance [6/3 ET 06:53] | 2026-06-03T20:10:00+09:00 | ⚠️ $70K 지지선 붕괴 — 리스크오프 가속 |
| 2026-06-03 | crypto | ETH | 1922 | -2.8% | USD | Yahoo Finance [6/3] | 2026-06-03T20:10:00+09:00 | |
| 2026-06-03 | crypto | CryptoFG | 29 | — | index | milkroad [6/2~3] | 2026-06-03T20:10:00+09:00 | Fear 공포권 유지 |
| 2026-06-04 | us_index | SP500 | 7584.31 | +0.41% | point | Yahoo Finance [6/4 ET 16:00 종가 / KST 6/5 05:00] | 2026-06-05T20:07:00+09:00 | AVGO -12.59% 충격에도 Dow +1.73% 신기록 — 기술→가치 대로테이션 |
| 2026-06-04 | us_index | NASDAQ | 26830.96 | -0.09% | point | Yahoo Finance [6/4 ET 16:00 종가] | 2026-06-05T20:07:00+09:00 | AVGO·반도체 투매 — NASDAQ 소폭 하락 |
| 2026-06-04 | us_index | DowJones | 51561.93 | +1.73% | point | Yahoo Finance [6/4 ET 16:00 종가] | 2026-06-05T20:07:00+09:00 | ⚠️ 신고가 — 8개 섹터 동반 상승 |
| 2026-06-05 | asia_index | KOSPI | 8160.59 | -5.54% | point | Yahoo Finance [6/5 KST 15:30 종가] | 2026-06-05T20:07:00+09:00 | ⚠️ 매도사이드카 09:08 발동. 장중 최저 8,057(-6.73%). 갭업(8,883) 후 급반전 |
| 2026-06-05 | asia_index | KOSDAQ | 1002.44 | -2.30% | point | Yahoo Finance [6/5 KST 15:30 종가] | 2026-06-05T20:07:00+09:00 | 1,000pt 간신히 방어 |
| 2026-06-05 | asia_index | Nikkei225 | 66588.12 | -1.31% | point | Yahoo Finance [6/5 일본장 종가] | 2026-06-05T20:07:00+09:00 | 갭업 +2.06% 개장 후 되돌림 — 전일(68,634) 대비 -2.99% |
| 2026-06-05 | asia_index | HangSeng | 24961.95 | -1.15% | point | Yahoo Finance [6/5 홍콩장 종가] | 2026-06-05T20:07:00+09:00 | |
| 2026-06-05 | asia_index | Shanghai | 4028 | -0.74% | point | Trading Economics [웹검색] | 2026-06-05T20:07:00+09:00 | |
| 2026-06-05 | fx | USDKRW | 1538.58 | +0.55% | KRW | Yahoo Finance [6/5 KST] | 2026-06-05T20:07:00+09:00 | ⚠️ 1,400 초과 — 원화 약세 지속 |
| 2026-06-05 | fx | DXY | 99.19 | -0.22% | index | Yahoo Finance [6/5] | 2026-06-05T20:07:00+09:00 | 달러 소폭 약세에도 KRW 약세 — 한국 고유 리스크 |
| 2026-06-05 | fx | USDJPY | 159.90 | -0.03% | JPY | Yahoo Finance [6/5] | 2026-06-05T20:07:00+09:00 | 160엔 턱밑 |
| 2026-06-05 | commodity | WTI | 92.90 | -0.15% | USD/barrel | Yahoo Finance [6/5] | 2026-06-05T20:07:00+09:00 | 이스라엘-레바논 휴전 지속 — $95.50 대비 하락 |
| 2026-06-05 | commodity | Gold | 4493.20 | +0.39% | USD/oz | Yahoo Finance [6/5] | 2026-06-05T20:07:00+09:00 | $4,500 직전 — 지정학 불확실성 지지 |
| 2026-06-05 | bond | US10Y | 4.46 | -4bp | % | 웹검색 Trading Economics [6/5] | 2026-06-05T20:07:00+09:00 | fetch_price 4.48(6/4) / 웹검색 4.46(6/5) — 범위 4.46~4.48 |
| 2026-06-05 | bond | US2Y | 4.04 | -1bp | % | 웹검색 Trading Economics / FRED DGS2 [6/5] | 2026-06-05T20:07:00+09:00 | |
| 2026-06-05 | bond | Spread2Y10Y | 0.44 | — | %p | 계산값 (4.48-4.04) | 2026-06-05T20:07:00+09:00 | 정상곡선 유지 |
| 2026-06-05 | us_index | VIX | 15.65 | +1.62% | index | Yahoo Finance [6/5] | 2026-06-05T20:07:00+09:00 | KOSPI -5.54% 대비 미국 공포 미반영 — 디버전스 |
| 2026-06-05 | us_index | SP500_futures | -0.61% | — | pct | Yahoo Finance/StockTwits [6/5 ET 07:00 프리마켓] | 2026-06-05T20:07:00+09:00 | ⚠️ 프리마켓 — 정규장 종가 아님. NFP(08:30 ET) 발표 대기 |
| 2026-06-05 | crypto | BTC | 62355 | -2.27% | USD | Yahoo Finance [6/5 KST 20:07] | 2026-06-05T20:07:00+09:00 | ⚠️ $65K 지지 실패. BTC ETF 13일 연속 유출 누적 -$4.4B |
| 2026-06-05 | crypto | ETH | 1671 | -5.57% | USD | Yahoo Finance [6/5 KST 20:07] | 2026-06-05T20:07:00+09:00 | BTC 대비 더 큰 낙폭 |
| 2026-06-23 | us_index | SP500 | 7365.32 | -1.44% | point | TheStreet/Yahoo Finance [2026-06-23 ET 16:00 종가 / KST 6/24 05:00] | 2026-06-24T09:10:00+09:00 | ⚠️ KOSPI 서킷브레이커 전파 + BoFA 3회 금리인상 경고 — 기술주 이틀째 급락 |
| 2026-06-23 | us_index | NASDAQ | 25587.00 | -2.21% | point | TheStreet/Yahoo Finance [2026-06-23 ET 16:00 종가] | 2026-06-24T09:10:00+09:00 | ⚠️ 580pt 급락 — NVDA -4.13%, GOOGL -1.02%, SOX 동반 하락 |
| 2026-06-23 | us_index | DowJones | 51413.00 | -0.58% | point | TheStreet [2026-06-23 ET 16:00 종가] | 2026-06-24T09:10:00+09:00 | 기술주 대비 방어적 낙폭 |
| 2026-06-23 | us_index | Russell2000 | 3028.93 | +0.83% | point | Yahoo Finance [2026-06-23 ET 16:00 종가] | 2026-06-24T09:10:00+09:00 | 나홀로 반등 — 빅테크 회피 + 중소형주 섹터 로테이션 |
| 2026-06-23 | us_index | VIX | 19.49 | +12.79% | index | Yahoo Finance [2026-06-23 ET 종가] | 2026-06-24T09:10:00+09:00 | ⚠️ 20 턱밑 — 이틀째 급등 |
| 2026-06-23 | us_stock | NVDA | — | -4.13% | % | Yahoo Finance [2026-06-23 ET 종가] | 2026-06-24T09:10:00+09:00 | AI capex 회의론 주도 |
| 2026-06-23 | us_stock | GOOGL | 346.14 | -1.02% | USD | Yahoo Finance [2026-06-23 ET 종가] | 2026-06-24T09:10:00+09:00 | DeepMind VP John Jumper Anthropic 이직 — AI 인재 이탈 2일차 |
| 2026-06-23 | us_stock | SPCX | — | -16.50% | % | Yahoo Finance/CNBC [2026-06-23 ET 종가] | 2026-06-24T09:10:00+09:00 | ⚠️ $25B 채권 발행(IPO 11일 만) — 순환금융 신용 균열 우려 |
| 2026-06-23 | fx | USDKRW | 1535.25 | — | KRW | Investing.com [2026-06-23] | 2026-06-24T09:10:00+09:00 | ⚠️ 1,400 초과 지속 |
| 2026-06-23 | fx | DXY | 101.00 | — | index | TradingEconomics [2026-06-23 ET 종가] | 2026-06-24T09:10:00+09:00 | ⚠️ 2025년 5월 이후 최고치 — BoFA 금리인상 경고 달러 강세 |
| 2026-06-23 | fx | USDJPY | 161.47 | — | JPY | 2026-06-23 | 2026-06-24T09:10:00+09:00 | 달러 강세 지속 |
| 2026-06-23 | commodity | WTI | 73.40 | — | USD/barrel | TradingEconomics [2026-06-23 ET] | 2026-06-24T09:10:00+09:00 | 미-이란 협상 진전으로 하락 |
| 2026-06-23 | commodity | Gold | 4129.07 | -1.49% | USD/oz | 150currency.com [2026-06-23 ET] | 2026-06-24T09:10:00+09:00 | 달러 강세 압박 — 리스크오프에도 하락 |
| 2026-06-23 | bond | US10Y | 4.48 | — | % | TradingEconomics/CNBC [2026-06-23 ET] | 2026-06-24T09:10:00+09:00 | BoFA 금리인상 경고 반영 상승 |
| 2026-06-23 | bond | US2Y | 4.19 | — | % | FRED DGS2 [2026-06-18 최신] | 2026-06-24T09:10:00+09:00 | FRED 미갱신 — 추정 유지 |
| 2026-06-23 | bond | Spread2Y10Y | 0.29 | — | %p | 계산값 (4.48-4.19) | 2026-06-24T09:10:00+09:00 | 정상곡선 유지 |
| 2026-06-24 | crypto | BTC | 64207.80 | — | USD | CoinGecko 추정 [KST 6/24 오전] | 2026-06-24T09:10:00+09:00 | 전일 급락 후 기술적 반등 |
| 2026-06-24 | crypto | ETH | 1747.35 | — | USD | CoinGecko 추정 [KST 6/24 오전] | 2026-06-24T09:10:00+09:00 | |
| 2026-06-24 | crypto | SOL | 73.80 | — | USD | CoinGecko 추정 [KST 6/24 오전] | 2026-06-24T09:10:00+09:00 | |
| 2026-06-24 | sentiment | FearGreed_stock | 27.5 | — | index | regime.json 자동수집 [KST 6/24] | 2026-06-24T09:10:00+09:00 | Fear — 전일 34.7 → 급하락 |
| 2026-06-24 | sentiment | FearGreed_crypto | 20 | — | index | Milkroad [6/23 기준] | 2026-06-24T09:10:00+09:00 | Extreme Fear 유지 |
| 2026-06-29 | asia_index | KOSPI | ~8333 | ~-1.0% | point | AsiaE / Sunday Guardian Live [2026-06-29 장중 KST 10:00 기준 — 확정 종가 미수집] | 2026-06-29T20:05:00+09:00 | ⚠️ 반등 실패. 삼성 -4.1%, SK하이닉스 -3.3%. D-1 8,411 대비 추가 하락. 이재명 2,000조 AI 투자계획 발표 앞두고 차익실현 우세 |
| 2026-06-29 | asia_index | KOSDAQ | ~900.68 | +5.79% | point | AsiaE [2026-06-29 장중] | 2026-06-29T20:05:00+09:00 | ⚠️ KOSPI vs KOSDAQ 극단 디버전스 — 중소형 성장주·바이오 순환매 |
| 2026-06-29 | asia_index | Nikkei225 | 68563.45 | -1.15% | point | Investtech Morning Report [2026-06-29 종가] | 2026-06-29T20:05:00+09:00 | SoftBank 여진 지속. D-1 69,360 대비 추가 하락 |
| 2026-06-29 | asia_index | HangSeng | 23075.84 | +1.78% | point | Investtech Morning Report [2026-06-29 종가] | 2026-06-29T20:05:00+09:00 | 미-이란 stand down 수혜. D-1 22,671 대비 반등 |
| 2026-06-29 | asia_index | Shanghai | 4027.27 | -2.26% | point | Investtech Morning Report [2026-06-29 종가] | 2026-06-29T20:05:00+09:00 | 추가 하락 |
| 2026-06-29 | us_index | SP500_futures | +0.8% | — | pct | CNBC / TheStreet [2026-06-29 ET 07:05 프리마켓] | 2026-06-29T20:05:00+09:00 | ⚠️ 프리마켓 — 정규장 종가 아님. 미-이란 호르무즈 stand down + 기술주 반등 기대 |
| 2026-06-29 | us_index | NASDAQ_futures | +1.2% | — | pct | CNBC [2026-06-29 ET 07:05 프리마켓] | 2026-06-29T20:05:00+09:00 | ⚠️ 프리마켓. 5연속 하락 후 기술주 반등 시도 |
| 2026-06-29 | us_index | Dow_futures | +188pt (+0.4%) | — | pt | CNBC [2026-06-29 ET 07:05 프리마켓] | 2026-06-29T20:05:00+09:00 | ⚠️ 프리마켓. Comcast +25% 분사 발표 부스트 |
| 2026-06-29 | fx | USDKRW | 1543.05 | +0.52% | KRW | ExchangeRates.org.uk [2026-06-29 아시아장] | 2026-06-29T20:05:00+09:00 | ⚠️ 1,400 초과 지속. 장중 1,536~1,549 범위 |
| 2026-06-29 | commodity | WTI | 70.79 | +2.8% | USD/barrel | TradingEconomics [2026-06-29 오픈/장중] | 2026-06-29T20:05:00+09:00 | 미-이란 호르무즈 통항 재개 합의 반등. D-1 $68.86 대비 |
| 2026-06-29 | commodity | Brent | ~72+ | — | USD/barrel | TradingEconomics [2026-06-29 장중] | 2026-06-29T20:05:00+09:00 | 4개월 저점 후 반등 |
| 2026-06-29 | commodity | Gold | ~4044 | -1.0% | USD/oz | LiteFinance [2026-06-29] | 2026-06-29T20:05:00+09:00 | 안전자산 선호 완화. D-1 $4,078 대비 하락 |
| 2026-06-29 | bond | US10Y | 4.37 | -3bp | % | FRED DGS10 [2026-06-26 확정] | 2026-06-29T20:05:00+09:00 | D-1 스냅샷 4.40% 대비 소폭 하향 조정 |
| 2026-06-29 | bond | US2Y | 4.10 | — | % | FRED DGS2 [2026-06-26 확정] | 2026-06-29T20:05:00+09:00 | |
| 2026-06-29 | bond | Spread2Y10Y | 0.27 | — | %p | FRED T10Y2Y [2026-06-26 확정] | 2026-06-29T20:05:00+09:00 | 정상곡선 유지 |
| 2026-06-29 | crypto | BTC | 60357 | — | USD | CoinStats [2026-06-29 KST 20:05] | 2026-06-29T20:05:00+09:00 | $60K 경계선 유지. Q2 손실 지속 우려 |
| 2026-06-29 | crypto | ETH | 1565 | — | USD | Changelly [2026-06-29] | 2026-06-29T20:05:00+09:00 | BTC 동조 |
| 2026-06-29 | crypto | SOL | 71.42 | — | USD | Paybis [2026-06-29] | 2026-06-29T20:05:00+09:00 | |
| 2026-06-29 | sentiment | FearGreed_stock | 25 | — | index | CNN / FearGreedMeter [2026-06-29] | 2026-06-29T20:05:00+09:00 | ⚠️ Fear — 기준선 25 접촉. 모닝과 동일 |
| 2026-06-29 | sentiment | FearGreed_crypto | 36 | — | index | Milkroad / CFGI [2026-06-29] | 2026-06-29T20:05:00+09:00 | Fear. 6/26 25 → 6/29 36 소폭 회복 |
| 2026-07-06 | asia_index | KOSPI | 8051.33 | -0.46% | point | 이투데이/서울경제/fnnews [2026-07-06 15:30 마감] | 2026-07-06T20:10:00+09:00 | 개인 +2.68조 매수 vs 외국인 -1.31조·기관 -1.47조 매도. 장중 고점 8327.26→저점 7815.53 극심한 변동성 |
| 2026-07-06 | asia_index | KOSDAQ | 847.07 | -2.46% | point | 이투데이 [2026-07-06 15:30 마감] | 2026-07-06T20:10:00+09:00 | KOSPI보다 낙폭 확대. 전자장비·전기제품·제약 약세 |
| 2026-07-06 | asia_index | 삼성전자 | 318000 | +2.75% | KRW | 서울경제 [2026-07-06 15:30 마감] | 2026-07-06T20:10:00+09:00 | 7/7 2분기 잠정실적 발표 앞두고 강세 |
| 2026-07-06 | asia_index | SK하이닉스 | 2340000 | -3.38% | KRW | 서울경제 [2026-07-06 15:30 마감] | 2026-07-06T20:10:00+09:00 | ADR 나스닥 상장 이벤트 앞두고 조정, 삼성전자와 디커플링 |
| 2026-07-06 | asia_index | Nikkei225 | 69737.69 | -0.01% | point | 이투데이 [2026-07-06 마감] | 2026-07-06T20:10:00+09:00 | 보합권. 도쿄일렉트론·어드반테스트 약세 주도 |
| 2026-07-06 | asia_index | Shanghai | ~4054 | -0.06% | point | Investing.com/이투데이 [2026-07-06 마감] | 2026-07-06T20:10:00+09:00 | 소폭 조정 |
| 2026-07-06 | asia_index | HangSeng | — | +1.04% | pct | 이투데이 [2026-07-06 KST 16:50 기준] | 2026-07-06T20:10:00+09:00 | 저가매수+기술소비주 반등. 종가 포인트 미확인 |
| 2026-07-06 | asia_index | TAIEX | 46556.39 | -0.48% | point | 이투데이 [2026-07-06 마감] | 2026-07-06T20:10:00+09:00 | TSMC 랠리 이후 숨고르기 |
| 2026-07-06 | us_index | SP500_futures | +0.5% | — | pct | CNBC [2026-07-06 ET 07시 무렵 프리마켓] | 2026-07-06T20:10:00+09:00 | ⚠️ 프리마켓 — 정규장 재개 전(22:30 KST). Foxconn 실적 서프라이즈 부스트 |
| 2026-07-06 | us_index | NASDAQ100_futures | +1.1% | — | pct | CNBC [2026-07-06 ET 07시 무렵 프리마켓] | 2026-07-06T20:10:00+09:00 | ⚠️ 프리마켓. NVDA +0.3%, AAPL -0.8% 오버나이트 |
| 2026-07-06 | fx | USDKRW | 1530.30 | +4.70원 | KRW | fnnews [2026-07-06 서울외환 마감] | 2026-07-06T20:10:00+09:00 | 24시간 거래 첫날(월 06시~토 06시 무중단) |
| 2026-07-06 | fx | DXY | 101.07 | +0.21% | index | streetstats/tradingeconomics [2026-07-06] | 2026-07-06T20:10:00+09:00 | |
| 2026-07-06 | commodity | WTI | 68.70 | +0.18% | USD/barrel | EBN [2026-07-06] | 2026-07-06T20:10:00+09:00 | $68선 안정 유지 |
| 2026-07-06 | commodity | Gold | 4195.30 | +1.69% | USD/oz | EBN [2026-07-06] | 2026-07-06T20:10:00+09:00 | 고용둔화發 금리인하 기대+달러약세 |
| 2026-07-06 | crypto | BTC | 62749.64 | +0.15% | USD | TokenPost 자정브리핑 [2026-07-06 00:07 KST] | 2026-07-06T20:10:00+09:00 | ⚠️ 20시 갱신치 미확보(인덱싱 지연), 자정치 유지 |
| 2026-07-06 | crypto | ETH | 1770.23 | -0.08% | USD | TokenPost 자정브리핑 [2026-07-06 00:07 KST] | 2026-07-06T20:10:00+09:00 | |
| 2026-07-06 | crypto | SOL | 80.14 | — | USD | Investing.com [2026-07-06 09:00 무렵] | 2026-07-06T20:10:00+09:00 | 등락률 미표기 |
| 2026-07-06 | sentiment | FearGreed_crypto | 24 | — | index | fear_greed.json 자동갱신 [2026-07-06 09:27 KST] | 2026-07-06T20:10:00+09:00 | Extreme Fear 지속 |
| 2026-07-06 | sentiment | FearGreed_stock | 31.9 | — | index | fear_greed.json 자동갱신 [source_ts 2026-07-03] | 2026-07-06T20:10:00+09:00 | Fear. source_ts 3일 경과 stale 가능성 |
| 2026-07-15 | asia_index | KOSPI | 7284.41 | +6.24% | point | 이투데이/뉴스핌/포쓰저널 [2026-07-15 KRX 15:30 마감] + yfinance ^KS11 교차검증 | 2026-07-15T20:05:00+09:00 | 서킷브레이커 후 급반등. 외국인 +2조3227억·기관 +1827억 순매수, 개인 -2조4680억 순매도. 미 6월 CPI 서프라이즈(컨센 하회) 여진 |
| 2026-07-15 | asia_index | KOSDAQ | 829.43 | +5.80% | point | 뉴스핌 [2026-07-15 15:30 마감] + yfinance ^KQ11 교차검증 | 2026-07-15T20:05:00+09:00 | 외국인 +231억·기관 +1085억 순매수, 개인 -1407억 순매도 |
| 2026-07-15 | asia_index | Nikkei225 | 68751.51 | +3.27% | point | yfinance ^N225 [2026-07-15 종가, 전일(7/14) 66574.96 대비 계산] | 2026-07-15T20:05:00+09:00 | CPI 서프라이즈發 아시아 리스크온 동반 |
| 2026-07-15 | asia_index | Shanghai | 3955.58 | +1.83% | point | yfinance 000001.SS [2026-07-15 종가, 전일(7/14) 3884.32 대비 계산] | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-15 | asia_index | HangSeng | 24681.10 | +1.86% | point | yfinance ^HSI [2026-07-15 종가, 전일(7/14) 24230.46 대비 계산] | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-15 | asia_index | Sensex | 77185.43 | -0.56%(잠정) | point | yfinance ^BSESN [2026-07-15 종가, 7/13 종가 77616.40 대비 계산 — 7/14 기준값 KB 미보유] | 2026-07-15T20:05:00+09:00 | ⚠️ WebSearch 별도소스 77054.94(-0.72%) 보도 — 소스간 편차, 익일 재검증 필요. 유가 상승 우려로 나홀로 약세 |
| 2026-07-15 | us_index | SP500_futures | 7601.50 | +0.14% | point | yfinance ES=F [2026-07-15 ET 07:05(KST 20:05) 프리마켓] | 2026-07-15T20:05:00+09:00 | ⚠️ 프리마켓 — 정규장 시작 전(22:30 KST, 2.5시간 후). 확정 종가 아님 |
| 2026-07-15 | us_index | NASDAQ100_futures | 29927.75 | +0.46% | point | yfinance NQ=F [2026-07-15 ET 07:05 프리마켓] | 2026-07-15T20:05:00+09:00 | ⚠️ 프리마켓 |
| 2026-07-15 | us_index | Dow_futures | 52806 | +0.03% | point | yfinance YM=F [2026-07-15 ET 07:05 프리마켓] | 2026-07-15T20:05:00+09:00 | ⚠️ 프리마켓 |
| 2026-07-15 | us_stock | ASML | — | +4%(프리마켓) | pct | Seeking Alpha/MarketScreener [2026-07-15 ET 프리마켓] | 2026-07-15T20:05:00+09:00 | 개장전 Q2 실적발표 앞두고 매출·가이던스 상향 기대 선반영 |
| 2026-07-14 | us_index | SP500 | 7543.59 | +0.38% | point | Yahoo Finance/CNBC [2026-07-14 ET 16:00 종가] | 2026-07-15T20:05:00+09:00 | 6월 CPI 서프라이즈(헤드라인 -0.4%MoM,+3.5%YoY vs 컨센+3.8%)+JPM·GS 등 대형은행 실적 서프라이즈 |
| 2026-07-14 | us_index | NASDAQ | 26107.01 | +0.90% | point | Yahoo Finance/CNBC [2026-07-14 ET 16:00 종가] | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-14 | us_index | DJIA | 52508.27 | +0.02%(+9.63pt) | point | Yahoo Finance/CNBC [2026-07-14 ET 16:00 종가] | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-14 | us_index | VIX | 16.50 | -3.85% | index | Yahoo Finance [2026-07-14 ET 16:00 종가] | 2026-07-15T20:05:00+09:00 | 리스크온 재개 |
| 2026-07-15 | fx | USDKRW | ~1489~1494 | — | KRW | yfinance KRW=X [2026-07-15 KST 20:05 스냅샷, 세션 1484.28~1496.50] | 2026-07-15T20:05:00+09:00 | ⚠️ 변동 중 — 서울외환 마감 확정치 아님. 1400 초과 지속 |
| 2026-07-15 | fx | DXY | 100.995 | — | index | yfinance DX-Y.NYB [2026-07-15 스냅샷] | 2026-07-15T20:05:00+09:00 | 7/13 종가 101.28 대비 하락 |
| 2026-07-14 | fx | USDJPY | 162.27 | -0.15% | JPY | TradingEconomics/Xe [2026-07-14 확정 종가] | 2026-07-15T20:05:00+09:00 | 40년래 최저권 지속 |
| 2026-07-15 | commodity | WTI | 79.98 | — | USD/barrel | yfinance CL=F [2026-07-15 스냅샷] | 2026-07-15T20:05:00+09:00 | 7/14 종가 79.34 대비 소폭 상승 |
| 2026-07-15 | commodity | Brent | 85.49 | — | USD/barrel | yfinance BZ=F [2026-07-15 스냅샷] | 2026-07-15T20:05:00+09:00 | 3거래일 연속 상승 — 이란-호르무즈 리스크 프리미엄 |
| 2026-07-15 | commodity | Gold | 4033.80 | -0.67% | USD/oz | yfinance GC=F [2026-07-15 스냅샷, 7/14 종가 4061.10 대비] | 2026-07-15T20:05:00+09:00 | CPI 서프라이즈에도 조정 — 금리인하 기대 약화 해석 |
| 2026-07-15 | commodity | Silver | 58.33 | — | USD/oz | yfinance SI=F [2026-07-15 스냅샷] | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-15 | commodity | Copper | 6.36 | — | USD/lb | yfinance HG=F [2026-07-15 스냅샷] | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-14 | bond | US10Y | 4.583 | -2bp | % | Bloomberg/CNBC [2026-07-14 확정, CPI 반응] | 2026-07-15T20:05:00+09:00 | 4.5% 이상 — 임계 유지 |
| 2026-07-14 | bond | US2Y | 4.185 | -7bp | % | Bloomberg [2026-07-14 확정] | 2026-07-15T20:05:00+09:00 | ⚠️ 일부 소스 -14bp(4.14%) 보도 — 편차 유의 |
| 2026-07-14 | bond | US30Y | 5.096 | -1bp미만 | % | Bloomberg [2026-07-14 확정] | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-14 | bond | Spread2Y10Y | 0.398 | — | %p | 계산값(4.583-4.185) | 2026-07-15T20:05:00+09:00 | 정상곡선 유지, 역전 아님 |
| 2026-07-15 | bond | HY_OAS | 2.74 | — | % | TradingEconomics ICE BofA US HY OAS [2026-07] | 2026-07-15T20:05:00+09:00 | 역사적으로 타이트한 수준(저 percentile) |
| 2026-07-15 | crypto | BTC | 64750.79 | +3.57% | USD | 시장집계(CoinGecko류) [2026-07-15 KST 20:05 무렵, 24h] | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-15 | crypto | ETH | 1874.42 | +4.89% | USD | 상동 | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-15 | crypto | SOL | 77.54 | +2.91% | USD | 상동 | 2026-07-15T20:05:00+09:00 | — |
| 2026-07-15 | crypto | TotalMarketCap | 2.3e12 | +3.2%(24h) | USD | 상동 | 2026-07-15T20:05:00+09:00 | 24h 거래량 $70.6B |
| 2026-07-14 | sentiment | FearGreed_stock | 44 | — | index | CNN Fear & Greed [2026-07-14 기준] | 2026-07-15T20:05:00+09:00 | Fear. 오늘(7/15) 갱신치 미확보 — 전일값 유지 |
| 2026-07-15 | sentiment | VIX_snapshot | 16.2~16.4 | — | index | yfinance ^VIX [2026-07-15 세션 16.19~16.43] | 2026-07-15T20:05:00+09:00 | ⚠️ 프리마켓 지표, 확정 아님 |
| 2026-07-15 | us_index | SP500 | 7572.40 | +0.38% | point | yfinance ^GSPC [2026-07-15 ET 16:00 종가] cross-check WebSearch(Yahoo Finance/thestreet.com) | 2026-07-16T09:10:00+09:00 | Apple 신고가(+4.01%, 중국 생성형AI 승인 보도)·ASML 가이던스 상향 견인 |
| 2026-07-15 | us_index | NASDAQ | 26269.23 | +0.62% | point | yfinance ^IXIC [2026-07-15 ET 16:00 종가] | 2026-07-16T09:10:00+09:00 | 메가캡 전반 강세(AAPL+4.01%,GOOGL+3.17%,META+3.07%,AMZN+3.02%,MSFT+2.78%) |
| 2026-07-15 | us_index | DJIA | 52658.64 | +0.29% | point | yfinance ^DJI [2026-07-15 ET 16:00 종가] | 2026-07-16T09:10:00+09:00 | — |
| 2026-07-15 | us_index | VIX | 15.67 | -5.03% | index | yfinance ^VIX [2026-07-15 ET 16:00 종가] | 2026-07-16T09:10:00+09:00 | 3거래일 연속 하락, 리스크온 심화 |
| 2026-07-15 | bond | US10Y | 4.545 | -4bp | % | yfinance ^TNX [2026-07-15 종가] cf. FRED DGS10 4.58%(2026-07-14) | 2026-07-16T09:10:00+09:00 | — |
| 2026-07-14 | bond | US2Y | 4.18 | — | % | [FRED: DGS2, 2026-07-14] | 2026-07-16T09:10:00+09:00 | ⚠️ yfinance 직접 미수집, FRED 1일 지연치 대체 |
| 2026-07-15 | bond | Spread2Y10Y | 0.42 | — | %p | [FRED: T10Y2Y, 2026-07-15] | 2026-07-16T09:10:00+09:00 | 정상곡선 유지 — yfinance 교차산출(0.365)과 편차, FRED 공식값 채택 |
| 2026-07-16 | fx | USDKRW | 1484.68 | -0.21% | KRW | yfinance KRW=X [2026-07-16 KST 09:10 스냅샷] | 2026-07-16T09:10:00+09:00 | ⚠️ 서울외환 개장전 스냅샷, 확정치 아님 — 점진적 안정화(7/14 1497.70→7/15 1487.88→7/16 1484.68) |
| 2026-07-15 | fx | DXY | 100.47 | -0.47% | index | yfinance DX-Y.NYB [2026-07-15 종가] | 2026-07-16T09:10:00+09:00 | — |
| 2026-07-15 | commodity | WTI | 80.15 | +1.02% | USD/barrel | yfinance CL=F [2026-07-15 종가] | 2026-07-16T09:10:00+09:00 | 호르무즈해협 리스크 프리미엄 지속 |
| 2026-07-15 | commodity | Gold | 4063.50 | +0.06% | USD/oz | yfinance GC=F [2026-07-15 종가] | 2026-07-16T09:10:00+09:00 | — |
| 2026-07-16 | crypto | BTC | 64742.00 | -0.33%(근사) | USD | yfinance BTC-USD [2026-07-16 KST 09:10 스냅샷] | 2026-07-16T09:10:00+09:00 | ⚠️ 7/15 일봉 데이터 결측, confidence medium |
| 2026-07-16 | crypto | ETH | 1920.99 | +1.67%(근사) | USD | yfinance ETH-USD [2026-07-16 KST 09:10 스냅샷] | 2026-07-16T09:10:00+09:00 | ⚠️ 7/15 일봉 데이터 결측, confidence medium |
| 2026-07-22 | asia_index | KOSPI | 6797.70 | +0.74% | point | yfinance(^KS11) [실측, 정규장 마감] | 2026-07-22T20:08:00+09:00 | 반도체 수출호조 랠리 연장 |
| 2026-07-22 | asia_index | KOSDAQ | 751.09 | -0.30% | point | yfinance(^KQ11) [실측, 정규장 마감] | 2026-07-22T20:08:00+09:00 | 소폭 되돌림 |
| 2026-07-22 | asia_index | Nikkei225 | 66115.60 | -0.18%(추정) | point | yfinance(^N225) [실측, KB확정 전일종가 대조] | 2026-07-22T20:08:00+09:00 | yfinance 캐시 전일종가와 0.25%p 상충 |
| 2026-07-22 | asia_index | ShanghaiComposite | 3867.03 | +0.06% | point | yfinance(000001.SS) [실측] | 2026-07-22T20:08:00+09:00 | 보합권 |
| 2026-07-22 | asia_index | HangSeng | 24892.66 | -0.95% | point | yfinance(^HSI) [실측] | 2026-07-22T20:08:00+09:00 | 반도체株 밸류에이션 경계감 |
| 2026-07-22 | asia_index | SENSEX | 76755.05 | -0.92% | point | yfinance(^BSESN) [실측] | 2026-07-22T20:08:00+09:00 | 반도체株 밸류에이션 경계감 |
| 2026-07-22 | us_index | SP500_futures | 7530.50 | -0.06%~-0.29% | point | yfinance(ES=F) + WebSearch(Benzinga ET05:39) [실측+인용] | 2026-07-22T20:08:00+09:00 | 프리마켓(ET07:08), 정규장 미개장 |
| 2026-07-22 | us_index | NASDAQ100_futures | 29155.75 | -0.14%~-0.71% | point | yfinance(NQ=F) + WebSearch(Benzinga ET05:39) [실측+인용] | 2026-07-22T20:08:00+09:00 | 반도체 냉각 반영 |
| 2026-07-22 | us_index | Dow_futures | 52424.00 | +0.08%~-0.09% | point | yfinance(YM=F) + WebSearch(Benzinga ET05:39) [실측+인용] | 2026-07-22T20:08:00+09:00 | 소스간 편차 |
| 2026-07-22 | us_index | VIX | 17.36 | +1.82% | index | yfinance(^VIX) [실측] | 2026-07-22T20:08:00+09:00 | 20 미만 유지 |
| 2026-07-22 | fx | USDKRW | 1479.20 | -0.06% | KRW | yfinance(KRW=X) [실측] | 2026-07-22T20:08:00+09:00 | 역외 실시간 |
| 2026-07-22 | fx | DXY | 101.16 | +0.01% | index | yfinance(DX-Y.NYB) [실측] | 2026-07-22T20:08:00+09:00 | 보합권 |
| 2026-07-22 | fx | USDJPY | 163.01 | -0.12% | JPY | yfinance(JPY=X) [실측] | 2026-07-22T20:08:00+09:00 | — |
| 2026-07-22 | commodity | WTI | 87.11 | +2.11% | USD/barrel | yfinance(CL=F) [실측] | 2026-07-22T20:08:00+09:00 | 후티 사우디 해상봉쇄·호르무즈 리스크 |
| 2026-07-22 | commodity | Gold | 4121.20 | -0.35% | USD/oz | yfinance(GC=F) [실측] | 2026-07-22T20:08:00+09:00 | $4,000선 상회 지속 |
| 2026-07-22 | commodity | Copper | 6.516 | -0.11% | USD/lb | yfinance(HG=F) [실측] | 2026-07-22T20:08:00+09:00 | 보합 |
| 2026-07-22 | bond | US10Y | 4.63 | +3bp | percent | yfinance(^TNX) [실측] | 2026-07-22T20:08:00+09:00 | 5월 중순 이후 고점권 유지 |
| 2026-07-22 | bond | US2Y | 4.26 | — | percent | FRED T10Y2Y(0.37%p,7/21) 역산 [파생, medium] | 2026-07-22T20:08:00+09:00 | 직접 실측 아님 |
| 2026-07-22 | bond | Spread2Y10Y | 37 | -3bp(전주比) | bp | FRED(T10Y2Y, 2026-07-21) | 2026-07-22T20:08:00+09:00 | 정상곡선 유지, 역전 아님 |
| 2026-07-22 | crypto | BTC | 66005.77 | -0.77% | USD | yfinance(BTC-USD) [실측] | 2026-07-22T20:08:00+09:00 | 24h |
| 2026-07-22 | crypto | ETH | 1927.70 | -0.05% | USD | yfinance(ETH-USD) [실측] | 2026-07-22T20:08:00+09:00 | 24h |
