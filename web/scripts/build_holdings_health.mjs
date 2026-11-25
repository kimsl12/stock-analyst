/**
 * build_holdings_health.mjs — 보유 종목 × 분석 신선도 데이터 빌드.
 *
 * 입력:
 *   knowledge-base/portfolio/user_portfolio.md  (보유 9종 — lib/portfolio_parser 재사용)
 *   analysis/_history/{TICKER}_*_timeline.json  (버전 이력)
 *   analysis/{최신 폴더}/scorecard.md            (등급·점수·손절·목표가 — lib/scorecard_parser)
 *
 * 출력: web/src/data/holdings_health.json
 *
 * 소비처:
 *   - HoldingsHealth.astro 위젯 (대시보드)
 *   - scripts/portfolio_watch.py (손절/목표가 도달 + 드리프트 감시)
 *
 * 신선도 기준: 재분석 주기(7~10일) 기준 fresh ≤ 10일 / aging ≤ 20일 / stale > 20일.
 *
 * 손절가 래칫: stop_loss = max(직전 유효 손절가, 최신 스코어카드 산출 손절가) — 보유 중에는 내려가지 않는다.
 *   최신 산출값은 stop_loss_raw, 직전값을 유지했으면 stop_ratcheted: true. (판정: lib/stop_ratchet.mjs)
 *   상태: scripts/launchd/.stop_ratchet.json (로컬 전용·gitignore — web/src/data/ 는 launchd 가 매일
 *   git checkout 으로 되돌리므로 별도 보관). 없으면 기존 holdings_health.json 값으로 시드. 매도 종목은 자동 제거.
 *   수동 리셋 = 상태 파일에서 해당 티커 삭제. (파일 전체 삭제는 재시드되므로 리셋이 아님)
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  extractCurrentSection,
  extractFrontmatter,
  parseHoldings,
} from './lib/portfolio_parser.mjs';
import { parseScorecard } from './lib/scorecard_parser.mjs';
import { applyStopRatchet, seedRatchetState } from './lib/stop_ratchet.mjs';
import { nowKstIsoShort, todayKst } from './_kst.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '../..');
const PORTFOLIO_MD = path.join(ROOT, 'knowledge-base/portfolio/user_portfolio.md');
const HISTORY_DIR = path.join(ROOT, 'analysis/_history');
const OUT = path.join(ROOT, 'web/src/data/holdings_health.json');
const RATCHET_STATE = path.join(ROOT, 'scripts/launchd/.stop_ratchet.json');

/** 래칫 상태 로드 — 파일 없음/손상 시 기존 holdings_health.json 값으로 시드. */
function loadRatchetState() {
  if (fs.existsSync(RATCHET_STATE)) {
    try {
      return JSON.parse(fs.readFileSync(RATCHET_STATE, 'utf-8'));
    } catch {
      console.warn('[holdings_health] WARN: .stop_ratchet.json 파싱 실패 — holdings_health.json 값으로 재시드');
    }
  }
  try {
    return seedRatchetState(JSON.parse(fs.readFileSync(OUT, 'utf-8')));
  } catch {
    return {};
  }
}

function freshness(days) {
  if (days == null) return null;
  if (days <= 10) return 'fresh';
  if (days <= 20) return 'aging';
  return 'stale';
}

function daysBetween(fromYmd, toYmd) {
  const a = new Date(`${fromYmd}T00:00:00+09:00`).getTime();
  const b = new Date(`${toYmd}T00:00:00+09:00`).getTime();
  if (!Number.isFinite(a) || !Number.isFinite(b)) return null;
  return Math.floor((b - a) / 86400000);
}

/** 티커의 timeline 파일 탐색 — {TICKER}_*_timeline.json (정확 prefix 매칭) */
function findTimeline(ticker) {
  if (!fs.existsSync(HISTORY_DIR)) return null;
  const file = fs
    .readdirSync(HISTORY_DIR)
    .find((f) => f.startsWith(`${ticker}_`) && f.endsWith('_timeline.json'));
  if (!file) return null;
  try {
    return JSON.parse(fs.readFileSync(path.join(HISTORY_DIR, file), 'utf-8'));
  } catch {
    return null;
  }
}

