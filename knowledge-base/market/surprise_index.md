---
updated: 2026-05-01
valid_until: 2026-05-31
file: surprise_index
category: market
confidence: medium
collection_status: PARTIAL
sources:
  - "knowledge-db/market/2026_daily_prices.md [2026-04-30 미국장 종가 기준]"
  - "knowledge-base/market/daily_snapshot.md [2026-05-01 모닝브리핑 기준]"
  - "임무 브리핑 04-30: AAPL Q2 FY26 AH +3% Beat / LLY Q1 Beat / CAT Q1 Beat / Core PCE 3월 0.0%(대폭 하회) / GDP Q1 ~2.3%(컨센 상회) / ECB 동결(25bp 컨센 Miss) / WTI $109.41 급등"
판정_공식: "누적 스코어 = (Beat × +1 + Miss × -1) / 총 건수. 스코어 > +0.3 = Beat 우세."
note: "2026-05-01 모닝 갱신. 04-30 AAPL AH Beat + LLY/CAT Beat + Core PCE 0.0% 골디락스 + ECB 동결 Miss 반영."
---

# 경제 서프라이즈 인덱스 (Economic Surprise Index)

> **쓰기 권한:** correlation-monitor
> **읽기 권한:** briefing-lead, global-macro-analyst, briefing-report-generator
> **갱신 빈도:** 매일 (B-4 — Beat/Miss 누적)

---

## CURRENT (2026-05-01 모닝 갱신 — AAPL AH +3% Beat + LLY/CAT Beat + Core PCE 0.0% 골디락스 + ECB 동결 Miss 반영)

### 최근 30일 서프라이즈 누적 (Beat/Miss) — 05-01 모닝 갱신

| 지역 | Beat | Miss | 중립 | 누적 스코어 | 방향성 |
|------|------|------|------|-----------|--------|
| **미국** | **28** | **5** | **9** | **+0.55** | Beat 강화 유지 — Core PCE 0.0%(대폭 Beat+1). GDP Q1 ~2.3%(Beat+1). AAPL AH Beat(+1). LLY Q1 Beat(+1). CAT Q1 Beat(+1). ECB 동결=미국 서프라이즈 외 처리. WTI $109 에너지 쇼크(Miss+1) |
| **유로존** | 2 | **3** | 3 | **-0.13** | 악화 확정 — ECB 동결(25bp 인하 컨센 Miss → Miss+1 추가). Brent $120+ 에너지 역풍. Lagarde "layer cake of shocks" |
| **중국** | 4 | 0 | 1 | **+0.80** | 강력 Beat 유지 — GDP +5.0% / PMI 51.2 / 수출 +12%. 신규 지표 미발표 |
| **한국** | 6 | **1** | 1 | **+0.63** | Beat 유지이나 소폭 약화 — Q1 GDP +1.7% 구조 유지. 단 4/30 KOSPI -1.38%(WTI $109 에너지 충격 Miss+1 처리) |

> 글로벌 가중 종합 스코어: **+0.51 (Beat 우세)** (미국 40%+유로존 20%+중국 20%+한국 20%). 전일 +0.55 대비 -0.04 (ECB Miss + WTI 에너지 충격 반영)

---

### 04-30 신규 확인 이벤트

