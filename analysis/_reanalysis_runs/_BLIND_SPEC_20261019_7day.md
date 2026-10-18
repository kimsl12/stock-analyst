# BLIND 재분석 공통 스펙 — 2026-10-19 (7일 임계 / stock_update-2 슬롯 / cap 10)

> 이 파일은 /재분석실행 7 20 의 BLIND 분석가 10명이 공통으로 읽는 지침이다.
> 당신은 **독립 재분석가**다. CURRENT 데이터만으로 독립 결론을 낸다.

## 절대 규칙 (BLIND — 앵커링 구조적 차단)

1. **READ 허용**: (a) 당신에게 지정된 `analysis/{DIR}/data.json` (yfinance 실측) (b) `knowledge-base/` 중 필요한 파일(macro/, market/, 관련 industry/).
2. **READ 금지**: 이전 버전 폴더(`analysis/{TICKER}_*_v{<N}/`), 기존 `reports/{TICKER}_*.html`, 이전 스코어/등급/목표가. **당신은 이전 결론을 모른다.** "이전엔 X였으나" 같은 비교 문장 금지.
3. **WebSearch 금지**. data.json + KB 만. data.json 에 없는 수치는 유도하거나 N/A 표기 — **지어내지 말 것**.
4. 출력은 **2개 파일만 Write**: `scorecard.md` + `_report_data.json` (지정 폴더). 다른 파일/HTML/커밋 금지.

## 데이터 무결성

- data.json 수치 그대로 인용(current_price, atr_14, stop_loss_2atr, 52주, valuation, consensus, dividend).
- data.json 의 `artifact_notes` 존중(이미 교정된 배당 스케일·52주). 이번 회차 전 종목 **미국 상장($)** — 통화 **$**.
- `price_as_of` = 기준일 **2026-10-16** (금요일 종가·주말·yfinance 개별주 지연·정상). 본문에 명시.
- 52주 고점이 현재가 대비 크게 높아도(예: COIN $173→52H $373·-54%, LVMUY $88→52H $153·-42%, BWXT $137→52H $242·-43%) 이는 **실제 조정·크래시**이지 아티팩트 아님 — 그대로 사용. LUNR 는 52H 아티팩트($46.75)가 이미 null 교정됨 → 52L $7.78 와 tgtMean $29 로 모멘텀 판단.

## 현재 레짐 (2026-10-19, 반드시 반영)

- **레짐: 🔴 조심(방어 우위) — 리스크오프 2일째.** 진앙은 반도체. 금요일(10/16) 미 세션: S&P −1.09% · 나스닥 −2.15% · **SOX −3.83%(진앙)** · 다우 −0.34%(가치 상대 방어) · 러셀2000 −1.66%. VIX **19.99(+21%·패닉 초입)**.
- CNN 공포탐욕 **17.9 (extreme fear)**, 1주 전 46.5. 주말 크립토는 $82K 회복(위험선호 선행 관찰·탈동조 HV6).
- 금리: **10Y 5.10%(고착·채권 랠리 부재)** · 2Y 4.77% · Fed Funds 3.88% · 10Y-2Y **+0.35%p(정상화 스티프닝)** · 10Y BEI 2.35%. Core PCE ~3.0%대.
- **Fed 매파 레짐**: 10월 FOMC(10/27~28) **인상 ~66%** · 12월 >72% · **2026 인하 배제**(Warsh 매파 의장·Williams 12월 인상 재확인). ★**비둘기 반사 오독 절대 금지** — WebSearch real-world 2025 비둘기(인하) 데이터 전면 배제.
- 셧다운 ~17일째 **데이터 블랙아웃**("깜깜이") — 9월 CPI/PPI/고용 공식 미발표. BOK 금통위 10/22(수).
- **USD DXY 121.6 강세** · **Gold $4,181(신고가권)** · **WTI $99(고착·$95+ HV4 트리거)** · 구리 강세. = **반도체發 섹터 집중 조정 → 가치·실물·에너지·방산으로 로테이션** 국면.

### 이번 코호트 섹터 함의 (10종 전부 미국 상장)

- **CVX(에너지)·FCX(구리/소재)**: WTI $99·구리 강세·실물 로테이션의 **수혜 축**. 강달러는 원자재엔 완만한 역풍.
- **GE(항공엔진)·BWXT(원자력/방산)**: 방산·실물 순풍. BWXT 는 SMR·해군 추진 테마이나 현재가 52주 저점권(-43%).
- **LLY(비만/당뇨 제약)·COST(소비 스테이플)**: 방어적 성장. 고금리下 고멀티플 부담 공존.
- **MA(결제/금융)**: 소비 사이클·강달러 국경간 거래 양면. 52주 고점권.
- **LVMUY(명품 소비재 ADR)**: 중국 소비 둔화·명품 사이클 저점 논쟁 — 52주 저점권·저PE·배당 3.4%.
- **COIN(크립토 거래소)**: 크립토 베타·규제. 주말 BTC $82K 회복이 단기 변수. -54% off 52H.
- **LUNR(우주·스펙)**: 적자·고변동 스펙주. tgtMean $29 애널 낙관 vs 현금소진 리스크 균형. 포지션 사이즈 경고 필수.

