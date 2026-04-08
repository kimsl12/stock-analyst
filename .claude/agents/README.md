# 종목분석 AI 에이전트 v3.0 (브리핑 시스템 통합)

> 이 README는 `.claude/agents/` 디렉토리 안내용. 시스템 전체 README 는 저장소 루트의 `README.md` 참조.

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| **v3.0** | **2026-04-07** | **검수 결과 18 FAIL 정정 — 명세대로 5 브리핑 에이전트 + 10 명령 + KB 헤더 + performance KB 재구현 (PR #17 + hotfix)** |
| v2.4 | 2026-04-07 | 브리핑 시스템 v3.4 통합 1차 시도 (명세 미부합 — v3.0 으로 재구현됨) |
| v2.3 | 2026-04-06 | 데이터 흐름 전면 개편 + 차트 템플릿 + 해외 종목 지원 + 가격 검증 |
| v2.2 | 2026-04-05 | ETF 분석 + 모델 최적화 + 장애 대응 |
| v2.1 | 2026-04-05 | ATR 손절/목표가 + 가중 스코어카드 + 슬래시 명령어 |
| v2.0 | 2026-04-05 | 9개 에이전트 체계 + DART API |
| v1.0 | 2026-04-05 | 초기 6개 에이전트 |

---

## v3.0 핵심 — 두 개의 파이프라인

`stock-analyst-lead` 가 사용자 요청을 키워드로 자동 분기한다 (Step -1).

### 🅰️ 종목 분석 파이프라인
개별 종목·ETF 한 건 심층 분석 → HTML 리포트 생성. 매수·매도 추천 + 목표가/손절가 포함.

### 🅱️ 브리핑 파이프라인 (v3.0 신규)
글로벌 매크로·크로스에셋 브리핑 자동 생성. 매수·매도 추천 없이 **관찰·해석·시나리오만**.
10개 슬래시 명령으로 모듈별 실행. `briefing-lead` 가 오케스트레이터.

---

## 디렉토리 구조

```
.claude/agents/                                ← 16개 에이전트 (종목 9 + 리드 1 + 브리핑 5 + 공용 1)
├── README.md                                  ← 본 파일
│
├── stock-analyst-lead.md                      ← 양 파이프라인 분기 리드 (opus)
│
├── (종목 분석 9개)
│   ├── data-collector.md                      ← 종목 데이터 수집 전담 (sonnet, 검색12회)
│   ├── company-overview.md                    ← 기업개요+Moat (sonnet, 검색금지)
│   ├── financial-analyst.md                   ← 재무 심층 (opus, 검색금지)
│   ├── business-analyst.md                    ← 산업·경쟁 (sonnet, 검색금지)
│   ├── momentum-analyst.md                    ← 가격 모멘텀 (sonnet, 검색금지)
│   ├── risk-analyst.md                        ← Devil's advocate (sonnet, 검색금지)
│   ├── scorecard-strategist.md                ← 10항목 종합 평점 (opus, 검색금지)
│   ├── etf-analyst.md                         ← ETF 단독 분석 (opus, 검색5회)
│   └── report-generator.md                    ← HTML 리포트 (sonnet, 검색금지)
│
├── (브리핑 5개, v3.0 신규 — 사용자 결정으로 전부 Opus)
│   ├── briefing-lead.md                       ← 오케스트레이터 (opus) — 10 명령 진입점, debate/contrarian-card, 자동 commit/push
│   ├── market-data-collector.md               ← 시장 데이터 수집 (opus, 검색15~20회)
│   ├── global-macro-analyst.md                ← G-1~G-8 매크로 4축 (opus)
│   ├── correlation-monitor.md                 ← 6 페어 Z-score + 서프라이즈 (opus, 검색금지)
│   └── briefing-report-generator.md           ← HTML 다크 테마 리포트 (opus)
│
├── (공용 1개)
│   └── kb-updater.md                          ← KB macro/ + industry/ 갱신 (sonnet, 양쪽 파이프라인 사용)
│
└── (보조 1개, .md 문서)
    └── stop-loss-rules.md                     ← ATR 손절/목표가 SSOT
```

---

## 모델 배정 (v3.0)

| 에이전트 | 모델 | 웹검색 | 비고 |
|---|---|---|---|
| `stock-analyst-lead` | **opus** | 판단 | 양 파이프라인 분기 리드 |
| `data-collector` | sonnet | 12회 | 종목 데이터 수집 (KB market/ 읽기 v3.0) |
| `company-overview` | sonnet | 금지 | 기업개요 + Moat (KB market/ 읽기 v3.0) |
| `financial-analyst` | **opus** | 금지 | DCF 등 재무 심층 |
| `business-analyst` | sonnet | 금지 | 산업·경쟁 |
| `momentum-analyst` | sonnet | 금지 | 가격 모멘텀 |
| `risk-analyst` | sonnet | 금지 | Devil's advocate |
| `scorecard-strategist` | **opus** | 금지 | 10항목 종합 평점 |
| `etf-analyst` | **opus** | 5회 | ETF 단독 (KB market/ + industry/ 읽기 v3.0) |
| `report-generator` | sonnet | 금지 | HTML 리포트 |
| `briefing-lead` ⭐ | **opus** | 판단 | 브리핑 오케스트레이터 (v3.0 신규) |
| `market-data-collector` ⭐ | **opus** | 15~20회 | 시장 데이터 수집 (v3.0 신규) |
| `global-macro-analyst` ⭐ | **opus** | 1~5회 | G-1~G-8 4축 분석 (v3.0 신규) |
| `correlation-monitor` ⭐ | **opus** | 금지 | 6 페어 + 서프라이즈 (v3.0 신규) |
| `briefing-report-generator` ⭐ | **opus** | 금지 | HTML 다크 테마 (v3.0 신규) |
| `kb-updater` | sonnet | O | macro/ + industry/ 갱신 (양쪽 공용) |
| `stop-loss-rules` | (.md SSOT) | — | ATR 시스템 문서 |

> ⭐ = v3.0 신규. 명세는 mixed Opus/Sonnet 였으나 **사용자 결정으로 5개 모두 Opus 통일**.

---

## 슬래시 명령어 (총 16개)

### KB 갱신 (1개)

| 명령어 | 사용 예시 | 설명 |
|---|---|---|
| `/KB업데이트` | `/KB업데이트 quantum (양자컴퓨팅, 양자통신, PQC)` | 지정 섹터·토픽을 웹검색으로 갱신. `knowledge-db/ append + knowledge-base/ CURRENT 덮어쓰기`. 브리핑·종목분석과 독립. `agent: kb-updater` |

### 종목 분석 (5개)

| 명령어 | 사용 예시 | 설명 |
|---|---|---|
| `/종목분석` | `/종목분석 삼성전자`, `/종목분석 VOO` | 전체 분석 (개별 종목 / ETF 자동 판별) |
| `/비교분석` | `/비교분석 삼성전자 SK하이닉스` | 두 종목 비교 |
| `/빠른분석` | `/빠른분석 네이버` | 핵심 지표 + ATR (5분 이내) |
| `/손절계산` | `/손절계산 삼성전자 80000` | ATR 손절/목표 계산 |
| `/리포트` | `/리포트 삼성전자` | 기존 분석 → HTML 재생성 |

### 브리핑 (10개, v3.0)

| 명령어 | 모듈 | 산출물 |
|---|---|---|
| `/모닝브리핑` | 🌅 A | `morning_{YYYYMMDD}.html` |
| `/이브닝브리핑` | 🌙 B | `evening_{YYYYMMDD}.html` |
| `/주간리포트` | 📊 C (+ Phase 0-D 성과 추적) | `weekly_{YYYYMMDD}.html` |
| `/리밸런싱 [유형]` | 🔄 D | `rebalancing_{유형}_{YYYYMMDD}.html` |
| `/크립토브리핑` | 🪙 E | `crypto_{YYYYMMDD}.html` |
| `/모델포트폴리오` | 🧭 F | `model_portfolio_{YYYYMMDD}.html` |
| `/글로벌인텔리전스` | 🌐 G | `global_intelligence_{YYYYMMDD}.html` |
| `/풀브리핑` | A+B+C+E (4편) | 4개 HTML |
| `/성과리뷰 [기간]` | C-9 단독 (1w/2w/1m/3m) | `performance_review_{기간}_{YYYYMMDD}.html` |
| `/내포트폴리오` | 사용자 1인 개인 데이터 (격리) | `user_portfolio_{YYYYMMDD}.html` |

전부 `agent: briefing-lead` 진입점.

### 자연어 진입

```
삼성전자 분석해줘            → A 파이프라인
오늘 모닝 브리핑              → B 파이프라인 (briefing-lead)
글로벌 매크로 4축 분석해줘    → B 파이프라인 (briefing-lead → global-macro-analyst)
```

stock-analyst-lead.md 의 Step -1 에서 키워드 감지 → 자동 분기.

---

## 양방향 연계 (briefing ↔ 종목분석)

### 종목분석 → 브리핑
사용자가 자연어로 브리핑 요청 → `stock-analyst-lead` Step -1 → `briefing-lead` 위임

### 브리핑 → 종목분석
`briefing-lead` 산출물의 **"🔬 심층 분석 권장 종목"** 슬롯에 식별된 티커:
- 거물 컨버전스 시그널 (B-7, C-4)
- 신규 투자 아이디어 확신 강도 "높음" (B-6, E-5)
- 직전 적중률 ≥ 60% 종목·섹터 (knowledge-db/performance/2026_hit_rate.md)

→ 사용자가 후속으로 `/종목분석 {티커}` 실행 시 `stock-analyst-lead` 가 인계

---

## 종목 분석 흐름

### 개별 종목

```
Phase 0-A: kb-updater (섹터·매크로 KB 최신화)
    ↓
Phase 0-B: data-collector (웹검색 12회 → analysis/에 JSON, KB market/ 읽기 추가)
    ↓
Phase 1: company-overview + financial-analyst + momentum-analyst (병렬, 검색0)
    ↓
Phase 2: business-analyst + risk-analyst (순차, 검색0)
    ↓
Phase 3: scorecard-strategist (10항목 종합)
    ↓
Phase 4: report-generator (chart_templates.py → reports/에 HTML)
    ↓
Git: add reports/ → commit → pull --rebase → push
```

### ETF

```
Phase 0: data-collector → Phase 1: etf-analyst (단독, 검색5회) → Phase 2: report-generator
```

---

## 브리핑 흐름 (v3.0)

```
사용자 → /{모듈명} → briefing-lead (오케스트레이터)
   ↓
[Phase 0-A] market-data-collector (--skip-collect 시 생략)
   → knowledge-base/market/ + knowledge-db/market/ 연도별 .md
   ↓
[Phase 0-B] global-macro-analyst + correlation-monitor (병렬, mode 차)
   → analysis/briefing/{global_macro,correlation}_*.md
   ↓
[Phase 0-C] briefing-lead 종합 (직렬)
   - debate-card 1건 이상 (보라)
   - contrarian-card 1건 이상 (주황)
   - 4종 모델 포트폴리오 방향 (해당 모듈)
   - 13F 시차 경고 (거물 인용 시)
   - 🔬 심층 분석 권장 종목 슬롯 (양방향 연계)
   → analysis/briefing/lead_{type}_*.md
   - knowledge-db/performance/2026_recommendations.md append
   ↓
[Phase 0-D] briefing-report-generator
   → reports/briefing/{type}_*.html (다크 테마)
   ↓
[Phase 0-E] 자동 commit/push + 사용자 보고 (다운로드 가능 경로)
```

상세: `docs/briefing_pipeline.md`

---

## 차트 7종 (chart_templates.py — 종목 분석 전용)

| # | 차트 | 우선순위 |
|---|---|---|
| 1 | 가격 범위 바 (52주 내 손절-현재-목표) | 필수 |
| 2 | 스코어카드 레이더 (10항목) | 필수 |
| 3 | 실적 바차트 (매출/영업이익) | 권장 |
| 4 | 수익성 라인 (ROE/OPM) | 선택 |
| 5 | 리스크 히트맵 (확률×영향도) | 선택 |
| 6 | 섹터 도넛 (ETF) | ETF 필수 |
| 7 | 수익률 비교 (ETF vs 지수) | ETF 권장 |

브리핑 리포트는 별도 .py 파일 없이 `briefing-report-generator` 가 인라인 HTML/CSS 로 생성.

---

## ATR 손절/목표가 시스템 (종목 분석 전용)

- STEP 1: `initial_stop = MAX(고정비율 8%, ATR14 × 2)`
- STEP 2: 트레일링 전환 = +10% 도달 시
- STEP 3: `trailing_stop = 고점 - ATR×2` (래칫, 하향 금지)
- STEP 4: `target = entry + risk × 손익비(기본 2)`
- ETF: 패시브 5%, 레버리지 12%, 배당 손익비 1.5
- SSOT: `stop-loss-rules.md`

---

## 장애 대응 (Circuit Breaker)

| 상황 | 동작 |
|---|---|
| 서브에이전트 실패 | 1회 재시도 → 포기 → 리드 직접 수행 |
| 토큰 한도 | 전체 중단 → 수집 데이터로 축소 리포트 |
| 2개+ 연속 실패 | 사용자에게 현황 보고 + 선택지(A/B/C) |
| HTML 생성 실패 (종목) | 차트 없는 텍스트 HTML → .md만 저장 |
| Phase 0-A 실패 (브리핑) | 파이프라인 중단 → 전일 KB 진행 여부 확인 |
| Phase 0-B 일부 실패 (브리핑) | 해당 분석가만 1회 재호출 → 2회 연속 실패 시 중단 |
| Phase 0-D HTML 실패 (브리핑) | `analysis/briefing/lead_*.md` 보존 + 사용자에게 경고 + git/push 진행 |
| /풀브리핑 토큰 한도 | weekly → crypto → evening → morning 순서로 폴백 |

---

## DART API

- 인증키: `.claude/settings.json` (단일 위치 — `claude-settings.json` 중복은 v3.0 에서 제거)
- 일일 한도: 10,000건
- 해외 종목: Yahoo Finance / Investing.com / Macrotrends 로 대체
