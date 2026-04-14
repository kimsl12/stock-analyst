---
updated: 2026-04-14
version: v3.2
maintainer: wiki-linter (자동) + briefing-lead (수동)
lint_last_run: 2026-04-13
lint_mode: full
---

# Knowledge Base Index — Wiki Master Index

> **목적:** 에이전트가 이 파일 하나만 읽으면 전체 KB 구조, 핵심 인사이트, 건강 상태를 파악할 수 있어야 한다.
> **갱신 주체:** wiki-linter (자동 갱신, 주 1회) + briefing-lead (브리핑 종료 시 인사이트 append)
> **활용법:** 에이전트는 질의 전 이 파일을 먼저 읽고, 필요한 파일만 드릴다운한다. Glob 탐색 금지.

---

## 🚨 P0 — 즉시 조치 필요 (FAILED / 만료)

> wiki-linter가 탐지한 긴급 항목. 브리핑 실행 전 반드시 확인.
> **최종 갱신: 2026-04-13 (wiki-linter full)**

| 파일 | 상태 | 영향 모듈 | 조치 |
|------|------|----------|------|
| `market/daily_snapshot.md` | ✅ SUCCESS (04-14) valid_until 04-15 | A-1, B-2, B-3 | -- |
| `market/economic_calendar.md` | ⛔ FAILED + confidence:none | A-4, B-1, C-6 | `/시장데이터수집` 재실행 |
| `market/correlation_matrix.md` | ⛔ FAILED + confidence:none | B-5 | `/시장데이터수집` 재실행 |
| `market/surprise_index.md` | ⛔ FAILED + 만료 (valid_until 04-08) | B-4 | `/시장데이터수집` 재실행 |
| `market/guru_positions.md` | ⛔ FAILED + confidence:none | A-5, B-7, C-4 | `/시장데이터수집 13F` 재실행 |
| `macro/political_cycle.md` | ✅ 갱신 완료 (04-14) confidence:high | G-2, C-3 | — |
| `macro/tech_breakthrough.md` | ✅ 갱신 완료 (04-14) confidence:high | G-3, C-3.5 | — |
| `macro/supply_chain.md` | ✅ 갱신 완료 (04-14) confidence:high | G-1, C-3 | — |
| `portfolio/model_portfolios.md` | ⚠️ confidence:low 미수집 | F-2~F-5 | `/모델포트폴리오` 실행 |
| `portfolio/user_portfolio.md` | ✅ 등록 완료 (04-13) confidence:high | /내포트폴리오 | — |
| `us_monetary_policy.md` (루트) | ⚠️ confidence:redirect — SSOT 아님 | 교차참조 | `macro/us_monetary_policy.md` 사용 |

> ✅ 네트워크 허용 환경 확인됨 (2026-04-13). FAILED 4건 재수집 가능.
> ⚠️ P1: industry/ 고아 파일 8개 — quantum, space, smr, telecom_next, banking_capital, advanced_materials, battery, infrastructure (_index.md Industry 테이블 미등재)

---

## ⚡ 최근 핵심 인사이트 (지난 7일 — briefing-lead append)

