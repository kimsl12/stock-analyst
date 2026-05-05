/**
 * 인증 헬퍼 (PLAN.md §9.3, 2026-05-05 비밀번호 방식 전환).
 *
 * 1인 사용 + 화이트리스트 1개 이메일 모델.
 *
 * 메인 흐름: 이메일 + 비밀번호 (signInWithPassword)
 * 보조 흐름: 비밀번호 분실 시 이메일 reset 링크 (resetPasswordForEmail) — 매직링크 대체
 *
 * - isAllowedUser: 클라이언트 사이드 1차 체크 (PUBLIC_ALLOWED_EMAIL 비교)
 * - signInWithPassword: 이메일/비번 로그인
 * - resetPasswordForEmail: 비번 분실/첫 설정 시 reset 링크 발송
 * - updatePassword: 인증된 세션 내에서 비번 설정/변경 (callback recovery 모드용)
 * - signOut / getCurrentSession: Supabase Auth 래퍼
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

/** 이메일 + 비밀번호 로그인. 메인 흐름. */
export async function signInWithPassword(
  email: string,
  password: string,
): Promise<{ ok: true; email: string } | { ok: false; error: string }> {
  const sb = createBrowserClient();
  if (!sb) return { ok: false, error: 'Supabase 클라이언트 초기화 실패 (환경변수 미설정)' };

  // 화이트리스트 외 이메일은 시도 자체를 차단
  if (!isAllowedUser(email)) {
    return { ok: false, error: '허용되지 않은 이메일입니다.' };
  }

  const { data, error } = await sb.auth.signInWithPassword({ email, password });
  if (error) {
    // Supabase는 "Invalid login credentials"를 영문으로 반환 — 사용자 친화적 메시지로 변환
    if (/invalid login credentials/i.test(error.message)) {
      return { ok: false, error: '이메일 또는 비밀번호가 올바르지 않습니다.' };
    }
    if (/email not confirmed/i.test(error.message)) {
      return { ok: false, error: '이메일 인증이 완료되지 않았습니다. 비밀번호 재설정 링크를 사용해주세요.' };
    }
    return { ok: false, error: error.message };
  }
  if (!data.user?.email) return { ok: false, error: '사용자 정보 누락' };
  return { ok: true, email: data.user.email };
}

/** 비밀번호 재설정 이메일 발송. 첫 비번 설정 + 분실 시 모두 사용. */
export async function resetPasswordForEmail(
  email: string,
  redirectTo: string,
): Promise<{ ok: true } | { ok: false; error: string }> {
  const sb = createBrowserClient();
  if (!sb) return { ok: false, error: 'Supabase 클라이언트 초기화 실패' };

  if (!isAllowedUser(email)) {
    return { ok: false, error: '허용되지 않은 이메일입니다.' };
  }

  const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo });
  if (error) return { ok: false, error: error.message };
  return { ok: true };
}

/** 인증된 세션 내에서 비밀번호 변경. callback recovery 모드 + /auth/setup-password에서 사용. */
export async function updatePassword(
  newPassword: string,
): Promise<{ ok: true } | { ok: false; error: string }> {
  const sb = createBrowserClient();
  if (!sb) return { ok: false, error: 'Supabase 클라이언트 초기화 실패' };

  if (newPassword.length < 8) {
    return { ok: false, error: '비밀번호는 8자 이상이어야 합니다.' };
  }

  const { error } = await sb.auth.updateUser({ password: newPassword });
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
