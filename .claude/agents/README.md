# 종목분석 AI 에이전트 v2.3

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v2.3 | 2026-04-06 | 데이터 흐름 전면 개편 + 차트 템플릿 + 해외 종목 지원 + 가격 검증 |
| v2.2 | 2026-04-05 | ETF 분석 + 모델 최적화 (Opus 4 + Sonnet 6) + 장애 대응 |
| v2.1 | 2026-04-05 | ATR 손절/목표가 + 가중 스코어카드 + 슬래시 명령어 |
| v2.0 | 2026-04-05 | 9개 에이전트 체계 + DART API |
| v1.0 | 2026-04-05 | 초기 6개 에이전트 |

---

## v2.3 핵심 개선

### 1. 데이터 흐름 전면 개편
- **data-collector만 웹검색**, 나머지 8개 에이전트는 **파일 읽기만**
- 웹검색 총 횟수: ~60회 → ~12회로 대폭 감소
- 에이전트 타임아웃 문제 해결 (테슬라 분석 시 4/8 타임아웃 → 0 예상)

### 2. 폴더 분리
- `analysis/` — 중간 작업 파일 (Git 커밋 안 함)
- `reports/` — 최종 리포트만 (Git 커밋)

### 3. 차트 템플릿 주입
- `chart_templates.py`에 7종 차트 사전 구현
- report-generator가 데이터만 넘기면 SVG 반환 (직접 SVG 생성 제거)

### 4. 해외 종목 데이터 소스 분기
- 한국 종목: DART API + 네이버금융
- 해외 종목: Yahoo Finance + Investing.com + Macrotrends
- ETF: KRX/ETF CHECK (국내) + etf.com/etfdb.com (해외)

### 5. 가격 데이터 검증 강화
- 현재가 ∈ 52주 범위 확인
- 2개 소스 교차검증 필수
- ATR 기준가 = 현재가 일치 확인
- VOO 가격 오류 ($87 vs 실제 $603) 재발 방지

---

## 설치 후 구조

```
stock-analyst/
├── .claude/
│   ├── settings.json                ← DART API 키
│   ├── agents/                      ← 11개 에이전트
│   │   ├── stock-analyst-lead.md    ← 오케스트레이터 (opus)
│   │   ├── data-collector.md        ← 유일한 웹검색 에이전트 (sonnet)
│   │   ├── company-overview.md      ← 기업개요+Moat (sonnet, 검색금지)
│   │   ├── financial-analyst.md     ← 재무분석 (opus, 검색금지)
│   │   ├── business-analyst.md      ← 산업분석 (sonnet, 검색금지)
│   │   ├── momentum-analyst.md      ← 모멘텀 (sonnet, 검색금지)
│   │   ├── risk-analyst.md          ← 리스크 (sonnet, 검색금지)
│   │   ├── scorecard-strategist.md  ← 스코어카드 (opus, 검색금지)
│   │   ├── etf-analyst.md           ← ETF 전용 (opus, 검색5회)
│   │   ├── report-generator.md      ← HTML 리포트 (sonnet, 검색금지)
│   │   └── stop-loss-rules.md       ← 손절/목표가 SSOT
│   └── commands/                    ← 5개 슬래시 명령어
│       ├── 종목분석.md   → /종목분석
│       ├── 비교분석.md   → /비교분석
│       ├── 빠른분석.md   → /빠른분석
│       ├── 손절계산.md   → /손절계산
│       └── 리포트.md     → /리포트
├── chart_templates.py               ← 차트 7종 템플릿 (Python)
├── .gitignore                       ← analysis/ 제외
├── analysis/                        ← 중간 작업 파일 (Git 미포함)
└── reports/                         ← 최종 리포트 (Git 포함)
```

---

## 사용법

### 슬래시 명령어

