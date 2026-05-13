-- ===========================================================
-- 종목분석 에이전트 — Supabase 스키마 (PLAN.md §6.1)
-- 실행 위치: Supabase Dashboard → SQL Editor → New query
-- 실행 순서: 1) schema.sql → 2) rls.sql → 3) verify.sql
--
-- 사용자 1인이지만 RLS 정책상 user_id 필드는 유지
-- (Phase 3에서 가족 공유 등 확장 가능성 대비)
-- ===========================================================

-- 사용자 포트폴리오 (로컬 user_portfolio.md 파일의 미러)
-- SSoT는 항상 로컬 md, Supabase는 web read 용 미러
create table if not exists portfolios (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id),
  profile jsonb not null,                       -- 투자 성향, 적립금, 기간, 관심 테마
  total_value_usd numeric,
  total_value_krw numeric,
  exchange_rate numeric,
  updated_at timestamptz not null default now(),
  source text not null default 'local_md'       -- 'local_md' | 'web' (Phase 3 양방향)
);

-- 보유 종목
create table if not exists holdings (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references portfolios(id) on delete cascade,
  ticker text not null,
  name text not null,
  asset_type text,                              -- 'ETF' | 'STOCK' | 'CRYPTO' | 'CASH'
  market text,                                  -- 'NYSE' | 'NASDAQ' | 'KRX' 등
  quantity numeric not null,
  avg_buy_price numeric,
  current_price numeric,
  current_value_usd numeric,
  weight_pct numeric,
  return_pct numeric,
  updated_at timestamptz not null default now()
);

-- 모델 포트폴리오 (4종 — 안전/중립/공격/배당)
create table if not exists model_portfolios (
  id uuid primary key default gen_random_uuid(),
  type text not null,                           -- 'safe' | 'balanced' | 'aggressive' | 'dividend'
  asset_class text not null,                    -- '미국 주식' | '한국 주식' | '채권' 등
  target_pct numeric not null,
  updated_at timestamptz not null default now()
);

-- 리포트 메타데이터 (검색·필터용 — 빌드 타임에 채워짐)
-- 정적 매니페스트(JSON) 우선이지만 Supabase에도 저장하여 SQL 검색 옵션 유지
create table if not exists reports (
  id uuid primary key default gen_random_uuid(),
  filename text not null unique,                -- 'morning_20260429.html' 등
  type text not null,                           -- 'morning' | 'evening' | 'weekly' | 'crypto'
                                                -- | 'user_portfolio' | 'stock_analysis' | 'etf'
  ticker text,                                  -- 종목분석/ETF만
  date date not null,
  title text,
  summary text,
  size_bytes integer,
  url_path text not null,
  created_at timestamptz not null default now()
);

create index if not exists idx_reports_type_date on reports(type, date desc);
create index if not exists idx_reports_ticker on reports(ticker) where ticker is not null;

-- ===========================================================
-- [v3.22, 2026-05-14] holdings UNIQUE constraint (UPSERT 용)
-- 같은 portfolio + 같은 ticker 는 행 1개만 유지 (수량·평단 누적 갱신)
-- ===========================================================
do $$ begin
  if not exists (
    select 1 from pg_constraint where conname = 'holdings_portfolio_ticker_unique'
  ) then
    alter table holdings add constraint holdings_portfolio_ticker_unique
      unique (portfolio_id, ticker);
  end if;
end $$;

-- ===========================================================
-- [v3.22] trade_log — 사용자 매수/매도 기록 (DailyPick 모달 입력)
-- ===========================================================
create table if not exists trade_log (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id),
  ticker text not null,
  name text,
  action text not null check (action in ('buy', 'sell')),
  quantity numeric not null check (quantity > 0),
  price numeric not null check (price > 0),
  currency text not null default 'USD' check (currency in ('USD', 'KRW')),
  -- 추천에서 발화된 거래 추적 (선택)
  pick_id uuid,                                  -- daily_picks_log.id FK (느슨)
  recommended_price numeric,
  recommended_score numeric,
  -- 메모
  note text,
  executed_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);

create index if not exists idx_trade_log_user_date on trade_log(user_id, executed_at desc);
create index if not exists idx_trade_log_ticker on trade_log(ticker);

-- ===========================================================
-- [v3.22] daily_picks_log — 매일 추천 + 사용자 액션 추적
-- 학습 데이터: 어떤 추천이 실제 매수로 이어졌는지, 시점 신뢰도, 사용자 패턴
-- ===========================================================
create table if not exists daily_picks_log (
  id uuid primary key default gen_random_uuid(),
  pick_date date not null,
  ticker text not null,
  name text,
  -- 추천 메타 (manifest + scorecard 발췌)
  score numeric not null,
  grade text,                                    -- '강력매수' | '매수' | '중립' 등
  recommended_buy_price numeric,
  recommended_stop_price numeric,
  recommended_tp_price numeric,
  holding_period_days integer,                   -- 예상 보유 기간 (산출 가능 시)
  reasons jsonb,                                 -- 매수 이유 bullet 배열
  currency text not null default 'USD',
  market text,                                   -- 'NASDAQ' | 'NYSE' | 'KRX' 등
  category text,                                 -- '신규(미보유)' | '리마인드(소량보유)' | '폴백'
  -- 사용자 액션 추적
  user_id uuid references auth.users(id),
  user_action text check (user_action in ('bought', 'dismissed', 'pending')),
  user_action_at timestamptz,
  trade_log_id uuid references trade_log(id),
  created_at timestamptz not null default now(),
  -- 같은 날 같은 종목 추천은 1행만
  constraint daily_picks_unique unique (pick_date, ticker)
);

create index if not exists idx_daily_picks_date on daily_picks_log(pick_date desc);
create index if not exists idx_daily_picks_user_action on daily_picks_log(user_id, user_action);

-- trade_log → daily_picks_log 의 pick_id FK (느슨, ON DELETE SET NULL)
-- 위 trade_log 생성 후 daily_picks_log 생성 순서라 alter 로 처리
do $$ begin
  if not exists (
    select 1 from pg_constraint where conname = 'trade_log_pick_fk'
  ) then
    alter table trade_log add constraint trade_log_pick_fk
      foreign key (pick_id) references daily_picks_log(id) on delete set null;
  end if;
end $$;

-- ===========================================================
-- Phase 3 예약 (보류)
-- ===========================================================
-- create table memos (
--   id uuid primary key default gen_random_uuid(),
--   user_id uuid references auth.users(id),
--   report_id uuid references reports(id),
--   content text,
--   created_at timestamptz default now()
-- );

-- ===========================================================
-- 완료. 다음: rls.sql 실행
-- ===========================================================
