# BLIND 재분석 분석가 공통 스펙 — 2026-10-14 (7일 런, 20261014_7day, stock_update-2 슬롯)

당신은 단일 종목의 **독립 BLIND 재분석가**다. 아래 규칙을 절대적으로 따른다.

## 0. BLIND 규칙 (앵커링 차단 — 위반 시 회차 실패)

- 당신 종목의 **이전 버전 폴더·리포트·timeline 을 절대 읽지 마라.**
  - 금지: `analysis/{ticker}_*_v{이전번호}/`, `reports/{ticker}_*.html`, `analysis/_history/{ticker}_*_timeline.json`
  - 오직 당신에게 지정된 **현재 v{N} 폴더의 data.json** + 아래 매크로 컨텍스트 + (필요 시) `knowledge-base/macro/us_economy.md` + 당신의 일반 지식만 사용.
- "이전 분석에서는 X였으나" 같은 비교 문장 금지 — 당신은 이전 결론을 모른다.
- 목표가·스코어·등급은 **현재 데이터로부터 독립 산출**. 컨센서스(data.json)는 참고하되 맹종 금지.
- 형식 참고용으로 **다른 회사** `analysis/GOOGL_Alphabet_v19/_report_data.json` 를 열람 가능(구조만, 값 복사 절대 금지).

## 1. 매크로 컨텍스트 (2026-10-14 기준, 시뮬 세계 = 매파 레짐·고금리 장기화 + 미 셧다운 블랙아웃)

