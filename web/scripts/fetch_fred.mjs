#!/usr/bin/env node
/**
 * fetch_fred.mjs — FRED (St. Louis Fed) API 매크로 지표 페치
 *
 * 출력: knowledge-base/macro/fred_snapshot.json
 *
 * 환경변수: FRED_API_KEY (필수, 미설정 시 graceful skip)
 * 발급: https://fredaccount.stlouisfed.org/login/secure/  (무료, 2분)
 *
 * 페치 시리즈 (15개 핵심 매크로):
 *   금리·통화: DGS10, DGS2, DFF, T10Y2Y, M2SL
 *   인플레이션: CPIAUCSL, PCEPILFE, T10YIE
 *   고용·경제: UNRATE, PAYEMS, GDPC1, INDPRO
 *   기타: DXY 대용 DTWEXBGS, VIX 대용 VIXCLS, 회사채 BAMLH0A0HYM2
 *
 * 각 시리즈: 최신값 + 1주 전 + 1개월 전 + 1년 전 + 변화율
 */
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { nowKstIsoShort } from './_kst.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const OUTPUT = path.join(PROJECT_ROOT, 'knowledge-base', 'macro', 'fred_snapshot.json');

// [v3.32, 2026-06-12] .env.local 자체 로드 (루트 + web/ 양쪽) — launchd·세션·prebuild
// 어디서 실행돼도 FRED_API_KEY 사용 가능. plain node 는 .env 를 자동 로드하지 않아
// web/.env.local 의 키가 한 번도 전달되지 못함 → 2026-05-30 이후 13일 stale 의 근본 원인.
{
  const { readFileSync } = await import('node:fs');
  for (const envPath of [path.join(PROJECT_ROOT, '.env.local'), path.join(PROJECT_ROOT, 'web', '.env.local')]) {
    try {
      for (const line of readFileSync(envPath, 'utf-8').split('\n')) {
        const m = line.match(/^\s*(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=\s*(.*)$/);
        if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '').trim();
      }
    } catch { /* 해당 경로 없으면 다음 */ }
  }
}

const API_KEY = process.env.FRED_API_KEY;

// 핵심 매크로 시리즈 정의 (label_ko + 단위 + 카테고리)
const SERIES = [
  // 금리·통화
  { id: 'DGS10', label: '10Y T-Bond', unit: '%', cat: 'rates', desc: '10년 미국채 수익률' },
  { id: 'DGS2', label: '2Y T-Bond', unit: '%', cat: 'rates', desc: '2년 미국채 수익률' },
  { id: 'DFF', label: 'Fed Funds Rate', unit: '%', cat: 'rates', desc: '연방기금금리' },
  { id: 'T10Y2Y', label: '10Y-2Y 스프레드', unit: '%p', cat: 'rates', desc: '장단기 금리차 (음수=역전)' },
  { id: 'M2SL', label: 'M2 통화량', unit: 'B$', cat: 'rates', desc: '광의통화 (10억 달러)' },
  // 인플레이션
  { id: 'CPIAUCSL', label: 'CPI', unit: 'YoY%', cat: 'inflation', desc: '소비자물가 (전년대비)', yoy: true },
  { id: 'PCEPILFE', label: 'Core PCE', unit: 'YoY%', cat: 'inflation', desc: 'Fed 선호 인플레 지표', yoy: true },
  { id: 'T10YIE', label: '10Y Breakeven', unit: '%', cat: 'inflation', desc: '시장의 기대 인플레이션' },
  // 고용·경제
  { id: 'UNRATE', label: '실업률', unit: '%', cat: 'jobs', desc: 'U-3 공식 실업률' },
  { id: 'PAYEMS', label: 'NFP 고용', unit: 'K', cat: 'jobs', desc: '비농업 고용 (전월대비 변화)', diff: true },
  { id: 'GDPC1', label: 'Real GDP', unit: 'YoY%', cat: 'growth', desc: '실질 GDP (전년대비)', yoy: true },
  { id: 'INDPRO', label: '산업생산', unit: 'YoY%', cat: 'growth', desc: '산업생산지수 (전년대비)', yoy: true },
  // 기타 시장
  { id: 'DTWEXBGS', label: 'USD 지수', unit: 'pt', cat: 'fx', desc: '광범위 달러 지수 (DXY 대용)' },
  { id: 'VIXCLS', label: 'VIX', unit: 'pt', cat: 'risk', desc: 'CBOE 변동성 지수' },
  { id: 'BAMLH0A0HYM2', label: '하이일드 스프레드', unit: '%', cat: 'risk', desc: '회사채 위험 프리미엄' },
];

async function fetchWithTimeout(url, ms = 10000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    return await fetch(url, { signal: ctrl.signal });
  } finally {
    clearTimeout(t);
  }
}

