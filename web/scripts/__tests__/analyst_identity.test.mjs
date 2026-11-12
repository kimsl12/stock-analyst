import { test } from 'node:test';
import assert from 'node:assert/strict';
import { resolveItem, canonFirm, buildAnalystBoard, hitScore, thesisScore } from '../lib/analyst_identity.mjs';

const r = (analyst_name, extra = {}) => resolveItem({ analyst_name, source: 'Bloomberg', source_type: 'media', ...extra });
const who = (res) => (res.kind === 'individual' ? res.person.key : null);

test('같은 사람 — 소속·직함 표기 차이는 하나로 병합', () => {
  const keys = [
    'Tom Lee',
    'Tom Lee (Fundstrat)',
    'Tom Lee (Fundstrat Global Advisors 공동창업자·리서치 총괄)',
    'Thomas Lee',
  ].map((n) => who(r(n)));
  assert.deepEqual(new Set(keys), new Set(['tom lee']));
  assert.equal(who(r('Mike Wilson, 최고투자책임자·미국 주식 수석 전략가 (Morgan Stanley)')), 'mike wilson');
  assert.equal(who(r('Michael Wilson')), 'mike wilson');
  assert.equal(who(r('Daniel Ives')), who(r('Dan Ives (Wedbush, 진행: Scott Wapner)')));
  assert.equal(who(r('마이클 하트넷')), who(r('Michael Hartnett (BoA)')));
});

test('소속 추출 — 괄호·쉼표 직함·기관 접두', () => {
  assert.equal(r('Savita Subramanian, 미국 주식·계량 전략 팀장 (Bank of America)').firm, 'Bank of America');
  assert.equal(r("Tom O'Malley, 반도체 담당 애널리스트 (Barclays)").firm, 'Barclays');
  const kr = r('상상인증권 송지연', { source_type: 'korea_brokerage', source: '상상인증권' });
  assert.equal(kr.person.display, '송지연');
  assert.equal(kr.firm, '상상인증권');
  // 전직은 소속 아님
  assert.equal(r('James Bullard (전 세인트루이스 연은 총재)').firm ?? null, null);
  // 애칭 괄호는 소속 아님
  assert.equal(r('Tomohiko (Tomo) Sano').firm ?? null, null);
});

test('사람 이름이 기관명과 겹쳐도 사람으로 인식', () => {
  assert.equal(who(r('Ed Yardeni')), 'ed yardeni');
  assert.equal(who(r('Peter Oppenheimer')), 'peter oppenheimer');
  assert.equal(r('Goldman Sachs Economics').kind, 'firm');
  assert.equal(r('TD Cowen', { source_type: 'ib_official', source: 'TD Cowen' }).kind, 'firm');
});

test('진행자·앵커는 예측 주체 아님', () => {
  assert.equal(r('Jonathan Ferro / Lisa Abramowicz / Annmarie Hordern').kind, 'excluded');
  assert.equal(r('Anthony Stephens (Bloomberg Television 시장 앵커)').kind, 'excluded');
  // 진행자를 빼면 1인 → 개인 산입
  assert.equal(who(r('Ben Snider (Goldman Sachs) / 진행: Scott Wapner')), 'ben snider');
  // 의견을 내는 진행자는 예외
  assert.equal(who(r('Jim Cramer (CNBC Mad Money 진행자)')), 'jim cramer');
});

test('2인 이상 — 같은 기관 공동 저자만 기관 산입, 패널은 제외', () => {
  assert.deepEqual(
    pick(r('iM증권 전유진·장호', { source_type: 'korea_brokerage', source: 'iM증권' })),
    { kind: 'firm', firm: 'iM증권' },
  );
  assert.deepEqual(
    pick(r('Jessica Reif Ehrlich, Matthew O\'Neill, Christopher Nardone (Bank of America)')),
    { kind: 'firm', firm: 'Bank of America' },
  );
  assert.deepEqual(
    pick(r('Grace Peters, Stephen Parker', { source_type: 'ib_official', source: 'JP Morgan' })),
    { kind: 'firm', firm: 'JPMorgan' },
  );
  assert.equal(r('Tom Lee (Fundstrat), Chris Harvey (CIBC) / 진행: Scott Wapner').kind, 'excluded');
  assert.equal(r('Kevin Warsh (Fed 의장) · Elizabeth Warren (상원의원)').kind, 'excluded');
  assert.equal(r('Goldman Sachs 팀 · Evercore ISI 팀').kind, 'excluded');
});

test('익명·매체·컨센서스 제외, 팀 명의는 기관', () => {
  assert.equal(r('N/A', { source: 'CNBC / The Motley Fool / CBS News' }).kind, 'excluded');
  assert.equal(r('Bloomberg TV 진행진').kind, 'excluded');
  assert.equal(r('복수 애널리스트 (Wall Street 컨센서스)').kind, 'excluded');
  assert.deepEqual(pick(r('N/A', { source_type: 'korea_brokerage', source: 'KB증권' })), { kind: 'firm', firm: 'KB증권' });
  assert.deepEqual(pick(r('하나증권 인터넷·미디어팀', { source_type: 'korea_brokerage', source: '하나증권' })), {
    kind: 'firm',
    firm: '하나증권',
  });
});

test('기관 별칭 통일', () => {
  for (const s of ['JP Morgan', 'JPMorgan Chase', 'J.P. Morgan', 'JP모간', 'JPMorgan AM']) assert.equal(canonFirm(s), 'JPMorgan');
  for (const s of ['BofA Securities', 'Bank of America (BofA Securities)', 'BoA', '뱅크오브아메리카']) assert.equal(canonFirm(s), 'Bank of America');
  assert.equal(canonFirm('하나금융투자'), '하나증권');
  assert.equal(canonFirm('파이퍼샌들러'), 'Piper Sandler');
  assert.equal(canonFirm('Bloomberg Television'), null); // 매체
});

test('점수 — 판정 없는 지표는 0점/만점으로 메우지 않음', () => {
  assert.equal(hitScore({ hit: 'partial' }), 0.5);
  assert.equal(hitScore({ hit: null }), null);
  assert.equal(thesisScore({ thesis_validity: 'correct' }), 1);
  assert.equal(thesisScore({ thesis_validity: 'pending' }), null);
  const mk = (i, outcome) => ({ analyst_name: 'Tom Lee', source: 'CNBC', source_type: 'media', outcome: { evaluated_at: '2026-11-01', ...outcome } });
  const items = [1, 2, 3, 4, 5].map((i) => mk(i, { hit: true, thesis_validity: 'logic_chain_correct' }));
  const b = buildAnalystBoard(items);
  // 오차 데이터 없음 → 오차 가중치 제외, 적중·논리만으로 100
  assert.equal(b.individuals[0].avg_error_pct, null);
  assert.equal(b.individuals[0].composite, 1);
});

test('평가 5건 미만은 순위 제외(표본 부족 목록)', () => {
  const ev = { evaluated_at: '2026-11-01', hit: true };
  const items = [
    ...Array.from({ length: 5 }, () => ({ analyst_name: 'Tom Lee', source: 'CNBC', source_type: 'media', outcome: ev })),
    { analyst_name: 'Roger Ferguson', source: 'CNBC', source_type: 'media', outcome: ev },
  ];
  const b = buildAnalystBoard(items);
  assert.deepEqual(b.individuals.map((x) => x.name), ['Tom Lee']);
  assert.deepEqual(b.lowSample.individuals.map((x) => x.name), ['Roger Ferguson']);
});

function pick(x) {
  return { kind: x.kind, firm: x.firm };
}
