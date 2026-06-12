# algo-trading/ — 알고리즘 매매 엔진 연동 폴더

> 종목분석 에이전트 시스템이 알고리즘 매매 엔진에 제공하는 명세, 정책, 시그널 데이터.
> 절대 경로: `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/`

---

## 폴더 구조

```
/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/
└── algo-trading/
    ├── README.md                          ← 이 파일 (인덱스 + 기능 명세)
    ├── algo_engine_handoff.md             ← 전체 명세서
    ├── algo_manual_hybrid_policy.md       ← 재량매매+알고관리 하이브리드 정책
    ├── build_signals.mjs                  ← 시그널 JSON 빌드 스크립트
    └── data/
        ├── macro_regime.json              ← 매크로 레짐 판정 + 긴급 트리거
        ├── stock_scores.json              ← 전체 종목 스코어/등급
        └── earnings_calendar.json         ← 실적 발표 캘린더
```

---

## 파일별 기능 명세

### 1. algo_engine_handoff.md

**경로:** `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/algo_engine_handoff.md`
**크기:** 535줄
**역할:** 알고리즘 매매 엔진이 필요로 하는 전체 명세서

**포함 내용:**

| 섹션                | 내용                                                                                                                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0. 매매 정책 A1~A6  | 진입 시그널 (3단계 Gate) / 포지션 크기 (스코어 가중) / 보유 상한 (레짐별 3~7종) / 회전 주기 (일일 15:40 + 주간 월요일) / 청산 시그널 (등급 하락, DailyPick 탈락, 기간 초과, 레짐 전환) / 재진입 정책 (10거래일 차단, 2연속 손절 90일 차단) |
| 1. 손절/목표가 로직 | ATR 2단계 래칫 시스템 전체 의사코드 (STEP 1~4) + 입력 변수 + 금지사항                                                                                                                                                                      |
| 2. 스코어카드 체계  | 10항목 가중치 (Moat 15%, 수익성 12%, ...) + 등급 A/B/C/D/F + 매크로 동적 조정                                                                                                                                                              |
| 3. 한국 종목 현황   | 12종 분석 완료 종목 스코어 + DailyPick 연동 방법                                                                                                                                                                                           |
| 4. 데이터 소스      | 7개 API/소스 (yfinance, DART, FRED, Polymarket, openinsider, CNN F&G, 13F) + 알고 엔진 추가 필요 데이터                                                                                                                                    |
| 5. KB 구조          | market/ macro/ industry/ portfolio/ 파일별 내용 + 갱신 주기                                                                                                                                                                                |
| 6. 모델 포트폴리오  | 4종 (안전/중립/공격/배당) 자산 배분 상세 비중                                                                                                                                                                                              |
| 7. 현재 매크로 환경 | 2026-05-19 기준 시장 진단 + 이번 주 이벤트 + Polymarket 활용법                                                                                                                                                                             |
| 8. 파일 경로 맵     | 알고 엔진에서 직접 참조 가능한 종목분석 시스템 전체 경로                                                                                                                                                                                   |

---

### 2. algo_manual_hybrid_policy.md

**경로:** `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/algo_manual_hybrid_policy.md`
**크기:** 152줄
**역할:** 사용자 재량 매매 포지션을 알고 엔진이 자동 관리하는 하이브리드 정책

**포함 내용:**

| 섹션                 | 내용                                                                                                                        |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 3채널 운영 구조      | ISA 적립식 (삼성증권, 낮음) / 알고 자동매매 (토스증권, 중간) / 재량+알고관리 (토스증권, 중간~높음)                          |
| 포지션 등록          | 매수 후 엔진에 등록 시 필수 입력: ticker, qty, entry_price, strategy_type                                                   |
| 전략 유형별 파라미터 | swing (ATR 2x, 손절 8%, R:R 2:1, 20일 타이머) / position (ATR 2.5x, 12%, 3:1, 60일) / value (ATR 3x, 15%, 5:1, 타이머 없음) |
| 엔진 자동 관리 로직  | 초기 손절 산출 → 매일 ATR 갱신 → 트레일링 전환 → 자동 매도 트리거                                                           |
| 재진입 차단          | 손절 10거래일 / 기간초과 5거래일 / 목표도달 즉시 가능 / 2연속 손절 90일                                                     |
| 리스크 관리 효과     | 손절 지연 차단 (래칫), 익절 실패 방지 (트레일링), 방치 대응 (자동 점검)                                                     |
| 사용자 오버라이드    | hold_override로 자동 매도 일시 중단 가능 (리스크 사용자 책임)                                                               |

---

### 3. build_signals.mjs

