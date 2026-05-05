/**
 * Supabase 클라이언트 헬퍼.
 *
 * - createServerClient(): 빌드 시점 / 서버 사이드 전용 (service_role 키, RLS 우회)
 * - createPublicClient(): 클라이언트(브라우저)용 (anon 키, RLS 적용)
 * - createBrowserClient(): 브라우저용 + 세션 영속화 (Magic Link 인증)
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

/**
 * 브라우저 인증용 클라이언트 (싱글톤).
 * - persistSession: LocalStorage에 세션 저장 (탭 간 공유, 새로고침 유지)
 * - autoRefreshToken: 만료 전 자동 갱신
 * - detectSessionInUrl: Magic Link 콜백 URL의 access_token/refresh_token 파싱
 *
 * Supabase 대시보드의 JWT expiry 설정이 실제 세션 수명을 좌우 (기본 1주, 30일로 변경 권장).
 */
let _browserClient: SupabaseClient | null = null;
export function createBrowserClient(): SupabaseClient | null {
  if (typeof window === 'undefined') return null; // SSR/SSG 환경 가드
  if (_browserClient) return _browserClient;
  if (!URL_VAL || !ANON_KEY) return null;
  _browserClient = createClient(URL_VAL, ANON_KEY, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true,
      storage: window.localStorage,
      storageKey: 'sb-stock-analyst-auth',
    },
  });
  return _browserClient;
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
