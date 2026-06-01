# 전체 프로젝트 종합 점검 — 2026-06-01

**범위**: 8섹터 × 3R (R1 cavecrew × 8 / R2 Explore × 8 / R3 종합 × 1)
**총 발견**: 약 132건 (R1 발견 ~250건 — R2 false-positive 89건 제거 후 + R2 신규 21건 추가)
**검증 방식**: R1 발견 → R2 교차검증 → R3 우선순위 재분류

---

## 요약 표

| 섹터          | P0    | P1     | P2     | P3    | 비고                                           |
| ------------- | ----- | ------ | ------ | ----- | ---------------------------------------------- |
| S1 Agents     | 0     | 4      | 3      | 0     | research-curator orphan REFUTED                |
| S2 Commands   | 3     | 4      | 5      | 0     | 4건 REFUTED (deploy/리포트/KB중복/재분석)      |
| S3 Scripts    | 1     | 3      | 2      | 1     | 3 generate\_\*.py REFUTED                      |
| S4 KB+DB      | 0     | 2      | 4      | 1     | 한글 비중 30→88 (설계 의도 인정)               |
| S5 Web        | 0     | 3      | 3      | 0     | TypeCounts orphan 신규 / A11y 14/16            |
| S6 Reports    | 0     | 2      | 3      | 0     | manifest 67건 REFUTED (DEDUPE_TYPES 의도)      |
| S7 Automation | 0     | 4      | 2      | 0     | 이중 스케줄링 신규 / wrapper drift             |
| S8 Docs       | 0     | 2      | 2      | 2     | reference 6건 stale 신규 / README 버전 REFUTED |
| **합계**      | **4** | **24** | **24** | **4** | **56건 actionable**                            |

---

## P0 — 즉시 fix (자동화 가능)

### S2 Commands

| #    | 위치                                         | 문제                               | Fix                                                                     |
| ---- | -------------------------------------------- | ---------------------------------- | ----------------------------------------------------------------------- |
| P0-1 | `.claude/commands/빠른분석.md` frontmatter   | `agent:` 필드 누락 → 라우팅 불명   | `agent: stock-analyst-lead` 추가                                        |
| P0-2 | `.claude/commands/재분석점검.md` frontmatter | `agent:` 필드 누락                 | `agent: stock-analyst-lead` 추가 (session-bootstrap 의존성도 함께 점검) |
| P0-3 | `.claude/commands/손절계산.md`               | agent 라우팅 경로 불명확 (R2 신규) | `agent: stock-analyst-lead` 또는 인라인 bash 명시                       |

### S3 Scripts

| #    | 위치                              | 문제                                            | Fix                                                  |
| ---- | --------------------------------- | ----------------------------------------------- | ---------------------------------------------------- |
| P0-4 | `scripts/daily_pick_update.sh:20` | `set -e` 누락 + `exit 0` 하드코딩 → silent skip | `set -euo pipefail` 추가 + build 실패 시 deploy 중단 |

**예상 처리 시간**: 10분 (4건 모두 단일 라인 frontmatter / shebang 수정)

---

## P1 — 사용자 결정 필요

### S1 Agents (4건)

| #    | 위치                                     | 문제                               | Fix 방향                                                                  |
| ---- | ---------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------- |
| P1-1 | `.claude/agents/date-rules.md`           | not-agent (rule 문서가 agent 폴더) | `reference/date-rules.md` 이동 + kb-updater 참조 경로 갱신                |
| P1-2 | `.claude/agents/stop-loss-rules.md`      | not-agent (rule 문서가 agent 폴더) | `reference/stop-loss-rules.md` 이동 + scorecard-strategist Read 경로 갱신 |
| P1-3 | `.claude/agents/kb-updater.md`           | date-rules 명시 참조               | P1-1 이동 시 동기 갱신 (REFUTED 방지)                                     |
| P1-4 | `.claude/agents/scorecard-strategist.md` | stop-loss-rules 명시 Read          | P1-2 이동 시 동기 갱신                                                    |

### S2 Commands (4건)

| #    | 위치                                  | 문제                             | Fix                              |
| ---- | ------------------------------------- | -------------------------------- | -------------------------------- |
| P1-5 | `.claude/commands/비교분석.md:9`      | Phase 0~3 경계 불명확            | Phase 헤더 명시 추가             |
| P1-6 | `.claude/commands/성과리뷰.md:77`     | 위임 책임 불명확                 | Step별 agent 명시                |
| P1-7 | `.claude/commands/빠른분석.md` STEP 2 | bash 위임 불명확                 | tool 명시 또는 인라인 컴퓨팅     |
| P1-8 | `.claude/commands/재분석점검.md`      | session-bootstrap.md 의존성 위험 | bootstrap stale 시 fallback 로직 |