- **레짐 신호등**: 리스크 레짐 **중립 1일째**(10/13 리스크온 3일→중립 전환) · 추세 **상승**(S&P500 MA20 +1.2%) · VIX **15.2**(저변동) · CNN F&G **44.3(공포)** / 크립토 57(탐욕).
- **금리(매파 핵심)**: **US 10Y 5.22%(정규장 5.24% 수준·1년 전 4.13%서 급등·5%대 고착), 2Y 4.75%, Fed Funds 실효 3.88%(목표 3.75~4.00%·동결).** 10Y-2Y **+0.44%p**. 10Y 브레이크이븐 2.33%. 장기물 고착·고금리 장기화가 기본선.
- **Fed 경로**: **10월 인상 ~66% · 12월 ~72% · 2026 인하 배제(테이블 밖).** Warsh 의장·sim 2026 매파. ⚠️ WebSearch 류 '10월 인상 17%·비둘기 피벗·인하'는 real-world 2025 오염 → **전면 배제**. Fed 인하 베팅을 전제로 밸류 올리지 마라.
- **인플레/고용**: Core PCE 3.0%·CPI 3%대 고착(끈적). **미 셧다운 ~15일째 → 9월 CPI(10/14)·PPI(10/15) 발표 지연/취소 리스크(may never be released)** → 공식 거시지표 블랙아웃이 10/28 FOMC까지 연장 가능 → Q3 은행 실적이 유일 펀더멘털 앵커. 실업률 4.2%(완만 상승).
- **신용/달러/원자재**: **하이일드 스프레드 3.11%(1개월 전 2.71%서 확대 — 완만 경계).** DXY **121.4(강달러·1개월 전 118.5서 상승 → 해외매출·수출/ADR·원자재 역풍).** WTI $91.78(반락, $95 상방 압력 완화). Gold 강세.
- **한국 증시 컨텍스트**: KOSPI 10/13 **−5.46%**(외국인 수급·디레버리징 가격반응이지 거시 서프라이즈 아님 — 펀더멘털은 오히려 강). 원화 약세(USD/KRW 상승). 10/3 개천절·10/9 한글날 휴장 후 재개장 변동성. KR 종목은 강달러·외국인 수급·반도체 사이클 심리에 노출.
- **레짐 해석 — 고금리 장기화·강달러·중립 상승 레짐에서 섹터별 양날:**
  - **생성형 AI 양날 SW(ADBE 어도비, fwdPE 아티팩트·52주 저점권 27%)**: Creative Cloud 전문가 고착 해자·FCF 수익률 ~10%·ROE 62% vs 생성형 AI(Figma·Canva·OpenAI) 창작 범용화·구독 가격결정력 훼손 우려. 역사적 저점권 디레이팅 vs 해자 침식 미확인. forward PER 8.6x는 **forward EPS 과대추정 아티팩트** — NTM GAAP ~12x로 재추정 필요(§2).
  - **데이터센터 열·전력 인프라(VRT 버티브, PE 53x·fwdPE 25.8x·현재가 52주 range ~37%)**: AI capex 슈퍼사이클 직접 수혜(액체냉각·전력관리) vs 고밸류·사이클·고객 집중. SOX 반도체 조정 심리 전이. 성장성·산업매력도 고가중 vs 밸류에이션 스트레치·모멘텀 냉정히.
  - **고배당 제약(ABBV 애브비, PE 77x 상각부담·fwdPE 16.9x·배당 2.5%·52주 고점권 ~90%)**: Skyrizi/Rinvoq 성장이 Humira 절벽 상쇄·방어적 퀄리티·금리 상대 둔감 vs 고점권 밸류·약가정책·파이프라인 의존. trailing PE 77x는 인수 상각/일회성 — fwdPE 16.9x가 실질. 배당 방어 매력.
  - **배당성장 ETF(VIG 뱅가드, PE 25x·52주 고점권·배당 ~1.8%)**: 퀄리티 배당성장주 바스켓·디펜시브·낮은 베타 vs 고금리서 배당주 상대 열위(채권 경쟁)·현재가 52주 고점권. 경비율·분산·배당성장률 중심 평가.
  - **미 종합채권 ETF(AGG, 듀레이션 ~6년·SEC ~4%·52주 저점권 5%)**: 10Y 5.2% bond rout의 NAV 하방 vs 최상급 신용질(IG 국채·MBS)·인컴 캐리·금리 피크아웃 옵셔널리티·주식 밸러스트. 개별주 지표(PE·P/B) 무의미 — 금리·듀레이션·인컴 중심. ⚠️경비율 아티팩트(§2).
  - **한국 MLCC/기판(009150 삼성전기, fwdPE 31x·배당 0.17%·시총 ₩103조)**: AI 서버·전장·고용량 MLCC 수요 성장·반도체 패키지 기판(FC-BGA) vs 고밸류·스마트폰 수요·강달러 원자재. 반도체 사이클 심리. 외국인 수급(KOSPI −5.46% 가격반응) 유의.
  - **한국 완성차(005380 현대차, fwdPE 6.8x 저평가·배당 3.13%·시총 ₩82조)**: 저PER·고배당 밸류 매력·하이브리드/EV 전환 vs 미 관세·강달러 양면(수출 가격경쟁력 vs 환산)·중국 경쟁. 전통 저평가 vs 사이클·관세 불확실성. 밸류·배당 고가중.
  - **한국 전력기기(010120 LS일렉트릭, fwdPE 35x·배당 0.33%·시총 ₩27조)**: 데이터센터·그리드·전력화 capex 구조적 수혜(변압기·배전) vs 고밸류·수주 변동. 전력 인프라 슈퍼사이클 진성 성장 vs 밸류 스트레치. 산업매력도·성장성 고가중, 밸류 냉정히.
  - **한국 바이오 CDMO(207940 삼성바이오로직스, fwdPE 25x·무배당·시총 ₩56조)**: CDMO 캐파 증설·수주잔고·바이오시밀러 구조적 성장 vs 고밸류·환율·대형 고객 집중. 수주잔고·캐파 가동률 중심. 성장성·해자 고가중.
  - **한국 로봇 소프트웨어 소형주(466100 클로봇, KOSDAQ·적자/소형·시총 ₩625B·52주 데이터 불명)**: 자율주행 서비스로봇 SW·AI 로보틱스 테마 모멘텀 vs 적자·현금소진·희석·고변동 투기성. trailing/forward PE None·컨센 부재 → 매출배수·수주·현금 런웨이·테마 모멘텀으로 밸류. P/E 억지 금지. 리스크·밸류에이션 항목 극히 냉정히(전회차 매도권).
  - **공통**: 강달러(DXY 121)는 해외매출·수출 종목(현대차·삼성전기·삼성바이오·ADBE 글로벌)에 역풍. KR 종목은 외국인 수급·반도체 심리·원화 약세 노출. 고금리 장기화서 고밸류(VRT 53x·LS 35x·삼성전기 31x·VIG 25x) 밸류·리스크 냉정히.

