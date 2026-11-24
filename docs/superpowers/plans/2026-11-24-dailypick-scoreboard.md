# 데일리픽 성적표 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 데일리픽 전 기간(2026-05-14~)을 단기(픽 단위)·장기(추천 단위, 논지 판정으로 묶음) 두 층으로 채점해 `/daily-pick/scoreboard` 페이지로 보여 주고, 매일·매주 자동 갱신한다.

**Architecture:** 픽 원장(JSON, git 추적) ← 매일 픽 생성 시 append + 1회 git 소급. 가격은 python/yfinance 로 로컬 캐시(`analysis/_daily_pick/prices.json`, gitignore)에 받고, 채점 로직은 순수 Node 모듈(`node --test`)로 원장+가격+논지판정 → `daily_pick_eval.json`(git 추적) 생성. Astro 정적 페이지가 eval JSON 만 읽는다. 논지 판정은 에이전트가 하되 대상 산출·anchor 계산은 결정적 스크립트.

**Tech Stack:** Node 20+ ESM (`node:test`), Astro 4, Python 3 + yfinance, bash(launchd), git.

**Spec:** `docs/superpowers/specs/2026-11-24-dailypick-scoreboard-design.md` (executors read both)

## Global Constraints

- 커밋은 **명시 경로만** (`git add <path>...`). 작업트리의 다른 변경(재분석 정리 등) 절대 포함 금지. `.env*` 파일 Read 금지.
- 커밋 메시지 끝: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
- UI 문구·주석은 한국어. 테스트: `cd web && npm test` (= `node --test scripts/__tests__/*.test.mjs`) 전체 통과 유지.
- `analysis/**` 는 gitignore — Vercel 빌드에 없음. 페이지·빌드는 커밋된 `web/src/data/*.json` 만 의존. 채점/가격 스크립트를 `prebuild` 에 넣지 않는다.
- 벤치마크: US = `^GSPC`, KRX = `^KS11`. 단기 기간 `[5, 20]` 메인 20 / 장기 기간 `[60, 120, 250]` 메인 120 / 만기 250 거래일.
- 적중 = 해당 기간 초과수익(종목 − 벤치마크, %p) > 0. 점수대 `<78` / `78≤s<81` / `≥81` (표기 75–77 / 78–80 / 81+). 집계 n < 10 → `small_sample: true`.
- 진입가 = 바 날짜 ≥ 픽일인 첫 바 종가. 장기 마감: 달성(일중 고가 ≥ tp, 청산가 = tp, 단 그 바 시가 ≥ tp 면 시가) / 논지 교체(`전환` 픽 진입 바 종가) / 만기(진입 후 250번째 바 종가) 중 먼저. 마감 후 기간 칸 = 마감 값 고정.
- 같은 분석 폴더(`analysis_dir`) 재픽 = 자동 `동일`(에이전트 불필요, eval 내부 계산, thesis 파일엔 저장 안 함 — spec §5.2 의 auto 행을 계산값으로 대체, 화면엔 `judged_by: "auto-same-version"` 로 표기).
- 배포: push → Vercel 자동 빌드(`vercel ls` 로 Ready 확인, sandbox 우회 필요) + `bash scripts/deploy_cloudflare.sh` 수동(sandbox 우회). 완료 링크는 `https://stock-analyst-jungwon1.vercel.app/`.
- 파일 경로(고정):
  - 원장 `web/src/data/daily_pick_ledger.json`
  - 판정 `web/src/data/daily_pick_thesis.json`, override `web/src/data/daily_pick_thesis_overrides.json`
  - 결과 `web/src/data/daily_pick_eval.json`
  - 가격 캐시 `analysis/_daily_pick/prices.json`

## Review Focus

1. **가격이 없는 티커/날짜** (yfinance 빈 응답, 상장폐지): 행은 `status: "no_price"` 로 남고 집계에서 제외, 스크립트는 계속 — Task 4 테스트 `no price series → no_price row`.
2. **오늘·주말 픽처럼 진입 바가 아직 없는 픽**: `pending` 으로 표시, 실패로 세지 않음 — Task 4 테스트 `entry bar not yet available`.
3. **tp 가 null 이거나 터무니없는 값**: 달성 마감 없음, `tp_status: "none"` — Task 2(소급 시 ±80% 가드)·Task 5(`no tp → never 달성`).
4. **같은 날 재실행·재생성**: 원장은 date 기준 upsert, 중복 행 0 — Task 1 테스트 `upsert replaces same date`.
5. **벤치마크와 종목의 휴장일 불일치** (US 휴일에 KR 종목 등): 벤치마크 값은 해당 날짜 이하 마지막 바 종가 — Task 4 테스트 `benchmark uses last bar on or before date`.