| 날짜 | 지역 | 지표 | 실제 | 컨센서스 | 판정 | 시장 반응 | 출처 |
|------|------|------|------|---------|------|---------|------|
| 04-30 (08:30 ET) | 미국 | **GDP Q1 2026 Advance** | ~+2.3% | 컨센 ~2.1% (GDPNow 1.2%) | **Beat (+0.2%p 이상)** | S&P 선물 급등. 침체 내러티브 후퇴. WTI $109 병존으로 스태그플레이션 우려 해소 | [임무 브리핑 04-30] |
| 04-30 (08:30 ET) | 미국 | **Core PCE 3월 MoM** | **0.0%** | +0.3% | **대폭 Beat (-0.3%p 하회)** | S&P 급등 +1.02%. VIX -10.21%. 채권 10Y +1bp(WTI 에너지 역풍으로 하방 제한) | [임무 브리핑 04-30] |
| 04-30 (장후) | 미국 | **AAPL Q2 FY26** | 서비스 Revenue 서프라이즈 | 서비스 ~$26.7B | **Beat** | AH +3%. 관세 충격 제한적. 서비스 수익 구조 확인. 5/1 NASDAQ 추가 상승 가능 | [임무 브리핑 04-30] |
| 04-30 (장후) | 미국 | **LLY Q1 2026** | Beat | 컨센 | **Beat** | 비만치료제 Zepbound/Mounjaro 수요 확인. 헬스케어 섹터 모멘텀 지지 | [임무 브리핑 04-30] |
| 04-30 (장후) | 미국 | **CAT Q1 2026** | Beat | 컨센 | **Beat** | 인프라·건설 수요 유지. 산업재 섹터 지지. 에너지 설비 수요 반영 가능 | [임무 브리핑 04-30] |
| 04-30 (14:15 ET) | 유로존 | **ECB 통화정책** | **동결 (금리 동결)** | 25bp 인하 컨센 | **Miss (매파 서프라이즈)** | EUR 강세. Brent $120 에너지 역풍 대응. Lagarde "불확실성 layer cake" 발언 | [임무 브리핑 04-30] |
| 04-30 (지속) | 미국/글로벌 | **WTI 급등 지속** | $109.41 | — | **Miss (에너지 쇼크 지속)** | KOSPI -1.38%(에너지 수입국 충격). 5/12 CPI 헤드라인 상방 압력 지속 | [임무 브리핑 04-30] |

> **Core PCE 0.0% 판정 주의:** 디스인플레이션 확인 = 서프라이즈 인덱스 Beat 처리(컨센 +0.3% 대비 대폭 하회). 단 WTI $109 환경에서 헤드라인 인플레 압력은 별도. 서비스 인플레 골디락스 + 에너지 쇼크 이중 구조 지속.

---

### 전체 서프라이즈 이벤트 이력 (04-13~04-30 누적)

