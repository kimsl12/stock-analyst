# AGENTS.md — 종목분석 에이전트 시스템 명세

> 작성: 2026-06-11 (`.claude/agents/` 22종 + `.claude/commands/` 22종 전수 호출 그래프 검증 기준)
> 세부 규칙의 단일 진실 소스(SSOT)는 각 에이전트 명세(`.claude/agents/*.md`)이며,
> 본 문서는 **시스템 맵 + 운영 계약 요약**이다. 두 문서가 어긋나면 에이전트 명세가 우선.

---

## 1. 구성 — 22 에이전트 (리드 3 + 전문 19)

### 리드 (오케스트레이터)

| 에이전트             | model / maxTurns | 역할                                                                                      | 호출하는 서브에이전트                                                                                                                                                                                                   |
| -------------------- | ---------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stock-analyst-lead` | opus / 40        | 종목·ETF 분석 총괄. 모드 판별(종목 vs ETF vs 브리핑) 후 위임                              | kb-updater, data-collector, company-overview, financial-analyst, business-analyst, momentum-analyst, risk-analyst, scorecard-strategist, etf-lead, report-generator, reanalysis-tracker, (브리핑 모드 시) briefing-lead |
| `briefing-lead`      | opus / 25        | 브리핑 10종 명령 총괄. **수집 금지 — 종합·작성만** (WebSearch/WebFetch 도구 제거됨, v3.6) | wiki-linter, market-data-collector, polymarket-collector, global-macro-analyst, correlation-monitor, research-curator, briefing-report-generator                                                                        |
| `etf-lead`           | —                | ETF 전용 3단계 파이프라인. 분석 직접 작성 금지                                            | data-collector, etf-analyst, report-generator                                                                                                                                                                           |

### 전문 에이전트

| 에이전트                | 역할                                                                                                      | 호출처                                             |
| ----------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `data-collector`        | 실시간 데이터 일괄 수집 (타 분석가는 웹검색 금지, 이 산출물만 read)                                       | stock-analyst-lead, etf-lead                       |
| `kb-updater`            | 섹터 매크로·산업 KB 갱신 (knowledge-db append + knowledge-base 덮어쓰기)                                  | stock-analyst-lead Phase 0-A, `/KB업데이트`        |
| `company-overview`      | 기업개요 + 해자(Moat)                                                                                     | Phase 1                                            |
| `financial-analyst`     | 재무 + 밸류에이션 + 목표가                                                                                | Phase 1                                            |
| `momentum-analyst`      | 모멘텀 + 컨센서스 + 수급                                                                                  | Phase 1                                            |
| `business-analyst`      | 산업 트렌드 + 경쟁구도                                                                                    | Phase 2                                            |
| `risk-analyst`          | 리스크 매트릭스 + Devil's Advocate                                                                        | Phase 2                                            |
| `scorecard-strategist`  | 10항목 가중 스코어카드 + ATR 손절/목표가 + § Confidence Interval + § 약한 가정 3개                        | Phase 3                                            |
| `report-generator`      | analysis/ → HTML 리포트 (report_template.py 호출)                                                         | 리드 3종, `/리포트`                                |
| `etf-analyst`           | ETF 종합 분석 (holdings·보수율·추적오차)                                                                  | etf-lead                                           |
| `market-data-collector` | 지수·환율·원자재·채권·크립토·캘린더·13F → knowledge-base/market/ 5파일                                    | briefing-lead Phase 0-A, stock-analyst-lead        |
| `polymarket-collector`  | Polymarket+Kalshi 예측 시장 확률 → prediction_markets.md (Phase 0-A에서 market-data-collector와 **병렬**) | briefing-lead                                      |
| `global-macro-analyst`  | 매크로 4축(지정학·정치·기술·에너지) + 시나리오 플래닝                                                     | briefing-lead                                      |
| `correlation-monitor`   | 6페어 상관계수 + 경제 서프라이즈 Beat/Miss + Z-score Alert                                                | briefing-lead (/이브닝·/주간·/크립토)              |
| `research-curator`      | 10섹터 × 4소스군 1차 자료, L1주간/L2월간/L3분기                                                           | briefing-lead (주기 매칭), `/리서치업데이트`       |
| `wiki-linter`           | KB 건강 점검 (만료·모순·고아 탐지 + 자동 수정)                                                            | briefing-lead Phase 0-LINT (/주간·/풀), `/KB점검`  |
| `reanalysis-tracker`    | 재분석 v{N} vs v{N-1} read-only 변화 추적 → `analysis/_reanalysis_runs/{YYYYMMDD}_run.md`                 | /재분석실행 Phase 2                                |
| `analyst-scraper`       | 애널리스트 리포트 수집 (PDF/웹/사후평가 3모드)                                                            | `/애널리스트PDF`, `/애널리스트스크랩`, `/성과리뷰` |

고아 에이전트 없음 — 22종 전부 위 경로로 연결 (2026-06-11 검증).

---

## 2. 커맨드 → 에이전트 라우팅 (22 커맨드)

| 진입 에이전트        | 커맨드                                                                                                                            |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `stock-analyst-lead` | /종목분석 /빠른분석 /비교분석 /손절계산 /재분석실행 /재분석점검                                                                   |
| `briefing-lead`      | /모닝브리핑 /이브닝브리핑 /주간리포트 /리밸런싱 /크립토브리핑 /모델포트폴리오 /글로벌인텔리전스 /풀브리핑 /성과리뷰 /내포트폴리오 |
| `kb-updater`         | /KB업데이트                                                                                                                       |
| `wiki-linter`        | /KB점검                                                                                                                           |
| `research-curator`   | /리서치업데이트                                                                                                                   |
| `report-generator`   | /리포트                                                                                                                           |
| `analyst-scraper`    | /애널리스트PDF /애널리스트스크랩                                                                                                  |

---

## 3. 종목분석 파이프라인 (stock-analyst-lead)

```
Step -2  세션 부트스트랩 (session-bootstrap.md read + stale 검증)
Step -1  모드 판별 (브리핑 → briefing-lead 위임 / 종목분석 → 계속)
Step  0  대상 유형 판별 (개별 종목 vs ETF → ETF면 etf-lead 단독 위임)
Phase 0  A: kb-updater(섹터 KB) → B: fetch_price.py(리드 직접 Bash)
         → C: data-collector → D: 파일 스캐폴딩(placeholder 생성)
