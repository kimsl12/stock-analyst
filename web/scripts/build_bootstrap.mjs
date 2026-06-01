#!/usr/bin/env node
/**
 * build_bootstrap.mjs — session-bootstrap.md "analysis/ 유효 파일" 섹션 자동 재생성
 *
 * 정책 (2026-05-29, Hybrid 모드):
 *   1. timeline.json (analysis/_history/) 을 단일 진실 소스로 사용
 *   2. 종목별 latest v 만 active 테이블에 prepend (날짜 desc)
 *   3. history[:-1] 는 archived 섹션으로 분리
 *   4. 본문 carry-over → 실패 시 scorecard.md 에서 score/grade/TP 추출 fallback
 *   5. fence 영역만 교체 (BEGIN AUTOGEN / END AUTOGEN)
 *   6. 헤더·진행 중 작업·KB 요약 등은 절대 수정 ❌
 *
 * 모드:
 *   --dry-run (기본): 새 fence 영역만 stdout 출력, 파일 변경 ❌
 *   --apply: session-bootstrap.md 의 fence 영역만 in-place 교체
 *
 * 호출:
 *   cd 프로젝트루트 && node web/scripts/build_bootstrap.mjs --dry-run
 *   cd 프로젝트루트 && node web/scripts/build_bootstrap.mjs --apply
 *
 * 자동 호출 시점:
 *   - /재분석실행 Phase 2.5 cleanup_reanalysis.mjs 직후
 *   - /종목분석 Phase 3 git push 직후
 *   - /KB점검 주간 호출 직전
 */
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..', '..');
const HISTORY_DIR = path.join(ROOT, 'analysis', '_history');
const BOOTSTRAP_PATH = path.join(ROOT, 'session-bootstrap.md');

const FENCE_BEGIN = '<!-- BEGIN AUTOGEN: analyses -->';
const FENCE_END = '<!-- END AUTOGEN: analyses -->';

const args = process.argv.slice(2);
const APPLY = args.includes('--apply');

function log(msg) { process.stderr.write(msg + '\n'); }

async function loadTimelines() {
  const files = (await readdir(HISTORY_DIR)).filter(f => f.endsWith('_timeline.json'));
  const timelines = [];
  for (const f of files) {
    try {
      const raw = await readFile(path.join(HISTORY_DIR, f), 'utf8');
      const t = JSON.parse(raw);
      if (!t.history || t.history.length === 0) continue;
      timelines.push(t);
    } catch (e) {
      log(`  WARN: timeline parse 실패 ${f} — ${e.message}`);
    }
  }
  return timelines;
}

function extractFromScorecard(content) {
  const out = { score: null, grade: null, target_price: null };
  if (!content) return out;
  const scoreMatch = content.match(/종합[^0-9]{0,30}(\d{2,3}(?:\.\d+)?)\s*\/?\s*100/);
  if (scoreMatch) out.score = scoreMatch[1];
  const gradeMatch = content.match(/(?:투자\s*등급|\*\*투자\s*등급\*\*)[^:]{0,5}[:：]?\s*\*{0,2}(강력매수|강력매도|매수\s*하단|매수|중립|매도)\*{0,2}/);
  if (gradeMatch) out.grade = gradeMatch[1].replace(/\s+/g, '');
  else {
    const fallbackGrade = content.match(/\*\*(강력매수|강력매도|매수\s*하단|매수|중립|매도)\*\*/);
    if (fallbackGrade) out.grade = fallbackGrade[1].replace(/\s+/g, '');
  }
  const tpMatch = content.match(/(?:12M\s*)?(?:목표가|Target\s*Price|TP)\s*[:：]?\s*\*{0,2}\$?([\d,]+(?:\.\d+)?)/);
  if (tpMatch) {
    const raw = tpMatch[1];
    if (raw.length >= 2) out.target_price = '$' + raw;
  }
  return out;
}

async function tryReadScorecard(folder) {
  const p = path.join(ROOT, 'analysis', folder, 'scorecard.md');
  if (!existsSync(p)) {
    const altP = path.join(ROOT, 'analysis', folder, 'etf.md');
    if (existsSync(altP)) return readFile(altP, 'utf8');
    return null;
  }
  return readFile(p, 'utf8');
}