| 날짜 | 지역 | 지표 | 실제 | 컨센서스 | 판정 | 출처 |
|------|------|------|------|---------|------|------|
| 04-13 | 미국 | 3월 CPI YoY | 3.3% | ~3.0% | Beat (상방 — 에너지 주도) | [BLS] |
| 04-13 | 미국 | Core CPI YoY | 2.6% | ~2.7% | 중립 (소폭 하방) | [BLS] |
| 04-13 | 미국 | ISM 제조 가격 | 78.3 | ~62.0 | Beat — 강력 상방 | [ISM] |
| 04-14 | 한국 | 3월 수출 | $86.1B (+48.3% YoY) | ~$70B | 극Beat (역대 최대) | [산업부] |
| 04-15 | 중국 | 3월 수출 YoY | +12% | ~+8% | Beat (+4%p) | [Reuters] |
| 04-16 | 중국 | Q1 GDP | +5.0% | +4.8% | Beat (+0.2%p) | [Invezz / CNBC Asia] |
| 04-16 | 중국 | 3월 PMI | 51.2 | 50.3 | Beat (+0.9p) | [TradingEconomics] |
| 04-17 | 미국 | Morgan Stanley Q1 EPS | $3.43 | $3.02 | Beat +13.6% | [CNBC] |
| 04-17 | 미국 | Bank of America Q1 EPS | $1.11 | $1.01 | Beat +9.9% | [Bloomberg] |
| 04-21 | 미국 | 소매판매 3월 MoM | +0.7% | +0.4% | Beat (+0.3%p) | [Census Bureau] |
| 04-21 | 미국 | Netflix Q1 Revenue | $12.25B | $12.18B | Beat (Q2 가이던스 Miss 병존) | [Variety] |
| 04-22 | 유로존 | ASML Q1 Revenue | €8.8B | 컨센 하회 예상 | Beat (가이던스 상향) | [공개 보도] |
| 04-22 | 미국 | Boeing Q1 EPS | -$0.11 | -$0.29 | Beat | [GurFocus / Sherwood News] |
| 04-22 | 미국 | Boeing Q1 Revenue | $22.2B | $21.78B | Beat | [Sherwood News] |
| 04-22 (AH) | 미국 | TSLA Q1 EPS | $0.41 | $0.37 | Beat (+10.8%) | [Electrek / CNBC] |
| 04-22 (AH) | 미국 | Netflix Q1 EPS | $1.23 | ~$0.76 | Beat (+62%, 일회성 포함) | [공개 보도] |
| 04-24 (AH) | 미국 | Intel Q1 EPS | $0.29 | $0.01 | Beat (+2,800%) | [BusinessWire / Yahoo Finance] |
| 04-24 (AH) | 미국 | Intel Q1 Revenue | $13.58B | $12.42B | Beat (+$1.16B) | [BusinessWire] |
| 04-24 | 미국 | S&P Global PMI (Flash) | Composite 52.0 | 50.6 | Beat (+1.4p) | [S&P Global] |
| 04-24 | 미국 | 실업청구 (4/18주) | 214K | 212K | 중립 | [US DOL] |
| 04-24 | 한국 | Q1 GDP (속보) | +1.7% QoQ | +0.9% | 극Beat (+0.8%p) | [Korea Times / BOK] |
| 04-28 | 미국 | UPS Q1 실적 | Beat | 컨센 하회 예상 | Beat | [임무 브리핑 04-28] |
| 04-28 | 미국 | GM Q1 실적 | EPS 인라인 / EBIT 상향 | 인라인 | 중립 | [임무 브리핑 04-28] |
| 04-28 | 미국 | GE Aerospace Q1 EPS | +16.3% Beat | 컨센 | Beat (강력) | [임무 브리핑 04-28] |
| 04-28 | 미국 | Honeywell Q1 EPS | Beat | 컨센 | Beat | [임무 브리핑 04-28] |
| 04-28 | 미국 | Honeywell Q1 Revenue | Miss | 컨센 | Miss | [임무 브리핑 04-28] |
| 04-29 (AH) | 미국 | MSFT Q3 FY26 EPS | $4.27 (+5.2%) | $4.06 | Beat | [CNBC / Gurufocus] |
| 04-29 (AH) | 미국 | META Q1 EPS | $7.31 (+9.9%) | $6.65 | Beat | [StockTitan / CNBC] |
| 04-29 (AH) | 미국 | AMZN Q1 EPS | $2.78 (+69%) | $1.64 | Beat | [StockTitan / CNBC] |
| 04-29 (AH) | 미국 | GOOGL Q1 EPS | $5.11 (+95%) | $2.62 | Beat | [9to5Google / Yahoo Finance] |
| 04-29 | 미국 | FOMC 표결 구조 | 8-4 분열 | 만장일치 컨센 | Miss (매파 서프라이즈) | [CNBC / CNN / PBS] |
| 04-29 | 글로벌 | UAE OPEC+ 탈퇴 | WTI $107 | 예상 외 | Miss (공급 쇼크) | [Al Jazeera / CNBC] |
| **04-30 (08:30 ET)** | **미국** | **GDP Q1 2026 Advance** | **~+2.3%** | **~2.1%** | **Beat** | [임무 브리핑 04-30] |
| **04-30 (08:30 ET)** | **미국** | **Core PCE 3월 MoM** | **0.0%** | **+0.3%** | **대폭 Beat** | [임무 브리핑 04-30] |
| **04-30 (장후)** | **미국** | **AAPL Q2 FY26** | **서비스 Beat** | **~$26.7B** | **Beat** | [임무 브리핑 04-30] |
| **04-30 (장후)** | **미국** | **LLY Q1 2026** | **Beat** | **컨센** | **Beat** | [임무 브리핑 04-30] |
| **04-30 (장후)** | **미국** | **CAT Q1 2026** | **Beat** | **컨센** | **Beat** | [임무 브리핑 04-30] |
| **04-30 (14:15 ET)** | **유로존** | **ECB 통화정책** | **동결** | **25bp 인하** | **Miss** | [임무 브리핑 04-30] |
| **04-30** | **미국/글로벌** | **WTI $109.41 지속** | **$109.41** | **—** | **Miss (에너지 쇼크 지속)** | [임무 브리핑 04-30] |

---

### "골디락스 Beat vs 에너지 쇼크 Miss" 이중 구조 (05-01 모닝 갱신)

