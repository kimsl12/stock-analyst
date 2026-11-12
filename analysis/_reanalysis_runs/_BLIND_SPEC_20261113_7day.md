# BLIND 재분석 공유 스펙 — 2026-11-13 (7일 임계, stock_update-2 슬롯)

> 이 문서는 각 종목 BLIND 분석가(general-purpose)가 **자기 종목 `data.json` 과 함께** 읽는 공유 스펙이다.
> **이전 버전(v{N-1}) 스코어카드·리포트·\_report_data.json 은 절대 읽지 않는다.** 앵커링 차단 = 구조적 분리.

## 0. 절대 규칙

1. **입력은 딱 2개:** (a) 이 스펙 문서, (b) 배정된 `analysis/{폴더}_v{N}/data.json`.
   - `analysis/{폴더}_v{N-1}/`, `reports/{티커}_*.html`, 과거 timeline 등 **이전 산출물 Read/Glob 금지.**
   - "이전 분석에서는 X였으나" 같은 비교 문장 금지 — 이전을 모른다.
2. **출력도 딱 2개** (배정 폴더에 Write):
   - `scorecard.md` — 아래 §2 형식 **정확히** 준수 (파서 호환).
   - `_report_data.json` — 아래 §3 스키마 **정확히** 준수 (render 소비).
   - 중간 .md(company/financial/...) 생략. 모든 산문은 `_report_data.json` 필드에 담는다.
3. **등급 enum 엄수:** `강력매수 / 매수 / 중립 / 매도 / 강력매도` 5개만. "비중축소·비중확대·보유·언더웨이트" 등 금지.
   레버리지/인버스 ETF도 이 5개 중 최근접 등급으로. (예: 하방 2배 레버리지 비적합 → 매도)
4. **숫자 필드는 숫자(float):** `_report_data.json` 의 current_price·low52·high52·atr·stop_loss·target_price·score 는
   따옴표 없는 숫자. market_cap·per·extra_kpis 값은 문자열 허용.
5. **목표가 통화기호 필수:** scorecard 의 `- **목표주가: $X**` 는 반드시 `$`(미국) 기호 포함(ETF 포함).

## 1. 매크로 레짐 (2026-11-13 기준 — 전 종목 공통 반영)

- **리스크오프 소화 국면.** 11/5~9 반도체 AI 디레버리징 급락 → 11/10~12 안도 랠리(바닥 3일 확정) → 11/12 '첫 소화일'(급등 자산 되돌림: 대만 −2.6%·하이닉스 −1.8%·NQ −0.8%).
- **매파 Fed:** 12/9 FOMC 임박, 2026 인하 테이블 밖, 10Y ~4.9%대 고착·재급등 압력, Core PCE 여전히 높음. 고베타·고멀티플 성장주 멀티플 압박 지속.
- **약한 채 남은 축:** 10Y·크립토·금(리스크 재평가 미완). VIX 중고점.
- 반영 원칙: 고베타/고밸류/금리민감 종목은 **매크로 적합성·모멘텀 저점수**로 구조 반영. 방어·가치·저베타는 상대 강점. 비둘기 반사 오독 금지(시뮬 2026 = 매파).

## 2. scorecard.md 형식 (정확 준수 — 파서 의존)

```markdown
# {티커} ({한글명} / {영문명}) — 재분석 v{N} 스코어카드

- **기준일:** 2026-11-13
- **현재가:** ${현재가} ({price_as_of} 종가 기준)
- **52주 레인지:** ${52L} ~ ${52H} (레인지 위치 {range_position_pct}%)
- **시가총액:** {market_cap} · PER trailing {x}/forward {y} · 베타 {beta}
- **ATR(14):** ${atr} ({atr_pct}%)

> ※ BLIND 재분석: 이전 버전 미참조. 현재 데이터·공개지식만으로 독립 추론.

---

## 10항목 가중 스코어카드

(가중점수 = 점수(0~10) × 가중치 / 10)

| 항목           | 점수(0~10) | 가중치  | 가중점수   |
| -------------- | ---------- | ------- | ---------- |
| 경제적 해자    | {0~10}     | 15      | {계산}     |
| 성장성         | {0~10}     | 10      | {계산}     |
| 수익성         | {0~10}     | 12      | {계산}     |
| 재무 건전성    | {0~10}     | 10      | {계산}     |
| 밸류에이션     | {0~10}     | 13      | {계산}     |
| 모멘텀·기술    | {0~10}     | 8       | {계산}     |
| 리스크(하방)   | {0~10}     | 10      | {계산}     |
| 산업·경쟁 지위 | {0~10}     | 12      | {계산}     |
| 경영·자본배분  | {0~10}     | 5       | {계산}     |
| 매크로 적합성  | {0~10}     | 5       | {계산}     |
| **합계**       |            | **100** | **{합계}** |

---

**종합 점수: {정수 N} / 100**

**투자등급: {enum 등급}**

- **목표주가: ${목표가}** (상승여력 {±%})
  - 근거: {1~2문장}
- **손절선(2ATR): ${손절가}** — 현재가 대비 {-%}

---

## 항목별 근거 요약

**경제적 해자 ({점수}):** {근거}
...(10항목 각 1~3문장)...

---

## § Confidence Interval

- **Bear (${X}):** {조건·근거}. {±%}.
- **Base (${Y}):** {조건·근거}. {±%} (목표가 = 중심).
- **Bull (${Z}):** {조건·근거}. {±%}.

---

## § 약한 가정 3개 (Most Fragile Assumptions)

1. **{가정}** — {설명}. — 반증 시 영향: {1줄}.
2. **{가정}** — {설명}. — 반증 시 영향: {1줄}.
3. **{가정}** — {설명}. — 반증 시 영향: {1줄}.
```