| 날짜 | 출처 | 인사이트 | 관련 KB | 제안 상태 |
|------|------|---------|--------|---------|
| 2026-04-13 | 이브닝브리핑 | 호르무즈 봉쇄 선언 — WTI $105 급등, 4/14 아시아 갭다운 -2~4% 경고. 위험등급 4→5 상향 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-13 | 이브닝브리핑 | Gold-DXY 역상관 약화 Z+1.8σ — Gold $4,724 구조적 Bull. 중앙은행 매수+재정적자=탈달러 수요 | `macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-13 | 이브닝브리핑 | WTI-인플레기대 동조화 Z+2.3σ — Core CPI 전이 2~3개월 시차. Fed 6월 인하 소멸 가능 | `macro/us_monetary_policy.md` | 진행중 |
| 2026-04-09 | ai_anthropic.md 신규 | Anthropic ARR $30B — OpenAI 최초 추월. 엔터프라이즈 LLM 점유율 40% | `industry/ai_anthropic.md` | — |
| 2026-04-07 | 모닝브리핑 | Gold Bull 중기 — 기축통화 균열 프리미엄, 중앙은행 매수 급증 | `macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-07 | 모닝브리핑 | SK하이닉스 Bull — HBM3E 대중 전면금지 → Tier1 한국 무제한 수혜 | `semiconductor.md §1 HBM` | 진행중 |
| 2026-04-07 | 모닝브리핑 | 한국 방산 Bull 장기 — 유럽 GDP 3% 방위비 + 우크라이나 재건 | `macro/geopolitics.md §5` | 진행중 |
| 2026-04-07 | 모닝브리핑 | 미국 장기국채(TLT) Bear — 관세 인플레 2차 효과 + 재정적자 | `macro/us_economy.md §8` | 진행중 |
| 2026-04-07 | 모닝브리핑 | CPI 베이스 시나리오 — 관세 전가율 50~70%, Core +0.5~1.5%p 상방 | `macro/us_monetary_policy.md` | 진행중 |
| 2026-04-13 | 주간리포트 | 위험등급 4->5 상향 — 호르무즈 봉쇄+CPI 3.3%+관세 삼중 인플레. 베이스 시나리오 WTI $100~115, S&P -3~5% | `market/daily_snapshot.md` | 진행중 |
| 2026-04-13 | 주간리포트 | KOSPI "코리아 프리미엄" 반전 리스크 — 원/달러 1,500+ 시 외국인 이탈+경상수지 적자 전환 가능 | `macro/korea_economy.md` | 진행중 |
| 2026-04-13 | 주간리포트 | 적중률 잠정 50%(3건 중 1.5건) — Gold Bull 적중, CPI 부분 적중, 시나리오 수정. 테일 리스크 가중치 상향 필요 | `performance/2026_recommendations.md` | -- |
| 2026-04-14 | 모닝브리핑 | VIX 19.12 "거짓 안정" — 소비심리 47.6(역대최저) vs VIX 괴리. 4~6주 내 25~30 재상승 경고 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-14 | 모닝브리핑 | DXY 98.34 구조적 약세 3년래 최저 — 재정적자+탈달러+Gold $4,781. 달러 표시 자산 실질가치 하락 | `macro/global_risk_factors.md` | 진행중 |
| 2026-04-14 | 모닝브리핑 | 호르무즈 봉쇄 Day 1 제한적 적용 — CENTCOM 비이란 통항 보장. 시장 "봉쇄 내성" 확인하나 2차효과 과소평가 | `macro/supply_chain.md` | 진행중 |
| 2026-04-14 | 내포트폴리오 | 미국주식 87.8% 극편중 진단 — 중립형 프로파일 vs 초공격형 실제. 채권1.1%/금0% 방어력 전무. 6개월 재조정 플랜 제시 | `portfolio/user_portfolio.md` | 진행중 |
| 2026-04-14 | 리밸런싱 | 달러현금 $705 즉시 활용(AGG $400+GLD $300) + 월적립 방향 전환. 6개월 목표: 미국72%/채권8%/금5%/크립토9% | `portfolio/rebalancing_history.md` | 진행중 |
| 2026-04-14 | 글로벌인텔리전스 | 4축 메가트렌드 "호르무즈-AI-탈달러 수렴" -- 지정학이 단기 3개월 압도적 동인. 호르무즈 해소 시점이 4축 전체 스위치포인트 | `macro/supply_chain.md, macro/geopolitics.md` | 진행중 |
| 2026-04-14 | 글로벌인텔리전스 | 숨은 테마 "비료-식량 인플레 2차 파동" -- 요소비료 +172% YoY, 한국 호르무즈 경유 38.4%. 6~7월 식품CPI +0.3~0.5%p. 시장 반영 10~20% | `macro/supply_chain.md` | 진행중 |
| 2026-04-14 | 글로벌인텔리전스 | TSMC N2 2nm GAA Q3 매출 N3/N5 추월 전망 -- Q1 $35.7B 사상최고. AI 초크포인트 집중도 심화. 대만 리스크 구조적 상존 | `macro/tech_breakthrough.md` | 진행중 |
| 2026-04-14 | 이브닝브리핑 | KOSPI 장중 6,000 돌파(6,026) 후 5,968 마감(+2.74%) -- 재협상 기대. 6,000 안착에는 호르무즈 해소 또는 Q2 반도체 실적 확인 필요 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-14 | 이브닝브리핑 | IEA/WB/IMF "봉쇄 해소해도 빠른 정상화 불가" 공동경고 -- War Risk Premium 구조화+IRGC 기뢰 21건+비료 복구 시차. 시장 과소평가 | `macro/supply_chain.md` | 진행중 |
| 2026-04-14 | 이브닝브리핑 | 정유 섹터 정제마진 $18(역대급) -- WTI $97+재고평가이익. S-Oil/SK이노 Q1 서프라이즈 가능하나 봉쇄 해소 시 반락 리스크 | `industry/energy.md` | 진행중 |

