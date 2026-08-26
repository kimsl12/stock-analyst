/**
 * GET /api/price/<ticker> — 실시간 주가 + ATR(14) + 52주 고저 + 시총
 *
 * [v3.41, 2026-08-25] Python(yfinance) → Node 재작성.
 * 배경: yfinance 의존성 + 프로젝트 파일 포함으로 함수 번들 273MB > 225MB 한도
 * → 8/13부터 전 배포 Error (본서버 12일 동결 사고). Node 재작성으로 번들 수 KB.
 *
 * 계약 (구 Python 함수와 동일 — 소비처 DailyPick/compare/timemachine 무수정):
 *   현재가·전일비·ATR14·손절/목표(2·3ATR)·52주 고저·시총·?at= 시간머신·KST fetch_time
 *   한국 6자리 → .KS/.KQ 자동 시도. 오류는 JSON {error} 200 (클라이언트 graceful).
 * 데이터 소스: Yahoo v8 chart API 직접 호출 (yfinance 와 동일 원천, SDK 없이).
 */

const CACHE_TTL = 300; // 5분 (CDN s-maxage 겸용)
const KST_OFFSET_MIN = 9 * 60;

const ALLOWED_ORIGINS = new Set([
  "https://stock-analyst-jungwon1.vercel.app",
  "http://localhost:4321",
  "http://127.0.0.1:4321",
]);

// warm 인스턴스 캐시 + 레이트리밋 (CDN 캐시가 1차 방어, 이건 보조)
const cache = new Map(); // key → {ts, data}
const rate = new Map(); // ip → [timestamps]
const RATE_LIMIT = 60;
const RATE_WINDOW_MS = 60_000;

function rateCheck(ip) {
  const now = Date.now();
  const hist = (rate.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  if (hist.length >= RATE_LIMIT) return false;
  hist.push(now);
  rate.set(ip, hist);
  return true;
}

function resolveSymbols(ticker) {
  const t = String(ticker || "")
    .trim()
    .toUpperCase();
  if (!t) return [];
  if (/^\d{6}$/.test(t)) return [`${t}.KS`, `${t}.KQ`];
  return [t];
}

async function fetchJson(url, timeoutMs = 8000) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const r = await fetch(url, {
      signal: ctrl.signal,
      headers: {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
      },
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } finally {
    clearTimeout(timer);
  }
}

/** Yahoo v8 chart → {bars: [{t,h,l,c,v}], meta} (null 바 제거) */
async function fetchChart(sym, params) {
  const qs = new URLSearchParams({ interval: "1d", ...params }).toString();
  const j = await fetchJson(
    `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(sym)}?${qs}`,
  );
  const result = j?.chart?.result?.[0];
  if (!result) throw new Error(j?.chart?.error?.description || "데이터 없음");
  const ts = result.timestamp || [];
  const q = result.indicators?.quote?.[0] || {};
  const bars = [];
  for (let i = 0; i < ts.length; i++) {
    const c = q.close?.[i];
    if (c == null) continue;
    bars.push({
      t: ts[i],
      h: q.high?.[i] ?? c,
      l: q.low?.[i] ?? c,
      c,
      v: q.volume?.[i] ?? null,
    });
  }
  return { bars, meta: result.meta || {} };
}

function calcAtr(bars, period = 14) {
  if (bars.length < period + 1) return null;
  const trs = [];
  for (let i = 1; i < bars.length; i++) {
    trs.push(
      Math.max(
        bars[i].h - bars[i].l,
        Math.abs(bars[i].h - bars[i - 1].c),
        Math.abs(bars[i].l - bars[i - 1].c),
      ),
    );
  }
  const tail = trs.slice(-period);
  return tail.reduce((a, b) => a + b, 0) / period;
}

function kstIso() {
  const d = new Date(Date.now() + KST_OFFSET_MIN * 60_000);
  return d.toISOString().replace(/\.\d{3}Z$/, "+09:00");
}

function rnd(v, decimals) {
  if (v == null || !Number.isFinite(v)) return null;
  const f = 10 ** decimals;
  return Math.round(v * f) / f;
}

// Yahoo crumb 인증 (quoteSummary 용) — yfinance 와 동일 흐름, warm 인스턴스 1시간 캐시
let crumbCache = null; // {cookie, crumb, ts}
const UA = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)' };

async function getCrumb() {
  if (crumbCache && Date.now() - crumbCache.ts < 3600_000) return crumbCache;
  const r1 = await fetch('https://fc.yahoo.com', { headers: UA, redirect: 'manual' });
  const cookie = (r1.headers.get('set-cookie') || '').split(';')[0];
  if (!cookie) throw new Error('쿠키 없음');
  const r2 = await fetch('https://query1.finance.yahoo.com/v1/test/getcrumb', {
    headers: { ...UA, Cookie: cookie },
  });
  const crumb = (await r2.text()).trim();
  if (!crumb || crumb.includes('<')) throw new Error('crumb 획득 실패');
  crumbCache = { cookie, crumb, ts: Date.now() };
  return crumbCache;
}

