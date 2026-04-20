# Intel (INTC) 사업 & 산업 분석
> [리드 직접 수행] 2026-04-15 | KB 참조: ai.md, geopolitics.md

## 1. 반도체 산업 메가트렌드

### 1.1 AI 반도체 수요 폭증
- 글로벌 AI 반도체 시장: 2025 $1,200억 → 2026E $1,800억 (+50% YoY, KB ai.md)
- 하이퍼스케일러 CapEx 합산: 2025 $2,300억 → 2026E $3,000억 (+30% YoY)
- **Intel 포지션**: 수혜 제한적 (AI GPU 점유 1% 미만). 파운드리로 간접 수혜 노림.

### 1.2 파운드리 시장 구조 재편
- 2025 파운드리 점유: TSMC 60% / Samsung 12% / UMC 6% / Intel Foundry 3% / SMIC 4%
- 2030E 목표: TSMC 55% / Samsung 15% / **Intel 10%** (미국 정부 지원)
- **지정학적 기회**: 미·중 분리로 대만 TSMC 의존 축소 움직임 → Intel 반사이익

### 1.3 CPU 시장 정체 + ARM 침투
- PC CPU 시장: 2024 -5% YoY → 2025 +3% YoY → 2026E +5% YoY (안정)
- AI PC (NPU 탑재 PC): 2025 전체의 15% → 2027E 40% → Intel Core Ultra 탑재
- ARM 진영 위협:
  - Apple M 시리즈: 프리미엄 노트북 15%+ 잠식
  - Qualcomm Snapdragon X: 2024 출시, 2026 점유 3% 추정
  - NVIDIA+MediaTek ARM PC (2025 공개) → 2026H2 본격화

### 1.4 서버 CPU 시장 — AI로 재편
- 일반 서버 CPU 수요: 2026E +5% YoY 성장 (AI 서버 제외)
- AI 서버 비중: 2025 35% → 2026E 45% → 2030E 60%
- AI 서버에서 CPU 역할: 핵심에서 보조로 격하 (GPU/ASIC 주도)
- **Intel Xeon 점유**: 58% (2025) → 55% (2026E 추정) — AMD EPYC 지속 잠식

## 2. Intel 주력 사업 분석

### 2.1 CCG (Client Computing, PC CPU) — 55.7% 매출
**현황**
- 2025 매출 $30.5B, OPM 28% (고마진 캐쉬카우)
- PC CPU 점유 75~78% (데스크톱 강, 노트북 약세)

**성장 동력**
- **Meteor Lake/Lunar Lake/Arrow Lake**: AI PC 세대 (NPU 탑재, 45 TOPS+)
- **Panther Lake (2026 출시)**: 18A 공정 기반, Apple M4 대응
- **Core Ultra 3**: 프리미엄 AI PC 시장 재도전

**리스크**
- Apple M 시리즈 전통적 시장 이탈
- Qualcomm Snapdragon X + NVIDIA ARM PC 신규 진입
- PC 수요 구조적 정체 가능성

**전망**: 2026E +3~5% 성장, OPM 25~28% 유지. 안정적 캐쉬카우 지속.

### 2.2 DCAI (Data Center & AI) — 24.1% 매출
**현황**
- 2025 매출 $13.2B, OPM 12% (회복 중)
- Xeon 서버 CPU 점유 58%, Gaudi 3 AI 가속기 점유 1%

**성장 동력**
- **Granite Rapids**: 서버 CPU, 2024 출시, 코어당 성능 개선
- **Sierra Forest**: E-core 서버, 클라우드 네이티브 타깃
- **Gaudi 3**: NVIDIA H100 대비 50% 저렴, 성능 70%
- **Clearwater Forest (2026H2)**: 18A 기반 E-core 서버 대작

**리스크**
- AMD EPYC (Genoa-X → Turin → Zen 6) 지속 위협
- AI 서버 CPU 역할 축소 (GPU/ASIC 중심 이동)
- Gaudi AI 점유 미미 (CUDA 생태계 장벽)

**전망**: 2026E +15~20% 성장, OPM 15~18% 전망. 구조 회복 중.

### 2.3 Intel Foundry — 8.2% 매출 (미래 Bet)
**현황**
- 2025 매출 $4.5B (외부 고객 $2B, 내부 $2.5B)
- OPM -85% (**현재 회사 전체 적자의 주범**)

**Tech Roadmap**
| 노드 | 상태 | 2026E 양산 | 비고 |
|------|------|----------|------|
| Intel 7 | 양산 중 | — | 과거 10nm ESF |
| Intel 4 | 양산 중 | — | Meteor Lake CPU |
| Intel 3 | 양산 중 | — | Sierra Forest, Granite Rapids |
| Intel 20A | 취소 | — | 18A 집중 |
| **Intel 18A** | 초기 생산 | 2026H2 본격 | **핵심** |
| Intel 14A | R&D | 2027~2028 | 차세대 |

