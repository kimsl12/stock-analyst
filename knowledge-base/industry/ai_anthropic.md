---
updated: 2026-04-09
valid_until: 2026-05-09
sector: ai
sub_sector: llm_foundation_model
company: Anthropic
ticker: 비상장 (IPO 검토 중)
sources: [Anthropic 공식, CNBC, Bloomberg, Yahoo Finance, TechCrunch, SaaStr, The AI Corner, Google Cloud, Tracxn, Forge Global, Wikipedia, CNN, Axios]
confidence: high
last_synced_from_db: 2026-04-09
db_records: 34
---

# Anthropic (엔트로픽) Knowledge Base

## ★ CURRENT (에이전트는 이 파일의 데이터를 그대로 사용) ★

---

### 1. 기업 개요

| 항목 | 내용 |
|------|------|
| 정식 명칭 | Anthropic, PBC (Public Benefit Corporation) |
| 설립 | 2021년 |
| 본사 | San Francisco, California, USA |
| 창업자 | Dario Amodei, Daniela Amodei 외 5명 (OpenAI 출신 7인) |
| CEO | Dario Amodei (전 OpenAI VP of Research) |
| 사장 | Daniela Amodei |
| 핵심 미션 | AI 안전성 연구 기반의 신뢰할 수 있는 AI 시스템 개발 |
| 법인 구조 | Public Benefit Corporation — 주주 이익과 공익 동시 추구 |

#### 주요 경영진 및 이사회

| 직책 | 이름 | 비고 |
|------|------|------|
| CEO / 공동창업자 | Dario Amodei | 전략 비전 및 운영 총괄 |
| 사장 / 공동창업자 | Daniela Amodei | 전략 방향 및 운영 |
| 공동창업자 | Jack Clark | 전략 이니셔티브 및 정책 |
| 공동창업자 | Tom Brown | 기술팀 관리, AI 연구 |
| 공동창업자 | Sam McCandlish | 기술팀 관리, AI 연구 |
| CISO | Jason Clinton | 사이버보안 전략 |

**이사회**: Dario Amodei, Daniela Amodei, Yasmin Razavi, Jay Kreps, Reed Hastings, Chris Liddell

---

### 2. 투자 유치 이력 (전체 누적 $67.3B)

| 라운드 | 시기 | 조달액 | 밸류에이션 | 주요 투자자 |
|--------|------|--------|-----------|------------|
| Series A | 2021 | $1.24억 | 비공개 | Jaan Tallinn, Google, Spark Capital |
| Series B | 2022 | $5.8억 | 비공개 | Google, Spark Capital, Salesforce Ventures |
| Series C | 2023.05 | $4.5억 | 비공개 | Spark Capital(리드), Google, Salesforce Ventures, Sound Ventures, Zoom Ventures |
| Amazon 투자 | 2023.09~ | **$80억** (누적) | — | Amazon (Project Rainier 연계, 커스텀 칩·DC 포함) |
| Google 투자 | 2023~ | **$30억+** (누적) | — | Google ($2B+$1B+). 2026년 100만 TPU 공급 계약 별도 |
| **Series E** | **2025.03** | **$35억** | **$615억** | Lightspeed Venture Partners(리드), Bessemer, Cisco, D1 Capital, Fidelity, General Catalyst, Jane Street, Menlo Ventures |
| **Series F** | **2025.09** | **$130억** | **$1,830억** | 비공개 (6개월 만에 밸류 3배) |
| **Series G** | **2026.02** | **$300억** | **$3,800억** | Coatue, GIC(싱가포르 국부펀드) 리드. D.E. Shaw Ventures, Dragoneer, Founders Fund, ICONIQ, MGX |

> 총 누적 조달: $67.3B (17회 라운드). Series G는 테크 역대 2번째 최대 민간 펀딩 (1위: OpenAI $40B+).
> 밸류에이션 추이: $61.5B(2025.03) -> $183B(2025.09) -> $380B(2026.02) — 12개월 내 6배 상승.

---

### 3. 매출 / ARR (연환산 매출)