---

## 🏭 Industry KB (`knowledge-base/industry/`)

| 파일 | 핵심 수치 | 최신 인사이트 | 갱신일 | 유효기간 | 신뢰도 |
|------|---------|------------|-------|---------|-------|
| `semiconductor.md` | 삼성 2026E OP 45~65조, SK 23~30조, HBM4 H2 양산 | 관세 간접 타격 -5~10% 우려 추가. 삼성 파운드리 3nm 수율 60% 미만 지속 | 04-07 | 05-07 | medium |
| `ai.md` | 글로벌 AI 시장 3,300~3,800억달러, CapEx 합산 2,950~3,200억 | DeepSeek 쇼크 후 CapEx 오히려 상향. 추론(Inference) 60%+ 비중 전환 | 04-07 | 05-07 | medium |
| `ai_anthropic.md` | ARR $300억, 밸류 $3,800억, IPO 2026 Q4 목표 | OpenAI ARR 최초 추월. 엔터프라이즈 40% 점유. Pentagon 갈등 리스크 | 04-09 | 05-09 | high |
| `auto.md` | HMG 750만대(글로벌 3위), 미국 관세 25% 발효 | 조지아 30만대로 부분 완충. 관세로 연간 이익 1.5~2.5조 감소 우려 | 04-07 | 05-07 | medium |
| `energy.md` | WTI $97~100, Brent $96~103, JKM LNG $17~18.75 | 호르무즈 봉쇄 유가 +40% 급등. 정제마진 $18 역대급. SPR 26일분. OPEC+ 206K 증산. 석화 나프타 $1,000 위기 | 04-14 | 05-14 | high |
| `science_tech.md` | 한국 R&D/GDP **5.1%**(세계 1위), 글로벌 R&D 3.8조달러, 정부 R&D 29.6조 | IonQ 99.99% 양자기록. Optimus Gen3 여름양산. Starlink 10K기. CHIPS Act 생산시대 | 04-14 | 05-14 | high |
| `bio_pharma.md` | GLP-1 시장 700~800억달러 | 삼성바이오 4공장 풀가동, CDMO Top 4 | 04-07 | 05-07 | medium |
| `quantum.md` | 양자컴퓨팅/통신/PQC/센서 | IBM Nighthawk·Google Willow 로드맵. NIST PQC 표준 확정 | 04-13 | 05-13 | medium |
| `space.md` | 우주경제·LEO위성·발사체 | SpaceX Falcon9 최고 발사율. AST SpaceMobile 위성직접통신 | 04-13 | 05-13 | medium |
| `smr.md` | SMR·핵융합 에너지 | NuScale 취소 후 Kairos·TerraPower·두산에너빌리티 수혜 | 04-13 | 05-13 | medium |
| `telecom_next.md` | 6G·위성통신·보안 | 삼성 6G 2030 목표. 위성직접통신 2026 상용화 | 04-13 | 05-13 | medium |
| `banking_capital.md` | 4대 금융지주 합산 순이익 18.4조(+11.4%) | KB·신한·하나·우리 사상 최대 실적. PE/VC 환경 개선 기대 | 04-13 | 05-13 | medium |
| `advanced_materials.md` | 마이크로LED 시장 0.5~1.1B USD, EDA 시장 | MicroLED CAGR 52~77%. EDA Synopsys·Cadence 과점 | 04-13 | 05-13 | medium |
| `battery.md` | 리튬 가격 동북아 $18,050/ton (Q1 2026) | 리튬 급등 후 조정. LFP 점유 확대 vs NCM 고성능 분화 | 04-13 | 05-13 | medium |
| `infrastructure.md` | 글로벌 건설 17.26조달러(+4.9%), 한국 수주 231.2조 | 현대건설·삼성물산 SMR EPC 추진. 데이터센터 전력망 수혜 | 04-13 | 05-13 | medium |

