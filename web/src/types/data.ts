// 데이터 JSON 파일 타입 정의
//
// tsconfig 의 resolveJsonModule 은 샘플 값으로 좁은 타입 추론을 만들기 때문에
// (예: 샘플이 null 인 필드는 null literal 로 좁혀짐) 위젯에서 `as any` 캐스팅이
// 필요했음. 본 파일에서 실제 schema 를 명시해 캐스팅을 제거한다.
//
// P2-15, P2-16 (2026-06-01 audit handoff) 처리.

// ---------- daily_pick.json ----------

export interface DailyPickItem {
  ticker: string;
  name: string;
  version: string;
  score: number;
  grade: string;
  analysis_date: string;
  analysis_dir: string;
  market: string;
  currency: string;
  current_price: number | null;
  buy_price: number | null;
  stop_price: number | null;
  tp_price: number | null;
  holding_period_days: number | null;
  reasons: string[];
}

export interface DailyPickJson {
  generated_at: string;
  generated_tz: string;
  pick_date: string;
  candidate_count: number;
  min_score: number;
  pick: DailyPickItem | null;
}

// ---------- kb.json ----------

export interface FredSeries {
  id: string;
  label: string;
  unit: string;
  cat: string;
  desc: string;
  date: string;
  value: number;
  prev_1w?: number | null;
  prev_1m?: number | null;
  prev_1y?: number | null;
  yoy_pct?: number | null;
  diff_1m?: number | null;
}

export interface FredData {
  available: boolean;
  api_key_required?: boolean;
  series: FredSeries[];
  updated_at: string | null;
}

// kb.json 의 다른 섹션은 위젯에서 `as any` 캐스팅 없이 정상 추론되고 있어
// 본 파일은 fred 만 정밀하게 정의. 추가 섹션 필요 시 점진 추가.
export interface KbJson {
  generated_at: string;
  generated_tz: string;
  fred?: FredData;
  [key: string]: unknown;
}