| 시점 | ARR | 성장률 | 비고 |
|------|-----|--------|------|
| 2024.12 | ~$10억 | — | 기점 |
| 2025.07 | ~$40억 | 7개월 만에 4x | Claude API 엔터프라이즈 채택 가속 |
| 2025.08 | ~$50억 | — | B2B 고객 30만+ 돌파 |
| 2025.12 | ~$90억 | 연간 ~9x 성장 | — |
| 2026.02 | ~$140억 | 2개월 만에 +56% | Claude Code ARR $25억 기여 |
| 2026.03 | ~$190~200억 | — | Bloomberg: ARR $20B 근접 |
| **2026.04** | **~$300억** | **+1,400% YoY** | **OpenAI($25B) 최초 추월** |

#### 수익 동력 분석

| 항목 | 내용 |
|------|------|
| Claude Code | ARR $25억 (2026.02). 2026년 초 대비 2배+. 개발자 에이전트 시장 핵심 |
| 엔터프라이즈 LLM | 시장 점유율 40% (OpenAI 27%, Google 21%) |
| B2B 고객 | 30만+ 기업, $1M+/연 지출 기업 1,000+ (2026.04) |
| 수익성 | 현재 적자 (대규모 인프라 투자). **2027년 FCF 흑자 전환 전망** |

> OpenAI 대비 학습 비용 1/4 수준에서 매출 역전. 엔터프라이즈 중심 전략이 높은 마진 구조에 기여.

---

### 4. 제품 라인업 — Claude 모델 패밀리

#### 현행 모델 (2026.04 기준)

| 모델 | API ID | 가격 (Input/Output per MTok) | 컨텍스트 | 최대 출력 | 학습 데이터 cutoff | 특징 |
|------|--------|------------------------------|----------|----------|------------------|------|
| **Claude Opus 4.6** | claude-opus-4-6 | $5 / $25 | 1M 토큰 | 128K | 2025.08 | 최고 지능, 코딩·추론 최강. Extended/Adaptive thinking |
| **Claude Sonnet 4.6** | claude-sonnet-4-6 | $3 / $15 | 1M 토큰 | 64K | 2026.01 | 속도+지능 균형. Extended/Adaptive thinking |
| **Claude Haiku 4.5** | claude-haiku-4-5 | $1 / $5 | 200K 토큰 | 64K | 2025.07 | 최고속, 근접 프론티어 지능. Extended thinking |

#### 레거시 모델 (여전히 이용 가능)

| 모델 | API ID | 가격 (Input/Output) | 컨텍스트 | 비고 |
|------|--------|---------------------|----------|------|
| Claude Sonnet 4.5 | claude-sonnet-4-5 | $3 / $15 | 200K | SWE-bench 77.2% 최고 |
| Claude Opus 4.5 | claude-opus-4-5 | $5 / $25 | 200K | 2025.11 출시 |
| Claude Opus 4.1 | claude-opus-4-1 | $15 / $75 | 200K | 2025.08 출시 |
| Claude Sonnet 4 | claude-sonnet-4-0 | $3 / $15 | 200K | 2025.05 출시 |
| Claude Opus 4 | claude-opus-4-0 | $15 / $75 | 200K | 2025.05 출시 |

> Claude Haiku 3 (claude-3-haiku-20240307) — **2026.04.19 지원 종료 예정**

#### 특수 모델

| 모델 | 상태 | 용도 |
|------|------|------|
| **Claude Mythos Preview** | 초대 전용 연구 프리뷰 | 방어적 사이버보안 (Project Glasswing) |

> Mythos Preview: 수만 건 취약점 탐지 능력. 악용 위험으로 공개 출시 보류. 11개 빅테크 기업 참여 (AWS, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorgan, Linux Foundation, Microsoft, Nvidia, Palo Alto Networks). Anthropic $100M 크레딧 + $4M 오픈소스 기부.

#### 모델 출시 히스토리

```
Claude 1 (2023.03) → Claude 2 (2023.07, 첫 대중 공개)
→ Claude 3 (2024.03) → Claude 3.5 Sonnet (2024.06)
→ Claude 4 / Opus 4 (2025.05, Claude Code GA 동시)
→ Claude Sonnet 4.5 (2025.09) → Claude Opus 4.5 (2025.11)
→ Claude Opus 4.6 / Sonnet 4.6 (현재 최신)
→ Claude 5 (2026 Q2~Q3 출시 예상, AGI 근접 추론)
```

#### Claude Code

- 2025.02 출시 (프리뷰) -> 2025.05 GA (Claude 4 동시 출시)
- 에이전트형 CLI 코딩 도구
- ARR $25억 (2026.02) — 전체 매출의 핵심 성장 엔진
- Cowork Dispatch 등 멀티에이전트 워크플로우 지원