---

## File Structure

| 파일                                                                                                    | 책임                                                   |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `web/scripts/lib/daily_pick_ledger.mjs` (신규)                                                          | 원장 행 생성·등급 정규화·upsert (순수)                 |
| `web/scripts/lib/analysis_archive.mjs` (신규)                                                           | 분석 폴더 → 라이브 폴더/tar.gz 아카이브 위치·파일 읽기 |
| `web/scripts/backfill_daily_pick_ledger.mjs` (신규, 1회성)                                              | git 이력 → 원장 소급                                   |
| `web/scripts/build_daily_pick.mjs` (수정)                                                               | 픽 생성 후 원장 upsert                                 |
| `scripts/fetch_daily_pick_prices.py` (신규)                                                             | 원장 티커+벤치마크 일봉 → 가격 캐시                    |
| `web/scripts/lib/daily_pick_eval.mjs` (신규)                                                            | 채점 순수 로직 (단기·장기·집계)                        |
| `web/scripts/build_daily_pick_eval.mjs` (신규)                                                          | CLI: eval 생성 / 미판정 큐 / override 무효 정리        |
| `web/src/pages/daily-pick/scoreboard.astro` (신규)                                                      | 성적표 페이지                                          |
| `web/src/components/widgets/DailyPick.astro` (수정)                                                     | "성적표 →" 링크                                        |
| `scripts/daily_pick_update.sh`, `scripts/automation_watchdog.sh`, `.claude/commands/성과리뷰.md` (수정) | 자동화                                                 |
| 테스트: `web/scripts/__tests__/daily_pick_ledger.test.mjs`, `daily_pick_eval.test.mjs` (신규)           |                                                        |

---

### Task 1: 원장 라이브러리 + 일일 append

**Files:**

- Create: `web/scripts/lib/daily_pick_ledger.mjs`
- Modify: `web/scripts/build_daily_pick.mjs` (main 의 비-VERCEL 경로, `writeFile(OUTPUT_JSON…)` 직후 ~line 508)
- Test: `web/scripts/__tests__/daily_pick_ledger.test.mjs`

**Interfaces:**

- Produces:
  - `normalizeGrade(raw: string|null) -> '강력매수'|'매수'|null` — 문자열 안 첫 등급어(`강력매수` 우선 검사 후 `매수`), 없으면 null.
  - `ledgerRowFromPick(payload: DailyPickJson, regime: object|null) -> LedgerRow|null` — payload.pick 이 null 이면 null.
  - `LedgerRow = { date, ticker, name, market, score, grade, version, analysis_dir, analysis_date, tp_price, reasons, regime }`; `regime = {risk_regime, weight_set, trend, vol_regime, fear_greed} | null`; `date = payload.pick_date`.
  - `upsertLedgerRow(ledger: LedgerRow[], row: LedgerRow) -> LedgerRow[]` — 같은 date 행 교체, date 오름차순 정렬, 새 배열 반환.

- [ ] **Step 1: 실패 테스트 작성** (`daily_pick_ledger.test.mjs`)
  - `normalizeGrade('강력매수 — TP $475,') === '강력매수'`, `normalizeGrade('매수') === '매수'`, `normalizeGrade('— TP $295') === null`, `normalizeGrade(null) === null`.
  - `ledgerRowFromPick({pick_date:'2026-11-19', pick:{ticker:'TSM',name:'TSMC',score:77,grade:'매수',version:'v22',analysis_dir:'TSM_TSMC_v22',analysis_date:'2026-11-19',market:'US',tp_price:445,reasons:['a']}}, {risk_regime:'리스크오프',weight_set:'하락장',trend:'하락',vol_regime:'고',fear_greed:17, vix:26})` → `date '2026-11-19'`, `grade '매수'`, `regime` 은 5개 키만(vix 제외).
  - `ledgerRowFromPick({pick_date:'2026-11-20', pick:null}, null) === null`.
  - `upsert replaces same date`: 2행 원장에 같은 date 새 행 upsert → 길이 2, 해당 행 ticker 교체, date 정렬 유지.
