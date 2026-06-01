# 다음 에이전트 핸드오프 — 2026-06-01 audit 후속 작업

> **이전 세션 종료**: 2026-06-01
> **2 commit 처리**: `eb0fbf36` (audit A+C+B 자동 17건 + E + F) + `a5ecb378` (KB 21건 + A11y 12 + reference + docs + timeline)
> **총 95 파일 변경 / push + Vercel + Cloudflare deploy 완료**
> **audit 원본**: [audit/2026-06-01_full_project_audit.md](./2026-06-01_full_project_audit.md)

---

## 세션 종료 시 상태 (인계 시점)

### 처리 완료 29건 (P0 4 + P1 23 + P2 2)

| ID           | 항목                                                                                      | commit   |
| ------------ | ----------------------------------------------------------------------------------------- | -------- |
| P0-1         | `빠른분석.md` frontmatter `agent: stock-analyst-lead`                                     | eb0fbf36 |
| P0-2         | `재분석점검.md` frontmatter `agent: stock-analyst-lead`                                   | eb0fbf36 |
| P0-3         | `손절계산.md` frontmatter `agent: stock-analyst-lead`                                     | eb0fbf36 |
| P0-4         | `daily_pick_update.sh` `set -euo pipefail` + `exit 1` (silent corruption 차단)            | eb0fbf36 |
| P1-1,2       | `date-rules.md` + `stop-loss-rules.md` → `reference/` 이동                                | eb0fbf36 |
| P1-3,4       | 14 파일 참조 일괄 갱신 (agents 6 + commands 2 + README + algo-trading 2 + scorecard Read) | eb0fbf36 |
| P1-5         | `비교분석.md` Phase 0-A~Phase 4 명시 + sequential 강제                                    | eb0fbf36 |
| P1-6         | `성과리뷰.md` 위임 책임 명시 (briefing-lead 직접, 메인 fallback)                          | eb0fbf36 |
| P1-7         | `빠른분석.md` STEP 2 책임 명시 (stock-analyst-lead Bash 직접)                             | eb0fbf36 |
| P1-8         | `재분석점검.md` fallback 추가 (fence 깨짐 시 build_bootstrap + timeline.json)             | eb0fbf36 |
| P1-9         | `deploy_cloudflare.sh` wrangler 1회 재시도 + 5초 backoff                                  | eb0fbf36 |
| P1-10, P1-20 | `daily_pick_update.sh` git pull WARN → ERROR + exit 1                                     | eb0fbf36 |
| P1-12        | `robotics_2026.jsonl:14` JSONL 깨짐 fix + 전수 파싱 검증                                  | eb0fbf36 |
| P1-13        | **KB 만료 21건 일괄 갱신** (industry 18 + market 2 + portfolio 1)                         | a5ecb378 |
| P1-14, P1-15 | orphan widget 2건 삭제 (TopHoldings, TypeCounts)                                          | eb0fbf36 |
| P1-16        | A11y 12 위젯 aria-label + SVG title + button label (17 라인)                              | a5ecb378 |
| P1-17        | unversioned analysis 9건 timeline 정합성 (2 신규 생성)                                    | a5ecb378 |
| P1-18        | CLAUDE.md `reports/` 폴더 구조 룰 신설 (4 위치 + research/ 추가)                          | eb0fbf36 |
| P1-19        | **이중 스케줄링 해소** — crontab 제거 (옵션 A), launchd 단독                              | eb0fbf36 |
| P1-22        | `.env.example` 생성 + `.gitignore` 강화                                                   | eb0fbf36 |
| P1-23        | reference 6건 부분 갱신 (2 frontmatter + 4 TODO)                                          | a5ecb378 |
| P1-24        | `docs/briefing_pipeline.md` 재작성 (309 → 596 라인, v3.0 → v3.22)                         | a5ecb378 |
| P2-9         | `scripts/_kst.py` 삭제 (orphan 확정)                                                      | eb0fbf36 |
| P2-10        | `scripts/briefing_commit.sh` 이모지 8개 → 텍스트 태그                                     | eb0fbf36 |

### 부수 처리

- `crontab` 백업: `/tmp/crontab_backup_20260601_1808.txt`
- `knowledge-base/_index.md`: P0 21건 → 0건 정리, version v3.2 → v3.22
- 21 jsonl append (각 KB 갱신과 함께)

---

## 이월 P2 22건 (다음 회차 처리 권고)

### S1 Agents (3건) — 비대 / Phase 헤더

| ID   | 위치                                                        | 문제                  | 권고                                                        |
| ---- | ----------------------------------------------------------- | --------------------- | ----------------------------------------------------------- |
| P2-1 | `.claude/agents/stock-analyst-lead.md` (1553L, maxTurns=40) | 비대 / fail rate 추정 | 섹션 분할 + maxTurns 검토 (다음 maxTurns 도달 사고 후 진행) |
| P2-2 | `.claude/agents/briefing-lead.md` (1461L, maxTurns=25)      | 비대                  | 동일                                                        |
| P2-3 | `.claude/agents/scorecard-strategist.md:617`                | Phase 헤더 부재       | `## Phase 1-4` 헤더 추가                                    |

