# 종목분석 에이전트 → 알고리즘 매매 에이전트 전달 자료

> 작성일: 2026-05-19
> 목적: 토스뱅크 API 기반 한국주식 알고리즘 매매 엔진 구축 시 참조 데이터

---

## 0. 매매 정책 (Trading Policy A1~A6)

종목분석 에이전트의 스코어카드 + DailyPick + ATR + 매크로 레짐을 알고리즘이 실행 가능한 규칙으로 변환한 정책.

### A1. 진입 시그널

3단계 필터를 **모두 통과**해야 진입:

```
Gate 1 — 종목 필터 (필수)
  스코어 ≥ 80 (A등급, Strong Buy)
  AND 분석일 경과 ≤ 30일 (stale 분석 차단)
  AND KRX 거래정지/관리종목 아님

Gate 2 — 매크로 필터 (필수)
  매크로 레짐 ≠ "거짓 안정"
  AND 해당 종목 섹터가 현재 레짐의 "비우호 섹터"에 미포함
  AND VIX < 25 (25+ = 시스템 리스크, 신규 진입 전면 중단)
  AND USD/KRW < 1,550 (외인 이탈 극단 구간 차단)

Gate 3 — 기술적 필터 (선택, 권장)
  RSI(14) < 70 (과매수 진입 회피)
  AND 현재가 ≤ 스코어카드 목표가 (추격 매수 방지)
```

**즉시 매수 (Gate 3 생략):** 스코어 ≥ 95 + 매크로 레짐 Goldilocks/Reflation이면 Gate 3 생략하고 즉시 진입. 역대급 확신 종목은 기술적 조정 대기 비용이 더 크다.

**매크로 레짐 판정 기준:**

| 레짐        | 조건                                      | 진입 허용                                 |
| ----------- | ----------------------------------------- | ----------------------------------------- |
| Goldilocks  | GDP ≥ 2% + Core PCE ≤ 2.5% + 10Y-2Y > 0   | 모든 섹터                                 |
| Reflation   | GDP ≥ 2% + Core PCE > 2.5%                | 에너지/소재/산업재 우호, Tech/REIT 비우호 |
| Stagflation | GDP < 2% + Core PCE > 2.5%                | 에너지/Gold/헬스케어만, 나머지 비우호     |
| 거짓 안정   | VIX < 18 + HY 스프레드 < 3 + Core PCE > 3 | **진입 전면 중단** (현금 대기)            |

**데이터 소스:**

- 스코어: `analysis/{ticker}/scorecard.md` 또는 `web/src/data/daily_pick.json`
- 매크로 레짐: `knowledge-base/macro/fred_snapshot.json` (FRED 15종)
- VIX/USD/KRW: `knowledge-base/market/daily_snapshot.md`
- RSI: yfinance 또는 토스 API 실시간

### A2. 포지션 크기

**스코어 가중 배분:**

```
종목당 비중 = base_weight × score_multiplier × regime_multiplier

base_weight:
  총 자본 / max_holdings (균등 배분 기준선)

score_multiplier:
  스코어 95~100 → 1.5x (확신 최상위)
  스코어 85~94  → 1.2x (A등급 상위)
  스코어 80~84  → 1.0x (A등급 하위)

regime_multiplier:
  Goldilocks + 우호 섹터 → 1.2x
  Reflation + 우호 섹터  → 1.1x
  Stagflation             → 0.7x (방어적)
  거짓 안정               → 0x (진입 차단)
```

**비중 상한:** 단일 종목 최대 30% (score_multiplier + regime_multiplier 적용 후에도 30% cap)

**예시 (총 자본 1,000만원, 5종목 기준):**

- base_weight = 200만원 (20%)
- SK하이닉스 94.5점 + Goldilocks + 반도체(우호) → 200만 x 1.2 x 1.2 = 288만원 (28.8%)
- 카카오 72점 → 진입 불가 (80점 미만)

### A3. 보유 종목 수 상한

```
매크로 레짐별 최대 보유:
  Goldilocks  → 최대 7종목
  Reflation   → 최대 5종목
  Stagflation → 최대 3종목 (집중 방어)
  거짓 안정   → 0종목 (전량 현금)

절대 상한: 10종목 초과 불가 (분산 과잉 → 관리 불가)
절대 하한: 1종목 (단일 종목 올인은 허용하되 비중 30% cap 적용)
```