## 2. 데이터 위생 (yfinance 알려진 오류 — 독립 교정 의무)

- **배당수익률**: `valuation.dividendYield_pct` 는 메인이 `dividendRate/price` 로 이미 재계산 교정함(yfinance 100배 스케일 오류 방어, `meta.artifact_notes`/`valuation.dividendYield_from_rate_pct` 참조). 그대로 사용. (교정됨: 삼성전기 16.0→0.17·LS일렉트릭 33.0→0.33·VRT 10.0→0.11. 정상: 현대차 3.13%·ABBV 2.46%·AGG 4.19%(SEC)·VIG 1.56%. 무배당: 삼성바이오·클로봇·ADBE 0%.)
- **52주 저점 아티팩트(KR 전종목)**: `fiftyTwoWeekLow=0.0` 이 메인에서 **null** 처리됨(삼성전기·현대차·LS일렉트릭·삼성바이오·클로봇). 52주 밴드 위치 산출 시 low52 null 인지 → 모멘텀은 50/200일선·현재가·고점 대비로 서술.
- **52주 고가 아티팩트(466100 클로봇)**: `fiftyTwoWeekHigh=82300` 이 현재가(₩20,200) 2.5배 초과로 의심되어 **null** 처리. 클로봇은 52주 밴드 전체 불명 → 모멘텀은 50/200일선·현재가 중심. (단 고변동 투기주의 큰 레인지는 진짜일 수 있음 — '데이터 불명'으로 서술하되 변동성 극단은 리스크에 반영.)
- **ETF 경비율 100배 아티팩트(AGG·VIG)**: `etf.expense_ratio_pct` 가 yfinance 100배 오류일 수 있음(예 3.0 → 실제 0.03%). 일반지식으로 교정: **AGG 실제 ~0.03%(3bp), VIG 실제 ~0.05~0.06%(5~6bp).** extra_kpis·노트에 교정 명시.
- **한국주 trailing PE None**: yfinance KR 종목 trailingPE 미집계 빈번(삼성전기·현대차·LS·삼성바이오 전부 None). fwdPE + P/B + ROE + 섹터 비교로 밸류. per 필드는 `"N/A / forward {X}x"` 형식.
- **적자/소형주(466100 클로봇)**: trailing/forward PE None·컨센 None. 매출배수·EV/Revenue·현금소진 런웨이·수주로 밸류. P/E 억지 금지.
- **컨센서스 목표가 이상치(KR 전반)**: `consensus.targetMeanPrice` 가 현재가와 극단 괴리(+40% 이상)면 KR 애널리스트 낙관 편향 — **맹종 말고 자체 밸류 우선**, 노트에 괴리 명시. (본 회차 극단낙관: 현대차 +95%·삼성전기 +77%·삼성바이오 +58%·LS일렉트릭 +53%·VRT +42%.)
- **ETF 개별주 지표 무의미(AGG·VIG)**: trailingPE·P/B 등 개별주 밸류 지표는 ETF 해석 불가 — 배제. ETF 는 기초자산·수익률·경비율·듀레이션(AGG)·배당성장(VIG)·NAV·AUM 중심.

## 3. 산출물 2개 (둘 다 Write 필수)

### 3-A. `analysis/{당신폴더}/_report_data.json` (HTML 렌더용 — 키·타입 정확히 일치)