### S2 Commands (5건) — v3.x 마커 / 헤더 일관성

| ID     | 위치                                    | 문제                                              |
| ------ | --------------------------------------- | ------------------------------------------------- |
| P2-4~8 | `.claude/commands/재분석실행.md` 외 5건 | v3.x 마커 lifecycle 정책 부재 — 정책 수립 후 일괄 |

### S3 Scripts (이미 처리 완료 — 잔여 없음)

### S4 KB+DB (4건)

| ID    | 위치                                                               | 문제                                   | 권고                                                   |
| ----- | ------------------------------------------------------------------ | -------------------------------------- | ------------------------------------------------------ |
| P2-11 | KB orphan 67/88 (76%) — research/ 35건 의도된 백서 라이브러리 제외 | 일부는 의도, 일부는 prune 후보         | orphan 분류 + prune 결정 사용자 검토 필요              |
| P2-12 | KB 본문 시간 표시 오류 13건 (`이번 주`, `올해` 등 상대 시간 잔재)  | KST/UTC 비일관                         | kb-updater 호출 시 절대 날짜로 교체                    |
| P2-13 | `reference/korean_translation_rules.md` orphan                     | 자동화 미적용                          | 검증 스크립트 도입 또는 prune                          |
| P2-14 | 한글 비중 88/88 < 80%                                              | **설계 의도 (데이터 무결성 > 한글화)** | 룰 자체 갱신 권고 (현실 반영) — 한글 비중 룰 자체 검토 |

### S5 Web (3건)

| ID    | 위치                                                  | 문제                                 | 권고                                        |
| ----- | ----------------------------------------------------- | ------------------------------------ | ------------------------------------------- |
| P2-15 | `web/src/components/widgets/DailyPick.astro:4`        | `pick.pick as any \| null` 타입 명시 | `daily_pick.json` schema 작성 → import 타입 |
| P2-16 | `web/src/components/widgets/MacroIndicators.astro:19` | `(kb as any).fred`                   | `kb.json.fred` schema 작성                  |
| P2-17 | `web/src/components/widgets/RecentlyViewed.astro`     | 설계상 비활성 (SSG placeholder)      | 이미 주석 충분 — 변경 불요                  |

### S6 Reports (3건)

| ID    | 위치                                                             | 문제           | 권고                                   |
| ----- | ---------------------------------------------------------------- | -------------- | -------------------------------------- |
| P2-18 | `reports/system_architecture.html`                               | placeholder    | 검토 후 삭제 또는 본문                 |
| P2-19 | `reports/analyst/briefing/index.html` 누락                       | 자동화 vs 생성 | build_main_index.py 에 추가            |
| P2-20 | `analysis/_history/` 통합 timeline.json 부재, 156 개별 파일 분산 | 대형 리팩터    | cleanup_reanalysis.mjs 룰 갱신 시 함께 |

### S7 Automation (2건)

| ID    | 위치                                           | 문제                                                    | 권고                                      |
| ----- | ---------------------------------------------- | ------------------------------------------------------- | ----------------------------------------- |
| P2-21 | `/Users/kimsl12/.claude/daily-pick-wrapper.sh` | git tracked 원본과 분리 — drift 위험                    | wrapper 제거 또는 git tracked 으로 단일화 |
| P2-22 | `.github/workflows/deploy-reports.yml`         | GitHub Actions 차단 환경에서 gh-pages 트리거만 살아있음 | 사용자 결정 (보존 vs 삭제)                |

### S8 Docs (2건)

| ID    | 위치                                     | 문제                                                             | 권고                                 |
| ----- | ---------------------------------------- | ---------------------------------------------------------------- | ------------------------------------ |
| P2-23 | `knowledge-base/industry/real_estate.md` | 38일 stale (P3 → P2 상향) — 단, 2026-06-01 KB 21건 갱신에 포함됨 | **이미 처리 완료 (kb-updater 갱신)** |
| P2-24 | `algo-trading/README.md:393`             | "## 향후 추가 예정" 일정 미명시                                  | 일정 추가 또는 섹션 삭제             |

---

## 이월 P3 4건 (모니터링)

| ID   | 위치                                                                      | 문제                       |
| ---- | ------------------------------------------------------------------------- | -------------------------- |
| P3-1 | `scripts/*.sh` shebang 비일관 (`#!/bin/bash` 1 + `#!/usr/bin/env bash` 2) | 통일 `#!/usr/bin/env bash` |
| P3-2 | `AGENTS.md` / `MEMORY.md` 미생성 (Claude SDK 표준)                        | 선택 — 사용자 의도 시 생성 |
| P3-3 | KB jsonl 만료 자동 알림 부재                                              | health_check 통합          |
| P3-4 | docs/briefing_pipeline.md 외 부수 문서 lifecycle 부재                     | 문서 갱신 정책 수립        |

---

## 추가 발견 (단계 2~3 작업 중)

### reference/ 큰 변경 권고 (P1-23 후속)

agent dispatch 가 식별한 사용자 결정 영역:

