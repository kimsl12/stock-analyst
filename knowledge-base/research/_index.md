---
title: Research KB — L1 주간 헤드라인 인덱스
description: 10개 섹터(반도체·에너지·매크로·바이오·핀테크·방산·테크플랫폼·소비재·산업재·자동차) × 4개 소스군(학술·씽크탱크·컨퍼런스/백서·규제) 주간 헤드라인 통합 인덱스
created: 2026-05-12
last_updated: 2026-06-27
update_cycle: weekly
status: active
total_headlines: 76
---

# Research KB — L1 주간 헤드라인 인덱스

> research-curator 가 매주 갱신. 본 인덱스는 **헤드라인 + 메타데이터** 만 보관. 본문 요약은 L2 (`{sector}/{topic}_{YYYYMM}.md`), 분기 종합은 L3 (`reports/research/{sector}_{YYYY}Q{N}.html`) 에서 다룬다.

## 운용 룰

| 항목        | 값                                                             |
| ----------- | -------------------------------------------------------------- |
| 갱신 주기   | 주간 (briefing-lead `/주간리포트` Phase 0-A 진입 시 자동 호출) |
| 보존 기간   | 12주 (지난 12주 헤드라인만 유지, 이전은 L2 승격 또는 폐기)     |
| 항목당 길이 | 1줄 (제목 + 1줄 요약 + 출처 + 발행일)                          |
| 인용 형식   | [`_citation_format.md`](_citation_format.md) 참조              |

## 인덱스 구조

각 섹터 섹션 안에 4개 소스군 (학술 / 씽크탱크 / 컨퍼런스/백서 / 규제) 하위로 헤드라인 누적.

---

## 🧠 Semiconductor (반도체)

### 학술