Phase 1  병렬 3: company-overview ∥ financial-analyst ∥ momentum-analyst
         → 파일 생성 검증 + 폴백 (0 byte면 리드가 반환 메시지로 직접 Write)
Phase 2  순차 2: business-analyst → risk-analyst
Phase 3  scorecard-strategist (리드가 종목 유형 판별값 전달)
Phase 4  report-generator (Write 1회 atomic / 이전 HTML read 금지 / 실패 시 재호출 1회)
종료     검증 0~6 → commit → build_manifest → push → 배포
```

산출물 계약: `analysis/{종목코드}_{종목명}_v{N}/` (company.md, financial.md, business.md,
momentum.md, risk.md, scorecard.md, data.json) → `reports/{TICKER}_{이름}_{YYYYMMDD}.html` (직속만).

### 재분석 (/재분석실행) — 스케줄 슬롯 환경 갭

스케줄 슬롯의 리드는 Task 도구가 없어 서브에이전트 위임 불가.
**메인 스레드가 종목당 자급식 specialist를 직접 병렬 디스패치** → BLIND `_content.json` →
중앙 generator 스크립트(`scripts/reanalysis_generate_{날짜}.py`, 회차별 생성)가 6 MD+HTML 일괄 생성.
BLIND 원칙: 이전 v{N-1} 폴더·HTML·timeline read 0건 (앵커링 차단).

---

## 4. 브리핑 파이프라인 (briefing-lead)

```
Phase 0-LINT  wiki-linter (/주간·/풀 한정 자동)
선행 스크립트  fetch_price.py --market --save (/모닝·/주간)
              node web/scripts/fetch_fred.mjs (/모닝·/이브닝·/주간·/글로벌)