function parseExistingRows(bootstrapContent) {
  const map = new Map();
  const lines = bootstrapContent.split('\n');
  const rowPattern = /^\| \*\*([\w가-힣\\*]+_v\d+)\*\* \| \*\*([\d-]+)\*\* \| (.+?) \| ([^|]+?) \|\s*$/;
  for (const line of lines) {
    const m = line.match(rowPattern);
    if (m) {
      const key = m[1].replace(/\\/g, '').replace(/\*/g, '');
      map.set(key, { body: m[3].trim(), status: m[4].trim() });
    }
  }
  return map;
}

function makeRowKey(timeline, v) {
  return `${timeline.ticker}_${timeline.name}_v${v}`;
}

function makeShortBody(extracted) {
  const parts = [];
  if (extracted.score) parts.push(extracted.score);
  if (extracted.grade) parts.push(extracted.grade);
  let body = parts.join(' ').trim() || '갱신 필요';
  if (extracted.target_price) body += ` — TP ${extracted.target_price}`;
  return body;
}

function makeStatus(activeRowExisting, isActive) {
  if (activeRowExisting && activeRowExisting.status) return activeRowExisting.status;
  if (isActive) return '유효 (자동 생성, 본문 갱신 권장)';
  return '아카이브 (v 대체됨)';
}

async function buildRow(timeline, historyEntry, existingMap, isActive) {
  const key = makeRowKey(timeline, historyEntry.v);
  const existing = existingMap.get(key);
  let body;
  if (existing && existing.body && !existing.body.startsWith('갱신 필요')) {
    body = existing.body;
  } else {
    const scContent = await tryReadScorecard(historyEntry.folder);
    const extracted = extractFromScorecard(scContent);
    body = makeShortBody(extracted);
  }
  const status = makeStatus(existing, isActive);
  const date = historyEntry.date;
  const head = `**${key}**`;
  return `| ${head} | **${date}** | ${body} | ${status} |`;
}

function compareByDate(a, b) {
  if (a.date < b.date) return 1;
  if (a.date > b.date) return -1;
  return 0;
}

async function buildFenceContent(timelines) {
  const existingMap = parseExistingRows(await readFile(BOOTSTRAP_PATH, 'utf8'));
  const activeRows = [];
  const archivedRows = [];
  for (const t of timelines) {
    const sorted = [...t.history].sort((a, b) => a.v - b.v);
    const latest = sorted[sorted.length - 1];
    const older = sorted.slice(0, -1);
    activeRows.push({ date: latest.date, row: await buildRow(t, latest, existingMap, true) });
    for (const h of older) {
      archivedRows.push({ date: h.date, row: await buildRow(t, h, existingMap, false) });
    }
  }
  activeRows.sort(compareByDate);
  archivedRows.sort(compareByDate);

  const lines = [];
  lines.push('| 폴더 | 날짜 | 스코어 | 상태 |');
  lines.push('|------|------|--------|------|');
  for (const { row } of activeRows) lines.push(row);
  lines.push('');
  lines.push('### 📦 아카이브 (옛 v — timeline.json 보존, bootstrap 참고용)');
  lines.push('');
  lines.push('| 폴더 | 날짜 | 스코어 | 상태 |');
  lines.push('|------|------|--------|------|');
  for (const { row } of archivedRows) lines.push(row);
  return { content: lines.join('\n'), activeCount: activeRows.length, archivedCount: archivedRows.length };
}

/**
 * 일회성 결과 섹션 prune (v3.22 — 2026-06-01).
 *
 * 룰:
 *   - 헤더 패턴 = `^## .* (\d{4}-\d{2}-\d{2}).*$` 또는 `^## .* \d{4}-\d{2}-\d{2}` (날짜 포함)
 *   - 헤더 안 날짜 vs todayKst 차이 > STALE_DAYS_THRESHOLD 시 섹션 전체 제거 (다음 `^## ` 또는 EOF 까지)
 *   - 보호 헤더 화이트리스트 (항상 유지, 날짜 매치 무시):
 *       "## 마지막 작업"
 *       "## analysis/ 유효 파일"
 *       "## 파이프라인 버전"
 *       "## ⚠️ 환경 상태"  (사용자 명시 결정 영역)
 *       "## 현재 KB 상태 요약"  (lead/wiki-linter 갱신 영역)
 *   - 일회성 결과 영역 (`## COST Costco 분석 결과 (2026-04-22, 신규)` 등) 만 prune
 */
