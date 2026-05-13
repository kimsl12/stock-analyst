# Anthropic, PBC — 기업개요 & Moat (v1, 2026-05-13)

> ⚠️ Anthropic 은 비상장 (private) 회사. 본 분석은 가격 기반 투자 권고가 아니며, AI 산업 경쟁구도 매핑 + 다음 펀딩 라운드 평가 참고용 정성 분석. 직접 투자 불가, 노출 경로는 Google(GOOGL) / Amazon(AMZN) 보유 또는 2차 시장 secondary.

## 1. 기업 개요

| 항목 | 내용 |
|------|------|
| 정식 명칭 | Anthropic, PBC (Public Benefit Corporation) |
| 설립 | 2021년 |
| 본사 | San Francisco, California |
| 창업자 | Dario Amodei, Daniela Amodei + OpenAI 출신 5인 (Sam McCandlish, Tom Brown, Jared Kaplan, Jack Clark, Chris Olah) |
| CEO | Dario Amodei (전 OpenAI VP of Research) |
| 사장(President) | Daniela Amodei |
| 법인 구조 | Public Benefit Corporation — 주주 이익과 공익 동시 추구 (Delaware) |
| 핵심 미션 | "Build reliable, interpretable, and steerable AI systems" — AI 안전성 연구 기반 신뢰 가능한 AI 개발 |
| 임직원 수 (2026 Q1 추정) | 약 1,800~2,000명 (2024 말 ~500명 → 4배 확장) |
| 이사회 | Dario Amodei, Daniela Amodei, Yasmin Razavi(Spark), Jay Kreps(Confluent), Reed Hastings(Netflix), Chris Liddell |

## 2. 지배구조 — 비상장이지만 독특한 구조

### 2.1 PBC + LTBT 이중 거버넌스
Anthropic 은 단순 비상장 스타트업이 아니라 **PBC + Long-Term Benefit Trust (LTBT)** 이중 구조이다.

- **PBC (Public Benefit Corporation)**: Delaware 법인. 정관에 "AI 안전성 + 인류 이익" 명시. 주주는 단기 이익만 요구할 수 없음.
- **LTBT (Long-Term Benefit Trust)**: 독립 신탁. 이사회 다수석을 점진 통제하는 구조. 트러스티 5인이 회사의 미션 일관성을 감독. 트러스티는 Anthropic 임직원·투자자가 아닌 외부 전문가.

이 구조는 OpenAI의 "501(c)(3) → Capped-Profit LLC → For-Profit 전환" 사태를 의식한 사전 방어 설계로, 향후 IPO 시에도 LTBT 통제권 유지가 핵심 협상 변수가 될 가능성이 크다.

### 2.2 핵심 인력 — OpenAI 출신 + Google Brain 출신 혼합
- **연구진**: OpenAI GPT-3 핵심 저자 다수 (Tom Brown — GPT-3 1저자, Jared Kaplan — Scaling Laws), Google Brain 출신 Chris Olah (interpretability research) 등.
- **2025~2026 신규 영입**: Mike Krieger (Instagram 공동창업자, CPO), Krishna Rao (CFO, 전 Airbnb), Jared Kaplan (Chief Science Officer 승격).

## 3. 핵심 제품 라인업 (2026 Q2 기준)

### 3.1 Claude 모델 패밀리
| 모델 | 포지셔닝 | 컨텍스트 | API 가격 (input/output, per 1M tok) | 출시 |
|------|---------|---------|------------------------------------|------|
| Claude Opus 4.7 | 최상위 추론, agent 작업 | 1M | $15 / $75 | 2026 Q2 |
| Claude Opus 4.5 | 직전 최상위 | 1M | $15 / $75 | 2026 Q1 |
| Claude Sonnet 4.5 | 균형 (가장 많이 호출됨) | 1M | $3 / $15 | 2026 Q1 |
| Claude Haiku 4.5 | 고속·저가 | 200K | $0.80 / $4 | 2026 Q1 |

### 3.2 Claude Code — 신규 성장 엔진
- 2025 Q3 발표 → 2026 Q1 GA. CLI + 에이전트형 코딩 도구.
- **Run-rate ARR $2.5B** (2026 초, Anthropic 자체 공시).
- GitHub Copilot 대비 "스위처" 51% 가 Claude Code로 이동 (Anthropic 내부 데이터, JetBrains·VS Code 익스텐션 텔레메트리).
- 경쟁: GitHub Copilot (Microsoft), Cursor, Cognition Devin, OpenAI Codex.

