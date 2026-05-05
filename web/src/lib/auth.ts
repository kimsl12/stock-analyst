/**
 * 인증 헬퍼 (PLAN.md §9.3).
 *
 * 1인 사용 + 화이트리스트 1개 이메일 모델.
 * - isAllowedUser: 클라이언트 사이드 1차 체크 (PUBLIC_ALLOWED_EMAIL 비교)
 * - signInWithMagicLink / signOut / getCurrentSession: Supabase Auth 래퍼
 * - requireAuth: 미인증 시 /login 리다이렉트 (인증 가드)
 * - enforceWhitelist: 콜백 후 비허용 이메일이면 강제 sign-out
 */
import type { Session } from '@supabase/supabase-js';
import { createBrowserClient } from './supabase';

const ALLOWED_EMAIL = (import.meta.env.PUBLIC_ALLOWED_EMAIL ?? '').toLowerCase().trim();

export function isAllowedUser(email: string | null | undefined): boolean {
  if (!email || !ALLOWED_EMAIL) return false;
  return email.toLowerCase().trim() === ALLOWED_EMAIL;
}

/** Magic Link 발송. 성공 시 메일함 안내 메시지 반환. */
export async function signInWithMagicLink(
  email: string,
  redirectTo: string,
): Promise<{ ok: true } | { ok: false; error: string }> {
  const sb = createBrowserClient();
  if (!sb) return { ok: false, error: 'Supabase 클라이언트 초기화 실패 (환경변수 미설정)' };

  // 화이트리스트 외 이메일은 발송 자체를 차단 (UX + 발송 비용 절감)
  if (!isAllowedUser(email)) {
    return { ok: false, error: '허용되지 않은 이메일입니다.' };
  }

  const { error } = await sb.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: redirectTo,
      shouldCreateUser: true, // 첫 가입 자동 생성 (이미 존재하면 무시)
    },
  });
  if (error) return { ok: false, error: error.message };
  return { ok: true };
}

export async function signOut(): Promise<void> {
  const sb = createBrowserClient();
  if (!sb) return;
  await sb.auth.signOut();
}

export async function getCurrentSession(): Promise<Session | null> {
  const sb = createBrowserClient();
  if (!sb) return null;
  const { data } = await sb.auth.getSession();
  return data.session ?? null;
}

/**
 * 콜백 후 화이트리스트 강제. 비허용 이메일이면 즉시 sign-out 후 false.
 * 허용 이메일이면 true.
 */
export async function enforceWhitelist(): Promise<{
  ok: boolean;
  email: string | null;
  reason?: string;
}> {
  const sb = createBrowserClient();
  if (!sb) return { ok: false, email: null, reason: 'no-client' };

  const { data, error } = await sb.auth.getUser();
  if (error || !data.user) return { ok: false, email: null, reason: 'no-user' };

  const email = data.user.email ?? null;
  if (!isAllowedUser(email)) {
    await sb.auth.signOut();
    return { ok: false, email, reason: 'not-allowed' };
  }
  return { ok: true, email };
}

/**
 * 클라이언트 사이드 인증 가드. 미인증 시 /login으로 리다이렉트.
 * Base.astro inline script에서 호출.
 */
export async function requireAuth(loginPath: string = '/login'): Promise<boolean> {
  const session = await getCurrentSession();
  if (!session) {
    const next = encodeURIComponent(window.location.pathname + window.location.search);
    window.location.replace(`${loginPath}?next=${next}`);
    return false;
  }
  // 화이트리스트 재검증 (세션이 살아있어도 이메일이 변경됐을 수 있음 — 방어적)
  if (!isAllowedUser(session.user.email)) {
    await signOut();
    window.location.replace(loginPath);
    return false;
  }
  return true;
}