- [ ] **Step 2: 실패 확인** — `cd web && node --test scripts/__tests__/daily_pick_ledger.test.mjs` → FAIL (모듈 없음)
- [ ] **Step 3: `daily_pick_ledger.mjs` 구현** (위 시그니처)
- [ ] **Step 4: 통과 확인** — 같은 명령 → PASS
- [ ] **Step 5: `build_daily_pick.mjs` 에 append 추가** — 비-VERCEL 경로에서 payload 기록 직후: `knowledge-base/market/regime.json` 읽기(실패 시 null) → `ledgerRowFromPick` → null 아니면 원장 파일 읽기(없으면 `[]`) → `upsertLedgerRow` → 2-space JSON 기록. VERCEL 경로·analysis 부재 경로에서는 원장 손대지 않음.
- [ ] **Step 6: 검증** — `cd web && node scripts/build_daily_pick.mjs` 를 2회 실행 → `node -e "const l=require('./src/data/daily_pick_ledger.json');console.log(l.length,l.at(-1).date)"` 가 1행·오늘 날짜(2회째도 1행). `npm test` 전체 PASS.
- [ ] **Step 7: 커밋** — `git add web/scripts/lib/daily_pick_ledger.mjs web/scripts/__tests__/daily_pick_ledger.test.mjs web/scripts/build_daily_pick.mjs` (원장 파일은 Task 2 소급 후 커밋). 메시지 `feat(daily_pick): 픽 원장 라이브러리 + 일일 append`.

### Task 2: 아카이브 리더 + 원장 소급

**Files:**

- Create: `web/scripts/lib/analysis_archive.mjs`, `web/scripts/backfill_daily_pick_ledger.mjs`
- Create(산출): `web/src/data/daily_pick_ledger.json`
- Test: `web/scripts/__tests__/daily_pick_ledger.test.mjs` (archive 함수 추가)

**Interfaces:**

- Consumes: Task 1 `normalizeGrade`, `upsertLedgerRow`, `ledgerRowFromPick`; `web/scripts/lib/scorecard_parser.mjs` 의 `parseTargetPrice(md)`, `parseGrade(md)`.
- Produces:
  - `findArchiveName(analysisDir: string, names: string[]) -> string|null` — `${analysisDir}_YYYYMMDD.tar.gz` 정확 매칭(접두 충돌 방지: `MU_Micron_v2` 가 `MU_Micron_v20_…` 에 매칭되면 안 됨), 복수면 날짜 최신.
  - `readAnalysisFile(projectRoot: string, analysisDir: string, filename: string) -> Promise<string|null>` — `analysis/{dir}/{filename}` 있으면 그것, 없으면 `analysis/_archive/` 의 tarball 에서 `tar -xzOf <tar> {dir}/{filename}` (execFile). 없으면 null.

- [ ] **Step 1: 실패 테스트** — `findArchiveName('MU_Micron_v2', ['MU_Micron_v20_20261001.tar.gz','MU_Micron_v2_20260601.tar.gz']) === 'MU_Micron_v2_20260601.tar.gz'`; 매칭 없음 → null.
- [ ] **Step 2: 실패 확인** → FAIL
- [ ] **Step 3: `analysis_archive.mjs` 구현**
- [ ] **Step 4: 통과 확인** → PASS
- [ ] **Step 5: 소급 스크립트 구현** `backfill_daily_pick_ledger.mjs` (CLI, `--dry-run` 지원):
  - `git log --format=%H %cI -- web/src/data/daily_pick.json` 전 커밋 → 각 `git show` 파싱 → `pick_date` 별 **커밋 시각이 가장 늦은** payload 채택, pick null 은 건너뜀.
  - version 진실 = `analysis_dir` (원장 `version` 필드는 `analysis_dir` 끝의 `vN` 으로 재기록).
  - regime: `git log --format=%H %cI -- knowledge-base/market/regime.json` → 각 스냅샷의 `date` 필드 → 픽일 이하 최신 스냅샷. 없으면 null.
  - grade: `normalizeGrade(pick.grade)`; null 이면 `readAnalysisFile(..., 'scorecard.md')` → `parseGrade`.
  - tp: pick.tp_price 없으면 scorecard `parseTargetPrice` → 없으면 `analysis/_history/{TICKER}_*_timeline.json` 에서 해당 `folder` 행 `target_price`(숫자 추출) → 그래도 없으면 null. 채운 tp 가 `pick.current_price ?? pick.buy_price` 대비 ±80% 밖이면 null.
  - 기존 원장 행(오늘 append 분)과 병합(upsert), 기록.
  - 끝에 요약 출력: 행 수, grade null 수, tp null 수/비율, regime null 수.
- [ ] **Step 6: 실행·검증** — `cd web && node scripts/backfill_daily_pick_ledger.mjs` → 행 ≥ 161, grade null 0 (0 아니면 해당 행 출력해 원인 수정 후 재실행), tp null 비율 보고. 첫 날짜 `2026-05-14`.
- [ ] **Step 7: 커밋** — `git add web/scripts/lib/analysis_archive.mjs web/scripts/backfill_daily_pick_ledger.mjs web/scripts/__tests__/daily_pick_ledger.test.mjs web/src/data/daily_pick_ledger.json`, 메시지 `feat(daily_pick): 아카이브 리더 + 원장 소급 (N행)`.

