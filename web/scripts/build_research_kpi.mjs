#!/usr/bin/env node
/**
 * build_research_kpi.mjs — Research KB v3.19 활용 KPI 산출
 *
 * 출력: web/src/data/research_kpi.json
 *
 * 데이터 소스:
 *  - knowledge-base/research/_index.md (L1 헤드라인)
 *  - knowledge-base/research/{sector}/_meta.md (섹터 frontmatter)
 *  - knowledge-base/research/{sector}/*.md (L2 카운트)
 *  - reports/research/{sector}_YYYYQN.html (L3 발행)
 *  - analysis/{stock_dir}/{scorecard,momentum,business,risk,company,financial}.md (인용 활용)
 *
 * 산출 KPI:
 *  - sectors[]: 10섹터 × {l1_count, l2_count, l3_count, status, last_updated, usage_count}
 *  - totals: L1/L2/L3 합계 + active/scaffolded 섹터 수
 *  - usage: 인용 적용 종목 수 + 최근 활용 사례 + 평균 인용 수
 *  - kpi_status: early|active|stable (자동 결정)
 */
import { readFile, writeFile, readdir, mkdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { nowKstIsoShort } from './_kst.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WEB_DIR = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(WEB_DIR, '..');
const RESEARCH_DIR = path.join(PROJECT_ROOT, 'knowledge-base', 'research');
const REPORTS_RESEARCH = path.join(PROJECT_ROOT, 'reports', 'research');
const ANALYSIS_DIR = path.join(PROJECT_ROOT, 'analysis');
const OUTPUT_JSON = path.join(WEB_DIR, 'src', 'data', 'research_kpi.json');

const SECTOR_DEFS = [
  { id: 'semiconductor', label: '반도체', emoji: '🧠', priority: 1 },
  { id: 'energy',        label: '에너지', emoji: '⚡', priority: 2 },
  { id: 'macro',         label: '매크로', emoji: '📊', priority: 3 },
  { id: 'biotech',       label: '바이오', emoji: '🧬', priority: 4 },
  { id: 'fintech',       label: '핀테크', emoji: '💳', priority: 5 },
  { id: 'defense',       label: '방산',     emoji: '🛡️', priority: 6 },
  { id: 'tech_platform', label: '기술/플랫폼', emoji: '💻', priority: 7 },
  { id: 'consumer',      label: '소비재', emoji: '🛒', priority: 8 },
  { id: 'industrials',   label: '산업재', emoji: '🏗️', priority: 9 },
  { id: 'auto',          label: '자동차', emoji: '🚗', priority: 10 },
];

// frontmatter 단순 파서 (key: value 한 줄짜리만)
function parseFrontmatter(text) {
  const m = text.match(/^---\s*\n([\s\S]*?)\n---/);
  if (!m) return {};
  const out = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^([a-z0-9_]+):\s*(.+)$/);
    if (kv) out[kv[1]] = kv[2].trim();
  }
  return out;
}

