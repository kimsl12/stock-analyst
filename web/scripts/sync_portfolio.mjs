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
// 마크다운 파서 유틸
// ────────────────────────────────────────────────────────────────────────
const RE_TABLE = /^\s*\|.+\|\s*$/;
const RE_SEP = /^\s*\|[\s\-:|]+\|\s*$/;

function splitRow(line) {
  return line.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
}

function findTableAfter(lines, headingRe) {
  for (let i = 0; i < lines.length; i++) {
    if (!headingRe.test(lines[i])) continue;
    for (let j = i + 1; j < Math.min(i + 30, lines.length); j++) {
      if (RE_TABLE.test(lines[j]) && RE_SEP.test(lines[j + 1] ?? '')) {
        const header = splitRow(lines[j]);
        const rows = [];
        for (let k = j + 2; k < lines.length; k++) {
          if (!RE_TABLE.test(lines[k]) || RE_SEP.test(lines[k])) break;
          rows.push(splitRow(lines[k]));
        }
        return { header, rows };
      }
    }
  }
  return null;
}

function stripBold(s) { return (s ?? '').replace(/\*\*/g, '').trim(); }
function cleanMoney(s) {
  const t = stripBold(s);
  if (!t || t === '—' || t === '-') return null;
  const v = t.replace(/[$,원\s]/g, '');
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}
function cleanQty(s) {
  const t = stripBold(s);
  if (!t || t === '—' || t === '-') return null;
  const v = t.replace(/[주,\s]/g, '');
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}
function cleanPct(s) {
  const t = stripBold(s);
  if (!t || t === '—' || t === '-') return null;
  // 첫 % 직전의 숫자(부호 포함) 추출 — "+10.7% (+$1,337.21)" 같은 부수정보 무시
  const m = t.match(/(-?\+?-?\d+(?:\.\d+)?)\s*%/);
  if (m) {
    const n = Number(m[1].replace(/^\+/, ''));
    return Number.isFinite(n) ? n : null;
  }
  const v = t.replace(/[%+\s,]/g, '');
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

// ────────────────────────────────────────────────────────────────────────
// user_portfolio.md 파싱
// ────────────────────────────────────────────────────────────────────────
function extractCurrentSection(md) {
  const m = md.match(/##\s*★\s*CURRENT\s*★\s*$([\s\S]*?)(?=^---\s*$|^##\s+\S)/m);
  if (!m) throw new Error('★ CURRENT ★ 섹션을 찾을 수 없음');
  return m[1];
}

function parseProfile(lines) {
  const t = findTableAfter(lines, /^###\s+투자자\s*프로파일/);
  if (!t) throw new Error('투자자 프로파일 표 미발견');
  const profile = {};
  for (const row of t.rows) {
    if (row.length < 2) continue;
    const k = row[0].trim();
    const v = stripBold(row[1]);
    if (k) profile[k] = v;
  }
  return profile;
}

function parseHoldings(lines) {
  const t = findTableAfter(lines, /^###\s+보유\s*종목/);
  if (!t) throw new Error('보유 종목 표 미발견');
  const out = [];
  // 헤더 컬럼 수 확인 (8컬럼 legacy: 티커|종목명|유형|시장|수량|평가금|비중|수익률,
  //                    9컬럼 v3.16+: 티커|종목명|유형|시장|수량|현재가|평가금|비중|수익률)
  const ncol = t.header.length;
  for (const row of t.rows) {
    if (row.length < 8) continue;
    let ticker, name, assetType, market, qty, priceUsd, valueUsd, weight, ret;
    if (ncol >= 9) {
      [ticker, name, assetType, market, qty, priceUsd, valueUsd, weight, ret] = row;
    } else {
      [ticker, name, assetType, market, qty, valueUsd, weight, ret] = row;
      priceUsd = null;
    }
    if (!ticker || ticker.startsWith('---')) continue;
    const isCash = /현금/.test(assetType) || /현금/.test(ticker);
    const normType = isCash ? 'CASH' : (assetType && assetType !== '—' ? assetType.toUpperCase() : null);
    const normMarket = market && market !== '—' ? market : null;
    const qVal = cleanQty(qty) ?? (isCash ? 0 : null);
    const vVal = cleanMoney(valueUsd);
    const wVal = cleanPct(weight);
    const rVal = cleanPct(ret);
    if (qVal == null) continue;
    const pVal = cleanMoney(priceUsd);
    const currentPrice = pVal != null ? pVal : (qVal > 0 && vVal != null ? vVal / qVal : null);
    out.push({
      ticker,
      name: name || ticker,
      asset_type: normType,
      market: normMarket,
      quantity: qVal,
      avg_buy_price: null,
      current_price: currentPrice,
      current_value_usd: vVal,
      weight_pct: wVal,
      return_pct: rVal,
    });
  }
  return out;
}

function parseTotals(lines) {
  const t = findTableAfter(lines, /^###\s+포트폴리오\s*총액/);
  let totalUsd = null;
  if (t) {
    for (const row of t.rows) {
      if (row.length < 2) continue;
      const label = stripBold(row[0]);
      if (/총액/.test(label)) {
        totalUsd = cleanMoney(row[1]);
        break;
      }
    }
  }
  let fx = null;
  for (const line of lines) {
    if (/환율/.test(line) && /원/.test(line)) {
      const m = line.match(/([\d,]+\.\d+)\s*원/);
      if (m) { fx = cleanMoney(m[1]); break; }
    }
  }
  const totalKrw = totalUsd && fx ? totalUsd * fx : null;
  return { total_value_usd: totalUsd, exchange_rate: fx, total_value_krw: totalKrw };
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

  const holdingsPayload = parsed.holdings.map((h) => ({ ...h, portfolio_id: portfolioId, updated_at: nowIso }));
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
let parsed;
try {
  const current = extractCurrentSection(md);
  const lines = current.split(/\r?\n/);
  parsed = {
    profile: parseProfile(lines),
    holdings: parseHoldings(lines),
    ...parseTotals(lines),
  };
} catch (e) {
  warn(`파싱 실패: ${e.message}`);
  process.exit(0); // graceful (빌드 깨지 않음)
}

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
  if (!userId) { warn(`Supabase에 사용자 ${EMAIL} 미등록 — skip`); process.exit(0); }
  const { portfolioId, n } = await upsertPortfolio(sb, userId, parsed);
  info(`OK: portfolio synced (id=${portfolioId.slice(0, 8)}…, ${n} holdings, total=$${parsed.total_value_usd ?? '?'})`);
} catch (e) {
  warn(`Supabase 호출 실패: ${e.message}`);
  process.exit(0); // graceful — 빌드는 계속
}
