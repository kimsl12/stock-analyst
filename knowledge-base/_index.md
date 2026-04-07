---
updated: 2026-04-07
---

# Knowledge Base Index

## 섹터-종목 매핑

| 섹터 | 대표 종목 | KB 파일 | 관련 매크로 |
|------|----------|---------|------------|
| 반도체 | 삼성전자, SK하이닉스, 마이크론, 한미반도체 | `semiconductor.md` | 미중관계, 금리, 관세 |
| AI 인프라 | NVIDIA, AMD, 브로드컴, TSMC | `industry/ai.md` | 금리, 기술규제, CapEx |
| AI 생태계 | OpenAI, Anthropic, Google, 네이버, 카카오 | `industry/ai.md` | AI 규제, 오픈소스 경쟁 |
| 에너지 | SK이노베이션, GS칼텍스, S-Oil, 한국전력, 두산에너빌리티, 한화솔루션 | `industry/energy.md` | 유가, 지정학, 탄소중립 |
| 2차전지 | LG에너지솔루션, CATL | `industry/battery.md` | 리튬가격, EV정책 |
| 바이오 | 삼성바이오, 셀트리온 | `industry/bio_pharma.md` | FDA, 환율 |
| 자동차 | 현대차, 기아, 토요타, BYD, 테슬라 | `industry/auto.md` | IRA, 관세, 리튬가격, EV정책 |

## 매크로 KB

| 파일 | 커버리지 | 최종 업데이트 |
|------|---------|------------|
| `macro/us_economy.md` | 미국 GDP, 고용, 인플레, 소비, PMI, 주택, 무역, 재정, Fed 정책, 리스크 | 2026-04-07 |
| `macro/us_monetary_policy.md` | Fed 금리, QT, 인플레이션 (요약 포인터 — 상세는 us_economy.md) | 2026-04-07 |
| `macro/geopolitics.md` | 미중 관세·기술전쟁, 대만, 중동, 북한, 유럽, 공급망 | 2026-04-07 |
| `macro/korea_economy.md` | 한국 GDP, 환율, 수출, 금리, 산업별 동향, 정책·규제 | 2026-04-07 |
| `macro/global_risk_factors.md` | 글로벌 Top 5 리스크, 시장 심리 지표, 원자재 가격 | 2026-04-07 |

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
| 2026-04-07 | `semiconductor.md` | **전면 갱신 (2차)** — DB 71건(+22건) 기반. 트럼프 관세 간접영향, 2026Q1 실적 프리뷰, 장비/소재 섹션, HBM4 스펙, 중국 자급화, 밸류에이션 신규 추가 |
| 2026-04-07 | `macro/us_economy.md` | 신규 생성 — 미국 경제 KB 전면 구축 (DB 33건 기반, GDP·고용·인플레·소비·PMI·주택·무역·재정·Fed·리스크 전 항목) |
| 2026-04-07 | `us_monetary_policy.md` | 갱신 — 미수집 해소, macro/us_economy.md 요약 포인터로 전환 |
| 2026-04-07 | `knowledge-db/macro_2026.jsonl` | 미국 경제 데이터 33건 추가 (기존 39건 → 총 72건) |
| 2026-04-07 | `macro/korea_economy.md` | 신규 생성 — 한국 경제 KB 전면 구축 (DB 38건 기반, GDP·금리·환율·수출·산업·정책 전 항목) |
| 2026-04-07 | `korea_economy.md` (루트) | 전면 갱신 — 미수집 해소, macro/korea_economy.md 요약본으로 전환 |
| 2026-04-07 | `knowledge-db/macro_2026.jsonl` | 신규 생성 — 한국 매크로 DB 38건 축적 |
| 2026-04-07 | `semiconductor.md` | 1차 갱신 — DB 49건 기반, 전 항목 최신화 (미수집 0건) |
| 2026-04-07 | `industry/auto.md` | 신규 생성 — 자동차 섹터 KB 최초 구축 (DB 45건 기반) |
| 2026-04-07 | `macro/geopolitics.md` | 신규 생성 — 지정학 KB 전면 갱신 (미중·대만·중동·북한·유럽·공급망) |
| 2026-04-07 | `macro/global_risk_factors.md` | 신규 생성 — 글로벌 Top5 리스크, 시장심리, 원자재 현황 |
| 2026-04-07 | `knowledge-db/geopolitics_2026.jsonl` | 신규 생성 — 지정학 DB 31건 축적 |
| 2026-04-07 | `industry/energy.md` | 신규 생성 — 에너지 섹터 KB 최초 구축 (DB 40건 기반) |
| 2026-04-07 | `knowledge-db/energy_2026.jsonl` | 신규 생성 — 에너지 DB 40건 축적 |
| 2026-04-07 | `industry/ai.md` | 신규 생성 — AI 섹터 KB 최초 구축 (DB 53건 기반, 전 분야 커버) |
| 2026-04-07 | `knowledge-db/ai_2026.jsonl` | 신규 생성 — AI DB 53건 축적 |
