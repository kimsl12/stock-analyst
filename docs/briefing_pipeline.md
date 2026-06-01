# 일일 브리핑 파이프라인 — 통합 가이드 (v3.22)

> 브리핑 시스템 v3.22 ↔ 종목분석 v2.4 통합. 10개 슬래시 명령 → briefing-lead 단일 진입점.
> 작성: 2026-04-07 (v3.0) | 갱신: 2026-06-01 (v3.22)
> 정본: `.claude/agents/briefing-lead.md` (본 문서는 운영자용 요약·참조)

---

## 1. 개요

본 파이프라인은 매 영업일 1편 이상의 **브리핑 리포트**를 생산한다.
시장 데이터 수집·매크로 4축 분석·상관관계 모니터링·예측 시장 확률·인사이더 시그널을
분리된 서브에이전트로 처리한 뒤, **briefing-lead** 가 통합·debate-card·contrarian-card·시나리오 분기를 도출하고
**briefing-report-generator** 가 다크/라이트 토글 HTML 리포트를 생성한다.

10개 슬래시 명령(`/모닝브리핑`, `/이브닝브리핑`, `/주간리포트`, `/리밸런싱`, `/크립토브리핑`,
`/모델포트폴리오`, `/글로벌인텔리전스`, `/풀브리핑`, `/성과리뷰`, `/내포트폴리오`)이 모두
**briefing-lead** 를 진입점으로 한다.

종목 분석 파이프라인 (`stock-analyst-lead` → 9개 종목분석가 → `report-generator`) 과는
**데이터·산출물·접근 권한·실행 순서가 완전히 분리**된다.

---

## 2. 호출 순서 (v3.22 표준 골격)

```
사용자 → /{모듈명} [YYYYMMDD] [--skip-collect] [--html]
   │
   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ briefing-lead (오케스트레이터, Opus)                                   │
│   - 페르소나: 30년 경력 수석 글로벌 매크로·크로스에셋 애널리스트         │
│   - 룰 4종 일괄 read: rules_and_constraints / source_registry /        │
│     guru_watchlist / korean_translation_rules                         │
│   - 도메인 KB(market/macro/industry/_index) 직접 read 금지 [v3.15]    │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-LINT — wiki-linter (mode=quick) [v3.2]                        │
│   - KB 건강 점검 (P0/P1 항목)                                          │
│   - P0 존재 시 사용자 선택지 제공 (재수집 / 진행 / 중단)                │
│   - --skip-lint 시 생략                                               │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-RESEARCH — research-curator 조건부 자동 호출 [v3.17→v3.18]    │
│   - 대상: /주간리포트, /글로벌인텔리전스, /모델포트폴리오, /풀브리핑    │
│   - 비대상: /모닝, /이브닝, /크립토, /성과리뷰, /리밸런싱, /내포트폴리오│
│   - 모드 자동 결정 (KST 요일·월 기준):                                 │
│       DOW=7 + 분기월(1/4/7/10) + DAY≤7 → quarterly+monthly+weekly     │
│       DOW=7 + DAY≤7 (분기 외)         → monthly+weekly                │
│       DOW=7 (일반 일요일)              → weekly                       │
│       DOW≠7                          → 스킵 (다음 일요일 재시도)      │
│   - 섹터: 10섹터 전체 [v3.18 확장, 기존 5섹터]                         │
│     (반도체·에너지·매크로·바이오·핀테크·방산·기술플랫폼·소비재·산업재·자동차)│
│   - 실패해도 Phase 0-A 진행 (블로킹 X)                                 │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-A — 데이터 수집 (병렬, --skip-collect 시 생략)                 │
│   ① 선행: node web/scripts/fetch_fred.mjs [v3.5]                      │
│        → knowledge-base/macro/fred_snapshot.json (15시리즈)            │
│   ② market-data-collector (Opus)                                      │
│        → knowledge-base/market/{daily_snapshot,economic_calendar,    │
│          guru_positions,correlation_matrix,surprise_index}.md         │
│        → knowledge-db/market/{2026_daily_prices,...}.md (append)     │
│   ③ polymarket-collector (Sonnet) — market-data-collector 와 병렬     │
│        → knowledge-base/market/prediction_markets.md (Polymarket +    │
│          Kalshi 이중 소스, v3.25)                                     │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-B — 분석 (병렬, 모드별 1~2개)                                  │
│   ②a global-macro-analyst (Opus, mode=quick/weekly/full/scenario)     │
│        → analysis/briefing/macro_{YYYYMMDD}.md (또는 global_macro_*) │
│   ②b correlation-monitor (Sonnet, mode=quick/full/weekly_summary/    │
│        crypto)                                                       │
│        → knowledge-base/market/correlation_matrix.md, surprise_index │
│        → analysis/briefing/correlation_{YYYYMMDD}.md                 │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 4 게이트 [v3.7] — lead_*.md 작성 진입 전 강제 검증              │
│   - market_data_{YYYYMMDD}.md · macro_{YYYYMMDD}.md ·                 │
│     correlation_{YYYYMMDD}.md 3종 파일 존재 + 크기 > 0 확인           │
│   - 부재 시 해당 서브에이전트 강제 호출 후 게이트 재평가               │
│   - 산출물 없으면 lead_*.md 작성 절대 시작 금지                       │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-C — 종합 (briefing-lead 직접 작성)                            │
│   - 인사이더 클러스터 매수 Top 5 [v3.5]                                │
│        ← knowledge-base/portfolio/insider_signals.json                │
│   - debate-card ≥ 1건 (보라 #8b5cf6)                                  │
│   - contrarian-card ≥ 1건 (주황 #d29922)                              │
│   - 예측 시장 신뢰 가중치 [v3.23→v3.25]                                │
│        Kalshi(Fed/CPI/GDP) × Polymarket(정치/지정학/크립토)            │
│   - 4종 모델 포트폴리오 방향 (안전/중립/공격/배당)                     │
│   - 13F 시차 경고 (거물 인용 시)                                       │
│   - 심층 분석 권장 종목 (stock-analyst-lead 양방향 연계)              │
│   - 실측 vs 추정 분리 [v3.18 §B]                                       │
│        5종 태그: [실측] / [KB] / [컨센서스] / [추정] / [인용]          │
│   → analysis/briefing/lead_{type}_{YYYYMMDD}.md                       │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Step 8.5 — knowledge-db/performance/ append                          │
│   - 2026_recommendations.md (신규 제안)                                │
│   - 2026_scenario_tracking.md (글로벌인텔리전스)                       │
│   - 2026_hit_rate.md (주간리포트 / 성과리뷰)                           │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Step 8.6 — knowledge-base/_index.md "최근 핵심 인사이트" append [v3.2]│
│   - 브리핑당 최대 3건                                                  │
│   - debate-card / contrarian-card 결론 포함 가능                       │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 0-D — HTML 리포트 (briefing-report-generator, run_in_background)│
│   ④ briefing-report-generator (Sonnet)                                │
│        → reports/briefing/{type}_{YYYYMMDD}.html                     │
│        - 다크/라이트 테마 토글 [v3.6]                                  │
│        - .debate-card(보라) + .contrarian-card(주황)                  │
│        - 시그널 바·히트맵·시나리오 트리·연쇄 효과 플로우                │
│        - 한국어 강제 변환 [v3.14] — 30+ 영어 키워드 grep + 한글 ≥80%   │
│        - Write 1회 atomic (Edit 분할 금지) [v3.15]                    │
│        - 이전 reports/briefing/*.html 절대 read 금지 [v3.15]          │
│        - 푸터(10 명령어 가이드) + disclaimer 자동 삽입                 │
│        - run_in_background=true (hang 방지) [v3.15]                   │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Step 14 — 자동 commit/push + manifest 동기화 [v3.16]                  │
│   - briefing-lead 가 Bash 직접 실행:                                  │
│     git add reports/briefing/ analysis/briefing/                     │
│             knowledge-base/portfolio/ knowledge-base/market/         │
│             knowledge-base/_index.md                                  │
│             knowledge-db/market/ knowledge-db/performance/           │
│     git commit -m "feat(briefing): {모듈} {YYYY-MM-DD}"               │
│   - manifest 동기화 (commit 후): node web/scripts/build_manifest.mjs  │
│     → reports/briefing/ 변경 시 manifest.json 누락 절대 금지          │
│       (Vercel 빌드 컨테이너에 .git 없음 — sort_key snapshot 필요)     │
│   - git pull --rebase origin main && git push origin main            │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Step 15 — 사용자 보고                                                  │
│   - file:// 절대경로 + Markdown 링크 형식                             │
│   - Vercel 본서버 URL (stock-analyst-jungwon1.vercel.app)             │
│   - Top 핵심 (debate/contrarian/4종방향) + 시차 고지 + 커밋 SHA       │
│   - Phase 0-D 백그라운드 완료 시 → 후속 commit/push (Step 15.5)       │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Step 16 — 자가 검증 17항목 [v3.18 §C]                                 │
│   - 명세 적합성 (spec_items grep), 필수 산출 (카드·4종·13F·인사이더)  │
│   - 실측/추정 태그 분리, 한글 ≥80%, KST 시간대, 인사이트 append      │
│   - 미통과 시 사용자 보고에 ⚠️ N/17 통과 + 미통과 목록 명시           │
└──────────────────────────────────────────────────────────────────────┘
```

