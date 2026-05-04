-- ===========================================================
-- Day 1 검증 쿼리 — schema.sql + rls.sql 적용 후 실행
--
-- 기대 결과:
-- - 4개 테이블 모두 존재
-- - 모두 RLS 활성화 상태
-- - 5개 정책(policy) 모두 존재
-- - 모든 테이블 row 0건
-- ===========================================================

-- ① 테이블 존재 확인 (4행 기대)
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name in ('portfolios', 'holdings', 'model_portfolios', 'reports')
order by table_name;

-- ② RLS 활성화 상태 확인 (4행 모두 rowsecurity = true 기대)
select schemaname, tablename, rowsecurity
from pg_tables
where schemaname = 'public'
  and tablename in ('portfolios', 'holdings', 'model_portfolios', 'reports')
order by tablename;

-- ③ 정책 존재 확인 (5행 기대)
select tablename, policyname, cmd
from pg_policies
where schemaname = 'public'
order by tablename, policyname;

-- ④ 인덱스 확인 (idx_reports_type_date, idx_reports_ticker 기대)
select indexname, tablename
from pg_indexes
where schemaname = 'public'
  and tablename = 'reports'
order by indexname;

-- ⑤ 빈 테이블 확인 (모두 0 기대)
select 'portfolios'       as t, count(*) as n from portfolios
union all
select 'holdings'         as t, count(*) as n from holdings
union all
select 'model_portfolios' as t, count(*) as n from model_portfolios
union all
select 'reports'          as t, count(*) as n from reports;

-- ===========================================================
-- 모두 기대 결과면 Day 1 DB 셋업 완료
-- 다음 단계: SETUP.md §3 — Auth 설정
-- ===========================================================
