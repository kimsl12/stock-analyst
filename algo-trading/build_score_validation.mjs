#!/usr/bin/env node
// build_score_validation.mjs — 스코어카드 정확성 검증
// 분석일 스코어 vs 현재 가격으로 등급별 실제 수익률 산출
// 출력: algo-trading/data/score_validation.json

import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { execSync } from 'child_process';

const ROOT = join(import.meta.dirname, '..');
const OUT = join(import.meta.dirname, 'data');
if (!existsSync(OUT)) mkdirSync(OUT, { recursive: true });

const now = new Date();
const kst = new Date(now.getTime() + 9 * 3600_000);
const timestamp = kst.toISOString().replace('T', ' ').slice(0, 19) + ' KST';
const today = kst.toISOString().slice(0, 10);

// HTML 리포트 파일명에서 분석일 추출
function getReportDates() {
  const dates = {};
  const dir = join(ROOT, 'reports');
  if (!existsSync(dir)) return dates;
  for (const f of readdirSync(dir)) {
    if (!f.endsWith('.html')) continue;
    const m = f.match(/^(.+?)_(\d{8})\.html$/);
    if (!m) continue;
    const ticker = m[1].split('_')[0];
    const d = m[2];
    const dateFmt = `${d.slice(0,4)}-${d.slice(4,6)}-${d.slice(6)}`;
    if (!dates[ticker] || dateFmt > dates[ticker]) dates[ticker] = dateFmt;
  }
  return dates;
}

// 스코어카드에서 스코어 추출 (build_signals.mjs v3 파싱 로직 동일)
function extractScore(content) {
  const lines = content.split('\n');
  for (const line of lines) {
    const pA = line.match(/(?:종합\s*스코어|총점)[:\s]*\*{0,2}(\d+\.?\d*)\s*[/]\s*100/);
    if (pA) return parseFloat(pA[1]);
    const pB = line.match(/합계[:\s]*\*{0,2}(\d+\.?\d*)\s*[/]\s*100/);
    if (pB) return parseFloat(pB[1]);
    if (/\|\s*\*{0,2}합계\*{0,2}\s*\|/.test(line)) {
      const cells = line.split('|').map(c => c.replace(/\*/g, '').trim()).filter(Boolean);
      for (const cell of cells) {
        const ic = cell.match(/^(\d+\.?\d*)\s*\/\s*100/);
        if (ic) return parseFloat(ic[1]);
      }
      for (let i = 1; i < cells.length; i++) {
        const c = cells[i];
        if (c === '100%' || c === '100' || c === '—' || c === '' || /합계/.test(c)) continue;
        const num = parseFloat(c);
        if (!isNaN(num) && num > 0 && num < 100) return num;
      }
    }
    if (/\|\s*\*{0,2}종합\s*스코어\*{0,2}\s*\|/.test(line)) {
      const cells = line.split('|').map(c => c.replace(/\*/g, '').trim()).filter(Boolean);
      for (const cell of cells) {
        const ic = cell.match(/^(\d+\.?\d*)\s*\/\s*100/);
        if (ic) return parseFloat(ic[1]);
      }
      for (let i = 1; i < cells.length; i++) {
        const c = cells[i];
        if (c === '100%' || c === '100' || c === '—' || c === '' || /종합|스코어/.test(c)) continue;
        const num = parseFloat(c);
        if (!isNaN(num) && num > 0 && num < 100) return num;
      }
    }
    const pE = line.match(/스코어\s*(\d+\.?\d*)\s*[/]\s*100/);
    if (pE) return parseFloat(pE[1]);
  }
  return null;
}

// 등급 판정
function gradeFromScore(score) {
  if (score == null) return null;
  if (score >= 80) return 'A';
  if (score >= 65) return 'B';
  if (score >= 50) return 'C';
  if (score >= 35) return 'D';
  return 'F';
}

// 스코어카드에서 진입가 추출
function extractEntryPrice(content) {
  // "매수가", "진입가", "현재가", "buy_price", "entry" 패턴
  const patterns = [
    /(?:추천\s*)?매수가[:\s]*[₩$]?([\d,]+\.?\d*)/,
    /(?:추천\s*)?진입가[:\s]*[₩$]?([\d,]+\.?\d*)/,
    /entry[_\s]*price[:\s]*[₩$]?([\d,]+\.?\d*)/i,
    /현재가[:\s]*[₩$]?([\d,]+\.?\d*)/,
  ];
  for (const p of patterns) {
    const m = content.match(p);
    if (m) return parseFloat(m[1].replace(/,/g, ''));
  }
  return null;
}

// daily_snapshot에서 현재가 추출
function getCurrentPrices() {
  const prices = {};
  const snap = join(ROOT, 'knowledge-base/market/daily_snapshot.md');
  if (!existsSync(snap)) return prices;
  // daily_snapshot에는 주요 지수만 있으므로, 개별 종목은 data.json에서
  return prices;
}

// analysis/{dir}/data.json에서 가격 추출
function getPriceFromData(dir) {
  const dataPath = join(ROOT, 'analysis', dir, 'data.json');
  if (!existsSync(dataPath)) return null;
  try {
    const d = JSON.parse(readFileSync(dataPath, 'utf8'));
    return d.current_price || d.price || d.close || null;
  } catch { return null; }
}

