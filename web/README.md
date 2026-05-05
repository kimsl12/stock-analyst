# 종목분석 에이전트 — 웹 플랫폼

Astro 4 (정적 SSG) + Supabase (Auth/DB) + Vercel (CDN) 스택.

> **단일 진실의 원천:** [PLAN.md](./PLAN.md). 본 README는 운영 매뉴얼이며, 설계 결정은 PLAN을 따른다.

## 구조

```
web/
├── PLAN.md                  # 14일 작업 명세 (단일 진실의 원천)
├── astro.config.mjs         # output: 'static'
├── vercel.json              # Python Serverless 함수 설정 (api/price/[ticker].py)
├── requirements.txt         # Python deps (yfinance) — Vercel 자동 인식
├── api/
│   └── price/[ticker].py    # 가격 fetch Edge Function (Vercel Python)
├── db/                      # Supabase 스키마/RLS/검증
├── public/                  # 정적 자원 + 매니페스트가 복사한 reports/*.html
├── scripts/
│   ├── build_manifest.mjs   # reports/ → src/data/manifest.json + public/reports/
│   ├── build_kb.mjs         # KB → src/data/kb.json (market+health+events+recs+timemachine+performance)
│   └── build_search_index.mjs  # reports/ HTML → public/search-data.json
└── src/
    ├── data/                # 빌드 산출물 (manifest/kb/search-data) — gitignore
    ├── components/          # ReportCard, FilterBar, SearchBox, ThemeToggle, widgets/(StatCard, MarketSnapshot, RecommendCloud, PerformanceDonut 등)
    ├── layouts/             # Base.astro (인증/테마 가드, 네비), Authenticated.astro
    ├── lib/                 # supabase.ts, auth.ts, recently-viewed.ts
    └── pages/               # index(대시보드), all, briefing/[type], stocks/[ticker], portfolio, timemachine, compare, login, auth/callback
```

## 환경변수

`web/.env.example`을 `web/.env.local`로 복사 후 값 채움 (Git 제외).

| 변수 | 노출 | 용도 |
|---|---|---|
| `PUBLIC_SUPABASE_URL` | 클라 | Supabase 프로젝트 URL |
| `PUBLIC_SUPABASE_ANON_KEY` | 클라 | RLS 적용 anon 키 |
| `SUPABASE_SERVICE_KEY` | 서버 only | RLS 우회 (sync 스크립트) |
| `PUBLIC_ALLOWED_EMAIL` | 클라 | 화이트리스트 이메일 (Magic Link) |

Vercel 대시보드 → Project Settings → Environment Variables 에 동일하게 등록.

## 개발

```bash
cd web
npm install                  # 첫 1회
npm run dev                  # http://localhost:4321
```

`predev`/`prebuild`에서 매니페스트/KB/검색 인덱스를 자동 생성한다.

## 빌드

```bash
npm run build                # dist/ 생성 (정적 SSG)
npm run preview              # 빌드 결과 미리보기
```

## 배포 (Vercel)

```bash
vercel --prod                # main 브랜치 → 즉시 배포
```

GitHub repo flag 상태이므로 Vercel CLI 우회 등록. 자동 alias: `stock-analyst-jungwon1.vercel.app`.

## 인증 (Magic Link)

1. 미인증 → `/` 접근 시 `/login?next=...` 자동 리다이렉트
2. 화이트리스트 이메일(`PUBLIC_ALLOWED_EMAIL`) 입력 → Supabase Magic Link 발송
3. 이메일 링크 클릭 → `/auth/callback` → 화이트리스트 재검증 → next 페이지 이동
4. 비허용 이메일은 콜백에서 즉시 sign-out

세션 저장: LocalStorage 키 `sb-stock-analyst-auth`. 30일 유지는 Supabase 대시보드 JWT expiry = 2592000 설정 필요.

## 테마

- 다크/라이트 토글: 우측 상단 ☀/☾ 버튼
- 기본값: 시스템 `prefers-color-scheme`
- 저장: LocalStorage 키 `theme`
- FOUC 방지: `<head>` inline 스크립트로 페인트 전 적용

## Supabase 동기화

```bash
# 종목분석 에이전트 루트에서
.venv/bin/python scripts/sync_portfolio_to_supabase.py
```

