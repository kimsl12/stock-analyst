# 종목분석 AI 에이전트 v2.4 (브리핑 통합)

Claude Code 기반 한국·해외 주식/ETF 분석 + 일일 시장 브리핑 통합 시스템.

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| **v2.4** | **2026-04-07** | **브리핑 시스템 v3.4 통합 — /일일브리핑 명령어 + 신규 에이전트 6개 + KB 확장** |
| v2.3 | 2026-04-06 | 데이터 흐름 전면 개편 + 차트 템플릿 + 해외 종목 지원 + 가격 검증 |
| v2.2 | 2026-04-05 | ETF 분석 + 모델 최적화 (Opus 4 + Sonnet 6) + 장애 대응 |
| v2.1 | 2026-04-05 | ATR 손절/목표가 + 가중 스코어카드 + 슬래시 명령어 |
| v2.0 | 2026-04-05 | 9개 에이전트 체계 + DART API |
| v1.0 | 2026-04-05 | 초기 6개 에이전트 |

---

## v2.4 핵심 — 두 개의 파이프라인

시스템은 이제 **두 개의 독립 파이프라인**을 병행한다. `stock-analyst-lead` 가 요청을 키워드로 자동 분기한다.

### 🅰️ 종목 분석 파이프라인 (기존 v2.3, 유지)
개별 종목·ETF 한 건 심층 분석 → HTML 리포트 생성.

### 🅱️ 일일 브리핑 파이프라인 (v3.4 신규 통합)
시장·매크로·거물 3개 레이어를 통합한 **일일 모닝 브리핑** 자동 생성.
매수·매도 추천 없이 **관찰·해석만**.

---

## 주요 명령어

| 명령어 | 용도 | 파이프라인 |
|---|---|---|
| `/종목분석 삼성전자` | 전체 분석 (개별 종목 자동 판별) | A |
| `/종목분석 VOO` | 전체 분석 (ETF 자동 판별) | A |
| `/비교분석 삼성전자 SK하이닉스` | 두 종목 비교 | A |
| `/빠른분석 네이버` | 핵심 지표 + ATR (5분 이내) | A |
| `/손절계산 삼성전자 80000` | ATR 손절/목표 계산 | A |
| `/리포트 삼성전자` | 기존 분석 → HTML 재생성 | A |
| **`/일일브리핑`** | **오늘(KST) 시장·매크로·거물 통합 브리핑** | **B** |
| `/일일브리핑 20260407` | 특정일 브리핑 | B |
| `/일일브리핑 --skip-collect` | 시장 수집 생략 (KB 최신 시) | B |
| `/일일브리핑 --skip-kb` | 매크로 KB 갱신 생략 | B |

**자연어 진입**도 지원: "삼성전자 분석해줘" → A. "오늘 일일 브리핑" → B.

---

## 에이전트 체계 (16개)

### 종목 분석 전용 (10개)

| 역할 | 모델 | 웹검색 | 비고 |
|---|---|---|---|
| `stock-analyst-lead` | opus | 판단 | 리드 — 양 파이프라인 분기 |
| `data-collector` | sonnet | 12회 | 종목 데이터 수집 전담 |
| `company-overview` | sonnet | 금지 | 기업개요 + Moat |
| `financial-analyst` | opus | 금지 | DCF 등 재무 심층 |
| `business-analyst` | sonnet | 금지 | 산업·경쟁 분석 |
| `momentum-analyst` | sonnet | 금지 | 가격 모멘텀 |
| `risk-analyst` | sonnet | 금지 | Devil's advocate |
| `scorecard-strategist` | opus | 금지 | 10항목 종합 평점 |
| `etf-analyst` | opus | 5회 | ETF 단독 분석 |
| `report-generator` | sonnet | 금지 | HTML 리포트 |

### 브리핑 전용 (6개, v2.4 신규)

| 역할 | 모델 | 웹검색 | 산출물 |
|---|---|---|---|
| `market-data-collector` | sonnet | MCP | `knowledge-base/market/` 5개 갱신 |
| `kb-updater` | sonnet | O | `knowledge-base/macro/`·`industry/` 갱신 |
| `market-analyst` | sonnet | 금지 | `analysis/briefing/market_analysis_*.md` |
| `macro-analyst` | sonnet | 금지 | `analysis/briefing/macro_analysis_*.md` |
| `guru-analyst` | sonnet | 금지 | `analysis/briefing/guru_analysis_*.md` |
| `briefing-synthesizer` | sonnet | 금지 | `reports/briefing/daily_briefing_*.md` (최종) |

`kb-updater` 는 **양쪽 파이프라인 공용** (종목 분석 Phase 0-A 에서도 호출).

---

## 디렉토리 구조