### Task 3: 가격 캐시 수집

**Files:**

- Create: `scripts/fetch_daily_pick_prices.py`

**Interfaces:**

- Consumes: 원장 JSON.
- Produces: `analysis/_daily_pick/prices.json` = `{ "generated_at": ISO, "symbols": { "<ticker>": {"symbol": "005930.KS", "dates": ["YYYY-MM-DD",...], "open": [...], "high": [...], "close": [...]} , "^GSPC": {...}, "^KS11": {...} } }` — 키는 **원장 ticker** (벤치마크는 심볼 그대로). 날짜는 거래소 현지 날짜.

- [ ] **Step 1: 구현** — 첫 줄 `# -*- coding: utf-8 -*-` (스케줄 C locale 대응). 원장 ticker 집합 + 벤치마크 2개. 심볼: US 그대로, KRX 6자리 → `.KS`, 응답 비면 `.KQ` 재시도. 기간: 원장 최소 date − 7일 ~ 오늘. `yf.download(..., auto_adjust=False, progress=False, group_by="ticker", threads=True)` 후 심볼별 `dropna(subset=["Close"])`. 실패 심볼은 stderr 경고 후 제외. 벤치마크 2개 중 하나라도 없으면 exit 1, 그 외 exit 0. 마지막 줄 `[ok] prices: <n>/<m> symbols`.
- [ ] **Step 2: 검증** — `python3 scripts/fetch_daily_pick_prices.py` → `[ok]` 출력, `python3 -c "import json;d=json.load(open('analysis/_daily_pick/prices.json'))['symbols'];print(len(d),d['^GSPC']['dates'][-1],d['005930']['symbol'])"` → 원장 고유 티커 수+2, 최근 거래일, `005930.KS`.
- [ ] **Step 3: 커밋** — `git add scripts/fetch_daily_pick_prices.py`, 메시지 `feat(daily_pick): 성적표용 가격 캐시 수집기`.

### Task 4: 채점 코어 — 단기 리뷰

**Files:**

- Create: `web/scripts/lib/daily_pick_eval.mjs`
- Test: `web/scripts/__tests__/daily_pick_eval.test.mjs`

**Interfaces:**

- Consumes: `LedgerRow` (Task 1), prices `symbols` 형식 (Task 3).
- Produces:
  - `SHORT_HORIZONS = [5, 20]`, `LONG_HORIZONS = [60, 120, 250]`, `BENCH = {US:'^GSPC', KRX:'^KS11'}`.
  - `entryIndex(series, date: string) -> number` (없으면 -1).
  - `closeOnOrBefore(series, date: string) -> number|null`.
  - `scoreBand(score: number) -> '75-77'|'78-80'|'81+'`.
  - `buildShortRows(ledger, symbols) -> ShortRow[]`; `ShortRow = { date, ticker, name, score, band, weight_set, status: 'ok'|'pending'|'no_price', entry_date, entry_price, h: { '5': {ret, excess, hit}|null, '20': ... } }` — ret/excess 는 % 단위 소수 둘째 자리 반올림 안 함(원값), 미도달 기간은 null.
  - `summarize(rows, key: string) -> { n, hit_rate, avg_return, avg_excess, small_sample }` — `rows[i].h[key]` 가 null 아닌 것만, n=0 이면 나머지 null.

- [ ] **Step 1: 실패 테스트** (합성 시계열 헬퍼 `mkSeries(startDate, closes, {opens,highs})` 를 테스트 파일에 정의, 영업일만 생성)
  - `entry bar not yet available`: 픽일이 마지막 바 이후 → `status 'pending'`, h 전부 null.
  - `entry uses first bar on or after pick date`: 토요일 픽 → 월요일 바 종가가 entry_price.
  - `5d return and excess`: 종목 100→110 (5바 뒤), 벤치 100→104 → `ret 10`, `excess 6`, `hit true`; 20d 미도달 → `h['20'] === null`.
  - `benchmark uses last bar on or before date`: 평가일에 벤치 바 없음 → 직전 바 종가 사용.
  - `no price series → no_price row`.
  - `scoreBand(77.6)==='75-77'`, `scoreBand(78)==='78-80'`, `scoreBand(81)==='81+'`.
  - `summarize` : hit 3/4 → `hit_rate 0.75`, `small_sample true` (n<10); 빈 입력 → `{n:0, hit_rate:null, ...}`.