> 상세 드릴다운: 각 파일의 § 섹션 번호 참조. 에이전트는 이 표로 파일 선택 후 해당 파일만 Read.
> [v3.5 신규 등재 — 04-13 wiki-linter]: quantum, space, smr, telecom_next, banking_capital, advanced_materials, battery, infrastructure

---

## 🌍 Macro KB (`knowledge-base/macro/`)

| 파일 | 핵심 수치 | 핵심 리스크 | 갱신일 | 신뢰도 |
|------|---------|-----------|-------|-------|
| `us_economy.md` | **CPI 3.3%(에너지 주도), Core CPI 2.6%, GDPNow Q1 +1.3%, Fed 3.50~3.75%, 침체확률 30~49%** | 2중 인플레(에너지+파이프라인). ISM가격 78.3. 소비심리 47.6(역대최저). 6월 인하 소멸 | 04-14 | ✅ high |
| `us_monetary_policy.md` | SSOT: `macro/us_monetary_policy.md` 참조 (루트 파일 = redirect 포인터) | 루트 파일 confidence:redirect — 수치 직접 참조 금지 | 04-13 | redirect |
| `geopolitics.md` | **IEEPA 위헌→실효 34.7%**. WTI $97, Brent $102. Gold $4,762. 리스크 5/5 | **이란전쟁·호르무즈 봉쇄**(극고). Section 301·50% 위협. 희토류 1년 유예 | 04-14 | ✅ high |
| `korea_economy.md` | **수출 3월 $86.1B(+48.3%), 반도체 $18.7B(+163.9%), KOSPI 5,778(+141% YoY), 금리 2.50%(7연속 동결), 원화 1,485원, 추경 26.2조** | 이란전쟁 공급충격+관세 이중 타격. 원화 약세 1,485원. 외국인 3월 $365억 순유출. 가계부채 1.5% 한도 | 04-14 | ✅ high |
| `global_risk_factors.md` | VIX 19.12, F&G 41(Fear), DXY 98.39, 금 $4,761, 브렌트 $98 | Top5: 호르무즈봉쇄·미중디커플링·스태그플레이션·대만·부채 | 04-14 | ✅ high |
| `political_cycle.md` | Section 122 글로벌10% 관세(07.24만료), 추경26.2조, 6개국 정치사이클 | 관세 법적 불확실성(Section 122 한시). 반도체 25% 관세 7월 확대 검토 | 04-14 | ✅ high |
| `tech_breakthrough.md` | AI·반도체·양자·바이오·에너지·로봇·우주·신소재 8개 분야 기술 단계 판정. 양자: QEC 돌파·IonQ $130M. 로봇: Atlas 양산·Waymo 50만회/주. 우주: Starlink 10K위성·1,000만 가입자. 신소재: 페로브스카이트 28%·SiC $52B | G-3 모듈 정상 운영 가능. 4개 미수집 분야 전면 데이터 채움 | 04-14 | ✅ high |
| `supply_chain.md` | WCI $2,309, SCFI 1707~1827, WTI $104/Brent $98, 구리 $12,630, HBM sold-out, 요소비료 $750(+56%), Section 122 15%(7/24만료), Section 232 반도체 25% | 호르무즈 미군 봉쇄 개시(04/14). IEA 역사상 최대 원유 차질. 에너지-비료-식량 삼중 인플레 전이. TSMC 3nm 극도 타이트 | 04-14 | ✅ high |

---

## 📊 Market KB (`knowledge-base/market/`) — 부분 재수집 필요

