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
| 2026-04-17 | us_index | VIX | 17.94 | -1.27% | index | Yahoo Finance [2026-04-16 종가] | 2026-04-17T18:00:00+09:00 | ⚠️ 17.94 — 소비심리 47.6 역대최저와 극단 괴리 |
| 2026-04-17 | asia_index | Nikkei225 | ~58930 | -1.0% | point | CNBC [2026-04-17 마감 추정] | 2026-04-17T18:00:00+09:00 | 04-17 -1% 수준 보도. 휴전 불확실 |
| 2026-04-17 | asia_index | SENSEX | 78497.56 | +0.65% | point | Goodreturns/Trading Economics [2026-04-17] | 2026-04-17T18:00:00+09:00 | 원유 하락 + 세계 성장 기대 |
| 2026-04-17 | asia_index | KOSPI | — | — | point | 미수집 — 마감치 미공시 | 2026-04-17T18:00:00+09:00 | 04-17 하락 출발 보도 |
| 2026-04-17 | asia_index | HangSeng | — | — | point | 미수집 | 2026-04-17T18:00:00+09:00 | 하락 출발 보도 |
| 2026-04-17 | fx | DXY | 98.19 | — | index | Trading Economics [2026-04-16] | 2026-04-17T18:00:00+09:00 | ⚠️ 3년래 최저권. 탈달러 구조화 |
| 2026-04-17 | fx | USDKRW | 1476.32 | — | KRW | Fed H.10 / PoundSterlingLive [2026-04-16] | 2026-04-17T18:00:00+09:00 | ⚠️ 1,400 초과 |
| 2026-04-17 | fx | USDJPY | 159.24 | +0.27% | JPY | [2026-04-17] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | commodity | WTI | 93.74 | — | USD/barrel | Investing.com / Trading Economics [2026-04-17] | 2026-04-17T18:00:00+09:00 | 이란 협상 기대 하방 지속. 4/16 종가 $94.62 |
| 2026-04-17 | commodity | Brent | 94.89 | -0.04% | USD/barrel | Trading Economics [2026-04-16] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | commodity | Gold | ~4800 | — | USD/oz | Bloomberg / Fortune [2026-04-17] | 2026-04-17T18:00:00+09:00 | ⚠️ $4,800 지지 테스트. $4,780 이탈 시 단기 약화 |
| 2026-04-17 | bond | US10Y | 4.31 | +0.65% | percent | FRED / Trading Economics [2026-04-17] | 2026-04-17T18:00:00+09:00 | ⚠️ 4거래일 연속 반등. 4.35% 임박 |
| 2026-04-17 | bond | US30Y | 4.93 | +0.80% | percent | [2026-04-16] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | crypto | BTC | ~75000 | +5.9% | USD | 247WallSt / CNBC [2026-04-17] | 2026-04-17T18:00:00+09:00 | 이란 협상 재개 기대. 리스크온 |
| 2026-04-17 | crypto | ETH | ~2377 | +8.6% | USD | 247WallSt [2026-04-17] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-17 | crypto | SOL | ~87.6 | +6.3% | USD | 247WallSt [2026-04-17] | 2026-04-17T18:00:00+09:00 | — |
| 2026-04-18 | us_index | SP500 | 7126.06 | +1.20% | point | Yahoo Finance / CNBC [2026-04-17 종가 — 04-18 최신 확인치] | 2026-04-18T20:00:00+09:00 | 04-18 종가 웹검색 미확인. 04-17 종가(7,126.06)가 검색 최신치. 신고가 기록 |
| 2026-04-18 | us_index | NASDAQ | 24468.48 | +1.52% | point | Yahoo Finance / CNBC [2026-04-17 종가] | 2026-04-18T20:00:00+09:00 | NASDAQ 13일 연승 (1992년 이후 최장) |
| 2026-04-18 | us_index | DJIA | 49447.43 | +1.79% | point | Yahoo Finance / CNBC [2026-04-17 종가] | 2026-04-18T20:00:00+09:00 | Dow 49,447 신고가 |
| 2026-04-18 | us_index | Russell2000 | 2713.66 | +0.30% | point | Yahoo Finance [2026-04-17 종가] | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | us_index | VIX | 17.48 | -2.56% | index | Yahoo Finance [2026-04-17 종가] | 2026-04-18T20:00:00+09:00 | ⚠️ 거짓 안정 5단계. 소비심리 47.6 괴리 30pt 역대급 |
| 2026-04-18 | asia_index | KOSPI | 6191.92 | -0.55% | point | DigitalToday / Seoul Economic Daily [2026-04-18 마감] | 2026-04-18T16:00:00+09:00 | 외인 차익실현. 신현승 4/21 취임 관망 |
| 2026-04-18 | asia_index | KOSDAQ | — | — | point | 미수집 | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | asia_index | Nikkei225 | 58475.90 | -1.75% | point | CNBC [2026-04-18 마감] | 2026-04-18T16:00:00+09:00 | 호르무즈 소화 후 차익실현 |
| 2026-04-18 | asia_index | HangSeng | ~26130 | -1.01% | point | CNBC [2026-04-18 마감 추정] | 2026-04-18T16:30:00+09:00 | 종가 추정 (이전 26394 기준 -1.01%) |
| 2026-04-18 | asia_index | ShanghaiComposite | — | -0.17% | point | CNBC [2026-04-18 CSI300 기준] | 2026-04-18T16:00:00+09:00 | CSI300 -0.17% 소폭 하락 |
| 2026-04-18 | asia_index | SENSEX | ~77800 | — | point | 추정 [2026-04-18] | 2026-04-18T20:00:00+09:00 | 04-17 77,950 기준. 04-18 미확인 |
| 2026-04-18 | fx | DXY | 98.23 | +0.01% | index | Yahoo Finance / TradingView [2026-04-17] | 2026-04-18T20:00:00+09:00 | ⚠️ 호르무즈 해소에도 반등 없음. 탈달러 구조적 약세 |
| 2026-04-18 | fx | USDKRW | ~1484 | — | KRW | PoundSterlingLive / USD-KRW History [2026-04-18 범위] | 2026-04-18T20:00:00+09:00 | ⚠️ 1,483~1,498 범위. 1,400 초과 지속 |
| 2026-04-18 | fx | EURUSD | ~1.137 | — | USD | DXY 구성비 역산 추정 | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | fx | USDJPY | ~156.5 | — | JPY | 추정 [04-17 158.58 → 04-18 하락] | 2026-04-18T20:00:00+09:00 | Nikkei -1.75% 동반 하락 |
| 2026-04-18 | commodity | WTI | ~93 | — | USD/barrel | TradingEconomics / Angle360 [2026-04-18] | 2026-04-18T20:00:00+09:00 | 호르무즈 완전개방 후 4일 -19%. $92~94 범위 |
| 2026-04-18 | commodity | Brent | ~96 | — | USD/barrel | TradingEconomics / Angle360 [2026-04-18] | 2026-04-18T20:00:00+09:00 | 전쟁 디스카운트 소멸. 이란 항구 봉쇄 잔존 |
| 2026-04-18 | commodity | Gold | ~4878 | +0.59% | USD/oz | GoldPrice.org / PriceGold.net [2026-04-18] | 2026-04-18T20:00:00+09:00 | ⚠️ 신고가 갱신권. DXY 하락에도 단절적 강세. 구조적 Bull |
| 2026-04-18 | commodity | Copper | ~6.07/lbs | — | USD/lbs | TradingEconomics [2026-04-15 최신] | 2026-04-18T20:00:00+09:00 | Section 232 50% 관세 압력 |
| 2026-04-18 | bond | US10Y | ~4.28 | — | percent | TradingEconomics / FRED [2026-04-18 추정] | 2026-04-18T20:00:00+09:00 | ⚠️ 4거래일 반등 추세 (4.25→4.31→4.28). 4.35% 분기점 |
| 2026-04-18 | bond | US2Y | ~3.81 | — | percent | FRED [2026-04-10 최신 3.81%] | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | bond | US30Y | ~4.88 | — | percent | 04-17 기준 유지 | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | bond | Spread2Y10Y | ~+47 | — | bp | 계산값 (4.28%-3.81%=0.47%) | 2026-04-18T20:00:00+09:00 | 정상 구간(비역전). 10Y-2Y +47bp |
| 2026-04-18 | crypto | BTC | 77319 | +3.42% | USD | CoinGabbar [2026-04-18] | 2026-04-18T20:00:00+09:00 | ⚠️ 독립 강세 2일 연속. Gold 동시 상승 = 탈달러 쌍끌이 |
| 2026-04-18 | crypto | ETH | 2424.73 | +3.89% | USD | CoinGabbar [2026-04-18] | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | crypto | SOL | ~85.92 | -2.45% | USD | CoinGabbar / CoinMarketCap [2026-04-18] | 2026-04-18T20:00:00+09:00 | Drift Protocol $280M 익스플로잇 TVL -$1B 여파 |
| 2026-04-18 | crypto | TotalMarketCap | ~2.70T | +2.8% | USD | CoinGabbar [2026-04-18] | 2026-04-18T20:00:00+09:00 | — |
| 2026-04-18 | crypto | FearAndGreedIndex | ~44 | — | index | OpenPR / Solana Fear&Greed 복합 [2026-04-18] | 2026-04-18T20:00:00+09:00 | Neutral 회복 중 (이전 Extreme Fear 9→44) |
