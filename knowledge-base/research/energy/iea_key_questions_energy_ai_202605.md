---
title: "IEA Key Questions on Energy and AI — 하이퍼스케일러 CapEx 2025년 $400B 돌파, 2026년 +75% 추가"
sector: energy
topic: iea_key_questions_energy_ai
date_published: 2026-05-08
date_collected: 2026-05-12
last_updated: 2026-05-12
source_type: White Paper
source: "IEA (International Energy Agency)"
url: https://www.iea.org/reports/key-questions-on-energy-and-ai
citation: "📄 [White Paper] IEA Key Questions on Energy and AI (2026-05) — 'Energy Demand from AI'"
key_finding: "IEA가 하이퍼스케일러 CapEx 2025년 $400B+ 돌파, 2026년 +75% 추가 증가 전망을 제시하면서 DC 전력 그리드 병목을 단순 수요 증가가 아닌 'CapEx 가속 자체의 부수효과' 로 재정의 — IEA Electricity 2026 의 'DC 2030 2배' 시나리오 상방 압력"
---

# IEA Key Questions on Energy and AI — Energy Demand from AI

## 핵심 발견 (5건)

- 글로벌 빅테크 통합 CapEx 가 **2025년 $400B+ 돌파**, 2026년 **+75% 추가 증가** 전망 — IEA Key Questions Executive Summary 본문 명시 ("the largest technology companies' capital expenditure exceeded USD 400 billion in 2025 – and is expected to jump by another 75% in 2026").
- **데이터센터 전력 수요 2030년 정량**: IEA 본문 명시 — 글로벌 DC 전력 **2025년 485 TWh → 2030년 약 950 TWh (대략 2배)**. AI 전용 DC 전력은 동기간 **3배** 증가. 2025년 DC 전력 증가율 +17% (AI 전용 DC +50%).
- **그리드 인터커넥션 lead time** 글로벌 명시: IEA 본문은 **"5~10년"** 으로 단일 범위 명시 (특정 주별 세부 분포 없음). PJM·ERCOT·SPP 등 미국 주요 RTO 의 인터커넥션 대기열은 IEA 외 별도 EIA·LBNL 자료가 7~10년대 상단 보고.
- **전력 밀도 폭증**: AI 서버 1랙 단위 전력 밀도 **2020-2025년 11배 증가**, 2027년까지 추가 4배 증가 전망 — 고성능 서버 랙 (대형 냉장고 크기) 1대가 2027년 **65가구 peak 전력 수요**에 상응 (IEA 본문 직접 인용).
- **DC 비유연성**: AI inferencing 트래픽 패턴은 풍력·태양광의 변동성과 매칭이 어려움 → 결과적으로 **베이스로드 (원자력·가스 + 일부 석탄 연장)** 의존이 시나리오상 유지.
- **그리드 CapEx 자체가 thesis** — 트랜스포머, HVDC, 변전소 캐파 부족이 DC 신규 진입 자체를 막고 있어, 그리드 인프라 (TPC·SO·DUK·NEE 송전 자산) 가 신규 베타.

## 데이터·근거

| 항목 | IEA Key Questions (2026-05) | IEA Electricity 2026 (2026-04) |
|---|---|---|
| 글로벌 DC 전력 2025 (TWh) | 485 (확정 보고) | - |
| 글로벌 DC 전력 2030 (TWh) | ~950 (약 2배 baseline) | 약 2배 |
| AI 전용 DC 전력 (2030) | 3배 (baseline, IEA 본문) | 3배 |
| 2025년 DC 전력 증가율 | +17% (AI DC +50%) | (별도 미공개) |
| 하이퍼스케일러 CapEx 2025 | $400B+ (Executive Summary 명시) | - |
| 하이퍼스케일러 CapEx 2026 | +75% (Executive Summary 명시) | - |
| 그리드 인터커넥션 lead time | 5~10년 (IEA 본문 명시, 글로벌 범위) | 5~7년 (글로벌 평균) |
| 전력 밀도 증가 (서버 랙) | 2020-25 11배 + 2027까지 +4배 | (별도 미공개) |

(IEA Key Questions on Energy and AI, Executive Summary, 2026년 발행 — WEO Special Report; IEA 5월 보도자료 "Data centre electricity use surged in 2025")

참고: IEA 본문은 미국 주별 (Virginia/Texas/Ohio/Arizona) 인터커넥션 대기열 세부 분포는 명시하지 않음 — 본 항목은 LBNL Berkeley Lab + EIA 보조 자료 인용. IEA 의 5~10년 명시는 글로벌 범위 단일 수치.

## 분석가 활용 가이드 — Bull / Bear / Contrarian

- **Bull case (CEG · VST · DUK · SO · NEE · TPC · SMR · OKLO · BWXT)**: 그리드 인터커넥션 lead time 7~10년 = DC 수요는 있으나 충족 능력이 부족 → 베이스로드 (원전·SMR·가스) 및 그리드 인프라 자산이 thesis 격상. CEG·VST 의 기존 원자력 자산 가치 재평가, NEE 의 그리드 + 신재생 균형 포트폴리오 강화.
- **Bear case (순수 신재생 + 변동성 자산)**: AI inferencing 패턴은 풍력·태양광 변동성과 매칭이 어려움 → 순수 신재생 비중 높은 사업자 (FSLR, ENPH, SEDG) 의 thesis 가 베이스로드 대비 후순위. 단, 그리드 인프라 결합 (FSLR + 송전망) 시 보완 가능.
- **Contrarian (수요 둔화 시나리오)**: 하이퍼스케일러 CapEx +75% 가이던스 자체가 2024-25 의 GenAI 붐 정점일 가능성. 만약 LLM 학습 단가가 하락하거나 (예: DeepSeek R3+ 류) inference 효율이 급격 개선되면 DC 신규 수요 둔화. 본 시나리오 시 그리드 + 원전 thesis 일시 약화 (그러나 그리드 CapEx 7~10년 lead time → 단기 충격 흡수 불가).

## 한계

- IEA Key Questions 는 White Paper 로, IEA WEO (10월) 의 공식 시나리오 수치보다 정밀도 낮음.
- 하이퍼스케일러 CapEx 가이던스는 분기별로 변동 — 2026 Q2-Q3 회계 결과 시 ±20% 조정 가능.
- "그리드 인터커넥션 lead time 7~10년"은 미국 특정 주 기준 — 전국 평균 또는 글로벌 평균은 다름.
- 무력화: 2026 Q3 까지 미국 그리드 인터커넥션 reform (FERC Order 2026 후속) 또는 ATM (Advanced Transmission Technology) 보급 가속 시 lead time 단축 가능 → 본 thesis 의 "병목" 부분 일부 완화.

## 인용 (Citation)

📄 [White Paper] IEA Key Questions on Energy and AI (2026-05) — "Energy Demand from AI" → 하이퍼스케일러 CapEx 2025년 $400B+ 돌파, 2026년 +75% 추가 + DC 인터커넥션 lead time 7~10년 = 그리드 자체가 thesis

URL: https://www.iea.org/reports/key-questions-on-energy-and-ai (보고서 본문) — Executive Summary 별 페이지: /executive-summary
보조 PDF: https://iea.blob.core.windows.net/assets/3179f7f8-01f6-4dd6-bffa-c9f7b73f1dc9/KeyQuestionsonEnergyandAI.pdf (WEO Special Report 원본 다운로드)
관련: `knowledge-base/research/energy/dc_power_iea_electricity_202604.md` (IEA Electricity 2026 baseline), `knowledge-base/industry/capex.md` (그리드 $720B), `knowledge-base/industry/energy.md` (원자력 풀체인)
