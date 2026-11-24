// daily_pick_eval.mjs — 데일리픽 성적표 채점 코어 (순수 함수)

export const SHORT_HORIZONS = [5, 20];
export const LONG_HORIZONS = [60, 120, 250];
export const BENCH = { US: '^GSPC', KRX: '^KS11' };

const SMALL_SAMPLE_N = 10;

const isEmpty = (s) => !s || !Array.isArray(s.dates) || s.dates.length === 0;

/** 날짜 ≥ date 인 첫 바의 인덱스, 없으면 -1 */
export function entryIndex(series, date) {
  if (isEmpty(series)) return -1;
  return series.dates.findIndex((d) => d >= date);
}

/** 날짜 ≤ date 인 마지막 바의 종가, 없으면 null */
export function closeOnOrBefore(series, date) {
  if (isEmpty(series)) return null;
  let v = null;
  for (let i = 0; i < series.dates.length; i++) {
    if (series.dates[i] <= date) v = series.close[i];
    else break;
  }
  return v;
}

/** 점수대 라벨 (<78 / 78≤s<81 / ≥81) */
export function scoreBand(score) {
  if (score >= 81) return '81+';
  if (score >= 78) return '78-80';
  return '75-77';
}

/** 단기 채점 행 생성 — 진입 바 종가 기준, N바 뒤 종가 vs 벤치마크 */
export function buildShortRows(ledger, symbols) {
  return ledger.map((r) => {
    const stock = symbols[r.ticker];
    const bench = symbols[BENCH[r.market]];
    const h = Object.fromEntries(SHORT_HORIZONS.map((n) => [String(n), null]));
    const base = {
      date: r.date,
      ticker: r.ticker,
      name: r.name,
      score: r.score,
      band: scoreBand(r.score),
      weight_set: r.regime?.weight_set ?? null,
      entry_date: null,
      entry_price: null,
      h,
    };
    if (isEmpty(stock) || isEmpty(bench)) return { ...base, status: 'no_price' };
    const idx = entryIndex(stock, r.date);
    if (idx < 0) return { ...base, status: 'pending' };

    const entryDate = stock.dates[idx];
    const entryPrice = stock.close[idx];
    const benchEntry = closeOnOrBefore(bench, entryDate);
    for (const n of SHORT_HORIZONS) {
      const j = idx + n;
      if (j >= stock.dates.length) continue;
      const evalDate = stock.dates[j];
      const benchEval = closeOnOrBefore(bench, evalDate);
      if (benchEntry == null || benchEval == null) continue;
      const ret = (stock.close[j] / entryPrice - 1) * 100;
      const excess = ret - (benchEval / benchEntry - 1) * 100;
      h[String(n)] = { ret, excess, hit: excess > 0 };
    }
    return { ...base, status: 'ok', entry_date: entryDate, entry_price: entryPrice };
  });
}

/** rows[i].h[key] 가 null 이 아닌 것만 집계. hit_rate 는 0~1, 평균은 % */
export function summarize(rows, key) {
  const cells = rows.map((r) => r.h?.[key]).filter((c) => c != null);
  const n = cells.length;
  if (n === 0) return { n: 0, hit_rate: null, avg_return: null, avg_excess: null, small_sample: true };
  const mean = (f) => cells.reduce((a, c) => a + f(c), 0) / n;
  return {
    n,
    hit_rate: cells.filter((c) => c.hit).length / n,
    avg_return: mean((c) => c.ret),
    avg_excess: mean((c) => c.excess),
    small_sample: n < SMALL_SAMPLE_N,
  };
}
