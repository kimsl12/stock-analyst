#!/usr/bin/env node
/**
 * cleanup_reanalysis.mjs — 종목 재분석 누적 정리 도구
 *
 * 정책 (2026-05-08, 사용자 승인 옵션 B + 압축 + 최신 1개):
 *   1. 종목별 v 폴더의 scorecard.md 메타를 추출하여 timeline.json 누적
 *   2. 직전 v{N-1}, v{N} 만 active 유지, 그 이전은 .tar.gz 압축 → analysis/_archive/
 *   3. reports/*.html 도 종목당 1개(최신 날짜)만 active, 나머지 .html.gz → reports/_archive/
 *   4. anomaly(이름 충돌, 고아 HTML)는 보고만, 자동 처리 ❌
 *
 * 모드:
 *   --dry-run (기본): 영향 받을 항목 표만 출력, 파일 변경 ❌
 *   --apply: 실제 timeline 생성 + archive 이동/압축
 *   --tickers AVGO,NVDA: 특정 티커만 (기본 = 전체)
 *
 * 호출:
 *   cd 프로젝트루트 && node web/scripts/cleanup_reanalysis.mjs --dry-run
 *   cd 프로젝트루트 && node web/scripts/cleanup_reanalysis.mjs --apply
 *   cd 프로젝트루트 && node web/scripts/cleanup_reanalysis.mjs --apply --tickers AVGO,NVDA,LLY
 *
 * /재분석실행 Phase 3 자동 통합용:
 *   해당 회차 종목만 한정해서 --apply --tickers ... 호출.
 */
