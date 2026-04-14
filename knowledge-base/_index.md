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
| `macro/political_cycle.md` | ✅ 갱신 완료 (04-13) confidence:high | G-2, C-3 | — |
| `macro/tech_breakthrough.md` | ✅ 갱신 완료 (04-13) confidence:high | G-3, C-3.5 | — |
| `macro/supply_chain.md` | ✅ 갱신 완료 (04-13) confidence:high | G-1, C-3 | — |
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

---

## 🏭 Industry KB (`knowledge-base/industry/`)

| 파일 | 핵심 수치 | 최신 인사이트 | 갱신일 | 유효기간 | 신뢰도 |
|------|---------|------------|-------|---------|-------|
| `semiconductor.md` | 삼성 2026E OP 45~65조, SK 23~30조, HBM4 H2 양산 | 관세 간접 타격 -5~10% 우려 추가. 삼성 파운드리 3nm 수율 60% 미만 지속 | 04-07 | 05-07 | medium |
| `ai.md` | 글로벌 AI 시장 3,300~3,800억달러, CapEx 합산 2,950~3,200억 | DeepSeek 쇼크 후 CapEx 오히려 상향. 추론(Inference) 60%+ 비중 전환 | 04-07 | 05-07 | medium |
| `ai_anthropic.md` | ARR $300억, 밸류 $3,800억, IPO 2026 Q4 목표 | OpenAI ARR 최초 추월. 엔터프라이즈 40% 점유. Pentagon 갈등 리스크 | 04-09 | 05-09 | high |
| `auto.md` | HMG 750만대(글로벌 3위), 미국 관세 25% 발효 | 조지아 30만대로 부분 완충. 관세로 연간 이익 1.5~2.5조 감소 우려 | 04-07 | 05-07 | medium |
| `energy.md` | WTI $68~72, Brent $72~76, JKM LNG $12~14 | OPEC+ 감산 유지. 두산에너빌리티 체코 기자재 2026 발주 기대 | 04-07 | 05-07 | medium |
| `science_tech.md` | 한국 R&D/GDP 4.9%(세계 1위), 정부 R&D 29.6조 | AI↔에너지 결합 메가트렌드. Tesla Optimus 2026 양산 개시 | 04-07 | 05-07 | medium |
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
| `us_economy.md` | GDP +2.7%(2025), +2.0%(2026E), Core CPI +3.1%, 침체확률 25~40% | 관세발 스태그플레이션. AI 투자(+0.3~0.5%p GDP 기여)가 부분 상쇄 | 04-07 | medium |
| `us_monetary_policy.md` | SSOT: `macro/us_monetary_policy.md` 참조 (루트 파일 = redirect 포인터) | 루트 파일 confidence:redirect — 수치 직접 참조 금지 | 04-13 | redirect |
| `geopolitics.md` | 관세 미→중 145%, 중→미 125%. HBM3E 이상 대중 금지 | 대만 충돌(저확률·극고영향). 희토류 전면금지(저확률·고영향) | 04-07 | high |
| `korea_economy.md` | GDP +1.9%(2026E), 금리 2.75%, 원화 1,410원 | 대미 관세 + 대중 수출 이중 타격. 가계부채 GDP 92~95% | 04-07 | medium |
| `global_risk_factors.md` | VIX 27~32(불안), F&G 25~35(Fear), 금 $2,900~3,100 | Top5 리스크: 미중·대만·부채·중동·기후 | 04-07 | high |
| `political_cycle.md` | 주요국 정치 일정·정책 변화·섹터 임팩트 | G-2 모듈 정상 운영 가능 | 04-13 | ✅ high |
| `tech_breakthrough.md` | AI·반도체·양자·바이오·에너지·로봇 기술 단계 판정 | G-3 모듈 정상 운영 가능 | 04-13 | ✅ high |
| `supply_chain.md` | 물류/운임·핵심광물·리쇼어링 현황 | G-1 공급망 모듈 정상 운영 가능 | 04-13 | ✅ high |

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
| `energy_2026.jsonl` | 42건 | kb-updater |
| `geopolitics_2026.jsonl` | 32건 | kb-updater |
| `science_tech_2026.jsonl` | 143건 (quantum/space/smr subtag 포함) | kb-updater |
| `bio_pharma_2026.jsonl` | 34건 | kb-updater |
| `macro_2026.jsonl` | 133건 | kb-updater |
| `telecom_next_2026.jsonl` | 28건 | kb-updater |
| `banking_capital_2026.jsonl` | 38건 | kb-updater |
| `advanced_materials_2026.jsonl` | 35건 | kb-updater |
| `battery_2026.jsonl` | 40건 | kb-updater |
| `infrastructure_2026.jsonl` | 23건 | kb-updater |
| `changelog_2026.jsonl` | 23건 | kb-updater |
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
| VIX | `global_risk_factors.md`: 27~32 | `us_economy.md §9`: 27~32 | 04-07 | ✅ 일치 |
| DXY | `global_risk_factors.md`: 101~104 | `us_economy.md §9`: 101~104 | 04-07 | ✅ 일치 |
| WTI | `energy.md §1`: $68~72 | `geopolitics.md §6`: $68~72 | 04-07 | ✅ 일치 |
| 원/달러 | `korea_economy.md`: 1,410원 | `global_risk_factors.md §2`: 1,420~1,460 | 04-07 | ⚠️ 범위 불일치 (허용 범위 내) |
| HBM3E 대중 수출 | `geopolitics.md §1-2`: 전면금지 | `semiconductor.md §5`: HBM3E 이상 금지 | 04-07 | ✅ 일치 |

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
| 2026-04-13 | `_index.md` | **v3.2 wiki-linter full** — P0 갱신 + Industry 고아파일 8개 등재 + Macro 3개 갱신 확인 + Market 상태 정정 + 교차참조 맵 갱신 | — |
| 2026-04-13 | `_index.md` | **v3.1 완전 재작성** — Wiki Index 전환 (LLM Wiki 원칙 적용) | — |
| 2026-04-09 | `industry/ai_anthropic.md` | **신규 생성** — Anthropic 개별기업 KB (34건) | +34 |
| 2026-04-09 | `knowledge-db/ai_2026.jsonl` | Anthropic 데이터 추가 (53→87건) | +34 |
| 2026-04-08 | `_index.md` (구버전) | F-07 처리 — performance KB + market KB 권한 컬럼 | — |
| 2026-04-07 | `macro/us_economy.md` | 신규 생성 — 미국 경제 KB 전면 구축 (33건) | +33 |
| 2026-04-07 | `macro/korea_economy.md` | 신규 생성 — 한국 경제 KB 전면 구축 (38건) | +38 |
| 2026-04-07 | `semiconductor.md` | 2차 갱신 — DB 71건(+22건), 관세 영향·HBM4 추가 | +22 |
| 2026-04-07 | `macro/geopolitics.md` | 신규 생성 — 지정학 KB 전면 갱신 | +31 |
| 2026-04-07 | `macro/global_risk_factors.md` | 신규 생성 — 글로벌 Top5 리스크 | — |
| 2026-04-07 | `industry/ai.md` | 신규 생성 — AI 섹터 KB (53건) | +53 |

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
