# BLIND 재분석 스펙 — 2026-11-27 (10일 임계, staock_update 슬롯, /재분석실행 10 10)

## 대상 (11-17 코호트, 정확히 10일 경과 · ANTHROPIC 184일 비상장 standing 제외)

| 티커 | 폴더                             | next_v | prev_v(미참조) | 타입            |
| ---- | -------------------------------- | ------ | -------------- | --------------- |
| TMO  | TMO_ThermoFisher_v16             | 16     | 15             | 주식(생명과학)  |
| VMC  | VMC_VulcanMaterials_v18          | 18     | 17             | 주식(건자재)    |
| T    | T_ATT_v23                        | 23     | 22             | 주식(통신)      |
| UNH  | UNH_UnitedHealth_v16             | 16     | 15             | 주식(헬스케어)  |
| TXN  | TXN_TexasInstruments_v23         | 23     | 22             | 주식(반도체)    |
| TMUS | TMUS_TMobile_v24                 | 24     | 23             | 주식(통신)      |
| UNP  | UNP_UnionPacific_v23             | 23     | 22             | 주식(철도)      |
| VEA  | VEA_VanguardDevelopedMarkets_v15 | 15     | 14             | ETF(선진국)     |
| USMV | USMV_iSharesMinVol_v23           | 23     | 22             | ETF(최소변동성) |
| VOO  | VOO_VanguardSP500_v23            | 23     | 22             | ETF(S&P500)     |

## BLIND 원칙 (앵커링 구조적 차단)

- 분석가는 자기 종목의 **이전 버전 폴더(v{prev}) · 이전 reports/\*.html 을 절대 read 금지.**
- 입력은 (1) 자기 폴더 `data.json` (yfinance 중앙수집·아티팩트 교정 완료) + (2) 아래 매크로 레짐 + (3) 공개 일반지식.
- "이전엔 X였으나" 식 비교 문장 금지 — 이전 모름. 현재 데이터로부터 독립 추론.
- WebSearch 미바인딩 슬롯 — 추가 웹수집 금지, data.json·일반지식만. 환각 금지, 불확실은 confidence 하향.

## 매크로 레짐 (2026-11-27 00:05 KST 실측, fred_snapshot·fear_greed)

- **CNN 공포탐욕 15 (극단적 공포)** — 1주 전 15.9, 1개월 전 29.8. 리스크오프 지속.
- 10Y 4.91% (1주 전 5.10%↓), 2Y 4.63% (1주 전 4.80%↓) — 금리 완화(불 스티프닝). 10Y-2Y +0.24.
- Fed Funds 3.88% 동결(매파적 동결 — 공포에도 인하 안 함). 12/9 FOMC 동결 우세.
- VIX 26.4 (1주 전 25.5↑), HY 스프레드 3.72% (1주 전 3.43%↑·신용 확대=경기둔화 신호).
- 10Y Breakeven 2.12%, 실업률 4.1%(4.2%→개선), USD지수(DTWEXBGS) 123.6.
- 서사: AI capex 디레버리징 → 성장주 이탈·방어/가치 회전. 추수감사절 단축주(11-26 목 휴장·11-27 금 조기폐장). 미 종가는 11-25(수) 기준.

## 산출물 (종목당 2파일, 폴더 안에)

1. `scorecard.md` — 본문(산문) + 10항목 가중표 + 아래 **필수 라인 포맷**:
   - `**종합 점수: {N} / 100**` (정수, 숫자 직후 ` / 100`)
   - `**투자등급: {강력매수|매수|중립|매도|강력매도}}**` (enum 밖 금지. 레버리지/비중축소류 → 최근접 tier)
   - `- **목표주가: {통화기호}{숫자}**`
   - `## § Confidence Interval` (Bear/Base/Bull 3시나리오 — 산문/표 자유)
   - `## § 약한 가정 3개 (Most Fragile Assumptions)` (각 가정 + 반증 시 영향 1줄)

2. `_report_data.json` — 렌더용. 아래 **정확 스키마**(값 타입 엄수):

```json
{
  "ticker": "TMO",
  "name": "써모피셔사이언티픽(TMO) — 재분석 v16 (이전 비교 미포함)",
  "date": "2026-11-27",
  "asset_type": "주식",            // ETF는 "ETF"
  "currency": "$",
  "score": 71,                      // 정수 0~100
  "grade": "매수",                   // enum
  "current_price": 685.52,          // 숫자 (data.json quote.current_price)
  "market_cap": "$254B",            // 문자열 가능(렌더가 파싱)
  "per": "trailing 36.2 / fwd 24.7",
  "low52": 435.27,                  // 숫자
  "high52": 727.56,                 // 숫자
  "atr": 19.80,                     // 숫자 (data.json quote.atr_14)
  "stop_loss": 645.91,              // 숫자 (data.json quote.stop_loss_2atr)
  "target_price": 740,              // 숫자
  "scorecard_items": [["경제적 해자",7],["성장성",7],["수익성",8],["재무 건전성",8],["밸류에이션",6],["모멘텀·기술",5],["리스크(하방)",6],["산업·경쟁 지위",8],["경영·자본배분",7],["매크로 적합성",7]],
  "extra_kpis": [["배당수익률","0.27%"],["베타","..."],["ROE","..."],["EV/EBITDA","..."],["PEG","..."],["잉여현금흐름(TTM)","..."]],
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
  "thesis": {"claim":"…","support":"…","falsifier":"…"},   // 반드시 dict (문자열 금지)
  "custom_sections": [
    {"title":"§ Confidence Interval","content":"Bear: … / Base: … / Bull: …"},   // 산문. 마크다운 표(파이프) 금지
    {"title":"§ 약한 가정 3개 (Most Fragile Assumptions)","content":"1. … / 2. … / 3. …"}
  ],
  "artifact_notes": []
}
```

### 타입 함정 (메모리 기반 — 위반 시 렌더 크래시)

- 가격 필드(current_price·low52·high52·atr·stop_loss·target_price)는 **숫자**(따옴표 금지).
- `scorecard_items` 점수는 **0~10** (0~100 아님). top-level `score`만 0~100.
- `thesis` 는 **dict** (claim/support/falsifier). 문자열로 쓰면 크래시.
- `custom_sections` CI 는 **산문** (마크다운 표 `| … |` 금지 — HTML 리터럴 파이프 노출).
- `extra_kpis` 는 `[label,value]` pair 리스트.
- ETF: scorecard 10항목은 ETF 적합 항목(보수율·추적오차·유동성·분산·배당·섹터배분 등)으로 유연 적용, moat_rating 은 "ETF(해자 N/A)" 식.

> 렌더 normalize 가드가 일부 드리프트를 교정하나(멱등), 위 스키마를 지키는 것이 1차 방어.
