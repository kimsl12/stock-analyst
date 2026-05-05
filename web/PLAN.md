# 종목분석 에이전트 — 웹 플랫폼 PLAN.md

**작성일:** 2026-04-30
**버전:** v1.0 (MVP + Phase 2)
**위임 대상:** 외부 에이전트 (이 문서만 받아도 self-contained 작업 가능)
**목적:** AI 에이전트가 생성한 분석 리포트를 외부에서 인증 후 접근할 수 있는 웹 플랫폼 구축

---

## 0. 본 문서의 사용법 (위임받은 에이전트 필독)

이 PLAN.md는 단일 진실의 원천(SSoT)이다. 작업 중 의사결정이 필요하면:
1. 본 문서의 "결정 사항(§3)" 섹션을 먼저 확인
2. 명시되지 않은 사항은 사용자(`jungwon9402@gmail.com`)에게 질문
3. 본 문서를 임의로 변경하지 말고, 변경 필요 시 사용자 승인 후 갱신

작업 흐름:
- Day 단위로 분해된 작업(§13)을 순서대로 진행
- 각 Day마다 검증 기준 충족 후 다음 Day 진행
- 매 Day 종료 시 git commit (메시지 형식 §15 참조)
- 절대 금지 사항(§16)을 어기지 말 것

---

## 1. 프로젝트 개요

### 1.1 배경

현재 시스템:
- 로컬 Claude Code 환경에서 AI 에이전트가 종목 분석·시장 브리핑 HTML 리포트를 생성
- `reports/` 디렉토리에 HTML 누적 → main 브랜치 push → GitHub Pages 자동 배포
- 사용자(1인)는 GitHub Pages URL로 외부 접속

