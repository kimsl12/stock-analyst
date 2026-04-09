# ETF 전용 데이터 수집 가이드

ETF는 개별 종목과 데이터 소스·항목이 완전히 다르다.
DART API는 ETF에 사용하지 않는다 (ETF는 재무제표가 없음).

## ETF 소스 우선순위 & 수집 항목

### 국내 ETF (KODEX, TIGER, KBSTAR, ACE, SOL, ARIRANG 등)

| 우선순위 | 소스 | 제공 데이터 | 신뢰도 | 접근 방식 |
|---------|------|-----------|--------|----------|
| 🥇 1순위 | **KRX 정보데이터시스템** (data.krx.co.kr) | 시세, NAV, 괴리율, 거래량, 추적오차, AUM | ⭐5 공식 | 웹 검색 "[ETF명] site:data.krx.co.kr" |
| 🥈 2순위 | **ETF CHECK** (etfcheck.co.kr) | 구성종목·비중, 보수율, 분배금, 섹터배분, 수익률, 경쟁ETF | ⭐4 코스콤 운영 | 웹 검색 "[ETF명] site:etfcheck.co.kr" |
| 🥉 3순위 | **네이버 금융 ETF** | 기본정보, 수익률, 구성종목 Top10, NAV | ⭐4 | 웹 검색 "[ETF명] 네이버금융" |
| 4순위 | **운용사 홈페이지** | 공식 Holdings PDF, 투자설명서, 보수율 | ⭐5 공식 | 웹 검색 "[ETF명] [운용사명] 구성종목" |

### 해외 ETF (SPY, QQQ, XLE, VTI, ARKK 등)

| 우선순위 | 소스 | 제공 데이터 | 신뢰도 | 접근 방식 |
|---------|------|-----------|--------|----------|
| 🥇 1순위 | **etf.com** | Holdings, 보수율, 수익률, 섹터배분, ESG, 펀드플로우 | ⭐5 FactSet 기반 | 웹 검색 "[티커] site:etf.com" |
| 🥈 2순위 | **etfdb.com** | 보수율, 배당, 수익률, Holdings, 카테고리 순위·비교 | ⭐5 FactSet 기반 | 웹 검색 "[티커] site:etfdb.com" |
| 🥉 3순위 | **Yahoo Finance** | 시세, 수익률, 보수율, Holdings Top10, 배당, 차트 | ⭐4 | 웹 검색 "[티커] yahoo finance" |
| 4순위 | **운용사 홈페이지** (iShares, Vanguard, SPDR 등) | 공식 Fact Sheet, Holdings | ⭐5 공식 | 웹 검색 "[티커] [운용사] holdings" |

## ETF 항목별 수집 쿼리 템플릿

```
[기본정보 — 1순위 소스에서 수집]
  국내: "[ETF명] KRX 기본정보" 또는 "[ETF명] ETF CHECK"
  해외: "[티커] etf.com" 또는 "[티커] overview etfdb.com"

[구성종목 Top 10 — 핵심 데이터]
  국내: "[ETF명] 구성종목 ETF CHECK" 또는 "[ETF명] PDF 구성종목"
  해외: "[티커] holdings etf.com" 또는 "[티커] top holdings"

[보수율(TER) + 추적오차]
  국내: "[ETF명] 보수율 추적오차" 또는 "[ETF명] ETF CHECK 비용"
  해외: "[티커] expense ratio etf.com"

[수익률 (기간별)]
  국내: "[ETF명] 수익률 1년 3년" 또는 "[ETF명] 네이버금융 수익률"
  해외: "[티커] performance etfdb.com" 또는 "[티커] returns"

[분배금(배당)]
  국내: "[ETF명] 분배금 배당 ETF CHECK"
  해외: "[티커] dividend yield etfdb.com"

[섹터·국가 배분]
  국내: "[ETF명] 섹터 비중" 또는 "[ETF명] 자산구성"
  해외: "[티커] sector allocation etf.com"

[경쟁 ETF]
  국내: "[ETF명] 유사 ETF 비교" 또는 "[기초지수명] ETF 비교"
  해외: "[티커] alternatives etfdb.com" 또는 "[티커] similar ETFs"

[AUM·유동성]
  국내: "[ETF명] 순자산 거래대금 KRX"
  해외: "[티커] aum volume etf.com"

[ATR — 손절 계산용]
  국내: 네이버 차트 API (개별 종목과 동일)
  해외: "[티커] yahoo finance historical prices" → ATR(14) 직접 계산
```

## ETF 교차검증 매트릭스

| 항목 | 1순위 소스 | 2순위 소스 | 불일치 시 처리 |
|------|-----------|-----------|-------------|
| 현재가/NAV | KRX (국내) / Yahoo (해외) | 네이버/etf.com | 1순위 채택 |
| 보수율 | ETF CHECK (국내) / etf.com (해외) | 운용사 홈페이지 | 운용사 기준 최종 확인 |
| 구성종목 비중 | ETF CHECK (국내) / etf.com (해외) | 운용사 PDF | 운용사 PDF가 최종 진실 |
| 수익률 | KRX (국내) / etfdb.com (해외) | 네이버/Yahoo | 1순위 채택, 차이 3%p 초과 시 플래그 |
| 분배금 수익률 | ETF CHECK (국내) / etfdb.com (해외) | 네이버/Yahoo | 1순위 채택 |
| AUM | KRX (국내) / etf.com (해외) | — | 단일 소스 |
| 괴리율 | KRX 공식 | ETF CHECK | KRX 채택 |

## ETF 검증 규칙

```
1. NAV 괴리율 교차검증:
   괴리율 = (현재가 - NAV) / NAV × 100
   KRX 제공값과 직접 계산값 비교 → 차이 0.1%p 초과 시 플래그

2. 보수율 검증:
   ETF CHECK vs 운용사 홈페이지 → 불일치 시 운용사 기준 채택
   (운용사가 보수 인하/인상 시 ETF CHECK 반영 지연 가능)

3. 구성종목 시점 확인:
   Holdings 데이터의 기준일 반드시 기록
   기준일이 30일 이상 경과 시 "구성종목 데이터 지연" 경고

4. 수익률 기간 일치 확인:
   1년 수익률을 비교할 때 소스 간 기준일이 동일한지 확인
   기준일 불일치 시 "(기준일 상이)" 표기

5. 레버리지/인버스 ETF 경고:
   ETF명에 "2X", "인버스", "레버리지", "곱버스" 포함 시
   → "장기투자 부적합 — 일별 수익률 추적 상품" 경고 자동 삽입

6. ETF 가격 정합성 검증 (v2.3 필수):
   현재가가 52주 범위 안에 있는지 확인
   현재가를 반드시 2개 소스에서 교차 확인 (Yahoo + etf.com 또는 Investing.com)
   ATR 계산 기준가와 현재가가 일치하는지 확인
   ❌ 불일치 발견 시: 즉시 재검색, 티커를 정확히 지정하여 재수집
   ❌ 52주 범위 밖의 현재가: 데이터 오류로 판정, 전체 가격 데이터 재수집
```
