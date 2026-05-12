---
title: "Samsung 36GB HBM4 12-Hi 3.3 TB/s — ISSCC 2026 양산 가시화"
sector: semiconductor
topic: hbm4_samsung_isscc
date_published: 2026-02-21
date_collected: 2026-05-12
source_type: Conference
source: "ISSCC 2026"
url: https://newsletter.semianalysis.com/p/isscc-2026-nvidia-and-broadcom-cpo
citation: "📄 [Conference] ISSCC 2026 (2026-02) — Samsung 36GB HBM4 12-Hi 3.3 TB/s, SF4 base + 1c DRAM"
key_finding: "Samsung 36GB HBM4 12-Hi가 3.3 TB/s·2048 IO·핀당 13Gb/s 달성 — NVIDIA Rubin 요건 부합, SK하이닉스 단독 우위 시나리오에 직접 도전"
---

# Samsung 36GB HBM4 12-Hi 3.3 TB/s — "Industry-First Commercial HBM4 With Ultimate Performance for AI Computing"

## 핵심 발견 (5건)

- Samsung이 ISSCC 2026에서 36GB·12-Hi HBM4 스택을 시연. **3.3 TB/s 대역폭**, **2048 IO 핀**, 핀당 최대 **13 Gb/s** 동작.
- 6세대 10nm급(1c) DRAM 코어 다이 + **SF4 로직 베이스 다이** 조합 — Samsung 파운드리·메모리 통합 가치사슬 활용 첫 양산급 제품.
- ABB(Adaptive Body-Bias) 제어로 스택된 코어 다이 간 프로세스 변동 보정 + **TSV 갯수 2배 증가**로 타이밍 마진 추가 개선.
- 채널별 TSV RDQS 타이밍 자동 캘리브레이션 (replica RDQS path + TDC + DCDL) — 12-Hi 적층에서 발생하는 타이밍 정합성 문제 해소.
- NVIDIA가 차세대 Rubin AI 플랫폼용 HBM4를 위해 Samsung에 종전 대비 약 2배 가격을 지불할 가능성이 보도됨 — SK하이닉스 단독 공급자 프리미엄 잠재 변화.

## 데이터·근거

| 항목 | Samsung HBM4 (ISSCC 2026) | 비교 (HBM3E 8-Hi 일반) |
|---|---|---|
| 용량 (스택당) | 36 GB | 24 GB |
| 대역폭 (스택당) | 3.3 TB/s | 1.2 TB/s |
| IO 핀 수 | 2,048 | 1,024 |
| 핀당 속도 | 13 Gb/s | 9.2 Gb/s |
| DRAM 노드 | 1c (10nm급 6세대) | 1b |
| 베이스 다이 | SF4 (Samsung Foundry 4nm) | 자체 DRAM 프로세스 |
| 적층 | 12-Hi | 8-Hi |

## 분석가 활용 가이드 — Bull / Bear / Contrarian

- **Bull case (Samsung 005930)**: Samsung Foundry SF4 + DRAM 1c 결합이 ISSCC 양산급 발표 단계까지 도달. NVIDIA 2배 가격 수주 보도 시 HBM 매출 점프 + 파운드리 가동률 동반 상승. HBM 시장 3강 구도(SK하이닉스·Samsung·Micron) 명문화.
- **Bear case (SK hynix 000660)**: Samsung 정식 양산 진입 시 SK하이닉스 단독 NVIDIA 공급자 프리미엄 단계적 침식. 2027년 마진 -3~5%p 가능성(NBER 메모리 사이클 연구 일반 패턴).
- **Contrarian**: ISSCC 발표 ≠ 양산. Samsung 13 Gb/s는 SK하이닉스 11.7 Gbps 16-Hi 48GB 대비 빠르지만 적층 수가 12 vs 16. 실제 NVIDIA Rubin 채택 시 16-Hi 48GB가 더 선호될 가능성 → Samsung 12-Hi 36GB는 "B등급 슬롯" 한정 수주 시나리오.

## 한계

- ISSCC paper는 양산 데이터가 아닌 **prototype 시연**. yield·신뢰성·고객 인증 단계는 별도.
- NVIDIA 2배 가격 보도는 NotebookCheck 등 2차 보도 기반, NVIDIA·Samsung 공식 confirm 없음.
- "Rubin 요건 충족" 표현은 공식 NVIDIA spec sheet가 아닌 추정. Rubin 정확 spec은 2026 H2 GTC에서 확정 예상.
- 무력화 시점: Samsung이 2026 Q3까지 NVIDIA 정식 인증 받지 못하면 본 thesis 약화.

## 인용 (Citation)

📄 [Conference] ISSCC 2026 (2026-02) — Samsung "36GB HBM4 12-Hi 3.3 TB/s with SF4 base die + 1c DRAM, 2048 IO, 13 Gb/s/pin" → SK하이닉스 단독 우위 시나리오에 직접 도전, Rubin 요건 부합

URL: https://newsletter.semianalysis.com/p/isscc-2026-nvidia-and-broadcom-cpo
관련: https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing
