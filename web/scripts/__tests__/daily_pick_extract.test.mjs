// daily_pick_extract.test.mjs — build_daily_pick.mjs 의 extractScorecardMeta 회귀 테스트
// 2026-06-15: 신형 압축 스코어카드(BLIND 재분석 v6) 가격·이유 추출 실패로 DailyPick 카드가
// 깨지던 사고(META current_price/buy_price/reasons null) + 통화기호 누락으로 "현재가 60%"(비중)를
// 가격으로 오캡처하던 사고(TSM $424 → 60) 방어.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  extractScorecardMeta,
  extractReasonsFromReportData,
  shortenReason,
  resolveReportUrl,
} from '../build_daily_pick.mjs';

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

// ---------------------------------------------------------------------------
// [v3.40, 2026-11-19] _report_data.json 기반 추천 이유 — BLIND 스코어카드에 논지 섹션이 없어
// reasons=[] → 위젯 "분석 본문 참조"만 표시되던 문제. + 리포트 링크 404 (버전 포함 파일명 조립).
// ---------------------------------------------------------------------------
const LLY = {
  thesis: {
    claim:
      "GLP-1 듀오폴리 리더로서 매출 +38.6%·영업마진 50%+·저베타 0.39 방어력을 갖춰 독립 '매수'. 다만 고금리·리스크오프 레짐의 멀티플 압박으로 상단 제약, 목표가 $1,450.",
    consensus: '29인 애널리스트 매수.',
    variant: '본 분석은 고금리 멀티플 압박을 반영해 컨센서스 중앙값보다 보수적인 $1,450을 제시.',
  },
  executive_summary:
    '일라이릴리는 GLP-1 듀오폴리 리더로서 매출 +38.6% YoY, 영업마진 51.3%의 엘리트급 펀더멘털을 유지한다. 포워드 PE 27.3x·PEG 1.31은 성장 감안 시 과하지 않다. 종합 74/100, 등급 \'매수\'.',
};

test('dict thesis — claim 핵심 문장 → ES(중복 제외) → "다만" 단서 마지막', () => {
  const r = extractReasonsFromReportData(LLY);
  assert.equal(r.length, 3);
  assert.ok(r[0].startsWith('GLP-1 듀오폴리 리더'));
  assert.ok(r[1].includes('PEG 1.31'), 'claim 과 수치(38.6%) 겹치는 ES 1문장은 건너뜀');
  assert.ok(r[2].startsWith('다만'), '단서는 마지막');
  assert.ok(!r.some((x) => /종합\s*74/.test(x)), '종합 점수 메타 문장 제외');
});

test('string thesis (드리프트) — 문자열 자체를 claim 으로 사용', () => {
  const r = extractReasonsFromReportData({
    thesis: '품질 대비 저평가된 AI 인프라 핵심 독점. 종합 77점·목표가 $445(+23%) 매수, 단 리스크오프로 분할 접근.',
  });
  assert.deepEqual(r, ['품질 대비 저평가된 AI 인프라 핵심 독점.', '단 리스크오프로 분할 접근.']);
});

test('필드 누락/이상 타입 — 크래시 없이 빈 배열 또는 폴백', () => {
  assert.deepEqual(extractReasonsFromReportData(null), []);
  assert.deepEqual(extractReasonsFromReportData({}), []);
  assert.deepEqual(extractReasonsFromReportData({ thesis: { claim: 42 }, executive_summary: null }), []);
  // claim 없음 → executive_summary(배열) 폴백, 마크다운 제거
  const r = extractReasonsFromReportData({
    executive_summary: ['**세계 1위** 파운드리로 첨단공정을 사실상 독점한다.', '`ROE 41.9%` 로 최상위 수익성을 유지한다.'],
  });
  assert.deepEqual(r, ['세계 1위 파운드리로 첨단공정을 사실상 독점한다.', 'ROE 41.9% 로 최상위 수익성을 유지한다.']);
  // 단서만 있는 경우 근거 없이 단서만 내보내지 않음
  assert.deepEqual(extractReasonsFromReportData({ thesis: { claim: '다만 밸류에이션 부담이 상승폭을 제한한다.' } }), []);
});

test('최대 3개 + 각 항목 길이 상한', () => {
  const r = extractReasonsFromReportData({
    thesis: { claim: '데이터센터 수요가 견조하다. 마진 방어력이 우수하다. 순현금 재무가 탄탄하다. 배당 성향이 꾸준히 오른다.' },
  });
  assert.equal(r.length, 3);
  for (const x of extractReasonsFromReportData(LLY)) assert.ok(x.length <= 90, x);
});

test('shortenReason — 괄호 보충설명 제거 후 맞으면 "…" 없이 반환', () => {
  const s = 'SGOV는 매파·고금리·AI 디레이팅·극단 공포(F&G 38.6) 레짐에서 두터운 캐리(3.64%)와 사실상 무변동의 안전성을 동시에 제공하는 최적의 자본 파킹처다.';
  const out = shortenReason(s);
  assert.ok(!out.includes('('));
  assert.ok(!out.endsWith('…'));
  assert.ok(out.length <= 90);
});

test('shortenReason — 절 경계(쉼표)에서 자르고 "…" 부착, 단어 중간 절단 없음', () => {
  const s =
    '포워드 EPS 50.80달러는 TTM 30.81달러 대비 큰 폭의 성장을 내재하고 있으며 이익 추정치는 꾸준히 상향되는 중이며, 포워드 PE 27.3배와 PEG 1.31배는 성장 감안 시 과하지 않다는 판단이다.';
  const out = shortenReason(s);
  assert.ok(out.endsWith('…'));
  assert.ok(out.length <= 91);
  assert.ok(s.startsWith(out.slice(0, -1)), '원문 앞부분 그대로');
  const next = s[out.length - 1];
  assert.ok(next === ',' || next === ' ' || next === '·', `경계에서 절단 (다음 글자: "${next}")`);
});

test('shortenReason — 90자 이하는 그대로', () => {
  assert.equal(shortenReason('짧은 이유.'), '짧은 이유.');
});

test('resolveReportUrl — 접두 정확 매칭(MU_ vs MUU_) + 최신 날짜', () => {
  const files = [
    'MUU_DirexionDailyMU2X_20261112.html',
    'MU_Micron_20261104.html',
    'MU_Micron_20261111.html',
    'MU_Micron_v3_notes.txt',
    'LLY_EliLilly_20261119.html',
  ];
  assert.equal(resolveReportUrl('MU', files), '/reports/MU_Micron_20261111.html');
  assert.equal(resolveReportUrl('MUU', files), '/reports/MUU_DirexionDailyMU2X_20261112.html');
  assert.equal(resolveReportUrl('LLY', files), '/reports/LLY_EliLilly_20261119.html');
  assert.equal(resolveReportUrl('TSM', files), null);
  assert.equal(resolveReportUrl('', files), null);
});

test('resolveReportUrl — 한국 6자리 티커 + NFD 파일명 NFC 정규화', () => {
  const nfd = '005930_삼성전자_20261119.html'.normalize('NFD');
  const url = resolveReportUrl('005930', ['005930_삼성전자_20260926.html', nfd]);
  assert.equal(url, '/reports/005930_삼성전자_20261119.html'.normalize('NFC'));
});