- [ ] **Step 2: 실패 확인** — `cd web && node --test scripts/__tests__/daily_pick_eval.test.mjs` → FAIL
- [ ] **Step 3: 구현** (위 시그니처)
- [ ] **Step 4: 통과 확인** → PASS
- [ ] **Step 5: 커밋** — `git add web/scripts/lib/daily_pick_eval.mjs web/scripts/__tests__/daily_pick_eval.test.mjs`, 메시지 `feat(daily_pick): 성적표 채점 코어 — 단기`.

### Task 5: 채점 코어 — 장기 리뷰 (추천 묶음·마감)

**Files:**

- Modify: `web/scripts/lib/daily_pick_eval.mjs`
- Test: `web/scripts/__tests__/daily_pick_eval.test.mjs`

**Interfaces:**

- Consumes: Task 4 헬퍼.
- Produces:
  - `Judgment = { date, ticker, anchor_date, anchor_version, version, verdict: '동일'|'보강'|'전환', rationale, judged_at, judged_by }`; overrides = `{ "<ticker>@<date>": '동일'|'보강'|'전환' }`.
  - `buildRecommendations(ledger, symbols, judgments: Judgment[], overrides) -> { recs: Rec[], pending: PendingItem[], invalid: Judgment[] }`.
  - `Rec = { ticker, name, anchor_date, anchor_version, anchor_score, band, weight_set, entry_date, entry_price, tp_price, tp_status: 'none'|'open'|'hit', repicks: [{date, version, verdict, rationale, judged_by}], close: {reason: '달성'|'논지 교체'|'만기', date, price, bars} | null, h: {'60':…, '120':…, '250':…}, status: 'ok'|'pending'|'no_price', provisional: boolean }`.
  - `PendingItem = { ticker, date, version, analysis_dir, anchor_date, anchor_version, anchor_analysis_dir }` — 티커별 **가장 이른** 미판정 재픽만.

알고리즘 (티커별 픽을 날짜순 순회; 테스트가 결정하지 못하는 부분):

```
open = null
for pick in picksOfTicker:
  if open and open.close(가격 기준: 달성/만기) 날짜 < pick 진입일: open 마감 확정 → open = null
  if open is null: open = newRec(pick); continue
  verdict = overrides[ticker@date] ?? (pick.analysis_dir == open.anchor_analysis_dir ? '동일'(auto)
            : judgment(ticker,date) where judgment.anchor_date == open.anchor_date)  # anchor 불일치 judgment → invalid 에 추가, 미판정 취급
  if verdict 없음: pending.push(...); open.provisional = true; 이 티커의 이후 픽은 모두 건너뜀(묶음 미확정); break
  if verdict == '전환': open 을 '논지 교체'로 마감(그 픽 진입 바, 단 가격 기준 마감이 더 이르면 그쪽) ; open = newRec(pick)
  else open.repicks.push(...)
```

가격 기준 마감: 진입 후 바 순회, 첫 `high ≥ tp` 바 → 달성(청산가 `open ≥ tp ? open : tp`), 아니면 250번째 바 → 만기. 기간 값: N번째 바가 마감 바 이후면 마감 청산가·마감일 벤치 종가로 고정. 마감됐으면 모든 기간 확정, 아니면 미도달 기간 null.

- [ ] **Step 1: 실패 테스트**
  - `same analysis_dir repick → auto 동일`: 같은 dir 재픽 → recs 1개, repicks[0].judged_by `'auto-same-version'`.
  - `전환 closes old rec at new entry`: 판정 `전환` → recs 2개, recs[0].close `{reason:'논지 교체', price:<새 픽 진입 종가>}`, recs[1].entry_price 동일 값.
  - `TP hit closes at tp, gap opens at open`: high ≥ tp 첫 바 → 청산가 = tp; 그 바 open > tp 인 별도 케이스 → 청산가 = open.
  - `no tp → never 달성`: tp null → `tp_status 'none'`, 250바 후 만기.
  - `frozen horizons after close`: 40바째 달성 → `h['120'].ret` = 달성 수익률, `h['250']` 도 같은 값.
  - `repick after closed rec starts new rec without judgment`: 달성 마감 후 재픽 → 판정 없이 recs 2개, pending 0.
  - `unjudged repick → pending, later picks skipped`: 판정 없는 재픽 2개 → pending 1건(첫 재픽), recs[0].provisional true.
  - `override wins and invalidates stale judgment`: 같은 날짜에 judgment `동일` + override `전환` → recs 2개; 이후 재픽의 judgment(anchor_date = 옛 anchor) → invalid 에 포함, 그 픽은 pending.
- [ ] **Step 2: 실패 확인** → FAIL
- [ ] **Step 3: 구현**
- [ ] **Step 4: 통과 확인** → PASS
- [ ] **Step 5: 커밋** — 같은 두 파일, 메시지 `feat(daily_pick): 성적표 채점 코어 — 장기 추천 묶음·마감`.