**경로:** `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/build_signals.mjs`
**크기:** 297줄
**역할:** 종목분석 시스템의 KB + 분석 결과를 알고 엔진이 소비하는 JSON으로 변환

**실행 방법:**

```bash
node /Volumes/외장SSD/클로드\ AI\ 폴더/작업폴더/종목분석\ 에이전트/algo-trading/build_signals.mjs
```

**출력 3개 파일:**

| 출력                        | 데이터 소스                 | 용도                                       |
| --------------------------- | --------------------------- | ------------------------------------------ |
| data/macro_regime.json      | FRED + daily_snapshot + F&G | 알고 엔진 Gate 2 (매크로 필터)             |
| data/stock_scores.json      | analysis/\*/scorecard.md    | 알고 엔진 Gate 1 (종목 필터) + 포지션 크기 |
| data/earnings_calendar.json | economic_calendar.md        | 실적 발표 전 포지션 보호                   |

**의존 데이터 (종목분석 시스템에서 읽는 파일):**

```
/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/
├── knowledge-base/macro/fred_snapshot.json          → 매크로 레짐 판정
├── knowledge-base/market/daily_snapshot.md           → VIX, USD/KRW, 지수
├── knowledge-base/market/fear_greed.json             → F&G 인덱스
├── knowledge-base/market/economic_calendar.md        → 실적 캘린더
└── analysis/*/scorecard.md                           → 종목별 스코어/등급
```

---

### 4. data/macro_regime.json

**경로:** `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/data/macro_regime.json`
**갱신:** build_signals.mjs 실행 시
**역할:** 현재 매크로 레짐 + 긴급 트리거 상태

**스키마:**

```json
{
  "generated_at": "KST 타임스탬프",
  "regime": "Goldilocks | Reflation | Stagflation | FalseCalm",
  "regime_kr": "한글 레짐명",
  "confidence": "high | medium | low",
  "indicators": {
    "fed_funds_rate": 3.64,
    "us_10y": 4.43,
    "us_2y": 3.93,
    "t10y2y_spread": 0.49,
    "core_pce_yoy": "number",
    "unemployment": 4.3,
    "hy_spread": 2.77,
    "breakeven_10y": 2.42,
    "gdp_yoy": "number | null",
    "vix": 18.43,
    "usd_krw": 1501.18,
    "fear_greed_cnn": "number | null",
    "fear_greed_crypto": "number | null"
  },
  "emergency": {
    "active": "boolean",
    "triggers": [
      {
        "type": "VIX_25 | VIX_30 | USDKRW_1550 | USDKRW_1600",
        "value": "number",
        "action": "string"
      }
    ]
  },
  "favorable_sectors": ["섹터 목록"],
  "unfavorable_sectors": ["섹터 목록"],
  "max_holdings": "레짐별 최대 보유 종목 수 (0~7)",
  "position_multiplier": "포지션 크기 배수 (0~1.2)"
}
```

**레짐별 동작:**

| regime      | max_holdings | position_multiplier | 알고 엔진 동작         |
| ----------- | ------------ | ------------------- | ---------------------- |
| Goldilocks  | 7            | 1.2                 | 적극 진입              |
| Reflation   | 5            | 1.1                 | 우호 섹터 선별 진입    |
| Stagflation | 3            | 0.7                 | 방어 섹터만, 축소 운영 |
| FalseCalm   | 0            | 0                   | 전면 중단, 전량 현금   |

**긴급 트리거:**

| trigger     | 조건             | action                                    |
| ----------- | ---------------- | ----------------------------------------- |
| VIX_25      | VIX >= 25        | swing/position 트레일링 1x ATR로 타이트화 |
| VIX_30      | VIX >= 30        | value 포지션도 타이트화                   |
| USDKRW_1550 | USD/KRW >= 1,550 | 한국 종목 전량 청산 검토                  |
| USDKRW_1600 | USD/KRW >= 1,600 | value 한국 종목도 청산 검토               |

---

### 5. data/stock_scores.json

**경로:** `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/data/stock_scores.json`
**갱신:** build_signals.mjs 실행 시
**역할:** 전체 분석 완료 종목의 스코어/등급/시장/stale 여부

**스키마:**

```json
{
  "generated_at": "KST 타임스탬프",
  "total_count": 116,
  "eligible_count": 13,
  "kr_eligible_count": 1,
  "stocks": [
    {
      "ticker": "000660",
      "name": "SK하이닉스",
      "version": "3",
      "score": 94.5,
      "grade": "A",
      "analysis_date": "2026-05-12",
      "market": "KRX",
      "dir": "000660_SK하이닉스_v3",
      "days_since_analysis": 7,
      "stale": false
    }
  ]
}
```

**필드 설명:**

