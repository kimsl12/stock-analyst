#!/usr/bin/env node
/**
 * build_daily_pick.mjs — 매일 추천 종목 1건 산출 (DailyPick 위젯용) [v3.22]
 *
 * 출력: web/src/data/daily_pick.json
 *
 * 추천 룰:
 *  1순위: session-bootstrap.md 점수 ≥80 종목 중 가장 최근 등장한 1건
 *  - 빌드 타임에는 holdings 미반영 (브라우저가 Supabase 조회해 분류 표시)
 *  - 추천 데이터 자체는 "오늘의 후보 1건" + 메타 (점수/등급/가격/이유)
 *
 * 데이터 소스:
 *  - session-bootstrap.md (점수·등급·티커·발화일)
 *  - analysis/{ticker}_*_v{N}/scorecard.md (최신 v — 가격·이유 발췌)
 *  - manifest.json (HTML link · name)
 */
import { readFile, writeFile, readdir, mkdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { nowKstIsoShort, todayKst } from './_kst.mjs';
import { parseScore, parseGrade, parseStopLoss, parseTargetPrice } from './lib/scorecard_parser.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WEB_DIR = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(WEB_DIR, '..');
const BOOTSTRAP = path.join(PROJECT_ROOT, 'session-bootstrap.md');
const ANALYSIS_DIR = path.join(PROJECT_ROOT, 'analysis');
const OUTPUT_JSON = path.join(WEB_DIR, 'src', 'data', 'daily_pick.json');

const MIN_SCORE = 80;
const REMIND_MIN_SCORE = 85;

// [v3.32, 2026-06-12] 비상장 종목 — 매수 불가 + /api/price 404 로 위젯 카드 깨짐 → 후보 제외.
// (2026-06-12 ANTHROPIC 85.5 가 픽으로 선정되어 카드 전체가 '—' 표시된 사고)
const UNLISTED = new Set(['ANTHROPIC', 'SPACEX']);

// ---------------------------------------------------------------------------
// 1. session-bootstrap.md 파싱 → 종목 후보 목록
//    표 형식: | **TICKER_Name_v{N}** | **YYYY-MM-DD** | **score grade** (...) | status |
// ---------------------------------------------------------------------------
async function parseBootstrap() {
  if (!existsSync(BOOTSTRAP)) return [];
  const text = await readFile(BOOTSTRAP, 'utf-8');
  const lines = text.split(/\r?\n/);
  const candidates = [];

  // 패턴: | **{TICKER}_{name}[_v{N}]** | **{YYYY-MM-DD}** | **{score} {grade}** ... |
  // 또는 비강조 버전도 허용
  const re = /^\|\s*\*?\*?([A-Z0-9가-힣]+)_([^|*]+?)(?:_v(\d+))?\*?\*?\s*\|\s*\*?\*?(\d{4}-\d{2}-\d{2})\*?\*?\s*\|\s*\*?\*?([\d.]+)\s+([^|*(]+?)\*?\*?\s*[(|]/;

  for (const line of lines) {
    const m = re.exec(line);
    if (!m) continue;
    const [, ticker, name, version, date, scoreStr, gradeRaw] = m;
    if (UNLISTED.has(ticker)) continue; // [v3.32] 비상장 제외
    const score = Number(scoreStr);
    if (!Number.isFinite(score) || score < MIN_SCORE) continue;
    const grade = gradeRaw.trim();
    // 비강추 등급 필터
    if (/중립|매도|hold|sell|⚠/i.test(grade) && score < REMIND_MIN_SCORE) continue;
    candidates.push({
      ticker,
      name: name.trim(),
      version: version ? `v${version}` : '',
      date,
      score,
      grade,
    });
  }
  return candidates;
}

// ---------------------------------------------------------------------------
// 2. 종목별 최신 scorecard.md 위치 찾기
// ---------------------------------------------------------------------------
async function findLatestScorecard(ticker, name) {
  if (!existsSync(ANALYSIS_DIR)) return null;
  const entries = await readdir(ANALYSIS_DIR, { withFileTypes: true });
  const candidates = entries
    .filter((e) => e.isDirectory())
    .map((e) => e.name)
    .filter((n) => n.startsWith(`${ticker}_`));

  if (candidates.length === 0) return null;

  // v 접미사 가장 큰 순 정렬 (v3 > v2 > v1 > 접미사 없음)
  candidates.sort((a, b) => {
    const va = Number(a.match(/_v(\d+)$/)?.[1] ?? 0);
    const vb = Number(b.match(/_v(\d+)$/)?.[1] ?? 0);
    return vb - va;
  });

  for (const dir of candidates) {
    const sc = path.join(ANALYSIS_DIR, dir, 'scorecard.md');
    if (existsSync(sc)) return { dir, path: sc };
  }
  return null;
}

// ---------------------------------------------------------------------------
// 3. scorecard.md 본문에서 핵심 정보 추출 (best-effort grep)
// ---------------------------------------------------------------------------
async function extractScorecardMeta(scorecardPath) {
  const text = await readFile(scorecardPath, 'utf-8');
  const out = {
    current_price: null,
    buy_price: null,
    stop_price: null,
    tp_price: null,
    current_score: null,
    current_grade: null,
    currency: 'USD',
    holding_period_days: null,
    reasons: [],
  };

  // 통화 추정 (₩ 또는 KRW 등장 → KRW)
  if (/₩|KRW|원\b/.test(text)) out.currency = 'KRW';

  // 현재가 (다양한 패턴)
  const cur = text.match(/현재가[:\s]*[*₩$]*([\d,.]+)/);
  if (cur) out.current_price = Number(cur[1].replace(/,/g, ''));

  // [v3.32] 손절·목표가 — lib/scorecard_parser 재사용 (통화 문맥 필수 패턴).
  // 구 정규식이 "종합 목표가: 12M 기준 $238" 의 "12" 를 TP 로 오캡처하던 사고 수정.
  out.stop_price = parseStopLoss(text);
  out.tp_price = parseTargetPrice(text);

  // [v3.32] 최신 스코어카드 기준 점수·등급 — bootstrap 의 구버전 행 점수 보정용
  out.current_score = parseScore(text);
  out.current_grade = parseGrade(text);

  // 매수가 (분할 평단 / 적정 매수가 / 추격 매수가)
  const buy = text.match(/(?:분할\s*매수\s*평단|적정\s*매수가|매수가|평단)[:\s]*\*?\*?[$₩]?([\d,.]+)/);
  if (buy) out.buy_price = Number(buy[1].replace(/,/g, ''));
  // fallback: buy_price 없으면 current_price 사용
  if (!out.buy_price) out.buy_price = out.current_price;

  // 예상 보유 기간 (신규 양식 — 향후 자동 채워짐)
  const period = text.match(/(?:예상\s*보유\s*기간|holding\s*period)[:\s]*\*?\*?(\d+)\s*(?:일|days?)/i);
  if (period) out.holding_period_days = Number(period[1]);

  // 매수 이유 (S6 / "투자 포인트" / "핵심 결론" 등에서 첫 3 bullet 발췌)
  const bulletSections = [
    /## (?:7\.|8\.|9\.).*?결론[\s\S]+?(?=^## |\Z)/m,
    /## .*?(?:핵심|투자\s*포인트|결론)[\s\S]+?(?=^## |\Z)/m,
  ];
  for (const re of bulletSections) {
    const m = re.exec(text);
    if (!m) continue;
    const bullets = m[0].match(/^[-•*]\s+(.+)$/gm);
    if (bullets && bullets.length >= 1) {
      out.reasons = bullets
        .slice(0, 3)
        .map((b) => b.replace(/^[-•*]\s+/, '').replace(/\*\*/g, '').trim().slice(0, 140));
      break;
    }
  }

  return out;
}

// ---------------------------------------------------------------------------
// 4. 시장 추정 (ticker 패턴)
// ---------------------------------------------------------------------------
function guessMarket(ticker) {
  if (/^\d{6}$/.test(ticker)) return 'KRX';
  if (/^[A-Z]{1,5}$/.test(ticker)) return 'US';
  return 'UNKNOWN';
}

// ---------------------------------------------------------------------------
// 5. 추천 선정 (1순위 — 가장 최근 강력 추천)
// ---------------------------------------------------------------------------
async function pickToday(candidates) {
  if (candidates.length === 0) return null;

  // [v3.26] 로테이션: 최근 추천 이력 → 같은 종목 연속 방지
  const historyPath = path.join(path.dirname(OUTPUT_JSON), 'daily_pick_history.json');
  let history = [];
  if (existsSync(historyPath)) {
    try { history = JSON.parse(await readFile(historyPath, 'utf-8')); } catch {}
  }

  // [v3.32] 일중 멱등성 — 오늘 이미 픽이 있으면 그 종목 유지 (재로테이션 금지).
  // 이력이 미커밋 상태로 Vercel 컨테이너가 재빌드할 때마다 픽이 굴러가던 버그 수정
  // (2026-06-12 실측: 자정 CEG → 재빌드마다 VIG/MSFT/AMZN 으로 변동).
  const today = todayKst();
  const todayEntry = [...history].reverse().find(h => h.date === today);

  // 최근 7일 추천 티커
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 7);
  const cutoffStr = cutoff.toISOString().slice(0, 10);
  const recentTickers = new Set(
    history.filter(h => h.date >= cutoffStr && h.date !== today).map(h => h.ticker)
  );

  // 정렬: 점수 desc → 발화일 desc
  const sorted = [...candidates].sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    return b.date.localeCompare(a.date);
  });

  // 1차: 최근 7일 추천 안 된 종목 우선.
  // 오늘 픽이 이미 있으면 그 종목을 "맨 앞에서 먼저" 시도 (멱등) — 단 최신 스코어카드
  // 검증에 탈락하면 (예: 재분석 강등) 정상 후보로 넘어간다. 잘못된 픽 고착 방지.
  const fresh = sorted.filter(c => !recentTickers.has(c.ticker));
  let pool = fresh.length > 0 ? fresh : sorted;
  if (todayEntry) {
    const samePick = pool.filter(c => c.ticker === todayEntry.ticker);
    const rest = pool.filter(c => c.ticker !== todayEntry.ticker);
    pool = [...samePick, ...rest];
  }

  for (const c of pool) {
    const sc = await findLatestScorecard(c.ticker, c.name);
    if (!sc) continue;
    const meta = await extractScorecardMeta(sc.path);

    // [v3.32] 최신 스코어카드 점수로 재검증 — bootstrap 행은 구버전(재분석 전) 점수일 수 있음.
    // 현재 점수가 임계 미달이면 추천 부적격 → 다음 후보로 (VIG 사고: bootstrap 83.75 vs 실제 v3 74).
    const liveScore = meta.current_score;
    if (liveScore != null && liveScore < MIN_SCORE) continue;
    const market = guessMarket(c.ticker);
    const currency = market === 'KRX' ? 'KRW' : market === 'US' ? 'USD' : meta.currency;

    const pick = {
      ticker: c.ticker,
      name: c.name,
      version: c.version,
      score: liveScore ?? c.score,
      grade: meta.current_grade ?? c.grade,
      analysis_date: c.date,
      analysis_dir: sc.dir,
      market,
      currency,
      current_price: meta.current_price,
      buy_price: meta.buy_price,
      stop_price: meta.stop_price,
      tp_price: meta.tp_price,
      holding_period_days: meta.holding_period_days,
      reasons: meta.reasons,
    };

    // 이력 갱신 (최근 30일만 보존, 같은 날 중복 push 금지 — 멱등 재실행 대비)
    const monthAgo = new Date();
    monthAgo.setDate(monthAgo.getDate() - 30);
    const monthAgoStr = monthAgo.toISOString().slice(0, 10);
    history = history.filter(h => h.date >= monthAgoStr);
    if (!history.some(h => h.date === todayKst() && h.ticker === c.ticker)) {
      history.push({ date: todayKst(), ticker: c.ticker, score: pick.score });
    }
    await writeFile(historyPath, JSON.stringify(history, null, 2), 'utf-8');

    return pick;
  }

  return null;
}

