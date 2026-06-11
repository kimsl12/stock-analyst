import test from 'node:test';
import assert from 'node:assert/strict';
import {
  parseScore,
  parseGrade,
  parseStopLoss,
  parseTargetPrice,
  parseScorecard,
} from '../lib/scorecard_parser.mjs';

// ── 개별주 형식 (NVDA v5 실물 발췌) ──────────────────────
const STOCK_MD = `# NVIDIA (NVDA) — 종합 스코어카드

분석일: 2026-06-06 | 현재가: $206.41 | 시가총액: $5.00조

| 밸류에이션 | 6 | 12% | 0.72 | 선행 PER ~28~30x 합리적이나 정점 가정 의존, 상방 +8% |
| **종합**   | — | 100% | **7.59** | **→ 75.9 / 100** |

**종합점수: 76 / 100**

## 2. 투자등급

### 매수 (Buy)

**근거**: 목표가 대비 상방이 +8%로 제한적

## 3. ATR 기반 손절가 / 목표가

| 손절가 (2 ATR)      | **$189.47**  | -8.2%       |
| 12M 펀더멘털 목표가 | **$223**     | +8.0%       |

- **목표가**: $223 (12M, +8.0%) | **신뢰구간** $183~$263
- **손절**: $189.47 (-8.2%) | **단기목표**: $231.82 (+12.3%)
`;

// ── ETF 형식 (VOO/VIG 실물 발췌) ─────────────────────────
const ETF_MD = `# VOO 스코어카드

- **종합 점수**: 72/100
- **투자 등급**: 매수

매수 진입 시 손절 참고선은 2ATR 기준 약 $229.8, 1차 목표는 3ATR 기준 약 $238.5.

- **목표가 범위**: USD620 ~ USD745 (중심 USD690, ±9%)
  - **Bull case**: 목표가 USD745
  - **Base case**: 목표가 USD690
  - **Bear case**: 목표가 USD620
`;

test('개별주: 종합점수 76 추출', () => {
  assert.equal(parseScore(STOCK_MD), 76);
});

test('개별주: 투자등급 헤딩(### 매수 (Buy)) → 매수', () => {
  assert.equal(parseGrade(STOCK_MD), '매수');
});

test('개별주: 손절가 표 행 $189.47', () => {
  assert.equal(parseStopLoss(STOCK_MD), 189.47);
});

test('개별주: 12M 펀더멘털 목표가 $223 — 산문 "+8%"에 오염되지 않음 (timeline 버그 회귀 테스트)', () => {
  assert.equal(parseTargetPrice(STOCK_MD), 223);
});

test('ETF: 종합 점수 72 + 투자 등급 매수', () => {
  assert.equal(parseScore(ETF_MD), 72);
  assert.equal(parseGrade(ETF_MD), '매수');
});

test('ETF: 산문 손절 참고선 $229.8', () => {
  assert.equal(parseStopLoss(ETF_MD), 229.8);
});

test('ETF: Base case 목표가 USD690 우선 (Bull 745 아님)', () => {
  assert.equal(parseTargetPrice(ETF_MD), 690);
});

test('빈 문서: 전부 null (throw 금지)', () => {
  const r = parseScorecard('# 빈 스코어카드');
  assert.equal(r.score, null);
  assert.equal(r.grade, null);
  assert.equal(r.stop_loss, null);
  assert.equal(r.target_price, null);
});

test('통화 기호 없는 숫자는 손절/목표가로 채택 안 함', () => {
  const md = '손절 기준은 8% 하락이다. 목표가 대비 상방이 +8%로 제한적.';
  assert.equal(parseStopLoss(md), null);
  assert.equal(parseTargetPrice(md), null);
});

test('parseScorecard: 분석일 추출', () => {
  assert.equal(parseScorecard(STOCK_MD).analysis_date, '2026-06-06');
});
