#!/usr/bin/env node
/**
 * build_search_index.mjs — reports HTML 본문 추출 → web/public/search-data.json
 *
 * PLAN.md §10.2 (본문 검색) 기반.
 * 클라이언트(SearchBox.astro)가 FlexSearch로 인덱싱 → 검색.
 *
 * 구조:
 *   { generated_at, count, documents: [{ id, title, type, date, ticker, url, body }] }
 *   - body: HTML 도큐먼트 본문 텍스트 (2.5KB 자름 — 검색 핵심 부분만)
 *
 * 출력: web/public/search-data.json (gzip 압축은 Vercel CDN이 자동 적용)
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
const REPORTS_DIR = path.join(PROJECT_ROOT, 'reports');
const MANIFEST_JSON = path.join(WEB_DIR, 'src', 'data', 'manifest.json');
const OUTPUT_JSON = path.join(WEB_DIR, 'public', 'search-data.json');

// 본문 길이 상한 (각 도큐먼트당)
const BODY_LIMIT = 2500;

// ---------------------------------------------------------------------------
// HTML → text 변환
// ---------------------------------------------------------------------------
const RE_SCRIPT = /<script[\s\S]*?<\/script>/gi;
const RE_STYLE = /<style[\s\S]*?<\/style>/gi;
const RE_TAG = /<[^>]+>/g;
const ENTITY_MAP = {
  '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
  '&quot;': '"', '&#39;': "'", '&apos;': "'",
};

function htmlToText(html) {
  let t = html.replace(RE_SCRIPT, ' ').replace(RE_STYLE, ' ').replace(RE_TAG, ' ');
  for (const [from, to] of Object.entries(ENTITY_MAP)) {
    t = t.split(from).join(to);
  }
  // numeric entities
  t = t.replace(/&#(\d+);/g, (_, n) => {
    try { return String.fromCharCode(parseInt(n, 10)); } catch { return ' '; }
  });
  // 공백 정규화
  t = t.replace(/\s+/g, ' ').trim();
  return t;
}

async function extractBody(filepath) {
  try {
    // 처음 60KB만 읽어 빠르게 (본문 전체 인덱싱 안 함)
    const text = await readFile(filepath, 'utf-8');
    return htmlToText(text).slice(0, BODY_LIMIT);
  } catch {
    return '';
  }
}

// ---------------------------------------------------------------------------
// 메인
// ---------------------------------------------------------------------------
async function main() {
  if (!existsSync(MANIFEST_JSON)) {
    console.error('WARN: manifest.json 없음 — build_manifest.mjs 먼저 실행 필요');
    return;
  }
  const manifest = JSON.parse(await readFile(MANIFEST_JSON, 'utf-8'));
  const items = manifest.items;

  const documents = [];
  for (const it of items) {
    // url_path는 /reports/... 또는 /reports/briefing/... → 실제 파일은 PROJECT_ROOT/reports/...
    const rel = it.url_path.replace(/^\/reports\//, '');
    const filepath = path.join(REPORTS_DIR, rel);
    if (!existsSync(filepath)) continue;
    const body = await extractBody(filepath);
    documents.push({
      id: it.url_path,
      title: it.title ?? it.filename,
      type: it.type,
      date: it.date,
      ticker: it.ticker ?? null,
      url: it.url_path,
      body,
    });
  }

  await mkdir(path.dirname(OUTPUT_JSON), { recursive: true });
  await writeFile(
    OUTPUT_JSON,
    JSON.stringify(
      {
        generated_at: nowKstIsoShort(),  // KST
        generated_tz: 'Asia/Seoul',
        count: documents.length,
        documents,
      },
    ),
    'utf-8',
  );

  const sizeBytes = (await stat(OUTPUT_JSON)).size;
  const rel = path.relative(PROJECT_ROOT, OUTPUT_JSON);
  console.log(
    `OK: search-data 생성 (${documents.length} docs, ${(sizeBytes / 1024).toFixed(1)} KB) → ${rel}`,
  );
}

main().catch((err) => {
  console.error('ERR:', err);
  process.exit(1);
});