Phase 0-A     market-data-collector ∥ polymarket-collector (병렬 Task)
모듈 분석      global-macro-analyst / correlation-monitor / research-curator (명령별 조건부)
종합          briefing-lead 가 lead_{type}_{날짜}.md 작성 (debate-card·contrarian-card·시나리오)
출력          briefing-report-generator → reports/briefing/{type}_{YYYYMMDD}.html
종료          commit → manifest → push → 배포
```

연계 데이터 흐름: 수집 에이전트는 `knowledge-base/market/` 에 쓰고, 분석 에이전트는 그 파일만 읽는다
(3계층: 수집 → 공시 → 종합). research KB 강제 인용은 /주간·/글로벌·/내포·/풀 4종 한정 (v3.23).

---

## 5. 병목 방지 룰 (운영 계약 — 위반 시 시간 폭주·maxTurns 사고 재발)

1. **수집은 전부 위임** — 리드 직접 WebSearch 금지 (briefing-lead 는 도구 자체 제거).
   리드가 직접 실행하는 것은 결정적 스크립트(fetch_price.py, fetch_fred.mjs)뿐.
2. **KB Read 분리** — briefing-lead 는 market/·macro/·industry/ 직접 Read 금지
   (portfolio/·reference/·performance/ 만 허용). 메인 컨텍스트 폭주 방지.
3. **재호출 캡** — 서브에이전트 재호출 최대 1회, supplemental 모드 명시. 무한 재호출 차단.
4. **스캐폴딩 + 산출물 게이트** — 호출 전 placeholder 생성, 완료 후 파일 크기 검증, 빈 파일이면 폴백.
5. **Write 1회 atomic** — HTML 은 Edit 분할 금지. 실패 시 컨텍스트 폐기 후 깨끗한 재호출 1회.
6. **이전 산출물 read 금지** — 이전 HTML / 재분석 시 v{N-1} read 차단 (시간·앵커링 양쪽 방지).
7. **template 사전 Read 금지** — report-generator 는 report*template.py 를 읽지 않고
   명세 인라인 딕셔너리로 `generate*{티커}.py` 즉시 Write→실행 (과거 7회 중복 Read 사고).
8. **체크포인트** — Phase 종료마다 TodoWrite + session-bootstrap 갱신 (build_bootstrap.mjs --apply).
9. **응답 끊김 ≠ 미완** — git log + ls-files + ahead/behind 4단계 검증 후 재호출 판단 (3회 중복 호출 사고).

---

## 6. 검증 게이트 (오류 방지 계약)

| 게이트     | 내용                                                                                                                                 |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 검증 0     | 출력 경로 직속 강제 — `reports/*.html` 직속 + briefing/ + analyst/items/ + research/ 4곳만 (그 외 서브디렉토리 = 본서버 404)         |
| 검증 1~3   | HTML 존재 / git commit 존재 / session-bootstrap 갱신                                                                                 |
| 검증 4     | 디자인 표준 6항목 (다크·라이트 토글 포함, briefing-report-generator 표준)                                                            |
| 검증 5     | 한국어 검증 — `reference/korean_translation_rules.md` (매핑 사전 + 한글 비중 80%). **리포트 본문 한정, KB 데이터 파일 제외**         |
| 검증 6     | manifest staleness 자동 복구 (push 직전 build_manifest 재실행 + diff 시 commit)                                                      |
| 포트폴리오 | schema contract + 단위 테스트 34종(`web/scripts/__tests__/`) + sync 사전·사후 검증 + health_check.mjs (Vercel=STRICT / 로컬=LENIENT) |

manifest 계약: Vercel 빌드 컨테이너에 .git 없음 → **로컬 build_manifest 후 manifest.json commit 필수**.

---

## 7. 배포 (SSOT: CLAUDE.md)

`reports/**/*.html` 변경 push 직후에만: ① `vercel --prod --yes` (본서버) → ② `bash scripts/deploy_cloudflare.sh` (미러).
gh-pages 는 GitHub Actions 복원(2026-06-05) 후 자동 3채널째. KB·analysis·스크립트만 변경 시 배포 생략.

---

## 8. 자동화·감시 레이어 (LLM 불필요 — 결정적 스크립트, 2026-06-11 신설)

| 구성                                    | 스케줄               | 역할                                                                                                                                            |
| --------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/notify.sh`                     | (헬퍼)               | 공용 알림 — macOS 알림센터 + `.env.local` NTFY_TOPIC 설정 시 ntfy.sh 폰 푸시                                                                    |
| `scripts/daily_pick_update.sh`          | launchd 00:05        | DailyPick 갱신 + 실패 지점 6곳 알림. **로그는 ~/Library/Logs/stockanalyst/ (외장 SSD 경로 StandardOutPath 는 launchd spawn 실패 EX_CONFIG=78)** |
| `scripts/automation_watchdog.sh`        | launchd 06:40·10:30  | daily_pick 신선도 + 미푸시 커밋 + holdings_health 재생성 + portfolio_watch 호출                                                                 |
| `scripts/portfolio_watch.py`            | watchdog 경유        | 손절/목표가 도달·접근(2%) + 목표 비중 드리프트(`scripts/portfolio_targets.json`, 기본 5%p) 알림. KST 일별 디듀프                                |
| `web/scripts/build_holdings_health.mjs` | prebuild + watchdog  | 보유종목 × 최신 scorecard(손절·목표·등급) → `holdings_health.json` (git tracked — Vercel 컨테이너엔 analysis/ 없음)                             |
| `scripts/score_recommendations.py`      | /성과리뷰 Step 0     | 추천 기록 203행 자동 채점 → `auto_scoring.json` (기준가·수익률·hit/miss — LLM 산수 배제)                                                        |
| `scripts/analyst_lookup.py`             | data-collector Phase | 티커별 애널리스트 아카이브(290+건) 최근 의견 마크다운 출력                                                                                      |
| `scripts/lint_agents.mjs`               | 수동/명세 수정 후    | 커맨드↔에이전트 라우팅·Agent(...) 목록·참조 경로 정합성 검사                                                                                    |
| `scripts/measure_turns.mjs`             | 수동/진단            | subagent jsonl 에서 에이전트별 사용 턴 vs maxTurns 근접도 측정                                                                                  |

---

## 9. 알려진 제약 / 이월 항목 (2026-06-11 기준)

- **리드 명세 비대** (stock-analyst-lead 1,566L / briefing-lead 1,495L) — 사고 이력 기반 운영 룰 집적.
  분할은 다음 maxTurns 사고 발생 시 진행하기로 보류 (audit P2-1/2).
- `scripts/reanalysis_*_2026*.py` 날짜별 스크립트는 회차 provenance 로 의도적 보존 (audit FP-6~8 REFUTED).
- KB orphan 분류(P2-11)·상대 시간 표기(P2-12)·\_history timeline 통합(P2-20)은 사용자 결정 대기.
- 커맨드 v3.x 마커 lifecycle 정책(P2-4~8) 미수립 — 현재는 의도된 누적 마커로 운용.