#### API 비용 최적화

- Prompt caching: 90% 절감
- Batch API: 50% 할인
- 결합 시 최대 95% 비용 절감 가능
- Message Batches API: Opus 4.6/Sonnet 4.6에서 300K 출력 토큰 지원

---

### 5. 경쟁 구도 (2026.04 기준)

| 기업 | 주요 모델 | ARR/매출 | 밸류에이션 | 전략 | 강점 |
|------|----------|----------|-----------|------|------|
| **Anthropic** | Claude Opus 4.6, Sonnet 4.6 | **$30B** (2026.04 ARR) | $380B (비상장) | 엔터프라이즈·API 중심 | 엔터프라이즈 점유율 40%, AI 안전성, 비용 효율 |
| **OpenAI** | GPT-4o, o1, o3 | ~$25B (ARR) | ~$300B+ (비상장) | 소비자+엔터프라이즈 | ChatGPT MAU 8억+, 브랜드 인지도, MS 파트너십 |
| **Google DeepMind** | Gemini 2.0, Ultra | 수십억 달러 (추정) | Alphabet 내 사업부 | 제품 통합 (Search, Workspace) | 자체 TPU, 7.5억+ MAU(Gemini), 데이터 해자 |
| **Meta AI** | Llama 3.1+ (오픈소스) | 비공개 (광고 수익 간접) | Meta 내 사업부 | 오픈소스 생태계 | 무료 배포, 개발자 커뮤니티, 메타버스 AI |
| **xAI** | Grok | 비공개 | ~$50B+ (비상장) | X(트위터) 통합 | 실시간 데이터, Elon Musk 네트워크 |

#### 소비자 앱 시장 점유율 (2026 초)

| 서비스 | 점유율 | 추세 |
|--------|--------|------|
| ChatGPT (OpenAI) | 45.3% (2025.01 69.1%에서 하락) | 하락 |
| Gemini (Google) | 25.2% (2025.01 14.7%에서 상승) | 상승 |
| Claude (Anthropic) | 엔터프라이즈 집중, 소비자 앱 점유율 미공개 | — |

#### 엔터프라이즈 LLM 지출 점유율

| 기업 | 점유율 |
|------|--------|
| **Anthropic** | **40%** |
| OpenAI | 27% |
| Google | 21% |
| 기타 | 12% |

---

### 6. IPO 전망

| 항목 | 내용 | 출처 |
|------|------|------|
| 목표 시기 | **2026년 10월** (Q4 2026) | FT, Yahoo Finance, 복수 매체 |
| S-1 제출 | 2026년 여름 예상 | Winbuzzer, MLQ.ai |
| 예상 밸류에이션 | $400~500B (IPO 시점) | 투자은행 추정 |
| 조달 목표 | $60B+ | Techi.com, Let's Data Science |
| 주관사 | Goldman Sachs, JPMorgan Chase | 복수 매체 |
| 법률 자문 | Wilson Sonsini | 복수 매체 |
| Anthropic 공식 입장 | "IPO 여부 결정 사항 없음" | Reuters |
| 변수 | SEC 매출 회계 처리 판단, AI 시장 분위기, 금리 환경 | 복수 분석 |

> OpenAI도 2026년 IPO 검토 중. AI 기업 동시 상장 시 시장 자금 분산 리스크.

---

### 7. AI 안전성 연구

#### Constitutional AI (헌법적 AI)

- 사전 정의된 윤리 원칙("헌법")으로 AI 행동을 지도
- 인간 레이블 없이 자기개선(Self-Improvement) 학습
- **Constitutional Classifiers** (2025): 범용 탈옥(jailbreak) 방어 시스템
- 버그바운티: 8단계 탈옥 데모 통과 시 $10,000, 범용 탈옥 전략 $20,000

#### Responsible Scaling Policy (RSP) v3.0

- 2년+ 운영 경험 반영, 투명성·책임·현실성 강화 구조 개편
- **ASL-3 보안 조치** 2025.05 발동: 화학·생물 오용 방어 입출력 분류기 배치
- **Provable Inference 프로토타입**: 2026.09 목표 — AI 출력의 증명 가능한 서명 기술
- Frontier Safety Roadmap: 데이터 보존 정책 개선, 2026.05.11 신규 목표 발표 예정

---