**확인된 골디락스 축 (거시·실적 동시 서프라이즈):**
- Core PCE 3월 0.0%(컨센 +0.3%, -0.3%p 대폭 하회) — 2024년 이후 최저
- GDP Q1 ~2.3%(GDPNow 1.2% 대폭 상회) — 침체 내러티브 해소
- AAPL Q2 FY26 AH +3% Beat — 관세 충격 제한. 서비스 수익 $26.7B+ 확인
- LLY Q1 Beat — 비만치료제 수요 구조적 지속
- CAT Q1 Beat — 인프라·건설 수요 유지
- AMZN/GOOGL 강력 Beat(+69%/+95%) — AI 클라우드 구조 확인

**지속되는 에너지 쇼크 Miss 축:**
- UAE OPEC+ 탈퇴 5/1 발효 현실화 — WTI $109.41 신규 고점. OPEC 점유율 30% 하회 확정
- ECB 동결(25bp 인하 컨센 Miss) — Brent $120 에너지 역풍 현실화
- WTI $90~109 4월 구간 = 5/12 CPI 헤드라인 에너지 항목 직접 상방 압력
- FOMC 8-4 분열(매파 서프라이즈) — 완화 경로 추가 지연. 파월 의장 5/15 임기 만료

**판정:** "Core PCE 0.0% 골디락스가 스태그플레이션 우려를 일시 해소했으나, WTI $109 에너지 쇼크가 5/12 CPI를 통해 헤드라인 인플레이션을 재자극할 구조적 리스크가 잔존. 단기(4~6주) 리스크온 환경 vs 중기(6~12주) 에너지 재인플레 시나리오 분기점."

---

### 종합 판정 (2026-05-01 모닝 기준)

**미국: Beat 강세 유지 (거시 + 실적 골디락스 — 에너지 역풍 이중 구조)** — 스코어 +0.55 (28 Beat / 5 Miss / 9 중립). Core PCE 0.0% + GDP +2.3% + AAPL/LLY/CAT Beat 5건 추가로 Beat 절대 수 대폭 증가. 단 WTI $109 에너지 쇼크 Miss 추가(5번째 Miss). 5/12 CPI + 5/8 NFP가 방향 최종 판별.

**유로존: Miss 전환** — -0.13. ECB 동결(25bp 인하 컨센 Miss) 반영으로 누적 스코어 마이너스 전환. Brent $120 에너지 역풍 구조 고착. Lagarde 불확실성 발언 = ECB 완화 경로 지연 확인.

**중국: 강력 Beat 유지** — +0.80. 신규 지표 미발표. GDP+PMI+수출 3중 구조 변화 없음. 5월 수출 지표(4월분) 발표 전 구조 유지.

**한국: Beat 소폭 약화** — +0.63. KOSPI -1.38%(WTI $109 에너지 수입국 충격 Miss 처리). Q1 GDP +1.7% 기저 구조 유지. 5/1 추가 조정(6,533.60 개장) 여부 모니터링.

**글로벌 종합: +0.51 (Beat 우세, 전일 대비 소폭 약화)** — Core PCE 0.0% 골디락스 Beat 강화이나 ECB 동결 Miss + WTI 에너지 쇼크 Miss 복합으로 글로벌 가중 스코어 소폭 하락. 단기 리스크온 환경은 유지되나 에너지 구조적 리스크 잔존.

---

### 이번 주 주요 서프라이즈 이벤트 달력 (05-01~05-12)

| 날짜 | 이벤트 | 컨센서스 (추정) | 서프라이즈 리스크 | 시장 영향 |
|------|------|--------------|----------------|---------|
| **5/1 (목) 정규장** | **AAPL 강세 반영** (AH +3%) | — | 극고 | NASDAQ 25,000+ 돌파 시나리오. BTC ETF 순유입 재전환 여부 연동 |
| **5/1 (목) 정규장** | **AMZN / GOOGL 강세 + META 약세 반영** | — | 극고 | 4/29 AH 실적 정규장 반영. AI 인프라 CapEx 역설 구조 소화 |
| **5/1 (목)** | UAE OPEC+ 탈퇴 발효 | — | 극고 | WTI $110+ 시나리오. BEI 반응 여부 실시간 모니터링 |
| 5/1 (목) | 한국 KOSPI 추가 조정 | 6,533.60 개장 | 고 | WTI $109 에너지 충격 지속 여부. 6,500 지지 확인 필요 |
| 5/5 (월) | 이란 핵협상 동향 | — | 극고 | 타결 시 WTI -15~20% 급락 = WTI↔BEI 이상 구조 반전 트리거 |
| **5/8 (목)** | **4월 NFP** | — | 극고 | 노동시장 에너지·관세 충격 반영 여부. 실업률 방향 |
| **5/12 (화)** | **4월 CPI** | — | **극고** | WTI $90~109 4월 구간 에너지 인플레 최종 판별. Core PCE 0.0% vs 헤드라인 괴리 확인 |
| 5/15 | 파월 Fed 의장 임기 만료 | — | 고 | 후임 의장 인선 + Fed 정책 연속성 불확실성 |

