# 종목분석 에이전트 — 작업 자동화 지침

## 사이트 배포 자동화 (필수)

`reports/**/*.html` (종목 / 브리핑 / 애널리스트) 변경이 포함된 main push 직후, **반드시 두 채널 모두 자동 실행**:

```bash
# 1. 본서버 (Vercel) — Astro+Supabase 풀 대시보드, 사용자가 실제 보는 곳
vercel --prod --yes

# 2. 미러 (Cloudflare Pages) — 우회 정적 호스팅, 보조 채널
bash scripts/deploy_cloudflare.sh
```

**Vercel 먼저, Cloudflare 나중**. Vercel 빌드 약 45초, Cloudflare 약 3~5초.

### 본서버 / 미러 구조

| 채널 | URL | 갱신 명령 | 자동 빌드 |
|------|-----|----------|----------|
| **Vercel (본)** | https://stock-analyst-jungwon1.vercel.app/ | `vercel --prod --yes` (root) | ❌ 깨짐 |
| Cloudflare (미러) | https://stock-analyst.pages.dev/ | `bash scripts/deploy_cloudflare.sh` | ❌ |

### 적용 시점
- 종목 분석 push (개별 / 묶음 / 페이즈 일괄)
- 브리핑 push (모닝 / 이브닝 / 주간 / 글로벌인텔리전스 / 풀 등)
- 애널리스트 항목 push (`reports/analyst/items/*/`)
- 단발성 HTML 추가 / 재생성 push

### 적용 제외
- `knowledge-base/`, `knowledge-db/`, `analysis/` 만 변경된 push (HTML 없음)
- 스크립트 / 워크플로 / 메타 파일만 변경된 push
- KB 갱신 단독 push

### 왜 둘 다 필요한가
GitHub Actions 계정 차단 (Ticket 4287825, 2026-04-15부터). 부수효과:
- GitHub Pages 자동 배포 차단
- **Vercel 자동 빌드 webhook 도 트리거 안 됨** (5/6 push 후 21시간 stale 확인)
- → main push 만으로 사이트 자동 갱신되지 않음. 수동 CLI 호출 필수.

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
