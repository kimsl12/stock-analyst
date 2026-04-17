---
file: 2026_correlation_log
year: 2026
created: 2026-04-07
write_owner: correlation-monitor
read_owners: [briefing-lead, global-macro-analyst, correlation-monitor, briefing-report-generator]
type: time_series
---

> **쓰기 권한:** correlation-monitor
> **읽기 권한:** briefing-lead, global-macro-analyst, correlation-monitor, briefing-report-generator
> **목적:** 2026년 시장 correlation log 시계열 영구 축적 (append-only).
> **마이그레이션:** 2026-04-07 `scripts/migrate_market_jsonl_to_md.py` 로 기존 .jsonl 변환.

# 2026 Correlation Log

| 갱신일 | 페어 | 90D 상관 | Z-score | Alert | 출처 |
|---|---|---|---|---|---|
| 2026-04-17 | S&P 500 ↔ 10Y 국채금리 | N/A (정성) | +1.8~2.2σ 추정 | 🔴 이상 | daily_snapshot_20260417, 4일 연속 동반 상승 |
| 2026-04-17 | NASDAQ ↔ BTC | N/A (정성) | +1.5~2.0σ 추정 | 🟡 주의 | BTC +5.9% 비대칭 급등, 탈동조→재동조 전환 |
| 2026-04-17 | USD/KRW ↔ KOSPI | N/A (정성) | ±0.5σ 추정 | 정상 | KRW 1,476 / KOSPI 6,091, 역상관 유지 |
| 2026-04-17 | Gold ↔ DXY | N/A (정성) | +1.8~2.3σ 추정 | 🟡→🔴 경계 | Gold ~$4,800 첫 조정 / DXY 98.19, 독립 모멘텀 꺾임 |
| 2026-04-17 | VIX ↔ S&P 500 | N/A (정성) | +2.2~2.8σ 추정 | 🔴 이상 (4일 연속) | VIX 17.94 vs 소비심리 47.6, 구조적 괴리 극단 |
| 2026-04-17 | WTI ↔ 10Y 인플레기대 | N/A (정성) | +1.5~2.0σ 추정 | 🟡 주의 | WTI $93.74 하방 vs 인플레기대 고착, 동조화 약화 |
