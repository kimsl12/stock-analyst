// [v3.32] 리포트 타입 한국어 라벨 — FilterBar·ReportCard 공용 (영문 type 원문 노출 방지)
export const TYPE_LABELS: Record<string, string> = {
  morning: "모닝",
  evening: "이브닝",
  weekly: "주간",
  crypto: "크립토",
  user_portfolio: "내포트",
  global_intelligence: "글로벌인텔",
  model_portfolio: "모델포트",
  rebalancing: "리밸런싱",
  performance_review: "성과리뷰",
  stock_analysis: "종목",
  etf: "ETF",
  analyst: "애널리스트",
  research: "리서치",
  daily_briefing: "데일리",
};

export function typeLabel(type: string): string {
  return TYPE_LABELS[type] ?? type.replace(/_/g, " ");
}