## OUTPUT 1 — `scorecard.md` (한글 비중 80%+)

```
# {TICKER} — {풀네임} · BLIND 재분석 v{N}

분석일: 2026-10-19 (기준가 price_as_of: 2026-10-16 — 금요일 종가·주말·yfinance 지연·정상)

- 기준가: 2026-10-16 · ${현재가}
- 자산유형 / 섹터 / 핵심 KPI 2~3줄

## 종합 판정

**종합 점수: {N} / 100**       ← 이 형식 정확히(숫자 직후 " / 100"). parseScore 의무.

**투자등급: {강력매수|매수|중립|매도|강력매도} ({영문})**

(판정 근거 3~5문장 — 레짐 연결)

## 10항목 스코어카드 (0~10)

| 항목 | 점수 | 근거 |
(성장성·수익성·재무건전성·밸류에이션·해자/경쟁력·모멘텀/수급·산업매력도·리스크·ESG/지배구조·촉매/이벤트)

## ATR 손절 · 12M 목표가
- 현재가 / ATR(14) / 2-ATR 손절가 / 12M 목표가 (전부 data.json 실측 기반)

## § Confidence Interval
- 기본(점추정) / 상단(Bull) / 하단(Bear) 목표가 + 구간 + 분산 동인

## § 약한 가정 3개
1~3. 결론을 뒤집을 수 있는 가정 + 각 "반증 시 영향" 1줄

_BLIND v{N} — 이전 버전/스코어/목표가 미참조. 독립 추론._
```

## OUTPUT 2 — `_report_data.json` (렌더 입력 · 아래 키 정확히)

```json
{
  "ticker": "{TICKER}",
  "name": "{풀네임} — 재분석 v{N} (이전 비교 미포함)",
  "date": "2026-10-16",
  "asset_type": "주식",
  "currency": "$",
  "score": {0~100 정수},
  "grade": "{강력매수|매수|중립|매도|강력매도} ({영문})",
  "current_price": {data.json current_price 숫자},
  "market_cap": {data.json marketCap 원값 숫자},
  "per": "trailing {x}x / forward {x}x",
  "low52": {숫자}, "high52": {숫자 또는 null},
  "atr": {data.json atr_14 숫자},
  "stop_loss": {data.json stop_loss_2atr 숫자},
  "target_price": {12M 목표가 숫자},
  "scorecard_items": [["성장성",7],["수익성",6],["재무건전성",6],["밸류에이션",5],["해자/경쟁력",7],["모멘텀/수급",4],["산업매력도",6],["리스크",5],["ESG/지배구조",6],["촉매/이벤트",6]],
  "extra_kpis": [["시가총액","..."],["배당수익률","..."],["Forward P/E","..."],["PEG","..."],["ROE","..."],["매출성장 YoY","..."],["52주 위치","..."]],
  "executive_summary": "6~10문장 — 레짐·논점·결론",
  "company_overview": "기업/사업 개요",
  "moat_rating": "넓음|중간|좁음|없음",
  "moat_details": "해자 근거",
  "financial_analysis": "재무 분석(data.json 실측 인용)",
  "valuation": "밸류에이션 분석 + 레짐 적합성",
  "momentum": "모멘텀/수급(50·200일선·52주 위치·베타)",
  "business_analysis": "핵심 논점(debate) — 컨센서스 vs 변이",
  "risk_summary": "최대 리스크 요약",
  "risks": [{"name":"...","level":"높음|중간|낮음","impact":"...","desc":"..."}, ...4~5개],
  "strategy": "진입/손절/목표 전략",
  "thesis": {"claim":"...","consensus":"...","variant":"...","falsifier":"수치+기한","action":"...","grade_line":"{등급} ({점수}점 / 100)","adversarial":"① ... ② ... ③ ..."},
  "custom_sections": [
    {"title":"📊 Confidence Interval","content":"기본/상단/하단 목표가 + 구간 + 분산 동인"},
    {"title":"⚠️ 약한 가정 3개 (Most Fragile Assumptions)","content":"<ol><li>... 반증 시 -N%.</li><li>...</li><li>...</li></ol>"},
    {"title":"🔁 BLIND 재분석 노트","content":"v{N} 독립 재분석. data.json yfinance 2026-10-16 종가 기준 정합 확인 + artifact_notes 반영."}
  ]
}
```

### 주의 (schema drift 방어)

- `custom_sections` 는 반드시 키 **`content`** 사용(`body` 아님 — 템플릿이 content 만 렌더).
- `scorecard_items` 는 **0~10** 정수(0~100 아님 — 레이더 차트 mx=10).
- `score` 는 0~100 정수. `grade` 는 5단계 중 하나.
- 숫자 필드(current_price·market_cap·low52·high52·atr·stop_loss·target_price)는 **문자열 아닌 숫자**. high52 가 data.json 에서 null 이면 null.
- 점수·등급·목표가는 CURRENT 데이터 + 레짐으로 **독립 산출**. 같은 회사라도 이전과 달라질 수 있음(정상).
- scorecard.md 의 **종합 점수**와 _report_data.json 의 **score**, 등급, 목표가는 **반드시 동일**해야 한다.
