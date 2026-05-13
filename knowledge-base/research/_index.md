---
title: Research KB — L1 주간 헤드라인 인덱스
description: 5개 섹터(반도체·에너지·매크로·바이오·핀테크) × 4개 소스군(학술·씽크탱크·컨퍼런스/백서·규제) 주간 헤드라인 통합 인덱스
created: 2026-05-12
last_updated: 2026-05-13
update_cycle: weekly
status: bootstrapped
total_headlines: 22
---

# Research KB — L1 주간 헤드라인 인덱스

> research-curator 가 매주 갱신. 본 인덱스는 **헤드라인 + 메타데이터** 만 보관. 본문 요약은 L2 (`{sector}/{topic}_{YYYYMM}.md`), 분기 종합은 L3 (`reports/research/{sector}_{YYYY}Q{N}.html`) 에서 다룬다.

## 운용 룰

| 항목 | 값 |
|---|---|
| 갱신 주기 | 주간 (briefing-lead `/주간리포트` Phase 0-A 진입 시 자동 호출) |
| 보존 기간 | 12주 (지난 12주 헤드라인만 유지, 이전은 L2 승격 또는 폐기) |
| 항목당 길이 | 1줄 (제목 + 1줄 요약 + 출처 + 발행일) |
| 인용 형식 | [`_citation_format.md`](_citation_format.md) 참조 |

## 인덱스 구조

각 섹터 섹션 안에 4개 소스군 (학술 / 씽크탱크 / 컨퍼런스/백서 / 규제) 하위로 헤드라인 누적.

---

## 🧠 Semiconductor (반도체)

### 학술
- 📄 [Preprint] arXiv:2511.12286 (2026-04) — "Sangam: Chiplet-Based DRAM-PIM Accelerator with CXL Integration for LLM Inferencing" → CXL-attached PIM-chiplet 메모리 모듈, H100 대비 디코딩 처리량·쿼리 지연 다대일 가속, GPU 대체·병행 사용 시나리오 제시

### 씽크탱크
- 📄 [Think Tank] McKinsey (2026-04-02) — "Computing to Propel Chip Boom" → 글로벌 반도체 시장 2030년 $1.6T (2024년 $775B 대비 CAGR 13%), 컴퓨팅·스토리지가 성장의 55%($460B) 기여
- 📄 [Think Tank] CSIS (2026-04) — "MATCH Act + China Industrial Chain Security Regulations" → 미국 ASML·Nikon·Canon 장비 다자 통제 입법화 추진 + 중국 4월 산업망·공급망 안전 통합 법령 시행

### 컨퍼런스/백서
- 📄 [Conference] ISSCC 2026 (2026-02) — Samsung "36GB HBM4 12-Hi, 3.3 TB/s" → SF4 로직 base die + 1c DRAM 노드 + TSV 4배 증가, 핀당 13Gb/s, 1V 이하 동작 — Rubin 요건 충족
- 📄 [Conference] ISSCC 2026 (2026-02) — SK hynix "48Gbps GDDR7 24Gb + LPDDR6 14.4Gbps + 48GB HBM4 11.7Gbps" → AI 플랫폼 다층 메모리 라인업, SOCAMM2 폼팩터 동시 공개

### 규제
- 📄 [Policy] US BIS / MATCH Act 입법 (2026-04) — "Multilateral Alignment of Technology Controls on Hardware Act" → 미국 단독 통제→동맹 다자 통제 전환, ASML/Nikon/Canon 우회 차단 명문화 시도
- 📄 [Policy] EU Commission (2026-05) — "EU 데이터센터 캐파 3배 확장 7개년 플랜" → EU 자체 클라우드·AI 컴퓨트 자립 정책, 한·미·일 반도체 수출 추가 수요 채널

---

## ⚡ Energy (에너지)

### 학술
- (이번 주 신규 없음 — NBER EEE·SSRN 4월 마지막 주 신규 게재 없음)

### 씽크탱크
- 📄 [Think Tank] IEA Electricity 2026 (2026-04) — "데이터센터 전력 수요 2030년 2배·AI 전용 3배" → 2025년 DC 전력 +17%, AI DC +50% 증가, 미국 전력 수요 증가의 약 50%가 DC 기여
- 📄 [White Paper] IEA Key Questions on Energy and AI (2026-05) — "Energy Demand from AI" → 하이퍼스케일러 CapEx 2025년 $400B 돌파, 2026년 +75% 추가 증가 전망, DC 전력 그리드 병목 가속화

### 컨퍼런스/백서
- (이번 주 신규 없음 — IEA WEO 2026 발표 10월 예정, ANS·BP Outlook 부재)

