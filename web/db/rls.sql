-- ===========================================================
-- RLS (Row Level Security) 정책 — PLAN.md §6.2
-- 실행 순서: schema.sql 다음, verify.sql 이전
--
-- 핵심 원칙:
-- - 모든 테이블 RLS 활성화
-- - 사용자는 본인 데이터만 read 가능
-- - write는 service_role 키로만 (RLS 우회 — sync 스크립트 전용)
-- ===========================================================

alter table portfolios       enable row level security;
alter table holdings         enable row level security;
alter table reports          enable row level security;
alter table model_portfolios enable row level security;

-- 본인 포트폴리오 read/write
drop policy if exists "own_portfolio_read"  on portfolios;
drop policy if exists "own_portfolio_write" on portfolios;
create policy "own_portfolio_read"  on portfolios
  for select using (auth.uid() = user_id);
create policy "own_portfolio_write" on portfolios
  for all    using (auth.uid() = user_id);

-- 본인 보유 종목 read (write는 service_role만)
drop policy if exists "own_holdings_read" on holdings;
create policy "own_holdings_read" on holdings
  for select using (
    exists (
      select 1 from portfolios p
      where p.id = holdings.portfolio_id
        and p.user_id = auth.uid()
    )
  );

-- reports와 model_portfolios는 인증된 사용자라면 read 가능
-- (write는 service_role만 — RLS 우회)
drop policy if exists "auth_reports_read" on reports;
drop policy if exists "auth_models_read"  on model_portfolios;
create policy "auth_reports_read" on reports
  for select using (auth.role() = 'authenticated');
create policy "auth_models_read"  on model_portfolios
  for select using (auth.role() = 'authenticated');

-- ===========================================================
-- [v3.22, 2026-05-14] trade_log + daily_picks_log RLS
-- 사용자는 본인 데이터만 read (write 는 service_role 전용 — /api/record-buy 가 처리)
-- ===========================================================
alter table trade_log        enable row level security;
alter table daily_picks_log  enable row level security;

drop policy if exists "own_trade_log_read" on trade_log;
create policy "own_trade_log_read" on trade_log
  for select using (auth.uid() = user_id);

-- [Astro SSG 환경] 클라이언트가 직접 본인 행 INSERT (anon 키로). service_role 우회 불요.
drop policy if exists "own_trade_log_insert" on trade_log;
create policy "own_trade_log_insert" on trade_log
  for insert with check (auth.uid() = user_id);

-- daily_picks_log 는 본인 액션 추적 행만 read.
-- user_id NULL 인 행 (= 아직 사용자 액션 전, "오늘의 추천" 자체) 도 인증 사용자면 read 허용.
drop policy if exists "own_or_open_picks_read" on daily_picks_log;
create policy "own_or_open_picks_read" on daily_picks_log
  for select using (
    auth.role() = 'authenticated'
    and (user_id is null or user_id = auth.uid())
  );

-- daily_picks_log INSERT/UPDATE 는 Phase 2 학습 자동화 단계 (현재 미사용 — service_role 만)
-- 현재 단계는 trade_log 기록만으로 추적. daily_picks_log 활성 시점에 정책 추가 예정.

-- ===========================================================
-- 완료. 다음: verify.sql 실행
-- ===========================================================
