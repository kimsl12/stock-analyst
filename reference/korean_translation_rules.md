---
updated: 2026-05-09
category: rules
applies_to: [briefing-lead, briefing-report-generator, stock-analyst-lead, report-generator, scorecard-strategist, 5명 분석가]
---

# 한국어 강제 변환 규칙 (v3.14)

> 본 문서는 모든 분석·리포트 본문의 한국어 작성 강제력을 높인다.
> v3.11 인라인 규칙이 잘 안 지켜져서 (사용자 지적, 2026-05-09) 매핑 사전 + 검증 룰을 단일 source 로 분리.

## 원칙

본문은 **한국어 작성**. 다음 3가지 예외만 영문 원문 유지, 그 외 모든 영어 표현은 매핑 사전대로 한글 옮김.

1. **고유명사** — 회사·제품·인덱스·티커·인물명 (예: NVIDIA, Trainium2, S&P 500, Powell)
2. **표준 약어** — 한글 변환 시 의미가 흐려지는 업계 통용 약어 (예: ETF, PER, PBR, ROE, EPS, ATR, RSI, FCF, DCF, EV/EBITDA, YoY, QoQ, GDP, CPI, PCE, FOMC, AI, GPU, ASIC, TAM, SAM, NAV, AUM, TER, NIM, OPM)
3. **인용구·영문 원문 발언** — 외신·SEC 공시·임원 발언 직접 인용

## 매핑 사전 (강제 변환)

### 투자 등급 / 평가

| 영어 | 한글 |
|------|------|
| Strong Buy | 강력매수 |
| Buy | 매수 |
| Hold / Neutral | 중립 (또는 보유) |
| Sell | 매도 |
| Strong Sell | 강력매도 |
| Overweight | 비중확대 |
| Underweight | 비중축소 |
| Equal Weight | 동일비중 (또는 중립) |
| Outperform | 시장수익률 상회 |
| Underperform | 시장수익률 하회 |
| Top Pick | 최선호 |
| Conviction Buy | 적극 매수 |

### 시장 방향 / 시나리오

| 영어 | 한글 |
|------|------|
| Bull / Bullish | 강세 (또는 상승) |
| Bear / Bearish | 약세 (또는 하락) |
| Bull case | 강세 시나리오 |
| Bear case | 약세 시나리오 |
| Base case | 기본 시나리오 |
| Tail risk / Tail case | 꼬리 위험 (또는 극단 시나리오) |
| Stress case | 스트레스 시나리오 |
| Devil's Advocate | 반대 관점 (또는 회의론) |
| Goldilocks | 골디락스 (음역 OK — 이미 한글 정착) |
| Stagflation | 스태그플레이션 (음역 OK) |
| Reflation | 리플레이션 (음역 OK) |
| Risk-on / Risk-off | 위험 선호 / 위험 회피 |

### 실적 / 컨센서스

| 영어 | 한글 |
|------|------|
| Beat | 상회 (또는 어닝 서프라이즈) |
| Miss | 하회 (또는 어닝 미스) |
| In-line | 부합 |
| Guidance | 가이던스 (음역 OK — 표준 약어 가까움) |
| Catalyst | 촉매 (또는 계기) |
| Trigger | 트리거 (또는 계기, 신호) |
| Headwind | 역풍 (또는 부정적 요인) |
| Tailwind | 순풍 (또는 긍정적 요인) |

### Moat / 경쟁우위

| 영어 | 한글 |
|------|------|
| Wide Moat | 넓은 해자 (또는 강한 경쟁우위) |
| Narrow Moat | 좁은 해자 (또는 보통 경쟁우위) |
| No Moat | 해자 없음 |
| Network Effect | 네트워크 효과 |
| Switching Cost | 전환 비용 |
| Pricing Power | 가격 결정력 |

### 가격 / 손익 표현

| 영어 | 한글 |
|------|------|
| Initial Stop | 초기 손절가 |
| Trailing Stop | 추적 손절가 |
| Take Profit | 익절 |
| Stop Loss | 손절 |
| Risk:Reward (R:R) | 손익비 (R:R 표기는 약어로 OK) |
| Drawdown | 최대 낙폭 |
| Volatility Decay | 변동성 감소 (레버리지 ETF 의 경우) |
| Profit Taking | 차익실현 |
| Capitulation | 항복 매도 |

### 매크로 / 정책

| 영어 | 한글 |
|------|------|
| Soft Landing | 연착륙 |
| Hard Landing | 경착륙 |
| Hawkish | 매파적 |
| Dovish | 비둘기파적 |
| Hike / Cut | 인상 / 인하 |
| Pause | 동결 |
| Yield Curve | 수익률 곡선 |
| Inversion | 역전 (장단기) |
| Quantitative Easing (QE) | 양적 완화 |
| Quantitative Tightening (QT) | 양적 긴축 |