| 명령어 | 사용 예시 | 설명 |
|--------|----------|------|
| `/종목분석` | `/종목분석 삼성전자` | 전체 분석 (개별종목 자동 판별) |
| `/종목분석` | `/종목분석 VOO` | 전체 분석 (ETF 자동 판별) |
| `/비교분석` | `/비교분석 삼성전자 SK하이닉스` | 두 종목 비교 |
| `/빠른분석` | `/빠른분석 네이버` | 핵심 지표 + ATR (5분 이내) |
| `/손절계산` | `/손절계산 삼성전자 80000` | ATR 손절/목표 계산 |
| `/리포트` | `/리포트 삼성전자` | 기존 분석 → HTML 재생성 |

### 자연어

```
삼성전자 분석해줘
테슬라 투자 의견 알려줘
SCHD ETF 분석해줘
```

---

## 오케스트레이션 흐름

### 개별 종목

```
Phase 0: data-collector (웹검색 12회 → analysis/에 JSON 저장)
    ↓ 파일 전달
Phase 1: company-overview + financial-analyst + momentum-analyst (병렬, 검색0회)
    ↓
Phase 2: business-analyst + risk-analyst (순차, 검색0회)
    ↓
Phase 3: scorecard-strategist (종합 평가, 검색0회)
    ↓
Phase 4: report-generator (chart_templates.py 사용 → reports/에 HTML 저장)
    ↓
Git: git add reports/ → commit → pull --rebase → push
```

### ETF

```
Phase 0: data-collector (웹검색 → analysis/에 JSON 저장)
    ↓
Phase 1: etf-analyst (단독 분석, 검색5회까지)
    ↓
Phase 2: report-generator (HTML 저장)
    ↓
Git: push
```

---

## 에이전트 모델 배정

| 역할 | 모델 | 웹검색 | 이유 |
|------|------|--------|------|
| lead | opus | 리드 판단 | 통합·판단·전략 |
| data-collector | sonnet | 12회 | 데이터 수집 전담 |
| company-overview | sonnet | 금지 | 파일 읽고 분석만 |
| financial-analyst | opus | 금지 | DCF 등 계산 필요 |
| business-analyst | sonnet | 금지 | 파일 읽고 분석만 |
| momentum-analyst | sonnet | 금지 | 파일 읽고 분석만 |
| risk-analyst | sonnet | 금지 | 파일 읽고 분석만 |
| scorecard-strategist | opus | 금지 | 종합 판단 필요 |
| etf-analyst | opus | 5회 | ETF 단독 수행 |
| report-generator | sonnet | 금지 | HTML 생성만 |

---

## 차트 7종 (chart_templates.py)

| # | 차트 | 용도 | 우선순위 |
|---|------|------|---------|
| 1 | 가격 범위 바 | 52주 내 손절-현재-목표 위치 | 필수 |
| 2 | 스코어카드 레이더 | 10항목 점수 면적 | 필수 |
| 3 | 실적 바차트 | 매출/영업이익 추이 | 권장 |
| 4 | 수익성 라인 | ROE/OPM 추이 | 선택 |
| 5 | 리스크 히트맵 | 확률×영향도 | 선택 |
| 6 | 섹터 도넛 (ETF) | 섹터별 비중 | ETF 필수 |
| 7 | 수익률 비교 (ETF) | ETF vs 지수 | ETF 권장 |

---

## ATR 손절/목표가 시스템

- STEP 1: initial_stop = MAX(고정비율 8%, ATR14×2)
- STEP 2: 트레일링 전환 = +10% 도달 시
- STEP 3: trailing_stop = 고점 - ATR×2 (래칫, 하향 금지)
- STEP 4: target = entry + risk × 손익비(기본 2)
- ETF: 패시브 5%, 레버리지 12%, 배당 손익비 1.5

---

## 장애 대응 (Circuit Breaker)

| 상황 | 동작 |
|------|------|
| 서브에이전트 실패 | 1회 재시도 → 포기 → 리드 직접 수행 |
| 토큰 한도 | 전체 중단 → 수집 데이터로 축소 리포트 |
| 2개+ 연속 실패 | 사용자에게 현황 보고 + 선택지(A/B/C) |
| HTML 생성 실패 | 차트 없는 텍스트 HTML → .md만 저장 |

---

## DART API

- 인증키: .claude/settings.json
- 일일 한도: 10,000건
- 해외 종목에서는 사용하지 않음 (Yahoo Finance 등 대체)
