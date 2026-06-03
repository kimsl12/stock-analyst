---
updated: 2026-06-03
valid_until: 2026-06-04
sources: [Polymarket Gamma API, Kalshi Trade API v2]
collection_status: PARTIAL_FAIL
polymarket_count: 0
kalshi_count: 0
total_volume: N/A
collection_note: |
  2026-06-03 KST 수집 시점에 Polymarket Gamma API 및 Kalshi Trade API v2 모두
  경제/매크로/지정학 마켓을 반환하지 않음. 두 API 모두 스포츠·단기 크립토 마켓만 노출.
  - Kalshi: /trade-api/v2/markets?status=open 요청 시 MLB/NBA/NHL/WNBA 스포츠 마켓만 반환
  - Kalshi: series_ticker=FOMC, category=economics, keyword=Fed 파라미터 모두 빈 배열 반환
  - Polymarket: /events?order=volume 요청 시 5분 크립토 업다운 마켓·스포츠 마켓만 반환
  - Polymarket: q=Iran, q=bitcoin 검색 시도 — 이란 없음, BTC는 5분 단기 마켓만 존재
  원인 추정: API 엔드포인트 변경 또는 세션/지역 필터링. 수동 확인 필요.
---

# 예측 시장 통합 스냅샷 (Polymarket + Kalshi)

> 실제 돈이 걸린 예측 확률. 카테고리별 1차 소스가 다름.
> 경제/FOMC: Kalshi 우선 (100% FOMC 적중). 정치/크립토: Polymarket 우선.

## 수집 현황

| 항목                       | 상태      | 비고                         |
| -------------------------- | --------- | ---------------------------- |
| Kalshi — 경제/FOMC 마켓    | 수집 실패 | API 응답: 스포츠 마켓만 반환 |
| Kalshi — 경기침체 2026     | 수집 실패 | API 응답: 관련 마켓 없음     |
| Polymarket — 이란 지정학   | 수집 실패 | API 응답: 관련 마켓 없음     |
| Polymarket — BTC 연말 가격 | 수집 실패 | 5분 단기 마켓만 존재         |

## 1. Fed/금리 정책 [1차: Kalshi]

[수집 미완] — Kalshi API가 FOMC 관련 마켓을 반환하지 않음. 수동 확인 필요: https://kalshi.com/markets/fomc

## 2. 인플레이션/경제 — 경기침체 2026 [1차: Kalshi]

[수집 미완] — Kalshi API에서 recession/GDP/CPI 마켓 없음. 수동 확인 필요: https://kalshi.com/markets/recession

## 3. 지정학 — 이란 [1차: Polymarket]

[수집 미완] — Polymarket API에서 Iran 관련 이벤트 없음. 수동 확인 필요: https://polymarket.com/category/geopolitics

## 4. 크립토 — BTC 연말 2026 [Polymarket 단독]

[수집 미완] — Polymarket API에서 BTC 연말 가격대 마켓 없음 (5분 단기 마켓만 존재). 수동 확인 필요: https://polymarket.com/category/crypto

---

## 소스 괴리 경고

해당 없음 (데이터 수집 실패)

## 주요 변화 (전회 대비)

해당 없음 (첫 수집 시도, 모든 항목 수집 실패)

## 신뢰도 가이드

| 조건               | 신뢰도 | 가중치 적용                        |
| ------------------ | ------ | ---------------------------------- |
| Kalshi FOMC 마켓   | 최상   | Polymarket 80:20 대신 Kalshi 90:10 |
| 거래량 $1M+ (양쪽) | 높음   | 1차 소스 70:30                     |
| 거래량 $100K~$1M   | 중간   | 1차 소스 60:40                     |
| 거래량 $50K 미만   | 참고   | 50:50                              |
| 소스 괴리 10%p+    | 주의   | 양쪽 평균 사용, 불확실성 명시      |

## 수집 메타

- 수집 시각: 2026-06-03 KST (정확 시각 미기록)
- Polymarket: gamma-api.polymarket.com — 마켓 0건 (경제/지정학 카테고리 없음)
- Kalshi: api.elections.kalshi.com — 마켓 0건 (스포츠 마켓만 반환)
- 시도 횟수: Kalshi 4회, Polymarket 4회 (총 8회 API 호출)
- 실패 원인: API 응답이 스포츠/단기 크립토 마켓만 포함. 경제 카테고리 필터링 파라미터 무효.
- 다음 수집 시 시도할 URL:
  - Kalshi: /trade-api/v2/markets?status=open&limit=1000 (전수 스캔 후 로컬 필터)
  - Polymarket: /events?active=true&closed=false&order=volumeNum&limit=500 (대량 수집 후 필터)