### Task 6: 집계 + eval CLI + 판정 큐

**Files:**

- Modify: `web/scripts/lib/daily_pick_eval.mjs`
- Create: `web/scripts/build_daily_pick_eval.mjs`
- Create(산출): `web/src/data/daily_pick_thesis.json` (`[]`), `web/src/data/daily_pick_thesis_overrides.json` (`{}`), `web/src/data/daily_pick_eval.json`
- Test: `web/scripts/__tests__/daily_pick_eval.test.mjs`

**Interfaces:**

- Consumes: Task 4·5.
- Produces:
  - `breakdown(rows, keyFn, horizonKey) -> Array<{ key, ...summarize }>` (key 오름차순, null key → `'기록 없음'`).
  - `concentration(shortRows, horizonKey='20') -> { equal_weight_hit_rate, top5_share, by_ticker: [{ticker, picks, hit_rate}] }` — 상위5 비중 = 픽 수 상위 5 종목 픽 합 / 전체 픽.
  - `buildEval({ ledger, symbols, judgments, overrides, now }) -> EvalJson` = `{ generated_at, counts: {picks, evaluated_short, recs, pending}, short: {rows, summary: {'5':…, '20':…}, by_band, by_regime}, long: {recs, summary: {'60','120','250'}, by_band, by_regime, close_reasons: {달성, '논지 교체', 만기, 진행중}, tp_hit_rate, avg_bars_to_tp}, concentration, pending: {items, invalid_count, oldest_unjudged_date} }`. 단기 by_band/by_regime 은 메인 `'20'`, 장기는 `'120'`.
  - CLI `node scripts/build_daily_pick_eval.mjs [--judgments-extra <file>] [--queue [--ticker T]] [--prune-invalid]`:
    - 기본: 원장·가격캐시·thesis·overrides(+extra) → eval 기록. 가격 캐시 없으면 exit 1(기존 eval 유지).
    - `--queue`: eval 기록 없이 `pending.items` 를 JSON 출력(`--ticker` 로 필터). 각 항목에 `anchor_source`/`target_source` = `readAnalysisFile` 로 확인한 위치(`live:analysis/...` | `archive:analysis/_archive/...tar.gz` | `missing`).
    - `--prune-invalid`: invalid 판정 행을 thesis 파일에서 제거하고 제거 수 출력.

- [ ] **Step 1: 실패 테스트** — `breakdown` null key → `'기록 없음'`; `concentration`: A 3픽(적중 3), B 1픽(실패) → `equal_weight_hit_rate 0.5`, `top5_share 1`; `buildEval` 스모크: 원장 3행·합성 가격 → `counts.picks 3`, `short.summary['5'].n` 기대값.
- [ ] **Step 2: 실패 확인** → FAIL
- [ ] **Step 3: 구현** (lib 함수 + CLI)
- [ ] **Step 4: 통과 확인** → PASS, `npm test` 전체 PASS
- [ ] **Step 5: 실데이터 실행** — thesis `[]`·overrides `{}` 파일 생성 → `cd web && node scripts/build_daily_pick_eval.mjs` → `counts` 출력 확인(picks = 원장 행 수, pending ≈ 재픽 가진 티커 수 이하). `node scripts/build_daily_pick_eval.mjs --queue --ticker NVDA` → 1건, source 가 `missing` 아님.
- [ ] **Step 6: 커밋** — `git add web/scripts/lib/daily_pick_eval.mjs web/scripts/build_daily_pick_eval.mjs web/scripts/__tests__/daily_pick_eval.test.mjs web/src/data/daily_pick_thesis.json web/src/data/daily_pick_thesis_overrides.json web/src/data/daily_pick_eval.json`, 메시지 `feat(daily_pick): 성적표 집계 + eval CLI + 판정 큐`.

### Task 7: 과거 논지 판정 소급 (에이전트 운영)

**Files:**

- Modify(산출): `web/src/data/daily_pick_thesis.json`, `web/src/data/daily_pick_eval.json`
- 임시: `/private/tmp/claude-501/-Volumes---SSD-----AI------------------/6d516fd1-2269-49b8-9adf-94a38f7e54d3/scratchpad/thesis_<TICKER>.json`

**Interfaces:**

- Consumes: Task 6 CLI (`--queue --ticker`, `--judgments-extra`), Task 2 `readAnalysisFile` 위치 정보.

