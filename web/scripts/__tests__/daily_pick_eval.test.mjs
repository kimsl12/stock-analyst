// daily_pick_eval.test.mjs — 데일리픽 성적표 채점 코어(단기·장기) 단위 테스트
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  entryIndex, closeOnOrBefore, scoreBand, buildShortRows, summarize, buildRecommendations,
  breakdown, concentration, buildEval,
} from '../lib/daily_pick_eval.mjs';

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

// ───────── 장기 리뷰 (추천 묶음·마감) ─────────
// 2026-11-02(월) 시작 영업일: idx0=11-02, 1=11-03, 2=11-04, 3=11-05, 4=11-06, 5=11-09, 6=11-10

const flat = (n, v) => Array(n).fill(v);
const near = (a, b) => Math.abs(a - b) < 1e-9;
const judg = (over = {}) => ({
  date: '2026-11-04', ticker: 'AAA', anchor_date: '2026-11-02', anchor_version: 'v1', version: 'v2',
  verdict: '동일', rationale: 'r', judged_at: '2026-11-21', judged_by: 'agent', ...over,
});
// 종목·벤치 시계열 묶음 (벤치 기본 평탄)
const px = (stock, bench) => ({ AAA: stock, '^GSPC': bench ?? mkSeries('2026-11-02', flat(stock.close.length, 1)) });

test('same analysis_dir repick → auto 동일', () => {
  const ledger = [row(), row({ date: '2026-11-04' })];
  const { recs, pending, invalid } = buildRecommendations(ledger, px(mkSeries('2026-11-02', flat(10, 100))), [], {});
  assert.equal(recs.length, 1);
  assert.equal(recs[0].repicks.length, 1);
  assert.equal(recs[0].repicks[0].verdict, '동일');
  assert.equal(recs[0].repicks[0].judged_by, 'auto-same-version');
  assert.equal(recs[0].repicks[0].rationale, null);
  assert.equal(pending.length, 0);
  assert.equal(invalid.length, 0);
  assert.equal(recs[0].close, null);
  assert.equal(recs[0].status, 'ok');
});

test('전환 closes old rec at new entry', () => {
  const ledger = [row(), row({ date: '2026-11-09', version: 'v2', analysis_dir: 'A_v2', score: 82 })];
  const stock = mkSeries('2026-11-02', [100, 101, 102, 103, 104, 105, 106, 107]);
  const j = judg({ date: '2026-11-09', verdict: '전환' });
  const { recs, pending } = buildRecommendations(ledger, px(stock), [j], {});
  assert.equal(recs.length, 2);
  assert.deepEqual(recs[0].close, { reason: '논지 교체', date: '2026-11-09', price: 105, bars: 5 });
  assert.equal(recs[1].anchor_date, '2026-11-09');
  assert.equal(recs[1].entry_price, 105);
  assert.equal(recs[1].band, '81+');
  assert.equal(recs[1].close, null);
  assert.equal(pending.length, 0);
});

test('TP hit closes at tp, gap opens at open', () => {
  // 진입 바(idx0) 고가 200 은 진입 전 → 무시 (R2). idx3 고가 112 ≥ tp 110 → 청산가 110
  const closes = flat(10, 100);
  const highs = [200, 100, 100, 112, 100, 100, 100, 100, 100, 100];
  const a = buildRecommendations([row({ tp_price: 110 })], px(mkSeries('2026-11-02', closes, { highs })), [], {});
  assert.deepEqual(a.recs[0].close, { reason: '달성', date: '2026-11-05', price: 110, bars: 3 });
  assert.equal(a.recs[0].tp_status, 'hit');
  // 그 바 시가가 이미 tp 위 → 청산가 = 시가
  const opens = [100, 100, 100, 115, 100, 100, 100, 100, 100, 100];
  const highs2 = [100, 100, 100, 116, 100, 100, 100, 100, 100, 100];
  const b = buildRecommendations([row({ tp_price: 110 })], px(mkSeries('2026-11-02', closes, { opens, highs: highs2 })), [], {});
  assert.equal(b.recs[0].close.price, 115);
  assert.equal(b.recs[0].close.reason, '달성');
});

test('no tp → never 달성', () => {
  const closes = flat(260, 100);
  closes[250] = 130;
  const highs = flat(260, 999);
  const stock = mkSeries('2026-11-02', closes, { highs });
  const { recs } = buildRecommendations([row({ tp_price: null })], px(stock), [], {});
  assert.equal(recs[0].tp_status, 'none');
  assert.deepEqual(recs[0].close, { reason: '만기', date: stock.dates[250], price: 130, bars: 250 });
  assert.ok(near(recs[0].h['250'].ret, 30));
});