| 파일 | 상태 | 갱신 빈도 | 영향 브리핑 모듈 | 재수집 명령 |
|------|------|----------|---------------|-----------|
| `daily_snapshot.md` | ✅ SUCCESS (04-13) valid_until 04-14 | 매 거래일 | A-1, B-2, B-3 | 내일 재실행 |
| `economic_calendar.md` | ⛔ FAILED + confidence:none | 주 1회 | A-4, B-1, C-6 | `/시장데이터수집` |
| `surprise_index.md` | ⛔ FAILED + 만료 (04-08) | 매일 | B-4 | `/시장데이터수집` |
| `correlation_matrix.md` | ⛔ FAILED + confidence:none | 주 1회 | B-5 | `/시장데이터수집` |
| `guru_positions.md` | ⛔ FAILED + confidence:none valid_until 07-07 | 분기 1회 | A-5, B-7, C-4 | `/시장데이터수집 13F` |

> **재수집 순서 권장:** economic_calendar → surprise_index → correlation_matrix → guru_positions (13F)
> daily_snapshot은 fetch_price.py --market --save로 매일 자동 갱신

---

## 💰 Portfolio KB (`knowledge-base/portfolio/`)

| 파일 | 상태 | 갱신 주체 | 비고 |
|------|------|---------|------|
| `model_portfolios.md` | ⚠️ 전 항목 미수집 | briefing-lead | `/모델포트폴리오` 실행 필요 |
| `rebalancing_history.md` | ✅ 첫 이력 등록 (04-14) | briefing-lead | 미국주식 87.8%→72%(6개월 목표) |
| `user_portfolio.md` | ✅ 갱신 완료 (04-14) confidence:high | briefing-lead | 총 2,820만원, 미국주식 87.8% |

---

## 📈 성과 추적 (`knowledge-db/performance/`)

| 파일 | 상태 | 데이터 | 갱신 주기 |
|------|------|-------|---------|
| `2026_recommendations.md` | 🟢 운영 중 | 제안 6건 (전부 진행중) | 매 브리핑 append |
| `2026_hit_rate.md` | ⚠️ 미등록 | — | `/성과리뷰` 첫 실행 시 생성 |
| `2026_scenario_tracking.md` | ⚠️ 미등록 | — | `/글로벌인텔리전스` 첫 실행 시 생성 |

---

## 🗄️ 시계열 원본 DB (`knowledge-db/`)

| 파일 | 레코드 수 | 갱신 주체 |
|------|---------|---------|
| `semiconductor_2026.jsonl` | 71건 | kb-updater |
| `ai_2026.jsonl` | 88건 (Anthropic 34건 포함) | kb-updater |
| `auto_2026.jsonl` | 46건 | kb-updater |
| `energy_2026.jsonl` | 76건 | kb-updater |
| `geopolitics_2026.jsonl` | 32건 | kb-updater |
| `science_tech_2026.jsonl` | 194건 (quantum/space/smr subtag 포함) | kb-updater |
| `bio_pharma_2026.jsonl` | 34건 | kb-updater |
| `macro_2026.jsonl` | 248건 | kb-updater |
| `telecom_next_2026.jsonl` | 28건 | kb-updater |
| `banking_capital_2026.jsonl` | 38건 | kb-updater |
| `advanced_materials_2026.jsonl` | 35건 | kb-updater |
| `battery_2026.jsonl` | 40건 | kb-updater |
| `infrastructure_2026.jsonl` | 23건 | kb-updater |
| `changelog_2026.jsonl` | 32건 | kb-updater |
| `market/2026_daily_prices.md` | — (archive) | market-data-collector |
| `market/2026_economic_indicators.md` | — (FAILED) | market-data-collector |
| `market/2026_guru_changes.md` | — (FAILED) | market-data-collector |
| `market/2026_correlation_log.md` | 0건 | correlation-monitor |

---

## 📚 참조 파일 (`reference/`)

| 파일 | 내용 | 에이전트 참조 시점 |
|------|------|----------------|
| `source_registry.md` | 37개 소스 + 접근성 등급 | data-collector, market-data-collector |
| `rules_and_constraints.md` | 금지사항 31개 | 모든 에이전트 (세션 시작 시) |
| `guru_watchlist.md` | 거물 투자자 8인 명단 | market-data-collector (13F 수집 시) |