> **데이터 흐름은 단방향. 역류 금지.**
> 분석가끼리 서로의 산출물을 읽지 않는다. 통합은 오직 `briefing-lead` 한 곳에서만.

---

## 3. 접근 권한 매트릭스

| 에이전트                  | KB industry/ | KB macro/ | KB market/               | KB portfolio/ | KB research/ | KB \_index                | knowledge-db/        | analysis/briefing/  | reports/briefing/ |
| ------------------------- | ------------ | --------- | ------------------------ | ------------- | ------------ | ------------------------- | -------------------- | ------------------- | ----------------- |
| wiki-linter               | ✅R          | ✅R       | ✅R                      | ✅R           | ✅R          | ✅R+W (P0만)              | ❌                   | ❌                  | ❌                |
| research-curator [v3.18]  | ❌           | ❌        | ❌                       | ❌            | ✅R+W        | ✅R+W (research 헤드라인) | ✅W (research/)      | ❌                  | ❌                |
| market-data-collector     | ❌           | ✅R       | ✅W                      | ❌            | ❌           | ✅W (P0)                  | ✅W (market/)        | ❌                  | ❌                |
| polymarket-collector      | ❌           | ❌        | ✅W (prediction_markets) | ❌            | ❌           | ❌                        | ❌                   | ❌                  | ❌                |
| correlation-monitor       | ❌           | ❌        | ✅W (corr, surprise)     | ❌            | ❌           | ❌                        | ✅R+W (market/)      | ✅W (자기 노트)     | ❌                |
| global-macro-analyst      | ❌           | ✅R       | ✅R                      | ❌            | ✅R          | ❌                        | ❌                   | ✅W (자기 산출물)   | ❌                |
| briefing-lead             | ✅R          | ✅R       | ✅R                      | ✅R+W         | ✅R          | ✅R+W (인사이트만)        | ✅W (performance/만) | ✅R+W (모든 산출물) | ❌                |
| briefing-report-generator | ❌           | ❌        | ✅R                      | ✅R           | ❌           | ❌                        | ❌                   | ✅R (lead·analysts) | ✅W               |