**초과 시 처리:** 보유 종목이 상한 초과 상태에서 신규 진입 시그널 → 가장 낮은 스코어 종목 1개 청산 후 교체.

### A4. 회전 주기

```
점검 타이밍:
  1차: 매일 KST 15:40 (정규장 마감 10분 후)
       → DailyPick 갱신 확인 + ATR 손절가 갱신 + 종가 기반 RSI 체크

  2차: 매주 월요일 09:00 (주간 리밸런싱)
       → 매크로 레짐 재판정 + 포지션 비중 재계산 + stale 분석(30일+) 종목 정리

점검 항목:
  일일: 손절/목표가 도달 여부, DailyPick 변동, 신규 A등급 종목 출현
  주간: FRED 매크로 데이터 갱신, 모델 포트폴리오 방향 변화, 재분석 결과 반영
```

**긴급 점검 트리거 (장중 즉시):**

- VIX 25+ 돌파 → 전 종목 트레일링 스탑 1x ATR로 타이트화
- USD/KRW 1,550+ → 한국 종목 전량 청산 검토
- KOSPI -5% 일간 → 신규 진입 24시간 중단

### A5. 청산 시그널 (손절 외)

손절(ATR/고정비율)은 별도 로직(§1 참조). 여기서는 **펀더멘털 + 시스템 기반 청산:**

```
청산 트리거 (어느 하나라도 충족 시):

  1. 등급 하락 — 재분석 결과 스코어 50 미만 (D등급 이하)
     → 다음 거래일 시가 전량 청산

  2. DailyPick 탈락 — 스코어 80 미만으로 하락하여 후보 풀에서 제거
     → 즉시 청산 아님. 5거래일 유예 후에도 80 미달이면 청산
     → 유예 중 ATR 트레일링은 정상 작동

  3. 매크로 레짐 전환 — 비우호 섹터로 전환
     → Stagflation 진입 시: 비우호 섹터 종목 5거래일 내 단계 축소 (50% → 전량)
     → 거짓 안정 진입 시: 전 종목 3거래일 내 전량 청산

  4. 목표가 도달
     → 기본 정책: 50% 매도 + 나머지 트레일링 유지 (균형형)
     → 보수적 모드: 전량 매도
     → 공격적 모드: 트레일링만 유지 (목표가 무시)

  5. 보유 기간 초과 — 60거래일(약 3개월) 경과 + 수익률 0% 미만
     → 횡보 포지션 자본 효율 저하 방지. 수익 중이면 트레일링 유지.
```

### A6. 재진입 정책

```
손절 후 재진입:
  차단 기간: 10거래일 (약 2주)
  재진입 조건: 차단 기간 경과 + 재분석 결과 스코어 85+ (손절 전 대비 상향)
  이유: 손절 직후 기술적 반등에 재진입하면 같은 하락 추세에 재노출

등급 하락 청산 후 재진입:
  차단 기간: 재분석 1회 이상 (최소 14일)
  재진입 조건: 새 분석에서 A등급(80+) 회복 + 매크로 레짐 우호
  이유: 등급 하락의 원인이 해소되었는지 새 데이터로 확인 필요

목표가 도달 청산 후 재진입:
  차단 없음 (즉시 재진입 가능)
  조건: 스코어 80+ 유지 + RSI < 70 + 현재가 < 이전 목표가
  이유: 실현 후 조정 시 정상적 재진입

같은 종목 연속 손절:
  동일 종목 2회 연속 손절 → 해당 종목 90일 차단
  이유: 분석 모델이 해당 종목 특성을 잘못 포착하고 있을 가능성
```

### 매매 정책 요약 다이어그램