| 필드                | 설명                   | 알고 엔진 사용                         |
| ------------------- | ---------------------- | -------------------------------------- |
| score               | 0~100 스코어카드 점수  | Gate 1 필터 (>= 80) + 포지션 크기 배수 |
| grade               | A/B/C/D/F              | 등급 하락 시 청산 트리거               |
| market              | KRX / US               | 한국 종목만 필터링                     |
| stale               | 분석일 30일+ 경과 여부 | true면 진입 차단                       |
| days_since_analysis | 분석 후 경과일         | stale 임박 종목 재분석 우선순위        |

**eligible 조건:** score >= 80 AND stale == false

---

### 6. data/earnings_calendar.json

**경로:** `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/data/earnings_calendar.json`
**갱신:** build_signals.mjs 실행 시
**역할:** 보유 종목의 실적 발표일 → 바이너리 이벤트 보호

**스키마:**

```json
{
  "generated_at": "KST 타임스탬프",
  "event_count": 8,
  "events": [
    {
      "raw": "원본 텍스트",
      "date": "2026-05-22",
      "ticker": "NVDA"
    }
  ]
}
```

**알고 엔진 사용:**

- 보유 종목의 실적 발표 3거래일 전 → 트레일링 타이트화 또는 포지션 50% 축소
- swing 전략: 실적 발표 당일 보유 금지 (사전 청산)
- position/value: 보유 유지하되 트레일링 1.5x ATR로 조임

---

## 종목분석 시스템 참조 경로 (알고 엔진에서 직접 읽기 가능)

```
/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/

[종목 분석 결과]
├── analysis/{ticker}_{name}_v{N}/scorecard.md    # 10항목 스코어카드
├── analysis/{ticker}_{name}_v{N}/data.json       # 수집 원본 데이터
├── web/src/data/daily_pick.json                   # DailyPick 후보 풀 (스코어 80+)

[시장 데이터 — KB]
├── knowledge-base/market/daily_snapshot.md        # 지수/환율/채권/크립토 종합
├── knowledge-base/market/prediction_markets.md    # Polymarket 예측 확률
├── knowledge-base/market/correlation_matrix.md    # 6쌍 상관계수 + Z-score
├── knowledge-base/market/surprise_index.md        # 경제 서프라이즈 Beat/Miss
├── knowledge-base/market/fear_greed.json          # CNN/Crypto F&G
├── knowledge-base/market/economic_calendar.md     # 경제 일정
├── knowledge-base/market/guru_positions.md        # 거물 8인 13F

[매크로 데이터 — KB]
├── knowledge-base/macro/fred_snapshot.json        # FRED 15개 시리즈
├── knowledge-base/macro/us_monetary_policy.md     # Fed 정책
├── knowledge-base/macro/korea_economy.md          # 한국 경제
├── knowledge-base/macro/geopolitics.md            # 지정학 리스크
├── knowledge-base/macro/global_risk_factors.md    # Top 5 글로벌 리스크

[포트폴리오 — KB]
├── knowledge-base/portfolio/model_portfolios.md   # 4종 모델 포트폴리오
├── knowledge-base/portfolio/user_portfolio.md     # 사용자 보유 종목
├── knowledge-base/portfolio/insider_signals.json  # 인사이더 클러스터 매수

[산업 — KB]
├── knowledge-base/industry/{sector}.md            # 26개 섹터별 현황

[손절 규칙 — SSOT]
├── reference/stop-loss-rules.md              # ATR 래칫 손절 계산 공식

[알고 매매 전용]
└── algo-trading/
    ├── algo_engine_handoff.md                     # 전체 명세 (정책 A1~A6 포함)
    ├── algo_manual_hybrid_policy.md               # 재량+알고 하이브리드
    ├── build_signals.mjs                          # 시그널 빌드 스크립트
    └── data/
        ├── macro_regime.json                      # 매크로 레짐 판정
        ├── stock_scores.json                      # 전체 종목 스코어
        ├── earnings_calendar.json                 # 실적 캘린더
        ├── polymarket_alerts.json                 # Polymarket 급변 트리거
        ├── polymarket_prev.json                   # Polymarket 이전 수집분 (비교용)
        ├── score_changes.json                     # 스코어 변동 감지
        └── stock_scores_prev.json                 # 스코어 이전 수집분 (비교용)
```

---

## 시그널 빌드 실행 방법

```bash
# 수동 실행
node "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/build_signals.mjs"

# 출력 확인
cat algo-trading/data/macro_regime.json | python3 -m json.tool
cat algo-trading/data/stock_scores.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'eligible: {d[\"eligible_count\"]}, kr: {d[\"kr_eligible_count\"]}')"
```

