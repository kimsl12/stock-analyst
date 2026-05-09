// portfolio_parser 단위 테스트 — Node 20+ built-in test runner
// 실행: node --test scripts/__tests__/portfolio_parser.test.mjs
// prebuild 에 통합되어 있어 npm run build 시 자동 실행됨.
// 실패하면 빌드 차단 → silent drift 사전 감지.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  cleanMoney,
  cleanPct,
  cleanQty,
  stripBold,
  splitRow,
  findTableAfter,
  extractCurrentSection,
  parseProfile,
  parseHoldings,
  parseTotals,
  validateParsed,
  extractFrontmatter,
  checkSchemaContract,
} from '../lib/portfolio_parser.mjs';

// ────────────────────────────────────────────────────────────────────────
// 셀 파싱 유틸
// ────────────────────────────────────────────────────────────────────────
test('stripBold: ** 마크다운 굵게 제거', () => {
  assert.equal(stripBold('**+10.7%**'), '+10.7%');
  assert.equal(stripBold('plain'), 'plain');
  assert.equal(stripBold(null), '');
});

test('cleanMoney: $, ,, 원, 공백 제거', () => {
  assert.equal(cleanMoney('$1,337.21'), 1337.21);
  assert.equal(cleanMoney('$13,788.91'), 13788.91);
  assert.equal(cleanMoney('1,460.08원'), 1460.08);
  assert.equal(cleanMoney('—'), null);
  assert.equal(cleanMoney(''), null);
});

test('cleanQty: 주, , 제거', () => {
  assert.equal(cleanQty('20.469743주'), 20.469743);
  assert.equal(cleanQty('3주'), 3);
  assert.equal(cleanQty('—'), null);
});

test('cleanPct: 단순 % 형식', () => {
  assert.equal(cleanPct('67.7%'), 67.7);
  assert.equal(cleanPct('-1.2%'), -1.2);
  assert.equal(cleanPct('+10.7%'), 10.7);
});

test('cleanPct: dual-info "+10.7% (+$1,337.21)" 형식 — 첫 % 숫자만 추출 (2026-05-09 사고 회귀 테스트)', () => {
  assert.equal(cleanPct('**+10.7%** (+$1,337.21)'), 10.7);
  assert.equal(cleanPct('+0.7% (+$2.87)'), 0.7);
  assert.equal(cleanPct('-0.0% (-$0.02)'), 0);
  assert.equal(cleanPct('-1.2% (-$12.30)'), -1.2);
  assert.equal(cleanPct('**+14.6%** (+$111.34)'), 14.6);
});

// ────────────────────────────────────────────────────────────────────────
// 표 파서
// ────────────────────────────────────────────────────────────────────────
test('splitRow: pipe 구분 + 양끝 trim', () => {
  assert.deepEqual(splitRow('| a | b | c |'), ['a', 'b', 'c']);
  assert.deepEqual(splitRow('|a|b|'), ['a', 'b']);
});