핵심 원칙:

- **briefing-lead 만이** `analysis/briefing/` 의 모든 분석가 산출물을 동시에 읽을 수 있다 (통합 게이트웨이)
- **briefing-lead 만이** `knowledge-db/performance/` 에 쓸 수 있다 (성과 추적 시스템)
- **briefing-report-generator 만이** `reports/briefing/` 에 쓸 수 있다 (HTML 출력 전담)
- **briefing-lead 메인 스레드는 도메인 KB(market/macro/industry/\_index) 직접 read 금지** [v3.15]
  — 서브에이전트에 위임. 단, portfolio/ + reference/ + research/ 작은 파일은 lead 직접 read OK.

---

## 4. 산출물 위치 일람

| 종류                    | 경로                                                            | 생성 주체                                        | 생명주기              | Git                   |
| ----------------------- | --------------------------------------------------------------- | ------------------------------------------------ | --------------------- | --------------------- |
| 시장 raw 일별 누적      | `knowledge-db/market/2026_daily_prices.md`                      | market-data-collector                            | 영구 (append)         | ✅                    |
| 경제 지표 발표 이력     | `knowledge-db/market/2026_economic_indicators.md`               | market-data-collector                            | 영구 (append)         | ✅                    |
| 거물 13F 변동 이력      | `knowledge-db/market/2026_guru_changes.md`                      | market-data-collector                            | 영구 (append)         | ✅                    |
| 상관관계 이력           | `knowledge-db/market/2026_correlation_log.md`                   | correlation-monitor                              | 영구 (append)         | ✅                    |
| 시장 CURRENT (5파일)    | `knowledge-base/market/*.md`                                    | market-data-collector + correlation-monitor      | 매일/주/분기 덮어쓰기 | ✅                    |
| 예측 시장 확률          | `knowledge-base/market/prediction_markets.md`                   | polymarket-collector                             | 매일 덮어쓰기         | ✅                    |
| 인사이더 시그널         | `knowledge-base/portfolio/insider_signals.json`                 | Vercel prebuild (openinsider.com)                | 매일 덮어쓰기         | ✅                    |
| FRED 스냅샷             | `knowledge-base/macro/fred_snapshot.json`                       | fetch_fred.mjs                                   | 매일 덮어쓰기         | ✅                    |
| 매크로 CURRENT (8파일)  | `knowledge-base/macro/*.md`                                     | kb-updater                                       | 주간 갱신             | ✅                    |
| 매크로 분석 산출물      | `analysis/briefing/macro_{YYYYMMDD}.md` (또는 `global_macro_*`) | global-macro-analyst                             | 시계열 누적           | ❌                    |
| 상관관계 노트           | `analysis/briefing/correlation_{YYYYMMDD}.md`                   | correlation-monitor                              | 시계열 누적           | ❌                    |
| 시장 데이터 노트        | `analysis/briefing/market_data_{YYYYMMDD}.md`                   | market-data-collector                            | 시계열 누적           | ❌                    |
| briefing-lead 종합 노트 | `analysis/briefing/lead_{type}_{YYYYMMDD}.md`                   | briefing-lead                                    | 시계열 누적           | ✅                    |
| **최종 HTML 리포트**    | `reports/briefing/{type}_{YYYYMMDD}.html`                       | briefing-report-generator                        | 시계열 누적           | ✅ 자동               |
| 신규 제안 누적          | `knowledge-db/performance/2026_recommendations.md`              | briefing-lead                                    | 영구 (append)         | ✅                    |
| 시나리오 추적           | `knowledge-db/performance/2026_scenario_tracking.md`            | briefing-lead                                    | 영구 (활성/종결)      | ✅                    |
| 적중률 통계             | `knowledge-db/performance/2026_hit_rate.md`                     | briefing-lead                                    | 영구 (append)         | ✅                    |
| 모델 포트폴리오 4종     | `knowledge-base/portfolio/model_portfolios.md`                  | briefing-lead                                    | CURRENT 덮어쓰기      | ✅                    |
| 리밸런싱 이력           | `knowledge-base/portfolio/rebalancing_history.md`               | briefing-lead                                    | 영구 (append)         | ✅                    |
| 사용자 포트폴리오       | `knowledge-base/portfolio/user_portfolio.md`                    | briefing-lead                                    | 사용자 입력           | ⚠️ git 추적 (검토 중) |
| 사용자 포트 실시간 가격 | `analysis/briefing/user_portfolio_prices_{YYYYMMDD}.json`       | fetch_price.py                                   | 사용자 포트 회차당    | ❌                    |
| Research KB             | `knowledge-base/research/{sector}/_meta.md` + L1/L2/L3          | research-curator                                 | 주간/월간/분기        | ✅                    |
| 인사이트 요약           | `knowledge-base/_index.md` "최근 핵심 인사이트"                 | briefing-lead (append) + wiki-linter (30일 정리) | 자동 정리             | ✅                    |
| 사이트 manifest         | `web/src/data/manifest.json`                                    | build_manifest.mjs                               | commit 기반           | ✅ 필수               |

`{type}` ∈ {`morning`, `evening`, `weekly`, `rebalancing_{유형}`, `crypto`, `model_portfolio`,
`global_intelligence`, `performance_review_{기간}`, `user_portfolio`}
(+ `/풀브리핑` 시 morning + evening + weekly + crypto 4편 동시).

---

## 5. 진입점 — 10개 슬래시 명령

