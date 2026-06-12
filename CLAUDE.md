# 종목분석 에이전트 — 작업 자동화 지침

## 사이트 배포 자동화 (필수) [2026-06-11 webhook 복귀 반영]

## 🔴 [임시·최우선] GitHub 플래그 기간 배포 룰 (2026-06-12 ~ 플래그 해제까지)

**상황**: GitHub 계정 플래그로 서드파티 OAuth(Vercel) 연결이 차단됨. 부수효과로 **Vercel deployment 가 전부 `Blocked` → production 승격(promote/alias) 불가 → 본서버 갱신 불가**. (2026-06-12 Vercel Deployments 화면에서 최근 Production 전부 "Blocked" 확인. `promote`·`alias set` 모두 `not ready (422)` 거부.) GitHub Support 티켓 #4287825 후속 답변 발송, 처리 대기 중.

**플래그 해제 전까지 강제 동작 — 이 4가지를 무조건 따른다**:

1. **Vercel 시도 금지.** `vercel --prod` / `vercel ls` 확인 전부 무의미하다(Blocked 라 100% 실패 + 좀비 백그라운드만 누적). **본서버 갱신을 시도하지 말 것.** 시간 낭비다.
2. **Cloudflare 미러가 유일 배포 채널.** `reports/**/*.html` 포함 push 직후 반드시 1줄만 실행:
   ```bash
   bash scripts/deploy_cloudflare.sh
   ```
3. **사용자 향 완료 링크 = Cloudflare** (`https://stock-analyst.pages.dev/`). 평소 "Vercel 본서버 우선" 룰의 한시적 예외(Vercel 이 stale 이므로). [[feedback_completion_links_vercel]] 예외 적용 중.
4. **완료 보고 형식 고정**: `Cloudflare 미러 ✅ / Vercel 본서버 ❌(GitHub 플래그로 promote 차단, 해제 후 일괄 복구)`.

**원복 트리거(이 블록 삭제 조건)**: 플래그 해제 신호 = ① 사용자가 "플래그 풀렸다" 고지, 또는 ② `vercel --prod --yes`(sandbox 우회 호출법은 아래) 후 deployment 가 `● Ready` 로 승격됨, 또는 ③ Vercel 대시보드 Deployments 에서 Production 이 Blocked→Ready 로 뜸. 셋 중 하나 확인되면 → **본 임시 블록 삭제 + 평상시 룰 복귀**, 그리고 `vercel --prod --yes` 한 번으로 그동안 누적된 reports 를 일괄 반영.

> 수동 `vercel --prod` 정확한 호출법(플래그 해제 후 사용): `dangerouslyDisableSandbox: true` + `timeout 160 vercel --prod --yes < /dev/null 2>&1 | tail -15`. 그냥 호출하면 sandbox 가 `~/.vercel` 토큰 차단(Not authorized) 또는 백그라운드 행. 상세: 메모리 [[project_github_actions_disabled]].

---

`reports/**/*.html` (종목 / 브리핑 / 애널리스트) 변경이 포함된 main push 직후:

```bash
# 1. 본서버 (Vercel) — push 가 자동 빌드 트리거 (webhook 재연결 2026-06-11 검증).
#    ⚠️ 단 간헐 누락 있음 (2026-06-12 실측: 09:33 push 빌드됨, 10:04 push 누락 —
#    GitHub 계정 플래그의 서드파티 전송 제한 추정. 백업 훅 추가 불가, 사용자가 GitHub 와 해결 예정).
#    push 후 1~2분 내 vercel ls 확인 필수 → 자동 빌드 미발생 시 즉시 수동: vercel --prod --yes

# 2. 미러 (Cloudflare Pages) — webhook 없음. 항상 수동 실행:
bash scripts/deploy_cloudflare.sh
```

### 본서버 / 미러 구조

