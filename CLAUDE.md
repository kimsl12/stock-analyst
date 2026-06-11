# 종목분석 에이전트 — 작업 자동화 지침

## 사이트 배포 자동화 (필수) [2026-06-11 webhook 복귀 반영]

`reports/**/*.html` (종목 / 브리핑 / 애널리스트) 변경이 포함된 main push 직후:

```bash
# 1. 본서버 (Vercel) — push 가 자동 빌드 트리거 (webhook 재연결 2026-06-11 검증).
#    push 후 1~2분 내 확인만: vercel ls 최신 행이 방금 push 의 자동 빌드 ● Ready 인지.
#    자동 빌드 미발생/실패 시에만 수동 fallback: vercel --prod --yes

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