### S3 Scripts (3건)

| #     | 위치                                                      | 문제                                         | Fix                         |
| ----- | --------------------------------------------------------- | -------------------------------------------- | --------------------------- | ---------------------- | -------------------------- |
| P1-9  | `scripts/deploy_cloudflare.sh:68,71,75,85`                | `                                            |                             | true` 4건 → error 은닉 | exit code 처리 + retry 1회 |
| P1-10 | `scripts/launchd/daily-pick.log`                          | git pull 실패 이력 (silent state corruption) | wrapper 에 fail-fast + 알림 |
| P1-11 | `scripts/build_main_index.py` vs `build_analyst_index.py` | 중복 설계                                    | 통합 또는 역할 명시 주석    |

### S4 KB+DB (2건)

| #     | 위치                                                                                                     | 문제       | Fix                                |
| ----- | -------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------- |
| P1-12 | `knowledge-base/knowledge-db/robotics_2026.jsonl:14`                                                     | JSONL 깨짐 | line 14 재검증 / 삭제 / 재수집     |
| P1-13 | 만료 21건 (industry/\* + market/correlation_matrix + market/surprise_index + portfolio/model_portfolios) | TTL 초과   | `/KB업데이트` 일괄 호출 또는 prune |

### S5 Web Dashboard (3건)

| #     | 위치                                   | 문제             | Fix                                                              |
| ----- | -------------------------------------- | ---------------- | ---------------------------------------------------------------- |
| P1-14 | `web/src/components/TopHoldings.astro` | orphan (참조 0)  | import 추가 또는 삭제                                            |
| P1-15 | `web/src/components/TypeCounts.astro`  | orphan (R2 신규) | import 추가 또는 삭제                                            |
| P1-16 | A11y 14/16 위젯 `aria-*` 전무          | 접근성 위배      | DailyPick:17-106, RecommendCloud:40, HoldingsDonut, 외 11개 일괄 |

### S6 Reports (2건)

| #     | 위치                        | 문제                                   | Fix                                                         |
| ----- | --------------------------- | -------------------------------------- | ----------------------------------------------------------- |
| P1-17 | `analysis/` unversioned 9건 | timeline.json 부분 등록                | v 마커 추가 또는 timeline 강제 등록                         |
| P1-18 | `reports/research/` 5건     | CLAUDE.md 룰 (reports/ 직속 only) 위배 | reports/ 이동 또는 룰 갱신 (build_manifest v3.17 이미 허용) |

### S7 Automation (4건)

| #     | 위치                                                                | 문제                                    | Fix                          |
| ----- | ------------------------------------------------------------------- | --------------------------------------- | ---------------------------- |
| P1-19 | crontab `5 0 * * *` + launchd `Hour=0 Minute=5`                     | **이중 스케줄링** → 동시 빌드/push 충돌 | 한쪽 비활성화 (launchd 권장) |
| P1-20 | `scripts/launchd/daily-pick.log` git pull --rebase 실패 후 continue | silent corruption                       | fail-fast                    |
| P1-21 | `scripts/deploy_cloudflare.sh`                                      | 재시도 부재                             | retry 1회 + backoff          |
| P1-22 | `.env.local` 미존재                                                 | 일부 스크립트 fallback 모호             | 템플릿 `.env.example` 생성   |

### S8 Docs (2건)

| #     | 위치                                     | 문제                                                                                                     | Fix                            |
| ----- | ---------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------ |
| P1-23 | `reference/` 6건 stale 53~55일 (R1 누락) | data-collector / dart_api / etf_guide / output_schema / sources / guru_watchlist / rules_and_constraints | 우선 검증 후 일괄 갱신         |
| P1-24 | `docs/briefing_pipeline.md` 26일 stale   | 파이프라인 변경 후 미반영                                                                                | briefing-lead v3.x 기준 재작성 |

**예상 처리 시간**: 사용자 검토 30~45분 + 실제 fix 60~90분

---

## P2 — 일괄 prune / 다음 회차

### S1 Agents (3건)

| #    | 위치                                                       | 문제                                |
| ---- | ---------------------------------------------------------- | ----------------------------------- |
| P2-1 | `.claude/agents/stock-analyst-lead.md` 1553L + maxTurns=40 | 비대 / fail rate 추정 (수치 미검증) |
| P2-2 | `.claude/agents/briefing-lead.md` 1461L + maxTurns=25      | 비대                                |
| P2-3 | `.claude/agents/scorecard-strategist.md:617`               | Phase 헤더 부재                     |

### S2 Commands (5건)

| #      | 위치                                    | 문제                                        |
| ------ | --------------------------------------- | ------------------------------------------- |
| P2-4~8 | `.claude/commands/재분석실행.md` 외 5건 | v3.x 마커 lifecycle 정책 부재 / 헤더 일관성 |

