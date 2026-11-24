// daily_pick_eval.test.mjs — 데일리픽 성적표 채점 코어(단기) 단위 테스트
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { entryIndex, closeOnOrBefore, scoreBand, buildShortRows, summarize } from '../lib/daily_pick_eval.mjs';

// 영업일(월~금)만 생성하는 합성 시계열
function mkSeries(startDate, closes, { opens, highs } = {}) {
  const dates = [];
  const d = new Date(startDate + 'T00:00:00Z');
  while (dates.length < closes.length) {
    const wd = d.getUTCDay();
    if (wd !== 0 && wd !== 6) dates.push(d.toISOString().slice(0, 10));
    d.setUTCDate(d.getUTCDate() + 1);
  }
  return { symbol: 'X', dates, open: opens ?? closes, high: highs ?? closes, close: closes };
}

const row = (over = {}) => ({
  date: '2026-11-02', ticker: 'AAA', name: 'A', market: 'US', score: 79, grade: '매수',
  version: 'v1', analysis_dir: 'A_v1', analysis_date: '2026-11-01', tp_price: null, reasons: [],
  regime: { weight_set: '상승장' }, ...over,
});

test('entry bar not yet available → pending', () => {
  const symbols = { AAA: mkSeries('2026-10-26', [100, 101, 102, 103, 104]), '^GSPC': mkSeries('2026-10-26', [1, 1, 1, 1, 1]) };
  const [r] = buildShortRows([row({ date: '2026-11-10' })], symbols);
  assert.equal(r.status, 'pending');
  assert.equal(r.entry_price, null);
  assert.equal(r.h['5'], null);
  assert.equal(r.h['20'], null);
});

test('entry uses first bar on or after pick date', () => {
  // 2026-11-07 은 토요일 → 월요일 11-09 바 종가가 진입가
  const stock = mkSeries('2026-11-02', [100, 101, 102, 103, 104, 105, 106, 107]);
  const bench = mkSeries('2026-11-02', [1, 1, 1, 1, 1, 1, 1, 1]);
  const [r] = buildShortRows([row({ date: '2026-11-07' })], { AAA: stock, '^GSPC': bench });
  assert.equal(r.status, 'ok');
  assert.equal(r.entry_date, '2026-11-09');
  assert.equal(r.entry_price, 105);
});

test('5d return and excess', () => {
  const stock = mkSeries('2026-11-02', [100, 101, 102, 103, 104, 110]);
  const bench = mkSeries('2026-11-02', [100, 101, 102, 103, 103, 104]);
  const [r] = buildShortRows([row()], { AAA: stock, '^GSPC': bench });
  assert.ok(Math.abs(r.h['5'].ret - 10) < 1e-9);
  assert.ok(Math.abs(r.h['5'].excess - 6) < 1e-9);
  assert.equal(r.h['5'].hit, true);
  assert.equal(r.h['20'], null);
  assert.equal(r.weight_set, '상승장');
  assert.equal(r.band, '78-80');
});

test('benchmark uses last bar on or before date', () => {
  const stock = mkSeries('2026-11-02', [100, 101, 102, 103, 104, 110]);
  // 벤치마크는 11-06 까지만 (평가일 11-09 바 없음) → 11-06 종가 사용
  const bench = mkSeries('2026-11-02', [100, 100, 100, 100, 104]);
  const [r] = buildShortRows([row()], { AAA: stock, '^GSPC': bench });
  assert.ok(Math.abs(r.h['5'].excess - 6) < 1e-9);
});

test('no price series → no_price row', () => {
  const [r] = buildShortRows([row()], { '^GSPC': mkSeries('2026-11-02', [1, 2]) });
  assert.equal(r.status, 'no_price');
  assert.equal(r.entry_date, null);
  assert.equal(r.h['5'], null);
});

test('scoreBand', () => {
  assert.equal(scoreBand(77.6), '75-77');
  assert.equal(scoreBand(78), '78-80');
  assert.equal(scoreBand(81), '81+');
});

test('entryIndex / closeOnOrBefore', () => {
  const s = mkSeries('2026-11-02', [1, 2, 3]);
  assert.equal(entryIndex(s, '2026-12-01'), -1);
  assert.equal(entryIndex(s, '2026-11-03'), 1);
  assert.equal(closeOnOrBefore(s, '2026-11-01'), null);
  assert.equal(closeOnOrBefore(s, '2026-11-08'), 3);
});

test('summarize', () => {
  const mk = (ret, excess) => ({ h: { 20: { ret, excess, hit: excess > 0 } } });
  const s = summarize([mk(10, 5), mk(4, 1), mk(2, 1), mk(-3, -2), { h: { 20: null } }], '20');
  assert.equal(s.n, 4);
  assert.equal(s.hit_rate, 0.75);
  assert.equal(s.avg_return, 3.25);
  assert.equal(s.avg_excess, 1.25);
  assert.equal(s.small_sample, true);
  assert.deepEqual(summarize([], '20'), { n: 0, hit_rate: null, avg_return: null, avg_excess: null, small_sample: true });
});
