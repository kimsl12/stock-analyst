#!/usr/bin/env node
/**
 * build_readme.mjs — README.md 자동 갱신 (fence 영역 한정)
 *
 * ─────────────────────────────────────────────────────────────────────
 * 수정 룰 (Single Source of Truth — 5/29 v3.21)
 * ─────────────────────────────────────────────────────────────────────
 *
 * ## 수정 가능 영역 (fence 2개)
 *
 * 1. <!-- BEGIN AUTOGEN: recent-briefing --> ~ <!-- END AUTOGEN: recent-briefing -->
 *    - 위치: README.md "### 최근 브리핑 (지난 일주일)" 헤더 직후
 *    - 데이터 소스: reports/briefing/*.html 파일명 (스캔 결과)
 *    - 필터: KST 기준 today - 파일날짜 ≤ 7일
 *    - 정렬: 날짜 desc (최신 위)
 *    - 출력 형식: `- [{label}]({BASE_URL}/briefing/{filename}) — {YYYY-MM-DD}`
 *    - 7일 cutoff 항목 0건 시 출력: "_지난 7일간 신규 브리핑 없음._"
 *
 * 2. <!-- BEGIN AUTOGEN: counts --> ~ <!-- END AUTOGEN: counts -->
 *    - 위치: README.md "### 누적" 헤더 직후
 *    - 데이터 소스 3종:
 *        a. 종목·ETF = reports/*.html (직속만, 서브디렉토리 제외)
 *        b. 브리핑   = reports/briefing/*.html
 *        c. 애널리스트 = reports/analyst/items/ 안 디렉토리 개수
 *    - 출력 형식: "종목·ETF **{N}건** + 브리핑 **{N}건** + 애널리스트 **{N}건** = 총 **{N}건** ({YYYY-MM-DD} 기준)"
 *    - 기준일: todayKst() = Asia/Seoul YYYY-MM-DD
 *
 * ## 절대 미수정 영역 (fence 밖)
 *
 *   - 헤더 + 버전 라인 (# 종목분석 AI 에이전트 v3.21)
 *   - 상단 링크 (Vercel/Cloudflare)
 *   - 최신 분석 묶음 큐레이션 (### 2026-05-11 — CapEx 슈퍼사이클 19종 등) — 사용자 수동 작성
 *   - 변경 이력 표 — lead 수동 Edit (버전 추가 시)
 *   - 버전별 상세 섹션 (v3.21 핵심 / v3.17 / v3.10 / v3.9 …)
 *
 * ## 브리핑 타입 매핑 (BRIEFING_TYPE_MAP)
 *
 *   파일 prefix              → 표시 라벨
 *   ─────────────────────────────────────
 *   morning_                 → 모닝 브리핑
 *   evening_                 → 이브닝 브리핑
 *   weekly_                  → 주간 리포트
 *   global_intelligence_     → 글로벌 인텔리전스
 *   crypto_                  → 크립토 브리핑
 *   model_portfolio_         → 모델 포트폴리오
 *   rebalance_               → 리밸런싱
 *   performance_review_1m_   → 성과 리뷰 1M
 *   performance_review_      → 성과 리뷰
 *   user_portfolio_          → 내 포트폴리오
 *   full_                    → 풀 브리핑
 *   (prefix 미매치 = drop, 표시 안 됨)
 *
 * ## 안전장치
 *
 *   1. fence 미발견 시 ensureFence() 로 자동 삽입 (헤더 직후 ~ 다음 ### 또는 ## 직전 영역 교체)
 *   2. fence 안 본문이 변경 없으면 readFile = writeFile 동등 → "변경 없음" 보고 후 readFile.md 미수정
 *   3. apply 안 하면 dry-run (기본) — stdout 만 출력
 *   4. KST 시각 기준 (Asia/Seoul) — _kst.mjs todayKst() 사용. UTC 슬라이스 금지
 *
 * ## 모드
 *
 *   --dry-run (기본): fence 영역만 stdout 출력
 *   --apply: README.md 의 fence 영역만 in-place 교체 (fence 밖 무수정)
 *
 * ## 호출
 *
 *   cd 프로젝트루트 && node web/scripts/build_readme.mjs --dry-run
 *   cd 프로젝트루트 && node web/scripts/build_readme.mjs --apply
 *
 * ## 자동 호출 시점
 *
 *   - wiki-linter mode=full Step 9-B (5/29 v3.21 — agent Edit 대체)
 *   - /KB점검 명시 호출 시 wiki-linter 가 trigger
 *   - 메인 핸드오프 fallback (KB점검.md "Fallback" 섹션, v3.22 5/29)
 *
 * ## 관련
 *
 *   - 자매 스크립트: build_bootstrap.mjs (session-bootstrap.md analyses fence)
 *   - 룰 문서: .claude/agents/wiki-linter.md Step 9-B + .claude/commands/KB점검.md Fallback
 */
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { todayKst } from './_kst.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..', '..');
const README_PATH = path.join(ROOT, 'README.md');
const REPORTS = path.join(ROOT, 'reports');
const BRIEFING_DIR = path.join(REPORTS, 'briefing');
const ANALYST_ITEMS_DIR = path.join(REPORTS, 'analyst', 'items');

const BASE_URL = 'https://stock-analyst-jungwon1.vercel.app/reports';

const APPLY = process.argv.includes('--apply');

function log(msg) { process.stderr.write(msg + '\n'); }

