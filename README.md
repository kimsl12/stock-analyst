# 종목분석 AI 에이전트 v3.10.1

> 멀티에이전트 투자분석 시스템. Claude Code + 19개 에이전트 + 18개 슬래시 명령어.

## 리포트 열람

📘 **[리포트 목록 보기](https://kimsl12.github.io/stock-analyst/)**

최근 리포트 (2026-04-22 기준):
- [Costco Wholesale (COST)](https://kimsl12.github.io/stock-analyst/reports/COST_Costco_20260422.html) — 2026-04-22, Buy 81.0
- [ExxonMobil (XOM)](https://kimsl12.github.io/stock-analyst/reports/XOM_ExxonMobil_20260422.html) — 2026-04-22, **Strong Buy 86.2**
- [iShares Russell 2000 (IWM)](https://kimsl12.github.io/stock-analyst/reports/IWM_iSharesRussell2000_20260422.html) — 2026-04-22, Buy 80.9 (ETF)
- [iShares Min Vol (USMV)](https://kimsl12.github.io/stock-analyst/reports/USMV_iSharesMinVol_20260421.html) — 2026-04-21, Buy 72.5 (ETF)
- [iShares TIPS (TIP)](https://kimsl12.github.io/stock-analyst/reports/TIP_iSharesTIPS_20260421.html) — 2026-04-21, Buy 77.3 (ETF)
- [Invesco S&P500 Equal Weight (RSP)](https://kimsl12.github.io/stock-analyst/reports/RSP_InvescoSP500EqualWeight_20260421.html) — 2026-04-21, Buy 77 (ETF)
- [Micron Technology (MU)](https://kimsl12.github.io/stock-analyst/reports/MU_Micron_20260421.html) — 2026-04-21, **Strong Buy 경계 83.0**
- [Adobe (ADBE)](https://kimsl12.github.io/stock-analyst/reports/ADBE_Adobe_20260421.html) — 2026-04-21, Buy 76.35
- [Alibaba (BABA)](https://kimsl12.github.io/stock-analyst/reports/BABA_Alibaba_20260421.html) — 2026-04-21, Buy 74.6

최근 브리핑:
- [리밸런싱 (사용자)](https://kimsl12.github.io/stock-analyst/reports/briefing/rebalancing_user_20260421.html) — 2026-04-21, VOO 91.5% → 35% 재편안
- [이브닝 브리핑](https://kimsl12.github.io/stock-analyst/reports/briefing/evening_20260423.html) — 2026-04-23

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| **v3.10.1** | **2026-04-24** | **날짜 추론 오기 재발 방지 패치 — `date-rules.md` SSOT 신설 + 5개 에이전트(kb-updater, briefing-lead, global-macro-analyst, market-data-collector, stock-analyst-lead) 최우선 규칙 삽입 + `/KB업데이트` `target_date` 필드 강제. 원인: kb-updater가 2026-04-22 날짜로 64개 메타 필드 오기록 (실제 2026-04-24)** |
| v3.10 | 2026-04-23 | 재분석 Stale 자동 경고 시스템 (14일+ 세션 시작 배너 + 섹터 KB 갱신 매크로 트리거 7일+ 예외) + `/재분석점검` 슬래시 명령 신규 (18개 명령어) |
| v3.9 | 2026-04-23 | Phase 3 종료 검증(HTML+commit+bootstrap 3단계) + 파일별 명시적 git add (병렬 경합 방지) + 버전 관리 명명 규칙 통일 (`_v2` 폴더 접미사·HTML은 날짜만) + R:R<1.5 진입 보류 자동 태깅 + 컨센서스 초과 경고 블록 자동 삽입 |
| v3.8 | 2026-04-21 | 일회성 산출물 자체 정리 규칙 (`generate_*.py`, `*_report_data.json` 커밋 전 무조건 삭제) + `.gitignore` 2중 방어 + bootstrap stale 검증 + Todo 의무화 + `.gitattributes` CRLF 영구 차단 |
| v3.7 | 2026-04-20 | luxury KB 신규 + 에너지/방산 industry 재편 + 루트 redirect 파일 SSOT 정리 |
| v3.6 | 2026-04-19 | `etf-lead` 에이전트 분리 (stock 파이프라인에서 ETF 전용 브랜치 분기) + 다크/라이트 테마 토글 |
| v3.5 | 2026-04-13 | session-bootstrap + KB 신뢰도 티어 + analysis 아카이브 + 에이전트 모순 해결 + fetch_price.py 시장지수 + 브리핑 스캐폴딩 |
| v3.2 | 2026-04-13 | LLM Wiki 전환 — wiki-linter + KB 피드백 루프 + Phase 0-LINT |
| v3.1 | 2026-04-09 | GitHub Pages 자동 배포 + 비상장 기업 분석 |
| v3.0 | 2026-04-07 | 브리핑 파이프라인 5 에이전트 + 10 명령어 |
| v2.3 | 2026-04-06 | 데이터 흐름 개편 + 해외 종목 + 가격 검증 |
| v2.0 | 2026-04-05 | 9개 에이전트 체계 + DART API |

---

## v3.10 핵심 — 재분석 Stale 자동 경고 시스템

2026-04-23 11종 일괄 재분석 사태(사용자 직접 점검 요청 전까지 방치) 재발 방지 목적.
세션 시작 시 자동 경고 + 능동 점검 명령 + 매크로 트리거 3계층 구조.

### 계층 1: 세션 시작 자동 경고 (Passive) — 임계값 14일+

stock-analyst-lead가 매 세션 첫 응답 직전 session-bootstrap.md stale 감지.

| 경과일 | 분류 | 자동 배너 |
|-------|-----|---------|
| 0~13일 | 🟢 유효 | 표시 안 함 (피로도 방지) |
| 14~29일 | 🟡 권고 | 표시 |
| 30일+ | 🔴 만료 | 표시 |

배너는 첫 응답 1회만 출력, 반복 금지. 사용자가 "조용히" 요청 시 해당 세션 스킵.

### 계층 2: 매크로 KB 갱신 트리거 (Active) — 7일+ 예외

knowledge-base/industry/·macro/ mtime이 최근 7일 이내이면, 해당 섹터 종목 분석이
**7일+** 경과한 경우도 자동 배너 포함 (타이밍 놓침 방지).

주요 매핑: semiconductor → AVGO·NVDA·MU·SNDK / ai → META·PLTR / defense_industry → BA·KTOS·012450
/ bio_pharma → LLY / energy → XOM·034020

### 계층 3: `/재분석점검` 슬래시 명령 (On-demand)

```
/재분석점검            → 기본 14일 임계값
/재분석점검 7          → 7일+ 감지 (엄격 모드)
/재분석점검 21         → 21일+ 감지 (느슨)
```

출력: 🔴 HIGH(즉시) / 🟡 MEDIUM(고려) / 🟢 LOW(유효) 3단 분류 + 일괄 재분석 옵션 A/B/C/D.

---

## v3.9 핵심 — 재분석 프로세스 안정화 & 진입 리스크 경고

2026-04-23 11종 재분석 과정에서 발견된 5가지 이슈를 구조적으로 해결.

### 이슈 1: Phase 3 종료 검증 의무화 (stock-analyst-lead / etf-lead)
서브에이전트 Executive Summary 반환 전 **3단계 검증 Bash 실행**:
- HTML 파일 존재 (`ls reports/{파일}`)
- git log 커밋 확인 (`git log | grep {티커}`)
- session-bootstrap.md 갱신 확인

실패 시: HTML 누락 → 재호출 / 커밋 누락 → 리드 직접 처리 / bootstrap 누락 → Edit.

### 이슈 2: 파일별 명시적 git add (병렬 경합 방지)
```
❌ git add reports/           (폴더 전체 — 다른 병렬 에이전트 산출물 섞임)
✅ git add reports/{특정파일}  (본 세션 파일만)
```
사례: 2026-04-23 두산에너빌리티 HTML이 카카오 커밋에 섞인 사고.

### 이슈 3: 버전 관리 명명 규칙 통일
```
analysis/{티커}_{종목명}_v2/          (폴더는 버전 접미사 필수)
analysis/{티커}_{종목명}_v1/          (재분석 시 기존 폴더 리네임 보존)
reports/{티커}_{종목명}_{YYYYMMDD}.html  (HTML은 날짜만, 버전 접미사 금지)
```
기존 reports HTML 삭제·덮어쓰기 금지 (델타 비교 보존 의무).

### 이슈 4: R:R < 1.5 진입 보류 자동 태깅 (scorecard-strategist)
| R:R | 태그 |
|-----|-----|
| ≥ 2.0 | (태그 없음) |
| 1.5~1.99 | 🟡 Acceptable |
| 1.0~1.49 | 🟠 **⚠️ 진입 보류 권고** |
| < 1.0 | 🔴 **⛔ 진입 금지 — 조정 대기 권고** |

스코어 72.4 Buy라도 R:R 0.41이면 "진입 보류" 태그가 스코어보다 우선 표시.

### 이슈 5: 컨센서스 초과 자동 경고 (report_template.py)
현재가 > 증권사 평균 목표가인 경우, HTML 리포트 **최상단에 노란색 경고 블록 자동 삽입**:
```
⚠️ 컨센서스 초과 경고
현재가가 증권사 평균 목표가 $X를 +X.X% 초과 — 업사이드 소진
```
scorecard에서 `consensus_warning`·`entry_warning` 필드로 전달.

---

## v3.8 핵심 — 산출물 정리 & 환경 안정화

### 일회성 산출물 자체 정리 규칙 (`stock-analyst-lead`)
Phase 3 git commit **직전** 본 세션에서 생성한 아래 파일을 **커밋 여부와 관계없이 무조건 삭제**:
- `generate_{티커}.py`
- `{티커}_report_data.json`, `{티커}_part*.json`, `{티커}_basic.json`
- `scripts/_tmp_*.txt`, `analysis/{티커}/_report_data.json`

### `.gitignore` 2중 방어
루트 한정 패턴으로 실수 커밋 시에도 자동 배제 (공용 모듈 `chart_templates.py`·`report_template.py`와 이름 충돌 없음):
```
/generate_*.py
/*_report_data.json
/*_part*.json
/*_basic.json
```

### `.gitattributes` CRLF 영구 차단 (2026-04-21 커밋 `6bd498c`)
외장 SSD 환경에서 재발한 CRLF 대량 "modification" 사태 해결:
- `* text=auto eol=lf` 전역 규칙
- `core.autocrlf=false` 고정
- 기존 인덱스 CRLF 오염 97개 파일 `git add --renormalize .`

### Bootstrap Stale 검증
매 세션 시작 시 `session-bootstrap.md` Read → 마지막 작업·KB 상태·유효 파일 즉시 파악. 작업 완료 시 `stock-analyst-lead`가 자동 갱신.

### Todo 의무화
다단계 작업에서 TodoWrite로 진행 상황 추적 (토큰 관리 + 중단 복구).

### Agent 도구 복구 (2026-04-21 확인)
이전 Task 도구 비활성화 이슈 해소 — sub-agent 호출권 정상 동작.

---

## 두 개의 파이프라인

`stock-analyst-lead` 가 사용자 요청을 키워드로 자동 분기한다 (Step -2 부트스트랩 → Step -1 판별).

### 🅰️ 종목 분석 파이프라인
개별 종목·ETF 한 건 심층 분석 → HTML 리포트 생성. 매수·매도 추천 + 목표가/손절가 포함.
**v3.6부터 ETF는 `etf-lead` 하위 오케스트레이터로 분기** (data-collector → etf-analyst → report-generator 3단계).

### 🅱️ 브리핑 파이프라인
글로벌 매크로·크로스에셋 브리핑 자동 생성. **신규 투자 아이디어 적극 제안** — 매크로 분석 기반
Bull/Bear 시나리오, 섹터·종목 아이디어, 진입 근거·리스크 병기.
슬래시 명령으로 모듈별 실행. `briefing-lead` 가 오케스트레이터.

---

## 디렉토리 구조

```
.claude/agents/                              ← 19개 에이전트
├── stock-analyst-lead.md                    ← 양 파이프라인 분기 리드 (opus)
│
├── (종목 분석 10개)
│   ├── data-collector.md                    ← 종목 데이터 수집 (sonnet)
│   ├── company-overview.md                  ← 기업개요+Moat (sonnet)
│   ├── financial-analyst.md                 ← 재무 심층 (sonnet)
│   ├── business-analyst.md                  ← 산업·경쟁 (sonnet)
│   ├── momentum-analyst.md                  ← 가격 모멘텀 (sonnet)
│   ├── risk-analyst.md                      ← Devil's advocate (sonnet)
│   ├── scorecard-strategist.md              ← 10항목 종합 + KB 피드백 (opus)
│   ├── etf-lead.md                          ← ETF 전용 오케스트레이터 (opus) [v3.6 신규]
│   ├── etf-analyst.md                       ← ETF 단독 분석 (opus)
│   └── report-generator.md                  ← HTML 리포트 (sonnet)
│
├── (브리핑 5개)
│   ├── briefing-lead.md                     ← 오케스트레이터 (opus)
│   ├── market-data-collector.md             ← 시장 데이터 수집 (sonnet)
│   ├── global-macro-analyst.md              ← G-1~G-8 매크로 4축 (opus)
│   ├── correlation-monitor.md               ← 6 페어 Z-score (sonnet)
│   └── briefing-report-generator.md         ← HTML 다크 테마 (sonnet)
│
├── (공용 2개)
│   ├── kb-updater.md                        ← KB 갱신 (opus, v3.4 미니사이클)
│   └── wiki-linter.md                       ← KB 건강 점검 (sonnet)
│
└── stop-loss-rules.md                       ← ATR 손절/목표가 SSOT

scripts/
├── fetch_price.py                           ← 실시간 주가 + 시장 지수 수집
└── ...

session-bootstrap.md                         ← 세션 간 연속성 확보
knowledge-base/_index.md                     ← KB 마스터 인덱스 (단일 SSOT)
.gitattributes                               ← CRLF 영구 차단 [v3.8 신규]
```

---

## 슬래시 명령어 (총 17개)

### KB 관리 (2개)

| 명령어 | 사용 예시 | 에이전트 | 설명 |
|---|---|---|---|
| `/KB업데이트` | `/KB업데이트 luxury` | kb-updater | 섹터·토픽 웹검색 갱신 (v3.4 미니사이클) |
| `/KB점검` | `/KB점검` | wiki-linter | P0~P2 탐지 + 자동 수정 |

### 종목 분석 (6개)

| 명령어 | 사용 예시 | 설명 |
|---|---|---|
| `/종목분석` | `/종목분석 삼성전자`, `/종목분석 IWM` | 전체 분석 (개별 종목 / ETF 자동 판별) |
| `/비교분석` | `/비교분석 삼성전자 SK하이닉스` | 두 종목 비교 |
| `/빠른분석` | `/빠른분석 네이버` | 핵심 지표 + ATR (5분 이내) |
| `/손절계산` | `/손절계산 삼성전자 80000` | ATR 손절/목표 계산 |
| `/리포트` | `/리포트 삼성전자` | 기존 분석 → HTML 재생성 |
| **`/재분석점검`** | `/재분석점검`, `/재분석점검 7` | **stale 분석 탐지 + 재분석 우선순위 목록 [v3.10]** |

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

## 종목 분석 흐름 (v3.8)

```
Phase 0-A: kb-updater (섹터 KB valid_until 초과 시만)
Phase 0-B: fetch_price.py (실시간 주가 + ATR)
Phase 0-C: WebSearch (실적, 컨센서스, 뉴스)
Phase 0-D: 스캐폴딩 (빈 파일 사전 생성)
    ↓
Phase 1: company-overview + financial-analyst + business-analyst
        + momentum-analyst + risk-analyst (5개 병렬)
Phase 1-검증: 파일 크기 확인 → 0이면 폴백
    ↓
Phase 2: scorecard-strategist (10항목 + 모순 해결 + KB 피드백)
    ↓
Phase 3-cleanup: generate_*.py / *_report_data.json 전량 삭제 [v3.8]
    ↓
Phase 3: report-generator → HTML → git commit & push
    ↓
session-bootstrap.md 자동 갱신
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

## Knowledge Base 구조 (2026-04-22 기준)

```
knowledge-base/                  ← CURRENT만 (SSOT)
├── _index.md                    ← 마스터 인덱스 (단일 SSOT)
├── industry/                    ← 19개 섹터 KB
│   ├── (핵심) semiconductor.md, ai.md, auto.md, bio_pharma.md
│   ├── (에너지) energy.md, battery.md, smr.md
│   ├── (방산·우주) defense_industry.md, space.md, quantum.md
│   ├── (소비·금융) luxury.md [v3.7 신규], banking_capital.md
│   ├── (인프라) advanced_materials.md, infrastructure.md
│   ├── (통신·로봇) telecom_next.md, robotics.md
│   ├── (자본지출) capex.md
│   ├── (크립토) crypto_bitcoin.md
│   └── (기타) science_tech.md
├── macro/                       ← 8개 매크로 KB
│   ├── us_economy.md, us_monetary_policy.md (SSOT)
│   ├── korea_economy.md, geopolitics.md, global_risk_factors.md
│   ├── political_cycle.md, tech_breakthrough.md, supply_chain.md
└── portfolio/                   ← 개인 데이터
    ├── model_portfolios.md      ← 4종 (안전/중립/공격/배당)
    └── user_portfolio.md        ← 등록 완료 (중립형, VOO 91.5% 편중 진단)

knowledge-db/                    ← 영구 축적 (append-only, 자동 번영)
```

**주의**: 루트 `geopolitics.md`, `global_risk_factors.md`, `us_monetary_policy.md`는
`macro/` 폴더의 SSOT로 redirect하는 포인터 파일로 유지 (기능 무결).

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

### ⚠️ 현재 상태 (2026-04-22)

GitHub Actions **계정 단위 비활성화 중** (GitHub Support 티켓 #4287825 심사 진행).
- `main` push는 정상 동작
- gh-pages 자동 배포는 Actions 복구 시까지 지연
- 로컬 HTML 리포트는 `reports/` 폴더에서 직접 열람 가능
