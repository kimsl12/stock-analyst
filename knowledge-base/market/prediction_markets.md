---
updated: 2026-06-12
valid_until: 2026-06-19
sources: [CME FedWatch (공개 집계), Kalshi (공개 집계), Polymarket (공개 집계)]
collection_status: PARTIAL
polymarket_count: 2
kalshi_count: 1
total_volume: "Polymarket 24h $49.9M / Kalshi $2.7M (Fed 마켓 기준)"
collection_note: |
  2026-06-12 수집. Polymarket Gamma / Kalshi Trade API 직접 호출은 누적 실패
  (6/3 경제 마켓 미노출 8회 + 6/12 Kalshi 429 rate-limit) → 웹 공개 집계 인용으로 전환.
  다음 수집 시 권장: API 1회만 시도 → 즉시 웹 집계 폴백 (턴 소진 방지).
---

# 예측 시장 스냅샷 (Prediction Markets)

> **수집**: 2026-06-12 KST · 웹 공개 집계 인용 (직접 API 실패 — frontmatter 참조)
> **신뢰 가중치 룰**: 경제 지표 Kalshi 우선 / 정치·지정학 Polymarket 우선 [v3.25]

## 1. Fed 금리 경로 — 6/16-17 FOMC

| 시나리오                   | 확률      | 소스 (시점)                         |
| -------------------------- | --------- | ----------------------------------- |
| **동결 (3.50~3.75% 유지)** | **96.5%** | CME FedWatch (2026-06-10)           |
| 동결                       | 97.8%     | Kalshi·Polymarket 집계 (2026-06-11) |
| 인상                       | ~2~3%     | 잔여 확률                           |

- **해석**: 5월 CPI 4.2% (에너지 +23.5% 주도) 쇼크에도 시장은 "6월 인상"이 아니라
  **"동결 + 매파 커뮤니케이션"** 으로 수렴. 근거리 인하 기대 급감 — 인하 경로 베팅이 뒤로 밀림.
- **하우스 뷰 매핑**: HV1(인플레 재가속·매파 장기화) **지지** — 인상 없이도 고금리 장기화가 기본 경로.
  6/6 시점 "매파 점도표 58%" 논쟁은 "점도표 톤" 문제로 이동 (인상 베팅 사실상 소멸).
- **관전 포인트**: 점도표 중간값 1회 인상 이상 = 시나리오 B 트리거 (모닝브리핑 6/11 분기 조건)

## 2. 기타 트래킹 (이번 수집에서 직접 수치 미확보)

| 항목                           | 상태                                     |
| ------------------------------ | ---------------------------------------- |
| 미-이란 합의 확률 (Polymarket) | 미확보 — 교착 지속 (HV4 유효, 뉴스 기준) |
| 2026 침체 확률                 | 미확보 — 다음 수집                       |
| BTC 연말 분포                  | 미확보 — 다음 수집 (HV6 참조용)          |

> 미확보 항목 인용 시 "예측시장 데이터 없음 — 자체 판단" 명기 (briefing-lead PARTIAL 룰).

## 신뢰 가중치 (v3.25 룰 보존)

| 조건               | 신뢰도 | 가중치 적용                        |
| ------------------ | ------ | ---------------------------------- |
| Kalshi FOMC 마켓   | 최상   | Polymarket 80:20 대신 Kalshi 90:10 |
| 거래량 $1M+ (양쪽) | 높음   | 1차 소스 70:30                     |
| 거래량 $100K~$1M   | 중간   | 1차 소스 60:40                     |
| 거래량 $50K 미만   | 참고   | 50:50                              |
| 소스 괴리 10%p+    | 주의   | 양쪽 평균 사용, 불확실성 명시      |

## 출처

- CME FedWatch: https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html
- Kalshi Fed 마켓: https://kalshi.com/markets/kxfeddecision/fed-meeting/kxfeddecision-26jun
- 집계 비교: https://defirate.com/prediction-markets/fed-decision-odds/
