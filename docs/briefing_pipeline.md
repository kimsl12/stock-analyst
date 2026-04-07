# 일일 브리핑 파이프라인 — 통합 가이드 (v3.0)

> 브리핑 시스템 v3.4 ↔ 종목분석 v2.4 통합 (Phase 1~5 완료, fix/audit-2026-04-07-v2 적용 후)
> 작성: 2026-04-07 | 상태: 명세(claude_code_instructions.md)대로 재구현 완료

---

## 1. 개요

본 파이프라인은 매 영업일 1편 이상의 **브리핑 리포트**를 생산한다.
시장 데이터 수집·매크로 4축 분석·상관관계 모니터링 3개 레이어를 분리하여 작업한 뒤
**briefing-lead** 가 종합·debate-card·contrarian-card·시나리오 분기를 도출하고
**briefing-report-generator** 가 다크 테마 HTML 리포트를 생성한다.

10개 슬래시 명령(/모닝브리핑, /이브닝브리핑, /주간리포트, /리밸런싱, /크립토브리핑,
/모델포트폴리오, /글로벌인텔리전스, /풀브리핑, /성과리뷰, /내포트폴리오)이 모두
**briefing-lead** 를 진입점으로 한다.

종목 분석 파이프라인 (`stock-analyst-lead` → 9개 종목분석가 → `report-generator`) 과는
**데이터·산출물·접근 권한·실행 순서가 완전히 분리**된다.

---

## 2. 호출 순서

```
사용자 → /{모듈명} [YYYYMMDD] [--skip-collect] [--html]
   │
   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ briefing-lead (오케스트레이터, Opus)                                   │
│   - 페르소나: 30년 경력 수석 글로벌 매크로·크로스에셋 애널리스트         │
│   - reference/{rules,sources,guru_watchlist} 사전 로드                │
│   - knowledge-db/performance/2026_recommendations.md 직전 컨텍스트 확인 │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-A. 데이터 수집 (직렬, --skip-collect 시 생략)                  │
│   ① market-data-collector (Opus)                                      │
│        → knowledge-base/market/{daily_snapshot,economic_calendar,    │
│          guru_positions}.md (CURRENT 덮어쓰기)                        │
│        → knowledge-db/market/{2026_daily_prices,                     │
│          2026_economic_indicators,2026_guru_changes}.md (append)     │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-B. 분석 (병렬 — 모드별 1~2개)                                  │
│   ②a global-macro-analyst (Opus)                                      │
│        → analysis/briefing/global_macro_{YYYYMMDD}.md                │
│        (mode: quick / weekly / full / scenario)                      │
│   ②b correlation-monitor (Opus)                                       │
│        → knowledge-base/market/{correlation_matrix,surprise_index}.md │
│        → knowledge-db/market/2026_correlation_log.md (append)        │
│        → analysis/briefing/correlation_{YYYYMMDD}.md (lead 인계 노트)│
│        (mode: quick / full / weekly_summary / crypto)                │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-C. 종합 (직렬, briefing-lead 가 직접 작성)                     │
│   ③ briefing-lead 종합                                                │
│       - debate-card 1건 이상 (보라 보더)                              │
│       - contrarian-card 1건 이상 (주황 보더)                          │
│       - 4종 모델 포트폴리오 방향 (해당 모듈)                          │
│       - 13F 시차 경고 (거물 인용 시)                                  │
│       - 심층 분석 권장 종목 (stock-analyst-lead 양방향 연계)            │
│       → analysis/briefing/lead_{type}_{YYYYMMDD}.md                  │
│   - knowledge-base/portfolio/ 갱신 (해당 모듈: rebalancing/model/user)│
│   - knowledge-db/performance/2026_recommendations.md append          │
│   - (/주간리포트, /성과리뷰) knowledge-db/performance/2026_hit_rate.md│
│   - (/글로벌인텔리전스) knowledge-db/performance/2026_scenario_tracking.md│
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-D. HTML 리포트 (직렬, briefing-report-generator 위임)          │
│   ④ briefing-report-generator (Opus)                                  │
│        → reports/briefing/{type}_{YYYYMMDD}.html                     │
│        다크 테마 + .debate-card(보라) + .contrarian-card(주황)        │
│        + 시그널 바 + 히트맵 + 시나리오 트리 + 연쇄 효과 플로우           │
│        + 푸터(10 명령어 가이드) + 주의사항 disclaimer 자동 삽입         │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-E. 자동 commit/push + 사용자 보고                              │
│   - briefing-lead 가 Bash 직접 실행:                                  │
│     git add reports/briefing/ analysis/briefing/                     │
│             knowledge-base/portfolio/ knowledge-base/market/         │
│             knowledge-db/market/ knowledge-db/performance/           │
│     git commit -m "feat(briefing): {모듈} {YYYY-MM-DD}"               │
│     git pull --rebase origin main && git push origin main            │
│   - 사용자 보고: 산출물 절대경로 + Top 핵심 + 시차 고지 + 커밋 SHA      │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
                          사용자 다운로드
```

