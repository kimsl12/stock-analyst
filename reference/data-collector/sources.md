# 데이터 수집 소스 — 접근성 등급별 분류

> 웹검색 시 아래 소스 우선순위를 따른다. 직접 접근 가능한 소스를 우선 사용하고,
> 간접 접근 소스는 뉴스 보도를 통해 인용한다.

## 🟢 직접 접근 (무료, 본문 확인 가능) — 우선 사용

| # | 소스 | 용도 | 검색 쿼리 예시 |
|---|------|------|---------------|
| 1 | **Yahoo Finance** | 시세, 재무제표, 컨센서스, ETF 구성종목 | `[티커] yahoo finance` |
| 2 | **Investing.com** | 가격, PER, PBR, 경제지표 | `[티커] investing.com` |
| 3 | **Macrotrends** | 장기 매출·순이익·FCF 추세 | `[티커] macrotrends revenue` |
| 4 | **Finviz** | 종목 스크리닝, 기술 지표 | `[티커] finviz` |
| 5 | **Barchart** | 옵션 플로우, 섹터 히트맵, ETF 랭킹 | `[티커] barchart` |
| 6 | **Seeking Alpha** | 기업 심층 분석, 실적 콜 요약 (일부 무료) | `[티커] seeking alpha` |
| 7 | **TradingView** | 차트, 기술 지표, 커뮤니티 아이디어 (일부 무료) | `[티커] tradingview` |
| 8 | **Reuters** | 국제 뉴스, 속보 | `[종목명] reuters` |
| 9 | **CoinGecko** | 크립토 시총, 거래량 | `[코인명] coingecko` |
| 10 | **DeFiLlama** | DeFi TVL, 프로토콜 자금 흐름 | `[프로토콜명] defillama` |
| 11 | **GeekNews** | 테크 뉴스 한글 요약 | `[키워드] site:news.hada.io` |
| 12 | **전자신문** | 국내 IT·반도체 동향 | `[키워드] site:etnews.com` |
| 13 | **ScienceDaily** | 과학·바이오 연구 속보 | `[키워드] sciencedaily` |
| 14 | **DART** | 한국 공시 (API 키 설정 완료) | DART API 직접 호출 |
| 15 | **EIA** | 미국 에너지 생산·소비·재고 데이터 (무료) | `eia [에너지원] data` |
| 16 | **ArXiv** | AI·양자 프리프린트 논문 (무료) | `arxiv [기술명]` |

## 🟢 한국 종목 컨센서스 소스 [v2.4 신규]

| # | 소스 | 용도 | 검색 쿼리 예시 |
|---|------|------|---------------|
| 17 | **한경컨센서스** | 증권사 컨센서스 종합 (영업이익, EPS, 목표가) | `[종목명] 한경컨센서스` 또는 `[종목명] site:consensus.hankyung.com` |
| 18 | **FnGuide** | 기관 컨센서스 (실적 전망, 투자의견) | `[종목명] FnGuide 컨센서스` 또는 `[종목명] site:comp.fnguide.com` |
| 19 | **네이버증권 리서치** | 증권사 리포트 개별 확인 | `[종목명] 네이버 증권 리서치 목표주가` |
| 20 | **증권사 리포트 PDF** | 개별 증권사 상세 추정치 | `[종목명] [증권사명] 리포트 2026 영업이익` |
| 21 | **Investing.com 한국** | 한국 종목 컨센서스, 애널리스트 수 | `[종목명] investing.com 컨센서스` |

## 🟡 간접 접근 (페이월/비공개 — 뉴스 보도를 통해 인용)

| # | 소스 | 실제 접근 방식 | 검색 쿼리 예시 |
|---|------|-------------|---------------|
| 22 | **Bloomberg** | 뉴스 보도 인용 | `[종목명] bloomberg 보도` |
| 23 | **Goldman Sachs** | IB 리서치 보도 인용 | `goldman sachs [종목명] 전망` |
| 24 | **Morgan Stanley** | IB 리서치 보도 인용 | `morgan stanley [종목명] 목표가` |
| 25 | **J.P. Morgan** | IB 리서치 보도 인용 | `jpmorgan [종목명] 리서치` |
| 26 | **BofA Securities** | 펀드매니저 서베이 보도 | `bofa [섹터명] 전망` |
| 27 | **Glassnode** | 무료 지표 또는 보도 | `glassnode [지표명]` |
| 28 | **BloombergNEF** | 에너지 전환 보도 | `bloombergnef [키워드]` |

## 🔴 제한적 접근 (시차·유료벽 존재)

| # | 소스 | 접근 가능 데이터 | 검색 쿼리 예시 |
|---|------|----------------|---------------|
| 29 | **Dataroma** | 13F 대가 포트폴리오 (무료, 시차 45일) | `dataroma [투자자명]` |
| 30 | **Gurufocus** | 포트폴리오 기본 (무료, 상세 유료) | `gurufocus [투자자명]` |
| 31 | **SEC EDGAR 13F** | 공시 원문 (시차 45일) | `sec edgar 13f [기업명]` |
| 32 | **FDA / EMA** | 신약 승인·임상 데이터 | `fda approval [약물명]` |
| 33 | **IEA** | 에너지 수급 전망 (요약만 무료, 상세 유료) | `iea [키워드] report` |

## 데이터 항목별 소스 매핑 (검색 순서)

```
현재가·시세    → Yahoo Finance → Investing.com (교차검증 필수)
재무제표       → DART(한국) / Macrotrends(해외) → Yahoo Finance
컨센서스(한국) → 한경컨센서스 → FnGuide → 네이버증권 리서치 → 증권사 PDF [v2.4]
컨센서스(해외) → Seeking Alpha → Yahoo Finance → IB 리서치 보도
증권사 목표가  → 한경컨센서스 → Investing.com → 개별 증권사 리포트 보도 [v2.4]
산업 동향      → KB 참조 → Reuters → Bloomberg 보도 → 전자신문(국내) [v2.4]
기술적 분석    → TradingView → Finviz → Barchart
거물 투자자    → Dataroma → Gurufocus → SEC EDGAR
크립토         → CoinGecko → DeFiLlama → Glassnode
ETF 정보       → Yahoo Finance → etf.com(해외) / ETF CHECK(국내)
바이오·신약    → FDA → ScienceDaily → Reuters
에너지·자원    → EIA → IEA → BloombergNEF 보도
```

## 가격 수집 검색 쿼리 템플릿

```
1차 검색 (Yahoo Finance — 분할 조정가 제공):
  "[티커] yahoo finance quote"
  → 결과에서 확인: 현재가, 52주 범위, 날짜

2차 검색 (교차검증):
  "[티커] stock price investing.com" (해외)
  "[티커] 현재가 네이버" (국내)
  → 1차와 비교: 가격 차이 5% 이내인지, 날짜가 동일한지

❌ 절대 하지 말 것:
  - "[티커] stock price" 만으로 검색 (날짜 없는 결과가 나올 수 있음)
  - 검색 결과의 첫 번째 숫자를 무조건 현재가로 채택
  - 날짜를 확인하지 않고 가격 사용
```