```
[매일 15:40 점검]
    │
    ├── 신규 진입 후보?
    │     └── Gate 1 (스코어 80+, 30일 이내)
    │         └── Gate 2 (레짐 ≠ 거짓안정, 섹터 우호, VIX<25, USD/KRW<1550)
    │             └── Gate 3 (RSI<70, 현재가 ≤ 목표가) [스코어 95+ 시 생략]
    │                 └── 비중 계산 (base × score_mult × regime_mult, cap 30%)
    │                     └── 보유 상한 체크 → 초과 시 최저 스코어 종목 교체
    │
    ├── 보유 종목 점검
    │     ├── ATR 손절가 도달? → 매도 (래칫 로직)
    │     ├── 목표가 도달? → 50% 매도 + 트레일링
    │     ├── 등급 D 이하? → 다음 거래일 전량 청산
    │     ├── DailyPick 탈락? → 5일 유예 후 청산
    │     ├── 보유 60일 + 손실? → 청산
    │     └── 레짐 전환 (비우호)? → 단계 축소
    │
    └── 긴급 트리거
          ├── VIX 25+ → 트레일링 타이트화
          ├── USD/KRW 1550+ → 한국주 전량 청산 검토
          └── KOSPI -5% → 신규 진입 24시간 중단
```

---

## 1. 손절/목표가 계산 로직 (SSOT)

### 아키텍처: 3기법 2단계 래칫 시스템

손절가는 올라가기만 하고 절대 내려가지 않는 래칫(ratchet) 구조.

#### 입력 변수

| 변수명              | 설명                     | 기본값      | 허용 범위     |
| ------------------- | ------------------------ | ----------- | ------------- |
| `entry_price`       | 매수가 (원)              | -           | -             |
| `atr_14`            | 14일 ATR (원)            | -           | API 자동 조회 |
| `atr_multiplier`    | ATR 배수                 | 2           | 1.5 ~ 3.0     |
| `fixed_stop_pct`    | 고정 손절률 (%)          | 8           | 5 ~ 15        |
| `trail_trigger_pct` | 트레일링 전환 수익률 (%) | 10          | 5 ~ 20        |
| `rr_ratio`          | 목표 손익비              | 2           | 1.5 ~ 5.0     |
| `current_high`      | 매수 이후 최고가 (원)    | entry_price | 매일 갱신     |
| `prev_stop`         | 직전 손절가 (원)         | -           | 시스템 내부   |

#### STEP 1 — 초기 손절가

```python
fixed_stop = entry_price * (1 - fixed_stop_pct / 100)
atr_stop   = entry_price - (atr_14 * atr_multiplier)
initial_stop = max(fixed_stop, atr_stop)  # 더 타이트한 쪽 채택
```

- 변동성 낮은 종목 → ATR이 타이트하게 조임
- 변동성 높은 종목 → 고정비율이 안전망

#### STEP 2 — 트레일링 전환 판단

```python
trail_threshold = entry_price * (1 + trail_trigger_pct / 100)
is_trailing = (current_high >= trail_threshold)
```

#### STEP 3 — 트레일링 손절가

```python
trailing_stop = current_high - (atr_14 * atr_multiplier)
final_stop = max(trailing_stop, prev_stop)  # 래칫: 절대 하향 금지
```

#### STEP 4 — 목표가

```python
risk = entry_price - initial_stop
target_price = entry_price + (risk * rr_ratio)
```

#### 전체 의사코드

```python
def calculate_stop_loss(entry_price, atr_14, current_high, prev_stop, config):
    # STEP 1
    fixed_stop = entry_price * (1 - config.fixed_stop_pct / 100)
    atr_stop = entry_price - (atr_14 * config.atr_multiplier)
    initial_stop = max(fixed_stop, atr_stop)

    # STEP 4
    risk = entry_price - initial_stop
    target_price = entry_price + (risk * config.rr_ratio)

    # STEP 2
    trail_threshold = entry_price * (1 + config.trail_trigger_pct / 100)

    if current_high < trail_threshold:
        return {
            "stop_price": initial_stop,
            "target_price": target_price,
            "mode": "FIXED",
            "trail_threshold": trail_threshold
        }
    else:
        # STEP 3
        trailing_stop = current_high - (atr_14 * config.atr_multiplier)
        final_stop = max(trailing_stop, prev_stop or initial_stop)
        return {
            "stop_price": final_stop,
            "target_price": target_price,
            "mode": "TRAILING",
            "locked_profit": final_stop - entry_price
        }
```

#### 매도 판단

```python
if current_price <= final_stop:
    # 매도 (손절 또는 익절)
if current_price >= target_price:
    # 전량매도(보수적) / 50%매도+트레일링(균형) / 트레일링유지(공격적)
```

#### 상태 관리 요구사항