const BRIEFING_TYPE_MAP = [
  { prefix: 'morning_', label: '모닝 브리핑' },
  { prefix: 'evening_', label: '이브닝 브리핑' },
  { prefix: 'weekly_', label: '주간 리포트' },
  { prefix: 'global_intelligence_', label: '글로벌 인텔리전스' },
  { prefix: 'crypto_', label: '크립토 브리핑' },
  { prefix: 'model_portfolio_', label: '모델 포트폴리오' },
  { prefix: 'rebalance_', label: '리밸런싱' },
  { prefix: 'performance_review_1m_', label: '성과 리뷰 1M' },
  { prefix: 'performance_review_', label: '성과 리뷰' },
  { prefix: 'user_portfolio_', label: '내 포트폴리오' },
  { prefix: 'full_', label: '풀 브리핑' },
];

function parseBriefingName(filename) {
  const m = filename.match(/^(.+?)_(\d{8})\.html$/);
  if (!m) return null;
  const stem = `${m[1]}_`;
  const ymd = m[2];
  const date = `${ymd.slice(0, 4)}-${ymd.slice(4, 6)}-${ymd.slice(6, 8)}`;
  for (const t of BRIEFING_TYPE_MAP) {
    if (stem.startsWith(t.prefix)) return { label: t.label, date, filename };
  }
  return null;
}

function daysBetween(isoA, isoB) {
  const a = Date.parse(isoA + 'T00:00:00+09:00');
  const b = Date.parse(isoB + 'T00:00:00+09:00');
  return Math.round((b - a) / 86400000);
}

async function buildRecentBriefingFence() {
  const today = todayKst();
  const entries = (await readdir(BRIEFING_DIR)).filter(f => f.endsWith('.html'));
  const parsed = entries.map(parseBriefingName).filter(Boolean);
  parsed.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
  const recent = parsed.filter(e => daysBetween(e.date, today) <= 7);
  if (recent.length === 0) {
    return '_지난 7일간 신규 브리핑 없음._';
  }
  const lines = recent.map(e => `- [${e.label}](${BASE_URL}/briefing/${e.filename}) — ${e.date}`);
  return lines.join('\n');
}

async function buildCountsFence() {
  const stockCount = (await readdir(REPORTS)).filter(f => f.endsWith('.html')).length;
  const briefingCount = (await readdir(BRIEFING_DIR)).filter(f => f.endsWith('.html')).length;
  let analystCount = 0;
  if (existsSync(ANALYST_ITEMS_DIR)) {
    const items = await readdir(ANALYST_ITEMS_DIR, { withFileTypes: true });
    analystCount = items.filter(d => d.isDirectory()).length;
  }
  const total = stockCount + briefingCount + analystCount;
  const today = todayKst();
  return `종목·ETF **${stockCount}건** + 브리핑 **${briefingCount}건** + 애널리스트 **${analystCount}건** = 총 **${total}건** (${today} 기준)`;
}

function replaceFence(content, name, newInner) {
  const begin = `<!-- BEGIN AUTOGEN: ${name} -->`;
  const end = `<!-- END AUTOGEN: ${name} -->`;
  const beginIdx = content.indexOf(begin);
  const endIdx = content.indexOf(end);
  if (beginIdx === -1 || endIdx === -1) {
    log(`  WARN: fence "${name}" 미발견 — 교체 생략 (수동 삽입 후 재실행 필요)`);
    return content;
  }
  const before = content.slice(0, beginIdx + begin.length);
  const after = content.slice(endIdx);
  return `${before}\n${newInner}\n${after}`;
}

function ensureFence(content, name, headerPattern, replaceTarget) {
  const begin = `<!-- BEGIN AUTOGEN: ${name} -->`;
  if (content.includes(begin)) return content;
  const idx = content.indexOf(headerPattern);
  if (idx === -1) {
    log(`  WARN: fence "${name}" 헤더 "${headerPattern}" 미발견 — 자동 삽입 실패`);
    return content;
  }
  const afterHeader = idx + headerPattern.length;
  const nextHeaderIdx = content.indexOf('\n### ', afterHeader + 1);
  const nextSectionIdx = content.indexOf('\n## ', afterHeader + 1);
  let cutEnd = -1;
  if (nextHeaderIdx !== -1 && (nextSectionIdx === -1 || nextHeaderIdx < nextSectionIdx)) {
    cutEnd = nextHeaderIdx;
  } else if (nextSectionIdx !== -1) {
    cutEnd = nextSectionIdx;
  } else {
    cutEnd = content.length;
  }
  const before = content.slice(0, afterHeader);
  const after = content.slice(cutEnd);
  const end = `<!-- END AUTOGEN: ${name} -->`;
  return `${before}\n\n${begin}\n${replaceTarget}\n${end}\n${after}`;
}

async function main() {
  const original = await readFile(README_PATH, 'utf8');
  const recentBriefing = await buildRecentBriefingFence();
  const counts = await buildCountsFence();

  log(`최근 브리핑 (7일): ${recentBriefing.split('\n').length}건`);
  log(`누적 카운트: ${counts}`);

  if (!APPLY) {
    log('--- dry-run (--apply 로 실제 적용) ---');
    process.stdout.write('### 최근 브리핑 (지난 일주일)\n\n');
    process.stdout.write(recentBriefing + '\n\n');
    process.stdout.write('### 누적\n\n');
    process.stdout.write(counts + '\n');
    return;
  }

  let updated = original;
  updated = ensureFence(updated, 'recent-briefing', '### 최근 브리핑 (지난 일주일)', recentBriefing);
  updated = ensureFence(updated, 'counts', '### 누적', counts);
  updated = replaceFence(updated, 'recent-briefing', recentBriefing);
  updated = replaceFence(updated, 'counts', counts);

  if (updated === original) {
    log('변경 없음 — README 그대로');
    return;
  }
  await writeFile(README_PATH, updated, 'utf8');
  log(`✅ README.md 갱신 완료 (recent-briefing + counts fence)`);
}

main().catch(e => { console.error(e); process.exit(1); });