> **데이터 흐름은 단방향이다. 역류 금지.**
> 분석가끼리 서로의 산출물을 읽지 않는다.
> 통합은 오직 `briefing-lead` 한 곳에서만 일어난다.

---

## 3. 접근 권한 매트릭스 (claude_code_instructions.md 명세 그대로)

| 에이전트 | KB industry/ | KB macro/ | KB market/ | KB portfolio/ | knowledge-db/ | analysis/briefing/ | reports/briefing/ |
|---|---|---|---|---|---|---|---|
| kb-updater | ✅쓰기 | ✅쓰기 | ❌ | ❌ | ✅쓰기 (industry/, macro/) | ❌ | ❌ |
| market-data-collector | ❌ | ✅읽기 | ✅쓰기 | ❌ | ✅쓰기 (market/) | ❌ | ❌ |
| correlation-monitor | ❌ | ❌ | ✅쓰기 | ❌ | ✅읽기+쓰기 (market/) | ✅쓰기 (자기 노트) | ❌ |
| global-macro-analyst | ❌ | ✅읽기 | ✅읽기 | ❌ | ❌ | ✅쓰기 (자기 산출물) | ❌ |
| briefing-lead | ✅읽기 | ✅읽기 | ✅읽기 | ✅읽기+쓰기 | ✅쓰기 (performance/) | ✅읽기+쓰기 (모든 산출물) | ❌ |
| briefing-report-generator | ❌ | ❌ | ✅읽기 | ✅읽기 | ❌ | ✅읽기 (lead·analysts) | ✅쓰기 |
| stock-analyst-lead 계열 (종목분석 9개) | (기존 유지) | (기존 유지) | ✅읽기 (S6 추가) | ❌ | (기존 유지) | ❌ | ❌ |

표기:
- ✅ = 허용, ❌ = 금지
- 종목분석 9개 = data-collector, company-overview, financial-analyst, business-analyst, momentum-analyst, risk-analyst, scorecard-strategist, report-generator, etf-analyst

핵심 원칙:
- **briefing-lead 만이** `analysis/briefing/` 의 모든 분석가 산출물을 동시에 읽을 수 있다 (통합 게이트웨이)
- **briefing-lead 만이** `knowledge-db/performance/` 에 쓸 수 있다 (성과 추적 시스템)
- **briefing-report-generator 만이** `reports/briefing/` 에 쓸 수 있다 (HTML 출력 전담)
- 종목분석 계열 에이전트는 본 브리핑 파이프라인의 어떤 폴더에도 쓰지 않는다 (S6 에서 market/ 읽기 권한만 1줄씩 추가됨)

---

## 4. 산출물 위치 일람 (연도별 .md 단일 파일 패턴)