// 메인
function build() {
  const reportDates = getReportDates();
  const analysisDir = join(ROOT, 'analysis');
  const stocks = [];

  for (const dir of readdirSync(analysisDir)) {
    const scPath = join(analysisDir, dir, 'scorecard.md');
    if (!existsSync(scPath)) continue;

    const content = readFileSync(scPath, 'utf8');
    const ticker = dir.split('_')[0];
    const nameParts = dir.split('_');
    const name = nameParts.length > 1 ? nameParts[1] : '';
    const version = dir.match(/v(\d+)/)?.[1] ?? '1';
    const market = /^\d/.test(ticker) ? 'KRX' : 'US';

    const score = extractScore(content);
    const grade = gradeFromScore(score);
    const entryPrice = extractEntryPrice(content);

    // 분석일: scorecard 본문 > HTML 리포트 파일명
    let analysisDate = null;
    const dateM = content.match(/분석일[:\s]*(\d{4}-\d{2}-\d{2})/);
    if (dateM) analysisDate = dateM[1];
    else if (reportDates[ticker]) analysisDate = reportDates[ticker];

    const daysSince = analysisDate
      ? Math.round((new Date(today) - new Date(analysisDate)) / 86400_000)
      : null;

    // 최신 버전만 유지
    const existing = stocks.findIndex(s => s.ticker === ticker);
    const record = {
      ticker, name, version, market, score, grade,
      analysis_date: analysisDate,
      days_since: daysSince,
      entry_price: entryPrice,
      current_price: null,
      return_pct: null,
      direction_correct: null,
      dir,
    };

    if (existing >= 0) {
      if (parseInt(version) > parseInt(stocks[existing].version)) {
        stocks[existing] = record;
      }
    } else {
      stocks.push(record);
    }
  }

  // 등급별 통계
  const gradeStats = { A: { count: 0, returns: [], correct: 0, wrong: 0 },
                       B: { count: 0, returns: [], correct: 0, wrong: 0 },
                       C: { count: 0, returns: [], correct: 0, wrong: 0 },
                       D: { count: 0, returns: [], correct: 0, wrong: 0 },
                       F: { count: 0, returns: [], correct: 0, wrong: 0 } };

  for (const s of stocks) {
    if (s.grade && gradeStats[s.grade]) {
      gradeStats[s.grade].count++;
      if (s.return_pct != null) {
        gradeStats[s.grade].returns.push(s.return_pct);
        if ((s.grade === 'A' || s.grade === 'B') && s.return_pct > 0) gradeStats[s.grade].correct++;
        else if ((s.grade === 'D' || s.grade === 'F') && s.return_pct < 0) gradeStats[s.grade].correct++;
        else gradeStats[s.grade].wrong++;
      }
    }
  }

  // 통계 계산
  const summary = {};
  for (const [grade, stat] of Object.entries(gradeStats)) {
    const avg = stat.returns.length > 0
      ? Math.round(stat.returns.reduce((a, b) => a + b, 0) / stat.returns.length * 100) / 100
      : null;
    const total = stat.correct + stat.wrong;
    summary[grade] = {
      count: stat.count,
      with_returns: stat.returns.length,
      avg_return_pct: avg,
      hit_rate: total > 0 ? Math.round(stat.correct / total * 1000) / 10 : null,
      correct: stat.correct,
      wrong: stat.wrong,
    };
  }

  const result = {
    generated_at: timestamp,
    validation_date: today,
    total_stocks: stocks.length,
    with_score: stocks.filter(s => s.score != null).length,
    with_entry_price: stocks.filter(s => s.entry_price != null).length,
    with_returns: stocks.filter(s => s.return_pct != null).length,
    note: '현재가 데이터 미연동 — 토스 API 또는 yfinance 연동 후 return_pct 산출 가능. 현 단계에서는 스키마와 등급 분포만 생성.',
    grade_distribution: summary,
    grade_expected_behavior: {
      A: '80~100점, Strong Buy — 매수 후 양의 수익률 기대',
      B: '65~79점, Buy — 매수 후 소폭 양의 수익률 기대',
      C: '50~64점, Hold — 보유 유지, 방향성 중립',
      D: '35~49점, Underweight — 비중 축소, 음의 수익률 예상',
      F: '0~34점, Sell — 즉시 청산, 강한 음의 수익률 예상',
    },
    validation_criteria: {
      description: '스코어 등급과 실제 수익률 간 정합성 검증',
      pass_conditions: [
        'A등급 평균 수익률 > B등급 평균 수익률 > C등급 > D등급 > F등급 (단조 감소)',
        'A등급 적중률(양의 수익) >= 70%',
        'A+B등급 적중률 >= 60%',
        'D+F등급 적중률(음의 수익) >= 50%',
      ],
      measurement_periods: ['7일 후', '14일 후', '30일 후', '60일 후', '90일 후'],
    },
    stocks: stocks.sort((a, b) => (b.score ?? 0) - (a.score ?? 0)),
  };

  const outPath = join(OUT, 'score_validation.json');
  writeFileSync(outPath, JSON.stringify(result, null, 2));

  console.log(`OK: score_validation.json`);
  console.log(`  total=${result.total_stocks}, with_score=${result.with_score}, with_entry=${result.with_entry_price}`);
  console.log(`  등급 분포: A=${summary.A.count} B=${summary.B.count} C=${summary.C.count} D=${summary.D.count} F=${summary.F.count}`);
  console.log(`  현재가 미연동 — 토스 API/yfinance 연동 시 return_pct 자동 산출`);
}

build();