| 채널              | URL                                        | 갱신 명령                                   | 자동 빌드            |
| ----------------- | ------------------------------------------ | ------------------------------------------- | -------------------- |
| **Vercel (본)**   | https://stock-analyst-jungwon1.vercel.app/ | push 자동 (fallback: `vercel --prod --yes`) | ✅ 2026-06-11 재연결 |
| Cloudflare (미러) | https://stock-analyst.pages.dev/           | `bash scripts/deploy_cloudflare.sh`         | ❌                   |

### 적용 시점

- 종목 분석 push (개별 / 묶음 / 페이즈 일괄)
- 브리핑 push (모닝 / 이브닝 / 주간 / 글로벌인텔리전스 / 풀 등)
- 애널리스트 항목 push (`reports/analyst/items/*/`)
- 단발성 HTML 추가 / 재생성 push

### 적용 제외

- `knowledge-base/`, `knowledge-db/`, `analysis/` 만 변경된 push (HTML 없음)
- 스크립트 / 워크플로 / 메타 파일만 변경된 push
- KB 갱신 단독 push

### 이력 (왜 이런 구조인가)

GitHub Actions 계정 차단 (Ticket 4287825, 2026-04-15) 부수효과로 Vercel webhook 까지 끊겨
51일간 양 채널 수동 배포 운용. 2026-06-05 차단 해제 → 2026-06-11 사용자가 Vercel Git 재연결,
빈 커밋 push 로 자동 빌드 검증 완료 (90초 내 ● Ready). 이후 Vercel 은 확인만, Cloudflare 는 수동 유지.
`scripts/daily_pick_update.sh` 의 수동 vercel 호출은 심야 무인 런 안전망으로 의도적 존치 (중복 빌드 무해).

Cloudflare Pages는 5/7에 우회 채널로 추가. 메인 사용자 트래픽은 Vercel, Cloudflare는 보조 미러.

### 실행 결과

- Vercel: cloud build (45초), `web/dist/` 출력, deployment URL 반환
- Cloudflare: 로컬 패키지 + wrangler upload (3~5초), 207~217 파일

### 실패 시 처리

- 한쪽 deploy 실패해도 다른쪽은 영향 없음. 단독 재실행 가능.
- Vercel: `vercel --prod --yes` 다시 호출
- Cloudflare: `bash scripts/deploy_cloudflare.sh` 다시 호출

### 관련 메모

- `~/.claude/projects/.../memory/project_github_actions_disabled.md` — 사건 전체 이력 + 본서버/미러 운영 가이드

## reports/ 폴더 구조 (허용 위치) [v3.22 — 2026-06-01 신설, P1-18 fix]

build_manifest.mjs 가 스캔하는 4 위치만 허용. 그 외 서브디렉토리 push 시 본서버에 404.

| 위치                           | 용도                                 | 갱신 주기  | 도입       |
| ------------------------------ | ------------------------------------ | ---------- | ---------- |
| `reports/*.html`               | 종목 / ETF 분석 (직속)               | 개별 호출  | v3.0       |
| `reports/briefing/*.html`      | 모닝/이브닝/주간/풀/글로벌 등 브리핑 | 매일~매주  | v3.0       |
| `reports/analyst/items/{id}/*` | 애널리스트 리포트 (meta+PDF+HTML)    | PDF/스크랩 | v3.5       |
| `reports/research/*.html`      | L3 분기 Deep Dive (리서치 큐레이션)  | 분기       | v3.17 신규 |

위 외 임의 서브디렉토리 (예: `reports/stock/`, `reports/etf/`, `reports/2026/`) 사용 시 manifest 미등록 → Vercel 본서버 안 보임.

신규 카테고리 추가 시 `web/scripts/build_manifest.mjs` 의 `DEDUPE_TYPES` + `STOCK_DIR` / `BRIEF_DIR` / `RESEARCH_DIR` / `ANALYST_DIR` 상수 동시 갱신 필수.