**ETF 주의:** 10항목 중 '경제적 해자·경영·자본배분' 등은 ETF 성격에 맞게 해석(지수 추종 효율·보수율·추적오차·유동성·구성). consensus target=None 은 ETF 정상 — 목표가는 NAV·기술적 레인지·기초지수 밸류로 직접 산출하되 `- **목표주가: $X**` 정형 유지.

## 3. _report_data.json 스키마 (정확 준수 — render 소비)

```json
{
  "ticker": "{티커}",
  "name": "{한글명}({티커}) — 재분석 v{N} (이전 비교 미포함)",
  "date": "2026-11-13",
  "asset_type": "주식", // ETF 는 "ETF"
  "currency": "$",
  "score": 70, // 정수 (scorecard 종합점수와 일치)
  "grade": "매수", // enum
  "current_price": 63.76, // float (data.json quote.current_price)
  "market_cap": "$261.8B", // 문자열 OK
  "per": "trailing 18.4 / fwd 16.9", // 문자열 (ETF 는 "N/A (ETF)")
  "low52": 61.39, // float
  "high52": 116.73, // float
  "atr": 1.81, // float (data.json quote.atr_14)
  "stop_loss": 60.14, // float (data.json quote.stop_loss_2atr)
  "target_price": 78, // float (scorecard 목표가와 일치)
  "scorecard_items": [
    { "name": "경제적 해자", "score": 8.0 },
    { "name": "성장성", "score": 7.0 },
    { "name": "수익성", "score": 9.0 },
    { "name": "재무 건전성", "score": 7.5 },
    { "name": "밸류에이션", "score": 7.5 },
    { "name": "모멘텀·기술", "score": 2.5 },
    { "name": "리스크(하방)", "score": 5.5 },
    { "name": "산업·경쟁 지위", "score": 8.5 },
    { "name": "경영·자본배분", "score": 8.0 },
    { "name": "매크로 적합성", "score": 3.5 }
  ], // 0~10 스케일, 10개, scorecard 표와 일치
  "extra_kpis": [
    { "name": "배당수익률", "value": "0.00%" },
    { "name": "목표가 상승여력", "value": "+22.3%" }
  ],
  "executive_summary": "{4~7문장 종합}",
  "company_overview": "{3~5문장}",
  "moat_rating": "{예: 넓음 (Wide)}",
  "moat_details": "{3~5문장}",
  "financial_analysis": "{4~6문장, 분기 매출 추이·마진·재무}",
  "valuation": "{3~5문장, 멀티플·목표가 근거}",
  "momentum": "{3~4문장, 이평선·레인지위치·수급}",
  "business_analysis": "{3~5문장, 산업·경쟁}",
  "risk_summary": "{3~5문장}",
  "strategy": "{3~5문장, 진입·손절·보유기간}",
  "risks": [
    {
      "name": "{리스크}",
      "level": "높음|중간|낮음",
      "impact": "{한줄}",
      "desc": "{1~2문장}"
    }
    // 4~5개
  ],
  "thesis": {
    "claim": "{핵심 논지 1~2문장}",
    "consensus": "{컨센서스 요약 — 애널리스트 수·목표 평균/중앙/고/저. ETF 는 '애널리스트 컨센서스 없음(ETF)' + 기초지수 전망}"
  },
  "custom_sections": [
    {
      "title": "Confidence Interval",
      "content": "Bear/Base/Bull 3줄(\\n 구분)"
    },
    { "title": "약한 가정 3개", "content": "1.~3. (\\n 구분)" }
  ],
  "artifact_notes": [] // data.json artifact_notes 가 있으면 요약 반영
}
```

## 4. 데이터 유의 (data.json 그대로 신뢰하되)

- `artifact_notes` 배열에 교정 내역(배당 스케일·52주·ETF 비용률)이 있으면 본문에 반영.
- yfinance FCF > 영업현금흐름이면 아티팩트 → 영업현금흐름 사용.
- 트레일링 EPS 일회성 왜곡 의심 시 forward/영업이익 기준 사용.
- ETF: expense_ratio_pct 는 이미 실측 교정됨(SLV 0.50·SPY 0.0945·VNQ 0.13·SOXX 0.35). consensus target=None 정상.