1. `reference/data-collector/*.md` 4개 frontmatter 추가 표준화 (`category: reference` / `type: static`)
2. `reference/data-collector/sources.md` L31~35, L64~67 `[v2.4 신규]` 마커 정리
3. `reference/guru_watchlist.md` 13F 예시 변경 불요 (현재 시점 유효)

### A11y 추가 권고 (P1-16 후속)

- FearGreedGauge, MarketHeatmap 은 이미 aria 적용 — 변경 안 함
- StatCard 는 동적 a/div root — 보간 라벨 `통계 카드: {label} {value} {sub}` 적용
- WCAG 2.1 AA 부분 준수 — 추가 점검 권고 (focus management, color contrast 등)

---

## 처리 우선순위 권고 (다음 회차)

```
1. P2-14 한글 비중 룰 자체 갱신 (현실 반영) — 룰 수정
2. P2-15, P2-16 타입 schema 작성 (daily_pick, kb.json) — 타입 안전성
3. P2-11 KB orphan 67건 분류 — prune vs 의도 분류
4. P2-12 KB 시간 표시 오류 13건 — 절대 날짜 교체
5. P2-20 timeline.json 통합 (대형 리팩터) — cleanup_reanalysis 룰 갱신
6. P2-21 wrapper drift (`/Users/kimsl12/.claude/daily-pick-wrapper.sh`)
7. P2-22 deploy-reports.yml 결정
8. P2-1,2,3 agent 비대 (다음 maxTurns 사고 후)
9. P3 4건 (모니터링 — 자연 진행)
```

---

## 검증 메타데이터 (이전 세션)

- **agent 호출 수**: 17 (R1 cavecrew × 8 + R2 Explore × 8 + R3 general × 1)
- **kb-updater dispatch**: 21회 병렬 (단계 3)
- **general-purpose dispatch**: 3회 (단계 2 — A11y / reference / briefing_pipeline)
- **R1 false-positive**: 19% (15/80) — research-curator orphan / manifest 67건 등
- **commits**: 2 (eb0fbf36 + a5ecb378), 총 95 파일
- **push**: origin main 성공
- **deploy**: Vercel + Cloudflare 양 채널 성공 (2회)

---

## 환경/제약 사항

### 활성 자동화

- **launchd**: `com.stockanalyst.daily-pick` 단독 (KST 00:05) — crontab 제거 완료
- **wrapper**: `/Users/kimsl12/.claude/daily-pick-wrapper.sh` ← `scripts/daily_pick_update.sh` (drift 위험 P2-21)

### Deploy 채널

- **Vercel 본**: `vercel --prod --yes` (수동, GitHub Actions 차단)
- **Cloudflare 미러**: `bash scripts/deploy_cloudflare.sh` (1회 재시도 + 5초 backoff 신설)

### 비밀 파일

- `.env.local` 미존재 — Cloudflare 는 wrangler OAuth 폴백
- `.env.example` 신규 (P1-22) — 사용자가 `cp .env.example .env.local` 후 채우기 권장
- `.gitignore` 루트 .env / .env.local / .env.\*.local 패턴 추가

### KB 만료 다음 시점

- 21건 모두 `valid_until: 2026-06-08` — **다음 회차 KB 점검 = 2026-06-08**
- `/KB점검` 수행 시 만료 검증 자동 수행 (wiki-linter full)

---

## 빠른 진입 방법

```bash
# 1. 이전 세션 상태 파악
cat audit/2026-06-01_full_project_audit.md   # 원본 audit 56건
cat audit/2026-06-01_handoff_next_session.md  # 본 파일 (인계 사항)

# 2. 처리 권고 P2-14 부터 시작
grep -rn "한글 비중\|korean_ratio\|80%" reference/ knowledge-base/ | head -20

# 3. P2-11 KB orphan 분류 (R2 가 본 67건)
grep -rn "knowledge-base" .claude/ web/scripts/ | grep -v audit/ | head -30
# 정적 참조 외 동적 read 패턴 확인 (briefing-lead 의 조건부 호출 등)

# 4. P2-15, P2-16 schema 작성
cat web/src/data/daily_pick.json | jq 'keys'
cat web/src/data/kb.json | jq '.fred | keys' 2>/dev/null
```

---

## 보존 룰 (재발 방지 학습)

이전 세션의 사용자 명시 룰:

1. **destructive 작업 + commit/push/deploy = 사용자 명시 승인 필수**
   - 이번 세션 초반: 자동 진행 → 사용자 비판 → 단계별 결정 게이트 회복
   - 다음 세션: 매 단계 사용자 결정 받음

2. **R1 (cavecrew) 결과 = R2 (Explore) 검증 후 사용**
   - cavecrew 가 SSOT 호출체인 추적 누락 → 19% false-positive
   - 단순 grep + 호출 그래프 빌드 후 orphan 확정

3. **묶음 단위 결정 받음 — 3건씩 묶음**
   - 묶음별 처리 방식 사용자 확인 후 진행

4. **caveman 모드 유지** — 응답 압축, 표 형식, 1줄/항목
