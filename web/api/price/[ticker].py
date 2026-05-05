"""
GET /api/price/<ticker> — 실시간 주가 + ATR(14) + 52주 고저 + 시총

설계:
- yfinance 단독 사용 (Vercel us-region에서 KRX 직접 접근 불가 → 한국 종목은 .KS/.KQ 자동 시도)
- in-memory TTL 캐시 (5분) — 동일 인스턴스 내 hit 시 ~50ms
- Rate limit 60/분 per-IP (단순 sliding window, in-memory)
- CORS: 자체 origin + localhost:4321 (dev)
- graceful: 데이터 없거나 yfinance 오류 시 JSON {"error": ...} 200 (클라이언트가 처리)

매개변수:
- path 변수 ticker (Vercel `[ticker].py` 자동 매핑)
- 또는 ?ticker= query (보조)
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import time
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────────────────
# CORS allow-list
# ─────────────────────────────────────────────────────────────────────────
ALLOWED_ORIGINS = {
    'https://stock-analyst-jungwon1.vercel.app',
    'http://localhost:4321',
    'http://127.0.0.1:4321',
}

# ─────────────────────────────────────────────────────────────────────────
# In-memory TTL cache (per warm instance)
# ─────────────────────────────────────────────────────────────────────────
_CACHE_TTL = 300  # 5분
_cache: dict[str, tuple[float, dict]] = {}

def _cache_get(key: str):
    rec = _cache.get(key)
    if not rec:
        return None
    ts, data = rec
    if time.time() - ts > _CACHE_TTL:
        _cache.pop(key, None)
        return None
    return data

def _cache_set(key: str, data: dict):
    _cache[key] = (time.time(), data)

# ─────────────────────────────────────────────────────────────────────────
# Rate limit (60 req/min per IP, sliding window)
# ─────────────────────────────────────────────────────────────────────────
_RATE_LIMIT = 60
_RATE_WINDOW = 60.0
_rate: dict[str, list[float]] = {}

def _rate_check(ip: str) -> bool:
    now = time.time()
    history = _rate.get(ip, [])
    history = [t for t in history if now - t < _RATE_WINDOW]
    if len(history) >= _RATE_LIMIT:
        return False
    history.append(now)
    _rate[ip] = history
    return True

# ─────────────────────────────────────────────────────────────────────────
# Ticker → yfinance symbol resolver
# ─────────────────────────────────────────────────────────────────────────
def _resolve_symbols(ticker: str) -> list[str]:
    """티커를 yfinance 심볼 후보 목록으로 변환. 한국 6자리 → .KS, .KQ 시도."""
    t = ticker.strip().upper()
    if not t:
        return []
    if t.isdigit() and len(t) == 6:
        return [f'{t}.KS', f'{t}.KQ']
    return [t]

# ─────────────────────────────────────────────────────────────────────────
# ATR(14) 계산
# ─────────────────────────────────────────────────────────────────────────
def _calc_atr(hist, period: int = 14):
    if len(hist) < period + 1:
        return None
    highs = hist['High'].values
    lows = hist['Low'].values
    closes = hist['Close'].values
    trs = []
    for i in range(1, len(hist)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    if len(trs) < period:
        return None
    return sum(trs[-period:]) / period

# ─────────────────────────────────────────────────────────────────────────
# 핵심: yfinance fetch
# ─────────────────────────────────────────────────────────────────────────
def fetch_price(ticker: str) -> dict:
    import yfinance as yf

    symbols = _resolve_symbols(ticker)
    if not symbols:
        return {'error': 'ticker 비어있음', 'ticker': ticker}

    last_err = None
    for sym in symbols:
        try:
            stock = yf.Ticker(sym)
            hist = stock.history(period='3mo')
            if hist.empty:
                last_err = f'{sym}: 데이터 없음'
                continue

            hist = hist.tail(30)
            latest = hist.iloc[-1]
            current_price = round(float(latest['Close']), 4)

            atr = _calc_atr(hist, period=14)
            info = {}
            try:
                info = stock.info or {}
            except Exception:
                info = {}

            currency = info.get('currency', 'USD')
            name = info.get('shortName') or info.get('longName') or ticker
            market = info.get('exchange') or 'US'

            hist_52w = stock.history(period='1y')
            high_52w = round(float(hist_52w['High'].max()), 4) if not hist_52w.empty else None
            low_52w = round(float(hist_52w['Low'].min()), 4) if not hist_52w.empty else None

            prev_close = round(float(hist.iloc[-2]['Close']), 4) if len(hist) >= 2 else None
            change_pct = round((current_price / prev_close - 1) * 100, 3) if prev_close else None

            decimals = 0 if currency == 'KRW' else 2
            return {
                'ticker': ticker,
                'symbol': sym,
                'name': name,
                'market': market,
                'currency': currency,
                'current_price': round(current_price, decimals),
                'prev_close': round(prev_close, decimals) if prev_close else None,
                'change_pct': change_pct,
                'high_52w': round(high_52w, decimals) if high_52w else None,
                'low_52w': round(low_52w, decimals) if low_52w else None,
                'market_cap': info.get('marketCap'),
                'volume': int(latest['Volume']) if latest.get('Volume') else None,
                'atr_14': round(atr, decimals) if atr else None,
                'atr_pct': round(atr / current_price * 100, 3) if atr else None,
                'stop_loss_2atr': round(current_price - 2 * atr, decimals) if atr else None,
                'target_3atr': round(current_price + 3 * atr, decimals) if atr else None,
                'date': hist.index[-1].strftime('%Y-%m-%d'),
                'fetch_time': datetime.utcnow().isoformat() + 'Z',
                'cache_ttl': _CACHE_TTL,
            }
        except Exception as e:
            last_err = f'{sym}: {e}'
            continue

    return {'error': last_err or '데이터 없음', 'ticker': ticker, 'tried': symbols}

# ─────────────────────────────────────────────────────────────────────────
# Vercel handler
# ─────────────────────────────────────────────────────────────────────────
class handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, body: dict, origin: str = ''):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', f'public, s-maxage={_CACHE_TTL}, stale-while-revalidate=60')
        if origin and origin in ALLOWED_ORIGINS:
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Vary', 'Origin')
        self.end_headers()
        self.wfile.write(json.dumps(body, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        origin = self.headers.get('Origin', '')
        self.send_response(204)
        if origin in ALLOWED_ORIGINS:
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Vary', 'Origin')
        self.end_headers()

    def do_GET(self):
        origin = self.headers.get('Origin', '')

        # Rate limit
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0].strip()
        if not _rate_check(ip):
            self._send_json(429, {'error': 'rate limit 60/min 초과'}, origin)
            return

        # ticker 추출 (path 변수 → query 보조)
        parsed = urlparse(self.path)
        # /api/price/AAPL → 마지막 segment
        path_segs = [s for s in parsed.path.split('/') if s]
        ticker = path_segs[-1] if path_segs else ''
        # path가 [ticker] 그대로 오는 경우 query fallback
        if ticker.startswith('[') or not ticker or ticker == 'price':
            qs = parse_qs(parsed.query)
            ticker = (qs.get('ticker') or [''])[0]

        if not ticker:
            self._send_json(400, {'error': 'ticker 미지정'}, origin)
            return

        # 캐시 hit
        cache_key = ticker.upper()
        cached = _cache_get(cache_key)
        if cached:
            self._send_json(200, {**cached, 'cached': True}, origin)
            return

        # fetch
        try:
            data = fetch_price(ticker)
            if 'error' not in data:
                _cache_set(cache_key, data)
            self._send_json(200, {**data, 'cached': False}, origin)
        except Exception as e:
            self._send_json(500, {'error': f'서버 오류: {e}', 'ticker': ticker}, origin)
