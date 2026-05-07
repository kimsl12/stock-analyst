#!/usr/bin/env node
/**
 * fetch_fear_greed.mjs — CNN + Crypto Fear & Greed Index 페치
 *
 * 출력: knowledge-base/market/fear_greed.json
 *   {
 *     updated_at: "2026-05-07T18:00:00+09:00",
 *     cnn: { score, rating, prev_close, prev_1w, prev_1m, prev_1y, source_ts },
 *     crypto: { score, rating, source_ts }
 *   }
 *
 * - CNN: production.dataviz.cnn.io/index/fearandgreed/graphdata (브라우저 UA 필요)
 * - Crypto: api.alternative.me/fng/?limit=1
 *
 * 실패 시: 기존 JSON 보존 (덮어쓰지 않음). 둘 중 하나만 실패해도 성공한 쪽은 갱신.
 */
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { nowKstIsoShort } from './_kst.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const OUTPUT = path.join(PROJECT_ROOT, 'knowledge-base', 'market', 'fear_greed.json');

const BROWSER_UA =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

async function fetchWithTimeout(url, options = {}, ms = 10000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    return await fetch(url, { ...options, signal: ctrl.signal });
  } finally {
    clearTimeout(t);
  }
}

async function fetchCnn() {
  const res = await fetchWithTimeout(
    'https://production.dataviz.cnn.io/index/fearandgreed/graphdata',
    {
      headers: {
        'User-Agent': BROWSER_UA,
        Accept: 'application/json, text/plain, */*',
        Referer: 'https://edition.cnn.com/markets/fear-and-greed',
        Origin: 'https://edition.cnn.com',
      },
    },
  );
  if (!res.ok) throw new Error(`CNN HTTP ${res.status}`);
  const j = await res.json();
  const fg = j?.fear_and_greed;
  if (!fg) throw new Error('CNN payload 형식 오류');
  return {
    score: Math.round(fg.score * 10) / 10,
    rating: fg.rating, // "extreme fear" / "fear" / "neutral" / "greed" / "extreme greed"
    prev_close: Math.round(fg.previous_close * 10) / 10,
    prev_1w: Math.round(fg.previous_1_week * 10) / 10,
    prev_1m: Math.round(fg.previous_1_month * 10) / 10,
    prev_1y: Math.round(fg.previous_1_year * 10) / 10,
    source_ts: fg.timestamp,
  };
}

async function fetchCrypto() {
  // limit=370 → 오늘 + 369일 전까지 확보 (1년 비교 + 여유분)
  const res = await fetchWithTimeout('https://api.alternative.me/fng/?limit=370');
  if (!res.ok) throw new Error(`Crypto HTTP ${res.status}`);
  const j = await res.json();
  const data = j?.data;
  if (!data || data.length === 0) throw new Error('Crypto payload 형식 오류');
  // data[0] = 오늘, data[1] = 어제, data[7] = 1주 전, data[30] = 1개월 전, data[365] = 1년 전
  const at = (i) => (data[i] ? Number(data[i].value) : null);
  const cur = data[0];
  return {
    score: Number(cur.value),
    rating: (cur.value_classification || '').toLowerCase(),
    prev_close: at(1),
    prev_1w: at(7),
    prev_1m: at(30),
    prev_1y: at(365),
    source_ts: cur.timestamp ? new Date(Number(cur.timestamp) * 1000).toISOString() : null,
  };
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
  const existing = await loadExisting();

  const [cnnRes, cryptoRes] = await Promise.allSettled([fetchCnn(), fetchCrypto()]);

  const cnn =
    cnnRes.status === 'fulfilled'
      ? cnnRes.value
      : existing?.cnn
        ? { ...existing.cnn, _stale: true, _error: cnnRes.reason?.message ?? 'unknown' }
        : null;

  const crypto =
    cryptoRes.status === 'fulfilled'
      ? cryptoRes.value
      : existing?.crypto
        ? { ...existing.crypto, _stale: true, _error: cryptoRes.reason?.message ?? 'unknown' }
        : null;

  const payload = {
    updated_at: nowKstIsoShort(),
    updated_tz: 'Asia/Seoul',
    cnn,
    crypto,
  };

  await mkdir(path.dirname(OUTPUT), { recursive: true });
  await writeFile(OUTPUT, JSON.stringify(payload, null, 2), 'utf-8');

  const rel = path.relative(PROJECT_ROOT, OUTPUT);
  const cnnTxt = cnn ? `${cnn.score} (${cnn.rating})${cnn._stale ? ' [stale]' : ''}` : '실패';
  const cryptoTxt = crypto
    ? `${crypto.score} (${crypto.rating})${crypto._stale ? ' [stale]' : ''}`
    : '실패';
  console.log(`OK: F&G 페치 — CNN=${cnnTxt}, Crypto=${cryptoTxt} → ${rel}`);

  if (cnnRes.status === 'rejected') console.error(`  CNN 페치 실패: ${cnnRes.reason?.message}`);
  if (cryptoRes.status === 'rejected') console.error(`  Crypto 페치 실패: ${cryptoRes.reason?.message}`);
}

main().catch((err) => {
  console.error('ERR:', err);
  // 빌드 깨지지 않도록 exit 0
  process.exit(0);
});
