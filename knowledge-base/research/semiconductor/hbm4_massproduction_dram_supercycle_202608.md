---
title: "HBM4 양산 개시(2026-02) + 서버 DRAM +60~70% — 메모리 슈퍼사이클·장기계약 거부·설비 대증설"
sector: semiconductor
topic: hbm4_massproduction_dram_supercycle
date_published: 2026-01
date_collected: 2026-08-01
last_updated: 2026-08-01
source_type: White Paper
source: "Introl(HBM4 슈퍼사이클 분석) + 업계 종합"
url: https://introl.com/blog/south-korea-hbm4-stargate-memory-supercycle-2026
citation: "📄 [White Paper] Introl (2026-01) — HBM4 Stargate 메모리 슈퍼사이클"
key_finding: "Samsung·SK Hynix가 2026-02 HBM4 동시 양산 개시. HBM4는 인터페이스 폭 2048비트(HBM3E 1024비트의 2배)·대역폭 2+TB/s(~1.7배)·스택당 최대 64GB·전력효율 20% 개선. 서버 DRAM 가격은 Q1 2026 전분기 대비 +60~70%, 양사는 2~3년 장기계약을 거부하고 분기 계약으로 단계적 인상 관철. OpenAI Stargate만으로 월 90만 DRAM 웨이퍼(글로벌 40%)·2029년까지 ~$720억 증분 수요 추정(현 HBM 캐파 월 ~40만 웨이퍼). SK Hynix 용인 클러스터 투자를 128조→600조원($410B)으로 확대, 첫 팹 2027 가동. NVIDIA는 3사 모두에서 HBM4 샘플 확보."
---

# HBM4 양산 개시 + DRAM 슈퍼사이클 (Introl·업계, 2026)

> 성숙 semiconductor 섹터 L2 보강분(2026-08). 기존 `hbm4_samsung_isscc`·`hbm4_skhynix_isscc`·`vlsi_symposium_3d_memory` 는 기술·수율 관점 — 본 요약은 **양산 개시·가격 사이클·수급·capex** 라는 메모리 슈퍼사이클의 시장 국면을 추가한다.

## 핵심 발견 (5건)

- **2026-02 HBM4 동시 양산**: Samsung·SK Hynix 가 **2026년 2월 HBM4 양산을 동시 개시**. Samsung 은 연말까지 월 25만 웨이퍼 목표, SK Hynix 는 이천 M16·청주 M15X 팹 가동 (📄 Introl, 2026-01).
- **HBM4 스펙 도약**: 인터페이스 폭 **2048비트**(HBM3E 1024비트의 2배), 대역폭 **2+TB/s**(~1.7배), 스택당 최대 **64GB**, 전력효율 HBM3E 대비 **20% 개선**. (JEDEC HBM4 표준 계열 — 인터페이스 2배 폭이 핵심.)
- **서버 DRAM +60~70% + 장기계약 거부**: Samsung·SK Hynix 가 서버 DRAM 가격을 **Q1 2026 전분기 대비 +60~70%** 인상. 원문 인용 _"Both companies have rejected long-term agreements of two to three years, instead requiring quarterly contracts that allow stepwise price increases."_ — 공급사 우위의 프라이싱 파워를 방증.
- **Stargate發 초과수요**: OpenAI **Stargate** 만으로 월 **90만 DRAM 웨이퍼(글로벌 생산의 40%)** 소모 가능, **2029년까지 ~$720억 증분 수요** 추정 — 현 HBM 캐파 월 ~40만 웨이퍼를 크게 상회. 구조적 공급 부족 서사.
- **대규모 capex 증설**: SK Hynix 용인 클러스터 투자를 **128조 → 600조원($410B)**로 확대(첫 팹 2027 가동), Samsung P5 팹 2028 가동. NVIDIA 는 3사(SK Hynix·Samsung·Micron) 모두에서 HBM4 샘플 확보, Samsung 물량 다수는 Rubin 시스템·일부 Google 향.

## 데이터·근거

