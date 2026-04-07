# 종목분석 AI 에이전트 v3.0 (브리핑 시스템 통합)

Claude Code 기반 한국·해외 주식/ETF 분석 + 글로벌 매크로·크로스에셋 브리핑 통합 시스템.

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| **v3.0** | **2026-04-07** | **검수 결과 18개 FAIL 정정 — 명세(claude_code_instructions.md)대로 5 에이전트 + 10 명령 + KB 헤더 + performance KB 재구현. fix/audit-2026-04-07-v2 브랜치 적용.** |
| v2.4 | 2026-04-07 | 브리핑 시스템 v3.4 통합 (1차 시도, 명세 미부합 — v3.0 으로 재구현됨) |
| v2.3 | 2026-04-06 | 데이터 흐름 전면 개편 + 차트 템플릿 + 해외 종목 지원 + 가격 검증 |
| v2.2 | 2026-04-05 | ETF 분석 + 모델 최적화 + 장애 대응 |
| v2.1 | 2026-04-05 | ATR 손절/목표가 + 가중 스코어카드 + 슬래시 명령어 |
| v2.0 | 2026-04-05 | 9개 에이전트 체계 + DART API |
| v1.0 | 2026-04-05 | 초기 6개 에이전트 |

---

## v3.0 핵심 — 두 개의 파이프라인

시스템은 **두 개의 독립 파이프라인**을 병행한다. `stock-analyst-lead` 가 요청을 키워드로 자동 분기한다.

### 🅰️ 종목 분석 파이프라인 (기존 유지)
개별 종목·ETF 한 건 심층 분석 → HTML 리포트 생성. 매수·매도 추천 + 목표가/손절가 포함.

### 🅱️ 브리핑 파이프라인 (v3.0 명세 재구현)
시장·매크로·상관관계 3개 레이어를 통합한 **글로벌 매크로·크로스에셋 브리핑** 자동 생성.
매수·매도 추천 없이 **관찰·해석·시나리오만**. 10개 슬래시 명령으로 모듈별 실행.

---

## 주요 명령어 (총 15개)

### 종목 분석 (5개)

| 명령어 | 용도 | 파이프라인 |
|---|---|---|
| `/종목분석 삼성전자` | 전체 분석 (개별 종목 자동 판별) | A |
| `/종목분석 VOO` | 전체 분석 (ETF 자동 판별) | A |
| `/비교분석 삼성전자 SK하이닉스` | 두 종목 비교 | A |
| `/빠른분석 네이버` | 핵심 지표 + ATR (5분 이내) | A |
| `/손절계산 삼성전자 80000` | ATR 손절/목표 계산 | A |
| `/리포트 삼성전자` | 기존 분석 → HTML 재생성 | A |

### 브리핑 (10개, v3.0)

| 명령어 | 모듈 | 산출물 |
|---|---|---|
| `/모닝브리핑` | 🌅 A — 어젯밤 미국장 + 거물 + 매크로 + 4종 방향 | `morning_{YYYYMMDD}.html` |
| `/이브닝브리핑` | 🌙 B — 글로벌 이슈 + 서프라이즈 + 상관관계 + 거물 심화 | `evening_{YYYYMMDD}.html` |
| `/주간리포트` | 📊 C — 한 주 심층 + Phase 0-D 성과 추적 | `weekly_{YYYYMMDD}.html` |
| `/리밸런싱 [유형]` | 🔄 D — 4종 모델 포트폴리오 재조정 | `rebalancing_{유형}_{YYYYMMDD}.html` |
| `/크립토브리핑` | 🪙 E — BTC/ETH/SOL + 온체인 + 규제 | `crypto_{YYYYMMDD}.html` |
| `/모델포트폴리오` | 🧭 F — 4종 현재 구성 + 웹 서치 종목/ETF | `model_portfolio_{YYYYMMDD}.html` |
| `/글로벌인텔리전스` | 🌐 G — 4축 교차 + 시나리오 플래닝 | `global_intelligence_{YYYYMMDD}.html` |
| `/풀브리핑` | 📘 A+B+C+E 4편 동시 (F·G 미포함) | 4개 HTML |
| `/성과리뷰 [기간]` | 📈 C-9 단독 — 1w/2w/1m/3m 적중률 | `performance_review_{기간}_{YYYYMMDD}.html` |
| `/내포트폴리오 [--view]` | 👤 사용자 1인 개인 데이터 (격리) | `user_portfolio_{YYYYMMDD}.html` |

