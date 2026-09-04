---
title: "Hot Chips 2026(HC38) — 메모리 월 심화: 컴퓨트 ~3×/2년 vs HBM 대역폭 <2×, 하이브리드 본딩 필수화 + 커스텀 ASIC 대량 등장(TPUv8·OpenAI Jalapeño·Rubin·MAIA200) + d-Matrix 3D-DRAM"
sector: semiconductor
topic: hotchips_2026_memory_wall
date_published: 2026-08
date_collected: 2026-09-05
last_updated: 2026-09-05
source_type: Conference
source: "Hot Chips 2026 (HC38) — SEMIVISION Research + Chip Log(Subbu) 컨퍼런스 리포팅 종합"
url: https://tspasemiconductor.substack.com/p/hot-chips-2026-the-memory-wall-is
citation: "📄 [Conference] Hot Chips 2026 (HC38) / SEMIVISION Research (2026-08) — 'The Memory Wall'"
key_finding: "Hot Chips 2026(HC38, 2026-08) 의 핵심 서사는 '병목이 컴퓨트에서 데이터 이동(메모리·인터커넥트·패키징)으로 이동'. AI 가속기 컴퓨트 성능은 ~3×/2년으로 증가하지만 HBM 대역폭은 역사적으로 <2×에 그쳐 메모리 월이 확대 → 하이브리드 본딩 채택이 필수화되고 HBM base die 를 선단 로직 공정으로 전환. 커스텀 실리콘이 대거 등장: Google TPUv8(Norman Jouppi), OpenAI 첫 추론 ASIC 'Jalapeño'(9개월 개발 — OpenAI 표현 '가장 빠른 ASIC 개발 사이클'), NVIDIA Vera CPU + Rubin GPU, Meta 칩, Microsoft MAIA 200, Groq LPU, Cerebras. d-Matrix 는 3D-DRAM(로직을 DRAM 스택/tensor engine 과 통합) 의 메모리 뱅크 아키텍처·성능·전력 수치를 발표 — HBM 대안 아키텍처의 상용화 근접 신호."
---

# Hot Chips 2026(HC38) — 메모리 월 심화 + 커스텀 ASIC 대량 등장 (2026-08)

> 성숙 semiconductor 섹터 L2 보강분(2026-09). 기존 `hbm4_samsung_isscc`·`hbm4_skhynix_isscc`·`vlsi_symposium_2026_3d_memory` 는 ISSCC/VLSI(2026 상반기)의 소자·수율·3D 메모리 기술 관점 — 본 요약은 **2026-08 Hot Chips(HC38)** 라는 신규 컨퍼런스에서 드러난 (1) 메모리 월의 정량화, (2) 하이브리드 본딩 필수화, (3) NVIDIA GPU 단일 의존을 흔드는 커스텀 ASIC 다변화, (4) HBM 대안(d-Matrix 3D-DRAM) 상용화 근접을 추가한다.

## 핵심 발견 (5건)

