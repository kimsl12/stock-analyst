#!/usr/bin/env node
/**
 * build_manifest.mjs — reports/ 디렉토리 스캔 → web/src/data/manifest.json + web/public/reports/ 복사
 *
 * PLAN.md §8.3, §10.3 기반.
 * Node 포팅 (원래 Python). 이유:
 *   - Vercel 빌드 컨테이너에 Python venv 부담 회피 (zero-config)
 *   - Node가 Astro 빌드의 1급 시민
 *   - Python 시작 오버헤드 제거 (로컬 빌드도 더 빠름)
 *
 * 실행: node scripts/build_manifest.mjs (또는 npm run prebuild/predev hook 자동)
 */
import { readdir, readFile, stat, mkdir, writeFile, rm, cp } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// ---------------------------------------------------------------------------
// 경로
// ---------------------------------------------------------------------------
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WEB_DIR = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(WEB_DIR, '..');
const REPORTS_DIR = path.join(PROJECT_ROOT, 'reports');
const OUTPUT_JSON = path.join(WEB_DIR, 'src', 'data', 'manifest.json');
const PUBLIC_REPORTS = path.join(WEB_DIR, 'public', 'reports');

// ---------------------------------------------------------------------------
// 분류 규칙
// ---------------------------------------------------------------------------
const KR_ETF_PREFIXES = new Set([
  'KODEX', 'TIGER', 'ACE', 'RISE', 'SOL', 'HANARO',
  'ARIRANG', 'PLUS', 'KOSEF', 'KIWOOM', 'KBSTAR', 'FOCUS',
]);

const BRIEFING_TYPE = {
  morning: 'morning',
  evening: 'evening',
  weekly: 'weekly',
  crypto: 'crypto',
  user_portfolio: 'user_portfolio',
  global_intelligence: 'global_intelligence',
  model_portfolio: 'model_portfolio',
  rebalancing_user: 'rebalancing',
  rebalancing: 'rebalancing',
  daily_briefing: 'daily_briefing', // legacy
};

// ---------------------------------------------------------------------------
// 파일명 파서
// ---------------------------------------------------------------------------
const RE_BRIEFING = /^([a-z_]+)_(\d{8})\.html$/;
const RE_STOCK = /^([0-9A-Z][0-9A-Za-z]*)_(.+)_(\d{8})\.html$/;
const RE_TITLE = /<title[^>]*>([\s\S]*?)<\/title>/i;

const fmtDate = (s) => `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`;

function parseBriefing(filename) {
  const m = RE_BRIEFING.exec(filename);
  if (!m) return null;
  const [, rawType, dateStr] = m;
  const btype = BRIEFING_TYPE[rawType];
  if (!btype) return null;
  return { type: btype, ticker: null, name: null, date: fmtDate(dateStr) };
}

function parseStock(filename) {
  const m = RE_STOCK.exec(filename);
  if (!m) return null;
  const [, ticker, name, dateStr] = m;
  const isEtf = KR_ETF_PREFIXES.has(ticker.toUpperCase());
  return {
    type: isEtf ? 'etf' : 'stock_analysis',
    ticker,
    name,
    date: fmtDate(dateStr),
  };
}