// ---------------------------------------------------------------------------
// 메인
// ---------------------------------------------------------------------------
async function main() {
  // [v3.22.2] Vercel 빌드 컨테이너 강제 우회
  //   원인: Linux 환경의 한글 디렉토리명 NFD/NFC 차이로 findLatestScorecard 실패 → pick=null
  //   해결: VERCEL=1 환경변수 감지 시 commit된 결과 그대로 사용 (build_manifest v3.16 패턴 모방)
  //   로컬은 정상 재생성 (매번 최신 analysis/ 기반)
  if (process.env.VERCEL && existsSync(OUTPUT_JSON)) {
    const rel = path.relative(PROJECT_ROOT, OUTPUT_JSON);
    console.log(`OK: Vercel 빌드 환경 감지 — committed ${rel} 그대로 사용 (로컬 빌드가 갱신 담당)`);
    return;
  }
  // 추가 안전망: analysis/ 부재 시 commit된 결과 그대로
  if (!existsSync(ANALYSIS_DIR) && existsSync(OUTPUT_JSON)) {
    const rel = path.relative(PROJECT_ROOT, OUTPUT_JSON);
    console.log(`OK: analysis/ 부재 — committed ${rel} 그대로 사용`);
    return;
  }

  const candidates = await parseBootstrap();
  const top = await pickToday(candidates);

  await mkdir(path.dirname(OUTPUT_JSON), { recursive: true });

  const payload = {
    generated_at: nowKstIsoShort(),
    generated_tz: 'Asia/Seoul',
    pick_date: todayKst(),
    candidate_count: candidates.length,
    min_score: MIN_SCORE,
    pick: top, // null 가능
  };

  await writeFile(OUTPUT_JSON, JSON.stringify(payload, null, 2), 'utf-8');

  const rel = path.relative(PROJECT_ROOT, OUTPUT_JSON);
  if (top) {
    console.log(
      `OK: daily_pick 생성 (${top.ticker} ${top.name} ${top.score} ${top.grade}, 후보=${candidates.length}) → ${rel}`,
    );
  } else {
    console.log(`OK: daily_pick 생성 (오늘 추천 없음, 후보=${candidates.length}) → ${rel}`);
  }
}

main().catch((err) => {
  console.error('ERR:', err);
  process.exit(1);
});
