/**
 * stop_ratchet.mjs — 보유 종목 손절가 래칫 (순수 함수, build_holdings_health.mjs 전용).
 *
 * 스코어카드 손절가는 "현재가 − 2×ATR" 산식이라 주가가 빠지면 재분석 때마다 함께 내려간다
 * → 손절 알림이 영영 울리지 않을 수 있다. 보유 중에는 손절가를 올리기만 한다:
 *   유효 손절가 = max(직전 유효 손절가, 신규 산출 손절가)
 *
 * 상태 형식: { [ticker]: { stop, set_at, source_v } }
 */

/** 직전값이 신규값의 이 배수를 넘으면 단위 아티팩트(액면분할·통화 단위 오류) 의심 → 래칫하지 않음 */
export const UNIT_GUARD_RATIO = 3;

function validStop(x) {
  return typeof x === 'number' && Number.isFinite(x) && x > 0;
}

/**
 * 래칫 판정 (종목 1건).
 * @param {number|null} prevStop 직전 유효 손절가
 * @param {number|null} rawStop  최신 스코어카드 산출 손절가
 * @returns {{stop: number|null, ratcheted: boolean, guard: boolean}}
 *   ratcheted = 직전값 유지(신규값 미채택) / guard = 3배 가드 발동(신규값 채택)
 */
export function ratchetStop(prevStop, rawStop) {
  const hasPrev = validStop(prevStop);
  const hasRaw = validStop(rawStop);
  if (!hasPrev) return { stop: hasRaw ? rawStop : null, ratcheted: false, guard: false };
  if (!hasRaw) return { stop: prevStop, ratcheted: true, guard: false };
  if (prevStop > rawStop * UNIT_GUARD_RATIO) return { stop: rawStop, ratcheted: false, guard: true };
  if (prevStop > rawStop) return { stop: prevStop, ratcheted: true, guard: false };
  return { stop: rawStop, ratcheted: false, guard: false };
}

/**
 * 보유 목록 전체에 래칫 적용 — analysis.stop_loss / stop_loss_raw / stop_ratcheted 를 in-place 갱신.
 * @param {Array<{ticker: string, analysis: object|null}>} holdings analysis.stop_loss = 신규 산출값
 * @param {object} state 직전 상태
 * @returns {{state: object, warnings: string[]}} 새 상태 — 보유 목록에 없는 티커는 제거
 *   (재매수 시 옛 고점 손절가로 오알림 방지)
 */
export function applyStopRatchet(holdings, state) {
  const next = {};
  const warnings = [];
  for (const h of holdings) {
    const prev = state?.[h.ticker] ?? null;
    const a = h.analysis;
    if (!a) {
      if (prev) next[h.ticker] = prev;
      continue;
    }
    const raw = a.stop_loss ?? null;
    const r = ratchetStop(prev?.stop ?? null, raw);
    if (r.guard) {
      warnings.push(
        `${h.ticker}: 직전 손절가 ${prev.stop} > 신규 ${raw} × ${UNIT_GUARD_RATIO} — 단위 아티팩트 의심, 래칫 미적용(신규값 채택)`,
      );
    }
    a.stop_loss = r.stop;
    a.stop_loss_raw = raw;
    a.stop_ratcheted = r.ratcheted;
    if (r.ratcheted || (r.stop != null && prev?.stop === r.stop)) {
      next[h.ticker] = prev;
    } else if (r.stop != null) {
      next[h.ticker] = { stop: r.stop, set_at: a.date ?? null, source_v: a.v ?? null };
    }
  }
  return { state: next, warnings };
}

/** 상태 파일이 없을 때 — 기존 holdings_health.json 의 손절가로 시드. */
export function seedRatchetState(health) {
  const state = {};
  for (const h of health?.holdings ?? []) {
    const a = h.analysis;
    if (a && validStop(a.stop_loss)) {
      state[h.ticker] = { stop: a.stop_loss, set_at: a.date ?? null, source_v: a.v ?? null };
    }
  }
  return state;
}