### 규제
- 📄 [Policy] US NRC Part 53 발효 (2026-04-29) — "Risk-informed Advanced Reactor Licensing" → 3월 26일 의결, 4월 29일 발효. 제조지 연료 주입·운영지 운반 허용·고밀도 인구 지역 입지 가능
- 📄 [Policy] US DOE 의회 증언 (2026-04 중순) — "첫 5~10기 신규 원전 DOE 대출 거의 확정" → 에너지 장관 의회 증언, LPO 자금 SMR/AP1000 일괄 지원 계획 명시
- 📄 [Policy] US NRC TRISO-X 연료 시설 (2026-05 예정) — "X-energy TRISO-X Fuel Facility 최종 라이선스" → 2025년 말 수직 시공 시작, 5월 내 NRC 최종 발급 예상 — SMR 연료 공급망 첫 가시화

---

## 🌍 Macro (매크로)

### 학술
- 📄 [Working Paper] NBER #34894 (2026) — "Inflation vs Inclusion: Stabilization Policy in the Wake of the Pandemic" (Alves & Violante) → 팬데믹 이후 인플레 통제와 포용적 노동시장 회복 간 정책 트레이드오프 정량 분석
- 📄 [Working Paper] BIS WP #1340 (2026-03) — "Stablecoin Flows and Spillovers to FX Markets" → 스테이블코인 자금 흐름이 FX 시장 변동성에 미치는 스필오버 측정, EM 통화 영향 통계적 유의

### 씽크탱크
- 📄 [White Paper] IMF WEO (2026-04-14) — "Global Economy in the Shadow of War" → 글로벌 성장 2026년 3.1%·2027년 3.2% (전망 하향), EM 3.9% (1월 4.2% 대비 하향), 중동 전쟁 인플레 상방 압력
- 📄 [White Paper] BIS Quarterly Review (2026-03) — "Markets recalibrate amid shifting currents" → 달러 약세 + EME 강세, M7·고모멘텀 테크→밸류/시클리컬 로테이션, 일본·호주 장기금리 급등

### 컨퍼런스/백서
- (이번 주 신규 없음 — Jackson Hole 8월·BIS AER 6월 예정, NBER SI 2026 Monetary Economics 7월 예정)

### 규제
- 📄 [Policy] BOJ Summary of Opinions (2026-05-12) — "4월 27-28일 정책결정회의 의견 요약" → 정책금리 0.75% 동결 (6-3 표결, Takata·Tamura·Nakagawa 1.0% 인상 반대), FY2026 코어 CPI 전망 1.9%→2.8% 상향 (중동發 유가 상승 반영). 의사록 본문은 6/19 예정
- 📄 [Policy] FOMC Statement (2026-04-29) — "정책금리 3.5~3.75% 동결 (3회 연속)" → 8-4 비반대 표결로 1992년 10월 이후 최대 dissent, Powell 마지막 주재 회의 가능성. 6/16-17 다음 회의서 dot plot 갱신
- 📄 [Policy] ECB 통화정책결정 (2026-04-30) — "기준금리 동결 (MRO 2.15% / DFR 2.0%)" → 4월 유로존 인플레 3%, 중동 전쟁 에너지가격 상방, 만장일치 동결 + 인상 옵션 토론 — Lagarde 데이터 의존 메시지
- 📄 [Policy] 한국은행 금통위 (2026-04-10) — "기준금리 2.5% 만장일치 동결 (7회 연속)" → 4월 CPI 2.6%(전월 2.2%→), 중동發 공급충격, 신현송 총재 5/28 첫 회의 예정

---

## 🧬 Biotech (바이오)

### 학술
- 📄 [Journal] NEJM (2026) — "Orforglipron Phase 3 ATTAIN-1 (oral GLP-1)" → 경구 GLP-1 수용체 작용제, 비만 환자 체중감소 placebo 대비 통계적 유의, Lilly Foundayo 4/1 FDA 승인 데이터 기반
- 📄 [Journal] NEJM SURMOUNT-5 (2026) — "Tirzepatide vs Semaglutide Head-to-Head" → 72주 추적, 비만/과체중 환자에서 tirzepatide(Zepbound)가 semaglutide(Wegovy)에 우월한 체중감소 — LLY 마진·점유율 thesis 보강

### 씽크탱크
- (이번 주 신규 없음 — McKinsey Pharma·BCG Health Care 4월 게재물 부재)