### 기술 / AI / 반도체 (도메인)

| 영어 | 한글 |
|------|------|
| Hyperscaler | 하이퍼스케일러 (음역 OK) |
| Capex / OpEx | 자본 지출 / 운영 비용 (CAPEX/OPEX 약어는 OK) |
| Foundry | 파운드리 (음역 OK) |
| Fabless | 팹리스 (음역 OK) |
| Wafer | 웨이퍼 (음역 OK) |
| Packaging | 패키징 |
| Yield | 수율 |
| Lithography | 노광 |

### 일반 (자주 슬립)

| 영어 | 한글 |
|------|------|
| approximately / about | 약 (또는 대략) |
| slightly | 약간 |
| significantly | 크게 |
| roughly | 대략 |
| momentum | 모멘텀 (음역 OK) |
| portfolio | 포트폴리오 (음역 OK) |
| consensus | 컨센서스 (음역 OK) |
| valuation | 밸류에이션 (음역 OK) |
| dividend | 배당 |
| dividend yield | 배당수익률 |
| earnings | 실적 |
| revenue | 매출 |
| profit | 이익 |
| margin | 마진 |
| exposure | 노출도 (또는 비중) |
| allocation | 배분 (또는 비중) |
| hedging | 헤지 (또는 헤지 거래) |

## 자가 검증 (HTML 출력 후)

```bash
HTML="reports/{종류}/{파일명}.html"
FAIL=()

# 1. 매핑 사전 영어 표현 (등급·시나리오) — 본문 안에 영문 잔류 검사
# (단 코드 블록·script·style 안은 제외 — 사용자 보는 본문만)
BODY=$(awk '/<body>/,/<\/body>/' "$HTML" | sed 's/<[^>]*>//g; s/&lt;[^&]*&gt;//g')

for kw in "Strong Buy" "Strong Sell" "Buy " "Hold" "Sell " "Bullish" "Bearish" \
          "Bull case" "Bear case" "Base case" "Top Pick" "Outperform" "Underperform" \
          "Beat " "Miss " "Catalyst" "Trigger" "Headwind" "Tailwind" \
          "Wide Moat" "Narrow Moat" "Soft Landing" "Hawkish" "Dovish" \
          "approximately" "significantly" "Take Profit" "Stop Loss"; do
  echo "$BODY" | grep -qF "$kw" && FAIL+=("$kw")
done

# 2. 본문 한글 비중 80% 이상 (기존 50자 → 비율 측정으로 강화)
KCHARS=$(echo "$BODY" | grep -oE '[가-힣]' | wc -l)
# 분모도 분자와 동일하게 grep -oE | wc -l 로 "문자 수" 카운트.
# (tr -cd | wc -c 는 바이트 수 → 한글 3바이트로 분모 부풀려져 비율 1/3 왜곡. wc -m 은 로케일 미설정 시 바이트 폴백되므로 사용 금지)
TOTAL=$(echo "$BODY" | grep -oE '[가-힣A-Za-z]' | wc -l)
[ "$TOTAL" -gt 0 ] && {
  RATIO=$(( KCHARS * 100 / TOTAL ))
  [ "$RATIO" -lt 80 ] && FAIL+=("korean-ratio-${RATIO}%")
}

if [ ${#FAIL[@]} -gt 0 ]; then
  echo "⚠️ 한국어 검증 실패: ${FAIL[*]}"
  echo "→ 매핑 사전 따라 본문 자체 교체 후 재출력 (최대 1회 재시도)"
fi
```

## 위반 시 처리

1. **자가 검증 실패** → 본문 영어 표현을 매핑 사전대로 한글 교체 → 재출력
2. **재시도 1회 실패** → briefing-lead 에 "한국어 룰 위반 ${영어 표현 목록}" 보고 후 lead 가 재작성
3. **3가지 예외에 해당하지 않으면 무조건 한글로** — "고유명사인지 의심스러우면 한글로" (예: 회사명·티커는 영문 OK, "Top Pick" 은 한글)

## 메모

- 본 매핑은 **본문에 적용**. CSS 클래스명·HTML 속성·코드 블록은 영문 유지 OK.
- 표 헤더(예: `Bull | Base | Bear`)도 한글 헤더로: `강세 | 기본 | 약세`.
- 종목 프로필 라벨에 영문 등급 있으면 한글로 변환 (예: "Buy" 셀 → "매수").
- 약어 사용 (PER, ROE, ATR 등) 은 v3.11 예외 그대로 유지.