| 종류 | 경로 | 생성 주체 | 생명주기 | Git |
|---|---|---|---|---|
| 시장 raw 일별 누적 | `knowledge-db/market/2026_daily_prices.md` | market-data-collector | 영구 (append-only) | ✅ 커밋 |
| 경제 지표 발표 이력 | `knowledge-db/market/2026_economic_indicators.md` | market-data-collector | 영구 (append-only) | ✅ 커밋 |
| 거물 13F 변동 이력 | `knowledge-db/market/2026_guru_changes.md` | market-data-collector | 영구 (append-only) | ✅ 커밋 |
| 상관관계 이력 | `knowledge-db/market/2026_correlation_log.md` | correlation-monitor | 영구 (append-only) | ✅ 커밋 |
| 시장 CURRENT (5파일) | `knowledge-base/market/{daily_snapshot,economic_calendar,guru_positions,correlation_matrix,surprise_index}.md` | market-data-collector + correlation-monitor | 매일/주/분기 덮어쓰기 | ✅ 커밋 |
| 매크로 raw | `knowledge-db/macro_{YYYY}.jsonl` | kb-updater | 영구 (append-only) | ✅ 커밋 |
| 매크로 CURRENT (8파일) | `knowledge-base/macro/*.md` | kb-updater | 주간 갱신 | ✅ 커밋 |
| 매크로 분석 산출물 | `analysis/briefing/global_macro_{YYYYMMDD}.md` | global-macro-analyst | 시계열 누적 | ❌ 미커밋 (산출물) |
| 상관관계 노트 | `analysis/briefing/correlation_{YYYYMMDD}.md` | correlation-monitor | 시계열 누적 | ❌ 미커밋 |
| briefing-lead 종합 노트 | `analysis/briefing/lead_{type}_{YYYYMMDD}.md` | briefing-lead | 시계열 누적 | ✅ 커밋 |
| **최종 HTML 리포트** | `reports/briefing/{type}_{YYYYMMDD}.html` | briefing-report-generator | 시계열 누적 | **✅ 자동 커밋 + 자동 push** |
| 신규 제안 누적 | `knowledge-db/performance/2026_recommendations.md` | briefing-lead | 영구 (append-only) | ✅ 커밋 |
| 시나리오 추적 | `knowledge-db/performance/2026_scenario_tracking.md` | briefing-lead | 영구 (활성/종결) | ✅ 커밋 |
| 적중률 통계 | `knowledge-db/performance/2026_hit_rate.md` | briefing-lead | 영구 (append-only) | ✅ 커밋 |
| 모델 포트폴리오 4종 | `knowledge-base/portfolio/model_portfolios.md` | briefing-lead | CURRENT 덮어쓰기 | ✅ 커밋 |
| 리밸런싱 이력 | `knowledge-base/portfolio/rebalancing_history.md` | briefing-lead | 영구 (append-only) | ✅ 커밋 |
| 사용자 포트폴리오 (개인) | `knowledge-base/portfolio/user_portfolio.md` | briefing-lead | 사용자 입력 | ⚠️ 향후 .gitignore 검토 |

`{type}` ∈ {morning, evening, weekly, rebalancing_{유형}, crypto, model_portfolio, global_intelligence, performance_review_{기간}, user_portfolio} (+ /풀브리핑 시 morning+evening+weekly+crypto 4편 동시).

---

## 5. 진입점 (사용자 인터페이스) — 10개 슬래시 명령

```bash
/모닝브리핑              # 🌅 MODULE A — 어젯밤 미국장 + 거물 + 매크로 + 4종
/이브닝브리핑            # 🌙 MODULE B — 글로벌 이슈 + 서프라이즈 + 상관관계 + 거물 심화
/주간리포트              # 📊 MODULE C — 주간 심층 + Phase 0-D 성과 추적
/리밸런싱 [유형]         # 🔄 MODULE D — 4종 모델 포트폴리오 재조정
/크립토브리핑            # 🪙 MODULE E — 크립토 + 온체인 + 규제
/모델포트폴리오          # 🧭 MODULE F — 4종 현재 구성 + 웹 서치 종목/ETF
/글로벌인텔리전스        # 🌐 MODULE G — 4축 교차 + 시나리오 플래닝
/풀브리핑                # 📘 A+B+C+E 4편 동시 (F·G 미포함)
/성과리뷰 [기간]         # 📈 C-9 단독 — 1w/2w/1m/3m 적중률
/내포트폴리오 [--view]   # 👤 사용자 1인 개인 데이터 (격리)
```

모든 명령의 `agent:` frontmatter 는 **`briefing-lead`** 로 통일.
명령 파일은 얇은 진입점 — 호출 순서·debate/contrarian-card·자동 commit/push 등 모든 로직은
`.claude/agents/briefing-lead.md` 에 정의됨.

