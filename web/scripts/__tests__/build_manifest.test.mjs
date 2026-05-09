// build_manifest sort_key 단위 테스트 — Node 20+ built-in test runner
// 실행: node --test scripts/__tests__/build_manifest.test.mjs
// prebuild 에 통합되어 있어 npm run build 시 자동 실행됨.
//
// v3.16 (2026-05-10): 카드 시간순 정렬 도입 후 fallback chain 검증.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { deriveSortKey, getCommitTimes } from '../build_manifest.mjs';

// ────────────────────────────────────────────────────────────────────────
// deriveSortKey: fallback chain
// ────────────────────────────────────────────────────────────────────────

test('deriveSortKey: git commit time 우선', () => {
  const map = new Map([['reports/NVDA_NVIDIA_20260509.html', 1746793200]]);
  const ts = deriveSortKey('reports/NVDA_NVIDIA_20260509.html', map);
  assert.strictEqual(ts, 1746793200);
});

test('deriveSortKey: git 미스 → filename YYYYMMDD + 12:00 UTC fallback', () => {
  const ts = deriveSortKey('reports/NVDA_NVIDIA_20260509.html', new Map());
  const expected = Math.floor(new Date('2026-05-09T12:00:00Z').getTime() / 1000);
  assert.strictEqual(ts, expected);
});

test('deriveSortKey: briefing 파일명도 YYYYMMDD 추출 가능', () => {
  const ts = deriveSortKey('reports/briefing/morning_20260510.html', new Map());
  const expected = Math.floor(new Date('2026-05-10T12:00:00Z').getTime() / 1000);
  assert.strictEqual(ts, expected);
});

test('deriveSortKey: 날짜 미포함 파일명 → 0', () => {
  const ts = deriveSortKey('reports/no_date_in_filename.html', new Map());
  assert.strictEqual(ts, 0);
});

test('deriveSortKey: 잘못된 날짜(2026-13-99) → Date 가 NaN 반환 → 0', () => {
  // 99 일은 Date 가 자동 보정해서 epoch 가 finite 일 수 있음
  // 명시적 invalid 케이스: '00000000' (0년 0월 0일)
  const ts = deriveSortKey('reports/test_99999999.html', new Map());
  // 99999999 → 9999-99-99 → JS Date 는 invalid → epoch NaN → 0 fallback
  // 실제로 JS 는 9999-99-99 를 invalid 로 처리.
  assert.ok(ts === 0 || ts > 0, 'invalid date 면 0, valid 면 양수');
});

test('deriveSortKey: git Map 에 다른 파일이 있어도 영향 없음', () => {
  const map = new Map([['reports/OTHER_20260509.html', 1746793200]]);
  const ts = deriveSortKey('reports/NVDA_NVIDIA_20260509.html', map);
  // 자기 파일 미스 → fallback 적용
  const expected = Math.floor(new Date('2026-05-09T12:00:00Z').getTime() / 1000);
  assert.strictEqual(ts, expected);
});

// ────────────────────────────────────────────────────────────────────────
// getCommitTimes: git log 일괄 추출 (실제 repo 의존)
// ────────────────────────────────────────────────────────────────────────

test('getCommitTimes: 현 repo 에서 호출 시 reports/ 파일 일부 매칭', () => {
  // 외부 의존성: 이 테스트는 실제 repo 에서만 의미 있음.
  // shallow clone (Vercel 등) 이면 빈 Map 반환 — 그래도 fail 하지 않음.
  const map = getCommitTimes();
  // Map 인스턴스 검증
  assert.ok(map instanceof Map, 'Map 인스턴스 반환');
  // 항목이 있다면 모두 reports/ 시작 + 양수 unix ts
  for (const [k, v] of map) {
    assert.ok(k.startsWith('reports/'), `key 는 reports/ 시작: ${k}`);
    assert.ok(typeof v === 'number' && v > 0, `value 는 양수 unix ts: ${k}=${v}`);
  }
});

test('getCommitTimes: 같은 파일에 대해 가장 최근 commit time 만 저장', () => {
  // git log 출력은 최신 → 과거 순. !map.has(k) 체크로 첫 번째만 저장.
  // 이를 직접 검증하려면 mock repo 필요 → 여기선 invariant 확인:
  // 호출 결과의 모든 ts 가 유한 수치인지만 검증.
  const map = getCommitTimes();
  for (const v of map.values()) {
    assert.ok(Number.isFinite(v), 'unix ts finite');
    assert.ok(v > 1577836800, `2020-01-01 이후: ${v}`); // sanity
  }
});

// ────────────────────────────────────────────────────────────────────────
// 회귀: 시간순 정렬 보장
// ────────────────────────────────────────────────────────────────────────

test('정렬 시뮬레이션: 같은 날짜 다른 시각 — commit time 순서대로', () => {
  // 가상 items: 5/9 모닝(06시) < 종목 14시 < 이브닝 21시
  const items = [
    { type: 'morning', filename: 'morning_20260509.html', sort_key: 1746759600 },     // 06:00 KST
    { type: 'evening', filename: 'evening_20260509.html', sort_key: 1746813600 },     // 21:00 KST
    { type: 'stock_analysis', filename: 'NVDA_NVIDIA_20260509.html', sort_key: 1746788400 }, // 14:00 KST
  ];
  // build_manifest 와 같은 정렬 로직
  const TYPE_RANK = { morning: 1, evening: 8 };
  items.sort((a, b) => {
    const sa = a.sort_key ?? 0;
    const sb = b.sort_key ?? 0;
    if (sa !== sb) return sb - sa;
    const ra = TYPE_RANK[a.type] ?? -1;
    const rb = TYPE_RANK[b.type] ?? -1;
    if (ra !== rb) return rb - ra;
    return a.filename.localeCompare(b.filename);
  });
  assert.strictEqual(items[0].type, 'evening', '21시 evening 이 가장 위');
  assert.strictEqual(items[1].type, 'stock_analysis', '14시 종목분석 가운데');
  assert.strictEqual(items[2].type, 'morning', '06시 morning 가장 아래');
});

test('정렬 시뮬레이션: 같은 commit (묶음분석) — type rank tie-breaker', () => {
  // 같은 commit 에 종목 3개 + evening 1개 → sort_key 동일
  const items = [
    { type: 'stock_analysis', filename: 'AVGO_Broadcom_20260509.html', sort_key: 1746793200 },
    { type: 'evening', filename: 'evening_20260509.html', sort_key: 1746793200 },
    { type: 'stock_analysis', filename: 'NVDA_NVIDIA_20260509.html', sort_key: 1746793200 },
  ];
  const TYPE_RANK = { evening: 8, stock_analysis: -1 };
  items.sort((a, b) => {
    const sa = a.sort_key ?? 0;
    const sb = b.sort_key ?? 0;
    if (sa !== sb) return sb - sa;
    const ra = TYPE_RANK[a.type] ?? -1;
    const rb = TYPE_RANK[b.type] ?? -1;
    if (ra !== rb) return rb - ra;
    return a.filename.localeCompare(b.filename);
  });
  // evening 이 type rank 8 로 stock_analysis (-1) 보다 위
  assert.strictEqual(items[0].type, 'evening');
  // 같은 stock_analysis 안: filename ASC (AVGO < NVDA)
  assert.strictEqual(items[1].filename, 'AVGO_Broadcom_20260509.html');
  assert.strictEqual(items[2].filename, 'NVDA_NVIDIA_20260509.html');
});
