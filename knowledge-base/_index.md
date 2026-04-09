---
updated: 2026-04-09
version: v3.0
---

# Knowledge Base Index

## 섹터-종목 매핑

| 섹터 | 대표 종목 | KB 파일 | 관련 매크로 |
|------|----------|---------|------------|
| 반도체 | 삼성전자, SK하이닉스, 마이크론, 한미반도체 | `semiconductor.md` | 미중관계, 금리, 관세 |
| AI 인프라 | NVIDIA, AMD, 브로드컴, TSMC | `industry/ai.md` | 금리, 기술규제, CapEx |
| AI 생태계 | OpenAI, Anthropic, Google, 네이버, 카카오 | `industry/ai.md` | AI 규제, 오픈소스 경쟁 |
| AI 개별기업 (비상장) | Anthropic (Claude) | `industry/ai_anthropic.md` | IPO, AI 안전, 엔터프라이즈 LLM |
| 에너지 | SK이노베이션, GS칼텍스, S-Oil, 한국전력, 두산에너빌리티, 한화솔루션 | `industry/energy.md` | 유가, 지정학, 탄소중립 |
| 2차전지 | LG에너지솔루션, CATL | `industry/battery.md` | 리튬가격, EV정책 |
| 바이오 | 삼성바이오, 셀트리온 | `industry/bio_pharma.md` | FDA, 환율 |
| 자동차 | 현대차, 기아, 토요타, BYD, 테슬라 | `industry/auto.md` | IRA, 관세, 리튬가격, EV정책 |
| 과학기술 (메타) | 양자/바이오/우주/로봇/SMR/6G/EDA/디스플레이 | `industry/science_tech.md` | 미중 디커플링, R&D 정책, 인재 |

## 매크로 KB

| 파일 | 커버리지 | 최종 업데이트 |
|------|---------|------------|
| `macro/us_economy.md` | 미국 GDP, 고용, 인플레, 소비, PMI, 주택, 무역, 재정, Fed 정책, 리스크 | 2026-04-07 |
| `macro/us_monetary_policy.md` | Fed 금리, QT, 인플레이션 (요약 포인터 -- 상세는 us_economy.md) | 2026-04-07 |
| `macro/geopolitics.md` | 미중 관세·기술전쟁, 대만, 중동, 북한, 유럽, 공급망 | 2026-04-07 |
| `macro/korea_economy.md` | 한국 GDP, 환율, 수출, 금리, 산업별 동향, 정책·규제 | 2026-04-07 |
| `macro/global_risk_factors.md` | 글로벌 Top 5 리스크, 시장 심리 지표, 원자재 가격 | 2026-04-07 |
| `macro/political_cycle.md` | 주요국 정치 사이클, 정책->섹터 임팩트 `[v3.4 신규]` | 2026-04-07 |
| `macro/tech_breakthrough.md` | AI·양자·바이오·에너지 기술 단계 판정 `[v3.4 신규]` | 2026-04-07 |
| `macro/supply_chain.md` | 반도체·배터리·의약품·희토류 공급망 재편 `[v3.4 신규]` | 2026-04-07 |

## 시장 KB `[v3.4 신규 / v3.0 권한 헤더 추가]`

| 파일 | 커버리지 | 갱신 주기 | 쓰기 |
|------|---------|----------|------|
| `market/daily_snapshot.md` | 미국·아시아 지수, 환율·원자재·채권·크립토 | 매 거래일 | market-data-collector |
| `market/economic_calendar.md` | 이번 주 경제 지표·이벤트·중앙은행 일정 | 주 1회 | market-data-collector |
| `market/surprise_index.md` | 경제 서프라이즈 누적 스코어 | 지표 발표 당일 | correlation-monitor |
| `market/correlation_matrix.md` | 자산 페어 6종 30D/90D 롤링 상관계수 | 매 거래일 | correlation-monitor |
| `market/guru_positions.md` | 거물 8인 13F 포지션 변화 (45일 시차) | 분기별 | market-data-collector |