### 컨퍼런스/백서
- 📄 [Conference] ASCO 2026 (2026-05/06 예정) — RASolute 302 / Daraxonrasib in PDAC plenary → KRAS 억제제 췌장암 3상 plenary 발표 예정, FDA 4/30 expanded access 동시 승인

### 규제
- 📄 [Policy] FDA (2026-04-01) — "Foundayo (orforglipron) 비만 적응증 승인" → 경구 GLP-1, Lilly 처방 채널·복약순응도 확장 → GLP-1 시장 구조 재편
- 📄 [Policy] FDA (2026-04-22) — "Tzield (teplizumab-mzwv) 1세 이상 적응증 확대" → 1형 당뇨 3기 발병 지연, 기존 8세→1세 sBLA 승인
- 📄 [Policy] FDA (2026-05-01) — "Veppanu (vepdegestrant) ESR1m ER+/HER2- 진행성 유방암 승인" → 경구 PROTAC 분해제 종양학 첫 승인 — Arvinas/Pfizer 파트너십
- 📄 [Policy] CMS IRA Negotiation 3차 (2026-04-20) — "Selected Drug List + Maximum Fair Prices 공개" → 15개 약물 (Part B/D), 협상 2026 진행, 가격 효력 2028-01-01. 4월 환자·임상 공청회 진행

---

## 💳 Fintech (핀테크)

### 학술
- 📄 [Working Paper] BIS WP #1340 (2026-03) — "Stablecoin Flows and Spillovers to FX Markets" → 스테이블코인 자금 흐름 FX 시장 스필오버 정량 측정 (Macro에도 인용)
- 📄 [Policy] BIS Papers #170 (2026-05-05) — "Impact of Stablecoins on International Monetary and Financial System" → EMDE 통화주권·MoE 역할 침식 우려, "사운드 머니" 미달성 + 분절적 규제 위험

### 씽크탱크
- 📄 [Think Tank] BIS Briefing (2026-04-20) — "Global Stablecoin Rulemaking Slowdown" → 글로벌 스테이블코인 규제 진전 둔화, BIS 협력 촉구, 단편화 시 시장 리스크 증폭·규제 차익 경고

### 컨퍼런스/백서
- (이번 주 신규 없음 — Money 20/20 10월 예정, Davos WEF 1월 완료 후속 부재)

### 규제
- 📄 [Policy] SEC Press Release 2026-30 (2026-03-17) — "SEC + CFTC 공동 암호자산 연방증권법 적용 해석" → token taxonomy 정립: digital commodities/collectibles/tools/stablecoins/digital securities — Atkins 의장 "10년 불확실성 해소"
- 📄 [Policy] SEC Staff Statement (2026-04-13) — "셀프 호스팅 지갑 인터페이스 브로커 미해당" → self-custody 지갑 거래 소프트웨어는 broker 규제 트리거 X — 디파이·온체인 지갑 사업자 진입 장벽 완화

---

## 보존 룰 (12주 슬라이딩 윈도우)

- 12주 (84일) 경과 헤드라인 자동 제거 (research-curator weekly 모드가 처리)
- 단, 다음 중 하나라도 해당하면 **L2 승격**:
  - L2 월간 수집에 활용됨 (월간 모드가 인용)
  - capex.md / industry KB 의 thesis 와 연결됨
  - 사용자가 명시적으로 표시 (`[KEEP]` 태그 부착)

## 차주 갱신 예상 항목 (2026-05-19 트래킹)

- **반도체**: VLSI Symposium 2026 (6월) 사전 paper digest, ISSCC 2026 양산 일정 후속, BIS/MATCH Act 의회 진전
- **에너지**: NRC X-energy TRISO-X 최종 라이선스 결과, DOE LPO 신규 disbursement, 중동 분쟁發 LNG 가격 동향
- **매크로**: BOJ 4월 회의 결과 (5월 발표), 한국은행 5/28 첫 신현송 회의 신호, IMF WEO 4월 후속 글로벌 부채 보조 보고
- **바이오**: ASCO 2026 plenary (5월말~6월) RASolute 302 + 신규 oncology 3상, FDA AdCom 5월 일정
- **핀테크**: SEC 추가 가이드라인 (스테이블코인·custody), 한국 금융위 가상자산법 시행령

## 폴백/미수집

- 한국 산업통상자원부 K-Chips 보도자료 4월 — 검색 실패, 다음 주 재시도
- bioRxiv/medRxiv 4월 신규 preprint — 검색 결과 일반 정보만, 구체 trial 미특정
- NBER EEE·SSRN Energy Economics 4월 마지막 주 — 신규 게재 없음
- 일본 METI 4월 보조금 보도 — 본 회차 미커버, 다음 회차 추가