---

## 🔄 KB 간 교차 참조 맵 (모순 감지용)

> wiki-linter가 주간 점검 시 이 맵 기준으로 수치 일관성 검증.

| 수치 | 파일 A | 파일 B | 마지막 검증 | 상태 |
|------|-------|-------|-----------|------|
| 미국 Fed 금리 | `us_monetary_policy.md` (루트): redirect 포인터 (수치 없음) | `macro/us_monetary_policy.md`: SSOT — 해당 파일 참조 | 04-13 | ✅ 구조 정리 완료 (루트→redirect 전환) |
| VIX | `global_risk_factors.md`: 19.12 | `us_economy.md §9`: 19.15 | 04-14 | ✅ 일치 (시점차 0.03) |
| DXY | `global_risk_factors.md`: 98.39 | `us_economy.md §9`: 98.65~99.05 | 04-14 | ✅ 일치 (시점차) |
| WTI | `energy.md §1`: $97~100 | `geopolitics.md §6`: $97.22 | 04-14 | ✅ 일치 (양쪽 호르무즈 급등 반영) |
| 원/달러 | `korea_economy.md`: 1,485원 | `global_risk_factors.md §2`: 1,485 | 04-14 | ✅ 일치 (korea_economy 갱신 완료) |
| HBM3E 대중 수출 | `geopolitics.md §1-2`: HBM3E·HBM4 금지 (3.3GB/s/mm² 기준) | `semiconductor.md §5`: HBM3E 이상 금지 | 04-14 | ✅ 일치 (기준 구체화) |

---

## 🏗️ 섹터-종목 빠른 매핑

| 종목/테마 | 1차 KB | 2차 KB (맥락) |
|---------|-------|-------------|
| 삼성전자, SK하이닉스, 한미반도체 | `semiconductor.md` | `macro/geopolitics.md §1`, `macro/korea_economy.md §5-1` |
| NVIDIA, AMD, 브로드컴 | `industry/ai.md §2` | `semiconductor.md §4` |
| Anthropic, OpenAI, Google AI | `industry/ai_anthropic.md`, `industry/ai.md §4` | `macro/geopolitics.md §1-2` |
| 현대차, 기아 | `industry/auto.md §3-2` | `macro/geopolitics.md §1-1` (관세) |
| LG에너지솔루션, 삼성SDI, SK온 | `industry/auto.md §6` | `macro/korea_economy.md §5-3` |
| 한화에어로, LIG넥스원, KAI | `macro/geopolitics.md §4, §5, §8` | `macro/political_cycle.md` (미수집) |
| 두산에너빌리티, 한수원 | `industry/energy.md §7` | `industry/science_tech.md §6` |
| 삼성바이오, 셀트리온 | `industry/bio_pharma.md` | `macro/korea_economy.md §5-5` |
| Gold, TLT, IAU | `macro/global_risk_factors.md §4` | `macro/us_monetary_policy.md` |
| BTC, ETH, SOL | `market/daily_snapshot.md` (FAILED) | `macro/global_risk_factors.md §2` |

---

## 📝 KB 업데이트 이력 (최근 10건)

