#!/usr/bin/env node
// build_signals.mjs — 알고리즘 매매 엔진용 시그널 JSON 생성
// 출력: algo-trading/data/{macro_regime,stock_scores,earnings_calendar}.json

import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const ROOT = join(import.meta.dirname, '..');
const OUT = join(import.meta.dirname, 'data');
if (!existsSync(OUT)) mkdirSync(OUT, { recursive: true });

const now = new Date();
const kst = new Date(now.getTime() + 9 * 3600_000);
const timestamp = kst.toISOString().replace('T', ' ').slice(0, 19) + ' KST';

// ============================================================
// 1. 매크로 레짐 판정
// ============================================================
function buildMacroRegime() {
  const result = {
    generated_at: timestamp,
    regime: 'Unknown',
    regime_kr: '판정 불가',
    confidence: 'low',
    indicators: {},
    emergency: { active: false, triggers: [] },
    favorable_sectors: [],
    unfavorable_sectors: [],
    max_holdings: 5,
    position_multiplier: 1.0,
  };

  // FRED 데이터
  const fredPath = join(ROOT, 'knowledge-base/macro/fred_snapshot.json');
  if (existsSync(fredPath)) {
    try {
      const fred = JSON.parse(readFileSync(fredPath, 'utf8'));
      const seriesArr = fred.series || [];

      const getValue = (key) => {
        const s = seriesArr.find(x => x.id === key);
        if (!s) return null;
        return s.value ?? null;
      };

      const ffr = getValue('DFF') || getValue('FEDFUNDS');
      const t10y = getValue('DGS10');
      const t2y = getValue('DGS2');
      const t10y2y = getValue('T10Y2Y');
      const corePce = getValue('PCEPILFE');
      const unrate = getValue('UNRATE');
      const hySpread = getValue('BAMLH0A0HYM2');
      const breakeven10y = getValue('T10YIE');
      const gdp = getValue('A191RL1Q225SBEA');

      result.indicators = {
        fed_funds_rate: ffr,
        us_10y: t10y,
        us_2y: t2y,
        t10y2y_spread: t10y2y,
        core_pce_yoy: corePce,
        unemployment: unrate,
        hy_spread: hySpread,
        breakeven_10y: breakeven10y,
        gdp_yoy: gdp,
        fred_date: fred.updated_at || null,
      };

      // 레짐 판정
      const gdpOk = gdp != null && gdp >= 2;
      const inflHigh = corePce != null && corePce > 2.5;
      const yieldNormal = t10y2y != null && t10y2y > 0;

      if (gdpOk && !inflHigh && yieldNormal) {
        result.regime = 'Goldilocks';
        result.regime_kr = '골디락스';
        result.confidence = 'high';
        result.favorable_sectors = ['Tech', 'Discretionary', 'Financials'];
        result.unfavorable_sectors = ['Utilities', 'Staples'];
        result.max_holdings = 7;
        result.position_multiplier = 1.2;
      } else if (gdpOk && inflHigh) {
        result.regime = 'Reflation';
        result.regime_kr = '리플레이션';
        result.confidence = 'high';
        result.favorable_sectors = ['Energy', 'Materials', 'Industrials'];
        result.unfavorable_sectors = ['Tech', 'REIT'];
        result.max_holdings = 5;
        result.position_multiplier = 1.1;
      } else if (!gdpOk && inflHigh) {
        result.regime = 'Stagflation';
        result.regime_kr = '스태그플레이션';
        result.confidence = 'high';
        result.favorable_sectors = ['Energy', 'Gold', 'Healthcare'];
        result.unfavorable_sectors = ['Tech', 'Discretionary', 'Financials'];
        result.max_holdings = 3;
        result.position_multiplier = 0.7;
      }

      // 거짓 안정 체크
      if (corePce != null && corePce > 3 && hySpread != null && hySpread < 3) {
        // VIX는 daily_snapshot에서 확인
      }
    } catch (e) {
      console.warn('WARN: FRED 파싱 실패:', e.message);
    }
  }

  // daily_snapshot에서 VIX, USD/KRW 추출
  const snapPath = join(ROOT, 'knowledge-base/market/daily_snapshot.md');
  if (existsSync(snapPath)) {
    const snap = readFileSync(snapPath, 'utf8');

    const vixMatch = snap.match(/VIX\s*\|\s*([\d.]+)/);
    const krwMatch = snap.match(/USD\/KRW\s*\|\s*([\d,.]+)/);

    const vix = vixMatch ? parseFloat(vixMatch[1]) : null;
    const usdkrw = krwMatch ? parseFloat(krwMatch[1].replace(/,/g, '')) : null;

    result.indicators.vix = vix;
    result.indicators.usd_krw = usdkrw;

    // 거짓 안정 최종 판정
    if (vix != null && vix < 18 &&
        result.indicators.hy_spread != null && result.indicators.hy_spread < 3 &&
        result.indicators.core_pce_yoy != null && result.indicators.core_pce_yoy > 3) {
      result.regime = 'FalseCalm';
      result.regime_kr = '거짓 안정';
      result.confidence = 'high';
      result.favorable_sectors = [];
      result.unfavorable_sectors = ['ALL'];
      result.max_holdings = 0;
      result.position_multiplier = 0;
    }

    // 긴급 트리거
    if (vix != null && vix >= 25) {
      result.emergency.active = true;
      result.emergency.triggers.push({ type: 'VIX_25', value: vix, action: 'trailing_tighten_1x_atr' });
    }
    if (vix != null && vix >= 30) {
      result.emergency.triggers.push({ type: 'VIX_30', value: vix, action: 'value_positions_tighten' });
    }
    if (usdkrw != null && usdkrw >= 1550) {
      result.emergency.active = true;
      result.emergency.triggers.push({ type: 'USDKRW_1550', value: usdkrw, action: 'kr_stocks_full_exit_review' });
    }
    if (usdkrw != null && usdkrw >= 1600) {
      result.emergency.triggers.push({ type: 'USDKRW_1600', value: usdkrw, action: 'value_kr_exit_review' });
    }
  }

  // F&G
  const fgPath = join(ROOT, 'knowledge-base/market/fear_greed.json');
  if (existsSync(fgPath)) {
    try {
      const fg = JSON.parse(readFileSync(fgPath, 'utf8'));
      result.indicators.fear_greed_cnn = fg.cnn?.value ?? null;
      result.indicators.fear_greed_crypto = fg.crypto?.value ?? null;
    } catch {}
  }

  const outPath = join(OUT, 'macro_regime.json');
  writeFileSync(outPath, JSON.stringify(result, null, 2));
  console.log(`OK: macro_regime.json (${result.regime_kr}, max_holdings=${result.max_holdings}, emergency=${result.emergency.active})`);
  return result;
}