`knowledge-base/portfolio/user_portfolio.md` → `portfolios` + `holdings` 테이블 upsert.
브리핑 파이프라인 Phase 4 후 자동 호출 (graceful fail).

## 검색

FlexSearch (esm.sh CDN 동적 import). `public/search-data.json` (~700KB)을 lazy load.
검색 박스에 입력 시 본문 매칭 + 200자 스니펫.

## 주요 라우트

| 경로 | 역할 | 인증 |
|---|---|---|
| `/` | 대시보드 (10개 위젯) | 필요 |
| `/all` | 전체 리포트 인덱스 + 검색/필터 | 필요 |
| `/briefing/[type]` | 종류별 (morning/evening/weekly/crypto) | 필요 |
| `/stocks` | 종목 카드 그리드 (날짜 desc) | 필요 |
| `/stocks/[ticker]` | 종목 상세 + iframe + 과거 분석 | 필요 |
| `/portfolio` | 포트폴리오 (Supabase) | 필요 |
| `/timemachine` | 시간 머신 — 1주/1개월/3개월 추천 + 수익률 | 필요 |
| `/compare?a=&b=` | 두 종목 비교 (지표 + iframe 분할) | 필요 |
| `/login` | Magic Link 발송 | 미요 |
| `/auth/callback` | 콜백 + 화이트리스트 | 미요 |
| `/api/price/[ticker]` | 실시간 가격 + ATR (Vercel Python) — `?at=YYYY-MM-DD`로 과거 시점 비교 | 미요 |

## /api/price 사양

- 메서드: `GET`
- 파라미터: path 변수 `ticker` (또는 `?ticker=`), 옵션 `?at=YYYY-MM-DD`
- 반환 (200 JSON): `current_price`, `change_pct`, `high_52w`, `low_52w`, `market_cap`, `atr_14`, `atr_pct`, `stop_loss_2atr`, `target_3atr`, `at_price`, `return_since_at_pct`
- 한국 종목: 6자리 숫자 입력 시 `.KS` → `.KQ` 순으로 yfinance 자동 폴백
- 캐시: in-memory 5분 + `Cache-Control: s-maxage=300, stale-while-revalidate=60` (Vercel Edge Cache)
- Rate limit: per-IP 60/분 (sliding window)
- CORS allow-list: `stock-analyst-jungwon1.vercel.app`, `localhost:4321`

## 성과 추적 (Day 14)

`/성과리뷰` 명령이 `knowledge-base/performance_history.md`에 행을 누적 append (8컬럼 표).
빌드 시 `build_kb.mjs`가 본 표를 파싱해 `kb.performance` (적중/오류/진행중/보류 + 적중률)를 생성.
PerformanceDonut 위젯은 누적 ≥ 1건이면 SVG 4-slice 도넛 + 적중률 % 표시, 0건이면 placeholder.

## 보안 모델

1. Vercel Deployment Protection (선택, Magic Link와 충돌 시 비활성화)
2. Supabase Auth Magic Link + 화이트리스트 이메일
3. RLS (Row Level Security) — 모든 테이블 `user_id = auth.uid()`
4. service_role 키는 빌드 시점에만 사용 (브라우저 노출 금지)

## 트러블슈팅

| 증상 | 원인 | 조치 |
|---|---|---|
| 매직 링크 클릭 후 redirect_to 오류 | Supabase Auth → URL Configuration 미등록 | Site URL + Redirect URLs 추가 |
| `/` 접근 시 무한 리다이렉트 | LocalStorage `sb-stock-analyst-auth` 손상 | DevTools에서 키 삭제 후 재로그인 |
| 다른 이메일 로그인 성공 | `PUBLIC_ALLOWED_EMAIL` 미설정 또는 Vercel 환경변수 누락 | Vercel + 로컬 모두 설정 후 재배포 |
| 빌드 시 `python: command not found` | Vercel 컨테이너 Python 부재 | 모든 빌드 스크립트는 Node `.mjs` 사용 (포팅 완료) |
| FlexSearch 검색 무응답 | search-data.json 미생성 | `npm run build` 또는 `node scripts/build_search_index.mjs` |
