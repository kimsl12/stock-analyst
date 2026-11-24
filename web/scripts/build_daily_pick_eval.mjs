#!/usr/bin/env node
/**
 * build_daily_pick_eval.mjs — 데일리픽 성적표 집계 CLI
 *
 * 입력: 원장 + 가격 캐시(analysis/_daily_pick/prices.json) + 논지 판정(thesis·overrides)
 * 출력: web/src/data/daily_pick_eval.json
 *
 * 사용: node scripts/build_daily_pick_eval.mjs [--judgments-extra <file>] [--queue [--ticker T]] [--prune-invalid]
 */
import { readFile, writeFile, rename } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildEval, buildRecommendations } from './lib/daily_pick_eval.mjs';
import { locateAnalysisFile } from './lib/analysis_archive.mjs';

const WEB_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PROJECT_ROOT = path.resolve(WEB_DIR, '..');
const DATA = path.join(WEB_DIR, 'src', 'data');
const LEDGER = path.join(DATA, 'daily_pick_ledger.json');
const THESIS = path.join(DATA, 'daily_pick_thesis.json');
const OVERRIDES = path.join(DATA, 'daily_pick_thesis_overrides.json');
const EVAL = path.join(DATA, 'daily_pick_eval.json');
const PRICES = path.join(PROJECT_ROOT, 'analysis', '_daily_pick', 'prices.json');

const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const opt = (n) => (args.includes(n) ? args[args.indexOf(n) + 1] : null);

// 파일이 없으면 fallback
async function readJson(file, fallback) {
  try {
    return JSON.parse(await readFile(file, 'utf8'));
  } catch (e) {
    if (e.code === 'ENOENT') return fallback;
    throw e;
  }
}

// 원자적 쓰기 (tmp + rename)
async function writeAtomic(file, obj) {
  const tmp = `${file}.tmp`;
  await writeFile(tmp, JSON.stringify(obj, null, 2) + '\n', 'utf8');
  await rename(tmp, file);
}

const ledger = await readJson(LEDGER, []);
const thesis = await readJson(THESIS, []);
const overrides = await readJson(OVERRIDES, {});
const extraFile = opt('--judgments-extra');
const extra = extraFile ? await readJson(path.resolve(extraFile), []) : [];
const judgments = [...thesis, ...extra];

const prices = await readJson(PRICES, null);
if (!prices?.symbols) {
  console.error(`가격 캐시 없음: ${PRICES} — 기존 eval 유지`);
  process.exit(1);
}
const symbols = prices.symbols;

if (flag('--queue')) {
  const { pending } = buildRecommendations(ledger, symbols, judgments, overrides);
  const only = opt('--ticker');
  const items = [];
  for (const p of pending.filter((x) => !only || x.ticker === only)) {
    items.push({
      ...p,
      anchor_source: await locateAnalysisFile(PROJECT_ROOT, p.anchor_analysis_dir, 'scorecard.md'),
      target_source: await locateAnalysisFile(PROJECT_ROOT, p.analysis_dir, 'scorecard.md'),
    });
  }
  console.log(JSON.stringify(items, null, 2));
} else if (flag('--prune-invalid')) {
  const { invalid } = buildRecommendations(ledger, symbols, judgments, overrides);
  const sig = (j) => `${j.ticker}@${j.date}|${j.anchor_date}|${j.verdict}`;
  const bad = new Set(invalid.map(sig));
  const kept = thesis.filter((j) => !bad.has(sig(j)));
  const removed = thesis.length - kept.length;
  if (removed > 0) await writeAtomic(THESIS, kept);
  console.log(`invalid 판정 ${removed}건 제거`);
} else {
  const ev = buildEval({ ledger, symbols, judgments, overrides, now: new Date() });
  await writeAtomic(EVAL, ev);
  console.log(JSON.stringify(ev.counts));
}