### knowledge-db/market/ 시계열 영구 저장소 `[v3.0 -- jsonl->연도별 .md 마이그레이션]`

| 파일 | 커버리지 | 쓰기 |
|------|---------|------|
| `knowledge-db/market/2026_daily_prices.md` | 일별 가격 시계열 (지수·환율·채권·크립토 22항목) | market-data-collector |
| `knowledge-db/market/2026_economic_indicators.md` | 경제지표 발표 이력 (CPI·NFP 등) | market-data-collector |
| `knowledge-db/market/2026_guru_changes.md` | 분기별 13F 포지션 변동 | market-data-collector |
| `knowledge-db/market/2026_correlation_log.md` | 6 페어 90D 상관 + Z-score 이력 | correlation-monitor |

> 마이그레이션: `scripts/migrate_market_jsonl_to_md.py` (commit 3793ab9). 기존 `20260407.jsonl` 은 `_archive/` 에 보존.

## 성과 추적 KB `[v3.0 신규 -- briefing-lead 전용]`

| 파일 | 커버리지 | 갱신 주기 | 쓰기 |
|------|---------|----------|------|
| `knowledge-db/performance/2026_recommendations.md` | 브리핑 신규 제안 누적 | 매 브리핑 실행 시 append | briefing-lead |
| `knowledge-db/performance/2026_scenario_tracking.md` | G-8 시나리오 분기점 확률 추이 | 주간/글로벌인텔리전스 실행 시 | briefing-lead |
| `knowledge-db/performance/2026_hit_rate.md` | 적중률 통계 (1w/2w/1m/3m) | /주간리포트 + /성과리뷰 | briefing-lead |

> briefing-lead 만 쓰기 권한 보유. 다른 모든 에이전트는 읽기만 가능. (docs/briefing_pipeline.md S3.1 D-01)

## 포트폴리오 KB `[v3.4 신규]`

| 파일 | 커버리지 | 갱신 주기 |
|------|---------|----------|
| `portfolio/user_portfolio.md` | 사용자 보유 종목·비중·프로파일 | 사용자 요청 시 |
| `portfolio/model_portfolios.md` | 4종 모델 포트폴리오 (안전/중립/공격/배당) | 주간 |
| `portfolio/rebalancing_history.md` | 리밸런싱 제안·실행 이력 누적 | 리밸런싱 시 |

## 참조 레지스트리 `[v3.4 신규]`

> 변경 드문 정적 데이터. `reference/` 디렉토리 (KB 외부).

| 파일 | 내용 |
|------|------|
| `../reference/source_registry.md` | 37개 소스 + 접근성 등급 |
| `../reference/rules_and_constraints.md` | 금지사항 31개 + 필수 준수 핵심 |
| `../reference/guru_watchlist.md` | 거물 투자자 추적 대상 8인 |

## 레거시 파일 (macro/ 하위로 이전됨)

| 파일 | 이전 위치 | 현재 위치 |
|------|---------|---------|
| `geopolitics.md` (루트) | knowledge-base/ | macro/geopolitics.md |
| `global_risk_factors.md` (루트) | knowledge-base/ | macro/global_risk_factors.md |
| `korea_economy.md` (루트) | knowledge-base/ | macro/korea_economy.md (요약본 루트 유지) |
| `us_monetary_policy.md` (루트) | knowledge-base/ | 루트 유지 + macro/us_economy.md로 확장 |

## 업데이트 이력