import { readdir, readFile, stat, mkdir, writeFile, rename, rm } from 'node:fs/promises';
import { existsSync, statSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { todayKst, nowKstIsoShort } from './_kst.mjs';
// [v3.39] 점수·등급·목표가 추출은 공유 파서 우선 (웹·시그널과 동일 SSOT) — 자체 정규식은 폴백만.
// 자체 등급 정규식이 반증 조건 "등급 {중립→매수}" 의 '→ 매수' 를 결론으로 오캡처한 사고 (2026-07-03, LIN·SPGI·LNG 등 6종).
import { parseScore, parseGrade, parseTargetPrice, parseAnalysisDate } from './lib/scorecard_parser.mjs';

// ---------------------------------------------------------------------------
// 경로
// ---------------------------------------------------------------------------
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const ANALYSIS_DIR = path.join(PROJECT_ROOT, 'analysis');
const REPORTS_DIR = path.join(PROJECT_ROOT, 'reports');
const HISTORY_DIR = path.join(ANALYSIS_DIR, '_history');
const ANALYSIS_ARCHIVE = path.join(ANALYSIS_DIR, '_archive');
const REPORTS_ARCHIVE = path.join(REPORTS_DIR, '_archive');

// ---------------------------------------------------------------------------
// 인자 파싱
// ---------------------------------------------------------------------------
function parseArgs(argv) {
  const out = { apply: false, tickers: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--apply') out.apply = true;
    else if (a === '--dry-run') out.apply = false;
    else if (a === '--tickers') out.tickers = (argv[++i] || '').split(',').map((s) => s.trim()).filter(Boolean);
  }
  return out;
}

// ---------------------------------------------------------------------------
// 폴더/파일명 파싱 (단계별 — regex 한 줄 lazy/greedy 충돌 방지)
// ---------------------------------------------------------------------------
const RE_TICKER_NAME = /^([A-Z]+|\d{6})_(.+)$/;
const RE_TRAILING_V = /^(.+?)_v(\d+)$/;

/**
 * 분석 폴더명 파싱: "010120_LSELECTRIC_v1" → {ticker:"010120", name:"LSELECTRIC", v:1}
 *                "SPY_SPDR_SP500"      → {ticker:"SPY",    name:"SPDR_SP500",     v:null}
 */
function parseAnalysisFolderName(folderName) {
  const vM = RE_TRAILING_V.exec(folderName);
  const baseName = vM ? vM[1] : folderName;
  const v = vM ? Number(vM[2]) : null;
  const tnM = RE_TICKER_NAME.exec(baseName);
  if (!tnM) return null;
  return { ticker: tnM[1], name: tnM[2], v };
}

/**
 * HTML 파일명 파싱: "010120_LSELECTRIC_20260508.html"     → {ticker, name, v:null, date}
 *                 "LLY_EliLilly_v2_20260423.html"       → {ticker, name, v:2,    date}  (옛 표기)
 */
function parseHtmlFilename(filename) {
  if (!filename.endsWith('.html')) return null;
  // 1. 끝의 _YYYYMMDD.html 추출
  const dateM = /^(.+)_(\d{8})\.html$/.exec(filename);
  if (!dateM) return null;
  const stemAndV = dateM[1];
  const date = dateM[2];
  // 2. 끝의 _vN 추출 (옛 표기 호환)
  const vM = RE_TRAILING_V.exec(stemAndV);
  const stem = vM ? vM[1] : stemAndV;
  const v = vM ? Number(vM[2]) : null;
  // 3. ticker_name 분리
  const tnM = RE_TICKER_NAME.exec(stem);
  if (!tnM) return null;
  return { ticker: tnM[1], name: tnM[2], v, date };
}

async function scanAnalysisFolders() {
  if (!existsSync(ANALYSIS_DIR)) return new Map();
  const entries = await readdir(ANALYSIS_DIR, { withFileTypes: true });
  const groups = new Map(); // key: "TICKER|NAME", value: [{folder, v, ticker, name, fullPath}, ...]

  for (const e of entries) {
    if (!e.isDirectory()) continue;
    if (e.name.startsWith('_') || e.name === 'briefing') continue;
    const meta = parseAnalysisFolderName(e.name);
    if (!meta) continue;
    const key = `${meta.ticker}|${meta.name}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({
      folder: e.name,
      v: meta.v,
      ticker: meta.ticker,
      name: meta.name,
      fullPath: path.join(ANALYSIS_DIR, e.name),
    });
  }
  return groups;
}

async function scanReportsHtml() {
  if (!existsSync(REPORTS_DIR)) return new Map();
  const entries = await readdir(REPORTS_DIR, { withFileTypes: true });
  const groups = new Map();

  for (const e of entries) {
    if (!e.isFile()) continue;
    const meta = parseHtmlFilename(e.name);
    if (!meta) continue;
    const key = `${meta.ticker}|${meta.name}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({
      filename: e.name,
      date: meta.date,
      v: meta.v,
      ticker: meta.ticker,
      name: meta.name,
      fullPath: path.join(REPORTS_DIR, e.name),
    });
  }
  return groups;
}

// ---------------------------------------------------------------------------
// scorecard.md 메타 추출 (best-effort, grep 휴리스틱)
// ---------------------------------------------------------------------------
async function extractScorecardMeta(folderPath, v) {
  const candidates = [
    path.join(folderPath, 'scorecard.md'),
    path.join(folderPath, `${path.basename(folderPath)}_scorecard.md`),
  ];
  let scPath = candidates.find((p) => existsSync(p));
  if (!scPath) {
    // 폴더 안에서 *scorecard*.md 찾기
    try {
      const files = await readdir(folderPath);
      const found = files.find((f) => /scorecard/i.test(f) && f.endsWith('.md'));
      if (found) scPath = path.join(folderPath, found);
    } catch { /* skip */ }
  }
  if (!scPath) return { v, date: null, score: null, grade: null, target_price: null, fragile_assumptions: null, scorecard_path: null };

  let text = '';
  try {
    text = await readFile(scPath, 'utf-8');
  } catch {
    return { v, date: null, score: null, grade: null, target_price: null, fragile_assumptions: null, scorecard_path: scPath };
  }

  // 작성일 — 한/영 헤더 또는 mtime
  let date = parseAnalysisDate(text);
  const dateMatch = /(?:작성일|Date)[^0-9]*(\d{4}[-./]\d{2}[-./]\d{2})/i.exec(text);
  if (!date && dateMatch) date = dateMatch[1].replace(/[./]/g, '-');
  if (!date) {
    try { date = statSync(scPath).mtime.toISOString().slice(0, 10); } catch { /* skip */ }
  }

  // 종합 스코어 — 공유 파서 우선, 레거시 패턴 폴백
  let score = parseScore(text);
  const scoreM1 = /(?:종합\s*점수|총점|Score|Total)\s*[:：]?\s*([0-9]+(?:\.[0-9]+)?)\s*\/\s*100\b/i.exec(text);
  if (score == null && scoreM1) score = Number(scoreM1[1]);
  if (score == null) {
    const scoreM2 = /([0-9]+(?:\.[0-9]+)?)\s*점\s*해당/i.exec(text);
    if (scoreM2) score = Number(scoreM2[1]);
  }
  if (score == null) {
    // 표 셀 패턴: "**종합 점수** | ... | **81.74**"
    const scoreM3 = /\*\*\s*종합\s*점수\s*\*\*[\s\S]{0,120}?\*\*\s*([0-9]+(?:\.[0-9]+)?)\s*\*\*/i.exec(text);
    if (scoreM3) score = Number(scoreM3[1]);
  }

  // 투자 등급 — "결론 표현(→, 최종, 투자 등급:, Grade:) 다음 30자 안 키워드" 우선
  // 옛 분석엔 등급 기준표 ("80~100: 강력매수, 65~79: 매수...") 가 있어 단순 alternation 매치 부정확
  let grade = parseGrade(text);
  const conclKoM = /(?:→\s*\*?\*?\s*|최종[^:\n]{0,10}|\*\*\s*투자\s*등급\s*[:：]\s*\*?\*?|투자\s*등급\s*[:：]\s*\*?\*?)\s*(강력매수|강력매도|매수|매도|중립)/.exec(text);
  if (!grade && conclKoM) grade = conclKoM[1];
  if (!grade) {
    const conclEnM = /(?:Grade|Rating)[^\n]{0,40}?\b(Strong\s*Buy|Strong\s*Sell|Buy|Hold|Neutral|Sell)\b/i.exec(text);
    if (conclEnM) grade = conclEnM[1].replace(/\s+/g, ' ');
  }
  if (!grade) {
    const conclAlphaM = /(?:Grade|Rating)\s*[:：]?\s*([A-F][+-]?)\b(?!\w)/i.exec(text);
    if (conclAlphaM) grade = conclAlphaM[1];
  }

  // 목표주가 — 한/영 패턴
  // 한글: "목표주가: ₩72,000", "목표가 410"
  // 영어: "Target Price: $410", "PT: 410", "Price Target: 410"
  // [v3.39] 공유 파서 우선 — 레거시 pattern 4 가 컨센/단기 목표를 12M 보다 먼저 오캡처
  // (AAPL $305, 207940 컨센 206만 사고) + 후행 콤마 잔류 (ISRG "$449,").
  let target_price = null;
  {
    const tpShared = parseTargetPrice(text);
    if (tpShared != null) {
      const isKrw = /원\b|₩/.test(text) && !/\$/.test(text.slice(0, 400));
      target_price = `${isKrw ? '₩' : '$'}${tpShared.toLocaleString('en-US')}`;
    }
  }
  // [v3.26 fix, 2026-06-11] 통화 문맥(기호/USD/원) 필수 — 기존 [^0-9$₩]* 패턴이
  // 산문 "목표가 대비 상방이 +8%" 의 "8" 을 오캡처 (NVDA v5 timeline TP "8" 사고).
  // lib/scorecard_parser.mjs 와 동일 원칙. 우선순위: 표 행 > Base case > 중심 > 일반.
  const tpPatterns = [
    /12M\s*펀더멘털\s*목표가[^|\n]*\|\s*\**\s*([\$₩])\s?([0-9,]+(?:\.[0-9]+)?)/,
    /Base\s*case\**\s*[:：]?\s*\**\s*목표가\s*(?:USD|([\$₩]))\s?([0-9,]+(?:\.[0-9]+)?)/i,
    /중심\s*(?:USD|([\$₩]))\s?([0-9,]+(?:\.[0-9]+)?)/,
    /(?:목표주가|목표가)[^0-9\n]{0,15}?([\$₩])\s?([0-9,]+(?:\.[0-9]+)?)/,
    /(?:목표주가|목표가)[^0-9\n]{0,15}?()([0-9,]+(?:\.[0-9]+)?)\s*원/,
  ];
  for (const re of tpPatterns) {
    if (target_price) break;
    const m = re.exec(text);
    if (m) {
      target_price = `${m[1] || (re === tpPatterns[4] ? '₩' : '$')}${m[2]}`;
      break;
    }
  }
  if (!target_price) {
    // PT 단독은 제외 (WACC/PT% 노이즈) — Target Price / Price Target 헤더만
    const tpEn = /(?:Target\s*Price|Price\s*Target)\s*[:：]?\s*([\$₩])?\s*([0-9,]+(?:\.[0-9]+)?)/i.exec(text);
    if (tpEn) target_price = `${tpEn[1] || '$'}${tpEn[2]}`;
  }
  if (!target_price) {
    const tpShared = parseTargetPrice(text);
    if (tpShared != null) {
      const isKrw = /원\b|₩/.test(text) && !/\$/.test(text.slice(0, 400));
      target_price = `${isKrw ? '₩' : '$'}${tpShared.toLocaleString('en-US')}`;
    }
  }

  // 약한 가정 — § 섹션 안의 "1." "2." "3." 글머리 첫 줄 추출 (있으면)
  let fragile_assumptions = null;
  const fragileSection = /^##.*(?:약한\s*가정|Most\s*Fragile)[\s\S]*?(?=\n##|$)/im.exec(text);
  if (fragileSection) {
    const items = [];
    const itemRe = /^\s*\d+\.\s*\*\*?(.+?)\*\*?\s*(?:\(|—|\n)/gm;
    let m;
    while ((m = itemRe.exec(fragileSection[0])) && items.length < 3) items.push(m[1].trim());
    if (items.length) fragile_assumptions = items;
  }

  return { v, date, score, grade, target_price, fragile_assumptions, scorecard_path: path.relative(PROJECT_ROOT, scPath) };
}

// ---------------------------------------------------------------------------
// timeline.json 빌드
// ---------------------------------------------------------------------------
async function buildTimeline(ticker, name, vEntries) {
  const sorted = [...vEntries].sort((a, b) => (a.v ?? 0) - (b.v ?? 0));
  const history = [];
  for (const entry of sorted) {
    const meta = await extractScorecardMeta(entry.fullPath, entry.v);
    history.push({
      v: entry.v ?? 1, // null → v1 취급
      folder: entry.folder,
      ...meta,
    });
  }
  return {
    ticker,
    name,
    updated_at: nowKstIsoShort(),
    history_count: history.length,
    history,
  };
}

// ---------------------------------------------------------------------------
// 압축 (Bash tar / gzip)
// ---------------------------------------------------------------------------
function tarGzFolder(srcFolderAbs, archiveAbs) {
  const parent = path.dirname(srcFolderAbs);
  const name = path.basename(srcFolderAbs);
  const r = spawnSync('tar', ['-czf', archiveAbs, '-C', parent, name], { stdio: 'inherit' });
  if (r.status !== 0) throw new Error(`tar 실패: ${name}`);
}

function gzipFile(srcFileAbs, archiveAbs) {
  // gzip -c < src > archive.gz (원본 보존)
  const r = spawnSync('sh', ['-c', `gzip -c "${srcFileAbs}" > "${archiveAbs}"`], { stdio: 'inherit' });
  if (r.status !== 0) throw new Error(`gzip 실패: ${path.basename(srcFileAbs)}`);
}

// ---------------------------------------------------------------------------
// anomaly 탐지
// ---------------------------------------------------------------------------
function detectAnomalies(analysisGroups, reportsGroups) {
  const anomalies = [];

  // A. 같은 티커, 다른 종목명 (SCHD 케이스)
  const byTickerAna = new Map();
  for (const [key, entries] of analysisGroups) {
    const [ticker, name] = key.split('|');
    if (!byTickerAna.has(ticker)) byTickerAna.set(ticker, new Set());
    byTickerAna.get(ticker).add(name);
  }
  for (const [ticker, names] of byTickerAna) {
    if (names.size > 1) {
      anomalies.push({
        type: 'duplicate_name',
        ticker,
        names: [...names],
        scope: 'analysis/',
        recommendation: '사용자 직접 결정 — 어느 종목명을 표준으로? 다른 폴더는 archive 또는 삭제',
      });
    }
  }

  // B. analysis 폴더 없는데 reports HTML 만 있음 (고아 HTML)
  const anaKeys = new Set(analysisGroups.keys());
  for (const repKey of reportsGroups.keys()) {
    if (!anaKeys.has(repKey)) {
      anomalies.push({
        type: 'orphan_html',
        ticker_name: repKey,
        scope: 'reports/',
        recommendation: '분석 폴더 없음 — HTML만 보존 (timeline 추출 불가, 메타 누락)',
      });
    }
  }

  // C. 종목명 다양성 (reports 내)
  const byTickerRep = new Map();
  for (const [key] of reportsGroups) {
    const [ticker, name] = key.split('|');
    if (!byTickerRep.has(ticker)) byTickerRep.set(ticker, new Set());
    byTickerRep.get(ticker).add(name);
  }
  for (const [ticker, names] of byTickerRep) {
    if (names.size > 1) {
      anomalies.push({
        type: 'duplicate_name',
        ticker,
        names: [...names],
        scope: 'reports/',
        recommendation: '사용자 직접 결정',
      });
    }
  }

  return anomalies;
}

// ---------------------------------------------------------------------------
// 처리 계획 산출 (분석 + 리포트)
// ---------------------------------------------------------------------------
function planAnalysisCleanup(analysisGroups, tickerFilter) {
  const plan = []; // {ticker, name, keep: [folder...], archive: [folder...], timeline_target}
  for (const [key, entries] of analysisGroups) {
    const [ticker, name] = key.split('|');
    if (tickerFilter && !tickerFilter.includes(ticker)) continue;

    // v null(루트) → v1 으로 취급, sort
    const sorted = [...entries].sort((a, b) => (a.v ?? 1) - (b.v ?? 1));
    if (sorted.length <= 2) {
      // active 만 유지 (1개 또는 2개 — 정리 불필요)
      plan.push({ ticker, name, keep: sorted.map((e) => e.folder), archive: [], timeline_target: `${ticker}_${name}_timeline.json` });
      continue;
    }
    // 마지막 2개만 keep, 나머지 archive
    const archive = sorted.slice(0, sorted.length - 2);
    const keep = sorted.slice(sorted.length - 2);
    plan.push({
      ticker, name,
      keep: keep.map((e) => e.folder),
      archive: archive.map((e) => e),
      timeline_target: `${ticker}_${name}_timeline.json`,
    });
  }
  return plan;
}

function planReportsCleanup(reportsGroups, tickerFilter) {
  const plan = []; // {ticker, name, keep: [filename], archive: [{filename, date}, ...]}
  for (const [key, entries] of reportsGroups) {
    const [ticker, name] = key.split('|');
    if (tickerFilter && !tickerFilter.includes(ticker)) continue;
    if (entries.length <= 1) continue; // 정리 불필요
    const sorted = [...entries].sort((a, b) => a.date.localeCompare(b.date));
    const keep = sorted[sorted.length - 1];
    const archive = sorted.slice(0, sorted.length - 1);
    plan.push({ ticker, name, keep: keep.filename, archive });
  }
  return plan;
}

// ---------------------------------------------------------------------------
// 출력 (dry-run / apply 공통)
// ---------------------------------------------------------------------------
function printPlan(anaPlan, repPlan, anomalies, applyMode) {
  console.log(`\n=== cleanup_reanalysis ${applyMode ? '[APPLY]' : '[DRY-RUN]'} ===\n`);

  // 1. analysis 정리 계획
  const anaArchiveCount = anaPlan.reduce((s, p) => s + p.archive.length, 0);
  console.log(`[1] analysis/ 정리 — 종목 ${anaPlan.length}, archive 폴더 ${anaArchiveCount}`);
  if (anaPlan.length === 0) console.log('   (정리할 항목 없음)');
  for (const p of anaPlan) {
    if (p.archive.length === 0) {
      console.log(`   ${p.ticker}_${p.name}: 유지 ${p.keep.length} (정리 불필요)`);
    } else {
      console.log(`   ${p.ticker}_${p.name}: 유지 [${p.keep.join(', ')}] / archive [${p.archive.map((a) => a.folder).join(', ')}]`);
    }
  }

  // 2. reports 정리 계획
  const repArchiveCount = repPlan.reduce((s, p) => s + p.archive.length, 0);
  console.log(`\n[2] reports/ 정리 — 종목 ${repPlan.length}, archive HTML ${repArchiveCount}`);
  if (repPlan.length === 0) console.log('   (정리할 항목 없음)');
  for (const p of repPlan) {
    console.log(`   ${p.ticker}_${p.name}: 유지 ${p.keep} / archive [${p.archive.map((a) => a.filename).join(', ')}]`);
  }

  // 3. timeline 생성
  console.log(`\n[3] analysis/_history/ timeline.json 생성: ${anaPlan.length} 파일`);

  // 4. anomaly 보고 (분류별)
  const dupAna = anomalies.filter((a) => a.type === 'duplicate_name' && a.scope === 'analysis/');
  const dupRep = anomalies.filter((a) => a.type === 'duplicate_name' && a.scope === 'reports/');
  const orphans = anomalies.filter((a) => a.type === 'orphan_html');

  console.log(`\n[4] Anomaly 보고 (자동 처리 ❌)`);
  console.log(`    A. 이름 충돌 — 사용자 직접 결정 필요: ${dupAna.length + dupRep.length} 건`);
  for (const a of [...dupAna, ...dupRep]) {
    console.log(`       ${a.ticker} (${a.scope}): ${a.names.join(' vs ')}`);
    console.log(`       → ${a.recommendation}`);
  }
  if (dupAna.length + dupRep.length === 0) console.log('       (없음)');

  console.log(`    B. 분석 폴더 없는 reports HTML (cleanup 정상 진행, timeline 만 누락): ${orphans.length} 건`);
  if (orphans.length > 0) {
    const list = orphans.map((a) => a.ticker_name.replace('|', '_')).join(', ');
    console.log(`       ${list}`);
  }

  console.log(`\n=== 종료 ${applyMode ? '(파일 변경됨)' : '(변경 없음 — --apply 로 실제 실행)'} ===\n`);
}

// ---------------------------------------------------------------------------
// apply 실행
// ---------------------------------------------------------------------------
async function applyAnalysisCleanup(anaPlan, analysisGroups) {
  await mkdir(HISTORY_DIR, { recursive: true });
  await mkdir(ANALYSIS_ARCHIVE, { recursive: true });

  for (const p of anaPlan) {
    // 1. timeline 생성 (모든 v 메타 추출 — archive 처리 전 수행)
    const allEntries = analysisGroups.get(`${p.ticker}|${p.name}`);
    const timeline = await buildTimeline(p.ticker, p.name, allEntries);
    const timelinePath = path.join(HISTORY_DIR, p.timeline_target);
    await writeFile(timelinePath, JSON.stringify(timeline, null, 2), 'utf-8');
    console.log(`  ✅ timeline: ${path.relative(PROJECT_ROOT, timelinePath)}`);

    // 2. archive (archive 대상이 있는 경우만)
    for (const arc of p.archive) {
      const dateForName = (timeline.history.find((h) => h.v === (arc.v ?? 1))?.date || todayKst()).replace(/-/g, '');
      const archiveName = `${p.ticker}_${p.name}_v${arc.v ?? 1}_${dateForName}.tar.gz`;
      const archivePath = path.join(ANALYSIS_ARCHIVE, archiveName);
      tarGzFolder(arc.fullPath, archivePath);
      await rm(arc.fullPath, { recursive: true, force: true });
      console.log(`  📦 archive: ${path.relative(PROJECT_ROOT, archivePath)}`);
    }
  }
}

async function applyReportsCleanup(repPlan) {
  await mkdir(REPORTS_ARCHIVE, { recursive: true });
  for (const p of repPlan) {
    for (const arc of p.archive) {
      const archivePath = path.join(REPORTS_ARCHIVE, `${arc.filename}.gz`);
      gzipFile(arc.fullPath, archivePath);
      await rm(arc.fullPath, { force: true });
      console.log(`  📦 archive: ${path.relative(PROJECT_ROOT, archivePath)}`);
    }
  }
}

// ---------------------------------------------------------------------------
// 메인
// ---------------------------------------------------------------------------
async function main() {
  const args = parseArgs(process.argv.slice(2));
  const tickerFilter = args.tickers;

  const analysisGroups = await scanAnalysisFolders();
  const reportsGroups = await scanReportsHtml();
  const anomalies = detectAnomalies(analysisGroups, reportsGroups);
  const anaPlan = planAnalysisCleanup(analysisGroups, tickerFilter);
  const repPlan = planReportsCleanup(reportsGroups, tickerFilter);

  printPlan(anaPlan, repPlan, anomalies, args.apply);

  if (!args.apply) {
    console.log('변경 사항 적용하려면: --apply');
    return;
  }

  console.log('\n[APPLY] 실행 중...\n');
  await applyAnalysisCleanup(anaPlan, analysisGroups);
  await applyReportsCleanup(repPlan);
  console.log('\n✅ 완료');
}

main().catch((err) => {
  console.error('ERR:', err);
  process.exit(1);
});