---

## 업데이트 로그

| 날짜 | 에이전트 | 변경 내용 |
|------|---------|----------|
| 2026-04-07 | market-data-collector | 수집 시도 — 전 항목 네트워크 차단. N/A 처리. |
| 2026-04-14~16 | briefing-lead (bypass) | 정성 이브닝 노트 3회 누적. |
| 2026-04-17 | correlation-monitor (이브닝, full) | 4지역 누적 정성 스코어. MS/BofA Beat 반영. |
| 2026-04-18 | market-data-collector | 주간 전면 갱신 — 중국 GDP +5.0% / 호르무즈 개방 / 다음 주 이벤트 달력 갱신. |
| 2026-04-19 (모닝) | correlation-monitor | 04-18 미국장 확정 기준 재검토. 수치 변동 없음 확인. |
| 2026-04-21 | market-data-collector | 소매판매 3월 +0.7% Beat + Netflix Beat 반영. 미국 +0.43→+0.47. 글로벌 +0.52→+0.54. |
| 2026-04-23 (이브닝) | correlation-monitor (full) | Boeing Q1 EPS Beat 추가. 미국 +0.47→+0.50. 한국 +0.80→+0.83. 글로벌 +0.54→+0.56. |
| 2026-04-23 (모닝) | correlation-monitor (quick) | TSLA EPS $0.41 Beat + Netflix EPS $1.23 Beat + ASML Beat 3건 추가. 미국 +0.50→+0.58. 유로존 0.00→+0.17. 글로벌 +0.56→+0.60. |
| 2026-04-24 | correlation-monitor (full) | 04-24 정기 갱신. 신규 확정 데이터 없음. 달력 04-24 기준 갱신. |
| 2026-04-26 | correlation-monitor (quick) | PMI Beat + Intel Beat + 한국 Q1 GDP Beat 3건 추가. 미국 13→15 Beat, 스코어 +0.58→+0.59. |
| 2026-04-27 | correlation-monitor (이브닝, full) | 이란 특사 취소 + KOSPI 6,615 신고가 이벤트 기록. |
| 2026-04-28 | correlation-monitor (이브닝, full) | UPS Beat + GM 중립 + GE Aerospace Beat + Honeywell EPS Beat / Rev Miss 반영. 미국 Beat 15→18. 스코어 +0.59→+0.56. |
| 2026-04-30 | correlation-monitor (모닝, full) | 04-29 빅테크 AH 4종 + FOMC + UAE 충격 반영. 미국 Beat 18→23(+5). 글로벌 +0.59→+0.60. |
| 2026-04-30 | correlation-monitor (이브닝, full) | GDP/PCE Beat + ECB 동결 Miss + LLY/CAT Beat 반영. 미국 Beat 23→24, 스코어 +0.56. 유로존 +0.17→0.00. |
| 2026-05-01 | correlation-monitor (모닝, full) | 04-30 확정: Core PCE 0.0%(대폭 Beat+1), GDP +2.3%(Beat+1), AAPL AH Beat(+1), LLY Beat(+1), CAT Beat(+1), WTI $109 지속(Miss+1), ECB 동결(Miss+1 — 유로존). 미국 Beat 24→28(+4), Miss 4→5(+1), 중립 8→9(+1). 스코어 +0.56→+0.55. 유로존 0.00→-0.13(Miss 전환). 한국 스코어 +0.86→+0.63(KOSPI -1.38% 에너지 충격 Miss 처리). 글로벌 +0.55→+0.51. "골디락스 Beat vs 에너지 쇼크 Miss" 이중 구조 명시화. |
