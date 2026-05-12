---
sector: semiconductor
created: 2026-05-12
last_updated: 2026-05-12
status: active
related_industry_kb:
  - knowledge-base/industry/semiconductor.md
  - knowledge-base/industry/capex.md
l1_index_count: 6
l2_summary_count: 5
l3_deep_dive_count: 0
deep_dive_priority: 1
---

# Research Meta — Semiconductor (반도체)

> capex 19종 분석 시 가장 영향 큰 섹터. SK하이닉스 94.5 강력매수 (최고) + HBM 풀체인 + DC 인프라 + CHIPS 건설 모두 연결.

## 현재 thesis (research-curator weekly/monthly 갱신)

- **HBM4 양산 가시성 ↑ + 경쟁 격화**: ISSCC 2026에서 Samsung 36GB HBM4 12-Hi 3.3 TB/s·핀당 13Gb/s 양산급 시연 + SK hynix 16-Hi 48GB HBM4 11.7Gbps·2TB/s CES 첫 공개. NVIDIA Vera Rubin 타깃. SK하이닉스 단독 우위 시나리오에 Samsung이 직접 도전 — 단가 압력 vs 시장 확대 양면 변수. (L2: hbm4_samsung_isscc / hbm4_skhynix_isscc_ces)
- **시장 규모 thesis 보강**: McKinsey 4/2 — 2030년 $1.6T (CAGR 13%), 컴퓨팅·스토리지가 성장의 55%($460B). 메모리·로직 3강 (SK하이닉스·Samsung·Micron + NVIDIA·AMD·AVGO) 직접 베타. (L2: mckinsey_chip_boom_1_6t)
- **지정학 리스크 격상 (입법 단계 진입)**: 미 MATCH Act 입법 + 중국 산업망·공급망 안전 통합 법령(4월 시행) + EU 데이터센터 3배 확장 플랜(5월). 행정 명령에서 양국 법체계 격돌로 격상 — 정권 교체 후퇴 가능성 ↓. (L2: match_act_china_industrial_chain)
- **차세대 메모리 아키텍처 학술 신호**: arXiv:2511.12286 Sangam — Chiplet-DRAM-PIM + CXL이 LLM 추론에서 H100 대비 디코딩 10.3×·쿼리지연 4.22×. GPU 단일 의존 thesis에 학술 도전 (2028~2030 양산 가능성). (L2: sangam_chiplet_pim_cxl)

## Key Uncertainties (지속 추적)

본 섹션은 **분석 에이전트가 카드 만들 때 우선 참조** 하는 목록.

- HBM4 양산 시점 (2027 Q1 vs 2028 H1)
- 마이크론 HBM3E/HBM4 진입 시 마진 침식 폭 (NBER 메모리 사이클 연구 기준)
- CHIPS Act 보조금 진행률 + 정부 변동 시 후퇴 확률
- TSMC 미국 팹 양산 일정 (2026 vs 2027) + 한국·일본 보조금 경쟁
- AI 추론 ASIC (Trainium/MTIA/TPU) 점유율 vs NVIDIA GPU 점유율 변화
- China memory (CXMT, YMTC) 양산 캐파 진전

## 카탈리스트 캘린더 (분기 단위)

| 분기 | 이벤트 | 출처 유형 |
|---|---|---|
| 2026 Q2 | ISSCC paper digest 후속 양산 일정 | Conference |
| 2026 Q3 | Hot Chips 신규 ASIC 발표 | Conference |
| 2026 Q4 | IEDM device manufacturing 진전 | Conference |
| 2026 H2 | 미국 정부 CHIPS Act 2차 disbursement | Policy |
| 2027 Q1 | HBM4 양산 시작 (가정) | Filing |

## L1 인덱스 카운트 (현재)

- 학술: 1
- 씽크탱크: 2
- 컨퍼런스: 2
- 규제: 2

## L2 월간 요약 목록 (최신 → 과거)

- 2026-05 `hbm4_samsung_isscc_202605.md` — Samsung 36GB HBM4 12-Hi 3.3 TB/s (ISSCC 2026)
- 2026-05 `hbm4_skhynix_isscc_ces_202605.md` — SK hynix 48GB HBM4 16-Hi + SOCAMM2 + LPDDR6 (CES 2026 + ISSCC 2026)
- 2026-04 `mckinsey_chip_boom_1_6t_202604.md` — McKinsey 2030년 $1.6T (CAGR 13%)
- 2026-04 `match_act_china_industrial_chain_202604.md` — MATCH Act + 중국 산업망 법령
- 2026-04 `sangam_chiplet_pim_cxl_202604.md` — arXiv Sangam Chiplet-PIM-CXL LLM 추론

## L3 분기 Deep Dive 이력

- (예정) `reports/research/semiconductor_2026Q3.html` — 2026-07 첫 일요일 발행 목표

## 분석 에이전트 활용 가이드

분석 에이전트가 본 섹터 L2 요약 인용 시:
- HBM 관련 종목 (000660 SK하이닉스, 005930 삼성전자, MU 마이크론) → HBM4·마진 사이클 L2 우선
- 장비 종목 (ASML, AMAT, LRCX, KLAC) → CHIPS Act 진행 + 한국·일본 보조금 정책 L2
- ASIC/GPU 종목 (NVDA, AVGO, MRVL, AMD) → Hot Chips + arXiv cs.AR L2
- 메모리 컨트롤러 (KIOXIA, WDC) → arXiv cs.AR + 마진 사이클 L2

## 관련 KB 교차 참조

- `knowledge-base/industry/semiconductor.md` — 산업 thesis 베이스
- `knowledge-base/industry/capex.md` — CapEx 트래커 (하이퍼스케일러 $775~830B)
- `knowledge-base/macro/supply_chain.md` — 공급망 재편 + CHIPS Act
- `knowledge-base/macro/tech_breakthrough.md` — 기술 단계 판정
