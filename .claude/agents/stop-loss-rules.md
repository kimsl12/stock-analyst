# 손절·목표가 계산 로직 모듈 (Stop-Loss & Target Price Rules)

> **버전**: v1.0  
> **최종 수정**: 2026-04-05  
> **적용 대상**: 투자 브리핑 시스템  
> **이 문서의 역할**: 계산 공식의 단일 진실 소스(Single Source of Truth). 코드 구현 시 이 문서의 공식을 그대로 따르며 임의 변경 금지.

---

## 1. 개요

3가지 기법을 조합한 2단계 손절 시스템:

| 기법 | 역할 | 적용 구간 |
|------|------|-----------|
| 고정비율 손절 | 최대 손실 한도 설정 (안전망) | 진입 직후 ~ 전 구간 |
| ATR 변동성 손절 | 종목별 변동폭 반영 | 진입 직후 ~ 전 구간 |
| 트레일링 스탑 | 수익 구간에서 이익 보호 | 전환 조건 충족 후 |

**핵심 원칙**: 손절가는 올라가기만 하고 절대 내려가지 않는 래칫(ratchet) 구조.

---

## 2. 입력 변수 정의

| 변수명 | 설명 | 기본값 | 입력 방식 |
|--------|------|--------|-----------|
| `entry_price` | 매수가 (원) | — | 사용자 입력 or 포트폴리오 데이터 |
| `atr_14` | 14일 ATR (원) | — | API 자동 조회 or 사용자 입력 |
| `atr_multiplier` | ATR 배수 | 2 | 설정값 (범위: 1.5 ~ 3.0) |
| `fixed_stop_pct` | 고정 손절률 (%) | 8 | 설정값 (범위: 5 ~ 15) |
| `trail_trigger_pct` | 트레일링 전환 수익률 (%) | 10 | 설정값 (범위: 5 ~ 20) |
| `rr_ratio` | 목표 손익비 | 2 | 설정값 (범위: 1.5 ~ 5.0) |
| `current_high` | 매수 이후 최고가 (원) | entry_price | 자동 추적 (매일 갱신) |
| `prev_stop` | 직전 손절가 (원) | — | 시스템 내부 상태값 |

---

## 3. 계산 공식

### STEP 1 — 초기 손절가 (진입 직후)

두 가지를 동시에 계산하고 **더 높은 값(더 타이트한 쪽)**을 채택한다.

```
fixed_stop = entry_price × (1 - fixed_stop_pct / 100)
atr_stop   = entry_price - (atr_14 × atr_multiplier)

initial_stop = MAX(fixed_stop, atr_stop)
```

**MAX를 사용하는 이유**:
- 둘 중 높은 값 = 허용 손실이 더 작은 쪽
- 변동성이 작은 종목 → ATR이 자동으로 타이트하게 조임
- 변동성이 큰 종목 → 고정비율이 안전망 역할

**채택 방법 판별**:
```
used_method = (fixed_stop >= atr_stop) ? "고정비율" : "ATR"
```

**계산 예시**:
```
[케이스 A] 변동성 낮은 종목
  entry_price = 100,000 / atr_14 = 3,000 / atr_multiplier = 2
  fixed_stop = 100,000 × 0.92 = 92,000
  atr_stop   = 100,000 - 6,000 = 94,000
  → initial_stop = 94,000 (ATR 채택, 더 타이트)

[케이스 B] 변동성 높은 종목
  entry_price = 100,000 / atr_14 = 5,000 / atr_multiplier = 2
  fixed_stop = 100,000 × 0.92 = 92,000
  atr_stop   = 100,000 - 10,000 = 90,000
  → initial_stop = 92,000 (고정비율 채택, 안전망 작동)
```

---

### STEP 2 — 트레일링 전환 판단

매수 이후 최고가가 전환 기준에 도달했는지 확인한다.

```
trail_threshold = entry_price × (1 + trail_trigger_pct / 100)

is_trailing = (current_high >= trail_threshold)
```

**전환 전**: STEP 1의 `initial_stop`을 유지  
**전환 후**: STEP 3으로 이동

**계산 예시**:
```
  entry_price = 100,000 / trail_trigger_pct = 10
  trail_threshold = 100,000 × 1.10 = 110,000
  → current_high가 110,000 이상이면 트레일링 모드 전환
```

---

### STEP 3 — 트레일링 손절가 (수익 구간)

전환 후 고점 기준으로 손절가가 따라 올라간다. **절대 내려가지 않는 래칫 구조**.

```
trailing_stop = current_high - (atr_14 × atr_multiplier)

final_stop = MAX(trailing_stop, prev_stop)
```

**MAX를 사용하는 이유**: 주가가 일시 하락해도 손절가는 내려가면 안 된다.  
**prev_stop 초기값**: 트레일링 전환 직전의 `initial_stop`

**계산 예시**:
```
  current_high = 130,000 / atr_14 = 3,000 / atr_multiplier = 2
  trailing_stop = 130,000 - 6,000 = 124,000
  prev_stop = 94,000
  → final_stop = 124,000 (상승)

  이후 current_high가 125,000으로 하락해도:
  trailing_stop = 125,000 - 6,000 = 119,000
  prev_stop = 124,000 (직전)
  → final_stop = 124,000 (유지, 내려가지 않음)
```