### 8. 최신 뉴스 (2025~2026)

| 날짜 | 사건 | 영향 |
|------|------|------|
| 2025.03 | Series E $35억 조달 ($615억 밸류) | 본격 스케일업 자금 확보 |
| 2025.05 | Claude 4 출시 + Claude Code GA | 에이전트 코딩 시장 진입 |
| 2025.05 | ASL-3 보안 조치 발동 | AI 안전 업계 선도 |
| 2025.09 | Series F $130억 ($1,830억 밸류) | 6개월 만에 밸류 3배 |
| 2025.09 | Claude Sonnet 4.5 출시 (SWE-bench 1위) | 코딩 벤치마크 최고 성능 |
| 2025.11 | Claude Opus 4.5 출시 | 지능 프론티어 갱신 |
| 2026.02 | **Series G $300억 ($3,800억 밸류)** | 테크 역대 2번째 최대 민간 펀딩 |
| 2026.02 | ARR $140억 돌파, Claude Code $25억 | 초고속 성장 확인 |
| 2026.03 | ARR $200억 근접 | Bloomberg 보도 |
| 2026.04.06 | **Google Cloud 100만 TPU 공급 계약** | 수십억 달러 규모 인프라 확장 |
| 2026.04.06 | **Broadcom TPU 칩 제조 확인** | Google-Broadcom-Anthropic 삼각 파트너십 |
| 2026.04.07 | **Project Glasswing + Mythos Preview 발표** | 차세대 사이버보안 방어 AI, 11개 빅테크 참여 |
| 2026.04.08 | **Pentagon 공급망 리스크 지정 소송 패소** | 자율 타겟팅·시민 감시 거부로 트럼프 행정부와 갈등 |
| 2026.04 | **ARR $300억 돌파, OpenAI 최초 추월** | 엔터프라이즈 AI 시장 1위 확정 |

---

### 9. 리스크 팩터

| 리스크 | 내용 | 심각도 |
|--------|------|--------|
| 대규모 적자 지속 | 인프라 투자 비용. 2027 FCF 흑자 전환까지 현금 소진 | 중간 |
| IPO 불확실성 | SEC 매출 회계, 시장 여건, AI 규제 변수 | 중간 |
| Pentagon 분쟁 | 공급망 리스크 지정 시 정부 계약 제한 가능 | 높음 |
| AI 안전 정책 갈등 | RSP 변경 보도(CNN 2026.02), 정부 요구와 안전 원칙 충돌 | 중간 |
| 경쟁 심화 | OpenAI GPT-5, Google Gemini 2.0, 오픈소스 LLM 압박 | 중간 |
| 밸류에이션 정당성 | $380B 밸류 vs ARR $30B — PSR ~12.7x (고평가 논쟁) | 중간 |
| 클라우드 의존 | Google Cloud + AWS 양대 인프라 의존 (경쟁사이자 투자자) | 낮음 |
| 인재 유출 | OpenAI, Google, xAI 등과의 인재 쟁탈전 | 낮음 |

---

### 10. 데이터 정합성 검증 (자동)

| 항목 | 검증 결과 |
|------|---------|
| 밸류에이션 추이 ($61.5B -> $183B -> $380B) | 단조 증가, 정상. 각 라운드 사이 2.5~3x 점프 합리적 |
| ARR 추이 ($1B -> $4B -> $9B -> $14B -> $30B) | 단조 증가, 급가속. 15개월 내 30x 성장은 극단적이나 다수 독립 매체 교차 확인 |
| 누적 조달 $67.3B vs 개별 합산 ($0.12+$0.58+$0.45+$8+$3+$3.5+$13+$30=$58.65B) | 차이 $8.65B — 비공개 라운드·전환사채 등 포함 시 합리적 범위. Tracxn 17회 라운드 기준 |
| 엔터프라이즈 점유율 40%+27%+21%=88% | 나머지 12%는 Mistral, Cohere, AWS Bedrock 자체 등. 합리적 |
| PSR 역산: $380B / $30B ARR = 12.7x | AI 섹터 고성장 기업 PSR 10~20x 범위 내. 합리적 |

---

*이 파일은 knowledge-db/ai_2026.jsonl 중 Anthropic 레코드 (34건)에서 생성되었습니다.*
*HISTORY는 knowledge-db/에 영구 보관됩니다.*
*마지막 웹검색 기반 갱신: 2026-04-09.*