- 📄 [Preprint] arXiv:2511.12286 (2026-04) — "Sangam: Chiplet-Based DRAM-PIM Accelerator with CXL Integration for LLM Inferencing" → CXL-attached PIM-chiplet 메모리 모듈, H100 대비 디코딩 처리량·쿼리 지연 다대일 가속, GPU 대체·병행 사용 시나리오 제시
- 📄 [Preprint] arXiv:2511.06838 (2026-05) — "P3-LLM: An Integrated NPU-PIM Accelerator for LLM Inference Using Hybrid Numerical Formats" → HBM-PIM/Ecco/Pimba 대비 평균 3.4배 가속, 하이브리드 수치 포맷으로 LLM 추론 최적화
- 📄 [Preprint] arXiv:2604.08044 (2026-04-09) — "A Full-Stack Performance Evaluation Infrastructure for 3D-DRAM-based LLM Accelerators" (3D-DRAM 기반 LLM 가속기 풀스택 성능 평가 인프라) → 3D-DRAM 적층 메모리 아키텍처를 LLM 추론에 적용한 성능 모델링 프레임워크 제시, HBM 후속 메모리 폼팩터 평가 도구 ([source](https://arxiv.org/html/2604.08044v1))
- 📄 [Preprint] arXiv:2606.05511 (2026-06-03) — "RH+: Row-Hit-Optimized Scheduling for PIM-based LLM Inference" (PIM 기반 LLM 추론을 위한 행-히트 최적화 스케줄링) → HBM3 PIM에서 진짜 병목은 전력제약(nCCDAB)이 아니라 DRAM 행 사이클타임(nRC, nCCDAB의 10~11배)임을 규명. 메모리 접근 stride를 64→1 컬럼으로 바꿔 사이클당 32회 연속 행-히트 유도 → 8.25~11.88배 가속, 에너지 74.5~77.1% 절감, EDP 32.4~52.0배 개선 ([source](https://arxiv.org/html/2606.05511))
- 📄 [Preprint] arXiv:2604.26103v2 (2026-04-30) — "AMMA: A Multi-Chiplet Memory-Centric Architecture for Low-Latency 1M Context Attention Serving" (저지연 100만 토큰 컨텍스트 어텐션 서빙을 위한 멀티칩렛 메모리 중심 아키텍처) → GPU 연산 다이를 4×4 메시의 HBM-PNM(processing-near-memory) 큐브 16개로 대체, 36GB 3.3TB/s HBM4 사양 기반 로직다이(≤5nm) 통합. NVIDIA H100 대비 어텐션 지연 15.5배↓·에너지 6.9배↓, batch=1에서 12.0~16.3배·batch=32에서 13~20배 가속, 100만 토큰 디코드 어텐션 타겟 — GPU 비의존 자율 가속기. HBM4 진영(SK하이닉스·삼성)에 PNM 통합 수요 신호 ([source](https://arxiv.org/html/2604.26103))
- 📄 [Preprint] arXiv:2605.05639v1 (2026-05-07) — "TokenStack: A Heterogeneous HBM-PIM Architecture and Runtime for Efficient LLM Inference" (효율적 LLM 추론을 위한 이종 HBM-PIM 아키텍처·런타임) → HBM 스택을 기능별 수직 분리(용량층=표준 HBM이 weight·activation·cold KV / 연산층=PIM이 hot KV). HBM4의 CMOS 로직 base die가 스택-로컬 데이터이동·주소변환·인라인 양자화를 호스트 개입 없이 수행 + UCIe 다이투다이 인터커넥트. AttAcc(전용 PIM 베이스라인) 대비 토큰 처리량 기하평균 1.62배↑, 2배 지연 SLO 충족 서빙 캐파 1.70배↑, 토큰당 에너지 30~47% 절감 — HBM4 로직 base die가 이전 세대 불가능했던 자율 DMA 활성화하는 thesis 보강 ([source](https://arxiv.org/html/2605.05639))

### 씽크탱크

- 📄 [Think Tank] McKinsey (2026-04-02) — "Computing to Propel Chip Boom" → 글로벌 반도체 시장 2030년 $1.6T (2024년 $775B 대비 CAGR 13%), 컴퓨팅·스토리지가 성장의 55%($460B) 기여
- 📄 [Think Tank] CSIS (2026-04) — "MATCH Act + China Industrial Chain Security Regulations" → 미국 ASML·Nikon·Canon 장비 다자 통제 입법화 추진 + 중국 4월 산업망·공급망 안전 통합 법령 시행

### 컨퍼런스/백서

- 📄 [Conference] ISSCC 2026 (2026-02) — Samsung "36GB HBM4 12-Hi, 3.3 TB/s" → SF4 로직 base die + 1c DRAM 노드 + TSV 4배 증가, 핀당 13Gb/s, 1V 이하 동작 — Rubin 요건 충족
- 📄 [Conference] ISSCC 2026 (2026-02) — SK hynix "48Gbps GDDR7 24Gb + LPDDR6 14.4Gbps + 48GB HBM4 11.7Gbps" → AI 플랫폼 다층 메모리 라인업, SOCAMM2 폼팩터 동시 공개
- 📄 [Conference] VLSI Symposium 2026 어드밴스 프로그램 (2026-05, 본회의 6/14-18) — "Advancing the AI Frontier Through VLSI Innovation" → 3D 로직·3D 메모리(Flash·HBM) 기술 포커스 세션 2개 + "High-Performance CMOS for DRAM: AI 시대 Mobile/Graphics/Datacenter/HBM 활성화" 워크숍 + "Beyond 6F2 — Scaling Frontiers and Future DRAM" 단기강좌 — 차세대 DRAM 스케일링 로드맵 (📄 호놀룰루 Hilton Hawaiian Village, OnDemand 6/22~)
- 📄 [Conference] VLSI Symposium 2026 (2026-06, 본회의 6/14-18) — Intel·SoftBank "HB3DM (ZAM 기반 3D 메모리), Paper T17.5" → 9층 하이브리드 본딩 적층(base 로직 + DRAM 8층), TSV 약 13,700개. 대역폭 약 0.25 Tb/s/mm² → 10GB 모듈당 약 5.3 TB/s로 HBM4 스택당 약 2 TB/s 대비 2배 이상. 전력 HBM 대비 약 40% 절감(무선 방열). 다만 용량은 모듈당 약 10GB로 HBM4 48GB 대비 낮음. 프로토타입 FY2027·상용화 FY2029 목표 — SK hynix·삼성 HBM 진영 차세대 경쟁 신호 ([source](https://www.trendforce.com/news/2026/04/30/news-intel-softbank-reportedly-to-unveil-zam-based-hb3dm-in-june-bandwidth-more-than-double-hbm4/))
- 📄 [Industry] Samsung HBM4 누적 매출 $1B 돌파 (2026-06-23) — "2월 12일 HBM4 첫 양산 후 4개월 만에 누적 매출 $1B 돌파" → Vera Rubin용 6세대 HBM4 공급사 3사(삼성·SK하이닉스·마이크론) 중 삼성이 2/12 업계 첫 양산 시작, 6/23 기준 누적 매출 $1B 도달(약 4개월). HBM4 스택당 약 $500 추정가 기준 — 삼성 HBM 진영 복귀·매출 기여 본격화 신호 ([source](https://www.techtimes.com/articles/317539/20260602/nvidia-vera-rubin-enters-full-production-samsung-sk-hynix-micron-named-hbm4-suppliers.htm))
- 📄 [Industry] SK hynix HBM3E→HBM4 전환 일부 지연, DDR5로 재조정 (2026-06-24) — "일부 HBM3E 라인의 HBM4 전환을 늦추고 DDR5 일반 DRAM 생산으로 재배치" → 업계 소식통 인용. HBM4 점유율 50~55% 선두를 유지하면서도 단기 수익성(DDR5 가격 강세) 우선 — HBM4 램프 속도 조절. 16-Hi HBM4 신규 발주를 두고 삼성·마이크론과 NVIDIA 공급 계약 경쟁 중. HBM 공급 타이트닝·메모리 믹스 재편 신호 ([source](https://www.techtimes.com/articles/319016/20260624/sk-hynix-dethroned-samsung-after-26-years-now-choosing-ddr5-profits-over-hbm4-ramp.htm))
- 📄 [Conference] VLSI Symposium 2026 (2026-05-22, 본회의 6/14-18 발표) — "PSMC, Intel·SAIMEMORY HB3DM 9층 Via-in-One 합류 — 파운드리·제조 파트너 확정" → 사전 예고(T17.5) 대비 제조 진영 구체화: 설계·IP는 SAIMEMORY, 3D 적층은 Intel, 제조 지원은 PSMC + 日 Shinko Electric. 9층 구조 — 약 3µm 초박형 실리콘 기판, 산화물 트렌치 TSV 10×85µm²/20µm 피치(층당 약 13.7K TSV), C타입 대비 저항 40%↓ O타입 콘택트, 0.95~1.2V 동작. 대역폭밀도 약 0.25 Tb/s/mm²(171mm² 다이 10GB 모듈당 약 5.3 TB/s, HBM4 스택당 약 2 TB/s의 2배 초과), 데이터전송 전력 0.35 W/mm² 미만·0.7 pJ/bit 미만. 프로토타입 2027·양산 2029 — HBM4E 예비 사양에 도전하는 비메모리 진영 연합 구도 ([source](https://www.trendforce.com/news/2026/05/22/news-psmc-joins-intel-saimemory-to-demo-9-layer-fusion-bonded-via-in-one-architecture-for-high-bandwidth-3d-memory/))

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
- 📄 [White Paper] IEA Oil Market Report (2026-05) — "Iran War Upends Oil Outlook" → 이란 분쟁으로 걸프 산유 약 10.5 mb/d 오프라인, 2026년 글로벌 공급 -3.9 mb/d·수요 -420 kb/d로 1.78 mb/d 적자 반전(기존 surplus 전망 뒤집힘). Q2 정유가동 -4.5 mb/d, 재고 Q2 평균 -8.5 mb/d (5~6월 최대 인출), Brent 약 $106/bbl 고착. "호르무즈 해협 재개통이 가격·공급 압력 완화의 단일 최대 변수" — 중동發 인플레 상방 채널 ([source](https://oilprice.com/Latest-Energy-News/World-News/IEA-Revises-2026-Forecast-Oil-Deficit-Widens-as-Iran-War-Cuts-Production.html))
- 📄 [Think Tank] CRS Report R45281 (2026-06) — "Iran Conflict and the Strait of Hormuz: Impacts on Oil, Gas, and Other Commodities" (이란 분쟁과 호르무즈 해협: 석유·가스·기타 원자재 영향) → 미·이스라엘 작전(2026-02~) + 이란 보복으로 3/4부터 이란이 호르무즈 "봉쇄" 선언·통항 선박 공격. 2025년 세계 해상 석유교역의 약 25%가 호르무즈 통과했고 우회 경로는 제한적. 재고 인출은 5~6월 최대, Brent 약 $106/bbl 유지, IEA 회원국 전략비축 4억 배럴 방출 합의 — 해협 통항이 가격 정상화의 핵심 변수 ([source](https://www.congress.gov/crs-product/R45281))
- 📄 [White Paper] 유가·호르무즈 통항 정상화 진전 (2026-06-17) — "Brent $78.24/bbl, 3/3 이후 최저 — 美·이란 휴전 프레임워크 + 해협 재개통 기대로 2026년 고점 대비 약 20% 하락" → 분쟁 중 50% 이상 급등했던 유가가 전쟁 전(2/28) 대비 약 7% 수준으로 회귀. 6/19 제네바 서명 예정 프레임워크: 이란이 호르무즈 near-total 봉쇄 해제 ↔ 美 이란 항만 봉쇄 해제. 단 정상화엔 시차 — 통항 대기 선박 500척 초과, 기뢰 제거에 수주 이상 소요로 정상 해운 복원은 수주~수개월 전망. 직전 회차(CRS $106/bbl) 대비 중동發 인플레 상방 압력 급속 완화 신호 ([source](https://www.aljazeera.com/economy/2026/6/17/oil-prices-continue-slide-amid-hopes-for-peace-opening-of-strait-of-hormuz))

### 컨퍼런스/백서

- (이번 주 신규 없음 — IEA WEO 2026 발표 10월 예정, ANS·BP Outlook 부재)

### 규제

- 📄 [Policy] US NRC Part 53 발효 (2026-04-29) — "Risk-informed Advanced Reactor Licensing" → 3월 26일 의결, 4월 29일 발효. 제조지 연료 주입·운영지 운반 허용·고밀도 인구 지역 입지 가능
- 📄 [Policy] US DOE 의회 증언 (2026-04 중순) — "첫 5~10기 신규 원전 DOE 대출 거의 확정" → 에너지 장관 의회 증언, LPO 자금 SMR/AP1000 일괄 지원 계획 명시
- 📄 [Policy] US NRC TRISO-X 연료 시설 (2026-02-16, 확정) — "X-energy TRISO-X TX-1 Category II 라이선스 발급" → 첫 미국 Category II HALEU 연료 제조 시설 인가, 40년 라이선스, TX-1 연 5톤U / 70만 TRISO 페블, Oak Ridge 입지 — 예정 일정(5월) 대비 3개월 앞당겨 2월 16일 발급 ([source](https://www.world-nuclear-news.org/articles/us-regulator-issues-licence-for-triso-x-fuel-facility)) [KEEP — SMR thesis 핵심]
- 📄 [Policy] US NRC 마이크로리액터 프레임워크 제안 (2026-04-24, 의견수렴 6/15 마감) — "High-Volume Microreactor Deployment 라이선스 규칙" → 마이크로리액터·유사 위험 프로파일 원자로의 신속·대량 배치를 겨냥한 첫 포괄적 리스크인폼·성능기반 라이선스 프레임워크. Part 53 발효(4/29)에 이은 후속 입법, 5/1 Federal Register 공고·6/15 공개 의견 마감 — SMR/마이크로리액터 배치 속도 제고 ([source](https://www.orrick.com/en/Insights/2026/05/NRC-Proposes-New-Framework-to-Enable-High-Volume-Microreactor-Deployment))
- 📄 [Policy] US DOE Gen III+ SMR 배치 어워드 (2026-05-15) — "8개사 $94M+ 비용분담 펀딩 (Tier 2)" → Gen III+ 경수로 SMR 근거리 배치 가속 위한 라이선스·공급망·부지준비 갭 해소. 부지준비 2사: Constellation $17.3M(NY ESP)·Nebraska Public Power $27.9M(NE ESP). 공급망 6사: BWXT $21.4M(원자로 압력용기 조립), Framatome $8.8M(연료 제조 확장), GNF Americas $3M(연료봉 라인), Scot Forge $12.3M 등. 5/15 발표 $800M TVA·Holtec 1차 배치 펀딩에 이은 후속 — 미 SMR 공급망·부지 본격 가동 ([source](https://www.ans.org/news/2026-05-15/article-8035/doe-selects-companies-for-94m-in-light-water-smr-deployment-awards/))
- 📄 [Policy] US DOE Office of Energy Dominance Financing — AP1000 대형원전 $17.5B 조건부 약정 (2026-06-23) — "Westinghouse AP1000 최대 10기 long-lead 장비 조달에 $17.5B 융자 약정 (American Supply Chain Loans)" → 최대 5건 융자(건당 원자로 2기 지원)로 2030년까지 10기 착공 목표. 원자로 압력용기 등 장납기 핵심 부품을 다수 프로젝트 일괄 구매 → 공급망 효율화·부품원가 절감·배치 일정 최대 3년 단축. Westinghouse 소유: Brookfield+기관 파트너 51%·Cameco 49% (8-K 공시). 본 약정은 SMR이 아닌 대형 경수로 본격 재가동 — capex 원자력 thesis(SMR→대형 동시 확장) 강화. 단 기술·법무·환경·재무 조건 충족 전까지 확정 자금 미집행 ([source](https://www.power-eng.com/nuclear/doe-commits-17-5-billion-to-finance-long-lead-equipment-for-u-s-fleet-of-westinghouse-ap1000-reactors/))

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
- 📄 [Policy] FOMC 의사록 (2026-05-20 공개) — "4월 28-29일 회의 의사록" → 8-4 동결 표결 (Miran 25bp 인하 선호 / Hammack·Kashkari·Logan 동결엔 동의하나 성명문 완화 바이어스 삽입 반대). 회의 시점 인플레 "상승·고착, 에너지가격 급등 주도", 노동시장 안정·실질 GDP 확장 지속 평가. 4월은 SEP 비공개 회의 (dot plot 없음), 차기 6/16-17 회의서 갱신 ([source](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260520a.htm))
- 📄 [Policy] ECB 통화정책결정 (2026-04-30) — "기준금리 동결 (MRO 2.15% / DFR 2.0%)" → 4월 유로존 인플레 3%, 중동 전쟁 에너지가격 상방, 만장일치 동결 + 인상 옵션 토론 — Lagarde 데이터 의존 메시지
- 📄 [Policy] 한국은행 MPC (2026-05-28) — "기준금리 2.50% 동결 (8회 연속), 신현송 총재 첫 회의 매파 시그널" → 류상대·장용성 위원 즉시 인상 소수의견, dot plot 7인 중 19/21점이 6개월 후 인상 전망 (동결은 2점). 2026년 CPI 전망 2.2%→2.7% 상향 (이란 분쟁發 유가 전가), GDP 전망 2.0%→2.6% 상향. 총재 "성장·물가·환율·부동산 모두 같은 방향" 연내 인상 사실상 확인 ([source](https://www.kedglobal.com/central-bank/newsView/ked202605280001))
- 📄 [Policy] FOMC 6/16-17 회의 프리뷰 (2026-06) — "동결 유력 + 완화→중립/긴축 바이어스 전환 가능성" → CME FedWatch 동결 확률 98.3%. 5월 헤드라인 CPI 4.2% YoY·코어 2.9%(둘 다 2% 목표 상회), 5월 신규고용 +172K(3개월 평균 188K)·실업률 4.3%로 견조. Desk 서베이 중앙값은 향후 1년 25bp 인하 2회 유지하되 시점을 26년 3~4분기·27년 1분기로 후퇴. 이란 분쟁發 인플레 지속 시 인상 가능성 다수 의견 — SEP/dot plot 본 회의서 갱신 (4월은 비공개 회의로 미발표) ([source](https://www.indexbox.io/blog/fed-meeting-preview-june-1617-fomc-decision-and-potential-bias-shift/))
- 📄 [Policy] FOMC Statement + SEP (2026-06-17) — "정책금리 3.50~3.75% 동결(만장 12-0), dot plot 인하→인상 반전 + Warsh 첫 주재" → 5/22 취임한 Kevin Warsh 의장 첫 회의서 만장일치 동결 — 4월 8-4 분열에서 급반전. SEP 2026년 말 중앙값 3.8%로 3월 3.4% 대비 상향(인하 함의→인상 함의로 전환). 18인 dot 분포: 9인 인상·8인 현 중앙값(3.625%)·1인 인하, 범위 3.4~4.4%. 인플레 위험 평가 17인 상방·1인 균형·0인 하방 — 중동發 에너지 인플레 고착 반영, 2026년 사실상 긴축 바이어스 진입 ([source](https://www.stocktitan.net/articles/fed-rate-decision-june-17-2026))
- 📄 [Policy] FOMC 성명문 구조 개편 + Fed 운영 개혁 태스크포스 (2026-06-17) — "Warsh 의장 성명문 약 300단어→약 130단어 축약, forward guidance 폐기" → 6/17 첫 주재 회의서 성명문을 대폭 단축(이전 300단어 초과 → 약 130단어). Warsh "forward guidance는 현 정책 국면에 부적합" — 일부 구(舊)표현 삭제하고 더 짧고 단순하게. 동시에 Fed 주요 운영(operations) 전반을 손볼 태스크포스 신설 발표 — Powell 압박 정쟁(독립성 논란) 끝 취임한 Warsh의 커뮤니케이션·거버넌스 구조 개혁 착수. 점도표 인상 반전(6/17 SEP, 위 항목)과 함께 Fed 운영 체제 전환 신호 ([source](https://www.cnbc.com/2026/06/17/fed-meeting-today-live-updates.html))
- 📄 [Policy] BOJ 통화정책결정 (2026-06-19) — "정책금리 +25bp 1.00% 인상 (7-1 표결), 1995년 9월 이후 최고" → 0.75%→1.00% 인상(보완당좌예금 1.0%·기본대출 1.25%). Asada Toichiro 위원만 반대(가격 상방보다 생산·고용 하방 위험 우려). 4월 6-3 분열에서 합의 강화. 기조 인플레가 에너지가격 상승으로 2% 목표 상회 가속 가능 평가, 인상 후에도 완화적 금융여건 유지. 가이던스는 중립·데이터 의존 — USD/JPY 발표 후 약 160.29(엔 일시 강세 후 되돌림). 추가 인상 지속 시사 + 중동 분쟁 영향 주시 ([source](https://www.ebc.com/forex/boj-at-1-percent-yen-usd-jpy-rate-hike))

---

## 🧬 Biotech (바이오)

### 학술

- 📄 [Journal] NEJM (2026) — "Orforglipron Phase 3 ATTAIN-1 (oral GLP-1)" → 경구 GLP-1 수용체 작용제, 비만 환자 체중감소 placebo 대비 통계적 유의, Lilly Foundayo 4/1 FDA 승인 데이터 기반
- 📄 [Journal] NEJM SURMOUNT-5 (2026) — "Tirzepatide vs Semaglutide Head-to-Head" → 72주 추적, 비만/과체중 환자에서 tirzepatide(Zepbound)가 semaglutide(Wegovy)에 우월한 체중감소 — LLY 마진·점유율 thesis 보강
- 📄 [Journal] NEJM (2026, NEJMoa2605555) — "Daraxonrasib or Chemotherapy in Previously Treated Metastatic Pancreatic Cancer" (전이성 췌장암 2차 치료 다라소라십 vs 항암화학) → RASolute 302 3상 동시 게재. RAS G12 변이 mPDAC에서 mOS 13.2 vs 6.7개월(HR 0.40, P<.0001, 사망위험 60%↓), 추적중앙값 8.5개월에 모든 1차·핵심 2차 종료점 충족·중대 이상반응은 더 적음 — RAS(ON) 다중선택 억제제 2차 표준요법 후보 ([source](https://www.nejm.org/doi/full/10.1056/NEJMoa2605555))

### 씽크탱크

- (이번 주 신규 없음 — McKinsey Pharma·BCG Health Care 4월 게재물 부재)

### 컨퍼런스/백서

- 📄 [Conference] ASCO 2026 (2026-05-31, plenary 발표 완료) — "RASolute 302 / Daraxonrasib in PDAC plenary" → 5/31 Dr. Wolpin(Dana-Farber) plenary 발표, standing ovation. mOS 13.2 vs 6.7개월, HR 0.40 (P<.0001), 사망위험 60% 감소 — KRAS G12 변이 PDAC 첫 명확한 OS 우월성. NEJM 동시 게재(NEJMoa2605555). Revolution Medicines 가치 재평가 모멘텀 ([source](https://ascopost.com/news/june-2026/daraxonrasib-nearly-doubles-survival-in-previously-treated-metastatic-pancreatic-cancer/)) [KEEP — Bio thesis 핵심]
- 📄 [Conference] ASCO 2026 (2026-06-02) — AstraZeneca "SERENA-6 camizestrant ctDNA 클리어런스 데이터" → ESR1 변이 발생 ER+/HER2- 진행성 유방암 1차 치료 중 조기 전환. 카미제스트란트+CDK4/6i군 8주차 총 ctDNA 중앙값 99%↓·51% 완전 클리어런스 vs AI군 64%↑·1.9% 클리어런스. mPFS 16.8 vs 9.2개월, 진행/사망위험 55%↓. FDA가 4월 ODAC 다수표결 실패 후 추가 분석 검토 위해 결정시한 연장 — ctDNA 데이터로 재설득 시도 ([source](https://www.precisionmedicineonline.com/precision-oncology/astrazeneca-hoping-sway-fda-camizestrant-ctdna-clearance-data-serena-6))
- 📄 [Conference] ASCO 2026 후속 업데이트 (2026-06) — AstraZeneca "SERENA-6 camizestrant 23.5개월 추적 PFS 업데이트" → 중앙추적 23.5개월에 카미제스트란트+CDK4/6i군 mPFS 16.8개월 vs AI+CDK4/6i군 9.2개월 유지(추적 연장에도 PFS 우월 견고). 단 FDA는 PFS2를 단독 유효성 종료점으로 불수용 통보 — 추가 데이터 검토 위해 PDUFA 연장(아래 규제 항목) ([source](https://www.onclive.com/view/serena-6-meets-pfs2-end-point-with-early-switch-to-camizestrant-in-er-her2-negative-esr1-mutated-advanced-breast-cancer))
- 📄 [Conference] ADA 86th Scientific Sessions (2026-06-05~08, New Orleans) — Structure Therapeutics "aleniglipron ACCESS II Phase 2b 데이터" → 경구 소분자 GLP-1 수용체 작용제. 120mg 용량서 36주차 placebo 대비 11.3% 체중감소(placebo-adjusted). Phase 3는 Q3 2026 개시 예정. Lilly orforglipron(기승인)·Novo CagriSema에 도전하는 차세대 경구 GLP-1 경쟁자 — 경구 비만치료제 시장 확장 thesis 보강 ([source](https://www.biospace.com/lilly-novo-face-off-at-ada-2026-as-others-seek-to-compete-in-obesity))
- 📄 [Conference] ADA 86th Scientific Sessions (2026-06-05~08, New Orleans) — Novo Nordisk "CagriSema(카그릴린타이드+세마글루타이드) REIMAGINE-1/2/3 데이터" → 아밀린 유사체+GLP-1 복합. T2D 환자서 혈당·체중 모두 세마글루타이드 단독 대비 우월하나, 체중감소는 tirzepatide(LLY) 대비 열위. retatrutide(triple agonist) 후기 데이터·survodutide·경구 elecoglipron 등 차세대 라인업 동반 발표 — 비만·당뇨 차세대 경쟁 구도 격화 ([source](https://www.medscape.com/viewarticle/latest-glp-1-based-therapy-be-featured-ada-2026a1000i3q))

### 규제

- 📄 [Policy] FDA (2026-04-01) — "Foundayo (orforglipron) 비만 적응증 승인" → 경구 GLP-1, Lilly 처방 채널·복약순응도 확장 → GLP-1 시장 구조 재편
- 📄 [Policy] FDA (2026-04-22) — "Tzield (teplizumab-mzwv) 1세 이상 적응증 확대" → 1형 당뇨 3기 발병 지연, 기존 8세→1세 sBLA 승인
- 📄 [Policy] FDA (2026-05-01) — "Veppanu (vepdegestrant) ESR1m ER+/HER2- 진행성 유방암 승인" → 경구 PROTAC 분해제 종양학 첫 승인 — Arvinas/Pfizer 파트너십
- 📄 [Policy] CMS IRA Negotiation 3차 (2026-04-20) — "Selected Drug List + Maximum Fair Prices 공개" → 15개 약물 (Part B/D), 협상 2026 진행, 가격 효력 2028-01-01. 4월 환자·임상 공청회 진행
- 📄 [Policy] FDA / AstraZeneca camizestrant PDUFA 연장 (2026-06) — "SERENA-6 ODAC 3-6 반대 + PFS2 종료점 불수용 → 결정시한 연장" → ODAC가 1차 치료 ER+/HER2- ESR1 변이 진행성 유방암 camizestrant+CDK4/6i 베네핏-리스크에 3-6 반대 표결. FDA는 PFS2를 유효성 근거 종료점으로 불수용 통보하고 추가 데이터 검토 위해 PDUFA 결정시한 연장 — 단 EU CHMP는 동 적응증 1차 치료 승인 권고(지역 규제 격차). Arvinas/Pfizer Veppanu(vepdegestrant) 등 SERD/PROTAC 경구 분해제 경쟁 구도에 영향 ([source](https://www.fiercebiotech.com/biotech/fda-delays-ruling-astrazenecas-breast-cancer-drug-after-negative-adcomm-vote))

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
- 📄 [Policy] GENIUS Act 시행 규칙 제정 진행 (2026-04~06, 의견수렴 6/9 마감) — "Treasury·OCC·FDIC·FinCEN/OFAC 시행 NPRM 일제 공개" → 7월 2026 최종규칙 시한 앞두고 4월 중 재무부·FDIC·FinCEN 각 시행 제안규칙 발표, 의견 6/9 마감. OCC는 은행·연방저축기관·외국 발행자·비은행 적격발행자 대상 결제 스테이블코인 발행 규칙, FinCEN/OFAC는 AML·제재 컴플라이언스 공동 규칙. 법 효력은 27/1/18 또는 최종규칙 후 120일 중 빠른 날 — 발행자 자격·준비금 규칙 윤곽 확정 단계 ([source](https://www.bhfs.com/insight/recent-updates-in-digital-assets-policy/))
- 📄 [Policy] US Treasury / FinCEN·OFAC PPSI 컴플라이언스 프레임워크 (2026-06, ABA 분석) — "결제 스테이블코인 발행자(PPSI)를 BSA 금융기관으로 편입" → 6/9 의견마감(4/8 공개) 후 ABA Business Law Today 분석. PPSI를 은행비밀법(BSA)상 금융기관으로 취급 — AML 프로그램 수립·의심거래 보고(SAR)·기록보존·정보공유 의무. 기존 송금업자(money transmitter) 규제와 차별화된 별도 컴플라이언스 트랙. 7/18 최종규칙 시한 앞두고 발행자 컴플라이언스 비용·진입요건 구체화 — Circle·Tether 등 발행자 운영부담 가중 채널 ([source](https://www.americanbar.org/groups/business_law/resources/business-law-today/2026-june/treasurys-proposed-stablecoin-compliance-framework/))
- 📄 [Policy] GENIUS Act 최종규칙 제정 막바지 — 6개 기관 7/18 시한 동시 입법 (2026-06-26 트래커) — "전 의견수렴 6/9 종료, 6개 기관이 5주 내 6개 제안 프레임워크 조율·최종규칙 발표 임박" → OCC·FDIC·NCUA·Treasury·FinCEN·OFAC 6개 기관이 GENIUS Act 제정 1주년(7/18)에 맞춰 최종규칙 동시 발표 압박. OCC 12 CFR Part 15(3월 제안), FDIC·Treasury(4월), FinCEN·OFAC AML NPRM(4월). 최종규칙 확정 후 발행자는 약 120일 유예 → 2026년 말 효력 발생. 발행자 자격·준비금·AML 요건 확정 단계 — 스테이블코인 발행 제도권 진입 본격화 ([source](https://www.chapman.com/publication-genius-act-rulemaking-tracker))

---

## 🛡️ Defense (방산·항공)

### 학술

- (이번 주 신규 없음 — RUSI·CNAS 5월 학술 게재물 부재, 다음 회차 SSRN 정치경제 분야 재시도)

### 씽크탱크

- 📄 [Think Tank] CSIS (2026-05-08) — "Deepening Strategic Alignment: Priorities for the U.S.-Japan Alliance" (Johnstone & Rubinstein) → 일본 5개년 방위비 +60%·1년차 +25% 단계 진입, 장사거리 정밀타격·능동 사이버·우주 자산 투자 확대 — 한미일 통합 억제·역할분담 재정립 ([source](https://www.csis.org/analysis/deepening-strategic-alignment-priorities-us-japan-alliance))
- 📄 [Think Tank] SIPRI Fact Sheet (2026-04) — "2025 World Military Expenditure" → 글로벌 군사비 사상 최고 갱신, 한국 2025년 $47.8B (+2.6%) — 3축 체계 (미사일방어·선제타격·보복능력) 지속 투자 ([source](https://www.sipri.org/sites/default/files/2026-04/2604_milex_2025.pdf))
- 📄 [Think Tank] CSIS (2026-04) — "Unpacking the $1.5 Trillion FY 2027 Defense Budget Topline" → 사상 최대 $1.5T 국방예산 요청(역대 최대). 재량 $1.15T + 조정(reconciliation) $350B 구조. Golden Dome 미사일방어 약 $17.5B 중 거의 전액 의무·조정예산(base는 약 $400M) — 우주기반 센서·요격체·층상 본토방어. 조정 절차 의존도가 높아 의회 통과 불확실성 동반 ([source](https://www.csis.org/analysis/unpacking-15-trillion-fy-2027-defense-budget-topline))

### 컨퍼런스/백서

- (이번 주 신규 없음 — RIAT·AUSA·DSEI 일정 외)

### 규제

- (이번 주 신규 없음 — FY27 예산안은 4월 의회 송부 완료, 세부 appropriations·reconciliation 심사 진행 중. CSIS 토플라인 분석은 씽크탱크 항목 참조)

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
- 📄 [Filing] Target Q1 FY26 Earnings (2026-05-20) — "EPS $1.71 (GAAP·조정 동일) / 매출 +6.7% / 동일점매출 +5.6%" → 6개 핵심 머천다이징 카테고리 전부 성장, 디지털 +8.9% (당일배송 +27% 초과). 연간 가이던스 상향 (매출 +4% 내외, EPS $7.50~8.50 상단 근접) — 단 가이던스는 관세 환급분 제외. Walmart 대비 동일점 성장 반전 ([source](https://corporate.target.com/news-features/article/2026/05/q1-2026-earnings))
- 📄 [Filing] Home Depot Q1 FY26 Earnings (2026-05-20) — "순매출 $41.8B (+4.8% YoY)" → 핵심 고객 회복력 유지, 연간 가이던스 재확인·컨센서스 상회. 관세 환급 신청 (연료비 상승 상쇄). 관세發 특정 카테고리 "완만한 가격 인상" 예상하나 전면 인상은 아님 ([source](https://www.fool.com/earnings/call-transcripts/2026/05/19/home-depot-hd-q1-2026-earnings-transcript/))
- 📄 [Filing] Lowe's Q1 FY26 Earnings (2026-05-20) — "EPS·매출 컨센서스 상회, 연간 가이던스 재확인" → 봄 시즌 강한 실행 + 온라인·가전·홈서비스·프로 부문 성장 견인. CEO Ellison "challenging housing macro" 인정 + 관세 영향 시인 — HD와 동일 기조 ([source](https://www.cnbc.com/2026/05/20/lowes-low-q1-2026-earnings.html))
- 📄 [Filing] Costco Q3 FY26 Earnings (2026-05-28, 분기말 5/10) — "순매출 +11.6% $69.15B / EPS $4.93(전년 $4.28) / 조정 동일점 +9.8%(미국 +6.8%)" → 디지털 매출 +21% 초과, 멤버십 수입 $1.37B(+10.7%). 인플레·관세 환경에서도 두 자릿수 성장·견조한 트래픽 — 디스카운트/벌크 채널의 관세 전가 방어력 입증. 단 밸류에이션 부담은 별개 이슈 ([source](https://www.stocktitan.net/news/COST/costco-wholesale-corporation-reports-third-quarter-and-year-to-date-ya9rfbnhnzg9.html))

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

## 차주 갱신 예상 항목 (2026-06-27 트래킹)

- **반도체**: SK hynix HBM3E→HBM4 전환 지연·DDR5 재배치 후속(NVIDIA 16-Hi HBM4 발주 향방), 삼성 HBM4 매출 램프 속도, VLSI 2026 OnDemand(6/22~) 삼성/SK 차세대 메모리 세션 실측, 메모리 PIM/PNM(TokenStack 계열) 후속 preprint, BIS/MATCH Act 의회 진전
- **에너지**: 호르무즈 통항 정상화 진척(기뢰 제거·대기선박 500척 해소)과 Brent 동향, IEA 7월 OMR, DOE AP1000 $17.5B 약정 후속(개별 5건 융자 confirm·정의적 자금 집행 조건), NRC 마이크로리액터 규칙 6/15 의견마감 후 검토, DOE Gen III+ SMR Tier 3
- **매크로**: FOMC 6/17 후속 — Warsh 성명 개편·운영 개혁 태스크포스 세부, FOMC 의사록(7월 공개), BOJ 1.0% 인상 후 엔/JGB 반응·추가 인상 경로, 한국은행 7월 회의 연내 인상 시점, ECB 6월 회의, NBER SI 2026 7월 트랙
- **바이오**: ADA 후속 GLP-1 readout(retatrutide·CagriSema REIMAGINE 상세), camizestrant 연장된 PDUFA 추가 데이터·재심, orforglipron/CagriSema FDA 리뷰 진전, FDA 7월 PDUFA(ONS-5010 7/29 등)·AdCom
- **핀테크**: GENIUS Act 7/18 최종규칙 발표 임박 — 6개 기관 최종규칙·발행자 자격·준비금 확정, 한국 금융위 가상자산법 2단계 시행령
- **방산**: FY27 appropriations·reconciliation 의회 심사 진전 (Golden Dome $17.5B 배분), 한국 방사청 3축 체계 신규 계약
- **테크플랫폼**: EU AI Act 8/2 Annex III 고위험 시행 D-36 가이드라인, NeurIPS/ICML 7월 트랙, MS Build 후속
- **소비재**: 6~7월 리테일 어닝, 관세 가격 전가 진행, 여름 소비 동향
- **산업재**: TSMC AZ Phase 2 장비 입고 Q3 2026 진행 추적, Samsung Taylor 양산 일정
- **자동차**: Tesla Q2 인도량·Cybercab 양산·Austin 로보택시 확대, EV 충전 크레딧 6/30 종료 후속

## 폴백/미수집 (2026-06-27 회차)

- 매크로 Alan Greenspan 별세(2026-06-22, Fed Board 공식 추모 공고) — 1차 정책/연구 자료 아닌 obituary 성격으로 인덱스 등재 보류(시장 영향 채널 아님). 다음 회차 추모·정책 회고 분석 게재 시 재검토
- VLSI Symposium 본회의(6/14-18) 삼성/SK 개별 HBM4 논문 실측 스펙 — OnDemand(6/22~) 상세 보도 미특정, 삼성 $1B 매출·SK 전환지연 산업 동향으로 대체 수집, 다음 회차 재시도
- 에너지 학술(NBER EEE·SSRN)·IEA 6월 OMR 본문(iea.org 403) — Al Jazeera/CRS 등 2차 보도로 Brent·Hormuz 수치 확정 수집, IEA 직접 본문은 다음 회차 재시도
- 테크플랫폼 6월 신규 학술/규제 — NeurIPS·ICML 7월 트랙, EU AI Act 6월 신규 가이드라인 미특정, 5월 헤드라인 유지
- 방산 6월 신규 — CNAS·RUSI 학술 게재물 부재, FY27 reconciliation 심사 진행(CSIS 토플라인 유지), 다음 회차 재시도
- 소비재·산업재·자동차 6월 신규 1차 자료 — 리테일 어닝 시즌 종료·분기말 대기로 신규 부재, 5월 어닝/IRA 헤드라인 유지
- bioRxiv/medRxiv 6월 신규 preprint — 구체 trial 미특정, ADA/ASCO 컨퍼런스 데이터로 대체, 다음 회차 재시도