### 3.3 Computer Use + Marketplace
- **Claude Computer Use**: 2026.03 GA. AWS Bedrock·Google Vertex·Microsoft Foundry 3대 멀티클라우드 배포. OpenAI Operator·Google Agentspace와 직접 경쟁.
- **Anthropic Marketplace**: 2026.03 론칭. Snowflake (데이터), Harvey (법무 AI), Replit (코딩) 등 엔터프라이즈 에이전트 마켓플레이스 — OpenAI GPT Store의 B2B 버전.

### 3.4 MCP (Model Context Protocol)
- 2024 말 오픈소스 공개. AI 에이전트가 외부 도구·데이터를 표준 방식으로 호출하는 프로토콜.
- 2026 Q2 기준 GitHub stars 60K+, OpenAI·Google도 부분 채택. **사실상 업계 표준화 진행 중** — Anthropic의 가장 강력한 비매출 해자.

### 3.5 Project Glasswing + Mythos Preview (보안 AI)
- 2026.04 발표. 방어적 사이버보안 AI. 수만 건 취약점 자동 탐지.
- 11개 빅테크 참여 (AWS, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorgan, Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks).
- Anthropic $100M 크레딧 + $4M 오픈소스 기부 — 정부·국방 영역 진입 전략 (Pentagon 갈등 우회용).

## 4. Economic Moat — Narrow → Wide 전환 중

### Moat 등급: 7.5 / 10 (Narrow-to-Wide)

| 구성요소 | 강도 | 근거 |
|----------|-----|------|
| 기술 리더십 (모델 품질) | 강함 | SWE-bench 1위, MMLU·GPQA 상위. Constitutional AI 학습 효율 (OpenAI 1/4 비용) |
| 전략적 투자자 네트워크 | **매우 강함** | Amazon $8B + Google $3B+ 동시 파트너십. AWS·GCP 모두 우선 배포 — 경쟁사 복제 불가 |
| 엔터프라이즈 침투 | **매우 강함** | 엔터프라이즈 LLM 시장 40% 점유 (Menlo). Fortune 500 70%+. $1M+/연 고객 1,000+ |
| Compute 우선권 | 강함 | TPU v7 Ironwood 100만 칩 + AWS Trainium2 ~30만 칩 — OpenAI 다음 규모 |
| 인재 해자 | 강함 | GPT-3 핵심 저자 + Google Brain interpretability 팀. PBC·LTBT 미션이 가치 지향 인재 유인 |
| 안전성 브랜드 | 보통 | RSP v3.0, Constitutional Classifiers. 단 Pentagon 분쟁(자율 타겟팅 거부)이 양날의 검 |
| 개발자 생태계 (MCP) | 보통→강함 | MCP가 업계 표준화되면 강력한 lock-in. 아직 진행 중 |
| 소비자 브랜드 | 약함 | ChatGPT 대비 인지도 낮음. claude.ai 트래픽 OpenAI 대비 1/5~1/10 |

### Moat 약점
1. **소비자 채널 부재** — 향후 광고 매출 진입 시 OpenAI·Google 대비 열위
2. **오픈소스 commoditization 위협** — Llama 5 (2026.04) 프론티어급 오픈웨이트 공개로 API 단가 압박
3. **자본 의존도** — 연간 burn $12~20B 추정. Amazon·Google 의존 심화 → 인수 시 PBC·LTBT 거버넌스 갈등 잠재
4. **정치 리스크 고도화** — 미 행정부와의 법적 분쟁(자율 타겟팅 거부)이 엔터프라이즈/정부 수주에 양면 영향

---

## 5. 핵심 발견 (v1 신규)

1. **PBC + LTBT 거버넌스가 IPO 시 최대 협상 변수** — 옛 분석(5/5)은 IPO 시기·밸류만 다뤘으나, LTBT 트러스티 통제권 유지/이양이 OpenAI 사태(2025 거버넌스 위기) 학습 효과로 핵심 이슈가 될 가능성.
2. **모델 라인업 v4.5 → v4.7 전환 완료** — KB 4/21 시점 Opus 4.5가 최상위였으나 5/13 기준 Opus 4.7 GA (사용자 시스템 컨텍스트 확인).
3. **MCP가 가장 저평가된 해자** — 옛 분석은 MCP를 "오픈소스 부수효과"로 다뤘으나, GitHub 60K stars + OpenAI·Google 부분 채택은 사실상 표준화 단계. 이는 Anthropic이 매출 없이도 생태계 lock-in을 가져가는 비대칭 자산.
4. **임직원 4배 확장** — 2024 말 500명 → 2026 Q1 1,800~2,000명. 인재 영입 속도 자체가 OpenAI·xAI 대비 우위.
5. **Big Six 계약 다변화** — 옛 분석은 AWS·GCP 양강만 다뤘으나, Snowflake·Harvey·Replit·JPMorgan·Cisco·Palo Alto 등 엔터프라이즈 채널 확장. 마켓플레이스 + Glasswing 으로 B2B 진입점 다각화.
