---
title: Research KB — L1 주간 헤드라인 인덱스
description: 10개 섹터(반도체·에너지·매크로·바이오·핀테크·방산·테크플랫폼·소비재·산업재·자동차) × 4개 소스군(학술·씽크탱크·컨퍼런스/백서·규제) 주간 헤드라인 통합 인덱스
created: 2026-05-12
last_updated: 2026-05-16
update_cycle: weekly
status: active
total_headlines: 35
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
- 📄 [Preprint] arXiv:2511.06838 (2026-05) — "P3-LLM: An Integrated NPU-PIM Accelerator for LLM Inference Using Hybrid Numerical Formats" → HBM-PIM/Ecco/Pimba 대비 평균 3.4배 가속, 하이브리드 수치 포맷으로 LLM 추론 최적화

### 씽크탱크
- 📄 [Think Tank] McKinsey (2026-04-02) — "Computing to Propel Chip Boom" → 글로벌 반도체 시장 2030년 $1.6T (2024년 $775B 대비 CAGR 13%), 컴퓨팅·스토리지가 성장의 55%($460B) 기여
- 📄 [Think Tank] CSIS (2026-04) — "MATCH Act + China Industrial Chain Security Regulations" → 미국 ASML·Nikon·Canon 장비 다자 통제 입법화 추진 + 중국 4월 산업망·공급망 안전 통합 법령 시행

### 컨퍼런스/백서
- 📄 [Conference] ISSCC 2026 (2026-02) — Samsung "36GB HBM4 12-Hi, 3.3 TB/s" → SF4 로직 base die + 1c DRAM 노드 + TSV 4배 증가, 핀당 13Gb/s, 1V 이하 동작 — Rubin 요건 충족
- 📄 [Conference] ISSCC 2026 (2026-02) — SK hynix "48Gbps GDDR7 24Gb + LPDDR6 14.4Gbps + 48GB HBM4 11.7Gbps" → AI 플랫폼 다층 메모리 라인업, SOCAMM2 폼팩터 동시 공개