test('findTableAfter: 제목 다음 첫 표 추출', () => {
  const lines = [
    '### 투자자 프로파일',
    '',
    '| 항목 | 값 |',
    '|---|---|',
    '| 기간 | 5년 |',
    '| 성향 | 배당형 |',
    '',
    '### 다음섹션',
  ];
  const t = findTableAfter(lines, /^###\s+투자자/);
  assert.deepEqual(t.header, ['항목', '값']);
  assert.equal(t.rows.length, 2);
  assert.deepEqual(t.rows[0], ['기간', '5년']);
});

// ────────────────────────────────────────────────────────────────────────
// fixture: 9컬럼 (현재 v3.16+)
// ────────────────────────────────────────────────────────────────────────
const FIXTURE_9COL = `
## ★ CURRENT ★

### 투자자 프로파일

| 항목 | 값 |
|------|-----|
| 투자 성향 | **배당형 (Dividend Income)** |
| 총 투자 가능 금액 | **매월 200만원 (적립식)** |
| 투자 기간 | **5년+ (장기)** |
| 등록일 | 2026-04-13 |

### 보유 종목 — 토스증권

| 티커 | 종목명 | 유형 | 시장 | 보유 수량 | 현재가 (USD) | 평가금 (USD) | 비중 | 수익률 |
|------|-------|------|------|----------|-----------|-----------|------|--------|
| VOO | Vanguard S&P 500 | ETF | NYSE | 20.469743주 | $672.54 | $13,788.91 | 67.7% | **+10.7%** (+$1,337.21) |
| GLD | SPDR Gold Shares | ETF | NYSE | 4.001475주 | $431.68 | $1,733.76 | 8.5% | **+3.4%** (+$57.78) |
| AGG | iShares Core US Agg Bond | ETF | NYSE | 3주 | $98.95 | $296.40 | 1.5% | -0.0% (-$0.02) |

### 포트폴리오 총액 (2026-05-09 기준)

| 항목 | 금액 (USD) | 비중 |
|------|----------|------|
| 해외주식 | $18,017.89 | 88.49% |
| **총액** | **$15,819.07** | **100%** |

환율 기준: USD/KRW = **1,460.08원**

---
`;

test('parseHoldings: 9컬럼 파싱 — VOO weight=67.7%, return=10.7%, price=$672.54', () => {
  const lines = extractCurrentSection(FIXTURE_9COL).split(/\r?\n/);
  const holdings = parseHoldings(lines);
  assert.equal(holdings.length, 3);
  const voo = holdings.find((h) => h.ticker === 'VOO');
  assert.equal(voo.weight_pct, 67.7);
  assert.equal(voo.return_pct, 10.7);
  assert.equal(voo.current_price, 672.54);
  assert.equal(voo.current_value_usd, 13788.91);
  assert.equal(voo.asset_type, 'ETF');
});

test('parseTotals: 총액 + 환율 추출', () => {
  const lines = extractCurrentSection(FIXTURE_9COL).split(/\r?\n/);
  const t = parseTotals(lines);
  assert.equal(t.total_value_usd, 15819.07);
  assert.equal(t.exchange_rate, 1460.08);
});

test('parseProfile: ** 굵게 제거 + 키-값 추출', () => {
  const lines = extractCurrentSection(FIXTURE_9COL).split(/\r?\n/);
  const p = parseProfile(lines);
  assert.equal(p['투자 성향'], '배당형 (Dividend Income)');
  assert.equal(p['투자 기간'], '5년+ (장기)');
});

// ────────────────────────────────────────────────────────────────────────
// fixture: 8컬럼 legacy (현재가 컬럼 없음, 4/29 까지 형식)
// ────────────────────────────────────────────────────────────────────────
const FIXTURE_8COL = `
## ★ CURRENT ★

### 투자자 프로파일

| 항목 | 값 |
|------|-----|
| 투자 성향 | **중립 (Balanced)** |
| 투자 기간 | **5년+** |
| 등록일 | 2026-04-13 |

### 보유 종목 — 토스증권

| 티커 | 종목명 | 유형 | 시장 | 보유 수량 | 평가금 (USD) | 비중 | 수익률 |
|------|-------|------|------|----------|-----------|------|--------|
| VOO | Vanguard S&P 500 | ETF | NYSE | 24.469743주 | $14,500.00 | 75.0% | **+8.0%** (+$1,000) |
| GLD | SPDR Gold Shares | ETF | NYSE | 4주 | $1,700.00 | 9.0% | **+2.5%** (+$40) |

### 포트폴리오 총액

| 항목 | 금액 (USD) | 비중 |
|------|----------|------|
| **총액** | **$19,300.00** | **100%** |

환율 기준: USD/KRW = **1,440.00원**

---
`;

test('parseHoldings: 8컬럼 legacy 호환 — 현재가는 평가금/수량 으로 역산', () => {
  const lines = extractCurrentSection(FIXTURE_8COL).split(/\r?\n/);
  const holdings = parseHoldings(lines);
  assert.equal(holdings.length, 2);
  const voo = holdings.find((h) => h.ticker === 'VOO');
  assert.equal(voo.weight_pct, 75.0);
  assert.equal(voo.return_pct, 8.0);
  // current_price = current_value_usd / quantity (8컬럼은 현재가 직접 컬럼 없음)
  assert.ok(Math.abs(voo.current_price - 14500 / 24.469743) < 0.01);
});

// ────────────────────────────────────────────────────────────────────────
// fixture: 컬럼 시프트 시나리오 — sync_portfolio 가 이를 차단해야 함
// ────────────────────────────────────────────────────────────────────────
test('parseHoldings: 컬럼 7개(부족) 표 — row 가 < 8 이면 skip → 결과 0건', () => {
  const broken = `
## ★ CURRENT ★
### 투자자 프로파일
| 항목 | 값 |
|---|---|
| 성향 | 배당형 |
| 기간 | 5년 |
| 등록일 | 2026-04-13 |
### 보유 종목
| 티커 | 종목명 | 유형 | 시장 | 수량 | 비중 | 수익률 |
|---|---|---|---|---|---|---|
| VOO | Vanguard | ETF | NYSE | 20주 | 75.0% | 10.0% |
### 포트폴리오 총액
| 항목 | 금액 |
|---|---|
| 총액 | $19,000 |
---
`;
  const lines = extractCurrentSection(broken).split(/\r?\n/);
  // 7컬럼은 < 8 이라 throw (parseHoldings 의 ncol < 8 가드)
  assert.throws(() => parseHoldings(lines), /컬럼 수/);
});

// ────────────────────────────────────────────────────────────────────────
// validateParsed — 검증 게이트 회귀 테스트
// ────────────────────────────────────────────────────────────────────────
test('validateParsed: 정상 9컬럼 데이터 → failures 0건', () => {
  const lines = extractCurrentSection(FIXTURE_9COL).split(/\r?\n/);
  const parsed = {
    profile: parseProfile(lines),
    holdings: parseHoldings(lines),
    ...parseTotals(lines),
  };
  const failures = validateParsed(parsed);
  assert.equal(failures.length, 0, `예상: 0건, 실제: ${JSON.stringify(failures)}`);
});

test('validateParsed: weight_pct 모두 NULL 시나리오 → "추출률" 검증 실패 (2026-05-09 사고 시뮬레이션)', () => {
  const parsed = {
    profile: { 성향: '배당형', 기간: '5년', 금액: '200만원' },
    total_value_usd: 20000,
    holdings: [
      { ticker: 'VOO', asset_type: 'ETF', weight_pct: null, return_pct: 67.7 },
      { ticker: 'GLD', asset_type: 'ETF', weight_pct: null, return_pct: 8.5 },
    ],
  };
  const failures = validateParsed(parsed);
  assert.ok(failures.some((f) => /weight_pct 추출률/.test(f)), `예상: weight_pct 실패, 실제: ${JSON.stringify(failures)}`);
});

test('validateParsed: 비중 합계 200% 시나리오 → 비중 합계 검증 실패', () => {
  const parsed = {
    profile: { 성향: '배당형', 기간: '5년', 금액: '200만원' },
    total_value_usd: 20000,
    holdings: [
      { ticker: 'VOO', asset_type: 'ETF', weight_pct: 100, return_pct: 10 },
      { ticker: 'GLD', asset_type: 'ETF', weight_pct: 100, return_pct: 5 },
    ],
  };
  const failures = validateParsed(parsed);
  assert.ok(failures.some((f) => /비중 합계/.test(f)), `예상: 비중 합계 실패, 실제: ${JSON.stringify(failures)}`);
});

test('validateParsed: holdings 0건 → "0건" 검증 실패', () => {
  const parsed = {
    profile: { 성향: '배당형', 기간: '5년', 금액: '200만원' },
    total_value_usd: 20000,
    holdings: [{ ticker: '원화현금', asset_type: 'CASH', weight_pct: 100 }],
  };
  const failures = validateParsed(parsed);
  assert.ok(failures.some((f) => /0건/.test(f)));
});

// ────────────────────────────────────────────────────────────────────────
// schema contract — frontmatter ↔ 표 헤더 일치 검증 (P1-4)
// ────────────────────────────────────────────────────────────────────────
test('extractFrontmatter: 배열 + 단순 키-값 파싱', () => {
  const md = `---
updated: 2026-05-09
schema_version: 9col-v3.16
holdings_table_columns: [티커, 종목명, 유형, 시장, 보유 수량, 현재가, 평가금, 비중, 수익률]
---
# 본문
`;
  const fm = extractFrontmatter(md);
  assert.equal(fm.updated, '2026-05-09');
  assert.equal(fm.schema_version, '9col-v3.16');
  assert.ok(Array.isArray(fm.holdings_table_columns));
  assert.equal(fm.holdings_table_columns.length, 9);
  assert.equal(fm.holdings_table_columns[5], '현재가');
});

test('checkSchemaContract: 정상 9컬럼 frontmatter ↔ 표 일치 → null', () => {
  const md = `---
holdings_table_columns: [티커, 종목명, 유형, 시장, 보유 수량, 현재가, 평가금, 비중, 수익률]
---
${FIXTURE_9COL}`;
  const err = checkSchemaContract(md);
  assert.equal(err, null, `예상: null, 실제: ${err}`);
});

test('checkSchemaContract: 컬럼 수 불일치 (8 vs 9) 감지', () => {
  // frontmatter 는 9컬럼인데 실제 표는 8컬럼 (사고 시나리오)
  const md = `---
holdings_table_columns: [티커, 종목명, 유형, 시장, 보유 수량, 현재가, 평가금, 비중, 수익률]
---
${FIXTURE_8COL}`;
  const err = checkSchemaContract(md);
  assert.ok(err && /컬럼 수 불일치/.test(err), `예상: 컬럼 수 불일치, 실제: ${err}`);
});

test('checkSchemaContract: frontmatter 누락 시 graceful (null)', () => {
  const md = `---
updated: 2026-05-09
---
${FIXTURE_9COL}`;
  const err = checkSchemaContract(md);
  assert.equal(err, null);
});

test('validateParsed: total_value_usd null → 실패', () => {
  const parsed = {
    profile: { 성향: '배당형', 기간: '5년', 금액: '200만원' },
    total_value_usd: null,
    holdings: [
      { ticker: 'VOO', asset_type: 'ETF', weight_pct: 67.7, return_pct: 10.7 },
      { ticker: 'GLD', asset_type: 'ETF', weight_pct: 8.5, return_pct: 3.4 },
    ],
  };
  const failures = validateParsed(parsed);
  assert.ok(failures.some((f) => /total_value_usd null/.test(f)));
});