```bash
/모닝브리핑              # 🌅 MODULE A — 직전 미국 정규장(D-1) 종가 + 거물 + 매크로 + 4종
/이브닝브리핑            # 🌙 MODULE B — 한국 마감 + 미국 프리마켓 + 글로벌 + 서프라이즈 + 상관관계
/주간리포트              # 📊 MODULE C — 주간 심층 + C-9 성과 추적 + 4종 주간 방향
/리밸런싱 [유형]         # 🔄 MODULE D — 4종 모델 포트폴리오 재조정
/크립토브리핑            # 🪙 MODULE E — BTC/ETH/SOL + 온체인 + 상관 + 규제
/모델포트폴리오          # 🧭 MODULE F — 4종 현재 구성 + 자산군별 비중 + 종목/ETF 웹 서치
/글로벌인텔리전스        # 🌐 MODULE G — 지정학·정치·기술·에너지 4축 교차 + 시나리오
/풀브리핑                # 📘 A+B+C+E 4편 동시 (F·G 미포함)
/성과리뷰 [기간]         # 📈 C-9 단독 — 1w/2w/1m/3m 적중률 + 교훈 노트
/내포트폴리오 [--view]   # 👤 사용자 1인 개인 데이터 (격리, 면책 제거 v2)
```

모든 명령의 `agent:` frontmatter 는 **`briefing-lead`** 로 통일.
명령 파일은 얇은 진입점 — 호출 순서·debate/contrarian-card·자동 commit/push 등 모든 로직은
`.claude/agents/briefing-lead.md` 에 정의됨.

### 모듈별 호출 순서 차이

| 명령                | LINT   | RESEARCH    | FRED   | market-data            | macro          | correlation    | polymarket       | 인사이더     | 비고                                                    |
| ------------------- | ------ | ----------- | ------ | ---------------------- | -------------- | -------------- | ---------------- | ------------ | ------------------------------------------------------- |
| `/모닝`             | ✅     | ❌          | ✅     | ✅ (us focus, 13F off) | quick          | quick          | 병렬             | ✅ Top5      | 4종 방향                                                |
| `/이브닝`           | ✅     | ❌          | ✅     | ✅ (both)              | quick          | full           | 병렬             | ✅ Top5      | 아침 대비 변화 + B-7 거물 심화                          |
| `/주간`             | ✅     | 일요일 조건 | ✅     | ✅ (--week)            | full           | weekly_summary | 병렬             | (옵션 Top10) | C-9 성과 추적, 스파크라인                               |
| `/리밸런싱`         | ✅     | ❌          | ❌     | ✅ (--quick)           | (KB read)      | ❌             | ❌               | ❌           | 도넛 차트 + 변화 화살표                                 |
| `/크립토`           | ✅     | ❌          | ❌     | ✅ (--crypto-focus)    | ❌             | crypto         | ✅ (크립토 마켓) | ❌           | BTC↔NASDAQ/Gold/USD                                     |
| `/모델포트폴리오`   | ✅     | 일요일 조건 | ❌     | ✅ (F-1만)             | (KB read)      | ❌             | ❌               | ❌           | F-6 비교표 + F-7 disclaimer                             |
| `/글로벌인텔리전스` | ✅     | 일요일 조건 | ✅     | ✅ (--macro-focus)     | full (G-1~G-8) | ❌             | ✅ (지정학)      | ❌           | 시나리오 트리 + 4축 매트릭스                            |
| `/풀브리핑`         | ✅ 1회 | 일요일 조건 | ✅ 1회 | ✅ 1회 (full)          | full           | full           | ✅ 1회           | ✅ Top5      | 단일 commit 4 산출물                                    |
| `/성과리뷰`         | ❌     | ❌          | ❌     | ✅ (--quick 검증)      | ❌             | ❌             | ❌               | ❌           | 적중률 공식 고정 (재해석 금지)                          |
| `/내포트폴리오`     | ❌     | ❌          | ❌     | ❌ (read only)         | (read only)    | ❌             | ❌               | ❌           | Phase 1.5 fetch_price.py + Supabase sync (v3.16 STRICT) |

### 자연어 진입 (stock-analyst-lead 경유)

사용자가 자연어로 "오늘 모닝 브리핑" 요청 시 `stock-analyst-lead` 의 Step -1 분기가 브리핑 모드로 라우팅하여
`briefing-lead` 에 위임. 안정성 우선이라면 슬래시 명령 직접 사용을 권장.

### 양방향 연계 (briefing → 종목분석)

briefing-lead 산출물의 **"심층 분석 권장 종목"** 슬롯에서 식별된 티커는 사용자가
`/종목분석 {티커}` 실행 → `stock-analyst-lead` 가 인계받는다.

식별 기준:

- 거물 컨버전스 시그널 (2명 이상 동일 종목 동일 방향 13F)
- 신규 투자 아이디어 중 확신 강도 "높음"
- 직전 적중률 ≥ 60% 종목·섹터

---

## 6. 종합 분석 산출 — 핵심 도구 5가지

### 6.1 debate-card (핵심 논쟁) — 1건 이상 강제

```markdown
> 💜 **debate-card — {주제}**
>
> **Bull 측 주장:** (3줄, [소스])
> **Bear 측 주장:** (3줄, [소스])
> **현재 시장 컨센서스:** Bull 우세 / Bear 우세 / 팽팽
> **briefing-lead 판단:** 어느 쪽 시나리오 확률을 높게 본다 + 이유 1줄
```