**자연어 진입**도 지원: "삼성전자 분석해줘" → A. "오늘 모닝 브리핑" → B (stock-analyst-lead Step -1 분기).

---

## 에이전트 체계 (16개 — 종목 9 + 브리핑 5 + 공용 1 + 보조 1)

### 종목 분석 전용 (9개)

| 역할 | 모델 | 웹검색 | 비고 |
|---|---|---|---|
| `stock-analyst-lead` | opus | 판단 | 리드 — 양 파이프라인 분기 (Step -1) |
| `data-collector` | sonnet | 12회 | 종목 데이터 수집 전담 (KB market/ 읽기 v3.0 추가) |
| `company-overview` | sonnet | 금지 | 기업개요 + Moat (KB market/ 읽기 v3.0 추가) |
| `financial-analyst` | opus | 금지 | DCF 등 재무 심층 (KB market/ 읽기 v3.0 추가) |
| `business-analyst` | sonnet | 금지 | 산업·경쟁 분석 (KB market/ 읽기 v3.0 추가) |
| `momentum-analyst` | sonnet | 금지 | 가격 모멘텀 (KB market/ 읽기 v3.0 추가) |
| `risk-analyst` | sonnet | 금지 | Devil's advocate (KB market/ 읽기 v3.0 추가) |
| `scorecard-strategist` | opus | 금지 | 10항목 종합 평점 (KB market/ 읽기 v3.0 추가) |
| `etf-analyst` | opus | 5회 | ETF 단독 분석 (KB market/ 읽기 v3.0 추가) |
| `report-generator` | sonnet | 금지 | HTML 리포트 (KB market/ 읽기 v3.0 추가) |

> 정확히는 위 표에 10개 에이전트가 나열돼 있으나, "종목 분석가"는 stock-analyst-lead 를 제외한 9개로 카운트하는 것이 명세 기준 일관됨 (검수 결과 F-14, F-18).

### 브리핑 전용 (5개, v3.0 명세)

| 역할 | 모델 | 웹검색 | 산출물 |
|---|---|---|---|
| `briefing-lead` | **opus** | 판단 | 오케스트레이터 — 10 명령 진입점, debate/contrarian-card, 자동 commit/push |
| `market-data-collector` | **opus** | O (15~20회) | `knowledge-base/market/` 5개 + `knowledge-db/market/` 4개 연도별 .md |
| `global-macro-analyst` | **opus** | O (1~5회) | `analysis/briefing/global_macro_*.md` (G-1 ~ G-8) |
| `correlation-monitor` | **opus** | 금지 (KB market/ 만) | `knowledge-base/market/{correlation_matrix,surprise_index}.md` |
| `briefing-report-generator` | **opus** | 금지 | `reports/briefing/{type}_*.html` (다크 테마 + debate/contrarian-card) |

> v3.0 결정: 명세는 mixed Opus/Sonnet 였으나 **사용자 결정으로 5개 모두 Opus 통일**.

### 공용 (1개)

| 역할 | 모델 | 웹검색 | 비고 |
|---|---|---|---|
| `kb-updater` | sonnet | O | `knowledge-base/macro/` + `industry/` 갱신 — 양쪽 파이프라인에서 사용 |

### 보조 (1개)

| 역할 | 비고 |
|---|---|
| `stop-loss-rules` | ATR 손절/목표가 SSOT (.md 파일, 에이전트 호출은 아님) |

---

## 디렉토리 구조

