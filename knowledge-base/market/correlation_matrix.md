---
updated: 2026-04-07
valid_until: 2026-04-14
file: correlation_matrix
sources: []
confidence: none
last_synced_from_db: 2026-04-07
collection_status: FAILED
failure_reason: "외부 네트워크 차단 환경 — 기초 시장 데이터 미수집으로 상관계수 산출 불가. 2회 재시도 후 중단."
---

# 자산 상관관계 매트릭스 (Correlation Matrix)

> **쓰기 권한:** correlation-monitor
> **읽기 권한:** briefing-lead, global-macro-analyst, briefing-report-generator
> **갱신 빈도:** 주 1회 (B-5 표준 6쌍 페어)
>
> WARNING: 이 파일의 CURRENT 섹션은 2026-04-07 수집 시도에서 모든 데이터 수집에 실패했습니다.
> 기초 시장 가격 데이터 (daily_snapshot.md) 미수집으로 상관계수 계산 자체가 불가능합니다.
> 에이전트는 이 데이터를 신뢰하지 말고 수동 입력 또는 재수집을 요청해야 합니다.

## ★ CURRENT ★

### 모니터링 페어 6개 — 30일 / 90일 롤링 상관계수

| # | 페어 | 30D 상관계수 | 90D 상관계수 | 과거 평균 | 1σ 범위 | 현재 Z-score | Alert |
|---|------|-------------|-------------|----------|--------|-------------|-------|
| 1 | S&P 500 ↔ 미국 10Y 국채금리 | N/A [미수집] | N/A | N/A | N/A | N/A | N/A |
| 2 | NASDAQ ↔ BTC | N/A [미수집] | N/A | N/A | N/A | N/A | N/A |
| 3 | USD/KRW ↔ KOSPI | N/A [미수집] | N/A | N/A | N/A | N/A | N/A |
| 4 | Gold ↔ DXY (달러인덱스) | N/A [미수집] | N/A | N/A | N/A | N/A | N/A |
| 5 | VIX ↔ S&P 500 | N/A [미수집] | N/A | N/A | N/A | N/A | N/A |
| 6 | WTI ↔ 미국 10Y 인플레이션기대 | N/A [미수집] | N/A | N/A | N/A | N/A | N/A |

**Alert 판정 기준:**
- 🟢 정상: Z-score ±1σ 이내
- 🟡 주의: Z-score ±1σ ~ ±2σ
- 🔴 이상: Z-score ±2σ 초과

### 이상 시그널 발생 시 해석 가이드

| 페어 | 이상 신호 의미 |
|------|----------------|
| S&P500 ↔ 10Y 금리 | 전통적 역상관 붕괴 → 금리·주식 동반 매도(스태그플레이션) 또는 동반 매수(유동성 랠리) |
| NASDAQ ↔ BTC | 동조화 심화 → 리스크 온/오프 전환. 탈동조화 → 크립토 독립 이벤트 |
| USD/KRW ↔ KOSPI | 전통적 역상관 강화 → 환 충격, 탈동조화 → 원화 표시 수익률 차별화 |
| Gold ↔ DXY | 역상관 약화 → Gold 독립 수요(지정학·인플레이션 헤지) |
| VIX ↔ S&P 500 | 역상관 붕괴 → 시장 구조 이상 (옵션 시장 왜곡 가능성) |
| WTI ↔ 인플레이션기대 | 동조화 강화 → 원자재발 인플레이션 재점화 경고 |

---

## 업데이트 로그

| 날짜 | 에이전트 | 변경 내용 |
|------|---------|----------|
| 2026-04-07 | market-data-collector | 수집 시도 — 기초 가격 데이터 전 항목 네트워크 차단(TCP 403 Forbidden)으로 미수집. 상관계수 산출 불가. 2회 재시도 후 N/A 처리. |