---

### STEP 4 — 목표가 (손익비 기반)

초기 리스크를 기준으로 최소 목표 수익을 역산한다.

```
risk = entry_price - initial_stop
target_price = entry_price + (risk × rr_ratio)
```

**계산 예시**:
```
  entry_price = 100,000 / initial_stop = 94,000 / rr_ratio = 2
  risk = 6,000
  target_price = 100,000 + 12,000 = 112,000

  rr_ratio = 3이면:
  target_price = 100,000 + 18,000 = 118,000
```

---

## 4. 매도 판단 로직

```
if (current_price <= final_stop):
    → 매도 (손절 또는 익절)

if (current_price >= target_price):
    → 분할매도 or 트레일링 유지 (사용자 설정에 따름)
```

### 목표가 도달 시 선택지

| 전략 | 동작 | 성향 |
|------|------|------|
| 전량 매도 | target_price 도달 시 100% 매도 | 보수적 |
| 분할 익절 | 50% 매도 + 나머지 트레일링 유지 | 균형 |
| 트레일링 유지 | 목표가 무시, 트레일링만으로 관리 | 공격적 |

---

## 5. 전체 흐름 (의사코드)

```
function calculateStopLoss(entry_price, atr_14, current_high, prev_stop, config):

    # STEP 1: 초기 손절가
    fixed_stop = entry_price × (1 - config.fixed_stop_pct / 100)
    atr_stop = entry_price - (atr_14 × config.atr_multiplier)
    initial_stop = MAX(fixed_stop, atr_stop)

    # STEP 4: 목표가
    risk = entry_price - initial_stop
    target_price = entry_price + (risk × config.rr_ratio)

    # STEP 2: 전환 판단
    trail_threshold = entry_price × (1 + config.trail_trigger_pct / 100)

    if current_high < trail_threshold:
        # 전환 전 — 초기 손절가 유지
        return {
            stop_price: initial_stop,
            target_price: target_price,
            mode: "FIXED",
            trail_threshold: trail_threshold
        }
    else:
        # STEP 3: 트레일링 손절가
        trailing_stop = current_high - (atr_14 × config.atr_multiplier)
        final_stop = MAX(trailing_stop, prev_stop or initial_stop)

        return {
            stop_price: final_stop,
            target_price: target_price,
            mode: "TRAILING",
            locked_profit: final_stop - entry_price
        }
```

---

## 6. 상태 관리 요구사항

종목별로 아래 상태를 지속적으로 저장·갱신해야 한다:

| 상태값 | 갱신 시점 | 비고 |
|--------|-----------|------|
| `entry_price` | 매수 시 1회 | 변경 불가 |
| `atr_14` | 매일 장 마감 후 | API 자동 갱신 권장 |
| `current_high` | 매일 장중/마감 후 | MAX(기존 high, 당일 고가) |
| `prev_stop` | 손절가 변경 시마다 | 래칫 구조 유지용 |
| `mode` | 전환 조건 충족 시 | FIXED → TRAILING (단방향) |

---

## 7. UI 표시 규칙 

### 결론 우선 원칙
- 카드 상단: 현재 손절가·목표가 숫자를 **크게** 표시 (최소 1.3rem)
- 카드 하단: 계산 과정은 **접이식(collapsible)** 으로 숨김
- 색상 코드: 손절 = 빨강, 목표 = 초록, 트레일링 = 노랑


### 종목 카드 내 배치 구조
```
┌─────────────────────────────┐
│ [종목명] [현재가]            │
│                             │
│ 🔴 손절가  94,000원 (-6.0%) │
│ 🟢 목표가 112,000원 (+12.0%)│
│ 🟡 모드: 고정 손절 중        │
│                             │
│ ▶ 계산 상세 보기 (접이식)    │
│   ├ 고정비율: 92,000원       │
│   ├ ATR 기반: 94,000원       │
│   └ 채택: ATR (더 타이트)    │
└─────────────────────────────┘
```

---

## 8. 설정 기본값 및 허용 범위

| 설정 항목 | 기본값 | 최소 | 최대 | 단위 |
|-----------|--------|------|------|------|
| 고정 손절률 | 8 | 5 | 15 | % |
| ATR 배수 | 2 | 1.5 | 3.0 | 배 |
| 트레일링 전환 수익률 | 10 | 5 | 20 | % |
| 목표 손익비 | 2 | 1.5 | 5.0 | :1 |

사용자가 설정을 변경하지 않으면 기본값으로 동작한다.  
설정 변경 시 해당 종목의 손절가·목표가를 즉시 재계산한다.

---

## 9. 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|-----------|
| 2026-04-05 | v1.0 | 최초 작성. 고정비율 + ATR + 트레일링 스탑 3중 조합 로직 정의 |

---

## 10. 금지 사항

1. 이 문서에 정의된 계산 공식을 코드 구현 시 임의 변경 금지
2. MAX 함수 대신 MIN 사용 금지 (손절가 선택 로직 역전됨)
3. 손절가를 하향 조정하는 로직 금지 (래칫 원칙 위반)
4. 트레일링 모드에서 FIXED 모드로 역전환 금지 (단방향 전환)
5. ATR 값을 0으로 허용 금지 (0 입력 시 에러 처리)
6. 사용자 확인 없이 설정 기본값 변경 금지