- **메모리 월 정량화 — 컴퓨트 ~3×/2년 vs HBM 대역폭 <2×**: HC38 의 관통 서사는 AI 의 다음 병목이 컴퓨트에서 데이터 이동으로 이동한다는 것. 원문 인용 _"AI accelerator compute capability has been increasing at roughly 3× every two years, while HBM bandwidth has historically improved at less than 2× over a comparable period."_ — 컴퓨트-메모리 대역폭 격차가 구조적으로 확대(📄 [Conference] Hot Chips 2026 / SEMIVISION, 2026-08).
- **하이브리드 본딩 필수화 + base die 선단 로직 전환**: 확대되는 메모리 월 대응으로 하이브리드 본딩 채택이 가속되고, HBM base die 를 선단 로직 공정으로 전환하는 흐름이 다수 발표에서 확인. Micron·Samsung·SK hynix 모두 메모리 아키텍처·HBM 패키징 로드맵 세션에 참여(📄 [Conference] Hot Chips 2026 / SEMIVISION·Chip Log, 2026-08). 후공정(TSV·하이브리드 본딩·advanced packaging) 낙수 강화.
- **커스텀 ASIC 대량 등장 — GPU 단일 의존 다변화**: 하이퍼스케일러 커스텀 실리콘이 대거 공개 — Google **TPUv8**(Norman Jouppi 발표), OpenAI 첫 추론 ASIC **'Jalapeño'**(9개월 개발, OpenAI 표현 _"the fastest ASIC development cycle ever achieved"_), NVIDIA **Vera CPU + Rubin GPU**, **Meta** 칩, Microsoft **MAIA 200**, **Groq LPU**, **Cerebras**(📄 [Conference] Hot Chips 2026 / Chip Log, 2026-08). NVIDIA GPU 독점 서사에 커스텀 실리콘 다변화가 정면 대비되는 국면.
- **d-Matrix 3D-DRAM — HBM 대안 상용화 근접**: d-Matrix 가 3D-DRAM 을 tensor engine 과 통합하는 방식(메모리 뱅크 아키텍처·성능·전력 수치 포함)을 발표 — HBM 을 우회/보완하는 대안 메모리 아키텍처가 발표 단계를 넘어 성능 수치를 제시하는 상용화 근접 신호(📄 [Conference] Hot Chips 2026 / Chip Log, 2026-08). 기존 `sangam_chiplet_pim_cxl`(arXiv, 2028~2030 장기 도전) 서사의 근시일 검증 포인트.
- **신규 메모리-컴퓨트 패브릭 등장**: Oxmiq Labs 가 AI 컴퓨트용 HBF(소스 표기 'Heterogeneous Fabric') 세션을 발표 — 메모리-컴퓨트 인터커넥트 계층의 아키텍처 실험이 넓어짐(📄 [Conference] Hot Chips 2026 / Chip Log, 2026-08).

## 데이터·근거

| 항목                | 데이터                                               | 출처                                                           |
| ------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| 컴퓨트 스케일링     | AI 가속기 ~3× / 2년                                  | 📄 [Conference] Hot Chips 2026 / SEMIVISION (2026-08)          |
| HBM 대역폭 스케일링 | 역사적 <2× / 동기간                                  | 📄 [Conference] Hot Chips 2026 / SEMIVISION (2026-08)          |
| 병목 이동           | 컴퓨트 → 데이터 이동(메모리·인터커넥트·패키징)       | 📄 [Conference] Hot Chips 2026 / SEMIVISION (2026-08)          |
| 하이브리드 본딩     | 채택 가속 + HBM base die 선단 로직 전환              | 📄 [Conference] Hot Chips 2026 / SEMIVISION·Chip Log (2026-08) |
| 커스텀 ASIC         | TPUv8·Jalapeño·Rubin+Vera·MAIA200·Meta·Groq·Cerebras | 📄 [Conference] Hot Chips 2026 / Chip Log (2026-08)            |
| OpenAI Jalapeño     | 추론 ASIC 9개월 개발("가장 빠른 ASIC 사이클")        | 📄 [Conference] Hot Chips 2026 / Chip Log (2026-08)            |
| d-Matrix 3D-DRAM    | 로직+DRAM/tensor engine 통합, 성능·전력 수치 발표    | 📄 [Conference] Hot Chips 2026 / Chip Log (2026-08)            |

## 분석가 활용 가이드 — Bull / Bear / Contrarian

