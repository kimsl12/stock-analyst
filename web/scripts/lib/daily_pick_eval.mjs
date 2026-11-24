// daily_pick_eval.mjs — 데일리픽 성적표 채점 코어 (순수 함수)

export const SHORT_HORIZONS = [5, 20];
export const LONG_HORIZONS = [60, 120, 250];
export const BENCH = { US: '^GSPC', KRX: '^KS11' };

const SMALL_SAMPLE_N = 10;
const EXPIRY_BARS = 250; // 장기 만기 거래일
const TP_RANGE = [0.2, 1.8]; // 목표가 유효 범위 (진입가 배수)

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

/** 수익률·초과수익 칸 (%·%p). 벤치 값이 없으면 null */
function perfCell(entryPrice, exitPrice, benchEntry, benchExit) {
  if (benchEntry == null || benchExit == null) return null;
  const ret = (exitPrice / entryPrice - 1) * 100;
  const excess = ret - (benchExit / benchEntry - 1) * 100;
  return { ret, excess, hit: excess > 0 };
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
      h[String(n)] = perfCell(entryPrice, stock.close[j], benchEntry, closeOnOrBefore(bench, stock.dates[j]));
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

// ───────── 장기 리뷰 (추천 묶음·마감) ─────────

/** 가격 기준 마감(달성/만기) — 진입 다음 바부터 탐색, 같은 바면 달성 우선. 없으면 null */
function priceClose(stock, entryIdx, tp) {
  const last = Math.min(entryIdx + EXPIRY_BARS, stock.dates.length - 1);
  for (let i = entryIdx + 1; i <= last; i++) {
    if (tp != null && stock.high[i] >= tp) {
      const price = stock.open[i] >= tp ? stock.open[i] : tp;
      return { reason: '달성', idx: i, date: stock.dates[i], price, bars: i - entryIdx };
    }
    if (i === entryIdx + EXPIRY_BARS) {
      return { reason: '만기', idx: i, date: stock.dates[i], price: stock.close[i], bars: EXPIRY_BARS };
    }
  }
  return null;
}

/** anchor 픽으로 새 추천(내부 상태 포함) 생성. idx: 진입 바 인덱스(-1=미도착), stock=null 이면 가격 없음 */
function newRec(pick, stock, idx) {
  const status = stock == null ? 'no_price' : idx < 0 ? 'pending' : 'ok';
  const entryPrice = status === 'ok' ? stock.close[idx] : null;
  const tp = pick.tp_price ?? null;
  // tp 유효성: null 이거나 진입가×[0.2,1.8] 밖이면 무효 (진입가 미확정이면 판단 보류 → 유효 취급)
  const tpValid = tp != null && (entryPrice == null || (tp >= entryPrice * TP_RANGE[0] && tp <= entryPrice * TP_RANGE[1]));
  return {
    ticker: pick.ticker,
    name: pick.name,
    anchor_date: pick.date,
    anchor_version: pick.version,
    anchor_score: pick.score,
    band: scoreBand(pick.score),
    weight_set: pick.regime?.weight_set ?? null,
    entry_date: status === 'ok' ? stock.dates[idx] : null,
    entry_price: entryPrice,
    tp_price: tp,
    tp_status: tpValid ? 'open' : 'none',
    repicks: [],
    close: null,
    status,
    provisional: false,
    // 내부 상태 (출력 전 제거)
    _dir: pick.analysis_dir,
    _idx: idx,
    _pc: status === 'ok' ? priceClose(stock, idx, tpValid ? tp : null) : null,
  };
}

/** 추천 확정 — 마감·기간 값 계산 후 내부 상태 제거 */
function finalizeRec(rec, stock, bench) {
  const { _dir, _idx, _pc, ...out } = rec;
  // 논지 교체 마감이 없으면 가격 기준 마감 적용
  const close = rec.close ?? _pc;
  out.close = close ? { reason: close.reason, date: close.date, price: close.price, bars: close.bars } : null;
  if (close?.reason === '달성') out.tp_status = 'hit';
  out.h = Object.fromEntries(LONG_HORIZONS.map((n) => [String(n), null]));
  if (rec.status !== 'ok') return out;
  const benchEntry = closeOnOrBefore(bench, rec.entry_date);
  const closeIdx = close ? close.idx : null;
  for (const n of LONG_HORIZONS) {
    const j = _idx + n;
    // 마감 바가 N번째 바 이하면 마감 값 고정, 아니면 N번째 바 종가, 미도달이면 null
    if (closeIdx != null && closeIdx <= j) {
      out.h[String(n)] = perfCell(rec.entry_price, close.price, benchEntry, closeOnOrBefore(bench, close.date));
    } else if (j < stock.dates.length) {
      out.h[String(n)] = perfCell(rec.entry_price, stock.close[j], benchEntry, closeOnOrBefore(bench, stock.dates[j]));
    }
  }
  return out;
}

/**
 * 장기 추천 묶음 — 티커별 픽을 날짜순으로 순회하며 추천(anchor+재픽)으로 묶고 마감을 계산.
 * judgments: 저장된 논지 판정 행, overrides: { "<ticker>@<date>": 판정 }.
 * 반환: recs(anchor_date 오름차순), pending(티커별 가장 이른 미판정 재픽), invalid(anchor 불일치 판정 행)
 */
export function buildRecommendations(ledger, symbols, judgments = [], overrides = {}) {
  const recs = [];
  const pending = [];
  const invalid = [];

  // 티커별 픽 (날짜순)
  const byTicker = new Map();
  for (const r of [...ledger].sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0))) {
    if (!byTicker.has(r.ticker)) byTicker.set(r.ticker, []);
    byTicker.get(r.ticker).push(r);
  }

  for (const [ticker, picks] of byTicker) {
    const stockRaw = symbols[ticker];
    const bench = symbols[BENCH[picks[0].market]];
    // 종목 또는 벤치 시계열이 없으면 가격 없음 — 묶음만 진행
    const stock = isEmpty(stockRaw) || isEmpty(bench) ? null : stockRaw;
    let open = null;
    const done = (rec) => recs.push(finalizeRec(rec, stock, bench));

    for (const pick of picks) {
      const idx = stock ? entryIndex(stock, pick.date) : -1;
      // 가격 기준 마감이 재픽 진입 바 날짜 이하면 이미 마감 (진입 바 미도착이면 마감이 반드시 앞섬)
      if (open?._pc && (idx < 0 || open._pc.date <= stock.dates[idx])) {
        done(open);
        open = null;
      }
      if (!open) {
        open = newRec(pick, stock, idx);
        continue;
      }
      // 열린 추천 중의 재픽인데 진입 바가 아직 없음 → 다음 회차로 미룸 (pending 큐에도 넣지 않음)
      if (stock && idx < 0) break;

      // 판정 결정: override > 같은 analysis_dir 자동 동일 > anchor 일치 판정 행
      let rep = null;
      const ov = overrides[`${ticker}@${pick.date}`];
      if (ov) {
        rep = { verdict: ov, rationale: null, judged_by: 'override' };
      } else if (pick.analysis_dir && pick.analysis_dir === open._dir) {
        rep = { verdict: '동일', rationale: null, judged_by: 'auto-same-version' };
      } else {
        for (const j of judgments) {
          if (j.ticker !== ticker || j.date !== pick.date) continue;
          if (j.anchor_date === open.anchor_date) rep ??= { verdict: j.verdict, rationale: j.rationale ?? null, judged_by: j.judged_by };
          else invalid.push(j); // 옛 anchor 기준 판정 → 무효
        }
      }

      if (!rep) {
        // 미판정 → 묶음 미확정: 이 티커의 이후 픽은 건너뜀
        pending.push({
          ticker, date: pick.date, version: pick.version, analysis_dir: pick.analysis_dir,
          anchor_date: open.anchor_date, anchor_version: open.anchor_version, anchor_analysis_dir: open._dir,
        });
        open.provisional = true;
        break;
      }

      if (rep.verdict === '전환') {
        // 논지 교체 마감 — 전환 픽 진입 바 종가 (가격 없음이면 픽 날짜·가격 null)
        open.close = stock
          ? { reason: '논지 교체', idx, date: stock.dates[idx], price: stock.close[idx], bars: idx - open._idx }
          : { reason: '논지 교체', date: pick.date, price: null, bars: null };
        done(open);
        open = newRec(pick, stock, idx);
      } else {
        open.repicks.push({ date: pick.date, version: pick.version, ...rep });
      }
    }
    if (open) done(open);
  }

  recs.sort((a, b) => (a.anchor_date < b.anchor_date ? -1 : a.anchor_date > b.anchor_date ? 1 : 0));
  pending.sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0));
  return { recs, pending, invalid };
}