// ============================================================
// 2. 전체 종목 스코어 JSON
// ============================================================
function buildStockScores() {
  const analysisDir = join(ROOT, 'analysis');
  const stocks = [];

  for (const dir of readdirSync(analysisDir)) {
    const scPath = join(analysisDir, dir, 'scorecard.md');
    if (!existsSync(scPath)) continue;

    const content = readFileSync(scPath, 'utf8');

    // 티커 추출
    const ticker = dir.split('_')[0];
    const nameParts = dir.split('_');
    const name = nameParts.length > 1 ? nameParts[1] : '';
    const version = dir.match(/v(\d+)/)?.[1] ?? '1';

    // 스코어 추출 (정밀 파싱 v3)
    let score = null;
    const lines = content.split('\n');
    for (const line of lines) {
      // 패턴 A: "종합 스코어: 85 / 100" 또는 "종합 스코어: **85 / 100**"
      const pA = line.match(/(?:종합\s*스코어|총점)[:\s]*\*{0,2}(\d+\.?\d*)\s*[/]\s*100/);
      if (pA) { score = parseFloat(pA[1]); break; }

      // 패턴 B: "### 합계: **83.9 / 100**"
      const pB = line.match(/합계[:\s]*\*{0,2}(\d+\.?\d*)\s*[/]\s*100/);
      if (pB) { score = parseFloat(pB[1]); break; }

      // 패턴 C: 표 행 "| **합계** | **100%** | — | **78.5** |"
      if (/\|\s*\*{0,2}합계\*{0,2}\s*\|/.test(line)) {
        const cells = line.split('|').map(c => c.replace(/\*/g, '').trim()).filter(Boolean);
        // "X / 100" 패턴이 셀 안에 있으면 그걸 우선
        for (const cell of cells) {
          const inCell = cell.match(/^(\d+\.?\d*)\s*\/\s*100/);
          if (inCell) { score = parseFloat(inCell[1]); break; }
        }
        if (score) break;
        // 없으면: 100, 100%, —, 빈값, 합계 건너뛰고 소수점 있는 숫자 찾기
        for (let i = 1; i < cells.length; i++) {
          const c = cells[i];
          if (c === '100%' || c === '100' || c === '—' || c === '' || /합계/.test(c)) continue;
          // "85" 같은 정수도 허용하되, 가중치(100)와 구분 위해 소수점 있거나 <100이면
          const num = parseFloat(c);
          if (!isNaN(num) && num > 0 && num < 100) { score = num; break; }
          // 정확히 "강력매수", "매수" 등 텍스트면 건너뜀
          if (/매수|매도|보유|Buy|Sell|Hold|등급/i.test(c)) continue;
        }
        if (score) break;
      }

      // 패턴 D: "| **종합 스코어** | **76.35** | **73.50** |" — v2 비교표
      if (/\|\s*\*{0,2}종합\s*스코어\*{0,2}\s*\|/.test(line)) {
        const cells = line.split('|').map(c => c.replace(/\*/g, '').trim()).filter(Boolean);
        // "X / 100" 패턴 우선
        for (const cell of cells) {
          const inCell = cell.match(/^(\d+\.?\d*)\s*\/\s*100/);
          if (inCell) { score = parseFloat(inCell[1]); break; }
        }
        if (score) break;
        for (let i = 1; i < cells.length; i++) {
          const c = cells[i];
          if (c === '100%' || c === '100' || c === '—' || c === '' || /종합|스코어/.test(c)) continue;
          const num = parseFloat(c);
          if (!isNaN(num) && num > 0 && num < 100) { score = num; break; }
        }
        if (score) break;
      }

      // 패턴 E: "스코어 85.0/100" 또는 "85/100점"
      const pE = line.match(/스코어\s*(\d+\.?\d*)\s*[/]\s*100/);
      if (pE) { score = parseFloat(pE[1]); break; }
    }

    // 등급 추출
    const gradeMap = {
      'Strong Buy': 'A', '강력매수': 'A',
      'Buy': 'B', '매수': 'B',
      'Hold': 'C', '보유': 'C',
      'Underweight': 'D', '비중축소': 'D',
      'Sell': 'F', '매도': 'F',
    };
    const gradeMatch = content.match(/(Strong Buy|Buy|Hold|Underweight|Sell|강력매수|매수|보유|비중축소|매도)/);
    const gradeRaw = gradeMatch ? gradeMatch[1] : null;
    const grade = gradeRaw ? (gradeMap[gradeRaw] || gradeRaw) : null;

    // 분석일 추출
    const dateMatch = content.match(/분석일[:\s]*(\d{4}-\d{2}-\d{2})/);
    const analysisDate = dateMatch ? dateMatch[1] : null;

    // 시장 판별 (숫자로 시작 = KRX)
    const market = /^\d/.test(ticker) ? 'KRX' : 'US';

    // 중복 제거: 같은 티커의 최신 버전만
    const existing = stocks.findIndex(s => s.ticker === ticker);
    if (existing >= 0) {
      if (parseInt(version) > parseInt(stocks[existing].version)) {
        stocks[existing] = { ticker, name, version, score, grade, analysis_date: analysisDate, market, dir };
      }
    } else {
      stocks.push({ ticker, name, version, score, grade, analysis_date: analysisDate, market, dir });
    }
  }

  // 스코어 순 정렬
  stocks.sort((a, b) => (b.score ?? 0) - (a.score ?? 0));

  // stale 판정 (30일+)
  const today = kst.toISOString().slice(0, 10);
  for (const s of stocks) {
    if (s.analysis_date) {
      const diff = (new Date(today) - new Date(s.analysis_date)) / 86400_000;
      s.days_since_analysis = Math.round(diff);
      s.stale = diff > 30;
    } else {
      s.days_since_analysis = null;
      s.stale = true;
    }
  }

  const result = {
    generated_at: timestamp,
    total_count: stocks.length,
    eligible_count: stocks.filter(s => (s.score ?? 0) >= 80 && !s.stale).length,
    kr_eligible_count: stocks.filter(s => (s.score ?? 0) >= 80 && !s.stale && s.market === 'KRX').length,
    stocks,
  };

  const outPath = join(OUT, 'stock_scores.json');
  writeFileSync(outPath, JSON.stringify(result, null, 2));
  console.log(`OK: stock_scores.json (total=${result.total_count}, eligible=${result.eligible_count}, kr_eligible=${result.kr_eligible_count})`);
  return result;
}