- **Bull case (메모리·패키징 병목 = 공급사·후공정 프라이싱 파워)**: 메모리 월이 병목으로 확정될수록 HBM 대역폭·용량이 AI 가속기 성능을 좌우 → SK하이닉스·Samsung·Micron HBM 3강 lock-in 강화. 하이브리드 본딩·base die 선단 로직 전환은 advanced packaging(TSV·하이브리드 본딩) 소부장 낙수. NVIDIA(Rubin+Vera 통합)·AVGO/MRVL(커스텀 ASIC 설계 파트너) 수혜.
- **Bear case (GPU 단일 의존 다변화 + HBM 대안)**: TPUv8·Jalapeño·MAIA200·Meta·Groq 등 커스텀 ASIC 대량 등장은 하이퍼스케일러의 NVIDIA GPU 의존도를 구조적으로 낮추는 신호 — NVIDIA 물량/마진 프리미엄에 장기 하방 압력. d-Matrix 3D-DRAM 이 성능 수치를 제시하며 상용화에 근접하면 HBM 물량의 일부를 대체 가능 → 메모리 3강 TAM 상단 서사 약화.
- **Contrarian (병목이 곧 다변화 촉매 — 그러나 다변화 실현은 미검증)**: 메모리 월이 심할수록 HBM 대안(3D-DRAM·PIM·HBF)과 커스텀 ASIC 투자가 늘지만, Jalapeño 9개월·TPUv8·MAIA200 이 실제 대량 배치되어 NVIDIA 점유율을 잠식하는지는 미검증(발표≠양산). 반대로 대안이 실패하면 HBM 병목이 더 심화되어 3강 프라이싱 파워가 오히려 강화되는 양면 시나리오. 발표 단계 수치는 벤더 자체 주장으로, 독립 벤치마크 전까지 할인 필요.

## 한계

- 본 요약은 Hot Chips 2026(HC38) 를 다룬 **컨퍼런스 리포팅 2건**(SEMIVISION Research 2026-08-27, Chip Log by Subbu 2026-08-20) fetch 기반 — IEEE 세션 원문/슬라이드 딥페치는 미수행. 성능·전력 수치는 벤더 발표 기준으로 독립 검증 전까지 할인.
- Samsung zHBM(HBM 프로세서 직접 적층·전력효율 개선), Micron/Samsung compute-in-HBM base die, D-Matrix 4-high 스택 등 세부 수치는 WebSearch 종합(딥페치 미수행)으로만 확인 → 정량 인용 시 원출처 재확인.
- 'HBF' 정식 명칭은 소스에 'Heterogeneous Fabric' 로 표기되었으나 업계 통용 'High Bandwidth Flash' 와 혼용 가능 — 명칭 확정 전 인용 주의.
- 무력화 조건: 하이브리드 본딩 캐파 확충으로 메모리 월이 완화되면 병목 서사 약화. 커스텀 ASIC 이 양산 실패(수율·소프트웨어 생태계)하면 다변화 서사 무력화 → NVIDIA GPU 우위 지속.

## 인용 (Citation)

📄 [Conference] Hot Chips 2026 (HC38) / SEMIVISION Research (2026-08) — "The Memory Wall Is Making Hybrid Bonding a Necessity" → AI 가속기 컴퓨트 ~3×/2년 vs HBM 대역폭 <2×, 병목이 컴퓨트→데이터 이동, 하이브리드 본딩 필수화 + base die 선단 로직 전환

📄 [Conference] Hot Chips 2026 (HC38) / Chip Log(Subbu) (2026-08) — "3D-DRAM, Rubin, TPUv8, and OpenAI's Chip" → 커스텀 ASIC 라인업(TPUv8·OpenAI Jalapeño 9개월·Rubin+Vera·MAIA200·Meta·Groq·Cerebras) + d-Matrix 3D-DRAM tensor engine 통합(성능·전력 수치)

URL(본 세션 fetch):

- https://tspasemiconductor.substack.com/p/hot-chips-2026-the-memory-wall-is (SEMIVISION Research, 2026-08-27)
- https://www.chiplog.io/p/hot-chips-2026-preview-3d-dram-rubin (Chip Log by Subbu, 2026-08-20)

보조(검색 종합, 딥페치 미수행): Samsung zHBM(HBM on-processor, 전력효율 ~70% 개선 주장); Micron/Samsung HBM base die 컴퓨트 통합; D-Matrix 4-high 스택 SRAM급 속도 주장 — 정량 인용 시 원출처 재확인.
관련: `knowledge-base/research/semiconductor/_meta.md`, `hbm4_massproduction_dram_supercycle_202608.md`, `sangam_chiplet_pim_cxl_202604.md`, `vlsi_symposium_2026_3d_memory_202606.md`