| 날짜 | 파일 | 변경 내용 |
|------|------|----------|
| 2026-04-09 | `industry/ai_anthropic.md` | **신규 생성** -- Anthropic 개별기업 KB 최초 구축 (DB 34건 기반, 기업개요·펀딩·ARR·모델·경쟁·IPO·안전성·최신뉴스 전 항목) |
| 2026-04-09 | `knowledge-db/ai_2026.jsonl` | Anthropic 전용 데이터 34건 추가 (기존 53건 -> 총 87건) |
| 2026-04-09 | `_index.md` | AI 개별기업(비상장) Anthropic 행 추가 |
| 2026-04-08 | `_index.md` | **F-07 처리** -- performance/ KB 섹션 + knowledge-db/market/ 4종 .md 시계열 + 시장 KB 권한 컬럼 추가 `[v3.0]` |
| 2026-04-07 | `knowledge-db/market/` | jsonl -> 연도별 4종 .md 마이그레이션 (`scripts/migrate_market_jsonl_to_md.py`) |
| 2026-04-07 | `knowledge-db/performance/` | 신규 3 파일 (recommendations / scenario_tracking / hit_rate) -- briefing-lead 전용 |
| 2026-04-07 | `_index.md` | **Phase 1 통합** -- market/ + portfolio/ + reference/ 섹션 + 매크로 3종(political_cycle/tech_breakthrough/supply_chain) 추가 `[v3.4]` |
| 2026-04-07 | `semiconductor.md` | **전면 갱신 (2차)** -- DB 71건(+22건) 기반. 트럼프 관세 간접영향, 2026Q1 실적 프리뷰, 장비/소재 섹션, HBM4 스펙, 중국 자급화, 밸류에이션 신규 추가 |
| 2026-04-07 | `macro/us_economy.md` | 신규 생성 -- 미국 경제 KB 전면 구축 (DB 33건 기반, GDP·고용·인플레·소비·PMI·주택·무역·재정·Fed·리스크 전 항목) |
| 2026-04-07 | `us_monetary_policy.md` | 갱신 -- 미수집 해소, macro/us_economy.md 요약 포인터로 전환 |
| 2026-04-07 | `knowledge-db/macro_2026.jsonl` | 미국 경제 데이터 33건 추가 (기존 39건 -> 총 72건) |
| 2026-04-07 | `macro/korea_economy.md` | 신규 생성 -- 한국 경제 KB 전면 구축 (DB 38건 기반, GDP·금리·환율·수출·산업·정책 전 항목) |
| 2026-04-07 | `korea_economy.md` (루트) | 전면 갱신 -- 미수집 해소, macro/korea_economy.md 요약본으로 전환 |
| 2026-04-07 | `knowledge-db/macro_2026.jsonl` | 신규 생성 -- 한국 매크로 DB 38건 축적 |
| 2026-04-07 | `semiconductor.md` | 1차 갱신 -- DB 49건 기반, 전 항목 최신화 (미수집 0건) |
| 2026-04-07 | `industry/auto.md` | 신규 생성 -- 자동차 섹터 KB 최초 구축 (DB 45건 기반) |
| 2026-04-07 | `macro/geopolitics.md` | 신규 생성 -- 지정학 KB 전면 갱신 (미중·대만·중동·북한·유럽·공급망) |
| 2026-04-07 | `macro/global_risk_factors.md` | 신규 생성 -- 글로벌 Top5 리스크, 시장심리, 원자재 현황 |
| 2026-04-07 | `knowledge-db/geopolitics_2026.jsonl` | 신규 생성 -- 지정학 DB 31건 축적 |
| 2026-04-07 | `industry/energy.md` | 신규 생성 -- 에너지 섹터 KB 최초 구축 (DB 40건 기반) |
| 2026-04-07 | `knowledge-db/energy_2026.jsonl` | 신규 생성 -- 에너지 DB 40건 축적 |
| 2026-04-07 | `industry/ai.md` | 신규 생성 -- AI 섹터 KB 최초 구축 (DB 53건 기반, 전 분야 커버) |
| 2026-04-07 | `knowledge-db/ai_2026.jsonl` | 신규 생성 -- AI DB 53건 축적 |
| 2026-04-07 | `industry/science_tech.md` | 신규 생성 -- 과학기술 메타 섹터 KB 최초 구축 (DB 45건, 양자·바이오·우주·로봇·SMR·6G·EDA 등) |
| 2026-04-07 | `knowledge-db/science_tech_2026.jsonl` | 신규 생성 -- 과학기술 DB 45건 축적 |