**18A 공정의 가치**
- PPA: TSMC N2 대비 +10~15% 성능 우위 (Intel 주장)
- 수율: 초기 40~50% (목표 60~70%) → **핵심 리스크**
- 외부 고객 수주:
  - **Microsoft**: 커스텀 AI 칩 (확정, 소량)
  - **Qualcomm**: 스마트폰 칩 협의 중
  - **Sony**: 게임 콘솔 칩 협의 중
  - **아마존/Google**: 비공식 협의

**전망**: 2027E Foundry BEP 도달, 2028E OPM +10~15%. **성공 시 회사 재평가 최대 동력**.

### 2.4 NEX (Network & Edge) — 10.8%
- 2025 매출 $5.9B, OPM 6% (부진)
- 5G 인프라 둔화, IoT 점진적 성장
- **분사 검토**: Altera (FPGA) 이미 분리, 추가 분사 가능

## 3. 경쟁 구도 심층 분석

### 3.1 AMD — 직접 경쟁 최강
| 영역 | Intel 점유 | AMD 점유 | 트렌드 |
|------|----------|---------|--------|
| PC CPU | 75~78% | 22~25% | AMD 점진 확대 |
| 서버 CPU | 58% | 32%+ | AMD 강세 지속 |
| GPU (게이밍) | 0% | 15% | — |
| AI GPU | ~1% | 10~15% | AMD 우위 |

- AMD Zen 6 (2026Q2~Q3): 서버 CPU 추가 잠식 위협
- 미·중 분리로 AMD 중국 매출 타격 시 Intel 반사이익

### 3.2 NVIDIA — AI 영역 절대 강자
- AI GPU 점유 80~85%, CUDA 생태계 Lock-in
- Intel의 대응 불가. **파운드리 고객으로 영입이 유일한 활로**
- 2026-04 NVIDIA-TSMC 동맹 공고, Intel 파운드리 진입 어려움

### 3.3 TSMC — 파운드리 절대 지배자
- 파운드리 점유 60%+, N2/A16 공정 기술 선도
- Apple, NVIDIA, AMD, Qualcomm 최첨단 공정 모두 TSMC
- Intel 18A가 유일한 TSMC 대안 → 성공 시 판도 재편

### 3.4 삼성 파운드리
- 점유 12%, 2nm 공정 수율 지속 이슈
- Intel과 미국 시장·외부 고객 경쟁
- 한국 정부 지원 對 미국 CHIPS Act 경쟁

### 3.5 경쟁 포지션 종합
```
AI GPU:       NVIDIA >>> AMD > Intel (거의 경쟁 불가)
서버 CPU:     Intel ≈ AMD (박빙, Intel 소폭 우위 유지)
PC CPU:       Intel > AMD > Apple > Qualcomm (Intel 압도적)
파운드리:     TSMC >>> Samsung > Intel (추격 중)
```

## 4. 성장성 평가

### TAM/SAM/SOM
- **TAM (2030E)**:
  - 반도체 전체: $1.5T
  - Intel 관련 영역 (CPU+파운드리+AI): $650B
- **SAM (Intel 접근 가능)**: $300B
- **SOM (2030E 실현 가능)**: $100~130B (연간 매출)
  - 2025 $55B → 2030E $100~130B = CAGR **+13~19%/년**

### 성장 스코어
| 항목 | 점수 | 근거 |
|------|-----|------|
| 시장 성장률 | 7/10 | AI 반도체 +30% CAGR, Intel은 간접 수혜 |
| 점유율 확대 | 5/10 | AI GPU 실패, 파운드리 희망 |
| 신규 사업 | 8/10 | Foundry 외부 고객, 18A 성공 가정 |
| 글로벌 확장 | 7/10 | 미·유럽·이스라엘 다중 팹 |
| **종합 성장성** | **6.75/10** | **중상위 (턴어라운드 보조 모멘텀 강)** |

## 5. 산업 분석 결론
1. **Tailwind (순풍)**: AI 반도체 성장, CHIPS Act, 지정학적 대만 대안 수요
2. **Headwind (역풍)**: CUDA Lock-in, AMD 경쟁, ARM 진영 확대
3. **Intel의 특별한 위치**: 유일한 미국계 IDM, 정부 전략자산
4. **성공 조건**: 18A 공정 수율 확보 + 외부 고객 2~3곳 메이저 수주
5. **실패 시**: Foundry 분사 → CPU 전업 회사로 전환 (Wide Moat 포기)
