// daily_pick_extract.test.mjs — build_daily_pick.mjs 의 extractScorecardMeta 회귀 테스트
// 2026-06-15: 신형 압축 스코어카드(BLIND 재분석 v6) 가격·이유 추출 실패로 DailyPick 카드가
// 깨지던 사고(META current_price/buy_price/reasons null) + 통화기호 누락으로 "현재가 60%"(비중)를
// 가격으로 오캡처하던 사고(TSM $424 → 60) 방어.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { extractScorecardMeta } from '../build_daily_pick.mjs';

test('신형 압축 카드($ 산문) — current_price/buy_price/reasons 채워짐 (META v6)', () => {
  const md = `# 메타 (META) — 스코어카드 (BLIND v6)
## 종합 평가
- **종합 점수**: 80/100
- **투자 등급**: 매수
- **카테고리**: 글로벌 1위 소셜 광고 플랫폼
## 투자 전략
장기 투자자에게 현 $588 부근은 합리적 분할매수 구간으로 판단된다. 압도적 광고 수익성을 감안하면 상향여력이 크다. 2단계 ATR 손절선($550) 이탈 시 비중 조절을 권한다.
## § Confidence Interval (95% CI)
- **목표가 범위**: USD520 ~ USD800 (중심 USD660, ±22%)
`;
  const m = extractScorecardMeta(md);
  assert.equal(m.current_price, 588);
  assert.equal(m.buy_price, 588); // current_price 폴백
  assert.equal(m.tp_price, 660);
  assert.ok(m.reasons.length >= 2, '투자 전략 산문에서 이유 추출');
  assert.ok(m.reasons[0].includes('588'));
});

test('신형 압축 카드(달러 접미사) — current_price 추출 (AVGO/GOOGL 형식)', () => {
  const md = `## 투자 전략
현재가 394.69달러는 컨센서스 중심값(약 500달러)을 하회해 진입 매력이 있다. 380~395달러 구간에서 1차 진입한다.
`;
  const m = extractScorecardMeta(md);
  assert.equal(m.current_price, 394.69);
});

test('"현재가 60%"(비중) 를 가격으로 오캡처하지 않음 — 통화기호 필수 (TSM 사고)', () => {
  const md = `| 현재가 | $424.04 (ADR) |
## 전략
분할매수: 현재가 60% + 2×ATR 눌림 시 40%.
`;
  const m = extractScorecardMeta(md);
  assert.equal(m.current_price, 424.04, '표의 $424.04 를 잡아야지 산문 60% 가 아님');
});

test('현재가 라인 없는 카드 — current_price null (LLY 콘텐츠 갭, 크래시 아님)', () => {
  const md = `## 투자 전략
장기 핵심 보유 종목으로 적합하다. 1,080달러(2 ATR 손절선) 부근 조정 시 비중 확대. 컨센서스 1,250달러를 1차 목표로 둔다.
`;
  const m = extractScorecardMeta(md);
  assert.equal(m.current_price, null);
  assert.equal(m.buy_price, null);
  assert.ok(m.reasons.length >= 1, '투자 전략에서 이유는 추출됨');
});

test('구형 카드(현재가 $205.19) — 정상 동작 회귀 방어 (NVDA 형식)', () => {
  const md = `| 항목 | 값 |
| 현재가 | $205.19 |
| 손절가 (2 ATR) | **$189.47** |
## 7. 핵심 결론
- 데이터센터 수요 견조
- 마진 방어력 우수
## 8. 리스크
- 경쟁 심화
`;
  const m = extractScorecardMeta(md);
  assert.equal(m.current_price, 205.19);
  assert.equal(m.stop_price, 189.47);
  assert.equal(m.reasons.length, 2);
});

test('한국 종목(원 접미사) — current_price 추출', () => {
  const md = `| 현재가 | 322,500원 |
## 투자 전략
반도체 업황 회복 기대.
`;
  const m = extractScorecardMeta(md);
  assert.equal(m.current_price, 322500);
});