// ============================================================
// 3. 실적 캘린더 JSON
// ============================================================
function buildEarningsCalendar() {
  const calPath = join(ROOT, 'knowledge-base/market/economic_calendar.md');
  const events = [];

  if (existsSync(calPath)) {
    const content = readFileSync(calPath, 'utf8');
    // 실적 관련 라인 추출 (earnings, 실적, Q1, Q2 등)
    const lines = content.split('\n');
    for (const line of lines) {
      if (/실적|earnings|Q[1-4]|분기/i.test(line) && /\d{1,2}\/\d{1,2}|\d{4}-\d{2}-\d{2}/.test(line)) {
        const dateMatch = line.match(/(\d{4}-\d{2}-\d{2})|(\d{1,2})\/(\d{1,2})/);
        const tickerMatch = line.match(/([A-Z]{1,5})\b/);
        if (dateMatch || tickerMatch) {
          events.push({
            raw: line.trim().replace(/^\||\|$/g, '').trim(),
            date: dateMatch ? (dateMatch[1] || `2026-${dateMatch[2]?.padStart(2,'0')}-${dateMatch[3]?.padStart(2,'0')}`) : null,
            ticker: tickerMatch ? tickerMatch[1] : null,
          });
        }
      }
    }
  }

  const result = {
    generated_at: timestamp,
    event_count: events.length,
    events,
  };

  const outPath = join(OUT, 'earnings_calendar.json');
  writeFileSync(outPath, JSON.stringify(result, null, 2));
  console.log(`OK: earnings_calendar.json (${events.length} events)`);
  return result;
}