### S3 Scripts (2건)

| #     | 위치                               | 문제                                      |
| ----- | ---------------------------------- | ----------------------------------------- |
| P2-9  | `scripts/_kst.py`                  | **진짜 orphan** (import 0건) — prune 가능 |
| P2-10 | `scripts/briefing_commit.sh:52-57` | 이모지 로그 → CLAUDE.md 위배              |

### S4 KB+DB (4건)

| #     | 위치                                           | 문제                                                       |
| ----- | ---------------------------------------------- | ---------------------------------------------------------- |
| P2-11 | KB orphan 67/88 (76%, R2 정정)                 | research/ 35건 제외 후 — 일부는 의도, 일부는 prune 후보    |
| P2-12 | 시간 표시 오류 13건                            | KST/UTC 표기 비일관                                        |
| P2-13 | `reference/korean_translation_rules.md` orphan | 자동화 미적용 (R2 신규)                                    |
| P2-14 | 한글 비중 88/88 < 80%                          | **설계 의도 (데이터 무결성 > 한글화)** — 룰 자체 갱신 권고 |

### S5 Web (3건)

| #     | 위치                                                   | 문제                                        |
| ----- | ------------------------------------------------------ | ------------------------------------------- |
| P2-15 | `web/src/components/DailyPick.astro:4` any 타입        | 타입 명시                                   |
| P2-16 | `web/src/components/MacroIndicators.astro:19` any 타입 | 타입 명시                                   |
| P2-17 | `web/src/components/RecentlyViewed.astro`              | 설계상 비활성 (SSG placeholder) — 주석 추가 |

### S6 Reports (3건)

| #     | 위치                                  | 문제                                               |
| ----- | ------------------------------------- | -------------------------------------------------- |
| P2-18 | `reports/system_architecture.html`    | placeholder                                        |
| P2-19 | `reports/analyst/briefing/index.html` | 누락                                               |
| P2-20 | `analysis/_history/`                  | 통합 timeline.json 부재, 156개 파일 분산 (R2 신규) |

### S7 Automation (2건)

| #     | 위치                                           | 문제                                                    |
| ----- | ---------------------------------------------- | ------------------------------------------------------- |
| P2-21 | `/Users/kimsl12/.claude/daily-pick-wrapper.sh` | git tracked 원본과 분리 (R2 신규) — drift 위험          |
| P2-22 | `.github/workflows/deploy-reports.yml`         | gh-pages 트리거 살아있음 — Actions 차단 환경에서 무의미 |

### S8 Docs (2건)

| #     | 위치                                                             | 문제                   |
| ----- | ---------------------------------------------------------------- | ---------------------- |
| P2-23 | `knowledge-base/industry/real_estate.md` 38일 stale (R3 P2 상향) | 갱신                   |
| P2-24 | `algo-trading/README.md:393`                                     | 사소한 typo / outdated |

**예상 처리 시간**: 일괄 prune 30분 + 다음 회차 위임

---

## P3 — 모니터링 (선택)

| #    | 위치                                                                               | 문제                   |
| ---- | ---------------------------------------------------------------------------------- | ---------------------- |
| P3-1 | `scripts/*.sh` shebang 비일관 (`#!/bin/bash` 1 + `#!/usr/bin/env bash` 2, R2 신규) | 통일                   |
| P3-2 | `AGENTS.md` / `MEMORY.md` 미생성 (Claude SDK 표준, R2 신규)                        | 선택                   |
| P3-3 | KB jsonl 만료 자동 알림 부재                                                       | 향후 health_check 통합 |
| P3-4 | docs/briefing_pipeline.md 외 부수 문서 lifecycle 부재                              | 정책 수립              |

---

## R1 false-positive 정정 (재발 방지 학습)

R1 cavecrew 발견 중 R2 Explore 검증으로 reject 된 항목 — 향후 cavecrew prompt 보정 reference.

