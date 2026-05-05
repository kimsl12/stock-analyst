/**
 * 인증 헬퍼 — 이메일 + 비밀번호 단일 흐름 (2026-05-05).
 *
 * 1인 사용 + 화이트리스트 1개 이메일.
 * 비밀번호는 `web/scripts/set_password.mjs`로 Supabase Admin API를 통해 직접 설정.
 * 매직링크/reset 흐름 모두 제거 — 사용자 결정.
 */
import type { Session } from '@supabase/supabase-js';
import { createBrowserClient } from './supabase';

const ALLOWED_EMAIL = (import.meta.env.PUBLIC_ALLOWED_EMAIL ?? '').toLowerCase().trim();

export function isAllowedUser(email: string | null | undefined): boolean {
  if (!email || !ALLOWED_EMAIL) return false;
  return email.toLowerCase().trim() === ALLOWED_EMAIL;
}

/** 이메일 + 비밀번호 로그인. 유일한 인증 흐름. */
export async function signInWithPassword(
  email: string,
  password: string,
): Promise<{ ok: true; email: string } | { ok: false; error: string }> {
  const sb = createBrowserClient();
  if (!sb) return { ok: false, error: 'Supabase 클라이언트 초기화 실패 (환경변수 미설정)' };

  if (!isAllowedUser(email)) {
    return { ok: false, error: '허용되지 않은 이메일입니다.' };
  }

  const { data, error } = await sb.auth.signInWithPassword({ email, password });
  if (error) {
    if (/invalid login credentials/i.test(error.message)) {
      return { ok: false, error: '이메일 또는 비밀번호가 올바르지 않습니다.' };
    }
    if (/email not confirmed/i.test(error.message)) {
      return { ok: false, error: '이메일 인증이 완료되지 않았습니다. 관리자에게 문의하세요.' };
    }
    return { ok: false, error: error.message };
  }
  if (!data.user?.email) return { ok: false, error: '사용자 정보 누락' };
  return { ok: true, email: data.user.email };
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

/** 콜백 후 화이트리스트 강제. 비허용이면 sign-out + false. */
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

/** 클라이언트 사이드 인증 가드. 미인증 시 /login 리다이렉트. */
export async function requireAuth(loginPath: string = '/login'): Promise<boolean> {
  const session = await getCurrentSession();
  if (!session) {
    const next = encodeURIComponent(window.location.pathname + window.location.search);
    window.location.replace(`${loginPath}?next=${next}`);
    return false;
  }
  if (!isAllowedUser(session.user.email)) {
    await signOut();
    window.location.replace(loginPath);
    return false;
  }
  return true;
}
