#!/usr/bin/env node
/**
 * fetch_openinsider.mjs — openinsider.com Form 4 인사이더 매수 시그널 페치
 *
 * 출력: knowledge-base/portfolio/insider_signals.json
 *
 * 페치 페이지:
 *   - /latest-cluster-buys  (3+ 인사이더 동시 매수, 최강 시그널)
 *   - /insider-purchases    (모든 인사이더 매수)
 *
 * 무료, API 없음 → HTML 테이블 파싱.
 *
 * 컬럼: X | FilingDate | TradeDate | Ticker | Company | Industry |
 *       Ins | TradeType | Price | Qty | Owned | ΔOwn | Value | 1d | 1w | 1m | 6m
 */
import { writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { nowKstIsoShort } from './_kst.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const OUTPUT = path.join(PROJECT_ROOT, 'knowledge-base', 'portfolio', 'insider_signals.json');

const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

async function fetchHtml(url, ms = 12000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    const res = await fetch(url, {
      signal: ctrl.signal,
      headers: { 'User-Agent': UA, Accept: 'text/html' },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.text();
  } finally {
    clearTimeout(t);
  }
}

const stripTags = (s) => s.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').trim();
const cleanTicker = (s) => {
  // <a ...>TICKER</a> 또는 ', DELAY, 1)" onmouseout="UnTip()">TICKER 같은 노이즈 제거
  const m = s.match(/>([A-Z][A-Z0-9.\-]{0,9})<\/a>/i) || s.match(/>([A-Z][A-Z0-9.\-]{0,9})$/i);
  if (m) return m[1].toUpperCase();
  const txt = stripTags(s);
  const m2 = txt.match(/[A-Z][A-Z0-9.\-]{0,9}/);
  return m2 ? m2[0].toUpperCase() : '';
};

function parseTable(html) {
  const m = html.match(/<table[^>]*class="tinytable"[\s\S]*?<\/table>/);
  if (!m) return [];
  const table = m[0];
  const rows = table.match(/<tr[\s\S]*?<\/tr>/g) || [];
  const out = [];
  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].match(/<t[hd][\s\S]*?<\/t[hd]>/g);
    if (!cells || cells.length < 13) continue;
    const cellTexts = cells.map(stripTags);
    const ticker = cleanTicker(cells[3]);
    if (!ticker) continue;
    const tradeType = cellTexts[7]; // "P - Purchase" or "S - Sale"
    const isPurchase = /P\s*-\s*Purchase/i.test(tradeType);
    if (!isPurchase) continue; // 매수만
    out.push({
      filing_date: cellTexts[1].split(' ')[0],
      trade_date: cellTexts[2],
      ticker,
      company: cellTexts[4],
      industry: cellTexts[5],
      insider_count: Number(cellTexts[6]) || null,
      trade_type: 'P',
      price: cellTexts[8].replace(/[$,]/g, '') ? Number(cellTexts[8].replace(/[$,]/g, '')) : null,
      qty: cellTexts[9].replace(/[+,]/g, '') ? Number(cellTexts[9].replace(/[+,]/g, '')) : null,
      delta_own_pct: cellTexts[11], // "+23%" 문자열 그대로
      value_usd: cellTexts[12].replace(/[$+,]/g, '') ? Number(cellTexts[12].replace(/[$+,]/g, '')) : null,
      r_1d: cellTexts[13] || null,
      r_1w: cellTexts[14] || null,
      r_1m: cellTexts[15] || null,
    });
  }
  return out;
}

function fmtUsd(n) {
  if (n == null) return '—';
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`;
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`;
  return `$${n}`;
}

async function main() {
  let cluster = [];
  let purchases = [];
  const errors = [];

  try {
    const html = await fetchHtml('http://openinsider.com/latest-cluster-buys');
    cluster = parseTable(html);
    console.log(`OK: cluster-buys ${cluster.length}건`);
  } catch (e) {
    errors.push(`cluster: ${e.message}`);
  }

  try {
    const html = await fetchHtml('http://openinsider.com/insider-purchases');
    purchases = parseTable(html);
    console.log(`OK: insider-purchases ${purchases.length}건`);
  } catch (e) {
    errors.push(`purchases: ${e.message}`);
  }

  // value formatted 추가
  for (const arr of [cluster, purchases]) {
    for (const it of arr) {
      it.value_fmt = fmtUsd(it.value_usd);
    }
  }

  const payload = {
    updated_at: nowKstIsoShort(),
    updated_tz: 'Asia/Seoul',
    cluster_buys: cluster.slice(0, 25),
    purchases: purchases.slice(0, 25),
    errors,
  };

  await mkdir(path.dirname(OUTPUT), { recursive: true });
  await writeFile(OUTPUT, JSON.stringify(payload, null, 2), 'utf-8');

  const rel = path.relative(PROJECT_ROOT, OUTPUT);
  console.log(`OK: 인사이더 시그널 (cluster=${cluster.length}, purchases=${purchases.length}) → ${rel}`);
  if (errors.length) console.error(`  warnings: ${errors.join(' | ')}`);
}

main().catch((err) => {
  console.error('ERR:', err);
  process.exit(0);
});