| 상태값         | 갱신 시점                              |
| -------------- | -------------------------------------- |
| `entry_price`  | 매수 시 1회 (불변)                     |
| `atr_14`       | 매일 장 마감 후                        |
| `current_high` | 매일 (= max(기존, 당일 고가))          |
| `prev_stop`    | 손절가 변경 시마다                     |
| `mode`         | FIXED → TRAILING (단방향, 역전환 금지) |

#### 금지 사항

1. MAX 대신 MIN 사용 금지 (손절 로직 역전)
2. 손절가 하향 조정 금지 (래칫 위반)
3. TRAILING → FIXED 역전환 금지
4. ATR 값 0 허용 금지

---

## 2. 10항목 가중 스코어카드 체계

### 평가 항목 + 레짐별 가중치 3벌 세트 [v3.24]

매크로 레짐에 따라 가중치 세트 자체가 교체된다. `macro_regime.json`의 regime 값으로 결정.

| #   | 항목               | 상승장  | 하락장  | 횡보장  | 평가 기준                        | 데이터 소스         |
| --- | ------------------ | :-----: | :-----: | :-----: | -------------------------------- | ------------------- |
| 1   | Moat (경제적 해자) |   12%   |   15%   |   15%   | Wide/Narrow/None → 10/6/2점      | 사업구조, 경쟁 우위 |
| 2   | 수익성             |   10%   |   12%   |   14%   | OPM, ROE, ROIC vs 동종 업계      | 재무제표            |
| 3   | 성장성             | **15%** | **8%**  |   10%   | 매출/이익 CAGR, 컨센서스 리비전  | 재무제표 + 컨센서스 |
| 4   | 재무건전성         |   8%    | **14%** |   12%   | 부채비율, FCF, 이자보상배율      | 재무제표            |
| 5   | 밸류에이션         |   8%    | **14%** | **13%** | PER/PBR vs 적정가, 목표주가 괴리 | 재무제표 + 시장     |
| 6   | 모멘텀             | **14%** | **6%**  |   8%    | 주가 모멘텀, 컨센서스 방향       | 기술적 지표         |
| 7   | 수급               |   10%   |   5%    |   7%    | 외국인/기관 순매수, 리비전       | 거래소 데이터       |
| 8   | 리스크             |   8%    | **14%** |   10%   | 발생가능성 x 영향도 Top 3        | 정성 평가           |
| 9   | 산업 매력도        |   10%   |   7%    |   7%    | Porter 5 Forces, 사이클 위치     | 산업 분석           |
| 10  | 경영진 역량        |   5%    |   5%    |   4%    | CEO 재임, 보상구조, 자본배분     | 공시                |

**레짐 → 가중치 세트 매핑:**

| macro_regime.json regime | 가중치 세트 | 핵심                                                 |
| ------------------------ | ----------- | ---------------------------------------------------- |
| Goldilocks               | 상승장      | 성장(15%) + 모멘텀(14%) 중심                         |
| Reflation                | 횡보장      | Moat(15%) + 수익성(14%) + 밸류(13%) 중심             |
| Stagflation              | 하락장      | 재무(14%) + 밸류(14%) + 리스크(14%) + Moat(15%) 중심 |
| FalseCalm                | 하락장      | 동일 (진입 자체가 차단이지만 보유 종목 재평가용)     |

### 등급 체계

| 점수   | 등급 | 투자의견    | 알고 엔진 액션         |
| ------ | ---- | ----------- | ---------------------- |
| 80~100 | A    | Strong Buy  | 진입 후보 (최우선)     |
| 65~79  | B    | Buy         | 진입 후보 (차선)       |
| 50~64  | C    | Hold        | 보유 유지, 신규 진입 X |
| 35~49  | D    | Underweight | 청산 검토              |
| 0~34   | F    | Sell        | 즉시 청산              |

**레짐 전환 시 등급 변동:** 같은 종목이라도 레짐이 바뀌면 가중치 세트 교체로 스코어가 변동한다. 예: 성장주가 상승장에서 A등급(성장 15%)이었다가 하락장 전환 시 B등급(성장 8%)으로 자동 강등될 수 있다.

---

## 3. 한국 종목 분석 현황 (12종)

