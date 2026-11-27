# BLIND 재분석 스펙 — 2026-11-28 (10일 임계, staock_update 슬롯, /재분석실행 10 10)

## 대상 (11-18 코호트, 정확히 10일 경과 · ANTHROPIC 비상장 standing 제외)

| 티커 | 폴더                        | next_v | prev_v(미참조) | 타입               |
| ---- | --------------------------- | ------ | -------------- | ------------------ |
| FCX  | FCX_FreeportMcMoRan_v16     | 16     | 15             | 주식(구리광산)     |
| DUK  | DUK_DukeEnergy_v18          | 18     | 17             | 주식(전력유틸)     |
| BWXT | BWXT_BWXTechnologies_v18    | 18     | 17             | 주식(원자력·방산)  |
| ETN  | ETN_Eaton_v22               | 22     | 21             | 주식(전력관리)     |
| GE   | GE_GEAerospace_v23          | 23     | 22             | 주식(항공엔진)     |
| CVX  | CVX_Chevron_v24             | 24     | 23             | 주식(석유메이저)   |
| CCJ  | CCJ_Cameco_v18              | 18     | 17             | 주식(우라늄)       |
| COST | COST_Costco_v24             | 24     | 23             | 주식(소매)         |
| COIN | COIN_Coinbase_v24           | 24     | 23             | 주식(크립토거래소) |
| CEG  | CEG_ConstellationEnergy_v22 | 22     | 21             | 주식(원자력유틸)   |

## BLIND 원칙 (앵커링 구조적 차단)

- 분석가는 자기 종목의 **이전 버전 폴더(v{prev}) · 이전 reports/\*.html 을 절대 read 금지.**
- 입력은 (1) 자기 폴더 `data.json` (yfinance 중앙수집·아티팩트 교정 완료) + (2) 아래 매크로 레짐 + (3) 공개 일반지식.
- "이전엔 X였으나" 식 비교 문장 금지 — 이전 모름. 현재 데이터로부터 독립 추론.
- WebSearch 미바인딩 슬롯 — 추가 웹수집 금지, data.json·일반지식만. 환각 금지, 불확실은 confidence 하향.

## 매크로 레짐 (2026-11-28 00:05 KST 실측, fred_snapshot·fear_greed)

- **CNN 공포탐욕 21.7 (극단적 공포)** — 전일 종가 15.6, 1주 전 18.6, 1개월 전 32.9. 11-27(금) 저녁 과매도 대반등(KOSPI +4.3%·KOSDAQ +8.1%·BTC $60K 돌파·VIX 하락)으로 심리 소폭 개선, 그러나 여전히 극단 공포권.
- 10Y 4.91% (1주 전 5.10%↓), 2Y 4.63% (1주 전 4.80%↓) — 금리 완화(불 스티프닝). 10Y-2Y +0.24(정상화).
- Fed Funds 3.88% 동결(매파적 동결 — 공포에도 인하 안 함). 12/9 FOMC 임박. **인하 전제 금지.**
- 크립토 공포탐욕 12 (극단 공포). BTC 11-27 저녁 $60K 재돌파(과매도 반등). 리스크오프 전반 완화 초기.
- 서사: AI capex 디레버리징 지속 → 성장주·고멀티플 이탈·방어/가치 회전. 11-27 반등은 과매도 되돌림 성격(바닥 확정 아님). 추수감사절 단축주(11-26 목 휴장·11-27 금 조기폐장) 종료. **미 최신 종가는 11-27(금) 조기폐장 세션 기준** (data.json price_as_of 참조).

## 산출물 (종목당 2파일, 폴더 안에)

1. `scorecard.md` — 본문(산문) + 10항목 가중표 + 아래 **필수 라인 포맷**:
   - 가중치 고정(앵커링·분산 방지): 경제적 해자 14 · 성장성 12 · 수익성 11 · 재무 건전성 10 · 밸류에이션 13 · 모멘텀·기술 9 · 리스크(하방) 8 · 산업·경쟁 지위 8 · 경영·자본배분 8 · 매크로 적합성 7 (합 100)
   - `**종합 점수: {N} / 100**` (정수, 숫자 직후 ` / 100`. 합산식 `=a+b+..=X/100` 금지)
   - `**투자등급: {강력매수|매수|중립|매도|강력매도}**` (enum 밖 금지. 비중축소/비중확대류 → 최근접 tier)
   - `- **목표주가: {통화기호}{숫자}**` (미국주 `$` 필수·쉼표 OK)
   - `- 손절가: {통화기호}{숫자}` (data.json quote.stop_loss_2atr 사용)
   - `## § Confidence Interval` (Bear/Base/Bull 3시나리오 — 산문)
   - `## § 약한 가정 3개 (Most Fragile Assumptions)` (각 가정 + 반증 시 영향 1줄)

2. `_report_data.json` — 렌더용. 아래 **정확 스키마**(값 타입 엄수):

```json
{
  "ticker": "FCX",
  "name": "프리포트맥모란(FCX) — 재분석 v16 (이전 비교 미포함)",
  "date": "2026-11-28",
  "asset_type": "주식",
  "currency": "$",
  "score": 64,
  "grade": "중립",
  "current_price": 50.41,
  "market_cap": "$72B",
  "per": "trailing 21.2 / fwd 12.0",
  "low52": 42.31,
  "high52": 80.24,
  "atr": 3.28,
  "stop_loss": 43.85,
  "target_price": 62,
  "scorecard_items": [["경제적 해자",7],["성장성",6],["수익성",6],["재무 건전성",7],["밸류에이션",7],["모멘텀·기술",5],["리스크(하방)",6],["산업·경쟁 지위",7],["경영·자본배분",7],["매크로 적합성",6]],
  "extra_kpis": [["배당수익률","1.24%"],["베타","..."],["ROE","..."],["EV/EBITDA","..."],["PEG","..."],["잉여현금흐름(TTM)","..."]],
  "executive_summary": "…",
  "company_overview": "…",
  "moat_rating": "넓음(Wide)/보통(Narrow)/없음 …",
  "moat_details": "…",
  "financial_analysis": "…",
  "valuation": "…",
  "momentum": "…",
  "business_analysis": "…",
  "risk_summary": "…",
  "strategy": "…",
  "risks": [{"name":"…","level":"높음/중간/낮음","impact":"…","desc":"…"}, … 4~5개],
  "thesis": {"claim":"…","support":"…","falsifier":"…"},
  "custom_sections": [
    {"title":"§ Confidence Interval","content":"Bear: … / Base: … / Bull: …"},
    {"title":"§ 약한 가정 3개 (Most Fragile Assumptions)","content":"1. … / 2. … / 3. …"}
  ],
  "artifact_notes": []
}
```

### 타입 함정 (메모리 기반 — 위반 시 렌더 크래시)

- 가격 필드(current_price·low52·high52·atr·stop_loss·target_price)는 **숫자**(따옴표 금지).
- `scorecard_items` 점수는 **0~10** (0~100 아님). top-level `score`만 0~100. CANON 이름/순서 엄수.
- `thesis` 는 **dict** (claim/support/falsifier). 문자열로 쓰면 크래시.
- `custom_sections` CI 는 **산문** (마크다운 표 `| … |` 금지 — HTML 리터럴 파이프 노출).
- `extra_kpis` 는 `[label,value]` pair 리스트.
- scorecard.md 종합점수와 _report_data.json score 는 **동일 정수**. 등급·목표가도 두 파일 일치.