test('implausible tp (> entry×1.8) → tp_status none, 달성 없음', () => {
  const highs = flat(10, 100);
  highs[4] = 5000;
  const stock = mkSeries('2026-11-02', flat(10, 100), { highs });
  const { recs } = buildRecommendations([row({ tp_price: 1000 })], px(stock), [], {});
  assert.equal(recs[0].tp_status, 'none');
  assert.equal(recs[0].tp_price, 1000);
  assert.equal(recs[0].close, null);
  // 경계값 1.8× 는 유효
  const ok = buildRecommendations([row({ tp_price: 180 })], px(stock), [], {});
  assert.equal(ok.recs[0].tp_status, 'hit');
});

test('frozen horizons after close', () => {
  const closes = flat(130, 100);
  const highs = flat(130, 100);
  highs[40] = 125; // 40바째 달성 → 청산가 120 (+20%)
  const bench = flat(130, 100);
  for (let i = 30; i < 130; i++) bench[i] = 110; // 마감일 벤치 +10%
  for (let i = 100; i < 130; i++) bench[i] = 200; // 마감 이후 벤치 변동은 무시돼야 함
  const p = px(mkSeries('2026-11-02', closes, { highs }), mkSeries('2026-11-02', bench));
  const { recs } = buildRecommendations([row({ tp_price: 120 })], p, [], {});
  assert.equal(recs[0].close.bars, 40);
  for (const k of ['60', '120', '250']) {
    assert.ok(near(recs[0].h[k].ret, 20), k);
    assert.ok(near(recs[0].h[k].excess, 10), k);
    assert.equal(recs[0].h[k].hit, true);
  }
});

test('repick after closed rec starts new rec without judgment', () => {
  const highs = flat(10, 100);
  highs[3] = 120;
  const ledger = [row({ tp_price: 110 }), row({ date: '2026-11-09', version: 'v2', analysis_dir: 'A_v2' })];
  const { recs, pending, invalid } = buildRecommendations(ledger, px(mkSeries('2026-11-02', flat(10, 100), { highs })), [], {});
  assert.equal(recs.length, 2);
  assert.equal(recs[0].close.reason, '달성');
  assert.equal(recs[1].anchor_date, '2026-11-09');
  assert.equal(pending.length, 0);
  assert.equal(invalid.length, 0);
});

test('price close on repick entry bar day counts as already closed (≤)', () => {
  // 재픽 11-09 진입 바(idx5) 장중에 tp 도달 → 재픽 시점엔 이미 마감 → 판정 불필요
  const highs = flat(10, 100);
  highs[5] = 120;
  const ledger = [row({ tp_price: 110 }), row({ date: '2026-11-09', version: 'v2', analysis_dir: 'A_v2' })];
  const { recs, pending } = buildRecommendations(ledger, px(mkSeries('2026-11-02', flat(10, 100), { highs })), [], {});
  assert.equal(recs.length, 2);
  assert.deepEqual(recs[0].close, { reason: '달성', date: '2026-11-09', price: 110, bars: 5 });
  assert.equal(pending.length, 0);
});

test('unjudged repick → pending, later picks skipped', () => {
  const ledger = [
    row(),
    row({ date: '2026-11-04', version: 'v2', analysis_dir: 'A_v2' }),
    row({ date: '2026-11-06', version: 'v3', analysis_dir: 'A_v3' }),
  ];
  const { recs, pending } = buildRecommendations(ledger, px(mkSeries('2026-11-02', flat(10, 100))), [], {});
  assert.equal(recs.length, 1);
  assert.equal(recs[0].provisional, true);
  assert.equal(recs[0].repicks.length, 0);
  assert.equal(recs[0].provisional_from, '2026-11-04');
  assert.deepEqual(pending, [{
    ticker: 'AAA', date: '2026-11-04', version: 'v2', analysis_dir: 'A_v2',
    anchor_date: '2026-11-02', anchor_version: 'v1', anchor_analysis_dir: 'A_v1',
  }]);
});