CSS 클래스: `.debate-card` (보라 #8b5cf6 좌측 보더).

### 6.2 contrarian-card (과소평가 포인트) — 1건 이상 강제

```markdown
> 🟠 **contrarian-card — {시장이 놓치고 있는 것}**
>
> **시장의 일반 가정:** (1~2줄)
> **반대 시그널:** (3줄, [소스])
> **만약 반대 시그널이 맞다면:** 어떤 자산이 어떻게 반응
> **확률 (briefing-lead 추정):** 낮음/중간/높음
```

CSS 클래스: `.contrarian-card` (주황 #d29922 좌측 보더).

### 6.3 예측 시장 신뢰 가중치 [v3.23 → v3.25 Kalshi 추가]

`knowledge-base/market/prediction_markets.md` 에 이벤트 확률이 있으면 반드시 적용.
**이중 소스 (Polymarket + Kalshi)** — 카테고리별 1차 소스 분리:

| 카테고리            | 1차 소스                     | 2차 소스                |
| ------------------- | ---------------------------- | ----------------------- |
| Fed/금리            | **Kalshi** (FOMC 100%)       | Polymarket              |
| CPI/인플레이션      | **Kalshi** (경제 71%)        | Polymarket (64%)        |
| GDP/실업률/경기침체 | **Kalshi** (Brier 0.05)      | Polymarket (Brier 0.08) |
| 미국 정치           | **Polymarket** (81%)         | Kalshi (78%)            |
| 지정학              | **Polymarket** (거래량 우위) | Kalshi                  |
| 크립토              | **Polymarket** (단독)        | —                       |

**확률 산출 공식:**

```
최종 확률 = 1차 소스 × 0.7 + briefing-lead 자체 판단 × 0.3
(이중 소스 합의 시) 소스 합의 = 1차 × 0.65 + 2차 × 0.35 → × 0.7 + lead × 0.3
```

**특수 가중치:** Kalshi FOMC 마켓 90:10, 양쪽 합의 75:25, 괴리 10%p+ 50:50, 마켓 종료 4시간 이내 90:10, 마켓 없음 0:100.

### 6.4 4종 포트폴리오 방향 — 모닝/이브닝/주간 강제

```markdown
| 포트폴리오 | 시사점 (1줄) | 방향           | 참고 자산군 |
| ---------- | ------------ | -------------- | ----------- |
| 🛡️ 안전형  | ...          | 유지/조정/경계 | ...         |
| ⚖️ 중립형  | ...          | 유지/조정/경계 | ...         |
| 🔥 공격형  | ...          | 유지/조정/경계 | ...         |
| 💰 배당형  | ...          | 유지/조정/경계 | ...         |
```

### 6.5 13F 시차 고지 (거물 인용 시 필수)

```
> ⚠️ **13F 시차 경고:** 분기말 기준, 최대 45일 시차. "현재 보유" 표현 금지.
```

### 6.6 인사이더 클러스터 매수 Top 5 [v3.5, /모닝·/이브닝 필수]

소스: `knowledge-base/portfolio/insider_signals.json` (Vercel prebuild 자동, openinsider.com).
필터: 3명 이상 동시 매수, 지난 7일 거래만, 데이터 0건 시 "최근 7일 클러스터 매수 없음" 1줄.
위치: B-7 거물 심화 다음, 4종 방향 직전.
출처 표기: `[openinsider.com, {filing_date}]`

---

## 7. 시간 폭주 방지 룰 [v3.15, 2026-05-09]

**배경:** 주간리포트 1회 작업 45분 (정상 15~20분). KB 10개+ 직접 Read → 컨텍스트 폭주 → compact 14분 손실 + 중복 실행 5분.

### 7.1 KB 카테고리별 Read 분리

| KB 경로                                         | 처리 주체                                          |
| ----------------------------------------------- | -------------------------------------------------- |
| `knowledge-base/market/`                        | **market-data-collector 위임** — 메인 lead Read ❌ |
| `knowledge-base/market/prediction_markets.md`   | polymarket-collector 위임 → lead 직접 Read OK      |
| `knowledge-base/macro/`                         | **global-macro-analyst 위임** — 메인 lead Read ❌  |
| `knowledge-base/industry/`                      | **global-macro-analyst 위임** — 메인 lead Read ❌  |
| `knowledge-base/_index.md`                      | **wiki-linter 위임** — 메인 lead Read ❌ (중복)    |
| `knowledge-base/portfolio/*.md`                 | lead 직접 Read OK (작은 파일)                      |
| `knowledge-base/portfolio/insider_signals.json` | lead 직접 Read OK                                  |
| `knowledge-base/research/`                      | lead 직접 Read OK (debate/contrarian-card 강화 시) |
| `reference/*.md`                                | lead 직접 Read OK (룰 4종)                         |
| `knowledge-db/performance/`                     | lead 직접 R+W OK (성과 추적)                       |

### 7.2 5룰 요약

1. **KB Read 분리** — 메인 lead 도메인 KB read 금지, 서브에이전트 위임
2. **이전 HTML 금지** — briefing-report-generator 가 이전 `reports/briefing/*.html` 절대 read 금지
   (양식은 generator.md 인라인 CSS 표준이 source). 시계열 비교 데이터는 lead 가 lead\_\*.md 에 미리 기록 후 generator 가 변환
3. **체크포인트 강제** — 각 Phase 완료 시 TodoWrite 갱신 + session-bootstrap.md "진행 중 작업" 행 갱신.
   compact 발생 시 어디까지 됐는지 즉시 파악 → 중복 실행 방지
4. **Write 1회 atomic** — generator 가 71KB HTML 을 Edit 분할 금지, Write 1회로 출력
5. **1회 실패 시 lead 재호출** — generator 자가 검증 실패 시 lead 가 generator 새로 호출
   (이전 컨텍스트 폐기, 동일 input)

### 7.3 메인 스레드 가이드 [v3.7]

❌ **금지:** KB 파일 사전 read 후 briefing-lead 프롬프트에 dump, "이미 확인했으니 종합만" 같은 단축 지시
✅ **허용:** mode·target_date·sections 등 단순 컨텍스트만 전달, 데이터 수집은 briefing-lead 가 본인 워크플로 따라

### 7.4 데이터 체크리스트 시스템 [v3.6]

서브에이전트 호출 프롬프트에 3 단계 체크리스트 명시:

- `required_must` (5~8건): 누락 시 1회 재호출
- `required_should` (5~10건): 누락 시 "미수집" 표기 후 진행
- `nice_to_have` (0~5건): 누락 시 무시

**재호출 캡:** 서브에이전트당 최대 1회 (= 워크플로 전체 최대 6회). 초과 시 강제 종료 + 미완성 표기.

---

## 8. v3.18 명세 적합성 + 실측/추정 분리 + 17항목 검증

### 8.1 A. 명세 → plan 1:1 (누락 0 룰)

lead\_\*.md 작성 전 본 문서 §"호출 순서" + briefing-lead.md §"명령별 호출 순서" + §"종합 분석 산출" 의
spec_items 를 TodoWrite 또는 lead.md 상단 `<!--Plan-->` 주석으로 기록. 모든 항목이 헤딩으로 들어가야 한다.
데이터 부재 시 항목 삭제 X → `[관측 불가 — 사유]` 로 표기.

### 8.2 B. 실측 vs 추정 분리 — 5종 태그

| 태그         | 의미                                         | 예                                                                       |
| ------------ | -------------------------------------------- | ------------------------------------------------------------------------ |
| `[실측]`     | 본 파이프라인 직접 수집 가격·수치            | SP500 종가 5,432.10 [실측, market-data-collector / yfinance]             |
| `[KB]`       | KB 적재 데이터 인용                          | Fed 정책금리 5.25% [KB, macro/fred_snapshot.json valid_until 2026-05-14] |
| `[컨센서스]` | 외부 컨센서스·애널리스트 합의                | NVDA 12M 컨센 $185 [컨센서스, FactSet]                                   |
| `[추정]`     | briefing-lead 자체 시나리오 가중치·확률 판단 | Bull 시나리오 60% [추정, briefing-lead 판단]                             |
| `[인용]`     | 외신·SEC 공시·임원 발언 직접 인용            | Powell: "Sticky inflation" [인용, FOMC 2026-04-30 회견록]                |

**13F 인용은 반드시 `[KB, 분기말]` — `[실측]` 절대 금지** (시차 사고 방지).

### 8.3 C. 산출물 검증 체크리스트 — 17항목 3시점

**3 시점:** Step 9 직후 (lead.md Write 완료) / Step 13 직전 (generator 호출 직전) / Step 13 직후 (HTML 완료).

```
[명세 적합성 §A]
 1. spec_source 명시 (docs/briefing_pipeline.md §{모듈})
 2. plan 의 spec_items 모두 lead_*.md 헤딩 존재
 3. 데이터 부재 항목 → "[관측 불가 — 사유]" 표기
 4. extra 섹션 추가 시 plan 에 추가 이유 1줄 기록

[필수 산출]
 5. debate-card ≥ 1건
 6. contrarian-card ≥ 1건
 7. 4종 포트폴리오 방향 표
 8. 13F 인용 시 시차 고지 1줄 동행
 9. 인사이더 클러스터 (모닝/이브닝/주간) 존재 또는 "최근 7일 0건"

[실측/추정 분리 §B]
10. 모든 수치·확률·방향성 주장에 5종 태그 1개 부여
11. 같은 수치에 [실측]+[추정] 동시 부여 0건
12. 13F 인용 모두 [KB, 분기말] (절대 [실측] 아님)
13. 컨센서스 수치 모두 [컨센서스] 태그

[언어·시간·출처]
14. 한국어 본문 (영어 잔류 < 20%, 한글 ≥ 80%)
15. 시간대 KST + 모듈별 미국장 상태 표현 정합
16. 출처 없는 수치 0건
17. knowledge-base/_index.md "최근 핵심 인사이트" 1~3줄 append 완료
```

**2회 보완 후에도 실패 시:** lead.md 최상단 ⚠️ 경고 박스 삽입 + commit/push 진행 (자동 파이프라인 절대 블로킹 X) + 사용자 보고 말미에 "⚠️ 자가 검증 N/17 통과 — 미통과 항목: {목록}" 명시.

---

## 9. Research KB 활용 [v3.17]

본 에이전트는 `knowledge-base/research/` 직접 read 권한이 있으므로 **debate/contrarian-card 생성 시점에만** 빠르게 조회.

- debate-card: `research/{sector}/_meta.md` "Key Uncertainties" 매칭 → L2 요약 1~2건 Read → Bull/Bear 근거에 research excerpt 인용 ≥ 1건
- contrarian-card: `research/_index.md` 컨센서스 충돌 항목 → L2 Read → 반대 가설 본문에 excerpt 인용 ≥ 1건
- 인용 형식: `📄 [Working Paper] BIS WP #1247 (2026-03) — §4 → ...` ( `research/_citation_format.md` 8 유형 분류 준수)
- 시간 예산: 카드당 최대 2분, 카드 3건 = 최대 6분 (v3.15 의 15~20분 룰 안에 흡수)
- 환각 방지: \_index.md / L2 요약본에 없는 출처를 "기억"으로 추가 인용 금지. URL·페이지 번호는 KB에서 직접 본 것만.

---

## 10. 절대 금지 사항

| #   | 금지                                                            | 비고                                                          |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------- |
| 1   | 매수·매도·익절·손절·비중조정·목표주가·손절가 표현               | `/내포트폴리오` v2 예외                                       |
| 2   | user_portfolio.md HTML 평문 노출 (개인 데이터)                  | `/내포트폴리오` 만 본인 데이터 사용                           |
| 3   | knowledge-base/industry/ 를 브리핑 분석가가 직접 읽기           | global-macro-analyst 만                                       |
| 4   | analysis/briefing/ 의 다른 분석가 산출물을 분석가가 서로 읽기   | briefing-lead 단독 통합 게이트웨이                            |
| 5   | debate-card / contrarian-card 누락                              | 각 1건 이상                                                   |
| 6   | 13F 시차 (분기말 ≤45일) 고지 누락                               | lead + report-generator 양쪽 검증                             |
| 7   | 영어 본문 작성 (한글 < 80%)                                     | report-generator 자가 변환 + grep 30+ 키워드                  |
| 8   | 분석가가 작성하지 않은 새 사실·수치를 lead 가 추가              | 인용 무결성                                                   |
| 9   | 종목 분석 산출물(`analysis/{종목}_*.md`)을 브리핑에서 생성·읽기 | 모드 혼선                                                     |
| 10  | main 외 브랜치로 push                                           | 브리핑 산출물 main 직접 push                                  |
| 11  | knowledge-db/ performance/ 외 폴더에 lead 가 쓰기               | lead frontmatter                                              |
| 12  | briefing-lead 직접 WebSearch / WebFetch                         | v3.6 에서 도구 제거. 모든 데이터 수집은 Task 위임             |
| 13  | briefing-report-generator 가 이전 reports/briefing/\*.html read | v3.15. 양식 source 는 generator.md 인라인 CSS                 |
| 14  | knowledge-base/\_index.md P0 섹션 외 임의 수정                  | wiki-linter / market-data-collector / lead 인사이트 append 만 |
| 15  | 1차 효과만 분석하고 멈추기                                      | G-6 2·3차 효과 강제                                           |
| 16  | 기술을 단계 판정 없이 나열                                      | G-3 🔬→🧪→🏭→🌍 단계 강제                                     |
| 17  | reports/briefing/ 변경 push 시 manifest.json 동기화 누락        | Vercel 빌드 컨테이너에 .git 없음 → snapshot 필수              |

---

## 11. 장애 대응

### Phase 0-A 실패 (market-data-collector)

**원칙: 자동 파이프라인을 블로킹하지 않는다.** 수집 실패/부분성공해도 일단 브리핑 생성, 사용자가 원할 때만 수동 웹서치로 보강.

- `SUCCESS` → 평소대로 Phase 0-B
- `PARTIAL` → 실패 카테고리만 `[관측 불가 — 사유]` 표기 후 자동 진행
- `FAILED` → 경고 배너 삽입 + 매크로 중심 압축 브리핑 자동 진행
- 산출물(MD/HTML) 최상단 ⚠️ 배너 고정 삽입
- 사용자 보고 말미에 **조건부 수동 웹서치 프롬프트** (PARTIAL/FAILED 시만)
- 사용자가 검색어 입력 시 lead 가 직접 WebSearch (예외적 유일 경로) → KB/DB 업데이트 → 리포트 재생성 → 재커밋·push
- 무응답/"그대로" 시 작업 종료

### Phase 0-B 실패

- 누락된 분석가만 1회 재호출 (같은 mode) — 재호출 캡 [v3.6]
- 2회 연속 실패 시 해당 섹션 "[데이터 미수집]" 표기 후 lead 진행
- 둘 다 실패 시 (해당 모듈에서 둘 다 필요한 경우) 작업 중단

### Phase 0-C 실패 (lead 종합)

- 입력 산출물 모두 존재함에도 종합 실패 → 사용자 즉시 보고 + 작업 중단

### Phase 0-D 실패 / hang [v3.15]

- HTML 생성 실패해도 `lead_*.md` 보존
- `run_in_background=true` 로 호출 → 부모 세션 무한 대기 차단
- Step 14 (commit/push) 즉시 진행 — 에이전트 완료 대기 X
- HTML 미생성 시: 사용자 보고에 "📄 HTML 생성 진행중 — lead\_\*.md 먼저 커밋 완료. HTML 완료 시 후속 커밋."
- 백그라운드 완료 통보 수신 시 → Step 15.5 후속 commit/push
- 통보 미수신 (세션 종료 / hang) → lead\_\*.md 이미 커밋됨, 후속 커밋 생략

### 토큰 한도 도달

- 즉시 모든 호출 중단, 현재까지 `analysis/briefing/*.md` 보존
- 사용자에게 새 세션에서 `--skip-collect` 로 재시작 안내
- `/풀브리핑` 자동 폴백: weekly → crypto → evening → morning 순서로 단순화

---

## 12. 종목 분석 파이프라인과의 분리 원칙

| 항목           | 종목 분석 (v2.4)                                                                                                                                                 | 브리핑 (v3.22)                                                                                                                   |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 진입점         | `/종목분석`, `/빠른분석`, `/리포트`, `/비교분석`, `/손절계산`                                                                                                    | 10개 슬래시 명령                                                                                                                 |
| 리드           | `stock-analyst-lead`                                                                                                                                             | `briefing-lead`                                                                                                                  |
| 데이터 수집    | `kb-updater` + `data-collector`                                                                                                                                  | `market-data-collector` + `polymarket-collector` + FRED                                                                          |
| 분석가         | 9개 (data-collector, company-overview, financial-analyst, business-analyst, momentum-analyst, risk-analyst, scorecard-strategist, report-generator, etf-analyst) | 3 + 보조 (global-macro-analyst, correlation-monitor, briefing-lead 종합 + research-curator + wiki-linter + polymarket-collector) |
| 작업 폴더      | `analysis/{티커}_*.md`                                                                                                                                           | `analysis/briefing/*_{날짜}.md`                                                                                                  |
| 최종 산출물    | `reports/{티커}_{날짜}.html`                                                                                                                                     | `reports/briefing/{type}_{날짜}.html`                                                                                            |
| 매수·매도 추천 | ✅ (목표가·손절가)                                                                                                                                               | ❌ (`/내포트폴리오` v2 예외)                                                                                                     |
| 13F 시차 고지  | n/a                                                                                                                                                              | ✅ 필수                                                                                                                          |
| KB 접근 범위   | industry + 일부 macro + market 읽기                                                                                                                              | market + macro + portfolio (W) + performance (W) + research (R)                                                                  |
| 양방향 연계    | stock-analyst-lead Step -1 → briefing-lead                                                                                                                       | briefing-lead "심층 분석 권장" → /종목분석                                                                                       |

두 파이프라인은 같은 저장소·같은 KB 인프라를 공유하지만, **에이전트 frontmatter tools 제한** + **상위 리드 모드 분기**로 격리.

---

## 13. 사이트 배포 (CLAUDE.md 의무)

`reports/briefing/*.html` 변경 push 직후 **두 채널 모두** 자동 실행:

```bash
# 1. 본서버 (Vercel) — 사용자 트래픽 메인
vercel --prod --yes

# 2. 미러 (Cloudflare Pages) — 보조 채널
bash scripts/deploy_cloudflare.sh
```

**Vercel 먼저 (≈45초), Cloudflare 나중 (≈3~5초).**
GitHub Actions 차단(2026-04-15)으로 Vercel 자동 webhook 도 끊겨 수동 CLI 호출 필수.
완료 링크는 항상 **Vercel 본서버 URL** (`stock-analyst-jungwon1.vercel.app`) 사용.

---

## 14. 변경 이력 (v3.0 → v3.22)

| 버전    | 날짜       | 변경                                                                                                                                                                                    |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v3.0    | 2026-04-07 | fix/audit-2026-04-07-v2 재구현 (5 에이전트 + 10 명령 + KB 헤더 + performance KB)                                                                                                        |
| v3.1    | 2026-04~   | scorecard-strategist KB 피드백 루프 (종목 측 연계)                                                                                                                                      |
| v3.2    | 2026-04~   | Phase 0-LINT (wiki-linter quick) 자동 호출 + Step 8.6 \_index.md "최근 핵심 인사이트" append + correlation-monitor 강화                                                                 |
| v3.4    | 2026-04~   | 통합 파이프라인 구조 (briefing-lead 단독 게이트웨이)                                                                                                                                    |
| v3.5    | 2026-05-07 | polymarket-collector 추가 + 인사이더 클러스터 매수 Top 5 (모닝/이브닝) + FRED 페치 선행 (fetch_fred.mjs 15시리즈) + 적중률 공식 고정                                                    |
| v3.6    | 2026-05-07 | 다크/라이트 테마 토글 + briefing-lead WebSearch/WebFetch 도구 제거 (3계층 무력화 차단) + 데이터 체크리스트 (must/should/nice) + 재호출 캡 1회                                           |
| v3.7    | 2026-05-07 | Phase 4 산출물 게이트 (market/macro/correlation 3종 파일 존재 검증) + 메인 스레드 KB 사전 주입 금지                                                                                     |
| v3.10.1 | 2026-05    | 날짜 Bash 확정 룰 ($TODAY / $TODAY_COMPACT)                                                                                                                                             |
| v3.11   | 2026-05-06 | 출력 언어 한국어 + 시간대 표준 (\_time_guide.md §3·§4·§5) + source 라벨링 KST/ET 병기                                                                                                   |
| v3.12   | 2026-05    | /내포트폴리오 Phase 4 — briefing-report-generator 위임 강제 (lead HTML 직접 작성 금지)                                                                                                  |
| v3.13   | 2026-05    | fetch_price.py JSON_OUTPUT_START/END 블록만 파싱 (한국 종목 KRX 경고 오독 차단)                                                                                                         |
| v3.14   | 2026-05-06 | 한글 강제 v3.14 — korean_translation_rules.md 매핑 사전 의무 + briefing-report-generator 자체 변환 + 30+ 영어 키워드 grep + 한글 비중 ≥ 80%                                             |
| v3.15   | 2026-05-09 | 시간 폭주 방지 5룰 (KB Read 분리 / 이전 HTML 금지 / 체크포인트 / Write 1회 atomic / 1회 실패 시 lead 재호출) + run_in_background hang 방지 + 시계열 비교 데이터 lead 책임               |
| v3.16   | 2026-05-10 | manifest 동기화 의무 (build_manifest.mjs commit 후 호출) + /내포트폴리오 Supabase STRICT 모드 + sync_portfolio 스키마 컨트랙트 + health_check.mjs 검증 게이트                           |
| v3.17   | 2026-05-12 | Phase 0-RESEARCH 신규 + research-curator 조건부 자동 호출 (일요일 + 모듈 매칭) + research KB 활용 (debate/contrarian-card 인용 ≥ 1건) + L3 분기 Deep Dive                               |
| v3.18   | 2026-05-15 | research-curator 5섹터 → 10섹터 확장 (반도체·에너지·매크로·바이오·핀테크·방산·기술플랫폼·소비재·산업재·자동차) + 명세 → plan 1:1 룰 + 실측/추정 5종 태그 + 17항목 검증 체크리스트 3시점 |
| v3.22   | 2026-05~   | audit/fence 자동화 + manifest dedupe + 누적 정리 (cleanup_reanalysis.mjs 등) + 작업 자동화 표준화                                                                                       |
| v3.23   | 2026-05~   | 예측 시장 신뢰 가중치 룰 도입 (Polymarket 1차)                                                                                                                                          |
| v3.25   | 2026-05~   | Kalshi 이중 소스 추가 (Fed/CPI/GDP 1차 Kalshi, 미국 정치/지정학/크립토 1차 Polymarket)                                                                                                  |

> 본 표는 docs/briefing_pipeline.md 갱신 시점(2026-06-01) 까지 누적된 v3.x 마이너 변경. 세부 운영 룰은 `.claude/agents/briefing-lead.md` 정본 참조.