- [ ] **Step 1: 대상 티커 목록** — `cd web && node scripts/build_daily_pick_eval.mjs --queue` → pending 있는 티커 목록.
- [ ] **Step 2: 티커별 general-purpose 에이전트 병렬 실행** (동시 최대 8, 나머지는 뒤이어). 각 에이전트 지시(요지):
  - 반복: `node scripts/build_daily_pick_eval.mjs --queue --ticker <T> --judgments-extra <tmp>` → 항목 없으면 종료.
  - 항목의 anchor/target 분석을 읽는다: live 면 파일 직접, archive 면 `tar -xzOf <tar> <dir>/scorecard.md` (+ 있으면 `_report_data.json`, `business.md` 앞부분). 디스크에 풀지 않는다.
  - spec §7 기준표 3항목(핵심 성장 동력 / 밸류에이션 근거 / 촉매·리스크)으로 판정: 셋 같음 `동일`, ①같고 ②③ 보강 `보강`, ①바뀜 `전환`.
  - `<tmp>` JSON 배열에 Judgment 행 append (`judged_by: "agent"`, `judged_at` = 오늘, rationale 한 줄 `v{a} 근거=… / v{b}=… → 판정`, 120자 이내).
  - 프로젝트 파일 수정·커밋 금지. 최종 보고: 판정 수, 분포, 애매했던 건.
- [ ] **Step 3: 병합** — 메인이 모든 tmp 를 thesis 파일에 합치고(중복 키 `ticker@date` 없음 확인) `node scripts/build_daily_pick_eval.mjs` → `pending.items` 0 될 때까지 Step 2 반복(남은 티커만).
- [ ] **Step 4: 검증** — thesis 행 수 ≤ 119, `pending.invalid_count 0`, 판정 분포·recs 수 보고. 무작위 3건 rationale 을 원문과 대조해 납득 가능한지 확인.
- [ ] **Step 5: 커밋** — `git add web/src/data/daily_pick_thesis.json web/src/data/daily_pick_eval.json`, 메시지 `data(daily_pick): 과거 재픽 논지 판정 소급 N건`.

### Task 8: 성적표 페이지 + 위젯 링크

**Files:**

- Create: `web/src/pages/daily-pick/scoreboard.astro`
- Modify: `web/src/components/widgets/DailyPick.astro` (~line 114 `.pick-actions` 또는 헤더 영역)

**Interfaces:**

- Consumes: `web/src/data/daily_pick_eval.json` (Task 6 `EvalJson`). 레이아웃 `../../layouts/Base.astro` (패턴: `web/src/pages/analyst/scoreboard.astro`).

- [ ] **Step 1: 페이지 구현** — spec §9 구성 순서 그대로: 헤더(픽 수·평가완료·추천 수·판정 대기) → 단기/장기 탭(JS 없이 `<details>` 또는 라디오+CSS; 기본 단기) → 메인 지표 4칸(단기 20일 / 장기 120일, 장기는 목표가 도달률) → 기간별 표 → 점수대별 → 장세별 → 종목 쏠림 → 목록(단기 행 / 장기 추천 행, 장기 행 `<details>` 펼치면 재추천별 판정+근거, `judged_by` auto 는 "같은 분석" 표기) → 집계 기준(접힘, spec §6 요약). 값 없음 `—`, `small_sample` 이면 "표본 적음" 배지, 대기는 `대기`. 수익률 % 소수 1자리, +/− 부호, 상승 `var(--up)`류 기존 색 변수 사용(analyst scoreboard 의 CSS 변수 관례 따름). 다크/라이트 모두, 표는 `.table-wrap{overflow-x:auto}`, th nowrap.
- [ ] **Step 2: 위젯 링크** — DailyPick 에 `<a href="/daily-pick/scoreboard">성적표 →</a>` (기존 `btn-report` 스타일 재사용 또는 헤더 날짜 옆 작은 링크).
- [ ] **Step 3: 빌드 검증** — `cd web && npx astro build` 성공, `ls dist/daily-pick/scoreboard/index.html`, `grep -c "표본 적음\|적중률" dist/daily-pick/scoreboard/index.html` ≥ 1, `grep -o 'href="/daily-pick/scoreboard"' dist/index.html` 존재.
- [ ] **Step 4: 눈으로 확인** — 빌드 산출 복사본에서 `window.location.replace(` 무력화 + `html{visibility:visible!important}` 주입 후 headless Chrome 1280px·500px 다크/라이트 스크린샷 → 표 깨짐·세로 한글 깨짐 없음 확인. 복사본 삭제.
- [ ] **Step 5: 커밋** — `git add web/src/pages/daily-pick/scoreboard.astro web/src/components/widgets/DailyPick.astro`, 메시지 `feat(daily_pick): 성적표 페이지 + 위젯 링크`.

### Task 9: 자동화 연결 (일일·주간·감시)

**Files:**

