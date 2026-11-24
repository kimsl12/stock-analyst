// backfill_daily_pick_ledger.mjs — git 이력의 daily_pick.json 으로 원장 소급 (--dry-run 지원)
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { normalizeGrade, ledgerRowFromPick, upsertLedgerRow } from './lib/daily_pick_ledger.mjs';
import { readAnalysisFile } from './lib/analysis_archive.mjs';
import { parseGrade, parseTargetPrice } from './lib/scorecard_parser.mjs';

const execFileP = promisify(execFile);
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const LEDGER = path.join(ROOT, 'web/src/data/daily_pick_ledger.json');
const PICK_PATH = 'web/src/data/daily_pick.json';
const REGIME_PATH = 'knowledge-base/market/regime.json';
const DRY = process.argv.includes('--dry-run');

const git = async (...args) =>
  (await execFileP('git', args, { cwd: ROOT, maxBuffer: 256 * 1024 * 1024 })).stdout;

async function history(file) {
  const log = (await git('log', '--format=%H %cI', '--', file)).trim().split('\n').filter(Boolean);
  const out = [];
  for (const line of log) {
    const [sha, at] = line.split(' ');
    try {
      out.push({ at, json: JSON.parse(await git('show', `${sha}:${file}`)) });
    } catch {} // 삭제·파싱 불가 커밋은 건너뜀
  }
  try {
    out.push({ at: '9999', json: JSON.parse(await readFile(path.join(ROOT, file), 'utf8')) }); // 작업트리
  } catch {}
  return out;
}

const marketOf = (t) => (/^\d{6}$/.test(String(t)) ? 'KRX' : 'US');
const num = (v) => {
  if (typeof v === 'number') return Number.isFinite(v) ? v : null;
  const m = String(v ?? '').replace(/,/g, '').match(/\d+(?:\.\d+)?/);
  return m ? Number(m[0]) : null;
};

// 1) pick_date 별 커밋 시각 최신 payload
const picks = new Map();
for (const { at, json } of await history(PICK_PATH)) {
  if (!json?.pick || !json.pick_date) continue;
  const cur = picks.get(json.pick_date);
  if (!cur || at >= cur.at) picks.set(json.pick_date, { at, json });
}

// 2) regime 스냅샷 (date 기준 정렬)
const regimes = (await history(REGIME_PATH))
  .filter((r) => r.json?.date)
  .sort((a, b) => (a.json.date === b.json.date ? (a.at < b.at ? -1 : 1) : a.json.date < b.json.date ? -1 : 1));
const regimeFor = (d) => {
  let hit = null;
  for (const r of regimes) if (r.json.date <= d) hit = r.json;
  return hit;
};

// 3) timeline
const histDir = path.join(ROOT, 'analysis/_history');
const timelines = {};
for (const f of await readdir(histDir)) {
  if (!f.endsWith('_timeline.json')) continue;
  try {
    const j = JSON.parse(await readFile(path.join(histDir, f), 'utf8'));
    timelines[String(j.ticker)] = j.history ?? [];
  } catch {}
}
const nfc = (s) => String(s ?? '').normalize('NFC');

let ledger = [];
try {
  ledger = JSON.parse(await readFile(LEDGER, 'utf8'));
} catch (e) {
  if (e.code !== 'ENOENT') throw e;
}

const stats = { gradeNull: [], tpNull: 0, regimeNull: 0, noDir: [], verFix: 0, scorecardGrade: 0, scTp: 0, tlTp: 0, guard: 0 };
for (const date of [...picks.keys()].sort()) {
  const { json: payload } = picks.get(date);
  const p = payload.pick;
  const row = ledgerRowFromPick(payload, regimeFor(date));
  row.market = p.market ?? marketOf(p.ticker);
  row.reasons = p.reasons ?? [];
  const tl = timelines[String(p.ticker)] ?? [];
  // analysis_dir 없으면 version 과 일치하는 timeline folder 가 유일할 때만 유도
  if (!row.analysis_dir) {
    const vn = Number(String(p.version ?? '').replace(/\D/g, ''));
    const c = tl.filter((h) => h.v === vn);
    if (c.length === 1) row.analysis_dir = c[0].folder;
    else stats.noDir.push(date);
  }
  const vm = row.analysis_dir?.match(/_v(\d+)$/);
  if (vm) {
    if (row.version !== `v${vm[1]}`) stats.verFix++;
    row.version = `v${vm[1]}`;
  }
  if (!row.regime) stats.regimeNull++;

  let md = null;
  const sc = async () => (md ??= row.analysis_dir ? ((await readAnalysisFile(ROOT, row.analysis_dir, 'scorecard.md')) ?? '') : '');
  if (!row.grade) {
    const g = normalizeGrade(parseGrade(await sc()) ?? '');
    if (g) { row.grade = g; stats.scorecardGrade++; }
  }
  if (!row.grade) stats.gradeNull.push(`${date} ${row.ticker} raw=${JSON.stringify(p.grade)} dir=${row.analysis_dir}`);

  if (row.tp_price == null) {
    let tp = num(parseTargetPrice(await sc()));
    if (tp != null) stats.scTp++;
    else {
      const h = tl.find((x) => nfc(x.folder) === nfc(row.analysis_dir));
      tp = num(h?.target_price);
      if (tp != null) stats.tlTp++;
    }
    const ref = p.current_price ?? p.buy_price;
    if (tp != null && ref && (tp < ref * 0.2 || tp > ref * 1.8)) { tp = null; stats.guard++; }
    row.tp_price = tp;
  }
  if (row.tp_price == null) stats.tpNull++;
  ledger = upsertLedgerRow(ledger, row);
}

if (!DRY) await writeFile(LEDGER, JSON.stringify(ledger, null, 2) + '\n');
console.log(`원장 행: ${ledger.length} (첫 날짜 ${ledger[0]?.date}, 끝 ${ledger.at(-1)?.date}) 고유 티커 ${new Set(ledger.map((r) => r.ticker)).size}`);
console.log(`grade null: ${stats.gradeNull.length} (scorecard 보강 ${stats.scorecardGrade})`);
console.log(`tp null: ${stats.tpNull}/${ledger.length} (${((stats.tpNull / ledger.length) * 100).toFixed(1)}%) [scorecard ${stats.scTp}, timeline ${stats.tlTp}, ±80% 가드 null ${stats.guard}]`);
console.log(`regime null: ${stats.regimeNull}, version 재기록: ${stats.verFix}, analysis_dir 미확정: ${stats.noDir.length}`);
for (const l of stats.gradeNull) console.log('  GRADE NULL', l);
for (const d of stats.noDir) console.log('  NO DIR', d);
if (DRY) console.log('(dry-run — 파일 미기록)');
