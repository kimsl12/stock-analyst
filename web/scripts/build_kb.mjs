#!/usr/bin/env node
/**
 * build_kb.mjs — knowledge-base/ 마크다운 파싱 → web/src/data/kb.json
 *
 * 추출 항목:
 *  - market_snapshot: daily_snapshot.md 미국지수+환율+원자재+아시아+크립토에서 7개 핵심 지수
 *  - kb_health:       _index.md P0/P1 표 행 카운트 + lint_last_run
 *  - upcoming_events: economic_calendar.md "다음 주" 섹션 + 미래 날짜 추출
 *  - recommendations: 최근 7일 briefing HTML들에서 .strong-buy 텍스트 추출 (D1)
 *
 * 모든 항목은 graceful: 파일 없거나 파싱 실패 시 null/[] 반환 (빌드 안 깨짐).
 */
import { readFile, writeFile, readdir, mkdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WEB_DIR = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(WEB_DIR, '..');
const KB = path.join(PROJECT_ROOT, 'knowledge-base');
const REPORTS_BRIEFING = path.join(PROJECT_ROOT, 'reports', 'briefing');
const OUTPUT_JSON = path.join(WEB_DIR, 'src', 'data', 'kb.json');

// ---------------------------------------------------------------------------
// 공통: 마크다운 표 파서 (| col1 | col2 |)
// ---------------------------------------------------------------------------
function splitRow(line) {
  return line.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
}

/** 헤더 정규식이 매칭되는 줄 다음의 첫 표를 파싱. */
function findTableAfter(text, headingRegex) {
  const lines = text.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    if (!headingRegex.test(lines[i])) continue;
    // 헤딩 다음에 표 헤더 행 찾기
    for (let j = i + 1; j < Math.min(i + 25, lines.length); j++) {
      if (/^\s*\|.+\|\s*$/.test(lines[j]) && /^\s*\|[\s\-:|]+\|\s*$/.test(lines[j + 1] ?? '')) {
        const headers = splitRow(lines[j]);
        const rows = [];
        for (let k = j + 2; k < lines.length; k++) {
          if (!/^\s*\|.+\|\s*$/.test(lines[k]) || /^\s*\|[\s\-:|]+\|\s*$/.test(lines[k])) break;
          rows.push(splitRow(lines[k]));
        }
        return { headers, rows };
      }
    }
  }
  return null;
}

const stripBold = (s) => (s ?? '').replace(/\*\*/g, '').trim();
const cleanNum = (s) => {
  const v = stripBold(s).replace(/[$,원%₩+]/g, '').replace(/\s+/g, '').trim();
  if (!v || v === '—' || v === '-') return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
};