```
stock-analyst/
├── .claude/
│   ├── settings.json                      ← DART API 키 (claude-settings.json 중복 정리됨)
│   ├── agents/                            ← 에이전트 16개
│   │   ├── stock-analyst-lead.md          ← 리드 (opus)
│   │   ├── (종목 9개)
│   │   ├── briefing-lead.md               ← 브리핑 오케스트레이터 (opus, v3.0)
│   │   ├── market-data-collector.md       ← (opus, v3.0)
│   │   ├── global-macro-analyst.md        ← (opus, v3.0)
│   │   ├── correlation-monitor.md         ← (opus, v3.0)
│   │   ├── briefing-report-generator.md   ← (opus, v3.0)
│   │   ├── kb-updater.md                  ← 공용
│   │   └── stop-loss-rules.md             ← 보조 (SSOT 문서)
│   └── commands/                          ← 슬래시 명령 15개 (종목 5 + 브리핑 10)
│
├── knowledge-base/                        ← 정제된 지식베이스 (Git 추적, CURRENT)
│   ├── _index.md
│   ├── market/                            ← 5개 (일일/주간 갱신)
│   ├── macro/                             ← 8개 (주간 갱신)
│   ├── industry/                          ← 섹터별
│   └── portfolio/                         ← 3개 (briefing-lead 쓰기)
│
├── knowledge-db/                          ← raw 축적 (Git 추적, append-only)
│   ├── market/                            ← 연도별 .md (2026_daily_prices, _economic_indicators, _guru_changes, _correlation_log)
│   ├── macro_2026.jsonl                   ← kb-updater
│   ├── industry/                          ← 섹터별
│   └── performance/                       ← 3개 (briefing-lead append)
│       ├── 2026_recommendations.md
│       ├── 2026_scenario_tracking.md
│       └── 2026_hit_rate.md
│
├── reference/                             ← 정적 참조 (변경 드뭄)
│   ├── source_registry.md                 ← 37개 데이터 소스 + 등급
│   ├── rules_and_constraints.md           ← 금지사항 31개 (#30·#33 삭제 사유 기재)
│   └── guru_watchlist.md                  ← 거물 8인 (Cathie Wood 4번, Seth Klarman 미포함)
│
├── analysis/                              ← 중간 작업 (Git 미포함, 대부분)
│   └── briefing/                          ← 분석가 산출물 (briefing-lead 종합 노트는 Git 추적)
│
├── reports/                               ← 최종 리포트 (Git 추적)
│   ├── {종목코드}_{종목명}_{YYYYMMDD}.html  ← 종목 분석
│   └── briefing/{type}_{YYYYMMDD}.html     ← 브리핑 (다크 테마)
│
├── docs/briefing_pipeline.md              ← v3.0 파이프라인 명세 (S5 재작성)
├── chart_templates.py                     ← 차트 7종 템플릿 (종목 분석용)
├── report_template.py                     ← HTML 리포트 (종목 분석용, v3.0)
└── README.md                              ← 본 파일
```

---

## 종목 분석 흐름 (Workflow A)

```
Phase 0-A: kb-updater (섹터·매크로 KB 최신화, 필요 시)
    ↓
Phase 0-B: data-collector (웹검색 12회 → analysis/에 JSON)
    ↓ 파일 전달
Phase 1: company-overview + financial-analyst + momentum-analyst (병렬, 검색0)
    ↓
Phase 2: business-analyst + risk-analyst (순차, 검색0)
    ↓
Phase 3: scorecard-strategist (10항목 종합, 검색0)
    ↓
Phase 4: report-generator (chart_templates.py → reports/에 HTML)
    ↓
Git: add reports/ → commit → pull --rebase → push
```

### ETF 흐름
```
Phase 0: data-collector → Phase 1: etf-analyst (단독, 검색5회) → Phase 2: report-generator
```

---

## 브리핑 흐름 (Workflow B — v3.0)