// ---------------------------------------------------------------------------
// 1. 섹터별 L1/L2/L3 카운트 + meta
// ---------------------------------------------------------------------------
async function buildSectorStats() {
  const sectors = [];
  for (const def of SECTOR_DEFS) {
    const sectorDir = path.join(RESEARCH_DIR, def.id);
    let status = 'missing';
    let last_updated = null;
    let l1_count = 0;
    let l2_count = 0;
    let l3_count = 0;
    let l3_latest_quarter = null;
    let thesis_summary = null;

    const metaFile = path.join(sectorDir, '_meta.md');
    if (existsSync(metaFile)) {
      const text = await readFile(metaFile, 'utf-8');
      const fm = parseFrontmatter(text);
      status = fm.status || 'unknown';
      last_updated = fm.last_updated || null;
      l1_count = Number(fm.l1_index_count) || 0;
      l2_count = Number(fm.l2_summary_count) || 0;
      l3_count = Number(fm.l3_deep_dive_count) || 0;

      // thesis 첫 bullet 만 (요약용)
      const thesisMatch = text.match(/##\s*현재 thesis[\s\S]*?\n\n- \*\*([^*]+)\*\*:\s*([^\n]+)/);
      if (thesisMatch) {
        thesis_summary = `${thesisMatch[1].trim()}: ${thesisMatch[2].trim().slice(0, 120)}`;
      }
    }

    // 실제 L2 파일 카운트 (_meta.md 제외) — frontmatter 값과 비교 검증
    if (existsSync(sectorDir)) {
      const files = await readdir(sectorDir);
      const actualL2 = files.filter((f) => f.endsWith('.md') && f !== '_meta.md').length;
      if (actualL2 !== l2_count) l2_count = actualL2; // 실측 우선
    }

    // L3 카운트 + 최신 분기
    if (existsSync(REPORTS_RESEARCH)) {
      const allReports = await readdir(REPORTS_RESEARCH);
      const sectorReports = allReports
        .filter((f) => new RegExp(`^${def.id}_\\d{4}Q[1-4]\\.html$`).test(f))
        .sort()
        .reverse();
      l3_count = sectorReports.length;
      if (sectorReports.length > 0) {
        const qm = sectorReports[0].match(/_(\d{4})Q([1-4])\.html$/);
        if (qm) l3_latest_quarter = `${qm[1]}Q${qm[2]}`;
      }
    }

    sectors.push({
      id: def.id,
      label: def.label,
      emoji: def.emoji,
      priority: def.priority,
      status,
      last_updated,
      l1_count,
      l2_count,
      l3_count,
      l3_latest_quarter,
      thesis_summary,
      usage_count: 0, // 후속 단계에서 채움
    });
  }
  return sectors;
}

// ---------------------------------------------------------------------------
// 2. analysis/ 디렉토리 스캔 → 인용 활용 통계
//   .md 파일 본문에서 `📄 [` 패턴 카운트 + 종목별 매핑
// ---------------------------------------------------------------------------
async function buildUsageStats(sectors) {
  if (!existsSync(ANALYSIS_DIR)) {
    return {
      stocks_with_citations: 0,
      total_citations: 0,
      avg_citations_per_stock: 0,
      recent_cases: [],
      sector_usage: {},
    };
  }

  const sectorById = new Map(sectors.map((s) => [s.id, s]));
  const entries = await readdir(ANALYSIS_DIR, { withFileTypes: true });
  const stockDirs = entries.filter((e) => e.isDirectory()).map((e) => e.name);

  const sectorUsage = Object.fromEntries(sectors.map((s) => [s.id, 0]));
  const cases = []; // { ticker, name, version, analyzed_at, citations_count, citations, sector }
  const reCitation = /📄\s*\[([A-Za-z\s/]+)\]\s*([^\n]+)/g;

  // 인용 → 섹터 매핑 휴리스틱
  function inferSectorFromCitation(citation) {
    const lc = citation.toLowerCase();
    if (/hbm|isscc|chip|nvidia|sk hynix|samsung|tsmc|memory|gpu|asml/i.test(lc)) return 'semiconductor';
    if (/oil|wti|smr|nuclear|doe|iea|nuclear regulatory|kepco|trisox|trsiox|small modular/i.test(lc)) return 'energy';
    if (/fomc|fed|cpi|inflation|boj|ecb|bls|bea/i.test(lc)) return 'macro';
    if (/nejm|jama|attain|fda|ema|cms|gilead|lilly|nvo/i.test(lc)) return 'biotech';
    if (/stablecoin|sec\b|cfpb|coinbase|bis papers|crypto|fintech|payments/i.test(lc)) return 'fintech';
    if (/lockheed|defense|raytheon|northrop|kaspersky|sipri|matsushita defense|hanwha aero/i.test(lc)) return 'defense';
    if (/meta|google|amazon|microsoft|aapl|naver|kakao|alibaba|saas/i.test(lc)) return 'tech_platform';
    if (/costco|walmart|coca|nike|lvmh|consumer|retail/i.test(lc)) return 'consumer';
    if (/caterpillar|cat\b|deere|honeywell|industrial|construction|infra/i.test(lc)) return 'industrials';
    if (/tesla|tsla|ford|gm|hyundai|kia|ev battery|toyota/i.test(lc)) return 'auto';
    return null;
  }

  for (const dir of stockDirs) {
    const stockDir = path.join(ANALYSIS_DIR, dir);
    let stockStat;
    try {
      stockStat = await stat(stockDir);
    } catch { continue; }
    if (!stockStat.isDirectory()) continue;

    const mdFiles = ['scorecard.md', 'momentum.md', 'business.md', 'risk.md', 'company.md', 'financial.md'];
    const citationSet = new Set();
    let latestMtime = 0;

    for (const fn of mdFiles) {
      const file = path.join(stockDir, fn);
      if (!existsSync(file)) continue;
      try {
        const text = await readFile(file, 'utf-8');
        const fStat = await stat(file);
        if (fStat.mtimeMs > latestMtime) latestMtime = fStat.mtimeMs;
        const matches = text.matchAll(reCitation);
        for (const m of matches) {
          const norm = `[${m[1].trim()}] ${m[2].trim().slice(0, 100)}`;
          citationSet.add(norm);
        }
      } catch { /* skip */ }
    }

    if (citationSet.size === 0) continue;

    // 디렉토리명 → ticker / name / version 파싱
    // 예: "000660_SK하이닉스_v3" / "COIN_Coinbase_v3"
    const dirMatch = dir.match(/^([^_]+)_([^_]+?)(?:_v(\d+))?$/);
    const ticker = dirMatch?.[1] ?? dir;
    const name = dirMatch?.[2] ?? '';
    const version = dirMatch?.[3] ? `v${dirMatch[3]}` : '';

    // 섹터 추정: 인용 내용으로 가장 빈도 높은 섹터
    const sectorCounts = {};
    for (const c of citationSet) {
      const s = inferSectorFromCitation(c);
      if (s) sectorCounts[s] = (sectorCounts[s] || 0) + 1;
    }
    let topSector = null;
    let maxCount = 0;
    for (const [s, c] of Object.entries(sectorCounts)) {
      if (c > maxCount) { maxCount = c; topSector = s; }
    }
    if (topSector) sectorUsage[topSector] = (sectorUsage[topSector] || 0) + citationSet.size;

    const analyzedAt = new Date(latestMtime).toISOString().slice(0, 10);

    cases.push({
      dir,
      ticker,
      name,
      version,
      sector: topSector,
      sector_label: topSector ? (sectorById.get(topSector)?.label ?? topSector) : '미분류',
      analyzed_at: analyzedAt,
      mtime_ms: latestMtime,
      citations_count: citationSet.size,
      citations: [...citationSet].slice(0, 8), // 최대 8건 표시
    });
  }

  // 최근순 정렬
  cases.sort((a, b) => b.mtime_ms - a.mtime_ms);
  const recent_cases = cases.slice(0, 10).map(({ mtime_ms, ...rest }) => rest);

  const total_citations = cases.reduce((s, c) => s + c.citations_count, 0);
  const stocks_with_citations = cases.length;
  const avg = stocks_with_citations > 0 ? Math.round((total_citations / stocks_with_citations) * 10) / 10 : 0;

  // sectorUsage → sectors[].usage_count 반영
  for (const s of sectors) {
    s.usage_count = sectorUsage[s.id] || 0;
  }

  return {
    stocks_with_citations,
    total_citations,
    avg_citations_per_stock: avg,
    recent_cases,
    sector_usage: sectorUsage,
  };
}

// ---------------------------------------------------------------------------
// 3. KPI status 자동 결정
// ---------------------------------------------------------------------------
function decideKpiStatus(sectors, usage) {
  const activeSectors = sectors.filter((s) => s.status === 'active').length;
  if (usage.stocks_with_citations >= 20 && activeSectors >= 8) return 'stable';
  if (usage.stocks_with_citations >= 5 && activeSectors >= 5) return 'active';
  return 'early';
}

// ---------------------------------------------------------------------------
// 메인
// ---------------------------------------------------------------------------
async function main() {
  const sectors = await buildSectorStats();
  const usage = await buildUsageStats(sectors);

  const totals = {
    l1_total: sectors.reduce((s, x) => s + x.l1_count, 0),
    l2_total: sectors.reduce((s, x) => s + x.l2_count, 0),
    l3_total: sectors.reduce((s, x) => s + x.l3_count, 0),
    active_sectors: sectors.filter((s) => s.status === 'active').length,
    scaffolded_sectors: sectors.filter((s) => s.status === 'scaffolded').length,
  };

  const kpi_status = decideKpiStatus(sectors, usage);

  await mkdir(path.dirname(OUTPUT_JSON), { recursive: true });
  await writeFile(
    OUTPUT_JSON,
    JSON.stringify(
      {
        generated_at: nowKstIsoShort(),
        generated_tz: 'Asia/Seoul',
        kpi_status,
        sectors,
        totals,
        usage,
      },
      null,
      2,
    ),
    'utf-8',
  );

  const rel = path.relative(PROJECT_ROOT, OUTPUT_JSON);
  console.log(
    `OK: research_kpi 생성 (sectors=${sectors.length}, L1=${totals.l1_total}, L2=${totals.l2_total}, L3=${totals.l3_total}, stocks_used=${usage.stocks_with_citations}, citations=${usage.total_citations}, status=${kpi_status}) → ${rel}`,
  );
}

main().catch((err) => {
  console.error('ERR:', err);
  process.exit(1);
});