// ---------------------------------------------------------------------------
// 1. market_snapshot
// ---------------------------------------------------------------------------
async function parseMarketSnapshot() {
  const file = path.join(KB, 'market', 'daily_snapshot.md');
  if (!existsSync(file)) return { items: [], updated: null };
  const text = await readFile(file, 'utf-8');

  // frontmatter updated
  const fm = text.match(/^---\s*\n([\s\S]*?)\n---/);
  const updatedMatch = fm?.[1]?.match(/updated:\s*([\d-]+)/);
  const updated = updatedMatch?.[1] ?? null;

  const items = [];

  // 미국 지수 표
  const us = findTableAfter(text, /^###\s+미국\s*지수/);
  if (us) {
    const map = new Map(us.rows.map((r) => [stripBold(r[0]), r]));
    for (const want of ['S&P 500', 'NASDAQ', 'VIX']) {
      const r = map.get(want);
      if (!r) continue;
      const value = cleanNum(r[1]);
      const change = stripBold(r[2] ?? '');
      const changeNum = cleanNum(r[2]?.replace('%', ''));
      items.push({
        label: want, value, value_fmt: stripBold(r[1]),
        change_pct: changeNum, change_fmt: change,
        category: 'us',
      });
    }
  }

  // 아시아: KOSPI
  const asia = findTableAfter(text, /^###\s+아시아/);
  if (asia) {
    for (const r of asia.rows) {
      if (stripBold(r[0]) === 'KOSPI') {
        items.push({
          label: 'KOSPI', value: cleanNum(r[1]), value_fmt: stripBold(r[1]),
          change_pct: cleanNum(r[2]?.replace('%', '')), change_fmt: stripBold(r[2] ?? ''),
          category: 'asia',
        });
        break;
      }
    }
  }

  // 환율: USD/KRW
  const fx = findTableAfter(text, /^###\s+환율/);
  if (fx) {
    for (const r of fx.rows) {
      if (stripBold(r[0]) === 'USD/KRW') {
        items.push({
          label: 'USD/KRW', value: cleanNum(r[1]), value_fmt: stripBold(r[1]),
          change_pct: cleanNum(r[2]?.replace('%', '')), change_fmt: stripBold(r[2] ?? ''),
          category: 'fx',
        });
        break;
      }
    }
  }

  // 원자재: WTI, Gold
  const cm = findTableAfter(text, /^###\s+원자재/);
  if (cm) {
    for (const r of cm.rows) {
      const label = stripBold(r[0]);
      if (label === 'WTI Crude Oil' || label === 'Gold Futures') {
        items.push({
          label: label === 'WTI Crude Oil' ? 'WTI' : 'Gold',
          value: cleanNum(r[1]), value_fmt: stripBold(r[1]),
          change_pct: cleanNum(r[2]?.replace('%', '')), change_fmt: stripBold(r[2] ?? ''),
          category: 'commodity',
        });
      }
    }
  }

  // BTC: 본문 검색 (~"BTC $XXX" 패턴)
  const btcMatch = text.match(/BTC\s*\$([\d,]+)/);
  if (btcMatch) {
    const v = Number(btcMatch[1].replace(/,/g, ''));
    items.push({
      label: 'BTC', value: v, value_fmt: `$${btcMatch[1]}`,
      change_pct: null, change_fmt: '',
      category: 'crypto',
    });
  }

  return { items, updated };
}

// ---------------------------------------------------------------------------
// 2. kb_health (F2)
// ---------------------------------------------------------------------------
async function parseKbHealth() {
  const file = path.join(KB, '_index.md');
  if (!existsSync(file)) return { p0: 0, p1: 0, last_lint: null, available: false };
  const text = await readFile(file, 'utf-8');

  const fm = text.match(/lint_last_run:\s*([\d-]+)/);
  const last_lint = fm?.[1] ?? null;

  const p0Tbl = findTableAfter(text, /^##\s*P0/);
  const p1Tbl = findTableAfter(text, /^##\s*P1/);
  const p0 = p0Tbl ? p0Tbl.rows.filter((r) => r[0] && !/^\[INFO\]/.test(r[0])).length : 0;
  const p1 = p1Tbl ? p1Tbl.rows.filter((r) => r[0] && !/^\[INFO\]/.test(r[0])).length : 0;

  return { p0, p1, last_lint, available: true };
}

// ---------------------------------------------------------------------------
// 3. upcoming_events (C3)
// ---------------------------------------------------------------------------
async function parseUpcomingEvents() {
  const file = path.join(KB, 'market', 'economic_calendar.md');
  if (!existsSync(file)) return [];
  const text = await readFile(file, 'utf-8');

  // "다음 주" 또는 "예정" 키워드가 들어간 섹션의 표만
  const lines = text.split(/\r?\n/);
  const events = [];
  const today = new Date().toISOString().slice(0, 10);

  for (let i = 0; i < lines.length; i++) {
    if (!/^\s*\|.+\|\s*$/.test(lines[i])) continue;
    if (!/^\s*\|[\s\-:|]+\|\s*$/.test(lines[i + 1] ?? '')) continue;
    // 표 발견. 데이터 행 파싱.
    for (let k = i + 2; k < lines.length; k++) {
      if (!/^\s*\|.+\|\s*$/.test(lines[k])) break;
      const cols = splitRow(lines[k]);
      if (cols.length < 4) continue;
      // 날짜 패턴 YYYY-MM-DD 또는 MM/DD
      const dateMatch = cols[0].match(/(\d{4})-(\d{2})-(\d{2})/);
      if (!dateMatch) continue;
      const date = `${dateMatch[1]}-${dateMatch[2]}-${dateMatch[3]}`;
      if (date < today) continue; // 과거 SKIP
      events.push({
        date,
        time: stripBold(cols[1] ?? ''),
        country: stripBold(cols[2] ?? ''),
        indicator: stripBold(cols[3] ?? ''),
      });
    }
    i = (lines.findIndex((l, idx) => idx > i + 1 && !/^\s*\|.+\|\s*$/.test(l)) ?? lines.length) - 1;
  }

  // 중복 제거 + 날짜+시간순
  const seen = new Set();
  const unique = events.filter((e) => {
    const k = `${e.date}|${e.time}|${e.indicator}`;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
  unique.sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time));
  return unique.slice(0, 12); // 다음 12건
}

// ---------------------------------------------------------------------------
// 4. recommendations (D1) — 최근 7일 briefing HTML에서 추천 종목 추출
//   - 1순위 패턴: /종목분석 TICKER 코드 블록 (실질 추천 카탈로그)
//   - 2순위 패턴: class="strong-buy" 텍스트 (legacy 호환)
//   - 빈도 카운트 → Top 25
// ---------------------------------------------------------------------------
async function parseRecommendations() {
  if (!existsSync(REPORTS_BRIEFING)) return [];
  const sevenDaysAgo = new Date();
  sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
  const cutoff = sevenDaysAgo.toISOString().slice(0, 10).replace(/-/g, '');

  const files = (await readdir(REPORTS_BRIEFING)).filter((f) => {
    const m = f.match(/_(\d{8})\.html$/);
    return m && m[1] >= cutoff;
  });

  const counts = new Map();

  // 1순위: /종목분석 TICKER (한글/영문/숫자 2~10자) — 빈 명령 제외
  const reCmd = /\/종목분석\s+([A-Z가-힣0-9]{2,10})\b/g;
  // 2순위: <span/td/.../> class="strong-buy" 안의 텍스트 (legacy)
  const reBuy = /<(?:span|td|div|li|strong|b)[^>]*class=['"][^'"]*strong-buy[^'"]*['"][^>]*>([^<]+)</gi;

  for (const fn of files) {
    try {
      const html = await readFile(path.join(REPORTS_BRIEFING, fn), 'utf-8');

      // 1순위: /종목분석 TICKER
      let m;
      while ((m = reCmd.exec(html)) !== null) {
        const t = m[1].trim();
        if (!t) continue;
        // 일반 키워드 제외 (안전)
        if (/^(BUY|SELL|HOLD|매수|매도|적정|관망|강력|예시)$/i.test(t)) continue;
        counts.set(t, (counts.get(t) ?? 0) + 1);
      }

      // 2순위: legacy .strong-buy
      while ((m = reBuy.exec(html)) !== null) {
        const raw = m[1].replace(/[(),:!?]/g, ' ').trim();
        const tokens = raw.split(/\s+/).filter((t) => t.length >= 2 && t.length <= 12);
        for (const t of tokens) {
          if (/^(매수|매도|강력|적정|관망|RECOMMEND|BUY|HOLD|SELL|STRONG)$/i.test(t)) continue;
          counts.set(t, (counts.get(t) ?? 0) + 1);
        }
      }
    } catch {
      /* skip */
    }
  }

  return [...counts.entries()]
    .map(([text, count]) => ({ text, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 25);
}

// ---------------------------------------------------------------------------
// 5b. performance — knowledge-base/performance_history.md 누적 표 파싱 (Day 14)
//   "추천일|종목|방향|진입가|현재가|수익률|결과|출처" 8컬럼 표에서 결과 컬럼 카운트
//   적중률 = 적중 / (적중 + 오류) — 진행중·보류 제외
// ---------------------------------------------------------------------------
async function parsePerformance() {
  const file = path.join(KB, 'performance_history.md');
  if (!existsSync(file)) {
    return { available: false, total: 0, hit: 0, miss: 0, ongoing: 0, hold: 0, hit_rate_pct: null, last_updated: null };
  }
  const text = await readFile(file, 'utf-8');
  const fm = text.match(/^---\s*\n([\s\S]*?)\n---/);
  const updMatch = fm?.[1]?.match(/updated:\s*([\d-]+)/);
  const last_updated = updMatch?.[1] ?? null;

  const lines = text.split(/\r?\n/);
  let inTable = false;
  const counts = { hit: 0, miss: 0, ongoing: 0, hold: 0, other: 0 };

  for (let i = 0; i < lines.length; i++) {
    if (/^\s*\|\s*추천일\s*\|/.test(lines[i]) && /^\s*\|\s*-+/.test(lines[i + 1] ?? '')) {
      inTable = true;
      i += 1;
      continue;
    }
    if (!inTable) continue;
    if (!/^\s*\|.+\|\s*$/.test(lines[i])) break;
    if (/^\s*\|\s*<!--/.test(lines[i])) continue;
    const cols = lines[i].trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
    if (cols.length < 8) continue;
    const result = cols[6] ?? '';
    if (/적중/.test(result)) counts.hit += 1;
    else if (/오류/.test(result)) counts.miss += 1;
    else if (/진행중/.test(result)) counts.ongoing += 1;
    else if (/보류/.test(result)) counts.hold += 1;
    else counts.other += 1;
  }

  const total = counts.hit + counts.miss + counts.ongoing + counts.hold + counts.other;
  const decided = counts.hit + counts.miss;
  const hit_rate_pct = decided > 0 ? Math.round((counts.hit / decided) * 1000) / 10 : null;

  return {
    available: true,
    total,
    hit: counts.hit,
    miss: counts.miss,
    ongoing: counts.ongoing,
    hold: counts.hold,
    hit_rate_pct,
    last_updated,
  };
}

// ---------------------------------------------------------------------------
// 5. timemachine — 1주/1개월/3개월 범위별 첫 추천일 + 빈도 (Day 12-13)
//   각 범위에서 ticker별 가장 오래된 추천일 = first_date
//   클라이언트가 /api/price/{ticker}?at={first_date} 호출하여 수익률 계산
// ---------------------------------------------------------------------------
async function parseTimemachine() {
  if (!existsSync(REPORTS_BRIEFING)) return { '1w': [], '1m': [], '3m': [] };

  const reCmd = /\/종목분석\s+([A-Z가-힣0-9]{2,10})\b/g;
  const periods = { '1w': 7, '1m': 30, '3m': 90 };
  const result = {};

  const all = await readdir(REPORTS_BRIEFING);
  for (const [key, days] of Object.entries(periods)) {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    const cutoff = cutoffDate.toISOString().slice(0, 10).replace(/-/g, '');

    const files = all.filter((f) => {
      const m = f.match(/_(\d{8})\.html$/);
      return m && m[1] >= cutoff;
    });

    /** ticker → { first: 'YYYYMMDD', count: N } */
    const seen = new Map();

    for (const fn of files) {
      const dateMatch = fn.match(/_(\d{8})\.html$/);
      if (!dateMatch) continue;
      const fileDate = dateMatch[1];

      try {
        const html = await readFile(path.join(REPORTS_BRIEFING, fn), 'utf-8');
        const fileTickers = new Set();
        let m;
        while ((m = reCmd.exec(html)) !== null) {
          const t = m[1].trim();
          if (!t) continue;
          if (/^(BUY|SELL|HOLD|매수|매도|적정|관망|강력|예시)$/i.test(t)) continue;
          fileTickers.add(t);
        }
        for (const t of fileTickers) {
          const cur = seen.get(t);
          if (!cur) {
            seen.set(t, { first: fileDate, count: 1 });
          } else {
            cur.count += 1;
            if (fileDate < cur.first) cur.first = fileDate;
          }
        }
      } catch {
        /* skip */
      }
    }

    result[key] = [...seen.entries()]
      .map(([ticker, v]) => ({
        ticker,
        first_date: `${v.first.slice(0, 4)}-${v.first.slice(4, 6)}-${v.first.slice(6, 8)}`,
        count: v.count,
      }))
      .sort((a, b) => b.count - a.count || a.first_date.localeCompare(b.first_date))
      .slice(0, 20);
  }

  return result;
}

// ---------------------------------------------------------------------------
// 메인
// ---------------------------------------------------------------------------
async function main() {
  const [market_snapshot, kb_health, upcoming_events, recommendations, timemachine, performance] = await Promise.all([
    parseMarketSnapshot().catch((e) => { console.error('market_snapshot err:', e.message); return { items: [], updated: null }; }),
    parseKbHealth().catch((e) => { console.error('kb_health err:', e.message); return { p0: 0, p1: 0, last_lint: null, available: false }; }),
    parseUpcomingEvents().catch((e) => { console.error('upcoming_events err:', e.message); return []; }),
    parseRecommendations().catch((e) => { console.error('recommendations err:', e.message); return []; }),
    parseTimemachine().catch((e) => { console.error('timemachine err:', e.message); return { '1w': [], '1m': [], '3m': [] }; }),
    parsePerformance().catch((e) => { console.error('performance err:', e.message); return { available: false, total: 0, hit: 0, miss: 0, ongoing: 0, hold: 0, hit_rate_pct: null, last_updated: null }; }),
  ]);

  await mkdir(path.dirname(OUTPUT_JSON), { recursive: true });
  await writeFile(
    OUTPUT_JSON,
    JSON.stringify(
      {
        generated_at: new Date().toISOString().slice(0, 19),
        market_snapshot,
        kb_health,
        upcoming_events,
        recommendations,
        timemachine,
        performance,
      },
      null,
      2,
    ),
    'utf-8',
  );

  const rel = path.relative(PROJECT_ROOT, OUTPUT_JSON);
  const tmCount = (timemachine['1w']?.length ?? 0) + (timemachine['1m']?.length ?? 0) + (timemachine['3m']?.length ?? 0);
  console.log(
    `OK: kb 데이터 생성 (market=${market_snapshot.items.length}, p0=${kb_health.p0}, p1=${kb_health.p1}, events=${upcoming_events.length}, recs=${recommendations.length}, tm=${tmCount}, perf=${performance.total}/${performance.hit_rate_pct ?? '—'}%) → ${rel}`,
  );
}

main().catch((err) => {
  console.error('ERR:', err);
  process.exit(1);
});
