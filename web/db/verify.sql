-- ===========================================================
-- Day 1 종합 검증 쿼리 — schema.sql + rls.sql 적용 후 실행
--
-- 단일 결과셋 (8행)으로 통합. 마지막 status 컬럼이 모두 'OK'면 통과.
-- 하나라도 'FAIL'이면 SETUP.md §6 트러블슈팅 참조.
--
-- ※ Supabase SQL Editor는 여러 SELECT 실행 시 마지막 결과만 UI에 표시되므로,
--   섹션별 분리 대신 단일 결과셋으로 통합함.
-- ===========================================================

with checks as (
  -- ① 테이블 4개 존재 확인
  select
    1                               as ord,
    'tables_exist'                  as check_name,
    count(*)::text                  as actual,
    '4'                             as expected,
    'public 스키마에 4개 테이블 존재' as note
  from information_schema.tables
  where table_schema = 'public'
    and table_name in ('portfolios', 'holdings', 'model_portfolios', 'reports')

  union all
  -- ② RLS 활성화 4개 확인
  select
    2,
    'rls_enabled',
    count(*)::text,
    '4',
    '4개 테이블 모두 RLS 활성화'
  from pg_tables
  where schemaname = 'public'
    and tablename in ('portfolios', 'holdings', 'model_portfolios', 'reports')
    and rowsecurity = true

  union all
  -- ③ 정책 5개 존재 확인
  select
    3,
    'policies_count',
    count(*)::text,
    '5',
    'own_portfolio_read/write, own_holdings_read, auth_reports_read, auth_models_read'
  from pg_policies
  where schemaname = 'public'
    and tablename in ('portfolios', 'holdings', 'model_portfolios', 'reports')

  union all
  -- ④ 인덱스 2개 존재 확인 (PK 인덱스 제외, 명시적 인덱스만)
  select
    4,
    'indexes_count',
    count(*)::text,
    '2',
    'idx_reports_type_date + idx_reports_ticker'
  from pg_indexes
  where schemaname = 'public'
    and tablename = 'reports'
    and indexname in ('idx_reports_type_date', 'idx_reports_ticker')

  union all
  -- ⑤ row 0건 (4개 테이블)
  select 5, 'rows_portfolios',       count(*)::text, '0', '빈 테이블' from portfolios
  union all
  select 6, 'rows_holdings',         count(*)::text, '0', '빈 테이블' from holdings
  union all
  select 7, 'rows_model_portfolios', count(*)::text, '0', '빈 테이블' from model_portfolios
  union all
  select 8, 'rows_reports',          count(*)::text, '0', '빈 테이블' from reports
)
select
  check_name,
  expected,
  actual,
  case when actual = expected then 'OK' else 'FAIL' end as status,
  note
from checks
order by ord;

-- ===========================================================
-- 기대 결과: 8행 모두 status = 'OK'
--
-- FAIL이 보일 경우:
--   tables_exist FAIL  → schema.sql 다시 실행
--   rls_enabled  FAIL  → rls.sql의 alter table ... enable row level security 실행
--   policies_count FAIL → rls.sql의 create policy 5개 실행
--   indexes_count FAIL → schema.sql 마지막 create index 2개 실행
--   rows_* FAIL        → 의도치 않은 데이터 — 확인 후 truncate 결정
--
-- 모두 OK면 다음 단계: SETUP.md §3 — Auth 설정
-- ===========================================================