// ============================================================
// 4. Polymarket 급변 트리거
// ============================================================
function buildPolymarketAlerts() {
  const pmPath = join(ROOT, 'knowledge-base/market/prediction_markets.md');
  const prevPath = join(OUT, 'polymarket_prev.json');
  const result = {
    generated_at: timestamp,
    alerts: [],
    threshold_pct: 15,
    market_count: 0,
  };

  if (!existsSync(pmPath)) {
    const outPath = join(OUT, 'polymarket_alerts.json');
    writeFileSync(outPath, JSON.stringify(result, null, 2));
    console.log('OK: polymarket_alerts.json (prediction_markets.md 미존재 — 빈 출력)');
    return result;
  }

  const content = readFileSync(pmPath, 'utf8');

  // 테이블에서 질문 + 확률 추출 (| 질문 | 확률% | 형태)
  const current = {};
  const tableRows = content.match(/\|[^|]+\|\s*\d+\.?\d*%/g) || [];
  for (const row of tableRows) {
    const cells = row.split('|').map(c => c.trim()).filter(Boolean);
    if (cells.length >= 2) {
      const question = cells[0];
      const pctMatch = cells[1].match(/([\d.]+)%/);
      if (pctMatch && question.length > 5) {
        current[question] = parseFloat(pctMatch[1]);
      }
    }
  }
  result.market_count = Object.keys(current).length;

  // 이전 수집분과 비교
  let prev = {};
  if (existsSync(prevPath)) {
    try { prev = JSON.parse(readFileSync(prevPath, 'utf8')); } catch {}
  }

  for (const [question, pct] of Object.entries(current)) {
    if (prev[question] != null) {
      const delta = pct - prev[question];
      if (Math.abs(delta) >= result.threshold_pct) {
        result.alerts.push({
          question,
          prev_pct: prev[question],
          current_pct: pct,
          delta_pct: Math.round(delta * 10) / 10,
          direction: delta > 0 ? 'UP' : 'DOWN',
          action: 'REGIME_RECHECK',
          severity: Math.abs(delta) >= 25 ? 'critical' : 'warning',
        });
      }
    }
  }

  // 현재값을 다음 비교용으로 저장
  writeFileSync(prevPath, JSON.stringify(current, null, 2));

  const outPath = join(OUT, 'polymarket_alerts.json');
  writeFileSync(outPath, JSON.stringify(result, null, 2));

  const alertCount = result.alerts.length;
  console.log(`OK: polymarket_alerts.json (markets=${result.market_count}, alerts=${alertCount}${alertCount > 0 ? ' — REGIME_RECHECK 필요' : ''})`);
  return result;
}

