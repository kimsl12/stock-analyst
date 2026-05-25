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
import { execSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { nowKstIsoShort } from './_kst.mjs';

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

// [v3.17 — 2026-05-12] research/ L3 분기 Deep Dive 섹터 한국어 라벨
// [v3.18 — 2026-05-12] P1 #6 — 5섹터 추가 (defense·tech_platform·consumer·industrials·auto)
const RESEARCH_SECTOR_LABELS = {
  semiconductor: '반도체',
  energy: '에너지',
  macro: '매크로',
  biotech: '바이오',
  fintech: '핀테크',
  defense: '방산',
  tech_platform: '기술/플랫폼',
  consumer: '소비재',
  industrials: '산업재',
  auto: '자동차',
};

// ---------------------------------------------------------------------------
// 파일명 파서
// ---------------------------------------------------------------------------
const RE_BRIEFING = /^([a-z_]+)_(\d{8})\.html$/;
const RE_STOCK = /^([0-9A-Z][0-9A-Za-z]*)_(.+)_(\d{8})\.html$/;
// [v3.17] research/{sector}_{YYYY}Q{N}.html (분기 단위 Deep Dive)
const RE_RESEARCH = /^([a-z]+)_(\d{4})Q([1-4])\.html$/;
const RE_TITLE = /<title[^>]*>([\s\S]*?)<\/title>/i;

const fmtDate = (s) => `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`;

// ---------------------------------------------------------------------------
// sort_key (commit time 기반, 시간순 정렬용)  [v3.16 — 2026-05-10]
// ---------------------------------------------------------------------------
// reports/ 하위 모든 파일의 가장 최근 commit unix time 을 일괄 추출.
// shallow clone (Vercel 기본) 에서 history 부족 시 빈 Map 반환 → fallback chain 작동.
export function getCommitTimes(repoRoot = PROJECT_ROOT) {
  const map = new Map();
  let raw = '';
  try {
    raw = execSync(
      `git log --name-only --pretty=format:'__C__|%ct' --diff-filter=AM -- 'reports/*.html' 'reports/briefing/*.html' 'reports/research/*.html' 'reports/analyst/items/*'`,
      {
        cwd: repoRoot,
        encoding: 'utf-8',
        maxBuffer: 50 * 1024 * 1024,
        stdio: ['ignore', 'pipe', 'pipe'],
      },
    );
  } catch (e) {
    console.error(`WARN: git log 실패 — fallback 사용 (${e.message.split('\n')[0]})`);
    return map;
  }
  let currentTs = null;
  for (const line of raw.split('\n')) {
    const t = line.trim();
    if (!t) continue;
    if (t.startsWith('__C__|')) {
      currentTs = Number(t.slice(6));
      if (!Number.isFinite(currentTs)) currentTs = null;
    } else if (currentTs && t.startsWith('reports/')) {
      // git log 는 최신 → 과거 순 출력. 첫 번째만 저장 = 가장 최근 commit time.
      if (!map.has(t)) map.set(t, currentTs);
    }
  }
  return map;
}

// reports/research/*.html 첫 commit time (= 발행일) 추출 [v3.21 — 2026-05-13]
// parseResearch 의 date 필드용. getCommitTimes 와 달리 --diff-filter=A (Added) + 최초 등장만.
// Q1=01-01 같은 분기 시작일 매핑 폐기 → 실제 발행 시점 사용 (다른 type 과 일관).
export function getResearchFirstCommitTimes(repoRoot = PROJECT_ROOT) {
  const map = new Map();
  let raw = '';
  try {
    raw = execSync(
      `git log --diff-filter=A --name-only --pretty=format:'__C__|%ct' -- 'reports/research/*.html'`,
      {
        cwd: repoRoot,
        encoding: 'utf-8',
        maxBuffer: 5 * 1024 * 1024,
        stdio: ['ignore', 'pipe', 'pipe'],
      },
    );
  } catch (e) {
    console.error(`WARN: research first-commit git log 실패 — 분기 시작일 fallback (${e.message.split('\n')[0]})`);
    return map;
  }
  let currentTs = null;
  for (const line of raw.split('\n')) {
    const t = line.trim();
    if (!t) continue;
    if (t.startsWith('__C__|')) {
      currentTs = Number(t.slice(6));
      if (!Number.isFinite(currentTs)) currentTs = null;
    } else if (currentTs && t.startsWith('reports/research/')) {
      // diff-filter=A 라 파일당 add commit 만. 단 git log 가 최신순이므로
      // 같은 파일의 add 가 여러 번 있으면 첫 등장만 저장 (= 가장 최근 추가).
      // 정상 케이스에선 파일당 add 1회.
      if (!map.has(t)) map.set(t, currentTs);
    }
  }
  return map;
}

// 파일경로 → unix sort_key. fallback chain:
//   1. git commit time (최신)
//   2. filename YYYYMMDD + 12:00 UTC
//   3. 0 (가장 아래)
export function deriveSortKey(relPath, gitTimes) {
  const ts = gitTimes.get(relPath);
  if (ts) return ts;
  const m = /(\d{8})/.exec(path.basename(relPath));
  if (m) {
    const y = m[1].slice(0, 4);
    const mo = m[1].slice(4, 6);
    const d = m[1].slice(6, 8);
    const epoch = Math.floor(new Date(`${y}-${mo}-${d}T12:00:00Z`).getTime() / 1000);
    if (Number.isFinite(epoch)) return epoch;
  }
  return 0;
}

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

// [v3.17 → v3.21, 2026-05-13] research L3 분기 Deep Dive 파일명 파서
// 예: semiconductor_2026Q3.html → sector=semiconductor, year=2026, quarter=3
// date 는 git first commit time (= 발행일) 우선, 부재 시 분기 시작월 1일 fallback.
// 다른 type (stock/briefing/analyst) 과 일관되게 "발행일" 의미로 통일.
function parseResearch(filename, researchFirstTimes) {
  const m = RE_RESEARCH.exec(filename);
  if (!m) return null;
  const [, sector, year, q] = m;
  if (!RESEARCH_SECTOR_LABELS[sector]) return null; // 등록된 10섹터 외 거부

  // 1순위: git first commit time (실제 발행일)
  const relPath = `reports/research/${filename}`;
  const ts = researchFirstTimes?.get(relPath);
  let dateStr;
  if (ts) {
    const dt = new Date(ts * 1000);
    dateStr = `${dt.getUTCFullYear()}-${String(dt.getUTCMonth() + 1).padStart(2, '0')}-${String(dt.getUTCDate()).padStart(2, '0')}`;
  } else {
    // fallback: 분기 시작월 1일 (Vercel 빌드 컨테이너 등 .git 부재 환경)
    const month = String(((Number(q) - 1) * 3) + 1).padStart(2, '0');
    dateStr = `${year}-${month}-01`;
  }

  return {
    type: 'research',
    ticker: RESEARCH_SECTOR_LABELS[sector], // 한국어 섹터명 (UI ticker 슬롯)
    name: `${year} Q${q} Deep Dive`,
    date: dateStr,
    sector,
    quarter: `${year}Q${q}`,
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
      if (name === '_archive') return false; // [v3.14] reports/_archive/ 미러링 제외
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

  // [v3.16] 모든 reports/ 파일의 git commit time 일괄 추출
  const gitTimes = getCommitTimes(PROJECT_ROOT);
  // [v3.21] research L3 first-commit time (= 발행일) 일괄 추출
  const researchFirstTimes = getResearchFirstCommitTimes(PROJECT_ROOT);
  let gitHits = 0;
  let gitMisses = 0;

  // [v3.16 — Vercel 우회] git log 사용 불가 + commit된 manifest 존재 시 그대로 사용.
  //   Vercel 빌드 컨테이너는 source-only 로 .git 미포함 → git log 항상 실패.
  //   이 경우 fallback (filename YYYYMMDD + 12:00 UTC) 만으로 정렬하면 같은 날 모두 동률 →
  //   기존 type rank 정렬과 동일하게 떨어져 시간순 의미가 사라짐.
  //   대신 로컬에서 commit한 manifest 를 그대로 쓰고, reports/ 복사만 수행.
  if (gitTimes.size === 0 && existsSync(OUTPUT_JSON)) {
    const copied = await copyReports();
    console.log(`OK: git log 사용 불가 (Vercel 등) — committed manifest 그대로 사용, ${copied} HTMLs copied`);
    return;
  }

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
    const relPath = `reports/briefing/${fn}`;
    const sortKey = deriveSortKey(relPath, gitTimes);
    if (gitTimes.has(relPath)) gitHits++; else gitMisses++;
    items.push({
      ...meta,
      filename: fn,
      url_path: `/reports/briefing/${fn}`,
      size_bytes: st.size,
      title: await extractTitle(filepath),
      sort_key: sortKey,
    });
  }

  // 1.5. reports/research/*.html (L3 분기 Deep Dive) [v3.17 — 2026-05-12, v3.21 발행일 매핑]
  const researchDir = path.join(REPORTS_DIR, 'research');
  for (const fn of await listHtml(researchDir)) {
    const meta = parseResearch(fn, researchFirstTimes);
    if (!meta) {
      warnings.push(`미인식 research 파일명: ${fn}`);
      continue;
    }
    const filepath = path.join(researchDir, fn);
    const st = await stat(filepath);
    const relPath = `reports/research/${fn}`;
    const sortKey = deriveSortKey(relPath, gitTimes);
    if (gitTimes.has(relPath)) gitHits++; else gitMisses++;
    items.push({
      ...meta,
      filename: fn,
      url_path: `/reports/research/${fn}`,
      size_bytes: st.size,
      title: await extractTitle(filepath),
      sort_key: sortKey,
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
    const relPath = `reports/${fn}`;
    const sortKey = deriveSortKey(relPath, gitTimes);
    if (gitTimes.has(relPath)) gitHits++; else gitMisses++;
    items.push({
      ...meta,
      filename: fn,
      url_path: `/reports/${fn}`,
      size_bytes: st.size,
      title: await extractTitle(filepath),
      sort_key: sortKey,
    });
  }

  // 3. reports/analyst/items/{id}/meta.json (애널리스트 리포트)
  const ANALYST_DIR = path.join(REPORTS_DIR, 'analyst', 'items');
  if (existsSync(ANALYST_DIR)) {
    const subdirs = (await readdir(ANALYST_DIR, { withFileTypes: true }))
      .filter((e) => e.isDirectory());
    for (const sub of subdirs) {
      const metaPath = path.join(ANALYST_DIR, sub.name, 'meta.json');
      const summaryPath = path.join(ANALYST_DIR, sub.name, 'summary.html');
      if (!existsSync(metaPath)) continue;
      try {
        const meta = JSON.parse(await readFile(metaPath, 'utf-8'));
        const st = existsSync(summaryPath) ? await stat(summaryPath) : { size: 0 };
        // analyst 는 summary.html 의 commit time 우선, 없으면 meta.json
        const summaryRel = `reports/analyst/items/${sub.name}/summary.html`;
        const metaRel = `reports/analyst/items/${sub.name}/meta.json`;
        const candidatePath = gitTimes.has(summaryRel) ? summaryRel : metaRel;
        const sortKey = deriveSortKey(candidatePath, gitTimes) ||
          // fallback to meta.date YYYY-MM-DD + 12:00 UTC
          (meta.date ? Math.floor(new Date(`${meta.date}T12:00:00Z`).getTime() / 1000) : 0);
        if (gitTimes.has(summaryRel) || gitTimes.has(metaRel)) gitHits++; else gitMisses++;
        items.push({
          type: 'analyst',
          ticker: meta.source || null, // MS / GS / CNBC / LS 등 (UI 의 ticker 슬롯에 source 표시)
          name: meta.target_name || meta.target || null,
          date: meta.date,
          filename: 'summary.html',
          url_path: `/reports/analyst/items/${sub.name}/summary.html`,
          size_bytes: st.size,
          title: meta.title,
          sort_key: sortKey,
          // analyst 전용 메타 (Astro 페이지에서 사용)
          source: meta.source_full || meta.source,
          source_type: meta.source_type,
          analyst_name: meta.analyst,
          rating: meta.rating,
          target_price: meta.target_price,
          target_currency: meta.target_currency,
          period: meta.period,
          target_kind: meta.target_kind,
          summary_bullets: meta.summary_bullets,
          outcome: meta.outcome ?? null,
        });
      } catch (e) {
        warnings.push(`analyst meta 파싱 실패: ${sub.name} (${e.message})`);
      }
    }
  }

  // 정렬 [v3.16 — 2026-05-10]: sort_key (commit time) DESC → type rank DESC → filename ASC
  //
  // 이전 (v3.7): date DESC → type rank DESC → filename DESC
  //   문제: 종목분석/etf/analyst 는 type rank 미등록 → 항상 브리핑 묶음 다음에 처박힘.
  //         예) 5/9 새벽 모닝브리핑이 5/9 낮 종목분석보다 위에 표시됨 (시간역행).
  //
  // 변경 (v3.16): commit time 기반 시간순 섞기. 브리핑/종목 type 무관 만든 시각 DESC.
  //   - sort_key = git commit unix time (없으면 filename YYYYMMDD 자정)
  //   - 같은 sort_key (= 같은 commit, 묶음분석): type rank DESC (evening > morning) 로 안정화
  //   - 그래도 동일하면 filename ASC (티커 알파벳)
  // [v3.25] 브리핑 sort_key 보정: 파일명 날짜 + 타입별 고정 시각 (KST)
  // 소급 생성 파일의 commit time이 실제 날짜와 다른 문제 해결.
  // 브리핑은 항상 "해당 날짜의 발행 시각"으로 정렬해야 자연스러움.
  const TYPE_HOUR_KST = {
    morning: 9,             // KST 09:00
    weekly: 12,             // KST 12:00
    model_portfolio: 14,    // KST 14:00
    rebalancing: 15,        // KST 15:00
    user_portfolio: 16,     // KST 16:00
    performance_review: 17, // KST 17:00
    global_intelligence: 18,// KST 18:00
    crypto: 19,             // KST 19:00
    evening: 20,            // KST 20:00
    daily_briefing: 8,      // legacy
  };
  for (const item of items) {
    const dateMatch = /(\d{8})/.exec(item.filename);
    const hourKST = TYPE_HOUR_KST[item.type];
    if (dateMatch && hourKST != null) {
      const ds = dateMatch[1];
      const y = ds.slice(0,4), mo = ds.slice(4,6), d = ds.slice(6,8);
      const utcHour = hourKST - 9;
      const epoch = Math.floor(new Date(`${y}-${mo}-${d}T${String(utcHour).padStart(2,'0')}:00:00Z`).getTime() / 1000);
      if (Number.isFinite(epoch)) item.sort_key = epoch;
    }
  }

  items.sort((a, b) => {
    const sa = a.sort_key ?? 0;
    const sb = b.sort_key ?? 0;
    if (sa !== sb) return sb - sa;                    // 1차: 날짜+시각 DESC
    return a.filename.localeCompare(b.filename);      // 2차: filename ASC
  });

  // [v3.14] 같은 (type, ticker, name) stock_analysis/etf 는 최신 1개만 manifest 등재
  // reports/_archive/ 가 cp filter 에서 제외되긴 하지만, archive 안 한 중복 reports 가 있을 때 안전망.
  // briefing/analyst 는 영향 없음 (ticker 가 type 이거나 source 라 식별자 다름)
  const DEDUPE_TYPES = new Set(['stock_analysis', 'etf']);
  const seenStock = new Set();
  const dedupedItems = [];
  for (const it of items) {
    if (!DEDUPE_TYPES.has(it.type)) {
      dedupedItems.push(it);
      continue;
    }
    const key = `${it.type}|${it.ticker}|${it.name}`;
    if (seenStock.has(key)) continue; // 이미 더 최신이 등재됨 (정렬 desc)
    seenStock.add(key);
    dedupedItems.push(it);
  }
  const dropped = items.length - dedupedItems.length;
  items.length = 0;
  items.push(...dedupedItems);

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
        generated_at: nowKstIsoShort(),  // KST
        generated_tz: 'Asia/Seoul',
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
  console.log(`OK: manifest 생성 (${items.length} items${dropped > 0 ? `, dedupe -${dropped}` : ''}, ${copied} HTMLs copied) → ${rel}`);
  console.log(`  sort_key: git ${gitHits} hits / ${gitMisses} fallback (filename YYYYMMDD)`);
  if (warnings.length) {
    console.error(`  (${warnings.length} warnings)`);
    for (const w of warnings.slice(0, 10)) console.error(`  WARN: ${w}`);
    if (warnings.length > 10) console.error(`  ... (${warnings.length - 10} more)`);
  }
}

// CLI 실행 가드 (단위 테스트에서 import 시 main() 자동 실행 방지)
// 한글 경로/공백 등 URL encoding 차이로 직접 비교가 실패할 수 있어 fileURLToPath 로 정규화.
if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  main().catch((err) => {
    console.error('ERR:', err);
    process.exit(1);
  });
}
