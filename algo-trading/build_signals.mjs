#!/usr/bin/env node
// build_signals.mjs — 알고리즘 매매 엔진용 시그널 JSON 생성
// 출력: algo-trading/data/{macro_regime,stock_scores,earnings_calendar}.json

import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { parseScorecard } from '../web/scripts/lib/scorecard_parser.mjs';

const ROOT = join(import.meta.dirname, '..');
const OUT = join(import.meta.dirname, 'data');
if (!existsSync(OUT)) mkdirSync(OUT, { recursive: true });

const now = new Date();
const kst = new Date(now.getTime() + 9 * 3600_000);
const timestamp = kst.toISOString().replace('T', ' ').slice(0, 19) + ' KST';

// FalseCalm(거짓 안정) 완전정지 히스테리시스 — 원조건(VIX<18·HY<3·PCE>3)이 이 일수만큼
// 연속 충족돼야 halt 확정. 경계(VIX≈18) whipsaw 방지. [2026-08-06 추가]
const FALSECALM_CONFIRM_DAYS = 2;

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

      // 지수형 시리즈는 원값(지수 레벨)이 아니라 전년 대비 %(yoy_pct)를 읽는다.
      // PCEPILFE 원값(~130)을 상승률로 오독 → 레짐이 상시 '물가 높음' 판정된 사고 (2026-07-20).
      const getYoy = (key) => {
        const s = seriesArr.find(x => x.id === key);
        if (!s) return null;
        return s.yoy_pct ?? null;
      };

      const ffr = getValue('DFF') || getValue('FEDFUNDS');
      const t10y = getValue('DGS10');
      const t2y = getValue('DGS2');
      const t10y2y = getValue('T10Y2Y');
      const corePce = getYoy('PCEPILFE');
      const unrate = getValue('UNRATE');
      const hySpread = getValue('BAMLH0A0HYM2');
      const breakeven10y = getValue('T10YIE');
      const gdp = getYoy('GDPC1'); // A191RL1Q225SBEA는 스냅샷에 없음(상시 null) → 실질 GDP YoY로 교체

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

    // 거짓 안정 최종 판정 (히스테리시스 — 원조건이 CONFIRM_DAYS 연속 충족 시에만 halt 확정, 경계 whipsaw 방지) [2026-08-06]
    const rawFalseCalm =
      vix != null && vix < 18 &&
      result.indicators.hy_spread != null && result.indicators.hy_spread < 3 &&
      result.indicators.core_pce_yoy != null && result.indicators.core_pce_yoy > 3;

    // 직전 macro_regime.json 에서 연속 카운터 이어받기 (필드 없으면 콜드스타트: 기존이 FalseCalm 이면 확정으로 시드)
    const todayKst = kst.toISOString().slice(0, 10);
    let prevStreak = 0, prevDate = null;
    try {
      const prevRegime = JSON.parse(readFileSync(join(OUT, 'macro_regime.json'), 'utf8'));
      prevDate = (prevRegime.generated_at || '').slice(0, 10);
      prevStreak = prevRegime.falsecalm_streak != null
        ? prevRegime.falsecalm_streak
        : (prevRegime.regime === 'FalseCalm' ? FALSECALM_CONFIRM_DAYS : 0);
    } catch { /* 최초 실행 — 0 */ }

    let streak;
    if (!rawFalseCalm) streak = 0;
    else if (prevDate === todayKst) streak = prevStreak; // 같은 날 재실행 — 중복 증가 방지
    else streak = prevStreak + 1;
    result.falsecalm_streak = streak;
    result.falsecalm_confirm_days = FALSECALM_CONFIRM_DAYS;

    if (rawFalseCalm && streak >= FALSECALM_CONFIRM_DAYS) {
      result.regime = 'FalseCalm';
      result.regime_kr = '거짓 안정';
      result.confidence = 'high';
      result.favorable_sectors = [];
      result.unfavorable_sectors = ['ALL'];
      result.max_holdings = 0;
      result.position_multiplier = 0;
    } else if (rawFalseCalm) {
      // 원조건 충족이나 미확정 — halt 보류, 기저 레짐 유지 (whipsaw 방지)
      result.falsecalm_pending = true;
      result.falsecalm_pending_note = `거짓 안정 원조건 ${streak}/${FALSECALM_CONFIRM_DAYS}일 연속 — 확정 전, 기저 레짐(${result.regime_kr}) 유지`;
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
  console.log(`OK: macro_regime.json (${result.regime_kr}, max_holdings=${result.max_holdings}, emergency=${result.emergency.active}${result.falsecalm_pending ? `, FalseCalm대기 ${result.falsecalm_streak}/${FALSECALM_CONFIRM_DAYS}일` : ''})`);
  return result;
}