| 티커   | 종목명             | 최신 버전 | 스코어 | 등급         | 섹터     |
| ------ | ------------------ | --------- | ------ | ------------ | -------- |
| 000660 | SK하이닉스         | v3        | 94.5   | A (강력매수) | 반도체   |
| 012450 | 한화에어로스페이스 | v2        | 100    | A (강력매수) | 방산     |
| 035420 | NAVER              | v3        | 100    | A (강력매수) | 플랫폼   |
| 000720 | 현대건설           | v1        | 100    | A (강력매수) | 건설     |
| 009150 | 삼성전기           | v2        | 81.25  | A (강력매수) | 전자부품 |
| 329180 | HD현대중공업       | v3        | 79.5   | B (매수)     | 조선     |
| 005930 | 삼성전자           | v2        | 79.0   | B (매수)     | 반도체   |
| 010120 | LS ELECTRIC        | v4        | 79.0   | B (매수)     | 전력기기 |
| 034020 | 두산에너빌리티     | v3        | 77.0   | B (매수)     | 에너지   |
| 052690 | 한전기술           | v1        | 73.0   | B (매수)     | 원자력   |
| 035720 | 카카오             | v3        | 72.0   | B (매수)     | 플랫폼   |
| 466100 | 클로봇             | v2        | 71.0   | B (매수)     | 로봇     |

### DailyPick 자동 필터링 시스템

`web/scripts/build_daily_pick.mjs`가 매일 실행:

- 전체 분석 완료 종목 중 스코어 80+ 자동 필터링
- 현재 후보 풀: 49건 (한국+미국)
- 출력: `web/src/data/daily_pick.json`
- 알고 엔진에서 이 JSON을 종목 풀 소스로 직접 참조 가능

---

## 4. 데이터 소스 + API 정보

### 현재 보유 데이터 파이프라인

| 소스               | 데이터                                        | API/방식          | 인증        | 비용 |
| ------------------ | --------------------------------------------- | ----------------- | ----------- | ---- |
| yfinance           | 주가, 지수, 환율, 원자재 (일봉)               | Python 라이브러리 | 불필요      | 무료 |
| DART               | 공시, 재무제표, 기업개요                      | REST API          | API 키 보유 | 무료 |
| FRED               | 매크로 15개 시리즈 (FFR, 10Y, CPI, 실업률 등) | REST API          | API 키 보유 | 무료 |
| Polymarket         | 예측 시장 확률 (Fed/지정학/경제/크립토)       | Gamma API         | 불필요      | 무료 |
| openinsider.com    | 인사이더 클러스터 매수 (Form 4)               | 웹 스크랩         | 불필요      | 무료 |
| CNN/Alternative.me | Fear & Greed Index (주식+크립토)              | REST API          | 불필요      | 무료 |
| Dataroma/SEC EDGAR | 13F 거물 포지션 (분기별)                      | 웹 스크랩         | 불필요      | 무료 |

### 알고 엔진이 추가로 필요한 데이터

| 데이터         | 용도               | 후보 소스                          |
| -------------- | ------------------ | ---------------------------------- |
| 분봉/틱 데이터 | 일중 매매 시그널   | 토스뱅크 API (확인 필요)           |
| 실시간 호가    | 주문 집행          | 토스뱅크 API WebSocket (확인 필요) |
| 체결 데이터    | 수급 분석          | 토스뱅크 API 또는 KRX OpenData     |
| 신용잔고       | 레버리지 위험 감지 | KRX, 금투협                        |

---

## 5. Knowledge Base 구조 (알고 엔진 참조 가능)

### 시장 데이터 (knowledge-base/market/)

| 파일                  | 내용                                              | 갱신 주기    |
| --------------------- | ------------------------------------------------- | ------------ |
| daily_snapshot.md     | 미국/아시아 지수, 환율, 원자재, 채권, 크립토 종합 | 매 브리핑 시 |
| prediction_markets.md | Polymarket 예측 확률 (Fed/지정학/경제)            | 매 브리핑 시 |
| correlation_matrix.md | 6쌍 상관계수 30D/90D + Z-score                    | 이브닝/주간  |
| surprise_index.md     | 경제 서프라이즈 Beat/Miss 누적                    | 이브닝/주간  |
| guru_positions.md     | 거물 8인 13F 포지션                               | 분기별       |
| economic_calendar.md  | 이번 주 경제 일정                                 | 주간         |
| fear_greed.json       | CNN F&G + Crypto F&G                              | 매 빌드      |

