// daily_pick_ledger.test.mjs — 데일리픽 원장 라이브러리 단위 테스트
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizeGrade, ledgerRowFromPick, upsertLedgerRow } from '../lib/daily_pick_ledger.mjs';

test('normalizeGrade — 첫 등급어 추출', () => {
  assert.equal(normalizeGrade('강력매수 — TP $475,'), '강력매수');
  assert.equal(normalizeGrade('매수'), '매수');
  assert.equal(normalizeGrade('— TP $295'), null);
  assert.equal(normalizeGrade(null), null);
});

test('ledgerRowFromPick — 행 구성 + regime 5키만', () => {
  const row = ledgerRowFromPick(
    {
      pick_date: '2026-11-19',
      pick: {
        ticker: 'TSM', name: 'TSMC', score: 77, grade: '매수', version: 'v22',
        analysis_dir: 'TSM_TSMC_v22', analysis_date: '2026-11-19', market: 'US',
        tp_price: 445, reasons: ['a'],
      },
    },
    { risk_regime: '리스크오프', weight_set: '하락장', trend: '하락', vol_regime: '고', fear_greed: 17, vix: 26 },
  );
  assert.equal(row.date, '2026-11-19');
  assert.equal(row.grade, '매수');
  assert.equal(row.ticker, 'TSM');
  assert.deepEqual(Object.keys(row.regime).sort(), ['fear_greed', 'risk_regime', 'trend', 'vol_regime', 'weight_set']);
});

test('ledgerRowFromPick — version 은 analysis_dir 끝 _vN 우선, 없으면 pick.version (M2)', () => {
  const mk = (version, analysis_dir) =>
    ledgerRowFromPick({ pick_date: '2026-11-19', pick: { ticker: 'TSM', name: 'TSMC', version, analysis_dir } }, null);
  assert.equal(mk('v21', 'TSM_TSMC_v22').version, 'v22');
  assert.equal(mk('v5', 'TSM_TSMC').version, 'v5');
  assert.equal(mk('v5', null).version, 'v5');
});

test('ledgerRowFromPick — pick null 이면 null', () => {
  assert.equal(ledgerRowFromPick({ pick_date: '2026-11-20', pick: null }, null), null);
});

test('upsert replaces same date', () => {
  const ledger = [
    { date: '2026-11-18', ticker: 'A' },
    { date: '2026-11-20', ticker: 'B' },
  ];
  const out = upsertLedgerRow(ledger, { date: '2026-11-18', ticker: 'C' });
  assert.equal(out.length, 2);
  assert.equal(out[0].ticker, 'C');
  const out2 = upsertLedgerRow(out, { date: '2026-11-19', ticker: 'D' });
  assert.deepEqual(out2.map((r) => r.date), ['2026-11-18', '2026-11-19', '2026-11-20']);
});

import { findArchiveName } from '../lib/analysis_archive.mjs';

test('findArchiveName — 접두 충돌 방지·최신 날짜·무매칭 null', () => {
  assert.equal(
    findArchiveName('MU_Micron_v2', ['MU_Micron_v20_20261001.tar.gz', 'MU_Micron_v2_20260601.tar.gz']),
    'MU_Micron_v2_20260601.tar.gz',
  );
  assert.equal(
    findArchiveName('MU_Micron_v2', ['MU_Micron_v2_20260601.tar.gz', 'MU_Micron_v2_20260701.tar.gz']),
    'MU_Micron_v2_20260701.tar.gz',
  );
  assert.equal(findArchiveName('MU_Micron_v2', ['MU_Micron_v20_20261001.tar.gz']), null);
});

test('findArchiveName — NFC/NFD 한글 정규화 매칭, 실제 이름 반환', () => {
  const nfd = '000660_SK하이닉스_v10_20260903.tar.gz'.normalize('NFD');
  assert.equal(findArchiveName('000660_SK하이닉스_v10'.normalize('NFC'), [nfd]), nfd);
});
