/**
 * KST (Asia/Seoul, UTC+9) 시간 헬퍼.
 *
 * 모든 시각 표기는 한국 시간(KST) 기준. UTC ISO + 'Z' 접미사 대신 +09:00 사용.
 * 날짜(YYYY-MM-DD) 추출은 한국 시간대 경계 기준 (toISOString().slice(0,10) 금지).
 */
export const KST_TZ = 'Asia/Seoul';
const KST_OFFSET_MS = 9 * 60 * 60 * 1000;

/**
 * 현재 시각 KST ISO 8601 (예: '2026-05-06T18:30:00+09:00').
 * Date.toISOString()이 항상 UTC를 반환하므로 9시간 더한 후 'Z'를 '+09:00'로 치환.
 */
export function nowKstIso(d = new Date()) {
  const local = new Date(d.getTime() + KST_OFFSET_MS);
  return local.toISOString().replace('Z', '+09:00');
}

/**
 * 현재 시각 KST ISO 19자 (예: '2026-05-06T18:30:00').
 * generated_at, updated_at 등 짧은 표기용.
 */
export function nowKstIsoShort(d = new Date()) {
  const local = new Date(d.getTime() + KST_OFFSET_MS);
  return local.toISOString().slice(0, 19);
}

/**
 * 한국 시간 기준 오늘 날짜 (YYYY-MM-DD).
 * 한국 새벽 1시 = UTC 16시 전날 → 반드시 KST 경계로 추출.
 */
export function todayKst() {
  return new Intl.DateTimeFormat('en-CA', { timeZone: KST_TZ }).format(new Date());
}

/**
 * 한국 시간 기준 N일 전/후 날짜 (YYYY-MM-DD).
 */
export function kstDate(daysOffset = 0) {
  const d = new Date(Date.now() + daysOffset * 86400000);
  return new Intl.DateTimeFormat('en-CA', { timeZone: KST_TZ }).format(d);
}

/**
 * 한국 시간 기준 N일 전 YYYYMMDD 형식 (briefing 파일명 cutoff 비교용).
 */
export function kstYmd(daysOffset = 0) {
  return kstDate(daysOffset).replace(/-/g, '');
}
