// stop_ratchet.test.mjs — 보유 종목 손절가 래칫 단위 테스트
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { ratchetStop, applyStopRatchet, seedRatchetState } from '../lib/stop_ratchet.mjs';

const holding = (ticker, stop, v = 2, date = '2026-11-20') => ({
  ticker,
  analysis: { v, date, stop_loss: stop, stop_loss_raw: null, stop_ratcheted: false },
});

test('ratchetStop — 신규값이 높으면 상향 반영', () => {
  assert.deepEqual(ratchetStop(100, 110), { stop: 110, ratcheted: false, guard: false });
  assert.deepEqual(ratchetStop(100, 100), { stop: 100, ratcheted: false, guard: false });
});

test('ratchetStop — 신규값이 낮으면 무시하고 직전값 유지', () => {
  assert.deepEqual(ratchetStop(100, 90), { stop: 100, ratcheted: true, guard: false });
});

test('ratchetStop — 직전값이 신규값의 3배 초과면 래칫 미적용 (단위 아티팩트 가드)', () => {
  assert.deepEqual(ratchetStop(400, 100), { stop: 100, ratcheted: false, guard: true });
  // 정확히 3배는 가드 아님 (초과만)
  assert.deepEqual(ratchetStop(300, 100), { stop: 300, ratcheted: true, guard: false });
});

test('ratchetStop — 직전값 없음 / 신규값 없음', () => {
  assert.deepEqual(ratchetStop(null, 90), { stop: 90, ratcheted: false, guard: false });
  assert.deepEqual(ratchetStop(100, null), { stop: 100, ratcheted: true, guard: false });
  assert.deepEqual(ratchetStop(null, null), { stop: null, ratcheted: false, guard: false });
});

test('applyStopRatchet — 필드 기록 + 상태 갱신 (상향은 교체, 하향은 직전 상태 유지)', () => {
  const state = {
    UP: { stop: 100, set_at: '2026-11-01', source_v: 1 },
    DOWN: { stop: 100, set_at: '2026-11-01', source_v: 1 },
  };
  const holdings = [holding('UP', 110), holding('DOWN', 90), holding('NEW', 50)];
  const { state: next, warnings } = applyStopRatchet(holdings, state);

  assert.deepEqual(warnings, []);
  const [up, down, fresh] = holdings.map((h) => h.analysis);
  assert.deepEqual([up.stop_loss, up.stop_loss_raw, up.stop_ratcheted], [110, 110, false]);
  assert.deepEqual([down.stop_loss, down.stop_loss_raw, down.stop_ratcheted], [100, 90, true]);
  assert.deepEqual([fresh.stop_loss, fresh.stop_loss_raw, fresh.stop_ratcheted], [50, 50, false]);

  assert.deepEqual(next.UP, { stop: 110, set_at: '2026-11-20', source_v: 2 });
  assert.deepEqual(next.DOWN, { stop: 100, set_at: '2026-11-01', source_v: 1 });
  assert.deepEqual(next.NEW, { stop: 50, set_at: '2026-11-20', source_v: 2 });
});

test('applyStopRatchet — 보유 목록에서 빠진 종목은 상태에서 제거', () => {
  const state = {
    HELD: { stop: 100, set_at: '2026-11-01', source_v: 1 },
    SOLD: { stop: 500, set_at: '2026-10-01', source_v: 3 },
  };
  const { state: next } = applyStopRatchet([holding('HELD', 95)], state);
  assert.deepEqual(Object.keys(next), ['HELD']);
});

test('applyStopRatchet — 3배 가드 발동 시 신규값 채택 + 경고 + 상태 교체', () => {
  const state = { SPLIT: { stop: 400, set_at: '2026-11-01', source_v: 1 } };
  const holdings = [holding('SPLIT', 100)];
  const { state: next, warnings } = applyStopRatchet(holdings, state);
  assert.equal(holdings[0].analysis.stop_loss, 100);
  assert.equal(holdings[0].analysis.stop_ratcheted, false);
  assert.equal(warnings.length, 1);
  assert.match(warnings[0], /SPLIT/);
  assert.deepEqual(next.SPLIT, { stop: 100, set_at: '2026-11-20', source_v: 2 });
});

test('applyStopRatchet — 신규 산출값 없음(파싱 실패)이면 직전 유효 손절가 유지 / 분석 없음은 상태 보존', () => {
  const state = {
    NOSTOP: { stop: 100, set_at: '2026-11-01', source_v: 1 },
    NOANALYSIS: { stop: 70, set_at: '2026-11-01', source_v: 1 },
  };
  const holdings = [holding('NOSTOP', null), { ticker: 'NOANALYSIS', analysis: null }];
  const { state: next } = applyStopRatchet(holdings, state);
  const a = holdings[0].analysis;
  assert.deepEqual([a.stop_loss, a.stop_loss_raw, a.stop_ratcheted], [100, null, true]);
  assert.deepEqual(next, state);
});

test('applyStopRatchet — 같은 값 재실행은 멱등 (상태의 set_at·source_v 불변)', () => {
  const state = { SAME: { stop: 100, set_at: '2026-11-01', source_v: 1 } };
  const { state: next } = applyStopRatchet([holding('SAME', 100, 5, '2026-11-25')], state);
  assert.deepEqual(next, state);
});

test('seedRatchetState — 기존 holdings_health.json 의 유효 손절가만 시드', () => {
  const health = {
    holdings: [
      { ticker: 'A', analysis: { v: 3, date: '2026-11-10', stop_loss: 12.5 } },
      { ticker: 'B', analysis: { v: 1, date: '2026-11-11', stop_loss: null } },
      { ticker: 'C', analysis: null },
    ],
  };
  assert.deepEqual(seedRatchetState(health), { A: { stop: 12.5, set_at: '2026-11-10', source_v: 3 } });
  assert.deepEqual(seedRatchetState(null), {});
});
