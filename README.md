# 종목분석 AI 에이전트 v3.5

> 멀티에이전트 투자분석 시스템. Claude Code + 18개 에이전트 + 17개 슬래시 명령어.

## 리포트 열람

📘 **[리포트 목록 보기](https://kimsl12.github.io/stock-analyst/)**

최근 리포트:
- [LS ELECTRIC (010120)](https://kimsl12.github.io/stock-analyst/reports/010120_LSELECTRIC_20260413.html) — 2026-04-13
- [SanDisk (SNDK)](https://kimsl12.github.io/stock-analyst/reports/SNDK_Sandisk_20260413.html) — 2026-04-13
- [두산에너빌리티 (034020)](https://kimsl12.github.io/stock-analyst/reports/034020_두산에너빌리티_20260413.html) — 2026-04-13
- [SK하이닉스 (000660)](https://kimsl12.github.io/stock-analyst/reports/000660_SK하이닉스_20260410.html) — 2026-04-10
- [Anthropic (엔트로픽)](https://kimsl12.github.io/stock-analyst/reports/ANTHROPIC_Anthropic_20260409.html) — 2026-04-09

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| **v3.5** | **2026-04-13** | **session-bootstrap + KB 신뢰도 티어 + analysis 아카이브 + 에이전트 모순 해결 + 성과 공식 고정 + fetch_price.py 시장지수 + 서브에이전트 Write v3.0 + 브리핑 스캐폴딩** |
| v3.2 | 2026-04-13 | LLM Wiki 전환 — wiki-linter + KB 피드백 루프 + Phase 0-LINT |
| v3.1 | 2026-04-09 | GitHub Pages 자동 배포 + 비상장 기업 분석 |
| v3.0 | 2026-04-07 | 브리핑 파이프라인 5 에이전트 + 10 명령어 |
| v2.3 | 2026-04-06 | 데이터 흐름 개편 + 해외 종목 + 가격 검증 |
| v2.0 | 2026-04-05 | 9개 에이전트 체계 + DART API |

---

## v3.5 핵심 — 구조적 안정화

### 세션 연속성
- `session-bootstrap.md`: 매 세션 시작 시 Read → 마지막 작업/KB 상태/유효 파일 즉시 파악
- stock-analyst-lead가 매 작업 완료 후 자동 갱신

### 서브에이전트 Write 안정화 (v3.0)
- 시스템 오버라이드: analysis/ 폴더 .md Write는 시스템 규칙 예외로 명시
- 3턴 Write: Read→Read→Write 강제 순서
- 폴백 마커: Write 실패 시 ===ANALYSIS_START/END=== 반환

### KB 신뢰도 티어 분리
- Tier 1 (high): web_search, user → CURRENT 핵심 수치
- Tier 2 (medium): scorecard-feedback → "참고" 섹션만 (핵심 수치 승격 금지)

### 실시간 주가 수집
- `scripts/fetch_price.py`: pykrx(한국) + yfinance(미국)
- `--market` 모드: 18개 시장 지수 일괄 수집 + daily_snapshot.md 자동 갱신

---

## 두 개의 파이프라인

`stock-analyst-lead` 가 사용자 요청을 키워드로 자동 분기한다 (Step -2 부트스트랩 → Step -1 판별).

### 🅰️ 종목 분석 파이프라인
개별 종목·ETF 한 건 심층 분석 → HTML 리포트 생성. 매수·매도 추천 + 목표가/손절가 포함.

### 🅱️ 브리핑 파이프라인
글로벌 매크로·크로스에셋 브리핑 자동 생성. **신규 투자 아이디어 적극 제안** — 매크로 분석 기반
Bull/Bear 시나리오, 섹터·종목 아이디어, 진입 근거·리스크 병기.
슬래시 명령으로 모듈별 실행. `briefing-lead` 가 오케스트레이터.

---

## 디렉토리 구조

```
.claude/agents/                              ← 18개 에이전트
├── stock-analyst-lead.md                    ← 양 파이프라인 분기 리드 (opus)
│
├── (종목 분석 9개)
│   ├── data-collector.md                    ← 종목 데이터 수집 (sonnet)
│   ├── company-overview.md                  ← 기업개요+Moat (sonnet, maxTurns 15)
│   ├── financial-analyst.md                 ← 재무 심층 (sonnet, maxTurns 15) [v3.5 opus→sonnet]
│   ├── business-analyst.md                  ← 산업·경쟁 (sonnet, maxTurns 15)
│   ├── momentum-analyst.md                  ← 가격 모멘텀 (sonnet, maxTurns 15)
│   ├── risk-analyst.md                      ← Devil's advocate (sonnet, maxTurns 15)
│   ├── scorecard-strategist.md              ← 10항목 종합 + KB 피드백 + 모순 해결 (opus, maxTurns 20)
│   ├── etf-analyst.md                       ← ETF 단독 분석 (opus)
│   └── report-generator.md                  ← HTML 리포트 (sonnet)
│
├── (브리핑 5개)
│   ├── briefing-lead.md                     ← 오케스트레이터 (opus) + 스캐폴딩/검증
│   ├── market-data-collector.md             ← 시장 데이터 수집 (sonnet)
│   ├── global-macro-analyst.md              ← G-1~G-8 매크로 4축 (opus) [v3.5 Write 강화]
│   ├── correlation-monitor.md               ← 6 페어 Z-score (sonnet) [v3.5 Write 강화]
│   └── briefing-report-generator.md         ← HTML 다크 테마 (sonnet)
│
├── (공용 2개)
│   ├── kb-updater.md                        ← KB 갱신 (opus, v3.4 미니사이클)
│   └── wiki-linter.md                       ← KB 건강 점검 + README 갱신 (sonnet)
│
└── stop-loss-rules.md                       ← ATR 손절/목표가 SSOT

scripts/
├── fetch_price.py                           ← 실시간 주가 + 시장 지수 수집 [v3.5]
└── ...

session-bootstrap.md                         ← 세션 간 연속성 확보 [v3.5]
knowledge-base/_index.md                     ← KB 마스터 인덱스 (단일 SSOT)
```

---

## 모델 배정 (v3.5)

| 에이전트 | 모델 | maxTurns | 웹검색 | 비고 |
|---|---|---|---|---|
| `stock-analyst-lead` | **opus** | 40 | 판단 | 양 파이프라인 분기 + session-bootstrap |
| `data-collector` | sonnet | 25 | 12회 | 종목 데이터 수집 |
| `company-overview` | sonnet | **15** | 금지 | 기업개요 + Moat. v3.0 Write |
| `financial-analyst` | **sonnet** | **15** | 금지 | 재무 심층. **v3.5 opus→sonnet** |
| `business-analyst` | sonnet | **15** | 금지 | 산업·경쟁. 턴 절약 규칙 |
| `momentum-analyst` | sonnet | **15** | 금지 | 가격 모멘텀. v3.0 Write |
| `risk-analyst` | sonnet | **15** | 금지 | Devil's advocate. 턴 절약 규칙 |
| `scorecard-strategist` | **opus** | **20** | 금지 | 종합 + KB 루프 + **모순 해결 규칙** |
| `etf-analyst` | **opus** | 15 | 5회 | ETF 단독 분석 |
| `report-generator` | sonnet | — | 금지 | HTML 리포트 |
| `briefing-lead` | **opus** | — | 판단 | 브리핑 오케스트레이터 + **스캐폴딩/검증** |
| `market-data-collector` | sonnet | — | 15~20회 | 시장 데이터 수집 |
| `global-macro-analyst` | **opus** | 20 | 1~5회 | G-1~G-8. **v3.5 Write 강화** |
| `correlation-monitor` | sonnet | 15 | 금지 | 6 페어. **v3.5 Write 강화** |
| `briefing-report-generator` | sonnet | — | 금지 | HTML 다크 테마 |
| `kb-updater` | **opus** | **30** | O | KB 갱신. **v3.4 미니사이클** |
| `wiki-linter` | sonnet | 20 | 금지 | KB 점검 + **README 갱신** |

---

## 슬래시 명령어 (총 17개)

### KB 관리 (2개)

| 명령어 | 사용 예시 | 에이전트 | 설명 |
|---|---|---|---|
| `/KB업데이트` | `/KB업데이트 semiconductor` | kb-updater | 섹터·토픽 웹검색 갱신 (v3.4 미니사이클) |
| `/KB점검` | `/KB점검` | wiki-linter | P0~P2 탐지 + 자동 수정 + README 갱신 |

### 종목 분석 (5개)

| 명령어 | 사용 예시 | 설명 |
|---|---|---|
| `/종목분석` | `/종목분석 삼성전자`, `/종목분석 VOO` | 전체 분석 (개별 종목 / ETF 자동 판별) |
| `/비교분석` | `/비교분석 삼성전자 SK하이닉스` | 두 종목 비교 |
| `/빠른분석` | `/빠른분석 네이버` | 핵심 지표 + ATR (5분 이내) |
| `/손절계산` | `/손절계산 삼성전자 80000` | ATR 손절/목표 계산 |
| `/리포트` | `/리포트 삼성전자` | 기존 분석 → HTML 재생성 |

### 브리핑 (10개)

| 명령어 | 모듈 | 산출물 |
|---|---|---|
| `/모닝브리핑` | 🌅 A | `morning_{YYYYMMDD}.html` |
| `/이브닝브리핑` | 🌙 B | `evening_{YYYYMMDD}.html` |
| `/주간리포트` | 📊 C | `weekly_{YYYYMMDD}.html` |
| `/리밸런싱` | 🔄 D | `rebalancing_{유형}_{YYYYMMDD}.html` |
| `/크립토브리핑` | 🪙 E | `crypto_{YYYYMMDD}.html` |
| `/모델포트폴리오` | 🧭 F | `model_portfolio_{YYYYMMDD}.html` |
| `/글로벌인텔리전스` | 🌐 G | `global_intelligence_{YYYYMMDD}.html` |
| `/풀브리핑` | A+B+C+E | 4개 HTML |
| `/성과리뷰` | C-9 단독 | `performance_review_{기간}_{YYYYMMDD}.html` |
| `/내포트폴리오` | 개인 데이터 | `user_portfolio_{YYYYMMDD}.html` |

---

## 종목 분석 흐름

```
Phase 0-B: fetch_price.py (실시간 주가+ATR)
Phase 0-C: WebSearch (실적, 컨센서스, 뉴스)
Phase 0-D: 스캐폴딩 (빈 파일 사전 생성)
    ↓
Phase 1: company-overview + financial-analyst + momentum-analyst (병렬)
Phase 1-검증: 파일 크기 확인 → 0이면 폴백
    ↓
Phase 2: business-analyst + risk-analyst
    ↓
Phase 3: scorecard-strategist (10항목 + 모순 해결 + KB 피드백)
    ↓
Phase 4: report-generator → HTML → git push
```

## 브리핑 흐름

```
fetch_price.py --market --save (daily_snapshot 선행 갱신)
    ↓
[Phase 0-LINT] wiki-linter (quick)
    ↓
[Phase 0-A] market-data-collector → 스캐폴딩 (빈 파일 생성)
    ↓
[Phase 0-B] global-macro-analyst + correlation-monitor (병렬)
    → 검증: 파일 크기 확인 → 0이면 반환 메시지에서 추출
    ↓
[Phase 0-C] briefing-lead 종합 (debate/contrarian/포트폴리오)
    ↓
[Step 8.6] knowledge-base/_index.md 인사이트 append
    ↓
[Phase 0-D] briefing-report-generator → HTML → git push
```

---

## Knowledge Base 구조

```
knowledge-base/                  ← CURRENT만 (SSOT)
├── _index.md                    ← 마스터 인덱스 (단일 SSOT)
├── industry/                    ← 12개 섹터 KB
│   ├── semiconductor.md, ai.md, auto.md, energy.md, bio_pharma.md
│   ├── quantum.md, space.md, smr.md                    [v3.5 신규]
│   ├── telecom_next.md, banking_capital.md              [v3.5 신규]
│   ├── advanced_materials.md, battery.md                [v3.5 신규]
│   └── infrastructure.md                                [v3.5 신규]
├── macro/                       ← 7개 매크로 KB
│   ├── us_economy.md, us_monetary_policy.md (SSOT)
│   ├── korea_economy.md, geopolitics.md, global_risk_factors.md
│   └── political_cycle.md, tech_breakthrough.md, supply_chain.md  [v3.5 신규]
├── market/                      ← 5개 시장 데이터
│   ├── daily_snapshot.md        ← fetch_price.py --market --save로 갱신
│   └── economic_calendar.md, correlation_matrix.md, guru_positions.md, surprise_index.md
└── portfolio/                   ← 개인 데이터
    ├── model_portfolios.md
    └── user_portfolio.md        ← 등록 완료 (중립형, VOO 83%)

knowledge-db/                    ← 영구 축적 (append-only)
├── semiconductor_2026.jsonl (71행), ai_2026.jsonl (88행)
├── science_tech_2026.jsonl (143행) — quantum/space/smr subtag
├── banking_capital_2026.jsonl (38행), telecom_next_2026.jsonl (28행)
├── battery_2026.jsonl (40행), advanced_materials_2026.jsonl (35행)
├── infrastructure_2026.jsonl (23행), macro_2026.jsonl (133행)
└── changelog_2026.jsonl
```

---

## ATR 손절/목표가 시스템

- STEP 1: `initial_stop = MAX(고정비율 8%, ATR14 × 2)`
- STEP 2: 트레일링 전환 = +10% 도달 시
- STEP 3: `trailing_stop = 고점 - ATR×2` (래칫, 하향 금지)
- STEP 4: `target = entry + risk × 손익비(기본 2)`
- SSOT: `stop-loss-rules.md`

---

## 데이터 검증

- `reference/data-collector/validation_rules.md` — 가격 8규칙 + 컨센서스 4규칙 + 소스 품질 3규칙(O1/O2/O3)
- O1: 소스 독립성 (동일 통신사발이면 3번째 소스 필수)
- O2: 1차 소스 우선 (IR/DART/Fed 원문 소급)
- O3: 발표·보도 주체 분리 표기

---

## DART API

- 인증키: `.claude/settings.json`
- 일일 한도: 10,000건
- 해외 종목: Yahoo Finance / Investing.com / `fetch_price.py`

---

## GitHub Pages 배포

- **URL**: `https://kimsl12.github.io/stock-analyst/reports/{파일명}.html`
- **GitHub Actions**: `.github/workflows/deploy-reports.yml`
- **레이아웃**: 2컬럼 (좌: 종목분석 / 우: 브리핑)