// ============================================================
// 2. 전체 종목 스코어 JSON
// ============================================================
function buildStockScores() {
  // [v2, 2026-06-12] 소스 전면 교체 — 신호가 2026-05-19 에 멈춰 있던 근본 수리.
  // 구버전 문제: ① analysis/ 전 폴더 스캔 + 자체 휴리스틱 점수 추출 (INTC 13 오염)
  //             ② 분석일을 scorecard 본문 "분석일:" 텍스트에서만 찾아 대부분 null
  //                → stale=true → 엔진 신선도 게이트(≤30일)가 전 종목 차단
  //             ③ 비상장(ANTHROPIC/SPACEX) 포함 — 매매 불가 종목이 eligible 에 진입 위험
  // 신버전: analysis/_history/*_timeline.json (재분석 시스템의 단일 진실 — 버전·날짜·점수)
  //         + web/scripts/lib/scorecard_parser.mjs 폴백 (웹 대시보드와 동일 파서, 테스트 13종)
  const UNLISTED = new Set(['ANTHROPIC', 'SPACEX']); // 비상장 — 매매 대상 아님
  const GRADE_LETTER = { '강력매수': 'A', '매수': 'B', '중립': 'C', '보유': 'C', '매도': 'F', '강력매도': 'F' };

  // [v2.1] 섹터 맵 — 엔진의 레짐별 비우호 섹터 차단용 (엔진 요청 2026-06-12).
  // scripts/build_sector_map.py 가 구축 (yfinance GICS → 엔진 11종 + ETF 오버라이드).
  // null = 광범위 인덱스·채권 → 엔진 "중립 통과" (의도).
  let sectorMap = {};
  const sectorPath = join(OUT, 'sector_map.json');
  if (existsSync(sectorPath)) {
    try { sectorMap = JSON.parse(readFileSync(sectorPath, 'utf8')).map ?? {}; } catch {}
  }

  const histDir = join(ROOT, 'analysis', '_history');
  const stocks = [];

  for (const fn of readdirSync(histDir)) {
    if (!fn.endsWith('_timeline.json')) continue;
    let tl;
    try { tl = JSON.parse(readFileSync(join(histDir, fn), 'utf8')); } catch { continue; }
    const ticker = tl.ticker;
    const hist = tl.history || [];
    if (!ticker || hist.length === 0) continue;
    if (UNLISTED.has(String(ticker).toUpperCase())) continue;

    const last = hist[hist.length - 1];
    const dir = last.folder ?? null;
    const name = dir ? (dir.split('_')[1] ?? '') : (tl.name ?? '');
    const version = dir?.match(/_v(\d+)$/)?.[1] ?? String(hist.length);

    let score = last.score ?? null;
    let gradeKr = last.grade ?? null;
    let analysisDate = last.date ?? null;

    // 폴백 — scorecard 본문 파싱 (timeline 미추출분)
    const scPath = last.scorecard_path ? join(ROOT, last.scorecard_path) : null;
    if (scPath && existsSync(scPath) && (score == null || gradeKr == null || analysisDate == null)) {
      const sc = parseScorecard(readFileSync(scPath, 'utf8'));
      score = score ?? sc.score;
      gradeKr = gradeKr ?? sc.grade;
      analysisDate = analysisDate ?? sc.analysis_date;
    }

    const market = /^\d/.test(String(ticker)) ? 'KRX' : 'US';
    const sec = sectorMap[String(ticker)] ?? null;
    stocks.push({
      ticker: String(ticker),
      name,
      version,
      sector: sec?.sector ?? null,
      sector_raw: sec?.sector_raw ?? null,
      score: score != null ? Number(score) : null,
      grade: gradeKr ? (GRADE_LETTER[gradeKr] ?? null) : null,
      grade_kr: gradeKr ?? null,
      analysis_date: analysisDate,
      market,
      dir,
    });
  }

  // 스코어 순 정렬
  stocks.sort((a, b) => (b.score ?? 0) - (a.score ?? 0));

  // stale 판정 (30일+ — 엔진 Gate 1 신선도 기준과 동일)
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
    source: 'analysis/_history timeline + scorecard_parser (v2, 2026-06-12)',
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