**권장 실행 주기:**

- 매일 KST 15:40 (정규장 마감 후) — 일일 점검
- 매주 월요일 09:00 — 주간 리밸런싱 전
- 브리핑 완료 직후 — 최신 KB 반영

---

### 7. data/polymarket_alerts.json

**경로:** `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/data/polymarket_alerts.json`
**갱신:** build_signals.mjs 실행 시
**역할:** Polymarket 확률 24시간 내 15%p+ 급변 감지 → 레짐 재판정 강제 트리거

**스키마:**

```json
{
  "generated_at": "KST 타임스탬프",
  "threshold_pct": 15,
  "market_count": "수집된 마켓 수",
  "alerts": [
    {
      "question": "마켓 질문 원문",
      "prev_pct": 45.0,
      "current_pct": 62.0,
      "delta_pct": 17.0,
      "direction": "UP | DOWN",
      "action": "REGIME_RECHECK",
      "severity": "warning (15~24%p) | critical (25%p+)"
    }
  ]
}
```

**알고 엔진 사용:**

- alerts 배열이 비어있으면 정상 — 추가 동작 불필요
- alerts가 1건 이상이면 `macro_regime.json`을 재확인하고 Gate 2 필터 재평가
- severity=critical이면 전 포지션 트레일링 1단계 타이트화 검토
- `polymarket_prev.json`은 이전 수집분 — 엔진이 직접 읽을 필요 없음 (빌드 내부용)

---

### 8. data/score_changes.json

**경로:** `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/data/score_changes.json`
**갱신:** build_signals.mjs 실행 시
**역할:** 종목 스코어/등급 변동 감지 → 알고 엔진에 진입/청산 시그널 전달

**스키마:**

```json
{
  "generated_at": "KST 타임스탬프",
  "changes": [
    {
      "ticker": "000660",
      "name": "SK하이닉스",
      "market": "KRX",
      "prev_score": 94.5,
      "current_score": 88.0,
      "score_delta": -6.5,
      "prev_grade": "A",
      "current_grade": "A",
      "direction": "DOWN"
    }
  ],
  "upgrades": ["등급 상향 종목 (D→C, C→B, B→A 등)"],
  "downgrades": ["등급 하향 종목 (A→B, B→C 등)"],
  "new_eligible": ["새로 80점+ 진입한 티커 목록"],
  "lost_eligible": ["80점 미만으로 이탈한 티커 목록"]
}
```

**알고 엔진 사용:**

- `new_eligible` — 새 진입 후보. Gate 1 통과 종목 추가
- `lost_eligible` — DailyPick 탈락 종목. A5 청산 정책 (5거래일 유예) 발동
- `downgrades`에서 D/F 등급 하향 — 즉시 청산 트리거
- `upgrades`에서 A 등급 진입 — 진입 후보 상향
- `stock_scores_prev.json`은 이전 스코어 — 엔진이 직접 읽을 필요 없음 (빌드 내부용)

---

### 9. data/algo_holdings.json — 역방향 (엔진이 씀)

**경로:** `/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/algo-trading/data/algo_holdings.json`
**갱신:** **알고 엔진이 직접 씀** — 체결 직후 즉시 + 매일 15:40 런 종료 시 (전체 덮어쓰기, atomic write 권장)
**역할:** 엔진 보유 포지션 + 체결 내역 → 종목분석 웹 대시보드 `/portfolio` "알고 자동매매" 섹션 자동 반영

다른 data/ 파일과 방향이 반대다 (유일한 엔진 → 종목분석 파일). 스키마 상세: `algo_engine_handoff.md` §9.

- `positions` — 현재 보유 전체 스냅샷 (channel: algo | manual_managed 구분)
- `trades` — 최신순 최근 50건 (reason_code: ENTRY/STOP/TRAIL_STOP/TARGET/TIME_EXIT/GRADE_EXIT/REGIME_EXIT/EMERGENCY/REPLACE)
- `engine_status` — live | paused | not_live (live + 2일 무갱신 → 종목분석 watchdog 경고)

종목분석 쪽 반영 파이프라인: launchd `com.stockanalyst.algo-sync` (KST 16:15) + watchdog (06:40/10:30) 이 변경 감지 → commit/push → Cloudflare 미러(풀사이트) + Vercel(플래그 해제 후) 배포.

---

## 향후 추가 예정

| 기능                          | 상태      | 설명                         |
| ----------------------------- | --------- | ---------------------------- |
| stock_scores.json 파싱 정밀화 | 개선 필요 | 일부 종목 스코어 오추출 수정 |
| 토스증권 API 연동             | 대기      | API 출시 후 주문 집행 연동   |
