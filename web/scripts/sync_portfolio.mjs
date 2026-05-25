#!/usr/bin/env node
/**
 * sync_portfolio.mjs — knowledge-base/portfolio/user_portfolio.md → Supabase 동기화 (Node 포팅).
 *
 * 매 prebuild에서 자동 실행. 환경변수 없으면 silent skip (로컬 빌드 안전).
 * Vercel 빌드 환경에서는 PUBLIC_SUPABASE_URL/SUPABASE_SERVICE_KEY/PUBLIC_ALLOWED_EMAIL 자동 주입.
 *
 * Python sync_portfolio_to_supabase.py 와 동일 로직:
 *   - ★ CURRENT ★ 섹션 추출
 *   - 투자자 프로파일 표 → portfolio.profile (jsonb)
 *   - 보유 종목 표 → holdings (전량 삭제 후 재삽입)
 *   - 포트폴리오 총액 표 → portfolio.total_value_usd/krw, exchange_rate
 *   - idempotent (동일 내용이면 no-op)
 */
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { nowKstIso } from './_kst.mjs';
import {
  extractCurrentSection,
  parseProfile,
  parseHoldings,
  parseTotals,
  parseCashFromTotals,
  validateParsed,
  checkSchemaContract,
} from './lib/portfolio_parser.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '../..');
const PORTFOLIO_MD = path.join(PROJECT_ROOT, 'knowledge-base', 'portfolio', 'user_portfolio.md');

