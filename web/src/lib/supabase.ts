/**
 * Supabase 클라이언트 헬퍼.
 *
 * - createServerClient(): 빌드 시점 / 서버 사이드 전용 (service_role 키, RLS 우회)
 * - createPublicClient(): 클라이언트(브라우저)용 (anon 키, RLS 적용)
 *
 * 환경변수 미설정 시 null 반환 → 호출자가 graceful fallback.
 */
import { createClient, type SupabaseClient } from '@supabase/supabase-js';

// Astro: PUBLIC_* 만 클라이언트 빌드에 inline. 그 외는 서버 사이드만 접근.
const URL_VAL =
  import.meta.env.PUBLIC_SUPABASE_URL ??
  (typeof process !== 'undefined' ? process.env.PUBLIC_SUPABASE_URL : undefined);

const SERVICE_KEY =
  import.meta.env.SUPABASE_SERVICE_KEY ??
  (typeof process !== 'undefined' ? process.env.SUPABASE_SERVICE_KEY : undefined);

const ANON_KEY =
  import.meta.env.PUBLIC_SUPABASE_ANON_KEY ??
  (typeof process !== 'undefined' ? process.env.PUBLIC_SUPABASE_ANON_KEY : undefined);

export function createServerClient(): SupabaseClient | null {
  if (!URL_VAL || !SERVICE_KEY) return null;
  return createClient(URL_VAL, SERVICE_KEY, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
}

export function createPublicClient(): SupabaseClient | null {
  if (!URL_VAL || !ANON_KEY) return null;
  return createClient(URL_VAL, ANON_KEY);
}

export type Portfolio = {
  id: string;
  user_id: string;
  profile: Record<string, string>;
  total_value_usd: number | null;
  total_value_krw: number | null;
  exchange_rate: number | null;
  updated_at: string;
  source: string;
};

export type Holding = {
  id: string;
  portfolio_id: string;
  ticker: string;
  name: string;
  asset_type: string | null;
  market: string | null;
  quantity: number;
  avg_buy_price: number | null;
  current_price: number | null;
  current_value_usd: number | null;
  weight_pct: number | null;
  return_pct: number | null;
  updated_at: string;
};