- Modify: `scripts/daily_pick_update.sh`, `scripts/automation_watchdog.sh`, `.claude/commands/성과리뷰.md`

**Interfaces:**

- Consumes: Task 3 수집기, Task 6 CLI.

- [ ] **Step 1: `daily_pick_update.sh`** —
  - step 3(build) 직후, step 4(변경 감지) 전에: `cd "$PROJECT_ROOT" && python3 scripts/fetch_daily_pick_prices.py && (cd web && node scripts/build_daily_pick_eval.mjs)`; 실패 시 `log` + `notify_fail "성적표 채점 실패 — 기존 eval 유지"` 후 계속(픽 발행은 진행). 실패 시 eval 파일은 `git checkout -- web/src/data/daily_pick_eval.json` 로 되돌림.
  - step 4 의 무변경 판정에 원장·eval 포함: `git diff --quiet web/src/data/daily_pick.json web/src/data/daily_pick_ledger.json web/src/data/daily_pick_eval.json`.
  - step 6 `git add` 에 `web/src/data/daily_pick_ledger.json web/src/data/daily_pick_eval.json` 추가. 커밋 메시지는 기존 형식 유지.
  - pull 전 `git checkout -- web/src/data/` 리셋은 그대로 둔다(원장은 같은 회차에 커밋되므로 안전 — 커밋 실패 시 다음 회차 build 가 오늘 행을 다시 upsert).
- [ ] **Step 2: `automation_watchdog.sh`** — 기존 `notify_warn` 패턴으로 2개 점검 추가: (a) `daily_pick_eval.json` 의 `generated_at` 날짜가 KST 오늘 기준 2일 초과 경과 → `notify_warn "데일리픽 성적표 미갱신 (generated_at=…)" high`; (b) `pending.oldest_unjudged_date` 가 14일 초과 경과 → `notify_warn "데일리픽 논지 판정 대기 14일 초과 — 토요일 /성과리뷰 확인"`.
- [ ] **Step 3: `.claude/commands/성과리뷰.md`** — "★ 후속 단계 — 애널리스트 사후 평가" 뒤에 "★ 후속 단계 — 데일리픽 논지 판정" 절 추가: (1) `cd web && node scripts/build_daily_pick_eval.mjs --prune-invalid` (2) `--queue` 로 대상 확인, 0건이면 생략 (3) 티커별로 Task 7 Step 2 절차(메인 인라인 또는 general-purpose 에이전트) — 기준표·rationale 형식 동일, thesis 파일에 직접 append (4) `node scripts/build_daily_pick_eval.mjs` 재실행, pending 0 확인 (5) 커밋 `git add web/src/data/daily_pick_thesis.json web/src/data/daily_pick_eval.json` 만, 메시지 `data(daily_pick): 주간 논지 판정 N건`. 판정은 동결 — 기존 행 수정 금지(override 파일만 사람이 편집).
- [ ] **Step 4: 검증** —
  - `bash -n scripts/daily_pick_update.sh && bash -n scripts/automation_watchdog.sh` 오류 없음.
  - 감시 (a): eval 사본의 `generated_at` 을 5일 전으로 바꿔 점검 함수(또는 해당 블록)를 그 사본 대상으로 실행 → 경고 문구 출력 확인, 원본 복구.
  - 일일 경로: 가격 수집 + eval CLI 를 스크립트와 같은 순서로 수동 실행해 성공 확인. (`daily_pick_update.sh` 전체 실행은 push·배포까지 하므로 Task 10 에서 1회.)
- [ ] **Step 5: 커밋** — `git add scripts/daily_pick_update.sh scripts/automation_watchdog.sh ".claude/commands/성과리뷰.md"`, 메시지 `chore(daily_pick): 성적표 일일 채점·주간 판정·감시 연결`.

### Task 10: 통합 배포·완료 보고

- [ ] **Step 1:** `cd web && npm test` 전체 PASS, `npx astro build` 성공.
- [ ] **Step 2:** `git push origin main` → `vercel ls`(sandbox 우회) Ready 확인 → `curl -s https://stock-analyst-jungwon1.vercel.app/daily-pick/scoreboard/ | grep -c 적중률` ≥ 1 → `bash scripts/deploy_cloudflare.sh`(sandbox 우회).
- [ ] **Step 3:** 다음 자정 launchd 회차 로그(`~/Library/Logs` 의 daily-pick 로그) 또는 사용자 동의 하에 `bash scripts/daily_pick_update.sh` 1회 실행으로 원장 append + eval 갱신 + 커밋 경로 확인.
- [ ] **Step 4: 보고** — 원장 행 수·tp 결측률, 판정 수·분포, 단기 20일/장기 120일 메인 지표, 쏠림 지표, 남은 한계.
