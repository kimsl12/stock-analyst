# 종목분석 에이전트 — 작업 자동화 지침

## 사이트 배포 자동화 (필수)

`reports/*.html` 또는 `reports/briefing/*.html` 이 포함된 main push 직후, **반드시 다음을 자동 실행**:

```bash
bash scripts/deploy_cloudflare.sh
```

### 적용 시점
- 종목 분석 push (개별 / 묶음 / 페이즈 일괄)
- 브리핑 push (모닝 / 이브닝 / 주간 / 글로벌인텔리전스 / 풀 등)
- 단발성 HTML 추가 / 재생성 push

### 적용 제외
- `knowledge-base/`, `knowledge-db/`, `analysis/` 만 변경된 push (HTML 없음)
- 스크립트 / 워크플로 / 메타 파일만 변경된 push
- KB 갱신 단독 push

### 왜
GitHub Actions 계정 차단 (Ticket 4287825, 2026-04-15부터). GitHub Pages 자동 배포 (`deploy-reports.yml`) + 1st-party Pages builder 모두 user-level Actions disable에 동시 차단됨. main push는 정상이지만 사이트 publish는 Cloudflare Pages로 우회 필요.

### 결과
- 사이트 URL: https://stock-analyst.pages.dev/
- 실행 시간: 3~5초 (205개 파일 기준)
- 실패 시: deploy 단독 재실행 가능. main push에는 영향 없음.
- GitHub Pages (`kimsl12.github.io/stock-analyst`)는 사용 중단 상태 — 차단 풀려도 당분간 Cloudflare 유지.

### 관련 메모
- `~/.claude/projects/.../memory/project_github_actions_disabled.md` — 사건 전체 이력 + 마이그레이션 가이드