### 매크로 데이터 (knowledge-base/macro/)

| 파일                   | 내용                                                     |
| ---------------------- | -------------------------------------------------------- |
| fred_snapshot.json     | FRED 15개 시리즈 (FFR, 10Y, CPI, 실업률, HY 스프레드 등) |
| us_monetary_policy.md  | Fed 금리 정책, QT/QE, 인플레이션 전망                    |
| korea_economy.md       | 한국 GDP, 수출, 환율, 한국은행 기준금리                  |
| geopolitics.md         | 지정학 리스크 (미중, 중동, 우크라 등)                    |
| global_risk_factors.md | Top 5 글로벌 리스크 순위                                 |

### 산업 데이터 (knowledge-base/industry/)

26개 섹터별 현황 파일:
semiconductor, energy, defense, bio_pharma, ai, auto, capex, smr, banking_capital,
consumer_retail, infrastructure, logistics, robotics, quantum, space, 등

### 포트폴리오 데이터 (knowledge-base/portfolio/)

| 파일                 | 내용                                                  |
| -------------------- | ----------------------------------------------------- |
| model_portfolios.md  | 4종 모델 포트폴리오 (안전/중립/공격/배당) 구성 + 비중 |
| user_portfolio.md    | 사용자 실제 보유 종목 + 프로파일                      |
| insider_signals.json | 인사이더 클러스터 매수 Top 5                          |

---

## 6. 모델 포트폴리오 4종 자산 배분

### 안전형 (Conservative)

| 자산군             | 비중 | 대표 종목                            |
| ------------------ | ---- | ------------------------------------ |
| 미국 중단기 국채   | 25%  | IEF, SHY, VGIT                       |
| 투자등급 회사채    | 12%  | LQD, VCIT                            |
| 배당 성장 ETF      | 13%  | SCHD, VIG, DGRO                      |
| 국내 우량주/배당주 | 12%  | KODEX 200 TR, 삼성전자, KODEX 고배당 |
| 금 (Gold)          | 13%  | GLD, IAU                             |
| 달러 MMF/단기 국채 | 18%  | SGOV, BIL                            |
| 글로벌 리츠        | 5%   | VNQI, REET                           |
| 헬스케어 방어      | 2%   | XLV, VHT                             |

### 공격형 (Aggressive)

빅테크 30%, AI/반도체 25%, 방산 10%, 크립토 5%, 성장주 20%, 현금 10%

### 중립형 (Balanced)

S&P(VOO) 28%, 국채 20%, 배당 15%, 국내 17%, Gold 10%, 현금 10%

### 배당형 (Dividend)

고배당 ETF 30%, 커버드콜(JEPI/JEPQ) 15%, 리츠 10%, 국채 20%, 배당 성장 15%, 현금 10%

---

## 7. 현재 매크로 환경 진단 (2026-05-19 기준)

| 변수            | 상태                                           | 알고 엔진 시사점                         |
| --------------- | ---------------------------------------------- | ---------------------------------------- |
| S&P 500         | 7,408 (트리플 마일스톤 이탈, 디레버리징 5일차) | 미국 연동 한국주 하방 압력               |
| KOSPI           | 7,516 (+0.31%, 미약 반등)                      | KOSDAQ -1.66% 괴리 — 소형주 주의         |
| USD/KRW         | 1,501 (1,500 돌파 유지)                        | 외인 이탈 가속 구간, 환 리스크 반영 필요 |
| VIX             | 19.06 (20 임계선 1pt 미만)                     | 변동성 자기 강화 루프 임박               |
| 30Y UST         | 5.13% (3일 연속 5%+ 고착)                      | 밸류에이션 하방 압력 구조적              |
| Gold            | $4,543                                         | 안전자산 헤지 효율 높아진 상태           |
| Fed 금리        | 3.64% (동결 3회차)                             | CPI 3.8%로 인하 불가                     |
| 경기 서프라이즈 | 5연속 하회 + CPI 상방                          | 스태그플레이션 패턴 고착                 |

### 이번 주 핵심 이벤트

