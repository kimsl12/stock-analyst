---
title: "Sangam — Chiplet 기반 DRAM-PIM 가속기 CXL 통합 (LLM 추론 H100 대비 10배)"
sector: semiconductor
topic: sangam_chiplet_pim_cxl
date_published: 2025-11-15
date_collected: 2026-05-12
source_type: Preprint
source: "arXiv:2511.12286 (UVA·UCSD)"
url: https://arxiv.org/abs/2511.12286
citation: "📄 [Preprint] arXiv:2511.12286 (2025-11) — 'Sangam: Chiplet-Based DRAM-PIM Accelerator with CXL Integration for LLM Inferencing'"
key_finding: "Chiplet-DRAM-PIM + CXL 통합 아키텍처가 LLaMA 70B 등 LLM 추론에서 H100 대비 디코딩 처리량 최대 10.3배·쿼리 지연 최대 4.22배 단축 — GPU 단일 의존 시나리오에 도전하는 차세대 메모리 아키텍처 학술 신호"
---

# Sangam — Chiplet-Based DRAM-PIM Accelerator with CXL Integration for LLM Inferencing

## 핵심 발견 (5건)

- **저자**: Khyati Kiyawat, Zhenxing Fan, Yasas Seneviratne, Morteza Baradaran, Akhil Shekar, Zihan Xia, Mingu Kang, Kevin Skadron (UVA·UCSD). arXiv 2025-11-15 게재.
- LLM 추론(특히 **decoding 단계**)이 GEMV·flat GEMM 위주 메모리 바운드로 지배됨을 정량 증명: "Inference, particularly the decoding phase, is dominated by memory-bound GEMV or flat GEMM operations with low operational intensity."
- 제안 아키텍처: **로직 chiplet + 메모리 chiplet 이종 노드** interposer 연결 + systolic array + SRAM 버퍼 — 기존 PIM의 용량·연산 한계 동시 해결.
- **CXL 통합**: GPU 대체(replacement) 또는 보조(co-processor) 양방향 시나리오 — H100 옆에 붙는 형태도, 단독 형태도 가능.
- 성능 (3개 모델 평균): LLaMA 2-7B / Mistral-7B / LLaMA 3-70B에서 **디코딩 처리량 10.3·9.5·6.36배** 향상, **쿼리 지연 3.93·4.22·2.82배** 단축. 에너지 효율 **H100 대비 자릿수(order of magnitude) 절감**.

## 데이터·근거

| 모델 | 디코딩 처리량 (vs H100) | 쿼리 지연 단축 | 에너지 효율 |
|---|---|---|---|
| LLaMA 2-7B | 10.3× | 3.93× | order of magnitude ↓ |
| Mistral-7B | 9.5× | 4.22× | order of magnitude ↓ |
| LLaMA 3-70B | 6.36× | 2.82× | order of magnitude ↓ |

핵심 가정: 로직 chiplet과 메모리 chiplet의 이종 프로세스 노드 결합 (메모리 1c, 로직 4nm급) + CXL 3.0 인터커넥트.

## 분석가 활용 가이드 — Bull / Bear / Contrarian

- **Bull case (메모리 3강)**: PIM이 본격화되면 메모리 ASP가 상승 (단순 DRAM → "compute-in-memory"). SK하이닉스 HBM-PIM 이미 발표, Samsung HBM3-PIM 데모. 본 논문은 chiplet + CXL 결합 가능성 학술 검증 → 메모리 제조사가 단순 부품 공급자에서 시스템 제공자로 격상.
- **Bear case (NVIDIA · H100)**: GPU 단일 아키텍처가 추론에서 가장 효율적이라는 thesis가 학술적으로 흔들림. NVIDIA가 자체 PIM/CXL 솔루션(NVLink Fusion 등) 미리 시장 선점하지 못하면 추론 GPU 점유율 둔화 가능.
- **Contrarian**: 학술 prototype과 양산 사이 5~7년 시차 일반. 본 논문도 시뮬레이션 + chiplet interposer는 양산 yield·열관리 큰 과제. CXL 3.0 자체가 2026 현재 막 보급 시작. 본 thesis는 2028~2030 사이 실현 가능성 — 현재 종목 thesis 직접 영향 제한적.

## 한계

- **시뮬레이션 기반 결과** — 실제 칩 테이프아웃 결과 X.
- 학습(training)에는 적용 안 됨, 추론(inference) 특화.
- chiplet interposer + CXL은 양산 시 yield·비용 큰 변수.
- 무력화: 동일 저자 그룹 또는 경쟁 그룹이 2026~2027 사이 silicon prototype 발표 시 본 thesis 재검토.

## 인용 (Citation)

📄 [Preprint] arXiv:2511.12286 (2025-11-15) — Kiyawat et al. "Sangam: Chiplet-Based DRAM-PIM Accelerator with CXL Integration for LLM Inferencing" §Results — LLaMA 3-70B에서 H100 대비 디코딩 6.36×, 쿼리 지연 2.82×

URL: https://arxiv.org/abs/2511.12286