### 규제
- 📄 [Policy] US BIS / MATCH Act 입법 (2026-04) — "Multilateral Alignment of Technology Controls on Hardware Act" → 미국 단독 통제→동맹 다자 통제 전환, ASML/Nikon/Canon 우회 차단 명문화 시도
- 📄 [Policy] EU Commission (2026-05) — "EU 데이터센터 캐파 3배 확장 7개년 플랜" → EU 자체 클라우드·AI 컴퓨트 자립 정책, 한·미·일 반도체 수출 추가 수요 채널
- 📄 [Policy] US CHIPS Act Phase 2 진행 (2026-05) — "TSMC AZ Fab21 3nm 장비 입고 Q3 2026, Samsung Taylor TPU/FSD 칩 다년 계약" → TSMC 3nm 양산 2027년 (원래 2028→1년 단축), Samsung Taylor — Tesla AI5/AI6 + Alphabet TPU 다년 계약 체결 ([source](https://markets.financialcontent.com/wral/article/tokenring-2026-1-1-the-silicon-renaissance-us-chips-act-enters-production-era-as-intel-tsmc-and-samsung-hit-critical-milestones))

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
- 📄 [Policy] US NRC TRISO-X 연료 시설 (2026-02-16, 확정) — "X-energy TRISO-X TX-1 Category II 라이선스 발급" → 첫 미국 Category II HALEU 연료 제조 시설 인가, 40년 라이선스, TX-1 연 5톤U / 70만 TRISO 페블, Oak Ridge 입지 — 예정 일정(5월) 대비 3개월 앞당겨 2월 16일 발급 ([source](https://www.world-nuclear-news.org/articles/us-regulator-issues-licence-for-triso-x-fuel-facility)) [KEEP — SMR thesis 핵심]

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
- 📄 [Policy] FOMC 6/16-17 일정 확정 (2026-05) — "SEP/Dot Plot 갱신 회의" → 4월 dot plot 유지 시 2026년 25bp 1회 인하 시그널. 4월 의사록 5/20 공개 예정 (3주 룰)
- 📄 [Policy] ECB 통화정책결정 (2026-04-30) — "기준금리 동결 (MRO 2.15% / DFR 2.0%)" → 4월 유로존 인플레 3%, 중동 전쟁 에너지가격 상방, 만장일치 동결 + 인상 옵션 토론 — Lagarde 데이터 의존 메시지
- 📄 [Policy] 한국은행 신현송 신임 총재 (2026-04-21 취임) — "5/28 첫 MPC 주재 예정, 금리 중립 수준 평가" → 인사청문에서 "현 정책금리 중립 수준 근접" 발언, 시장 동결 컨센서스. 중동 전쟁發 공급 충격 평가가 변수 ([source](https://www.kedglobal.com/central-bank/newsView/ked202604210005))

---

## 🧬 Biotech (바이오)

### 학술
- 📄 [Journal] NEJM (2026) — "Orforglipron Phase 3 ATTAIN-1 (oral GLP-1)" → 경구 GLP-1 수용체 작용제, 비만 환자 체중감소 placebo 대비 통계적 유의, Lilly Foundayo 4/1 FDA 승인 데이터 기반
- 📄 [Journal] NEJM SURMOUNT-5 (2026) — "Tirzepatide vs Semaglutide Head-to-Head" → 72주 추적, 비만/과체중 환자에서 tirzepatide(Zepbound)가 semaglutide(Wegovy)에 우월한 체중감소 — LLY 마진·점유율 thesis 보강

### 씽크탱크
- (이번 주 신규 없음 — McKinsey Pharma·BCG Health Care 4월 게재물 부재)

### 컨퍼런스/백서
- 📄 [Conference] ASCO 2026 (2026-05-31, plenary 확정) — "RASolute 302 / Daraxonrasib in PDAC plenary" → 5/31 15:21 CDT McCormick Place Hall B1, Dr. Wolpin 발표. mOS 13.2 vs 6.7개월, HR 0.40 (P<.0001), 사망위험 60% 감소 — KRAS G12 변이 PDAC 첫 명확한 OS 우월성. Revolution Medicines 가치 재평가 모멘텀 ([source](https://ascopost.com/issues/may-10-2026/ras-inhibitor-daraxonrasib-in-metastatic-pancreatic-cancer/)) [KEEP — Bio thesis 핵심]

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

## 🛡️ Defense (방산·항공)

### 학술
- (이번 주 신규 없음 — RUSI·CNAS 5월 학술 게재물 부재, 다음 회차 SSRN 정치경제 분야 재시도)

### 씽크탱크
- 📄 [Think Tank] CSIS (2026-05-08) — "Deepening Strategic Alignment: Priorities for the U.S.-Japan Alliance" (Johnstone & Rubinstein) → 일본 5개년 방위비 +60%·1년차 +25% 단계 진입, 장사거리 정밀타격·능동 사이버·우주 자산 투자 확대 — 한미일 통합 억제·역할분담 재정립 ([source](https://www.csis.org/analysis/deepening-strategic-alignment-priorities-us-japan-alliance))
- 📄 [Think Tank] SIPRI Fact Sheet (2026-04) — "2025 World Military Expenditure" → 글로벌 군사비 사상 최고 갱신, 한국 2025년 $47.8B (+2.6%) — 3축 체계 (미사일방어·선제타격·보복능력) 지속 투자 ([source](https://www.sipri.org/sites/default/files/2026-04/2604_milex_2025.pdf))

### 컨퍼런스/백서
- (이번 주 신규 없음 — RIAT·AUSA·DSEI 일정 외)

### 규제
- (이번 주 신규 없음 — DoD FY27 예산안 6월 의회 송부 예정)

---

## 💻 Tech / Platform (빅테크·SaaS·플랫폼)

### 학술
- (이번 주 신규 없음 — NeurIPS·ICML 페이퍼 트랙 6월 예정)

### 씽크탱크
- (이번 주 신규 없음)

### 컨퍼런스/백서
- (이번 주 신규 없음 — Google I/O 5월 완료, MS Build 5월말 예정 후속)

### 규제
- 📄 [Policy] EU AI Act Omnibus 정치 합의 (2026-05-07) — "고위험 AI 시스템 컴플라이언스 마감 연장 + 규칙 명료화" → AI 생성 친밀 콘텐츠 신규 규칙. Annex III 고위험 AI(고용·신용·교육·법 집행) 2026-08-02 시행. 위반 시 최대 €35M / 글로벌 매출 7% 과징금 ([source](https://www.lw.com/en/insights/ai-act-update-eu-resolves-to-change-rules-and-extend-deadlines))
- 📄 [Policy] EU Commission AI 투명성 가이드라인 협의 (2026-05) — "AI Office 시행·감독 권한 명료화" → 회원국 당국 + AI Office 양층 거버넌스, draft Code of Practice 공개 — 하이퍼스케일러 컴플라이언스 비용 가중

---

## 🛍️ Consumer (소비재·리테일·식음료)

### 학술
- (이번 주 신규 없음 — NBER Industrial Organization·SSRN Retail 4월 마지막 주 신규 부재)

### 씽크탱크
- (이번 주 신규 없음)

### 컨퍼런스/백서
- (이번 주 신규 없음 — Shoptalk 3월 완료, NRF Big Show 1월 완료)

### 규제
- 📄 [Filing] Walmart Q1 FY26 Earnings (2026-05-15) — "EPS 0.61(예 0.58) / 매출 $165.61B(예 $165.84B) / e커머스 첫 분기 흑자" → 미국 평균 객단가 +2.8% YoY, 거래 +1.6%. CFO Rainey "5월 말 가격 인상 가능" — 관세 전가 본격화 신호. Target/HD/Lowe's 차주 어닝 대기 ([source](https://corporate.walmart.com/content/dam/corporate/documents/newsroom/2025/05/15/walmart-releases-q1-fy26-earnings/q1-fy26-earnings-release.pdf))

---

## 🏭 Industrials (산업재·인프라·물류)

### 학술
- (이번 주 신규 없음 — NBER Productivity·SSRN OM 4월 마지막 주 신규 부재)

### 씽크탱크
- 📄 [Think Tank] Westside Construction / CHIPS Act 건설 (2026-05) — "America's Semiconductor Construction Boom" → TSMC AZ Phase 2 완공·장비 입고 Q3 2026, Samsung Taylor 장비 이전 중, Intel 18A AZ 가동 — 미국 첨단 제조 클러스터 본격 전환기 ([source](https://www.buildwcg.com/blog-posts/semiconductor-fab-construction-boom-2026))

### 컨퍼런스/백서
- (이번 주 신규 없음)

### 규제
- (이번 주 신규 없음)

---

## 🚗 Auto / Mobility (자동차·EV·배터리)

### 학술
- 📄 [Working Paper] SIEPR Stanford Policy Brief (2026) — "Clean vehicle tax credit: The new industrial policy and its impact" → IRA 30D 신차 EV 크레딧이 산업정책 회귀 사례. Tesla/GM은 30D 후속 IRA 적격 재진입 (Model 3/Y + Lyriq/Bolt/Bolt EUV) ([source](https://siepr.stanford.edu/publications/policy-brief/clean-vehicle-tax-credit-new-industrial-policy-and-its-impact))

### 씽크탱크
- (이번 주 신규 없음 — McKinsey Mobility 4월 게재물 부재)

### 컨퍼런스/백서
- (이번 주 신규 없음 — Auto Shanghai 4월 완료, Munich IAA 9월 예정)

### 규제
- 📄 [Policy] IRA 30D 신차 EV 크레딧 (확정 적용) — "2026년 배터리 부품 70% / 핵심광물 70% 요건 단계 상향" → 부품 80%('27)→90%('28)→100%('29), 광물 80%('27~). Tesla 공지 "연방 EV 크레딧 9/30 종료" 시나리오 동시 부상 — 사이클 후반부 수요 풀인 ([source](https://www.tesla.com/IRA))

---

## 보존 룰 (12주 슬라이딩 윈도우)

- 12주 (84일) 경과 헤드라인 자동 제거 (research-curator weekly 모드가 처리)
- 단, 다음 중 하나라도 해당하면 **L2 승격**:
  - L2 월간 수집에 활용됨 (월간 모드가 인용)
  - capex.md / industry KB 의 thesis 와 연결됨
  - 사용자가 명시적으로 표시 (`[KEEP]` 태그 부착)

## 차주 갱신 예상 항목 (2026-05-23 트래킹)

- **반도체**: VLSI Symposium 2026 (6월) 사전 paper digest, ISSCC 2026 양산 일정 후속, BIS/MATCH Act 의회 진전
- **에너지**: DOE LPO 신규 disbursement, 중동 분쟁發 LNG 가격 동향, NRC SMR 신규 ESP 신청 동향
- **매크로**: FOMC 4월 의사록 5/20 공개, 한국은행 5/28 첫 신현송 회의 결과, BOJ 의사록 본문 6/19, IMF WEO 후속 글로벌 부채 보조 보고
- **바이오**: ASCO 2026 plenary 5/31 RASolute 302 본 발표 + 신규 oncology 3상, FDA AdCom 5월 일정
- **핀테크**: SEC 추가 가이드라인 (스테이블코인·custody), 한국 금융위 가상자산법 시행령
- **방산**: DoD FY27 예산안 의회 송부 (6월 예정), 한국 방사청 3축 체계 신규 계약
- **테크플랫폼**: EU AI Act 8/2 시행 D-100 가이드라인 후속, MS Build 발표, Google I/O 후속
- **소비재**: Target/HD/Lowe's/Costco 차주 어닝, 관세 가격 전가 본격화 모니터링
- **산업재**: TSMC AZ Phase 2 장비 입고 Q3 2026 진행 추적, Samsung Taylor 양산 일정
- **자동차**: Tesla Q2 인도량 가이던스, IRA 30D 9/30 종료 시나리오 후속, 미국 EV 시장 점유율

## 폴백/미수집

- 한국 산업통상자원부 K-Chips 보도자료 4월~5월 — 검색 실패, 다음 주 재시도
- bioRxiv/medRxiv 4월~5월 신규 preprint — 검색 결과 일반 정보만, 구체 trial 미특정
- NBER EEE·SSRN Energy Economics 4월 마지막 주~5월 1주 — 신규 게재 없음
- 일본 METI 4월~5월 보조금 보도 — 본 회차 미커버, 다음 회차 추가
- CNAS·RUSI 방산 학술 — 5월 신규 게재물 없음
- NeurIPS·ICML 페이퍼 트랙 — 6월 release 대기
- RASolute 302 IR 페이지 WebFetch timeout — ASCO Post / OncDaily 보조 출처로 검증