| #     | 섹터 | R1 주장                                                 | R2 검증 결과                                                                       |
| ----- | ---- | ------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| FP-1  | S1   | research-curator orphan                                 | **REFUTED** — briefing-lead.md:1359-1369 Phase 0-RESEARCH 조건부 호출 확인         |
| FP-2  | S2   | 리포트.md agent 누락                                    | **REFUTED** — L4 frontmatter 에 `agent: report-generator` 명시                     |
| FP-3  | S2   | 이브닝/주간/크립토/풀브리핑 deploy 룰 미명시            | **REFUTED** — briefing-lead.md Step 14 SSOT 분리 (command 본문에 중복 명시 불필요) |
| FP-4  | S2   | KB업데이트 / KB점검 중복                                | **REFUTED** — 수집(kb-updater) vs 진단(wiki-linter) 역할 분리                      |
| FP-5  | S2   | 재분석실행 v3.x lifecycle 불명확                        | **REFUTED** — 의도된 버전 마커, 정책 존재                                          |
| FP-6  | S3   | reanalysis_data_save.py orphan                          | **REFUTED** — session-bootstrap.md 직접 호출                                       |
| FP-7  | S3   | reanalysis_generate_20260528.py orphan                  | **REFUTED** — session-bootstrap.md 직접 호출                                       |
| FP-8  | S3   | reanalysis_generate_20260529.py orphan                  | **REFUTED** — session-bootstrap.md 직접 호출                                       |
| FP-9  | S4   | KB orphan 83/88 (94%)                                   | **REFINED** — 67/88 (76%), research/ 35건 의도된 백서 라이브러리                   |
| FP-10 | S4   | 한글 비중 < 80% 30+건                                   | **REFINED** — 88/88 전부 미달, 단 **설계 의도 (데이터 무결성)** 으로 버그 아님     |
| FP-11 | S5   | DailyPick.astro:446 /api/price/ fetch (static SSG 위배) | **REFUTED** — vercel.json functions 정의 있음, 의도된 하이브리드                   |
| FP-12 | S5   | any 타입 4건                                            | **REFINED** — 실제 2건 (DailyPick:4 + MacroIndicators:19)                          |
| FP-13 | S6   | manifest 미등록 67건                                    | **REFUTED** — build_manifest.mjs DEDUPE_TYPES 의도된 로직                          |
| FP-14 | S7   | deploy-reports.yml orphan                               | **REFUTED** — gh-pages 트리거 살아있음 (P2 강등)                                   |
| FP-15 | S8   | README.md v3.17 vs build_readme.mjs v3.21 불일치        | **REFUTED** — 의도된 버전 헤더, fence 만 자동 갱신                                 |

**False-positive 비율**: 15/약 80 (19%) — cavecrew prompt 가 "참조 검증" 단계를 누락하는 경향. R2 Explore 가 SSOT/upstream 호출체인 추적으로 정정.

**R2 신규 발견 21건**: kb-updater 참조 / 손절계산 라우팅 / 빠른분석 STEP2 / 재분석점검 bootstrap 의존성 / daily-pick.log git pull 실패 / Bash shebang / korean_translation_rules.md orphan / TypeCounts.astro / A11y 14/16 / analysis/\_history / 이중 스케줄링 / wrapper drift / reference 6건 stale / AGENTS.md / MEMORY.md.

---

## 권고 실행 순서

| 단계 | 항목                                                    | 예상 시간   | 자동화      |
| ---- | ------------------------------------------------------- | ----------- | ----------- |
| 1    | P0 자동 fix (4건: frontmatter 3 + daily_pick_update.sh) | **10분**    | ✅          |
| 2    | 사용자 P1 검토 (24건)                                   | **30~45분** | ❌ (게이트) |
| 3    | P1 실제 fix (사용자 승인 후)                            | **60~90분** | 부분 ✅     |
| 4    | P2 일괄 prune (24건)                                    | **30분**    | 부분 ✅     |
| 5    | P3 모니터링 (4건)                                       | 다음 회차   | —           |

**핵심 권고**:

1. **P0 4건 즉시 실행** (frontmatter 누락 3건 + daily_pick_update.sh set -e) — fix 명령 단순
2. **P1-19 이중 스케줄링 우선 확인** — crontab 또는 launchd 한쪽 비활성화 (daily_pick 중복 빌드 / git push 충돌 위험)
3. **P1-1,2 rule 문서 이동** — kb-updater + scorecard-strategist 참조 동시 갱신 (P1-3,4 동기)
4. **P1-23 reference 6건 stale** — 53~55일 경과, 빠른 검증 후 갱신
5. R1 false-positive 학습 → 다음 cavecrew prompt 에 "SSOT 호출체인 추적 후 orphan 단정" 룰 추가

---

## 검증 메타데이터

- R1 cavecrew dispatch: 2026-06-01 (8 sectors × cavecrew-investigator)
- R2 Explore dispatch: 2026-06-01 (8 sectors × Explore)
- R3 종합: 2026-06-01 (current)
- 총 agent 호출: 17 (cavecrew × 8 + Explore × 8 + general × 1)
- R1 발견 수: 약 250건 (warning 다수 포함)
- R2 검증 후: 132건 actionable (false-positive 89건 제거 + 신규 21건)
- P0~P3 분류: 56건 actionable (P0=4 / P1=24 / P2=24 / P3=4)
- False-positive 율: 19%
- 검증 방식: R2 가 R1 의 SSOT/upstream 참조를 grep + Read 로 교차검증