// ---------------------------------------------------------------------------
// HTML title 추출 (첫 8KB만)
// ---------------------------------------------------------------------------
async function extractTitle(filepath) {
  try {
    const text = await readFile(filepath, { encoding: 'utf-8' });
    const chunk = text.slice(0, 8192);
    const m = RE_TITLE.exec(chunk);
    if (!m) return null;
    const cleaned = m[1].replace(/\s+/g, ' ').trim();
    return cleaned || null;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// 디렉토리 1단계 .html 목록
// ---------------------------------------------------------------------------
async function listHtml(dir) {
  if (!existsSync(dir)) return [];
  const entries = await readdir(dir, { withFileTypes: true });
  return entries
    .filter((e) => e.isFile() && e.name.endsWith('.html'))
    .map((e) => e.name)
    .sort();
}

// ---------------------------------------------------------------------------
// reports/ → web/public/reports/ 복사 (제외 패턴 적용)
// ---------------------------------------------------------------------------
async function copyReports() {
  if (!existsSync(REPORTS_DIR)) return 0;
  if (existsSync(PUBLIC_REPORTS)) {
    await rm(PUBLIC_REPORTS, { recursive: true });
  }
  await mkdir(path.dirname(PUBLIC_REPORTS), { recursive: true });
  await cp(REPORTS_DIR, PUBLIC_REPORTS, {
    recursive: true,
    filter: (src) => {
      const name = path.basename(src);
      if (name === '.DS_Store' || name === '.gitkeep') return false;
      if (name.startsWith('._')) return false;
      if (name.endsWith('.md')) return false;
      if (name.endsWith('.json')) return false;
      return true;
    },
  });

  // 복사된 .html 카운트
  let count = 0;
  async function walk(dir) {
    const ents = await readdir(dir, { withFileTypes: true });
    for (const e of ents) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) await walk(p);
      else if (e.name.endsWith('.html')) count++;
    }
  }
  await walk(PUBLIC_REPORTS);
  return count;
}

// ---------------------------------------------------------------------------
// 메인
// ---------------------------------------------------------------------------
async function main() {
  if (!existsSync(REPORTS_DIR)) {
    console.error(`WARN: reports/ 미발견: ${REPORTS_DIR}`);
    process.exit(0);
  }

  const items = [];
  const warnings = [];

  // 1. reports/briefing/*.html
  const briefingDir = path.join(REPORTS_DIR, 'briefing');
  for (const fn of await listHtml(briefingDir)) {
    const meta = parseBriefing(fn);
    if (!meta) {
      warnings.push(`미인식 briefing 파일명: ${fn}`);
      continue;
    }
    const filepath = path.join(briefingDir, fn);
    const st = await stat(filepath);
    items.push({
      ...meta,
      filename: fn,
      url_path: `/reports/briefing/${fn}`,
      size_bytes: st.size,
      title: await extractTitle(filepath),
    });
  }

  // 2. reports/*.html (루트 = 종목분석/ETF)
  for (const fn of await listHtml(REPORTS_DIR)) {
    const meta = parseStock(fn);
    if (!meta) {
      warnings.push(`미인식 stock 파일명: ${fn}`);
      continue;
    }
    const filepath = path.join(REPORTS_DIR, fn);
    const st = await stat(filepath);
    items.push({
      ...meta,
      filename: fn,
      url_path: `/reports/${fn}`,
      size_bytes: st.size,
      title: await extractTitle(filepath),
    });
  }

  // 정렬: date desc → filename desc
  items.sort((a, b) => {
    if (a.date !== b.date) return b.date.localeCompare(a.date);
    return b.filename.localeCompare(a.filename);
  });

  // 복사
  const copied = await copyReports();

  // by_type 집계
  const byType = {};
  for (const it of items) byType[it.type] = (byType[it.type] || 0) + 1;

  await mkdir(path.dirname(OUTPUT_JSON), { recursive: true });
  await writeFile(
    OUTPUT_JSON,
    JSON.stringify(
      {
        generated_at: new Date().toISOString().slice(0, 19),
        count: items.length,
        by_type: byType,
        items,
      },
      null,
      2,
    ),
    'utf-8',
  );

  const rel = path.relative(PROJECT_ROOT, OUTPUT_JSON);
  console.log(`OK: manifest 생성 (${items.length} items, ${copied} HTMLs copied) → ${rel}`);
  if (warnings.length) {
    console.error(`  (${warnings.length} warnings)`);
    for (const w of warnings.slice(0, 10)) console.error(`  WARN: ${w}`);
    if (warnings.length > 10) console.error(`  ... (${warnings.length - 10} more)`);
  }
}

main().catch((err) => {
  console.error('ERR:', err);
  process.exit(1);
});
