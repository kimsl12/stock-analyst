#!/usr/bin/env node
/**
 * set_password.mjs — Supabase Admin API로 화이트리스트 사용자의 비밀번호 직접 설정.
 *
 * 사용법:
 *   cd web
 *   node scripts/set_password.mjs '<새 비밀번호 8자 이상>'
 *
 * 환경:
 *   PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_KEY, PUBLIC_ALLOWED_EMAIL
 *   web/.env.local 또는 셸 export 모두 인식.
 *
 * 동작:
 *   1) 화이트리스트 이메일로 admin.listUsers() → 사용자 검색
 *   2) 없으면 admin.createUser() (email_confirm: true)
 *   3) 있으면 admin.updateUserById() (password 갱신)
 *
 * 매직링크/reset 흐름 모두 폐기 후 첫 비번 설정 + 변경 모두 본 스크립트로 일원화.
 */
import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// .env.local 자동 로드 (외부 의존 없이)
function loadEnv(p) {
  if (!existsSync(p)) return;
  const text = readFileSync(p, 'utf-8');
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const eq = line.indexOf('=');
    if (eq < 1) continue;
    const k = line.slice(0, eq).trim();
    let v = line.slice(eq + 1).trim();
    // strip surrounding quotes
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1);
    }
    if (process.env[k] === undefined) process.env[k] = v;
  }
}

loadEnv(path.resolve(__dirname, '..', '.env.local'));
loadEnv(path.resolve(__dirname, '..', '.env'));

const SUPABASE_URL = process.env.PUBLIC_SUPABASE_URL;
const SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;
const ALLOWED_EMAIL = (process.env.PUBLIC_ALLOWED_EMAIL ?? '').toLowerCase().trim();
// argv[2] 우선, 없으면 BUILD_NEW_PASSWORD env (Vercel build-env로 주입)
const newPassword = process.argv[2] || process.env.BUILD_NEW_PASSWORD;

function fail(msg, code = 1) {
  console.error(`✗ ${msg}`);
  process.exit(code);
}

// 비번 미지정 → silent skip (일반 빌드에서는 호출만 되고 작업 안 함)
if (!newPassword) {
  console.log('[set_password] BUILD_NEW_PASSWORD 미설정 — skip');
  process.exit(0);
}

if (!SUPABASE_URL || !SERVICE_KEY || !ALLOWED_EMAIL) {
  fail(
    '환경변수 누락\n' +
      '  필요: PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_KEY, PUBLIC_ALLOWED_EMAIL\n' +
      '  → web/.env.local 작성 또는 셸 export 후 재실행',
  );
}
if (newPassword.length < 8) {
  fail('비밀번호는 8자 이상이어야 합니다.');
}

// 동적 import (의존성: web/node_modules/@supabase/supabase-js — 이미 설치됨)
const { createClient } = await import('@supabase/supabase-js');

const sb = createClient(SUPABASE_URL, SERVICE_KEY, {
  auth: { persistSession: false, autoRefreshToken: false },
});

console.log(`▶ Supabase: ${SUPABASE_URL}`);
console.log(`▶ 대상 이메일: ${ALLOWED_EMAIL}`);

// 1. 사용자 조회
const { data: list, error: lerr } = await sb.auth.admin.listUsers();
if (lerr) fail(`listUsers 실패: ${lerr.message}`);
const user = list.users.find((u) => (u.email ?? '').toLowerCase() === ALLOWED_EMAIL);

let userId;
if (user) {
  userId = user.id;
  console.log(`▶ 기존 사용자 발견 (id=${userId})`);
} else {
  console.log('▶ 사용자 없음 — 신규 생성');
  const { data: created, error: cerr } = await sb.auth.admin.createUser({
    email: ALLOWED_EMAIL,
    password: newPassword,
    email_confirm: true,
  });
  if (cerr) fail(`createUser 실패: ${cerr.message}`);
  userId = created.user.id;
  console.log(`▶ 신규 사용자 생성 완료 (id=${userId})`);
}

// 2. 비번 + email_confirm 강제 갱신 (이미 있어도 안전)
const { error: uerr } = await sb.auth.admin.updateUserById(userId, {
  password: newPassword,
  email_confirm: true,
});
if (uerr) fail(`updateUserById 실패: ${uerr.message}`);

console.log('');
console.log(`✓ ${ALLOWED_EMAIL} 비밀번호 설정 완료.`);
console.log('  → https://stock-analyst-jungwon1.vercel.app/login 에서 새 비번으로 로그인하세요.');