// ============================================================
// 5. 스코어 변동 감지
// ============================================================
function buildScoreChanges(currentScores) {
  const prevPath = join(OUT, 'stock_scores_prev.json');
  const result = {
    generated_at: timestamp,
    changes: [],
    upgrades: [],
    downgrades: [],
    new_eligible: [],
    lost_eligible: [],
  };

  if (!existsSync(prevPath) || !currentScores) {
    // 첫 실행: 현재를 prev로 저장
    if (currentScores) {
      const prevData = {};
      for (const s of currentScores.stocks) {
        prevData[s.ticker] = { score: s.score, grade: s.grade, stale: s.stale };
      }
      writeFileSync(prevPath, JSON.stringify(prevData, null, 2));
    }
    const outPath = join(OUT, 'score_changes.json');
    writeFileSync(outPath, JSON.stringify(result, null, 2));
    console.log('OK: score_changes.json (첫 실행 — 기준선 저장)');
    return result;
  }

  let prev = {};
  try { prev = JSON.parse(readFileSync(prevPath, 'utf8')); } catch {}

  const gradeRank = { 'A': 5, 'B': 4, 'C': 3, 'D': 2, 'F': 1 };

  for (const s of currentScores.stocks) {
    const p = prev[s.ticker];
    if (!p) continue;

    const scoreDelta = (s.score ?? 0) - (p.score ?? 0);
    const prevRank = gradeRank[p.grade] ?? 0;
    const currRank = gradeRank[s.grade] ?? 0;
    const gradeChanged = p.grade !== s.grade;

    if (Math.abs(scoreDelta) >= 5 || gradeChanged) {
      const change = {
        ticker: s.ticker,
        name: s.name,
        market: s.market,
        prev_score: p.score,
        current_score: s.score,
        score_delta: Math.round(scoreDelta * 10) / 10,
        prev_grade: p.grade,
        current_grade: s.grade,
        direction: scoreDelta > 0 ? 'UP' : 'DOWN',
      };
      result.changes.push(change);

      if (currRank > prevRank) result.upgrades.push(change);
      if (currRank < prevRank) result.downgrades.push(change);
    }

    // eligible 변동 (80점 경계 진입/이탈)
    const wasEligible = (p.score ?? 0) >= 80 && !p.stale;
    const isEligible = (s.score ?? 0) >= 80 && !s.stale;
    if (!wasEligible && isEligible) result.new_eligible.push(s.ticker);
    if (wasEligible && !isEligible) result.lost_eligible.push(s.ticker);
  }

  // 현재를 prev로 갱신
  const prevData = {};
  for (const s of currentScores.stocks) {
    prevData[s.ticker] = { score: s.score, grade: s.grade, stale: s.stale };
  }
  writeFileSync(prevPath, JSON.stringify(prevData, null, 2));

  const outPath = join(OUT, 'score_changes.json');
  writeFileSync(outPath, JSON.stringify(result, null, 2));

  const up = result.upgrades.length;
  const down = result.downgrades.length;
  const newE = result.new_eligible.length;
  const lostE = result.lost_eligible.length;
  console.log(`OK: score_changes.json (upgrades=${up}, downgrades=${down}, new_eligible=${newE}, lost_eligible=${lostE})`);
  return result;
}

// ============================================================
// 실행
// ============================================================
console.log('=== algo-trading signal build ===');
buildMacroRegime();
const scores = buildStockScores();
buildEarningsCalendar();
buildPolymarketAlerts();
buildScoreChanges(scores);
console.log('=== done ===');