```
사용자 → /{모듈명} → briefing-lead (오케스트레이터)
   │
   ▼
[Phase 0-A] market-data-collector (직렬, --skip-collect 시 생략)
   → knowledge-base/market/ + knowledge-db/market/ 연도별 .md
   ▼
[Phase 0-B] global-macro-analyst + correlation-monitor (병렬, mode 차)
   → analysis/briefing/{global_macro,correlation}_*.md
   ▼
[Phase 0-C] briefing-lead 종합 (직렬)
   - debate-card 1건 이상 (보라)
   - contrarian-card 1건 이상 (주황)
   - 4종 모델 포트폴리오 방향 (해당 모듈)
   - 13F 시차 경고 (거물 인용 시)
   - 심층 분석 권장 종목 (양방향 연계)
   → analysis/briefing/lead_{type}_*.md
   - knowledge-db/performance/2026_recommendations.md append
   - (해당 모듈) knowledge-base/portfolio/ 갱신
   ▼
[Phase 0-D] briefing-report-generator
   → reports/briefing/{type}_*.html (다크 테마 + 시각화 + 푸터 + disclaimer)
   ▼
[Phase 0-E] 자동 commit/push + 사용자 보고 (다운로드 가능 경로)
```

### 접근 권한 원칙

| 에이전트 | KB market/ | KB macro/ | KB portfolio/ | knowledge-db/ |
|---|---|---|---|---|
| market-data-collector | ✅쓰기 | ✅읽기 | ❌ | ✅쓰기 (market/) |
| correlation-monitor | ✅쓰기 | ❌ | ❌ | ✅읽기+쓰기 (market/) |
| global-macro-analyst | ✅읽기 | ✅읽기 | ❌ | ❌ |
| briefing-lead | ✅읽기 | ✅읽기 | ✅읽기+쓰기 | ✅쓰기 (performance/) |
| briefing-report-generator | ✅읽기 | ❌ | ✅읽기 | ❌ |
| 종목분석 9개 (v3.0) | ✅읽기 | (기존) | ❌ | (기존) |

상세: `docs/briefing_pipeline.md §3`

### 절대 금지 사항 (브리핑 핵심 13종)
1. 매수·매도·익절·손절·비중조정·목표주가 표현
2. `knowledge-base/portfolio/user_portfolio.md` HTML 평문 노출
3. `knowledge-base/industry/` 를 브리핑 분석가가 직접 읽기
4. `analysis/briefing/` 의 다른 분석가 산출물을 분석가끼리 읽기 (briefing-lead 만 통합)
5. debate-card 또는 contrarian-card 누락 (각 1건 이상)
6. 13F 시차(≤45일) 고지 누락
7. 영어 본문
8. 분석가가 작성하지 않은 새 사실·수치를 briefing-lead 가 추가
9. `analysis/{종목}_*.md` 를 브리핑 파이프라인에서 생성·읽기
10. main 외 브랜치로 push
11. 1차 효과만 분석하고 멈추기 (G-6 강제 2·3차 효과)
12. 기술을 단계 판정 없이 나열 (G-3 🔬→🧪→🏭→🌍 강제)
13. `knowledge-db/` 의 performance/ 외 폴더에 briefing-lead 가 쓰기

총 31개 금지 조항: `reference/rules_and_constraints.md`. 본 표는 브리핑 핵심만 추림.

---

## ATR 손절/목표가 시스템 (종목 분석 전용)

- STEP 1: `initial_stop = MAX(고정비율 8%, ATR14 × 2)`
- STEP 2: 트레일링 전환 = +10% 도달 시
- STEP 3: `trailing_stop = 고점 - ATR×2` (래칫, 하향 금지)
- STEP 4: `target = entry + risk × 손익비(기본 2)`
- ETF: 패시브 5%, 레버리지 12%, 배당 손익비 1.5
- SSOT: `.claude/agents/stop-loss-rules.md`

## 차트 7종 (`chart_templates.py`, 종목 분석 전용)

| # | 차트 | 우선순위 |
|---|---|---|
| 1 | 가격 범위 바 (52주 내 손절-현재-목표) | 필수 |
| 2 | 스코어카드 레이더 (10항목) | 필수 |
| 3 | 실적 바차트 (매출/영업이익) | 권장 |
| 4 | 수익성 라인 (ROE/OPM) | 선택 |
| 5 | 리스크 히트맵 (확률×영향도) | 선택 |
| 6 | 섹터 도넛 (ETF) | ETF 필수 |
| 7 | 수익률 비교 (ETF vs 지수) | ETF 권장 |

