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
-- 완료. 다음: verify.sql 실행
-- ===========================================================