| 날짜 | 파일 | 변경 | 레코드 |
|------|------|------|-------|
| 2026-04-14 | `macro/supply_chain.md` | **주간 갱신** -- 호르무즈 미군 봉쇄 개시(04/14), 운임 반등(WCI $2,309/SCFI 1707~1827), WTI $104/Brent $98(EIA 연평균 $96), 요소비료 $750(+56%), 구리 $12,630(Triple Demand), HBM sold-out, TSMC 3nm 타이트, Section 122 15% 7/24만료, Section 232 반도체 25%, MATCH법안, 사이버공격 +61%, 희토류 Phase2 유예(~11/10) | +20 |
| 2026-04-14 | `macro/korea_economy.md` | **전면 갱신** -- 기준금리 2.75%→2.50% 정정(7연속 동결), 수출 3월 $86.1B 사상최대(+48.3%), 반도체 $18.7B(+163.9%), KOSPI 5,778(+141% YoY, 기존 2,500 대비 대폭 정정), 원/달러 1,485원, 추경 26.2조 국회통과, 가계부채 관리방안, 이창용→신현송 총재교체, 경상수지 $1,500억 전망 | +22 |
| 2026-04-14 | `industry/science_tech.md` | **전면 갱신** -- 15개 섹션 최신화: 양자(IonQ 99.99%/IQM Shor 2048bit), 6G(3GPP 60%/삼성 TSG RAN 의장), 사이버보안(Wiz $320억/SGNL $7.4억), 로봇(Optimus Gen3/Figure AI $390억), 우주(Starlink 10K기/SpaceX $7,500억), 바이오(경구 GLP-1/CRISPR 359사), SMR(Kairos 2026/Meta-TerraPower 8기), R&D(OECD 3.8T/한국 5.1%), CHIPS Act(Intel 18A 양산/트럼프 지분), EDA(Synopsys L4), 특허(370만건) | +51 |
| 2026-04-14 | `macro/tech_breakthrough.md` | **미수집 4분야 전면 채움** — 양자컴퓨팅(QEC·IonQ $130M·Quantinuum 48논리큐빗·Infleqtion IPO), 로봇(Atlas 양산·Optimus Gen3·Agibot 1만대·Waymo 10도시·Tesla 로보택시), 우주(Starlink 10K위성·1,000만 가입자·SpaceX IPO $1.5T·KASA 1.12조), 신소재(그래핀 EUV·초전도 151K·페로브스카이트 28%·SiC $52B). Disruption Map +5행 | +25 |
| 2026-04-14 | `macro/political_cycle.md` | **갱신** — 미국 관세 IEEPA→Section 122 전환, 반도체 25% 관세, 한국 추경 26.2조+상법3차 확정, 중국·EU·일본·인도 4개국 신규, 리스크캘린더 7건 추가 | +12 |
| 2026-04-14 | `macro/geopolitics.md` | **전면 갱신** — IEEPA 위헌·부산합의 반영(실효 34.7%), 이란전쟁·호르무즈 봉쇄, WTI $97/Brent $102, Gold $4,762, 리스크 5/5 상향, 북한 3일 무기시험, OPEC+ 증산, 희토류 유예 | +20 |
| 2026-04-14 | `macro/global_risk_factors.md` | **전면 갱신** — IMF WEO 4월(3.3%), 호르무즈 봉쇄 1위, VIX 19.12, DXY 98.39, 금 $4,761, 브렌트 $98, IEEPA 관세 무효화, 소비자심리 47.6 역대최저 | +22 |
| 2026-04-13 | `_index.md` | **v3.2 wiki-linter full** — P0 갱신 + Industry 고아파일 8개 등재 + Macro 3개 갱신 확인 + Market 상태 정정 + 교차참조 맵 갱신 | — |
| 2026-04-13 | `_index.md` | **v3.1 완전 재작성** — Wiki Index 전환 (LLM Wiki 원칙 적용) | — |
| 2026-04-09 | `industry/ai_anthropic.md` | **신규 생성** — Anthropic 개별기업 KB (34건) | +34 |
---

## 🤖 에이전트 활용 가이드

```
질문 유형별 1차 참조 파일:

"삼성전자 실적은?" → semiconductor.md §3 컨센서스
"Fed 금리 전망?" → macro/us_monetary_policy.md (루트 파일)
"오늘 시장 상황?" → market/daily_snapshot.md ⚠️ 현재 FAILED
"미중 관세 영향?" → macro/geopolitics.md §1-1
"AI 투자 동향?" → industry/ai.md §3 CapEx
"Anthropic 현황?" → industry/ai_anthropic.md §3 ARR, §6 IPO
"한국 방산 투자?" → macro/geopolitics.md §4, §5, §8
"지정학 리스크?" → macro/global_risk_factors.md §1 Top5
"포트폴리오 구성?" → portfolio/model_portfolios.md ⚠️ 현재 미수집
```

> **에이전트 원칙:** 이 인덱스로 대상 파일 특정 → 해당 파일만 Read → 분석 완료 후 인사이트를 "최근 핵심 인사이트" 섹션에 1줄 append (briefing-lead만).