### 자연어 진입 (stock-analyst-lead 경유)

사용자가 자연어로 "오늘 모닝 브리핑", "거물 동향 종합" 등을 요청하면
`stock-analyst-lead` 의 **Step -1: 요청 모드 판별** 이 브리핑 모드로 분기하여
`briefing-lead` 에 위임한다.

> 자연어 진입은 라우팅 보조용. 최선의 안정성은 슬래시 명령 직접 사용.

### 양방향 연계 (briefing → 종목분석)

briefing-lead 산출물의 **"심층 분석 권장 종목"** 슬롯에서 특정 티커 발견 시,
사용자가 후속으로 자연어 또는 `/종목분석 {티커}` 실행 → `stock-analyst-lead` 가 인계.

식별 기준:
- 거물 컨버전스 시그널 (B-7, C-4) — 2명 이상 동일 종목 동일 방향 13F
- 신규 투자 아이디어 (B-6, E-5) 중 확신 강도 "높음"
- 직전 적중률 ≥ 60% 종목·섹터 (knowledge-db/performance/2026_hit_rate.md)

---

## 6. 절대 금지 사항 일람

| # | 금지 | 위반 시 | 검증 위치 |
|---|---|---|---|
| 1 | 매수·매도·익절·손절·비중조정·목표주가·손절가 표현 | 브리핑 폐기 | briefing-lead 자가검증 |
| 2 | knowledge-base/portfolio/user_portfolio.md HTML 평문 노출 | 개인 데이터 누설 | briefing-report-generator 자가검증 |
| 3 | knowledge-base/industry/ 를 브리핑 분석가가 직접 읽기 | 산업 분석 파이프라인 침범 | global-macro-analyst, correlation-monitor frontmatter tools 제한 |
| 4 | analysis/briefing/ 의 다른 분석가 산출물을 분석가가 서로 읽기 | 데이터 역류 | briefing-lead 단독 통합 게이트웨이 |
| 5 | debate-card 또는 contrarian-card 누락 | 브리핑 폐기 | briefing-lead 자가검증 (각 1건 이상) |
| 6 | 13F 시차(분기말 기준 ≤45일) 고지 누락 | 브리핑 폐기 | briefing-lead + briefing-report-generator 양쪽 |
| 7 | 영어 본문 작성 | 브리핑 폐기 | briefing-lead 자가검증 |
| 8 | 분석가가 작성하지 않은 새 사실·수치를 briefing-lead 가 추가 | 인용 무결성 파괴 | briefing-lead 자가검증 |
| 9 | 종목 분석 산출물(`analysis/{종목}_*.md`)을 브리핑 파이프라인에서 생성·읽기 | 모드 혼선 | stock-analyst-lead Step -1 분기 |
| 10 | main 외 브랜치로 push (브리핑 산출물은 main 직접 push) | 이력 분산·충돌 | briefing-lead Phase 0-E |
| 11 | 1차 효과만 분석하고 멈추기 (G-6 2·3차 효과 강제) | 분석 깊이 부족 | global-macro-analyst 자가검증 |
| 12 | 기술을 단계 판정 없이 나열 (🔬→🧪→🏭→🌍 G-3 강제) | 투자 타이밍 오판 위험 | global-macro-analyst 자가검증 |
| 13 | knowledge-db/ 의 performance/ 외 폴더에 briefing-lead 가 쓰기 | 권한 위반 | briefing-lead frontmatter |

총 31개 금지 조항 (`reference/rules_and_constraints.md`). 본 표는 브리핑 파이프라인 핵심만 추림.

---

## 7. 장애 대응

### Phase 0-A 실패 (market-data-collector)
- 파이프라인 일시 중단
- 사용자에게 보고: "데이터 수집 단계 실패 — 전일 KB 로 진행할지 확인 요청"
- 사용자 동의 시: `--skip-collect` 로 재실행 (전일 KB 사용)

### Phase 0-B 실패 (global-macro-analyst 또는 correlation-monitor)
- 누락된 분석가만 1회 재호출 (같은 mode)
- 2회 연속 실패 시: 해당 섹션을 "[데이터 미수집]" 으로 표기하고 briefing-lead 가 진행
- 단, 둘 다 실패 시 (해당 모듈에서 둘 다 필요한 경우) 작업 중단