// .env.local 로드 (외부 의존 없이)
function loadEnv(p) {
  if (!existsSync(p)) return;
  const text = require('node:fs').readFileSync(p, 'utf-8');
  for (const raw of text.split(/\r?\n/)) {
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
// require for sync read (Node 20+)
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
loadEnv(path.resolve(__dirname, '..', '.env.local'));

const URL = process.env.PUBLIC_SUPABASE_URL;
const KEY = process.env.SUPABASE_SERVICE_KEY;
const EMAIL = (process.env.ALLOWED_EMAIL || process.env.PUBLIC_ALLOWED_EMAIL || '').toLowerCase().trim();

function info(msg) { console.log(`[sync_portfolio] ${msg}`); }
function warn(msg) { console.warn(`[sync_portfolio] WARN: ${msg}`); }
function err(msg) { console.error(`[sync_portfolio] ERROR: ${msg}`); }

// STRICT 모드: 검증 실패 시 exit 1 (Vercel/CI/prod 빌드 차단)
// LENIENT 모드: 검증 실패 시 warn 만 (로컬 빌드는 깨지지 않게)
const STRICT = String(process.env.SYNC_STRICT ?? '').toLowerCase() === '1'
  || String(process.env.SYNC_STRICT ?? '').toLowerCase() === 'true';

function fail(msg) {
  err(msg);
  if (STRICT) {
    err(`STRICT 모드 — 빌드 중단 (production 데이터 오염 방지)`);
    process.exit(1);
  }
  warn(`LENIENT 모드 — 경고만 출력하고 진행 (로컬 환경)`);
}

// 파서/검증 함수는 ./lib/portfolio_parser.mjs 모듈에서 import (단위 테스트 가능)

// ────────────────────────────────────────────────────────────────────────
// graceful skip 분기
// ────────────────────────────────────────────────────────────────────────
if (!existsSync(PORTFOLIO_MD)) {
  info('user_portfolio.md 없음 — skip');
  process.exit(0);
}
if (!URL || !KEY || !EMAIL) {
  info(`env 미설정 (URL=${URL ? 'OK' : 'MISSING'}, KEY=${KEY ? 'OK' : 'MISSING'}, EMAIL=${EMAIL ? 'OK' : 'MISSING'}) — skip`);
  process.exit(0);
}

// ────────────────────────────────────────────────────────────────────────
// Supabase upsert
// ────────────────────────────────────────────────────────────────────────
async function getUserId(sb, email) {
  const { data, error } = await sb.auth.admin.listUsers();
  if (error) { warn(`listUsers 실패: ${error.message}`); return null; }
  const user = (data?.users ?? []).find((u) => (u.email ?? '').toLowerCase() === email.toLowerCase());
  return user?.id ?? null;
}

async function upsertPortfolio(sb, userId, parsed) {
  const nowIso = nowKstIso();  // KST (Supabase timestamptz는 +09:00 인식)
  const portfolioPayload = {
    user_id: userId,
    profile: parsed.profile,
    total_value_usd: parsed.total_value_usd,
    total_value_krw: parsed.total_value_krw,
    exchange_rate: parsed.exchange_rate,
    updated_at: nowIso,
    source: 'local_md',
  };

  const { data: existing, error: e1 } = await sb
    .from('portfolios')
    .select('id')
    .eq('user_id', userId)
    .order('updated_at', { ascending: false })
    .limit(1);
  if (e1) throw new Error(`portfolios select: ${e1.message}`);

  let portfolioId;
  if (existing && existing.length > 0) {
    portfolioId = existing[0].id;
    const { error } = await sb.from('portfolios').update(portfolioPayload).eq('id', portfolioId);
    if (error) throw new Error(`portfolios update: ${error.message}`);
  } else {
    const { data, error } = await sb.from('portfolios').insert(portfolioPayload).select('id');
    if (error) throw new Error(`portfolios insert: ${error.message}`);
    portfolioId = data[0].id;
  }

  // holdings 전량 삭제 후 재삽입
  const { error: dErr } = await sb.from('holdings').delete().eq('portfolio_id', portfolioId);
  if (dErr) throw new Error(`holdings delete: ${dErr.message}`);

  const rawPayload = parsed.holdings.map((h) => ({ ...h, portfolio_id: portfolioId, updated_at: nowIso }));
  // 같은 ticker 중복 제거 (현금 등 — 마지막 항목 우선)
  const deduped = new Map();
  for (const h of rawPayload) deduped.set(h.ticker, h);
  const holdingsPayload = [...deduped.values()];
  if (holdingsPayload.length > 0) {
    const { error } = await sb.from('holdings').insert(holdingsPayload);
    if (error) throw new Error(`holdings insert: ${error.message}`);
  }
  return { portfolioId, n: holdingsPayload.length };
}

// ────────────────────────────────────────────────────────────────────────
// 메인
// ────────────────────────────────────────────────────────────────────────
const md = await readFile(PORTFOLIO_MD, 'utf-8');

// schema contract: frontmatter holdings_table_columns vs 실제 표 헤더 비교 (P1-4)
const schemaErr = checkSchemaContract(md);
if (schemaErr) {
  fail(`schema contract 위반: ${schemaErr}`);
  if (!STRICT) process.exit(0);
} else {
  info(`schema contract 검증 통과 (frontmatter ↔ 표 헤더 일치)`);
}

let parsed;
try {
  const current = extractCurrentSection(md);
  const lines = current.split(/\r?\n/);
  const stockHoldings = parseHoldings(lines);
  const cashHoldings = parseCashFromTotals(lines); // 자동: 포트폴리오 총액 표 → CASH rows
  parsed = {
    profile: parseProfile(lines),
    holdings: [...stockHoldings, ...cashHoldings],
    ...parseTotals(lines),
  };
  info(`파싱 완료 (보유 종목 ${stockHoldings.length} + 현금 ${cashHoldings.length} = ${parsed.holdings.length}건)`);
} catch (e) {
  fail(`파싱 실패: ${e.message}`);
  if (!STRICT) process.exit(0);
}

// 사전 검증 게이트 (parsed 데이터 무결성)
const failures = validateParsed(parsed);
if (failures.length > 0) {
  err(`사전 검증 실패 ${failures.length}건:`);
  for (const f of failures) err(`  - ${f}`);
  fail(`parsed 데이터 무결성 검증 실패 — supabase 갱신 차단`);
  if (!STRICT) process.exit(0);
}
info(`사전 검증 통과 (holdings=${parsed.holdings.length}, total=$${parsed.total_value_usd})`);

let createClient;
try {
  ({ createClient } = await import('@supabase/supabase-js'));
} catch {
  warn('@supabase/supabase-js 미설치 — skip');
  process.exit(0);
}

const sb = createClient(URL, KEY, { auth: { persistSession: false, autoRefreshToken: false } });
try {
  const userId = await getUserId(sb, EMAIL);
  if (!userId) {
    fail(`Supabase에 사용자 ${EMAIL} 미등록`);
    if (!STRICT) process.exit(0);
  }
  const { portfolioId, n } = await upsertPortfolio(sb, userId, parsed);
  info(`upsert OK (id=${portfolioId.slice(0, 8)}…, ${n} holdings, total=$${parsed.total_value_usd ?? '?'})`);

  // 사후 검증: read-back 으로 supabase 실제 데이터 검사
  const { data: rb, error: rbErr } = await sb
    .from('holdings')
    .select('ticker, weight_pct, return_pct, asset_type')
    .eq('portfolio_id', portfolioId);
  if (rbErr) {
    fail(`read-back 실패: ${rbErr.message}`);
    if (!STRICT) process.exit(0);
  }
  const rbNonCash = (rb ?? []).filter((h) => h.asset_type !== 'CASH');
  const rbWOk = rbNonCash.filter((h) => h.weight_pct != null && h.weight_pct > 0).length;
  const rbWRate = rbNonCash.length > 0 ? rbWOk / rbNonCash.length : 0;
  if (rbNonCash.length === 0 || rbWRate < 0.8) {
    fail(`read-back 검증 실패: holdings ${rbNonCash.length}건, weight_pct 추출률 ${(rbWRate * 100).toFixed(0)}% — supabase 데이터 무결성 깨짐`);
    if (!STRICT) process.exit(0);
  }
  info(`read-back 검증 통과 (${rbNonCash.length} holdings, weight_pct ${(rbWRate * 100).toFixed(0)}% 커버)`);
  info(`OK: portfolio synced (id=${portfolioId.slice(0, 8)}…, ${n} holdings, total=$${parsed.total_value_usd ?? '?'})`);
} catch (e) {
  fail(`Supabase 호출 실패: ${e.message}`);
  if (!STRICT) process.exit(0);
}