test('override wins and invalidates stale judgment', () => {
  const ledger = [
    row(),
    row({ date: '2026-11-04', version: 'v2', analysis_dir: 'A_v2' }),
    row({ date: '2026-11-06', version: 'v3', analysis_dir: 'A_v3' }),
  ];
  const stale = judg({ date: '2026-11-06', version: 'v3' });
  const judgments = [judg({ date: '2026-11-04', verdict: '동일' }), stale];
  const { recs, pending, invalid } = buildRecommendations(
    ledger, px(mkSeries('2026-11-02', flat(10, 100))), judgments, { 'AAA@2026-11-04': '전환' },
  );
  assert.equal(recs.length, 2);
  assert.equal(recs[0].close.reason, '논지 교체');
  assert.equal(recs[1].anchor_date, '2026-11-04');
  assert.equal(recs[1].repicks.length, 0);
  assert.equal(recs[1].provisional, true);
  assert.deepEqual(invalid, [stale]);
  assert.equal(pending.length, 1);
  assert.equal(pending[0].date, '2026-11-06');
  assert.equal(pending[0].anchor_date, '2026-11-04');
});

test('repick without entry bar yet → stop, no pending; sole new pick → pending rec', () => {
  const stock = mkSeries('2026-11-02', flat(5, 100)); // 11-06 까지
  const ledger = [row(), row({ date: '2026-11-10', version: 'v2', analysis_dir: 'A_v2' })];
  const a = buildRecommendations(ledger, px(stock), [], {});
  assert.equal(a.recs.length, 1);
  assert.equal(a.recs[0].repicks.length, 0);
  assert.equal(a.recs[0].provisional, false);
  assert.equal(a.pending.length, 0);
  const b = buildRecommendations([row({ date: '2026-11-10', tp_price: 110 })], px(stock), [], {});
  assert.equal(b.recs[0].status, 'pending');
  assert.equal(b.recs[0].tp_status, 'none'); // 진입가 미확정 → tp 검증 불가
  assert.equal(b.recs[0].entry_price, null);
  assert.equal(b.recs[0].h['60'], null);
});

test('no price series → no_price recs, bundling still applies', () => {
  const ledger = [row(), row({ date: '2026-11-09', version: 'v2', analysis_dir: 'A_v2' })];
  const j = judg({ date: '2026-11-09', verdict: '전환' });
  const { recs } = buildRecommendations(ledger, { '^GSPC': mkSeries('2026-11-02', [1, 2]) }, [j], {});
  assert.equal(recs.length, 2);
  assert.equal(recs[0].status, 'no_price');
  assert.equal(recs[0].close.reason, '논지 교체');
  assert.deepEqual(recs[0].close, { reason: '논지 교체', date: '2026-11-09', price: null, bars: null });
  assert.equal(recs[0].h['120'], null);
  assert.equal(recs[1].status, 'no_price');
  assert.equal(buildRecommendations([row({ tp_price: 110 })], {}, [], {}).recs[0].tp_status, 'none');
});

test('provisional rec: close null and horizons after unjudged repick null (R10b)', () => {
  // anchor tp 110, 미판정 재픽 bar5(11-09), 이후 bar8 에서 tp 도달 → 진행 중 처리
  const highs = flat(130, 100);
  highs[8] = 120;
  const stock = mkSeries('2026-11-02', flat(130, 100), { highs });
  const ledger = [row({ tp_price: 110 }), row({ date: '2026-11-09', version: 'v2', analysis_dir: 'A_v2' })];
  const a = buildRecommendations(ledger, px(stock), [], {});
  assert.equal(a.recs[0].provisional, true);
  assert.equal(a.recs[0].provisional_from, '2026-11-09');
  assert.equal(a.recs[0].close, null);
  assert.equal(a.recs[0].tp_status, 'open');
  assert.equal(a.recs[0].h['60'], null);
  // 재픽이 bar70 → 60일 칸(재픽 이전)은 유지, 120일 칸은 null
  const s2 = mkSeries('2026-11-02', flat(130, 100));
  const b = buildRecommendations([row(), row({ date: s2.dates[70], version: 'v2', analysis_dir: 'A_v2' })], px(s2), [], {});
  assert.equal(b.recs[0].provisional_from, s2.dates[70]);
  assert.ok(b.recs[0].h['60'] != null && near(b.recs[0].h['60'].ret, 0));
  assert.equal(b.recs[0].h['120'], null);
  assert.equal(b.recs[0].h['250'], null);
  // 비잠정 추천은 provisional_from null
  assert.equal(buildRecommendations([row()], px(s2), [], {}).recs[0].provisional_from, null);
});

test('tp at or below entry → tp_status none, no 달성 (R1)', () => {
  // 실제 사례: VOO 진입 685.26, tp 600 → 1바째 달성 기록되던 문제
  const stock = mkSeries('2026-11-02', flat(10, 100));
  for (const tp of [90, 100]) {
    const { recs } = buildRecommendations([row({ tp_price: tp })], px(stock), [], {});
    assert.equal(recs[0].tp_status, 'none', String(tp));
    assert.equal(recs[0].close, null, String(tp));
  }
});