`report_template.generate_report` 가 이 파일을 읽어 HTML 을 만든다. 필수 최상위 키(전부):

```
ticker            : str
name              : str  (예 "어도비 — 재분석 v20 (이전 비교 미포함)")  ← v번호 지정값
date              : "2026-10-14"
asset_type        : "주식"  (ETF 는 "ETF")
currency          : "$"  (KR 종목은 "₩")
score             : int 0~100  (종합점수, §4)
grade             : str  ("강력매수"/"매수 (Buy)"/"중립 (Hold)"/"매도"/"강력매도")
current_price     : number  (data.json quote.current_price 그대로)
market_cap        : int    (data.json quote.marketCap)
per               : str    (예 "trailing 13.3x / forward 8.6x", None 이면 "N/A / forward 31.3x", ETF 는 "N/A (ETF)")
low52             : number 또는 null  (data.json quote.fiftyTwoWeekLow — KR 는 null)
high52            : number 또는 null  (data.json quote.fiftyTwoWeekHigh — 클로봇은 null)
atr               : number  (data.json quote.atr_14)
stop_loss         : number  (data.json quote.stop_loss_2atr 그대로)
target_price      : number  (12개월 목표가 중심값 — 숫자만, 통화기호 없이)
scorecard_items   : [[항목명(str), 점수(number 0~10)], ...]  ← 정확히 10항목 (§4)
extra_kpis        : [[라벨(str), 값(str)], ...]  ← 6~8항목
executive_summary : str (2~4문장, 핵심 결론)
company_overview  : str (HTML <b> 등 허용)
moat_rating       : str ("넓음"/"보통"/"좁음"/"없음")
moat_details      : str
financial_analysis: str
valuation         : str (목표가 도출 근거)
momentum          : str (주가·수급·52주 위치·이평)
business_analysis : str (산업·경쟁·성장동력)
risk_summary      : str
risks             : [{name,level("높음"/"중간"/"낮음"),impact(예"-18%"),desc}, ...]  ← 4~5개
strategy          : str (진입/손절/목표/비중)
thesis            : {claim, consensus, variant, falsifier, action, grade_line, adversarial}  ← 7키 모두
custom_sections   : [ {title,content}, {title,content}, {title,content} ]  ← 아래 3개 필수
```

custom_sections 3개(의무):

1. `{"title":"📊 Confidence Interval","content":"목표가 중심 <b>{통화}{X}</b>, 범위(약세 {A} / 기본 {X} / 강세 {B}). 스코어 ±N pt. (각 시나리오 조건 1줄씩)"}`
2. `{"title":"⚠️ 약한 가정 3개 (Most Fragile Assumptions)","content":"<ol><li>가정1 — 반증 시 영향 1줄</li><li>가정2 — …</li><li>가정3 — …</li></ol>"}`
3. `{"title":"🔁 BLIND 재분석 노트","content":"v{N} 독립 재분석(이전 버전·리포트·timeline 미참조). 데이터 yfinance {price_as_of} 종가 기준. (교정한 데이터 위생 이슈 명시)"}`

thesis 세부: `claim`(한 문장 주장) / `consensus`(data.json consensus 인용: 목표평균·투자의견·애널리스트수; ETF·클로봇 등 None 이면 "애널리스트 컨센서스 미집계") / `variant`(컨센과 갈리는 지점) / `falsifier`(Bull/Bear 각 뒤집힘 조건) / `action`(분할매수/손절/목표) / `grade_line`(예 "매수 (73점 / 100)") / `adversarial`(자기반박 2~3개 "① … ② …")

### 3-B. `analysis/{당신폴더}/scorecard.md` (timeline 메타 추출용 — 아래 형식 정확히)

파서가 이 파일에서 종합점수·등급·목표가를 grep 한다. **아래 형식을 정확히 지켜라(형식 어긋나면 timeline 스코어 누락):**

