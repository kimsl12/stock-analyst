/**
 * scorecard_parser.mjs — analysis/{폴더}/scorecard.md 에서 핵심 수치 추출.
 *
 * 지원 형식 (2026-06 기준 실존 변형):
 *   개별주: "**종합점수: 76 / 100**" / "## 2. 투자등급" + "### 매수 (Buy)"
 *           표 "| 손절가 (2 ATR) | **$189.47** | ..." / "| 12M 펀더멘털 목표가 | **$223** | ..."
 *   ETF:    "- **종합 점수**: 72/100" / "- **투자 등급**: 매수"
 *           "- **Base case**: 목표가 $238" / "목표가 범위: USD620 ~ USD745 (중심 USD690)"
 *           산문 "손절 참고선은 2ATR 기준 약 $229.8"
 *
 * 원칙: 통화 기호($/₩/USD/원) 또는 표 행 문맥이 있어야 숫자를 채택한다.
 *       (산문의 "+8%" 같은 퍼센트 수치 오인 방지 — timeline target_price 버그 회귀 방어)
 */

const GRADES = ['강력매수', '강력 매수', '매수', '중립', '보유', '매도', '강력매도', '강력 매도'];

function toNum(s) {
  if (s == null) return null;
  const n = parseFloat(String(s).replace(/,/g, ''));
  return Number.isFinite(n) ? n : null;
}

/** 종합 점수 (0~100). 미발견 시 null. */
export function parseScore(md) {
  // 형식 변형 [v3.32 보강]: "종합점수: 76 / 100" / "종합 스코어: **77 / 100**" /
  // "등급: 중립 (Hold) — 70.5점" / 산문 "스코어 45 → 중립"
  const patterns = [
    /종합\s*(?:점수|스코어)\D{0,8}(\d{1,3}(?:\.\d+)?)\s*\/\s*100/,
    /등급[^\n]{0,40}?—\s*(\d{2,3}(?:\.\d+)?)\s*점/,
    /스코어\s*(\d{2,3}(?:\.\d+)?)\s*→/,
  ];
  for (const re of patterns) {
    const m = md.match(re);
    if (m) return toNum(m[1]);
  }
  return null;
}

/** 투자 등급 (강력매수/매수/중립/보유/매도/강력매도). 미발견 시 null. */
export function parseGrade(md) {
  // 1. "투자 등급**: 매수" / "- **투자 등급**: 매수"
  const m1 = md.match(/투자\s*등급\**\s*:?\**\s*:?\s*\**\s*(강력\s?매수|강력\s?매도|매수|중립|보유|매도)/);
  if (m1) return m1[1].replace(/\s/g, '');
  // 2. "## N. 투자등급" 섹션 직후 "### 매수 (Buy)" 헤딩
  const m2 = md.match(/##\s*\d*\.?\s*투자\s*등급[\s\S]{0,200}?###\s*(강력\s?매수|강력\s?매도|매수|중립|보유|매도)/);
  if (m2) return m2[1].replace(/\s/g, '');
  // 3. [v3.32] "등급: 중립 (Hold) — 70.5점" / "> **등급: 매수**" (재분석 v5 계열)
  const m3 = md.match(/(?:^|\n)[>\s#*-]*등급\s*[:：]\s*\**\s*(강력\s?매수|강력\s?매도|매수|중립|보유|매도)/);
  if (m3) return m3[1].replace(/\s/g, '');
  return null;
}

/** ATR 손절가. 통화 기호 필수. 미발견 시 null. */
export function parseStopLoss(md) {
  const patterns = [
    /손절가?[^|\n]*\|\s*\**\s*[\$₩]\s?([\d,]+(?:\.\d+)?)/, // 표 행
    /\*\*손절\*\*:?\s*[\$₩]\s?([\d,]+(?:\.\d+)?)/, // 요약 라인
    /손절[^$₩\n]{0,40}?[\$₩]\s?([\d,]+(?:\.\d+)?)/, // 산문 ("손절 참고선은 ... 약 $229.8")
    /손절가?[^|\n]*\|\s*\**\s*([\d,]+(?:\.\d+)?)\s*원/, // 한국 종목 "180,000원"
  ];
  for (const re of patterns) {
    const m = md.match(re);
    if (m) {
      const n = toNum(m[1]);
      if (n != null && n > 1) return n;
    }
  }
  return null;
}

/** 목표가 (Base/12M 중심값). 통화 기호(USD/$/₩/원) 문맥 필수. 미발견 시 null. */
export function parseTargetPrice(md) {
  const patterns = [
    /12M\s*펀더멘털\s*목표가[^|\n]*\|\s*\**\s*[\$₩]?\s?([\d,]+(?:\.\d+)?)/, // 개별주 표
    /Base\s*case\**:?\s*\**\s*목표가\s*(?:USD|[\$₩])\s?([\d,]+(?:\.\d+)?)/i, // ETF Base case
    /중심\s*(?:USD|[\$₩])\s?([\d,]+(?:\.\d+)?)/, // ETF "중심 USD690"
    /\*\*목표가\*\*:?\s*[\$₩]\s?([\d,]+(?:\.\d+)?)/, // 요약 라인
    /목표가[^|\n]*\|\s*\**\s*[\$₩]\s?([\d,]+(?:\.\d+)?)/, // 일반 표 행
    /목표가[^\n]{0,30}?([\d,]+(?:\.\d+)?)\s*원/, // 한국 종목
  ];
  for (const re of patterns) {
    const m = md.match(re);
    if (m) {
      const n = toNum(m[1]);
      if (n != null && n > 1) return n;
    }
  }
  return null;
}

/** 분석일 (scorecard 본문 "분석일: 2026-06-06"). 미발견 시 null. */
export function parseAnalysisDate(md) {
  const m = md.match(/분석일\s*[:：]\s*(\d{4}-\d{2}-\d{2})/);
  return m ? m[1] : null;
}

/** 전체 파싱 — 한 번에. */
export function parseScorecard(md) {
  return {
    score: parseScore(md),
    grade: parseGrade(md),
    stop_loss: parseStopLoss(md),
    target_price: parseTargetPrice(md),
    analysis_date: parseAnalysisDate(md),
  };
}