function latestAnalysis(ticker) {
  const tl = findTimeline(ticker);
  if (!tl || !Array.isArray(tl.history) || tl.history.length === 0) return null;
  const last = tl.history[tl.history.length - 1];
  const entry = {
    v: last.v ?? null,
    folder: last.folder ?? null,
    date: last.date ?? null,
    score: last.score ?? null,
    grade: last.grade ?? null,
    stop_loss: null, // main() 의 래칫 적용 후 = 유효 손절가
    stop_loss_raw: null,
    stop_ratcheted: false,
    target_price: null,
  };
  // scorecard 직접 파싱이 단일 진실 — timeline 의 target_price 필드는 추출 버그 이력이 있어 사용 금지
  const scPath = last.scorecard_path ? path.join(ROOT, last.scorecard_path) : null;
  if (scPath && fs.existsSync(scPath)) {
    const sc = parseScorecard(fs.readFileSync(scPath, 'utf-8'));
    entry.score = sc.score ?? entry.score;
    entry.grade = sc.grade ?? entry.grade;
    entry.stop_loss = sc.stop_loss;
    entry.target_price = sc.target_price;
    entry.date = entry.date ?? sc.analysis_date;
  }
  const days = entry.date ? daysBetween(entry.date, todayKst()) : null;
  entry.days_since = days;
  entry.freshness = freshness(days);
  return entry;
}

function main() {
  // Vercel 빌드 컨테이너: .vercelignore 가 analysis/ 를 제외 → 재생성 불가.
  // manifest.json 과 동일 패턴: 로컬 생성 + git tracked 파일을 그대로 사용.
  if (!fs.existsSync(HISTORY_DIR)) {
    if (fs.existsSync(OUT)) {
      console.log('[holdings_health] analysis/ 미존재 (빌드 컨테이너) — git tracked holdings_health.json 유지');
      return;
    }
    console.error('[holdings_health] FATAL: analysis/_history 도 기존 산출물도 없음');
    process.exit(1);
  }

  const md = fs.readFileSync(PORTFOLIO_MD, 'utf-8');
  const fm = extractFrontmatter(md);
  const lines = extractCurrentSection(md).split('\n');
  const holdings = parseHoldings(lines);
  if (!holdings.length) {
    console.error('[holdings_health] FATAL: 보유 종목 파싱 0건 — user_portfolio.md 형식 확인');
    process.exit(1);
  }

  const out = {
    generated_at: nowKstIsoShort(),
    portfolio_as_of: fm?.updated ?? null,
    holdings: holdings
      .filter((h) => h.asset_type !== 'CASH')
      .map((h) => ({
        ticker: h.ticker,
        name: h.name,
        type: h.asset_type ?? null,
        qty: h.quantity ?? null,
        price_md: h.current_price ?? null, // 포트폴리오 md 기록 시점 가격 (실시간 아님)
        value_md: h.current_value_usd ?? null,
        weight_pct: h.weight_pct ?? null,
        return_pct: h.return_pct ?? null,
        analysis: latestAnalysis(h.ticker),
      })),
  };

  // 손절가 래칫 — OUT 덮어쓰기 전에 상태 로드 (상태 파일 없으면 기존 OUT 이 시드 소스)
  const ratchet = applyStopRatchet(out.holdings, loadRatchetState());
  for (const w of ratchet.warnings) console.warn(`[holdings_health] WARN: ${w}`);
  fs.mkdirSync(path.dirname(RATCHET_STATE), { recursive: true });
  fs.writeFileSync(RATCHET_STATE, JSON.stringify(ratchet.state, null, 2) + '\n');

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
  const analyzed = out.holdings.filter((h) => h.analysis).length;
  const ratcheted = out.holdings.filter((h) => h.analysis?.stop_ratcheted).map((h) => h.ticker);
  console.log(
    `[holdings_health] ${out.holdings.length}종 (분석 보유 ${analyzed}종) → web/src/data/holdings_health.json`,
  );
  if (ratcheted.length) console.log(`[holdings_health] 손절가 래칫 유지 ${ratcheted.length}종: ${ratcheted.join(', ')}`);
}

main();