브리핑 리포트는 별도 .py 파일 없이 `briefing-report-generator` 에이전트가 인라인 HTML/CSS 로 생성.

## 장애 대응 (Circuit Breaker)

| 상황 | 동작 |
|---|---|
| 서브에이전트 실패 | 1회 재시도 → 포기 → 리드 직접 수행 |
| 토큰 한도 | 전체 중단 → 수집 데이터로 축소 리포트 |
| Phase 0-A 실패 (브리핑) | 파이프라인 중단 → 전일 KB 진행 여부 확인 |
| Phase 0-B 일부 실패 (브리핑) | 해당 분석가만 1회 재호출 → 2회 연속 실패 시 중단 |
| Phase 0-D HTML 실패 | `analysis/briefing/lead_*.md` 보존 + 사용자에게 경고 + git/push 진행 |
| /풀브리핑 토큰 한도 | weekly → crypto → evening → morning 순서로 폴백 |

## DART API

- 인증키: `.claude/settings.json` (단일 위치 — `claude-settings.json` 중복 v3.0 제거)
- 일일 한도: 10,000건
- 해외 종목: Yahoo Finance / Investing.com / Macrotrends 로 대체

---

## 참고 문서

- **`docs/briefing_pipeline.md`** — v3.0 브리핑 파이프라인 전체 명세 (S5 재작성)
- **`knowledge-base/_index.md`** — KB 전체 인덱스
- **`reference/source_registry.md`** — 37개 데이터 소스 + 등급 🟢🟡🔴
- **`reference/rules_and_constraints.md`** — 금지사항 31개
- **`reference/guru_watchlist.md`** — 거물 투자자 8인 (Cathie Wood 4번)
- **`knowledge-db/performance/`** — 성과 추적 시스템 (recommendations + scenario_tracking + hit_rate)

---

## 빠른 시작

```bash
# 종목 분석
/종목분석 삼성전자

# 모닝 브리핑
/모닝브리핑

# 풀 브리핑 (4편 동시)
/풀브리핑

# 글로벌 매크로 4축 분석
/글로벌인텔리전스

# 성과 리뷰 (1개월 적중률)
/성과리뷰 1m
```

---

## v3.0 변경 요약 (검수 결과 18 FAIL 정정)

| 카테고리 | v2.4 | v3.0 | 변경 |
|---|---|---|---|
| 브리핑 에이전트 | 6개 (잘못된 명칭) | **5개 (명세)** | market-analyst, macro-analyst, guru-analyst, briefing-synthesizer 삭제 → briefing-lead, global-macro-analyst, correlation-monitor, briefing-report-generator 신규 + market-data-collector 명세 기준 재작성 |
| 브리핑 명령어 | 1개 (`/일일브리핑`) | **10개 (명세)** | /일일브리핑 삭제 → 10개 신규 |
| KB 헤더 권한 | 부재 또는 잘못된 에이전트 참조 | 명세 매트릭스 정합 | 13개 KB 파일 헤더 권한 정정 |
| performance KB | 부재 | 3파일 신규 | recommendations + scenario_tracking + hit_rate |
| jsonl 패턴 | snapshots_2026.jsonl (불일치) | 2026_*.md (연도별) | 4파일 일관 |
| 거물 8인 명단 | Seth Klarman 포함 (불일치) | Cathie Wood 4번 (정합) | 3 파일 통일 |
| 종목분석가 9개 market/ 권한 | 미명시 | "✅ 읽기 가능" 1줄 명시 | 9파일 |
| report_template.py | v2.3 표기 | v3.0 | 1줄 |
| settings.json 중복 | claude-settings.json 별도 존재 | 단일 (.claude/settings.json) | 중복 제거 |
| docs/briefing_pipeline.md | briefing-synthesizer 중심 | 5 명세 에이전트 + 연도별 | 전체 재작성 |
| README | v2.4 표기 | v3.0 + 16 에이전트 + 15 명령 | 본 파일 |
