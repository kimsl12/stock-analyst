#!/usr/bin/env node
/**
 * health_check.mjs — sync_portfolio 직후 supabase 데이터 무결성 최종 검증.
 *
 * prebuild 흐름의 마지막 단계 (Astro build 직전).
 * - portfolios 최신 row 의 updated_at, total_value_usd, source 점검
 * - holdings 의 weight_pct/return_pct 추출률 점검
 * - 결과를 web/src/data/health.json 으로 저장 → SSG 페이지에서 배지 표시 가능
 *
 * STRICT 모드 (Vercel/CI): 검증 실패 시 exit 1 → astro build 차단
 * LENIENT 모드 (로컬): warn 만 출력하고 health.json 에 status='unhealthy' 기록
 *
 * 환경변수 미설정 시 graceful skip (status='unknown').
 */
import { writeFile } from 'node:fs/promises';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WEB_DIR = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(WEB_DIR, '..');
const HEALTH_PATH = path.join(WEB_DIR, 'src', 'data', 'health.json');

function loadEnv(p) {
  if (!existsSync(p)) return;
  for (const raw of readFileSync(p, 'utf-8').split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const eq = line.indexOf('=');
    if (eq < 1) continue;
    const k = line.slice(0, eq).trim();
    let v = line.slice(eq + 1).trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
    if (process.env[k] === undefined) process.env[k] = v;
  }
}
loadEnv(path.resolve(WEB_DIR, '.env.local'));

const URL = process.env.PUBLIC_SUPABASE_URL;
const KEY = process.env.SUPABASE_SERVICE_KEY;
const STRICT = String(process.env.HEALTH_STRICT ?? '').toLowerCase() === '1'
  || String(process.env.HEALTH_STRICT ?? '').toLowerCase() === 'true';

const log = (msg) => console.log(`[health_check] ${msg}`);
const warn = (msg) => console.warn(`[health_check] WARN: ${msg}`);
const err = (msg) => console.error(`[health_check] ERROR: ${msg}`);

async function writeHealth(payload) {
  await writeFile(HEALTH_PATH, JSON.stringify(payload, null, 2) + '\n', 'utf-8');
  log(`health.json 기록: status=${payload.status}`);
}

const nowIso = new Date().toISOString();

if (!URL || !KEY) {
  log('env 미설정 — graceful skip (status=unknown)');
  await writeHealth({ status: 'unknown', reason: 'env 미설정', checked_at: nowIso, checks: [] });
  process.exit(0);
}

let createClient;
try {
  ({ createClient } = await import('@supabase/supabase-js'));
} catch {
  log('@supabase/supabase-js 미설치 — graceful skip');
  await writeHealth({ status: 'unknown', reason: '@supabase/supabase-js 미설치', checked_at: nowIso, checks: [] });
  process.exit(0);
}

const sb = createClient(URL, KEY, { auth: { persistSession: false, autoRefreshToken: false } });
const checks = [];
let failures = 0;

function check(name, ok, detail) {
  checks.push({ name, ok, detail });
  if (ok) log(`✓ ${name} — ${detail}`);
  else { warn(`✗ ${name} — ${detail}`); failures++; }
}

// ────────────────────────────────────────────────────────────────────────
// C1. portfolios 최신 row
// ────────────────────────────────────────────────────────────────────────
const { data: pData, error: pErr } = await sb
  .from('portfolios')
  .select('id, updated_at, total_value_usd, source')
  .order('updated_at', { ascending: false })
  .limit(1);

if (pErr || !pData || pData.length === 0) {
  check('portfolios 존재', false, pErr?.message ?? 'row 0건');
  await writeHealth({ status: 'unhealthy', reason: 'portfolios 없음', checked_at: nowIso, checks });
  if (STRICT) { err('STRICT — 빌드 중단'); process.exit(1); }
  process.exit(0);
}
const p = pData[0];
check('portfolios 존재', true, `id=${p.id.slice(0, 8)}…, source=${p.source}`);

// C2. updated_at 최신성 (24시간 이내)
const ageHours = (Date.now() - new Date(p.updated_at).getTime()) / 3600000;
check(
  'portfolios updated_at 최신성 (24시간 이내)',
  ageHours < 24,
  `${ageHours.toFixed(1)}시간 전`,
);

// C3. total_value_usd
check(
  'portfolios.total_value_usd > 0',
  (p.total_value_usd ?? 0) > 0,
  `$${p.total_value_usd ?? 0}`,
);

// ────────────────────────────────────────────────────────────────────────
// C4~C6. holdings
// ────────────────────────────────────────────────────────────────────────
const { data: hData, error: hErr } = await sb
  .from('holdings')
  .select('ticker, weight_pct, return_pct, current_price, asset_type')
  .eq('portfolio_id', p.id);

if (hErr) {
  check('holdings 조회', false, hErr.message);
  await writeHealth({ status: 'unhealthy', reason: 'holdings 조회 실패', checked_at: nowIso, checks });
  if (STRICT) { err('STRICT — 빌드 중단'); process.exit(1); }
  process.exit(0);
}

const nonCash = (hData ?? []).filter((h) => h.asset_type !== 'CASH');
check('holdings 존재 (현금 외)', nonCash.length > 0, `${nonCash.length}건`);

if (nonCash.length > 0) {
  const wOk = nonCash.filter((h) => h.weight_pct != null && h.weight_pct > 0).length;
  const wRate = wOk / nonCash.length;
  check(
    'holdings weight_pct 추출률 ≥ 80%',
    wRate >= 0.8,
    `${(wRate * 100).toFixed(0)}% (${wOk}/${nonCash.length})`,
  );

  const rOk = nonCash.filter((h) => h.return_pct != null).length;
  const rRate = rOk / nonCash.length;
  check(
    'holdings return_pct 추출률 ≥ 50%',
    rRate >= 0.5,
    `${(rRate * 100).toFixed(0)}% (${rOk}/${nonCash.length})`,
  );

  const wTotal = nonCash.reduce((s, h) => s + (h.weight_pct ?? 0), 0);
  check(
    'holdings 비중 합계 50~105% (현금 외)',
    wTotal >= 50 && wTotal <= 105,
    `${wTotal.toFixed(1)}%`,
  );
}

// ────────────────────────────────────────────────────────────────────────
// 결과 + health.json 기록
// ────────────────────────────────────────────────────────────────────────
const status = failures === 0 ? 'healthy' : 'unhealthy';
await writeHealth({
  status,
  reason: failures === 0 ? null : `${failures}건 검증 실패`,
  checked_at: nowIso,
  portfolio_id: p.id,
  portfolio_updated_at: p.updated_at,
  total_value_usd: p.total_value_usd,
  holdings_count: nonCash.length,
  checks,
});

if (failures > 0) {
  err(`${failures}건 검증 실패 — production 데이터 무결성 깨짐 가능`);
  if (STRICT) { err('STRICT — 빌드 중단'); process.exit(1); }
  warn('LENIENT — 빌드는 계속하지만 health.json 에 unhealthy 기록');
} else {
  log(`✅ 모든 검증 통과 (${checks.length}건)`);
}