**현재 문제점:**
1. GitHub Actions 비활성화 (티켓 #4287825, 14일째 무진척) → Pages 자동 배포 마비
2. 누적된 60+ HTML 리포트의 인덱싱·검색·필터 기능 부재
3. user_portfolio 데이터가 로컬 md 파일이라 외부에서 조회 불가
4. 추천 종목의 사후 성과 추적 불가 (현재 가격과의 비교)

### 1.2 목표

GitHub 의존도 분산 + 사용성 개선을 위한 웹 플랫폼 구축:
- **외부 호스팅** (Vercel) — Actions 복구 보험
- **DB 백엔드** (Supabase) — 포트폴리오·메모·트래킹 데이터 저장
- **인증** (Supabase Auth Magic Link) — 1인 사용자 외부 노출 보안
- **인덱스·검색·필터·대시보드** — 누적 리포트 활용도 극대화
- **시간 머신** — 추천 종목의 사후 성과 자동 추적

### 1.3 범위 (In/Out)

**In (이번 작업 범위)**
- MVP: 리포트 인덱스, 3축 필터, 본문 검색, 카테고리 분류, Supabase 셋업, Magic Link 인증
- Phase 2: 대시보드 홈, 시간 머신, 종목 비교 빌더

**Out (Phase 3 — 계획만 명시, 본 작업에서는 미구현)**
- 개인 메모/노트
- 추천 vs 실제 매수 트래킹
- TradingView 위젯 통합
- PWA (오프라인 + 푸시 알림)
- 새 리포트 알림 (Supabase Realtime)

---

## 2. 핵심 의사결정 (사용자 확정)

| # | 결정 항목 | 결정 | 결정일 |
|---|---|---|---|
| 1 | user_portfolio 저장 전략 | **3중 동기화** (로컬 md 유지 + GitHub 유지 + Supabase 신규 추가) | 2026-04-30 |
| 2 | 인증 방식 | **Magic Link** (Supabase Auth, 이메일 1개만 등록) | 2026-04-30 |
| 3 | 도메인 | **`stock-analyst-jungwon1.vercel.app`** 무료 서브도메인 (원안 `stock-analyst-jungwon1.vercel.app`은 타 사용자가 점유 — 2026-05-04 변경, Vercel 자동 alias 그대로 채택) | 2026-04-30 / 2026-05-04 |
| 4 | 빌드 트리거 | 매 push 자동 빌드 (Vercel 기본) | 2026-04-30 |
| 5 | 호스팅 | **Vercel** (사용자 지정) | 2026-04-30 |
| 6 | DB | **Supabase** (사용자 지정) | 2026-04-30 |
| 7 | 프레임워크 | **Astro** (정적 SSG, Vercel 친화) | 2026-04-30 |
| 8 | Phase 2 기능 | 대시보드 + 시간 머신 + 종목 비교 (즐겨찾기 제외) | 2026-04-30 |
| 9 | 본 작업 범위 | MVP + Phase 2까지. Phase 3 계획만 명시 | 2026-04-30 |

---

## 3. 데이터 동기화 전략 (★ 중요)

### 3.1 단일 진실의 원천 (SSoT)

**user_portfolio 데이터: 로컬 md 파일이 SSoT**

이유:
- AI 에이전트가 직접 read/write하는 주체이므로 로컬 파일이 가장 신뢰성 있음
- GitHub은 백업 + 버전 이력
- Supabase는 웹 노출용 미러 (read-only on web)

### 3.2 동기화 방향

```
┌─────────────────────────────────────────────────┐
│  AI 에이전트 (briefing-lead, etc.)               │
│  ↓ write                                         │
│  knowledge-base/portfolio/user_portfolio.md      │  ← SSoT
│  ↓ git push                              ↓ sync  │
│  GitHub repo (백업·이력)            Supabase     │
│                                          ↑ read  │
│                                       Vercel 웹   │
└─────────────────────────────────────────────────┘
```

### 3.3 동기화 트리거

방식 A: **AI 에이전트가 user_portfolio.md write 직후 Supabase upsert** (권장)
- briefing-lead Phase 4 (사용자 입력 반영) 다음 단계에 추가
- Bash 호출: `python scripts/sync_portfolio_to_supabase.py`
- 실패 시 graceful: 경고만 표시, 로컬 작업은 계속

방식 B: GitHub Action으로 push 시 Supabase 자동 sync (Actions 복구 시 검토)

**v1: 방식 A 채택**

### 3.4 웹에서 포트폴리오 수정?

v1: **웹은 read-only**. 수정은 로컬 명령어 (`/내포트폴리오` 인터랙티브)로만.
v2 (Phase 3): 양방향 동기화 (웹에서 수정 → Supabase write → 로컬 md sync) — 추후 검토

### 3.5 충돌 처리

3중 저장이지만 SSoT가 로컬 md 단일이므로 **충돌은 발생할 수 없는 구조**. Supabase·GitHub은 항상 로컬 md의 후속 상태.

만약 Supabase에 직접 데이터가 들어가면 (수동 SQL 등) → 자동 덮어쓰기 (sync 시 로컬이 우선).

---

## 4. 기술 스택

| 레이어 | 기술 | 무료 한도 | 용도 |
|---|---|---|---|
| 호스팅 | Vercel (Hobby) | 100GB 대역폭/월, 1000 빌드/월 | 정적 + Serverless |
| 프레임워크 | Astro 4.x | - | SSG + Vue/React 컴포넌트 옵션 |
| DB | Supabase (Free) | 500MB DB, 1GB 파일, 2GB 대역폭 | Postgres + Auth + Edge Function |
| 인증 | Supabase Auth | Magic Link 무제한 (이메일 OTP) | 1인 사용자 보호 |
| 검색 | FlexSearch | - | 클라이언트 본문 검색 |
| 차트 | Chart.js 4.x | - | 대시보드 시각화 |
| Edge Function | Vercel Serverless (Python) | 100GB-Hours/월 | yfinance/pykrx 가격 fetch |
| 빌드 | Astro + 커스텀 Python 스크립트 | - | reports/ 매니페스트 생성 |
| 환경 | Node 20.x + Python 3.11+ | - | 빌드·런타임 |

**총 비용: 0원/월**

---

## 5. 디렉토리 구조

```
종목분석 에이전트/                          # 기존 프로젝트 루트
├── .claude/                                # 기존 — AI 에이전트 정의
├── analysis/                               # 기존 — 분석 산출물
├── knowledge-base/                         # 기존 — KB
├── reports/                                # 기존 — HTML 리포트
├── scripts/                                # 기존 + 신규
│   ├── fetch_price.py                      # 기존
│   └── sync_portfolio_to_supabase.py       # 신규 — Supabase 동기화
├── web/                                    # 신규 — 웹 플랫폼 (이번 작업)
│   ├── PLAN.md                             # 본 문서
│   ├── package.json                        # Node 의존성
│   ├── astro.config.mjs                    # Astro 설정
│   ├── tsconfig.json
│   ├── .env.local                          # 로컬 secrets (Git 제외)
│   ├── .env.example                        # 예시
│   ├── public/                             # 정적 자산
│   │   └── favicon.svg
│   ├── src/
│   │   ├── pages/                          # Astro 라우팅
│   │   │   ├── index.astro                 # 인덱스 (로그인 후 메인)
│   │   │   ├── login.astro                 # Magic Link 입력
│   │   │   ├── auth/callback.astro         # 인증 콜백
│   │   │   ├── briefing/[type].astro       # 브리핑 카테고리
│   │   │   ├── stocks/[ticker].astro       # 종목 상세
│   │   │   ├── portfolio/index.astro       # 포트폴리오 (Supabase read)
│   │   │   ├── dashboard.astro             # Phase 2: 대시보드
│   │   │   ├── timemachine.astro           # Phase 2: 시간 머신
│   │   │   ├── compare.astro               # Phase 2: 비교 빌더
│   │   │   └── api/
│   │   │       ├── price/[ticker].ts       # Phase 2: yfinance proxy
│   │   │       └── auth/                   # Magic Link 핸들러
│   │   ├── components/
│   │   │   ├── ReportCard.astro
│   │   │   ├── FilterBar.astro
│   │   │   ├── SearchBox.astro
│   │   │   ├── ThemeToggle.astro
│   │   │   ├── DonutChart.astro            # Phase 2
│   │   │   └── Timeline.astro              # Phase 2
│   │   ├── layouts/
│   │   │   ├── Base.astro                  # 다크/라이트 토글 포함
│   │   │   └── Authenticated.astro         # 인증 보호 래퍼
│   │   ├── lib/
│   │   │   ├── supabase.ts                 # Supabase 클라이언트
│   │   │   ├── manifest.ts                 # 빌드 타임 매니페스트 로더
│   │   │   ├── search.ts                   # FlexSearch 인덱스
│   │   │   └── auth.ts                     # 인증 헬퍼
│   │   └── styles/
│   │       └── global.css                  # 다크/라이트 변수
│   └── scripts/
│       ├── build_manifest.mjs              # reports/ → manifest.json (Node, Vercel zero-config)
│       └── build_search_index.mjs          # 본문 → FlexSearch 인덱스 (Node, Day 5)
└── ...
```

---

## 6. Supabase 스키마 설계

### 6.1 테이블 (MVP + Phase 2)

```sql
-- ===========================================================
-- 사용자 1인이지만 RLS 정책상 user_id 필드는 유지
-- (Phase 3에서 가족 공유 등 확장 가능성 대비)
-- ===========================================================

-- 사용자 포트폴리오 (로컬 md 파일의 미러)
create table portfolios (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id),
  profile jsonb not null,           -- 투자 성향, 적립금, 기간, 관심테마
  total_value_usd numeric,
  total_value_krw numeric,
  exchange_rate numeric,
  updated_at timestamptz not null default now(),
  source text not null default 'local_md'  -- 'local_md' | 'web' (Phase 3)
);

-- 보유 종목
create table holdings (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references portfolios(id) on delete cascade,
  ticker text not null,
  name text not null,
  asset_type text,                  -- 'ETF' | 'STOCK' | 'CRYPTO' | 'CASH'
  market text,                      -- 'NYSE' | 'NASDAQ' | 'KRX' | etc.
  quantity numeric not null,
  avg_buy_price numeric,
  current_price numeric,
  current_value_usd numeric,
  weight_pct numeric,
  return_pct numeric,
  updated_at timestamptz not null default now()
);

-- 모델 포트폴리오 (4종 — 안전/중립/공격/배당)
create table model_portfolios (
  id uuid primary key default gen_random_uuid(),
  type text not null,               -- 'safe' | 'balanced' | 'aggressive' | 'dividend'
  asset_class text not null,        -- '미국 주식' | '한국 주식' | '채권' | etc.
  target_pct numeric not null,
  updated_at timestamptz not null default now()
);

-- 리포트 메타데이터 (검색·필터용 — 빌드 타임에 채워짐)
-- 정적 매니페스트 우선이지만 Supabase에도 저장하여 SQL 검색 옵션 유지
create table reports (
  id uuid primary key default gen_random_uuid(),
  filename text not null unique,    -- 'morning_20260429.html' 등
  type text not null,               -- 'morning' | 'evening' | 'weekly' | 'crypto' | 'user_portfolio' | 'stock_analysis' | 'etf'
  ticker text,                      -- 종목분석/ETF만
  date date not null,
  title text,
  summary text,
  size_bytes integer,
  url_path text not null,
  created_at timestamptz not null default now()
);

create index idx_reports_type_date on reports(type, date desc);
create index idx_reports_ticker on reports(ticker) where ticker is not null;

-- ===========================================================
-- Phase 3 예약 테이블 (이번 작업에서는 생성하지 않음 — 미래 참고용)
-- ===========================================================

-- create table memos (
--   id uuid primary key default gen_random_uuid(),
--   user_id uuid references auth.users(id),
--   report_id uuid references reports(id),
--   content text,
--   created_at timestamptz default now()
-- );

-- create table trade_log (
--   id uuid primary key default gen_random_uuid(),
--   user_id uuid references auth.users(id),
--   ticker text not null,
--   action text not null,             -- 'buy' | 'sell'
--   quantity numeric,
--   price numeric,
--   recommendation_report_id uuid references reports(id),
--   executed_at timestamptz
-- );
```

### 6.2 RLS (Row Level Security) 정책

```sql
alter table portfolios enable row level security;
alter table holdings enable row level security;
alter table reports enable row level security;
alter table model_portfolios enable row level security;

-- 본인 데이터만 read/write
create policy "own_portfolio_read" on portfolios
  for select using (auth.uid() = user_id);
create policy "own_portfolio_write" on portfolios
  for all using (auth.uid() = user_id);

create policy "own_holdings_read" on holdings
  for select using (
    exists(select 1 from portfolios p where p.id = holdings.portfolio_id and p.user_id = auth.uid())
  );

-- reports와 model_portfolios는 인증된 사용자 read 가능 (write는 service_role만)
create policy "auth_reports_read" on reports
  for select using (auth.role() = 'authenticated');
create policy "auth_models_read" on model_portfolios
  for select using (auth.role() = 'authenticated');
```

### 6.3 사용자 등록

Magic Link 1인 사용이지만 Supabase Auth는 사용자 테이블 자동 관리.
초기 설정: Supabase 대시보드 → Authentication → Email 템플릿에 한국어 적용.
**허용 이메일: `jungwon9402@gmail.com`** (RLS 또는 Auth Hook으로 화이트리스트 강제)

---

## 7. AI 에이전트 ↔ Supabase 어댑터

### 7.1 sync 스크립트

`scripts/sync_portfolio_to_supabase.py` 신규 작성:

```python
"""
사용자 포트폴리오 로컬 md → Supabase 동기화

사용법:
    python scripts/sync_portfolio_to_supabase.py

briefing-lead의 /내포트폴리오 Phase 4 (사용자 입력 반영) 다음에 자동 호출.
실패 시 경고만 표시, 로컬 작업은 영향 없음.
"""
import os, sys, re, json
from datetime import datetime
from pathlib import Path

try:
    from supabase import create_client
except ImportError:
    print("WARN: supabase-py 미설치 — sync 스킵", file=sys.stderr)
    sys.exit(0)  # 로컬 작업은 계속

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")  # service_role 키
USER_EMAIL = "jungwon9402@gmail.com"

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("WARN: Supabase 환경변수 미설정 — sync 스킵", file=sys.stderr)
    sys.exit(0)

# 1. user_portfolio.md 파싱 (CURRENT 섹션의 표 구조)
# 2. 사용자 ID 조회 (USER_EMAIL → auth.users)
# 3. portfolios upsert (단일 row, user_id 기준)
# 4. holdings 전체 삭제 후 재삽입 (transactional)
# 5. 결과 stdout 출력
```

상세 구현은 위임 에이전트가 작성. 핵심 룰:
- **graceful fail** — Supabase 실패해도 로컬·GitHub 작업은 계속
- **service_role 키** 사용 (RLS 우회, AI 에이전트 권한 강함)
- **idempotent** — 여러 번 실행해도 같은 결과

### 7.2 briefing-lead 통합

`.claude/agents/briefing-lead.md`의 `/내포트폴리오` Phase 4 마지막에 추가:

```
[Phase 4-후] Supabase 동기화 (선택, graceful fail)
  - Bash: python scripts/sync_portfolio_to_supabase.py
  - 성공: stdout "OK: portfolio synced"
  - 실패: 경고 박스로 표시 (분석 결과는 영향 없음)
  - 환경변수 미설정: 자동 SKIP, 경고 없음
```

위임 에이전트가 이 통합도 수행.

### 7.3 reports 매니페스트 동기화

`scripts/sync_reports_to_supabase.py`:
- `reports/` 디렉토리 스캔 → Supabase reports 테이블에 upsert
- 빌드 타임에 Vercel이 호출 (또는 Cron Action)
- v1에서는 정적 매니페스트(JSON)와 병행

---

## 8. 라우팅 / 페이지 구조

### 8.1 페이지 목록

| 라우트 | 파일 | 인증 | 설명 |
|---|---|---|---|
| `/login` | `pages/login.astro` | ❌ | Magic Link 이메일 입력 |
| `/auth/callback` | `pages/auth/callback.astro` | ❌ | Magic Link 클릭 처리 |
| `/` | `pages/index.astro` | ✅ | 인덱스 (모든 리포트 카드 그리드) |
| `/briefing/morning` | `pages/briefing/[type].astro` | ✅ | 모닝 브리핑 모음 |
| `/briefing/evening` | 동일 | ✅ | 이브닝 브리핑 모음 |
| `/briefing/weekly` | 동일 | ✅ | 주간 리포트 모음 |
| `/stocks` | `pages/stocks/index.astro` | ✅ | 종목분석 인덱스 |
| `/stocks/MRVL` | `pages/stocks/[ticker].astro` | ✅ | 종목 상세 (HTML 임베드) |
| `/portfolio` | `pages/portfolio/index.astro` | ✅ | 사용자 포트폴리오 (Supabase read) |
| `/dashboard` | `pages/dashboard.astro` | ✅ | **Phase 2** 대시보드 홈 |
| `/timemachine` | `pages/timemachine.astro` | ✅ | **Phase 2** 시간 머신 |
| `/compare?a=X&b=Y` | `pages/compare.astro` | ✅ | **Phase 2** 종목 비교 |

### 8.2 인증 보호

`layouts/Authenticated.astro` 래퍼로 모든 인증 페이지 감싸기:
- Supabase 세션 확인
- 미인증 시 `/login`으로 리다이렉트
- 화이트리스트 이메일 확인 (`jungwon9402@gmail.com` 외 차단)

### 8.3 매니페스트 기반 정적 라우팅

빌드 타임:
1. `scripts/build_manifest.py` 실행 → `reports/` 스캔 → `web/src/data/manifest.json` 생성
2. Astro 빌드 시 manifest 로드 → 동적 라우트 prerender
3. FlexSearch 인덱스 빌드 → `web/public/search-index.json`

---

## 9. 인증 흐름 (Magic Link)

### 9.1 흐름도

```
1. 사용자가 stock-analyst-jungwon1.vercel.app 접속
2. 미인증 → /login 자동 리다이렉트
3. 이메일 입력 (jungwon9402@gmail.com 외 차단)
4. Supabase 매직 링크 발송
5. 이메일에서 링크 클릭 → /auth/callback
6. 세션 토큰 저장 (브라우저 LocalStorage + httpOnly cookie)
7. / 인덱스로 리다이렉트
8. 30일 세션 유지 (자동 갱신)
```

### 9.2 환경변수

```bash
# web/.env.local (Git 제외)
PUBLIC_SUPABASE_URL=https://xxx.supabase.co
PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...   # 서버 사이드만 (sync 스크립트용)
PUBLIC_ALLOWED_EMAIL=jungwon9402@gmail.com   # SSG 클라 가드용 (빌드 임베드)
```

Vercel 환경변수에도 동일 설정.

> **주의**: `output: 'static'` SSG 환경에서 클라이언트 사이드 화이트리스트 검증을
> 위해 `PUBLIC_` 접두사가 필요. 이메일 자체는 빌드 산출물에 노출되나, 실제
> 차단은 Supabase 콜백 거부 + sign-out + RLS의 다중 방어로 처리.

### 9.3 화이트리스트 강제

```typescript
// web/src/lib/auth.ts
export function isAllowedUser(email: string): boolean {
  const allowed = import.meta.env.PUBLIC_ALLOWED_EMAIL;
  return email.toLowerCase() === allowed.toLowerCase();
}
```

비허용 이메일이 매직 링크 받아도 콜백에서 거부 + 즉시 sign out.

---

## 10. 검색·필터 설계

### 10.1 3축 필터

| 축 | 옵션 | 데이터 소스 |
|---|---|---|
| 종류 | 모닝/이브닝/주간/크립토/내포트폴리오/종목분석/ETF | 매니페스트 `type` |
| 날짜 | 최근 7일 / 30일 / 90일 / 1년 / 전체 | 매니페스트 `date` |
| 종목 | 텍스트 입력 + 자동완성 | 매니페스트 `ticker` |

### 10.2 본문 검색 (FlexSearch)

빌드 타임:
- `reports/` 모든 HTML 파싱 → 본문 텍스트 추출
- FlexSearch 인덱스 생성 → `public/search-index.json`
- 클라이언트가 lazy load
- 검색 결과: 매칭 리포트 + 미리보기 스니펫

### 10.3 카테고리 자동 분류

매니페스트 빌더가 파일명 패턴으로 자동 분류:
- `morning_*.html` → briefing/morning
- `evening_*.html` → briefing/evening
- `weekly_*.html` → briefing/weekly
- `crypto_*.html` → briefing/crypto
- `user_portfolio_*.html` → portfolio
- `{TICKER}_*.html` → stocks/{ticker} (대문자 패턴)
- `KODEX*_*.html` 등 ETF 패턴 → etfs

---

## 11. Phase 2 기능 상세

### 11.1 대시보드 홈 (`/dashboard`)

| 위젯 | 데이터 | 시각화 |
|---|---|---|
| 누적 카운트 | 매니페스트 집계 | metric-card 그리드 (브리핑 N개, 종목 N개, ETF N개) |
| 최근 7일 추천 풀 | 매니페스트 + 본문 파싱 | 종목 칩 클라우드 |
| 매크로 스냅샷 | KB market/daily_snapshot.md | metric-grid (S&P, VIX, Gold, USD/KRW) |
| 적중률 도넛 | KB performance_history.md | Chart.js 도넛 |
| 자산군 분포 | Supabase portfolios + holdings | Chart.js 도넛 (사용자 포트) |

### 11.2 시간 머신 (`/timemachine`)

UI:
- 슬라이더: 1주 / 1개월 / 3개월 전
- 리스트: 그 시점에 추천된 종목들
- 각 종목: 추천 당시 가격 → 현재 가격 → 수익률 자동 계산

데이터 흐름:
1. 매니페스트에서 N개월 전 리포트 필터링
2. 본문에서 추천 종목 추출 (`강력 매수`, `Top` 등 키워드)
3. **`/api/price/[ticker]` Edge Function 호출** → 현재 가격
4. 비교 표시

Edge Function (`web/src/pages/api/price/[ticker].ts`):
```typescript
// Vercel Serverless Function (Python 런타임)
// scripts/fetch_price.py 호출 → JSON 반환
// CORS 허용, 5분 캐시
```

### 11.3 종목 비교 빌더 (`/compare?a=MRVL&b=NVDA`)

UI:
- URL 파라미터로 두 종목 지정
- 화면 좌우 분할
- 좌: MRVL 분석 리포트 임베드
- 우: NVDA 분석 리포트 임베드
- 상단: 핵심 지표 비교 표 (PER, ATR, 점수, 등급 등)

데이터:
- 매니페스트에서 ticker별 최신 분석 리포트 조회
- 본문 메타데이터 추출

---

## 12. Phase 3 계획 (이번 작업 외 — 메모)

| 기능 | 예상 소요 | 의존 |
|---|---|---|
| 개인 메모 | 2일 | Supabase memos 테이블 추가 |
| 추천 vs 실제 매수 트래킹 | 4-5일 | Supabase trade_log + Edge Function 손익 계산 |
| TradingView 위젯 통합 | 2일 | 무료 위젯 임베드 (`tradingview.com/widget`) |
| PWA (오프라인 + 푸시) | 3-4일 | Service Worker + Web Push API |
| 새 리포트 알림 | 2일 | Supabase Realtime + 브라우저 알림 |
| 양방향 동기화 | 5일 | 충돌 해결 정책 + Supabase webhook |
| 가족 공유 | 3일 | Auth 화이트리스트 확장 + RLS 조정 |

본 작업에서는 **스키마·라우팅·UI 슬롯만 미리 예약**해두고 구현은 다음 작업에서.

---

## 13. Day별 작업 분해 (MVP + Phase 2, 2주)

### Week 1 — MVP

#### Day 1: Supabase 셋업

**작업:**
- [ ] Supabase 프로젝트 생성 (`stock-analyst` 또는 사용자 지정)
- [ ] Postgres 스키마 적용 (§6.1 SQL 실행)
- [ ] RLS 정책 적용 (§6.2)
- [ ] Auth → Email 템플릿 한국어 적용
- [ ] Magic Link 활성화 + 화이트리스트 이메일 등록 (`jungwon9402@gmail.com`)
- [ ] Service Role 키 발급 + 안전 보관
- [ ] `web/.env.example` 작성

**검증:**
- [ ] Supabase 대시보드에서 SQL Editor로 `select * from portfolios` 실행 → 빈 테이블 확인
- [ ] 매직 링크 테스트 (이메일 받기)

**Commit:** `feat(web): Supabase 프로젝트 셋업 + 스키마 적용`

#### Day 2: 포트폴리오 동기화 스크립트

**작업:**
- [ ] `scripts/sync_portfolio_to_supabase.py` 작성
- [ ] `requirements.txt`에 `supabase-py` 추가 (또는 별도 환경)
- [ ] user_portfolio.md 파서 작성 (CURRENT 섹션 표 추출)
- [ ] graceful fail 로직
- [ ] briefing-lead.md `/내포트폴리오` Phase 4-후에 호출 추가
- [ ] 1회 수동 실행 테스트 → Supabase에 데이터 들어감 확인

**검증:**
- [ ] `select * from portfolios` → 1행 (사용자 데이터)
- [ ] `select * from holdings` → 보유 종목 6~7개
- [ ] 환경변수 미설정 시 graceful skip 확인

**Commit:** `feat(web): user_portfolio Supabase 동기화 스크립트`

#### Day 3: Astro 프로젝트 + 매니페스트 빌더

**작업:**
- [ ] `cd web && npm create astro@latest .` (TypeScript, strict, no integrations)
- [ ] Vercel 어댑터 설치 (`@astrojs/vercel`)
- [ ] `scripts/build_manifest.py` 작성 — `reports/` 스캔 → `web/src/data/manifest.json`
  - 파일명 패턴 → type, ticker, date 추출
  - 파일 메타데이터 (size, mtime)
  - title 추출 (HTML `<title>`)
- [ ] Astro 빌드 hook에 통합 (`prebuild` script)
- [ ] Vercel 프로젝트 생성 + GitHub repo 연결
- [ ] 환경변수 등록 (Vercel 대시보드)
- [ ] 첫 배포 → `stock-analyst-jungwon1.vercel.app` 활성화 (빈 페이지라도)

**검증:**
- [ ] `manifest.json` 생성됨 (60+ 항목)
- [ ] Vercel 빌드 통과
- [ ] 배포 URL 접속 가능

**Commit:** `feat(web): Astro 프로젝트 + 매니페스트 빌더 + Vercel 배포`

#### Day 4: 인덱스 페이지 + 카드 그리드 + 카테고리 라우팅

**작업:**
- [ ] `layouts/Base.astro` (다크/라이트 토글, 헤더, 푸터)
- [ ] `components/ReportCard.astro` (제목, 날짜, 종류, 사이즈)
- [ ] `pages/index.astro` (모든 리포트 카드 그리드)
- [ ] `pages/briefing/[type].astro` (동적 라우트, type별 필터)
- [ ] `pages/stocks/index.astro` + `pages/stocks/[ticker].astro` (HTML iframe 임베드)
- [ ] `pages/portfolio/index.astro` (Supabase read, 보유 종목 표)
- [ ] CSS 변수 시스템 (briefing-report-generator와 동일 팔레트)
- [ ] 모바일 반응형

**검증:**
- [ ] `/` 접속 → 모든 카드 보임
- [ ] `/briefing/morning` → 모닝 브리핑만
- [ ] `/stocks/MRVL` → MRVL 분석 임베드
- [ ] `/portfolio` → Supabase 데이터 표시

**Commit:** `feat(web): MVP 인덱스 + 카테고리 라우팅 + 포트폴리오 페이지`

#### Day 5: 3축 필터 + 검색 인덱스

**작업:**
- [ ] `components/FilterBar.astro` (종류·날짜·종목 셀렉터)
- [ ] 클라이언트 JS 필터링 로직
- [ ] `scripts/build_search_index.py` 작성 — 본문 텍스트 추출 + FlexSearch 인덱스
- [ ] `components/SearchBox.astro` (검색 입력 + 결과 드롭다운)
- [ ] FlexSearch 클라이언트 통합 (lazy load)
- [ ] 검색 결과: 매칭 리포트 + 200자 스니펫

**검증:**
- [ ] 필터 3축 모두 작동
- [ ] 검색어 입력 → 결과 즉시 표시
- [ ] 모바일에서 검색 UI 정상

**Commit:** `feat(web): 3축 필터 + FlexSearch 본문 검색`

#### Day 6: Magic Link 인증 + 화이트리스트

**작업:**
- [x] `lib/supabase.ts` (Supabase 클라이언트, createBrowserClient 추가)
- [x] `lib/auth.ts` (세션·화이트리스트 헬퍼: isAllowedUser/signIn/signOut/requireAuth/enforceWhitelist)
- [x] `pages/login.astro` (이메일 입력 폼)
- [x] `pages/auth/callback.astro` (콜백 처리 + 화이트리스트 검증)
- [x] `layouts/Authenticated.astro` (인증 보호 래퍼 — Base.astro thin wrapper)
- [x] 모든 인증 필요 페이지에 적용 (Base.astro inline + module 이중 가드, noAuth props로 /login·/auth/callback 예외)
- [x] 30일 세션 유지 설정 (클라이언트 측 persistSession + autoRefreshToken; 실제 만료는 Supabase 대시보드 JWT expiry 설정 필요)

**검증 (Day 6 후 사용자 측 확인):**
- [ ] 미인증 상태로 `/` 접속 → `/login` 리다이렉트
- [ ] `jungwon9402@gmail.com`으로 매직 링크 → 클릭 → 로그인 성공
- [ ] 다른 이메일 시도 → 콜백에서 즉시 거부 + sign out + 안내
- [ ] 30일 후 자동 갱신 확인 (Supabase 대시보드 JWT expiry = 2592000초 설정 후)

**사용자 작업 (커밋 후):**
1. Vercel 환경변수에 `PUBLIC_ALLOWED_EMAIL=jungwon9402@gmail.com` 추가
2. Supabase 대시보드 → Auth → URL Configuration:
   - Site URL: `https://stock-analyst-jungwon1.vercel.app`
   - Redirect URLs: `https://stock-analyst-jungwon1.vercel.app/auth/callback` 추가 (로컬 테스트 시 `http://localhost:4321/auth/callback`도 추가)
3. Supabase 대시보드 → Auth → Providers → Email: Magic Link 활성화 (기본 활성)
4. Supabase 대시보드 → Auth → Sessions → JWT expiry: `2592000` (30일)
5. (선택) Vercel Project Settings → Deployment Protection: 비활성화 (Magic Link 동작 위해 공개 필수)

**Commit:** `feat(web): Magic Link 인증 + 이메일 화이트리스트`

#### Day 7: MVP 마감 + 다크/라이트 + 검증

**작업:**
- [ ] `components/ThemeToggle.astro` (다크/라이트 토글, LocalStorage 저장)
- [ ] CSS 변수 라이트 테마 분기
- [ ] 모든 페이지 다크/라이트 일관성
- [ ] Lighthouse 점수 측정 (모바일·데스크탑)
- [ ] 검증 체크리스트 통과
- [ ] README.md (web/ 디렉토리)
- [ ] 배포 URL 사용자 공유

**검증:**
- [ ] 다크/라이트 토글 정상
- [ ] Lighthouse 성능 90+
- [ ] 모든 페이지 모바일 대응
- [ ] 60+ 리포트 모두 접근 가능

**Commit:** `feat(web): MVP 완료 — 다크/라이트 + 검증`

### Week 2 — Phase 2

#### Day 8-9: 대시보드 홈

**작업:**
- [ ] `pages/dashboard.astro`
- [ ] 누적 카운트 위젯 (매니페스트 집계)
- [ ] 최근 7일 추천 종목 풀 (본문 파싱 → 키워드 추출)
- [ ] 매크로 스냅샷 (KB daily_snapshot.md 빌드 타임 로드)
- [ ] 자산군 분포 도넛 (Supabase 데이터 + Chart.js)
- [ ] 적중률 도넛 (KB performance_history.md, 파일 없으면 SKIP)

**검증:**
- [ ] `/dashboard` → 모든 위젯 렌더
- [ ] Chart.js 도넛 정상 표시
- [ ] 모바일 그리드 1열 변환

**Commit:** `feat(web): Phase 2 — 대시보드 홈`

#### Day 10-11: Edge Function (가격 fetch API)

**작업:**
- [ ] `web/src/pages/api/price/[ticker].ts` Vercel Serverless Function
- [ ] Python 런타임으로 `scripts/fetch_price.py` 호출
- [ ] 또는 yfinance/pykrx 직접 호출 (Python serverless)
- [ ] CORS 허용 (자체 origin만)
- [ ] 5분 캐시 (Vercel KV 또는 Edge Cache)
- [ ] Rate limit (분당 60회)

**검증:**
- [ ] `curl https://stock-analyst-jungwon1.vercel.app/api/price/MRVL` → JSON
- [ ] 한국 종목 (`/api/price/012450`) 정상
- [ ] 캐시 hit 시 응답 속도 < 100ms

**Commit:** `feat(web): Phase 2 — 가격 fetch Edge Function`

#### Day 12-13: 시간 머신

**작업:**
- [ ] `pages/timemachine.astro`
- [ ] 슬라이더 UI (1주/1개월/3개월)
- [ ] 시점별 추천 종목 추출 (빌드 타임)
- [ ] 클라이언트에서 `/api/price` 호출 → 현재 가격
- [ ] 비교 표 (추천 당시 가 → 현재 가 → 수익률)
- [ ] 정렬 (수익률 순)

**검증:**
- [ ] `/timemachine` → 슬라이더 작동
- [ ] 추천 당시 가격 + 현재 가격 표시
- [ ] 수익률 색상 코딩 (양/음)

**Commit:** `feat(web): Phase 2 — 시간 머신`

#### Day 14: 종목 비교 빌더 + 마감

**작업:**
- [ ] `pages/compare.astro` (URL 파라미터 `?a=&b=`)
- [ ] 좌우 분할 레이아웃
- [ ] 두 종목 분석 리포트 임베드
- [ ] 핵심 지표 비교 표 (PER, ATR, 점수 등)
- [ ] 모바일에서는 상하 분할
- [ ] 최종 회귀 테스트
- [ ] README 갱신
- [ ] Phase 3 백로그 issue 작성 (계획만)

**검증:**
- [ ] `/compare?a=MRVL&b=NVDA` → 비교 표시
- [ ] 비교 표 정확
- [ ] 모바일 상하 분할

**Commit:** `feat(web): Phase 2 완료 — 종목 비교 빌더 + 마감`

---

## 14. CI/CD

### 14.1 Vercel 자동 배포

- GitHub `main` push → 자동 빌드 + 배포
- Preview deployment: feature 브랜치 push 시 별도 URL 생성
- 빌드 명령: `npm run build` (Astro)
- prebuild 훅: `python scripts/build_manifest.py && python scripts/build_search_index.py`

### 14.2 환경변수 (Vercel 대시보드)

| 키 | 값 | 노출 |
|---|---|---|
| `PUBLIC_SUPABASE_URL` | https://xxx.supabase.co | 클라이언트 |
| `PUBLIC_SUPABASE_ANON_KEY` | eyJ... | 클라이언트 |
| `SUPABASE_SERVICE_KEY` | eyJ... | 서버만 |
| `ALLOWED_EMAIL` | jungwon9402@gmail.com | 서버만 |

### 14.3 .gitignore 추가

```
# web/
web/node_modules/
web/.astro/
web/dist/
web/.env.local
web/src/data/manifest.json   # 빌드 산출물
web/public/search-index.json # 빌드 산출물
```

---

## 15. Commit 메시지 규칙

```
{type}(web): {간단한 설명}

{상세 내용 — 선택}

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

`type`: `feat` | `fix` | `chore` | `docs` | `refactor` | `test`

매 Day 종료 시 commit 1회 이상.

---

## 16. 절대 금지 사항

위임 에이전트는 다음을 절대 어기지 말 것:

1. **본 PLAN.md 임의 변경 금지** — 변경 필요 시 사용자(`jungwon9402@gmail.com`)에게 질문
2. **Supabase Service Key 클라이언트 노출 금지** — 항상 서버 사이드만
3. **`SUPABASE_SERVICE_KEY` 또는 인증 토큰 commit 금지**
4. **사용자 포트폴리오 평문 노출 금지** — 인증 보호 페이지에서만 표시
5. **다른 이메일로 인증 허용 금지** — 화이트리스트 강제
6. **AI 에이전트 코드 수정 금지** (단, briefing-lead Phase 4-후 sync 호출 추가는 예외 — §7.2)
7. **로컬 user_portfolio.md를 Supabase write 결과로 덮어쓰기 금지** — SSoT는 항상 로컬 md
8. **Phase 3 기능 미리 구현 금지** — 스키마 슬롯만 예약
9. **vercel.app 외 도메인 구입 금지** — 사용자 결정 시점까지
10. **Pages 자동 배포 의존 코드 작성 금지** — Vercel 빌드 단독 자립

---

## 17. 위임받은 에이전트 — 작업 시작 체크리스트

작업 시작 전 확인:

- [ ] 본 PLAN.md 전체 1회 정독
- [ ] 사용자 이메일: `jungwon9402@gmail.com` 확인
- [ ] 프로젝트 루트: `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트`
- [ ] 외장 SSD 파일시스템 quirks 인지 (한글 파일명, ._* 메타파일, CRLF)
- [ ] Git 사용자: `kimsl12 <jungwon9402@gmail.com>`
- [ ] 작업 위치: `web/` 디렉토리 (신규 생성됨)
- [ ] 기존 코드 수정 최소화 (briefing-lead 한 줄 추가 외 X)
- [ ] 매 Day 완료 시 commit + push
- [ ] 막히면 사용자에게 즉시 질문

작업 시작:
```bash
cd "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/web"
# Day 1부터 시작
```

---

## 18. 변경 이력

| 일자 | 버전 | 변경 | 작성자 |
|---|---|---|---|
| 2026-04-30 | v1.0 | 초안 작성 (MVP + Phase 2) | Claude Opus 4.7 + 사용자 |

---

**END OF PLAN.md**