test('invalid verdict values → unjudged; bad judgment rows → invalid', () => {
  const ledger = [row(), row({ date: '2026-11-04', version: 'v2', analysis_dir: 'A_v2' })];
  const stock = mkSeries('2026-11-02', flat(10, 100));
  const bad = judg({ verdict: '같음' });
  const a = buildRecommendations(ledger, px(stock), [bad], {});
  assert.deepEqual(a.invalid, [bad]);
  assert.equal(a.pending.length, 1);
  assert.equal(a.recs[0].provisional, true);
  // 비정상 override 값 → 미판정 (유효 판정 행으로 넘어가지 않음)
  const b = buildRecommendations(ledger, px(stock), [judg({ verdict: '보강' })], { 'AAA@2026-11-04': '전환!' });
  assert.equal(b.pending.length, 1);
  assert.equal(b.recs.length, 1);
  assert.equal(b.recs[0].repicks.length, 0);
});

test('frozen horizons after 논지 교체 close at bar 40', () => {
  const closes = flat(300, 100);
  closes[40] = 120;
  for (let i = 41; i < 300; i++) closes[i] = 150; // 마감 이후 종목 변동 무시
  const bench = flat(300, 100);
  for (let i = 30; i < 300; i++) bench[i] = 110;
  for (let i = 100; i < 300; i++) bench[i] = 200;
  const stock = mkSeries('2026-11-02', closes);
  const ledger = [row(), row({ date: stock.dates[40], version: 'v2', analysis_dir: 'A_v2' })];
  const j = judg({ date: stock.dates[40], verdict: '전환' });
  const { recs } = buildRecommendations(ledger, px(stock, mkSeries('2026-11-02', bench)), [j], {});
  assert.deepEqual(recs[0].close, { reason: '논지 교체', date: stock.dates[40], price: 120, bars: 40 });
  for (const k of ['60', '120', '250']) {
    assert.ok(near(recs[0].h[k].ret, 20), k);
    assert.ok(near(recs[0].h[k].excess, 10), k);
    assert.equal(recs[0].h[k].hit, true, k);
  }
});

// ───────── 집계 (Task 6) ─────────

const cell = (hit) => ({ ret: hit ? 5 : -5, excess: hit ? 5 : -5, hit });

test('breakdown: null key → 기록 없음, 키 오름차순', () => {
  const rows = [
    { k: 'b', h: { 20: cell(true) } },
    { k: null, h: { 20: cell(false) } },
    { k: 'a', h: { 20: cell(true) } },
  ];
  const out = breakdown(rows, (r) => r.k, '20');
  assert.deepEqual(out.map((o) => o.key), ['a', 'b', '기록 없음']);
  assert.equal(out[0].n, 1);
});

test('concentration: A 3픽 적중, B 1픽 실패', () => {
  const mk = (t, hit) => ({ ticker: t, h: { 20: cell(hit) } });
  const c = concentration([mk('A', true), mk('A', true), mk('A', true), mk('B', false)], '20');
  assert.equal(c.equal_weight_hit_rate, 0.5);
  assert.equal(c.top5_share, 1);
  assert.deepEqual(c.by_ticker[0], { ticker: 'A', picks: 3, hit_rate: 1 });
});

test('buildEval 스모크: 원장 3행·합성 가격', () => {
  const closes = Array.from({ length: 30 }, (_, i) => 100 + i);
  const symbols = { AAA: mkSeries('2026-10-01', closes), '^GSPC': mkSeries('2026-10-01', closes.map(() => 100)) };
  const ledger = [
    row({ date: '2026-10-01', ticker: 'AAA' }),
    row({ date: '2026-10-05', ticker: 'AAA', analysis_dir: 'A_v1' }),
    row({ date: '2026-10-06', ticker: 'AAA', analysis_dir: 'A_v1' }),
  ];
  const now = new Date('2026-11-24T00:00:00Z');
  const ev = buildEval({ ledger, symbols, judgments: [], overrides: {}, now });
  assert.equal(ev.counts.picks, 3);
  assert.equal(ev.short.summary['5'].n, 3);
  assert.equal(ev.counts.evaluated_short, 3);
  assert.equal(ev.generated_at, now.toISOString());
  assert.equal(ev.long.recs.length, 1);
  assert.deepEqual(Object.keys(ev.long.close_reasons), ['달성', '논지 교체', '만기', '진행중']);
  assert.equal(ev.pending.oldest_unjudged_date, null);
});