async function fetchMarketCap(sym) {
  // 실패 시 null — compare 페이지 graceful (구 Python 함수도 info 실패 시 동일)
  try {
    const { cookie, crumb } = await getCrumb();
    const url = `https://query2.finance.yahoo.com/v10/finance/quoteSummary/${encodeURIComponent(sym)}?modules=price&crumb=${encodeURIComponent(crumb)}`;
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 5000);
    try {
      const r = await fetch(url, { headers: { ...UA, Cookie: cookie }, signal: ctrl.signal });
      const j = await r.json();
      return j?.quoteSummary?.result?.[0]?.price?.marketCap?.raw ?? null;
    } finally {
      clearTimeout(timer);
    }
  } catch {
    crumbCache = null; // 만료 의심 — 다음 호출에서 재발급
    return null;
  }
}

async function fetchPrice(ticker, at) {
  const symbols = resolveSymbols(ticker);
  if (!symbols.length) return { error: "ticker 비어있음", ticker };

  let lastErr = null;
  for (const sym of symbols) {
    try {
      const { bars, meta } = await fetchChart(sym, { range: "1y" });
      if (!bars.length) {
        lastErr = `${sym}: 데이터 없음`;
        continue;
      }

      const recent = bars.slice(-30);
      const latest = recent[recent.length - 1];
      const currentPrice = latest.c;
      const atr = calcAtr(recent, 14);

      const currency = meta.currency || "USD";
      const decimals = currency === "KRW" ? 0 : 2;
      const name = meta.shortName || meta.longName || ticker;
      const market = meta.exchangeName || meta.fullExchangeName || "US";

      const high52 = Math.max(...bars.map((b) => b.h));
      const low52 = Math.min(...bars.map((b) => b.l));
      const prevClose = recent.length >= 2 ? recent[recent.length - 2].c : null;

      // ?at= 시간 머신 — 해당일 종가 + 이후 수익률
      let atPrice = null;
      let returnSinceAt = null;
      if (at && /^\d{4}-\d{2}-\d{2}$/.test(at)) {
        try {
          const p1 = Math.floor(new Date(`${at}T00:00:00Z`).getTime() / 1000);
          const { bars: atBars } = await fetchChart(sym, {
            period1: String(p1),
            period2: String(p1 + 10 * 86400),
          });
          if (atBars.length) {
            atPrice = atBars[0].c;
            returnSinceAt = rnd((currentPrice / atPrice - 1) * 100, 2);
          }
        } catch {
          /* at 실패는 무시 — 본 응답은 유효 */
        }
      }

      return {
        ticker,
        symbol: sym,
        name,
        market,
        currency,
        current_price: rnd(currentPrice, decimals),
        prev_close: prevClose != null ? rnd(prevClose, decimals) : null,
        change_pct: prevClose
          ? rnd((currentPrice / prevClose - 1) * 100, 3)
          : null,
        high_52w: rnd(high52, decimals),
        low_52w: rnd(low52, decimals),
        market_cap: await fetchMarketCap(sym),
        volume: latest.v != null ? Math.round(latest.v) : null,
        atr_14: atr != null ? rnd(atr, decimals) : null,
        atr_pct: atr != null ? rnd((atr / currentPrice) * 100, 3) : null,
        stop_loss_2atr:
          atr != null ? rnd(currentPrice - 2 * atr, decimals) : null,
        target_3atr: atr != null ? rnd(currentPrice + 3 * atr, decimals) : null,
        date: new Date(latest.t * 1000).toISOString().slice(0, 10),
        at: at || null,
        at_price: atPrice != null ? rnd(atPrice, decimals) : null,
        return_since_at_pct: returnSinceAt,
        fetch_time: kstIso(),
        fetch_tz: "Asia/Seoul",
        cache_ttl: CACHE_TTL,
      };
    } catch (e) {
      lastErr = `${sym}: ${e.message || e}`;
    }
  }
  return { error: lastErr || "데이터 없음", ticker, tried: symbols };
}

module.exports = async (req, res) => {
  const origin = req.headers.origin || "";
  const setCors = () => {
    if (ALLOWED_ORIGINS.has(origin)) {
      res.setHeader("Access-Control-Allow-Origin", origin);
      res.setHeader("Vary", "Origin");
    }
  };

  if (req.method === "OPTIONS") {
    setCors();
    res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    res.status(204).end();
    return;
  }

  setCors();
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader(
    "Cache-Control",
    `public, s-maxage=${CACHE_TTL}, stale-while-revalidate=60`,
  );

  const ip =
    String(req.headers["x-forwarded-for"] || "")
      .split(",")[0]
      .trim() || "unknown";
  if (!rateCheck(ip)) {
    res.status(429).json({ error: "rate limit 60/min 초과" });
    return;
  }

  const ticker = String(req.query.ticker || "").trim();
  const at = String(req.query.at || "").trim();
  if (!ticker) {
    res.status(400).json({ error: "ticker 미지정" });
    return;
  }

  const cacheKey = `${ticker.toUpperCase()}|${at}`;
  const hit = cache.get(cacheKey);
  if (hit && Date.now() - hit.ts < CACHE_TTL * 1000) {
    res.status(200).json({ ...hit.data, cached: true });
    return;
  }

  try {
    const data = await fetchPrice(ticker, at);
    if (!data.error) cache.set(cacheKey, { ts: Date.now(), data });
    res.status(200).json({ ...data, cached: false });
  } catch (e) {
    res.status(500).json({ error: `서버 오류: ${e.message || e}`, ticker });
  }
};
