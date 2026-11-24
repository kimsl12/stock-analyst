// daily_pick_ledger.mjs — 데일리픽 원장(append-only 일일 기록) 순수 함수

/** 문자열 안 첫 등급어 — 강력매수 우선, 없으면 null */
export function normalizeGrade(raw) {
  if (typeof raw !== 'string') return null;
  if (raw.includes('강력매수')) return '강력매수';
  if (raw.includes('매수')) return '매수';
  return null;
}

/** payload.pick 이 null 이면 null. regime 은 5개 키만 보존 */
export function ledgerRowFromPick(payload, regime) {
  const p = payload?.pick;
  if (!p) return null;
  // 버전 진실 소스는 analysis_dir (spec §5.2) — 끝 _vN 이 있으면 그것, 없으면 pick.version
  const dirVer = typeof p.analysis_dir === 'string' ? p.analysis_dir.match(/_(v\d+)$/)?.[1] : null;
  return {
    date: payload.pick_date,
    ticker: p.ticker,
    name: p.name,
    market: p.market,
    score: p.score,
    grade: normalizeGrade(p.grade),
    version: dirVer ?? p.version,
    analysis_dir: p.analysis_dir,
    analysis_date: p.analysis_date,
    tp_price: p.tp_price ?? null,
    reasons: p.reasons ?? [],
    regime: regime
      ? {
          risk_regime: regime.risk_regime ?? null,
          weight_set: regime.weight_set ?? null,
          trend: regime.trend ?? null,
          vol_regime: regime.vol_regime ?? null,
          fear_greed: regime.fear_greed ?? null,
        }
      : null,
  };
}

/** 같은 date 행 교체 후 date 오름차순 정렬한 새 배열 */
export function upsertLedgerRow(ledger, row) {
  return [...ledger.filter((r) => r.date !== row.date), row].sort((a, b) =>
    a.date < b.date ? -1 : a.date > b.date ? 1 : 0,
  );
}