| 항목           | 데이터                                  | 출처                              |
| -------------- | --------------------------------------- | --------------------------------- |
| HBM4 양산 개시 | 2026-02 (Samsung·SK Hynix 동시)         | 📄 [White Paper] Introl (2026-01) |
| 인터페이스 폭  | 2048비트 (HBM3E 2배)                    | 📄 [White Paper] Introl (2026-01) |
| 대역폭 / 용량  | 2+TB/s(~1.7배) / 64GB per stack         | 📄 [White Paper] Introl (2026-01) |
| 서버 DRAM 가격 | Q1 2026 +60~70% (분기계약)              | 📄 [White Paper] Introl (2026-01) |
| Stargate 수요  | 월 90만 웨이퍼(글로벌 40%)·~$720억 증분 | 📄 [White Paper] Introl (2026-01) |
| 현 HBM 캐파    | 월 ~40만 웨이퍼                         | 📄 [White Paper] Introl (2026-01) |
| SK Hynix capex | 용인 128조→600조원($410B), 첫 팹 2027   | 📄 [White Paper] Introl (2026-01) |

## 분석가 활용 가이드 — Bull / Bear / Contrarian

- **Bull case (메모리 슈퍼사이클·공급사 프라이싱 파워)**: DRAM +60~70%·장기계약 거부·분기 인상은 공급사 우위 국면 — SK Hynix·Samsung·Micron 마진 급개선. HBM4 2048비트·2+TB/s 는 AI 가속기(NVIDIA Rubin) 필수 부품으로 lock-in. Stargate發 초과수요는 다년 캐파 부족 서사. 소부장·후공정(TSV·하이브리드 본딩) 낙수효과.
- **Bear case (사이클 정점·대증설 반작용)**: +60~~70% 인상·600조원 capex 급증은 메모리 사이클 특유의 **과증설→공급과잉 반전** 씨앗. 첫 팹 2027·P5 2028 가동 시 공급 급증 → 2027~~2028 가격 whipsaw 리스크(에너지/전력기기 lead-time 병목과 유사 패턴). 하이퍼스케일러 capex 둔화 시 수요 급랭.
- **Contrarian (Stargate 수요 가정의 취약성)**: 월 90만 웨이퍼(글로벌 40%)·$720억 증분은 단일 프로젝트(Stargate) 실현 가정에 크게 의존 — 자금조달·전력(DC 전력난·전력기기 병목)·부지 제약이 겹치면 수요 실현이 지연. "분기계약·장기계약 거부"는 공급사조차 사이클 지속성에 확신이 없다는 방증일 수 있음(장기 물량 lock-in 회피).

## 한계

- 본 요약은 Introl(업계 분석 블로그) fetch 기반 — 수치(월 25만 웨이퍼·$720억·600조원)는 분석 추정치, 기업 공시·JEDEC 원문과 교차 확인 권장.
- HBM 시장규모($38B→$58B) 등 일부 수치는 WebSearch 종합(딥페치 미수행) → 정량 인용 시 원출처 재확인.
- NVIDIA 공급사별 점유율은 소스에서 구체 비율 미제공.
- 무력화 조건: AI capex 둔화·하이퍼스케일러 발주 축소 시 DRAM 가격 급락. 대증설 완공(2027~2028) 시 공급과잉 반전.

## 인용 (Citation)

📄 [White Paper] Introl (2026-01) — HBM4 2026-02 양산 개시(2048비트·2+TB/s·64GB) + 서버 DRAM +60~70%·장기계약 거부 + Stargate 월 90만 웨이퍼·$720억 증분 + SK Hynix 용인 600조원 capex → 메모리 슈퍼사이클·공급사 프라이싱 파워 vs 대증설 공급과잉 반작용

URL: https://introl.com/blog/south-korea-hbm4-stargate-memory-supercycle-2026 (Introl, 2026-01)
보조(검색 종합, 딥페치 미수행): HBM 시장 $38B(2025)→$58B(2026); JEDEC JESD270-4 HBM4 표준(2025-04); SK Hynix HBM 점유 62%(Q2 2025)
관련: `knowledge-base/research/semiconductor/_meta.md`, `knowledge-base/research/semiconductor/hbm4_skhynix_isscc_ces_202605.md`, `knowledge-base/research/semiconductor/vlsi_symposium_2026_3d_memory_202606.md`, `knowledge-base/research/energy/`