| 일자  | 이벤트                            | 영향             |
| ----- | --------------------------------- | ---------------- |
| 5/19~ | 13F Q1 순차 공개 (Buffett 포지션) | 바닥/천장 시그널 |
| 5/22  | NVIDIA Q1 실적 ($43.5B 컨센)      | 반도체 방향 결정 |
| 미정  | Warsh 신임 Fed 의장 첫 발언       | 금리 방향        |

### Polymarket 예측 확률 (활용 방법)

알고 엔진이 `knowledge-base/market/prediction_markets.md` 를 참조하면:

- Fed 금리 결정 확률 → 금리 민감 종목(리츠, 은행, 성장주) 포지션 조절
- 경기침체 확률 → 방어/경기순환 섹터 비중 자동 조정
- 지정학 이벤트 확률 → 방산/에너지 종목 가중치 반영

적중률: 1개월 전 90.4%, 1일 전 95.8%, 거래량 $100K+ 마켓 84%
가중치: Polymarket 70% + 자체 판단 30% (briefing-lead 규칙)

---

## 8. 파일 경로 맵 (알고 엔진에서 직접 참조 가능한 파일)

```
종목분석 에이전트/
├── analysis/{ticker}_{name}_v{N}/
│   ├── scorecard.md              # 10항목 스코어카드 + 등급 + ATR 손절/목표가
│   ├── company.md                # 기업개요 + Moat 분석
│   ├── financial.md              # 재무분석 + 밸류에이션
│   ├── business.md               # 산업 트렌드 + 경쟁구도
│   ├── momentum.md               # 수급 + 컨센서스 + 기술적 지표
│   ├── risk.md                   # 리스크 식별 + 정량화
│   └── data.json                 # 수집 원본 데이터 (가격, 재무, 매크로)
│
├── knowledge-base/
│   ├── market/daily_snapshot.md   # 시장 전체 스냅샷
│   ├── market/prediction_markets.md  # Polymarket 예측 확률
│   ├── market/correlation_matrix.md  # 자산 상관계수
│   ├── market/fear_greed.json    # F&G 인덱스
│   ├── macro/fred_snapshot.json  # FRED 매크로 15종
│   ├── portfolio/model_portfolios.md  # 4종 모델 포트폴리오
│   ├── portfolio/insider_signals.json # 인사이더 매수 시그널
│   └── industry/{sector}.md      # 26개 섹터별 현황
│
├── web/src/data/
│   ├── daily_pick.json           # 스코어 80+ 종목 풀 (매일 갱신)
│   ├── manifest.json             # 전체 리포트 목록
│   └── kb.json                   # KB 데이터 압축본
│
└── reference/
    ├── source_registry.md        # 데이터 소스 등록부
    └── stop-loss-rules.md        # 손절/목표가 계산 SSOT
```

---

## 신호 파이프라인 v2 변경 통지 (2026-06-12 — 종목분석 에이전트)

**상황**: stock_scores.json 이 2026-05-19 이후 멈춰 있던 문제 해소. 원인은 ① 일일 빌드 스케줄 자체가 부재 ② 자체 점수 추출 휴리스틱 오염 (INTC 13 등) ③ analysis_date 대부분 null → 그쪽 신선도 게이트가 전 종목 차단.

**변경 사항** (스키마 하위 호환 — 기존 필드 전부 유지):

1. **소스 교체**: analysis/_history/*_timeline.json (재분석 시스템 단일 진실) + 웹 대시보드와 동일한 scorecard 파서. analysis_date 결측 0/111 (이전: 대부분 null).
2. **신규 필드** `grade_kr` (강력매수/매수/중립/매도), `source` (헤더). 기존 `grade` 는 동일 레터 매핑 (A/B/C/F) 유지.
3. **비상장 제외**: ANTHROPIC·SPACEX 는 매매 불가 → 목록에서 제거 (이전엔 eligible 진입 위험).
4. **자동 빌드**: launchd `com.stockanalyst.signals` 매일 **KST 15:25** (그쪽 1차 점검 15:40 전). 실패 시 알림 + watchdog 이 매일 신선도 검증 (stale 시 high 알림).
5. macro_regime.json 의 FRED 입력도 2026-06-12 부로 일일 갱신 복구 (5/30~6/12 stale 였음).

**그쪽 확인 권장**: 신선도 게이트 기준일을 `analysis_date` 로 쓰고 있다면 그대로 호환. `stale` 필드(30일 기준)도 동일 의미로 재계산됨.