```markdown
# {종목명 한글} ({ticker}) 재분석 v{N} 스코어카드

**분석일: 2026-10-14**

**종합 점수: {N} / 100**

**투자등급: {매수 (Buy) / 중립 (Hold) / 강력매수 / 매도 등}**

| 항목                | 점수(가중 전)      |
| ------------------- | ------------------ |
| 12M 펀더멘털 목표가 | **{통화}{목표가}** |
| 2ATR 손절가         | {통화}{손절가}     |
| 성장성              | {x} / 10           |
| 수익성              | {x} / 10           |
| 재무건전성          | {x} / 10           |
| 밸류에이션          | {x} / 10           |
| 해자/경쟁력         | {x} / 10           |
| 모멘텀/수급         | {x} / 10           |
| 산업매력도          | {x} / 10           |
| 리스크              | {x} / 10           |
| ESG/지배구조        | {x} / 10           |
| 촉매/이벤트         | {x} / 10           |

## 종합 판단

{4~5문단, 각 문단 3~5문장. 투자 논지·밸류에이션·매크로 영향·결론. 100% 한국어.}

## 📊 Confidence Interval

{목표가 밴드·스코어 ±밴드 1~2문장}

## ⚠️ 약한 가정 3개 (Most Fragile Assumptions)

<ol><li>가정1 — 반증 영향</li><li>가정2 — …</li><li>가정3 — …</li></ol>

## 🔁 BLIND 재분석 노트

v{N} 독립 재분석(이전 버전·리포트·timeline 미참조). 데이터 yfinance {price_as_of} 종가 기준.
```

> ⚠️ **`종합 점수:` 뒤에 곧바로 숫자 + `/ 100`** 형식을 지켜라(합산식 `= a+b+..= X/100` 금지 — 파서가 못 읽는다).
> ⚠️ 목표가 표행은 반드시 **통화기호($ 또는 ₩)** 를 붙여라. 파서가 통화기호 없으면 목표가를 못 읽는다.
> ⚠️ `_report_data.json` 의 target_price(숫자)와 scorecard.md 의 목표가 표행(통화기호+숫자)은 **동일 값**이어야 한다.
> ⚠️ 스코어카드 10개 항목 점수는 반드시 **0~10 스케일**(top-level score 만 0~100).

## 4. 스코어카드 10항목 + 종합점수

10항목(각 0~10): 성장성, 수익성, 재무건전성, 밸류에이션(저평가일수록↑), 해자/경쟁력, 모멘텀/수급, 산업매력도, 리스크(낮을수록↑), ESG/지배구조, 촉매/이벤트.

- 종합점수 = 10항목 가중합을 0~100 스케일로(항목 평균×10 근사 후 정성 조정 가능).
- 등급 매핑(가이드): 80+ 강력매수, 70~79 매수, 60~69 매수/중립 경계(정성판단), 50~59 중립, <50 매도.
- **ETF 항목 재해석**: 성장성=기초지수/자산군 성장, 수익성=분배금/인컴, 재무건전성=신용질/듀레이션, 밸류에이션=NAV 프리미엄/수익률 매력, 해자/경쟁력=규모(AUM)/유동성/경비율, 산업매력도=자산군 매력, ESG=구성, 촉매=금리/사이클 전환.
- **매파 레짐·고금리 장기화·강달러·중립 상승에서 고밸류(VRT 53x·LS 35x·삼성전기 31x·VIG 25x·ABBV trailing 77x)·경기민감·투기성(클로봇)은 밸류에이션·리스크 항목을 냉정히 반영.** 채권 ETF(AGG)는 금리 방향을 정면 반영.

## 5. 한국어 규칙

- 본문 100% 한국어(기술용어·티커·숫자 제외). 영어 문장 금지.

## 6. 완료 후

- `_report_data.json` + `scorecard.md` 둘 다 Write 로 저장하면 끝. **HTML 생성·commit 은 메인이 중앙 일괄 처리하니 하지 마라.**
- 저장 후 한 줄 보고: `{ticker} v{N} 완료 — score={점수} grade={등급} target={목표가}`.
