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
-- Phase 3 예약 테이블 (이번 작업에서는 생성하지 않음 — 미래 참고용)
-- ===========================================================
-- create table memos (
--   id uuid primary key default gen_random_uuid(),
--   user_id uuid references auth.users(id),
--   report_id uuid references reports(id),
--   content text,
--   created_at timestamptz default now()
-- );
--
-- create table trade_log (
--   id uuid primary key default gen_random_uuid(),
--   user_id uuid references auth.users(id),
--   ticker text not null,
--   action text not null,                       -- 'buy' | 'sell'
--   quantity numeric,
--   price numeric,
--   recommendation_report_id uuid references reports(id),
--   executed_at timestamptz
-- );

-- ===========================================================
-- 완료. 다음: rls.sql 실행
-- ===========================================================