const STALE_DAYS_THRESHOLD = 30;
const PROTECTED_HEADERS = [
  '## 마지막 작업',
  '## analysis/ 유효 파일',
  '## 파이프라인 버전',
  '## ⚠️ 환경 상태',
  '## 현재 KB 상태 요약',
];

function todayKst() {
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Seoul' }).format(new Date());
}

function daysBetween(isoA, isoB) {
  const a = Date.parse(isoA + 'T00:00:00+09:00');
  const b = Date.parse(isoB + 'T00:00:00+09:00');
  return Math.round((b - a) / 86400000);
}

function pruneStaleSections(bootstrap, logFn) {
  const lines = bootstrap.split('\n');
  const today = todayKst();
  const out = [];
  const removed = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const headerMatch = line.match(/^## (.+)$/);
    if (!headerMatch) {
      out.push(line);
      i++;
      continue;
    }
    const isProtected = PROTECTED_HEADERS.some(h => line.startsWith(h));
    const dateMatch = line.match(/(\d{4}-\d{2}-\d{2})/);
    if (isProtected || !dateMatch) {
      out.push(line);
      i++;
      continue;
    }
    const sectionDate = dateMatch[1];
    const age = daysBetween(sectionDate, today);
    if (age <= STALE_DAYS_THRESHOLD) {
      out.push(line);
      i++;
      continue;
    }
    // 30일+ stale 일회성 섹션 — 다음 `## ` 헤더까지 또는 EOF 까지 제거
    let j = i + 1;
    while (j < lines.length && !/^## /.test(lines[j])) j++;
    removed.push({ header: line, date: sectionDate, age, lineCount: j - i });
    i = j;
  }
  if (removed.length > 0) {
    logFn(`prune: ${removed.length} stale 섹션 제거 (>${STALE_DAYS_THRESHOLD}일 경과)`);
    for (const r of removed) {
      logFn(`  - ${r.header} (${r.age}일 경과, ${r.lineCount}줄)`);
    }
  }
  return out.join('\n');
}

function replaceFence(bootstrap, newInner) {
  const beginIdx = bootstrap.indexOf(FENCE_BEGIN);
  const endIdx = bootstrap.indexOf(FENCE_END);
  if (beginIdx === -1 || endIdx === -1) {
    const headerPattern = '## analysis/ 유효 파일 (최근 30일)';
    const headerIdx = bootstrap.indexOf(headerPattern);
    if (headerIdx === -1) throw new Error('bootstrap 헤더 "## analysis/ 유효 파일 (최근 30일)" 미발견 — fence 삽입 불가');
    const afterHeader = headerIdx + headerPattern.length;
    const nextSectionIdx = bootstrap.indexOf('\n## ', afterHeader);
    const cutEnd = nextSectionIdx === -1 ? bootstrap.length : nextSectionIdx;
    const before = bootstrap.slice(0, afterHeader);
    const after = bootstrap.slice(cutEnd);
    return `${before}\n\n${FENCE_BEGIN}\n${newInner}\n${FENCE_END}\n${after}`;
  }
  const before = bootstrap.slice(0, beginIdx + FENCE_BEGIN.length);
  const after = bootstrap.slice(endIdx);
  return `${before}\n${newInner}\n${after}`;
}

async function main() {
  const timelines = await loadTimelines();
  log(`timeline 로드: ${timelines.length} 종목`);
  const { content, activeCount, archivedCount } = await buildFenceContent(timelines);
  log(`active ${activeCount} 행 / archived ${archivedCount} 행`);
  if (!APPLY) {
    log('--- dry-run (--apply 로 실제 적용) ---');
    process.stdout.write(content + '\n');
    return;
  }
  const original = await readFile(BOOTSTRAP_PATH, 'utf8');
  let updated = replaceFence(original, content);
  updated = pruneStaleSections(updated, log);
  if (updated === original) {
    log('변경 없음 — bootstrap 그대로');
    return;
  }
  await writeFile(BOOTSTRAP_PATH, updated, 'utf8');
  log(`✅ session-bootstrap.md 갱신 완료 (active ${activeCount} / archived ${archivedCount})`);
}

main().catch(e => { console.error(e); process.exit(1); });
