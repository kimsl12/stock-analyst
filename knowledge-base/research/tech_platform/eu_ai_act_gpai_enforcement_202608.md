---
title: "EU AI Act Chapter V — GPAI(범용 AI) 집행 권한 2026-08-02 발효 + 과징금 개시"
sector: tech_platform
topic: eu_ai_act_gpai_enforcement
date_published: 2026-08-01
date_collected: 2026-08-01
last_updated: 2026-08-01
source_type: Policy
source: "EU AI Act — Chapter V (artificialintelligenceact.eu 해설 + EU AI Office)"
url: https://artificialintelligenceact.eu/enforcement-of-chapter-v-under-the-eu-ai-act/
citation: "📄 [Policy] EU AI Act Ch.V — Art.91~93·101 (2026-08-02 집행 발효)"
key_finding: "GPAI(범용 AI) 모델 제공자 의무는 2025-08-02 발효됐으나, EU 집행위(AI Office)의 감독·집행 권한은 정확히 1년 뒤인 2026-08-02 발효. 이날부터 정보요구(Art.91)·평가(Art.92)·시정/회수(Art.93)·과징금(Art.101)이 실제 집행 가능. 과징금 상한은 '전세계 매출 3% 또는 €1,500만 중 큰 금액'. 2025-08-02 이전 출시 모델은 2027-08-02까지 유예, 이후 출시 모델은 시장 출시 즉시 준수 의무. GPAI 제공자는 하위 제공자용 문서화·EU 저작권 준수 정책·학습데이터 요약 공개가 핵심 의무."
---

# EU AI Act Chapter V — GPAI 집행 발효 (2026-08-02)

> 신규 tech_platform 섹터 L2 보강분(2026-08). 기존 `eu_ai_act_omnibus_202606`(고위험 AI 마감 연장)와 구분되는 **범용 AI(GPAI) 집행 개시** 트랙. 수집 시점(2026-08-01) 바로 다음 날이 집행 발효일이라 카탈리스트 타이밍이 정확.

## 핵심 발견 (5건)

- **의무 발효(2025-08-02) vs 집행 발효(2026-08-02) 분리**: GPAI 모델 제공자 의무는 2025-08-02 적용됐으나, EU AI Office 의 **감독·집행 권한**은 정확히 1년 유예 후 **2026-08-02** 발효. 원문 인용 _"While GPAI model providers' obligations took effect on August 2, 2025, the Commission's supervision and enforcement powers activate one year later on August 2, 2026."_ (📄 artificialintelligenceact.eu, Ch.V 해설).
- **집행 4대 권한**: ① 정보요구(Art.91 — 문서·기술사양·준수 증거), ② 평가(Art.92 — 준수 검증·시스템 리스크 조사), ③ 시정조치(Art.93 — 준수·리스크 완화·시장 제한/리콜), ④ 과징금(Art.101).
- **과징금 상한**: **전세계 연매출 3% 또는 €1,500만 중 큰 금액**. (금지 관행 위반에 적용되는 매출 7%/€3,500만 최고 구간과 구분 — 본 GPAI 트랙은 3%/€15M 구간.)
- **준수 타임라인 이원화**: 2025-08-02 **이전** 시장 출시 모델은 **2027-08-02**까지 준수 유예. 2025-08-02 **이후** 출시 모델은 **시장 출시 즉시** 준수 의무.
- **GPAI 제공자 핵심 의무**: 하위 제공자(downstream)용 정보·문서 유지·제공, EU 저작권 준수 정책 채택, 학습 콘텐츠 요약 공개. 시스템 리스크 보유 GPAI(대형 파운데이션 모델)는 추가로 모델 평가·리스크 평가·중대 인시던트 보고·사이버보안 의무.

## 데이터·근거

| 항목         | 내용                                                           | 출처                       |
| ------------ | -------------------------------------------------------------- | -------------------------- |
| 의무 발효    | 2025-08-02 (GPAI 제공자)                                       | 📄 [Policy] EU AI Act Ch.V |
| 집행 발효    | 2026-08-02 (AI Office 감독·과징금)                             | 📄 [Policy] EU AI Act Ch.V |
| 과징금 상한  | 매출 3% 또는 €15M 중 큰 금액 (Art.101)                         | 📄 [Policy] EU AI Act Ch.V |
| 유예(구모델) | 2025-08-02 이전 출시 → 2027-08-02 준수                         | 📄 [Policy] EU AI Act Ch.V |
| 집행 권한    | 정보요구·평가·시정/리콜·과징금                                 | 📄 [Policy] Art.91~93·101  |
| 관련(보조)   | GPAI Code of Practice 최종본 2025-07-10 공개(자발적 준수 도구) | 검색 헤드라인              |

## 분석가 활용 가이드 — Bull / Bear / Contrarian

- **Bull case (규제 명확성 = 대형 선점)**: 집행 발효로 컴플라이언스 역량·법무 자원을 갖춘 대형(MSFT/OpenAI·GOOGL·META·AMZN·AAPL)이 유리 — 문서화·저작권·리스크 평가 인프라 선점 시 EU 시장 접근 유지. 규제 불확실성 해소는 엔터프라이즈 AI 도입(CRM Agentforce·NOW·ORCL) 채택 안정화 요인.
- **Bear case (과징금·컴플라이언스 비용)**: 매출 3%(글로벌 매출 기준) 과징금은 빅테크에 실질 위협 — 학습데이터 요약 공개·저작권 정책은 소송·경쟁 정보 노출 리스크. 오픈소스/스타트업엔 문서화 부담이 진입장벽. 미-EU 규제 마찰(무역·디지털) 재점화 가능.
- **Contrarian (집행 유예의 실효성 논쟁)**: 집행 권한은 8/2 발효되나 실제 과징금 부과까지는 조사·시정 절차가 선행 — 즉각적 처벌보다 "정보요구→시정" 단계가 먼저. 시장이 "8/2 집행 = 즉시 벌금"으로 과잉 반응하면 오히려 역발상 기회. 구모델(2027-08-02 유예)이 대다수라 단기 실집행 범위는 제한적일 수 있음.

## 한계

- 본 요약은 artificialintelligenceact.eu(민간 해설 포털) 의 Chapter V 정리를 fetch 한 것 — 조문 번호(Art.91~93·101)·날짜는 해설 기준. 실제 조문·EU AI Office 공식 가이드라인과 교차 확인 권장.
- GPAI Code of Practice(2025-07-10 최종본)는 검색 헤드라인 기반 보조 정보 — 개별 원문 딥페치 미수행.
- 무력화 조건: EU 집행위가 집행 우선순위를 시스템 리스크 대형 모델에 한정하거나, 미-EU 규제 협상으로 적용 완화 시 실질 영향 축소.

## 인용 (Citation)

📄 [Policy] EU AI Act Chapter V — Art.91~93·101 (2026-08-02 집행 발효) → GPAI 모델 제공자 감독·집행 권한 발효 + 과징금 매출 3%/€15M + 구모델 2027-08-02 유예 → 빅테크 EU AI 컴플라이언스 비용·시장 접근 리스크

URL: https://artificialintelligenceact.eu/enforcement-of-chapter-v-under-the-eu-ai-act/ (Chapter V 집행 해설, 2026-08-02 발효 기준)
보조(검색 헤드라인, 딥페치 미수행): GPAI Code of Practice 최종본 2025-07-10 공개(자발적 준수 도구), 의무 적용 2025-08-02
관련: `knowledge-base/research/tech_platform/_meta.md`, `knowledge-base/research/tech_platform/eu_ai_act_omnibus_202606.md`, `knowledge-base/industry/ai.md`