```
stock-analyst/
├── .claude/
│   ├── settings.json                  ← DART API 키
│   ├── agents/                        ← 에이전트 16개
│   │   ├── stock-analyst-lead.md      ← 리드 (opus, 양쪽 분기)
│   │   ├── (종목 분석 9개)
│   │   └── (브리핑 6개 — v2.4 신규)
│   └── commands/                      ← 슬래시 명령어 6개
│       ├── 종목분석.md / 비교분석.md / 빠른분석.md
│       ├── 손절계산.md / 리포트.md
│       └── 일일브리핑.md               ← v2.4 신규
│
├── knowledge-base/                    ← 정제된 지식베이스 (Git 추적)
│   ├── _index.md                      ← KB 전체 인덱스
│   ├── market/                        ← v2.4 신규: 5개 (일일 갱신)
│   ├── macro/                         ← 매크로 8개
│   ├── industry/                      ← 섹터별 KB
│   └── portfolio/                     ← v2.4 신규: 3개
│
├── knowledge-db/                      ← raw 축적 (Git 미포함, jsonl)
│
├── reference/                         ← v2.4 신규: 정적 참조
│   ├── source_registry.md             ← 37개 데이터 소스 + 등급
│   ├── rules_and_constraints.md       ← 금지사항 31개
│   └── guru_watchlist.md              ← 거물 투자자 8인
│
├── analysis/                          ← 중간 작업 (Git 미포함)
│   └── briefing/                      ← v2.4: 3분석가 산출물
│
├── reports/                           ← 최종 리포트 (Git 포함)
│   ├── {종목코드}_{종목명}_{YYYYMMDD}.md / .html
│   └── briefing/                      ← v2.4: 일일 브리핑
│
├── docs/briefing_pipeline.md          ← v2.4: 파이프라인 명세
├── chart_templates.py                 ← 차트 7종 템플릿
└── README.md
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

## 일일 브리핑 흐름 (Workflow B — /일일브리핑)

```
[Phase 0-A] 데이터 수집 (직렬)
   ① market-data-collector  → knowledge-base/market/ 5개
   ② kb-updater              → knowledge-base/macro/ + industry/

[Phase 0-B] 분석 (병렬 3개)
   ③a market-analyst → analysis/briefing/market_analysis_{YYYYMMDD}.md
   ③b macro-analyst  → analysis/briefing/macro_analysis_{YYYYMMDD}.md
   ③c guru-analyst   → analysis/briefing/guru_analysis_{YYYYMMDD}.md

[Phase 0-C] 통합 (직렬)
   ④ briefing-synthesizer → reports/briefing/daily_briefing_{YYYYMMDD}.md
```

### 접근 권한 원칙
- 각 분석가는 **자기 영역만** 읽기·쓰기 (데이터 역류 차단)
- `briefing-synthesizer` 만이 analysis/briefing/ 3개 산출물 **동시 읽기** 허용 (단일 통합 게이트웨이)
- `knowledge-base/portfolio/` 는 브리핑 파이프라인 **전원 접근 금지**
- 상세: `docs/briefing_pipeline.md §3`

### 금지사항 10종 (브리핑)
1. 매수·매도·익절·손절·비중조정·목표주가 표현
2. `knowledge-base/portfolio/` 직접 읽기
3. `knowledge-base/industry/` 를 브리핑 분석가가 직접 읽기
4. `analysis/briefing/` 의 다른 분석가 산출물을 분석가끼리 읽기
5. Top 3 액션 아이템 ≠ 정확히 3개
6. 13F 시차(≤45일) 고지 누락
7. 영어 본문 작성
8. 새로운 사실·수치를 synthesizer 가 추가 (인용 무결성)
9. `analysis/{종목}_*.md` 를 브리핑 파이프라인에서 생성·읽기
10. 미검증 산출물 외부 공개

상세: `docs/briefing_pipeline.md §6`

---

## ATR 손절/목표가 시스템

- STEP 1: `initial_stop = MAX(고정비율 8%, ATR14 × 2)`
- STEP 2: 트레일링 전환 = +10% 도달 시
- STEP 3: `trailing_stop = 고점 - ATR×2` (래칫, 하향 금지)
- STEP 4: `target = entry + risk × 손익비(기본 2)`
- ETF: 패시브 5%, 레버리지 12%, 배당 손익비 1.5
- SSOT: `.claude/agents/stop-loss-rules.md`

## 차트 7종 (`chart_templates.py`)

| # | 차트 | 우선순위 |
|---|---|---|
| 1 | 가격 범위 바 (52주 내 손절-현재-목표) | 필수 |
| 2 | 스코어카드 레이더 (10항목) | 필수 |
| 3 | 실적 바차트 (매출/영업이익) | 권장 |
| 4 | 수익성 라인 (ROE/OPM) | 선택 |
| 5 | 리스크 히트맵 (확률×영향도) | 선택 |
| 6 | 섹터 도넛 (ETF) | ETF 필수 |
| 7 | 수익률 비교 (ETF vs 지수) | ETF 권장 |

## 장애 대응 (Circuit Breaker)

| 상황 | 동작 |
|---|---|
| 서브에이전트 실패 | 1회 재시도 → 포기 → 리드 직접 수행 |
| 토큰 한도 | 전체 중단 → 수집 데이터로 축소 리포트 |
| 2개+ 연속 실패 | 사용자에게 현황 보고 + 선택지(A/B/C) |
| HTML 생성 실패 | 차트 없는 텍스트 HTML → .md만 저장 |
| Phase 0-A 실패 (브리핑) | 파이프라인 중단 → 전일 KB 로 진행 여부 확인 |
| Phase 0-B 일부 실패 (브리핑) | 해당 분석가만 1회 재호출 → 2회 연속 실패 시 중단 |

## DART API

- 인증키: `.claude/settings.json`
- 일일 한도: 10,000건
- 해외 종목: Yahoo Finance / Investing.com / Macrotrends 로 대체

---

## 참고 문서

- **`docs/briefing_pipeline.md`** — v2.4 브리핑 파이프라인 전체 명세
- **`knowledge-base/_index.md`** — KB 전체 인덱스
- **`reference/source_registry.md`** — 37개 데이터 소스 + 등급 🟢🟡🔴
- **`reference/rules_and_constraints.md`** — 금지사항 31개
- **`reference/guru_watchlist.md`** — 거물 투자자 8인

---

## 빠른 시작

```bash
# 종목 분석
/종목분석 삼성전자

# 일일 브리핑
/일일브리핑

# 오늘 KB 이미 최신이면
/일일브리핑 --skip-collect --skip-kb
```
