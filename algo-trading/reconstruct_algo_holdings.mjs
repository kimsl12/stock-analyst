#!/usr/bin/env node
// reconstruct_algo_holdings.mjs — 역보고 폴백 브리지 [2026-08-06 신설]
//
// 배경: 엔진 §9 역방향 계약(algo_holdings.json write)이 2026-06-12 통지 후 미구현(engine_status: not_live).
//       그 사이 엔진이 실거래를 했으나 /portfolio "알고 자동매매" 섹션은 "데이터 없음"만 표시.
// 이 스크립트: 엔진을 건드리지 않고, 우리가 유지하는 user_portfolio.md(토스 스크린샷 파생 SSOT)에서
//              protected_holdings.json(수동 채널)을 제외한 = 알고 채널 보유를 재구성해 algo_holdings.json 을 쓴다.
//              schema algo-holdings-v1 준수 → /portfolio 가 그대로 렌더 (engine_status="reconstructed" 로 정직 표기).
// 갱신: user_portfolio.md 가 새 스크린샷으로 갱신될 때마다 재실행하면 반영됨.
// 엔진 우선: 기존 파일이 engine_status="live"(엔진 실제 보고 개시)면 덮어쓰지 않고 양보한다.

import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { extractCurrentSection, extractFrontmatter, parseHoldings } from '../web/scripts/lib/portfolio_parser.mjs';

const ROOT = join(import.meta.dirname, '..');
const DATA = join(import.meta.dirname, 'data');
const OUT_PATH = join(DATA, 'algo_holdings.json');

const now = new Date();
const kst = new Date(now.getTime() + 9 * 3600_000);
const ts = kst.toISOString().replace('T', ' ').slice(0, 19) + ' KST';

// 0. 엔진 우선 가드 — 이미 live(엔진 실제 보고)면 재구성 건너뜀
try {
  const existing = JSON.parse(readFileSync(OUT_PATH, 'utf8'));
  if (existing.engine_status === 'live') {
    console.log('SKIP: engine_status=live — 엔진 실보고 우선, 폴백 재구성 건너뜀');
    process.exit(0);
  }
} catch { /* 파일 없음/파싱 실패 — 재구성 진행 */ }

// 1. user_portfolio.md 파싱 (스크린샷 파생 SSOT, 파서 재사용 = silent-drift 계약 준수)
const md = readFileSync(join(ROOT, 'knowledge-base/portfolio/user_portfolio.md'), 'utf8');
const fm = extractFrontmatter(md);
const sourceDate = fm.updated || '(미상)';
const holdings = parseHoldings(extractCurrentSection(md).split(/\r?\n/));

// 2. 보호 종목(수동 채널) 로드 → 알고 채널 = 비보호 & 비현금
const prot = JSON.parse(readFileSync(join(DATA, 'protected_holdings.json'), 'utf8'));
const protectedSet = new Set((prot.protected ?? []).map((p) => p.ticker));
const algo = holdings.filter((h) => h.asset_type !== 'CASH' && !protectedSet.has(h.ticker));

// 3. 스키마 v1 포지션 매핑 (엔진 내부값 entry/stop/target/score 는 미상 → null)
const positions = algo.map((h) => ({
  ticker: h.ticker,
  name: h.name,
  channel: 'algo',
  strategy_type: null,
  qty: h.quantity,
  entry_price: null,
  entry_date: null,
  current_price: h.current_price,
  current_value: h.current_value_usd,
  return_pct: h.return_pct,
  stop_price: null,
  target_price: null,
  stop_mode: null,
  score_at_entry: null,
}));

const hasKrx = algo.some((h) => h.market === 'KRX' || /^\d{6}$/.test(h.ticker));

const out = {
  schema_version: 'algo-holdings-v1',
  generated_at: ts,
  engine_status: 'reconstructed',
  currency: hasKrx ? 'MIXED' : 'USD',
  cash_krw: null,
  reconstruction: {
    method: 'user_portfolio.md(토스 스크린샷 파생) − protected_holdings.json',
    source_snapshot_date: sourceDate,
    note: '엔진 §9 역보고 미구현 폴백. 알고 채널 = 비보호 보유 추정. 매매 이력(trades)·진입가·손절·목표가·스코어는 스냅샷으로 재구성 불가(null). 엔진이 §9 구현(engine_status=live) 시 이 파일을 덮어쓰며 자동 대체.',
    protected_excluded: [...protectedSet],
  },
  positions,
  trades: [],
};

writeFileSync(OUT_PATH, JSON.stringify(out, null, 2) + '\n');
console.log(
  `OK: algo_holdings.json 재구성 — 알고채널 ${positions.length}건 [${positions.map((p) => p.ticker).join(', ') || '없음'}] ` +
  `(source: user_portfolio ${sourceDate}, status=reconstructed)`
);