### Phase 0-C 실패 (briefing-lead 종합)
- 입력 산출물 모두 존재함에도 종합 실패 → 사용자에게 즉시 보고하고 작업 중단

### Phase 0-D 실패 (briefing-report-generator)
- HTML 생성 실패해도 `analysis/briefing/lead_*.md` 는 보존
- 사용자 보고에 "HTML 생성 실패: {원인}" 1줄 추가하고 git/push 진행

### 토큰 한도 도달
- 즉시 모든 호출 중단
- 현재까지 생성된 `analysis/briefing/*.md` 만 보존
- 사용자에게 새 세션에서 `--skip-collect` 로 재시작 안내
- /풀브리핑 의 경우 자동 폴백: weekly → crypto → evening → morning 순서로 단순화

---

## 8. 종목 분석 파이프라인과의 분리 원칙

| 항목 | 종목 분석 (v2.4) | 브리핑 (v3.0 통합) |
|---|---|---|
| 진입점 | `/종목분석 [티커]`, `/빠른분석`, `/리포트`, `/비교분석`, `/손절계산` | 10개 슬래시 명령 |
| 리드 | `stock-analyst-lead` | `briefing-lead` (직접) |
| 데이터 수집 | `kb-updater` + `data-collector` | `market-data-collector` + `kb-updater` |
| 분석가 | **9개** (data-collector, company-overview, financial-analyst, business-analyst, momentum-analyst, risk-analyst, scorecard-strategist, report-generator, etf-analyst) | **3개** (global-macro-analyst, correlation-monitor, briefing-lead 종합) |
| 작업 폴더 | `analysis/{티커}_*.md` | `analysis/briefing/*_{날짜}.md` |
| 최종 산출물 | `reports/{티커}_{날짜}.html` | `reports/briefing/{type}_{날짜}.html` |
| 매수·매도 추천 | ✅ (목표가·손절가 포함) | ❌ (관찰·점검·리서치만) |
| 13F 시차 고지 | n/a | ✅ 필수 |
| KB 접근 범위 | industry + 일부 macro + market 읽기 (S6) | market + macro (industry/portfolio 별도 권한) |
| 양방향 연계 | stock-analyst-lead Step -1 → briefing-lead | briefing-lead 산출물 "심층 분석 권장" 슬롯 → /종목분석 |

두 파이프라인은 같은 저장소·같은 KB 인프라를 공유하지만, **에이전트 frontmatter 의 tools 제한**과
**상위 리드의 모드 분기**로 물리적·논리적 격리를 유지한다.

---

## 9. Phase 진행 현황 (2026-04-07 기준 — fix/audit-2026-04-07-v2)

- ✅ **S1** (`b17e117`): 잘못된 4 에이전트 + 1 명령 git rm
- ✅ **S2** (`6153efe`): 명세 5개 에이전트 신규 (briefing-lead, market-data-collector, global-macro-analyst, correlation-monitor, briefing-report-generator) — 전부 Opus
- ✅ **S3** (`9d60d64`): 10개 슬래시 명령 (전부 agent: briefing-lead)
- ✅ **S4** (`ad14bfc`): KB 헤더 권한 정합 + knowledge-db/performance/ 3파일 신규 + Cathie Wood 통일
- 🟢 **S5** (현재): 본 docs/briefing_pipeline.md 명세 기반 재작성 + market-data-collector jsonl 패턴 → 연도별 .md 정합
- ⏭ **S6**: 9개 종목분석가 market/ 읽기 권한 1줄 + report_template.py v3.0 + README 통합 + settings 중복 정리 + 카운트 정정

---

## 10. 변경 이력

| 날짜 | 커밋 | 변경 |
|---|---|---|
| 2026-04-07 | b17e117~9d60d64 | fix/audit-2026-04-07-v2: 명세대로 5 에이전트 + 10 명령 + KB 헤더 + performance KB 재구현 |
| 2026-04-07 | (Phase 4, 폐기됨) | 본 가이드 최초 작성 (briefing-synthesizer 중심 — 명세 미부합으로 폐기) |