async function fetchSeries(id) {
  const url = `https://api.stlouisfed.org/fred/series/observations?series_id=${id}&api_key=${API_KEY}&file_type=json&sort_order=desc&limit=400`;
  const res = await fetchWithTimeout(url);
  if (!res.ok) throw new Error(`${id} HTTP ${res.status}`);
  const j = await res.json();
  return j.observations || [];
}

function parseValue(v) {
  if (!v || v === '.') return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function findClosest(observations, daysBack) {
  if (!observations.length) return null;
  const targetDate = new Date(observations[0].date);
  targetDate.setDate(targetDate.getDate() - daysBack);
  const target = targetDate.toISOString().slice(0, 10);
  let best = null;
  for (const o of observations) {
    if (o.date <= target) {
      best = o;
      break;
    }
  }
  return best;
}

function summarize(spec, obs) {
  if (!obs.length) return null;
  const cur = obs[0];
  const curVal = parseValue(cur.value);
  if (curVal == null) return null;

  // 시계열 길이 체크
  const oneWeek = findClosest(obs, 7);
  const oneMonth = findClosest(obs, 30);
  const oneYear = findClosest(obs, 365);

  const result = {
    id: spec.id,
    label: spec.label,
    unit: spec.unit,
    cat: spec.cat,
    desc: spec.desc,
    date: cur.date,
    value: curVal,
  };

  if (spec.yoy) {
    // YoY 계산: cur / 1년전 - 1
    const yoyVal = oneYear ? parseValue(oneYear.value) : null;
    if (yoyVal != null && yoyVal !== 0) {
      result.yoy_pct = Math.round(((curVal / yoyVal - 1) * 100) * 100) / 100;
    }
  } else if (spec.diff) {
    // 전월 대비 차이 (NFP 같은 누적 시리즈)
    const prevVal = oneMonth ? parseValue(oneMonth.value) : null;
    if (prevVal != null) {
      result.diff_1m = Math.round(curVal - prevVal);
    }
  } else {
    // 일반: 절대값 + 변화량
    result.prev_1w = oneWeek ? parseValue(oneWeek.value) : null;
    result.prev_1m = oneMonth ? parseValue(oneMonth.value) : null;
    result.prev_1y = oneYear ? parseValue(oneYear.value) : null;
  }

  return result;
}

async function loadExisting() {
  if (!existsSync(OUTPUT)) return null;
  try {
    return JSON.parse(await readFile(OUTPUT, 'utf-8'));
  } catch {
    return null;
  }
}

async function main() {
  if (!API_KEY) {
    console.log('SKIP: FRED_API_KEY 미설정. https://fredaccount.stlouisfed.org/login/secure/ 에서 무료 발급 후 .env 에 추가하세요.');
    // 빈 placeholder 작성 (위젯이 "키 미설정" 상태 표시)
    const existing = await loadExisting();
    if (!existing) {
      await mkdir(path.dirname(OUTPUT), { recursive: true });
      await writeFile(
        OUTPUT,
        JSON.stringify(
          { updated_at: nowKstIsoShort(), updated_tz: 'Asia/Seoul', api_key_required: true, series: [] },
          null,
          2,
        ),
        'utf-8',
      );
    }
    return;
  }

  console.log(`==> FRED ${SERIES.length}개 시리즈 페치 중...`);

  const results = await Promise.allSettled(SERIES.map((s) => fetchSeries(s.id)));

  const series = [];
  const failed = [];
  for (let i = 0; i < SERIES.length; i++) {
    const spec = SERIES[i];
    const r = results[i];
    if (r.status === 'fulfilled') {
      const summary = summarize(spec, r.value);
      if (summary) series.push(summary);
      else failed.push(`${spec.id}(empty)`);
    } else {
      failed.push(`${spec.id}(${r.reason?.message || 'err'})`);
    }
  }

  // 실패 시 기존 데이터 유지
  const existing = await loadExisting();
  if (series.length === 0 && existing?.series?.length > 0) {
    console.error(`ERR: 모든 시리즈 실패 - 기존 스냅샷 보존`);
    return;
  }

  const payload = {
    updated_at: nowKstIsoShort(),
    updated_tz: 'Asia/Seoul',
    api_key_required: false,
    count: series.length,
    series,
  };

  await mkdir(path.dirname(OUTPUT), { recursive: true });
  await writeFile(OUTPUT, JSON.stringify(payload, null, 2), 'utf-8');

  const rel = path.relative(PROJECT_ROOT, OUTPUT);
  console.log(`OK: FRED ${series.length}/${SERIES.length} 시리즈 → ${rel}`);
  if (failed.length) console.error(`  실패: ${failed.join(', ')}`);
}

main().catch((err) => {
  console.error('ERR:', err);
  process.exit(0); // 빌드 깨지지 않도록
});
