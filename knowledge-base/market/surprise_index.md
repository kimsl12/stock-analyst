---
updated: 2026-04-30
valid_until: 2026-05-30
file: surprise_index
category: market
confidence: medium
collection_status: PARTIAL
sources:
  - "knowledge-db/market/2026_daily_prices.md [2026-04-29 미국장 종가 기준]"
  - "knowledge-base/market/daily_snapshot.md [2026-04-30 모닝브리핑 기준]"
  - "임무 브리핑 04-29: MSFT EPS $4.27 Beat / META CapEx 상향·EPS Beat / AMZN EPS $2.78 대폭 Beat / GOOGL EPS $5.11 대폭 Beat / UAE OPEC 탈퇴 쇼크 / FOMC 동결 8-4 분열"
  - "Al Jazeera / CNBC / Fortune [UAE OPEC 탈퇴 2026-04-28~29]"
  - "StockTitan / CNBC / Gurufocus [빅테크 AH 실적 2026-04-29]"
판정_공식: "누적 스코어 = (Beat × +1 + Miss × -1) / 총 건수. 스코어 > +0.3 = Beat 우세."
note: "2026-04-30 모닝 full 갱신. 04-29 빅테크 4종 AH 실적(MSFT/META/AMZN/GOOGL) + FOMC 동결(8-4 분열) + UAE OPEC 탈퇴 충격 반영. GDP Q1 Advance + Core PCE 3월 4/30 08:30 ET 발표 예정."
---

# 경제 서프라이즈 인덱스 (Economic Surprise Index)

> **쓰기 권한:** correlation-monitor
> **읽기 권한:** briefing-lead, global-macro-analyst, briefing-report-generator
> **갱신 빈도:** 매일 (B-4 — Beat/Miss 누적)

---

## CURRENT (2026-04-30 이브닝 갱신 — GDP/PCE Beat + ECB 동결 Miss + LLY/CAT Beat 반영)

### 최근 30일 서프라이즈 누적 (Beat/Miss) — 04-30 이브닝 갱신

| 지역 | Beat | Miss | 중립 | 누적 스코어 | 방향성 |
|------|------|------|------|-----------|--------|
| **미국** | **24** | **4** | **8** | **+0.56** | Beat 유지 — GDP ~2.3% Beat(+1). LLY/CAT Beat(+2, 기업 실적). Core PCE 0.0% 둔화(중립 판정 — 방향 유리하나 인플레 서프라이즈 기준상 중립). AAPL 4/30 장후 미발표 |
| **유로존** | 2 | **2** | 3 | **0.00** | 악화 — ECB 동결(25bp 인하 컨센 Miss → Miss +1). Brent $120 에너지 역풍. Lagarde "layer cake of shocks" |
| **중국** | 4 | 0 | 1 | **+0.80** | 강력 Beat 유지 — GDP +5.0% / PMI 51.2 / 수출 +12%. 신규 지표 미발표 |
| **한국** | 6 | 0 | 1 | **+0.86** | 극Beat 유지 — Q1 GDP +1.7%. KOSPI 장중 ATH 6,750이나 종가 -1.38% 반전 |

> 글로벌 가중 종합 스코어: **+0.55 (Beat 우세)** (미국 40%+유로존 20%+중국 20%+한국 20%). 모닝 대비 -0.05 (ECB Miss 반영)

---

### 04-29 신규 확인 이벤트

| 날짜 | 지역 | 지표 | 실제 | 컨센서스 | 판정 | 시장 반응 | 출처 |
|------|------|------|------|---------|------|---------|------|
| 04-29 (AH) | 미국 | **MSFT Q3 FY26 EPS** | $4.27 | $4.06 | **Beat (+5.2%)** | AH 혼조 — Azure +40%(컨센 +37% 상회). Q4 가이던스 소폭 하회로 상쇄. AI 연환산매출 $37B(+123%) | [CNBC / Gurufocus / Shacknews] |
| 04-29 (AH) | 미국 | **META Q1 EPS** | $7.31 | $6.65 | **Beat (+9.9%)** | AH -7% — EPS Beat이나 CapEx $125~145B(기존 $115~135B 대폭 상향) 실망 매도. Q2 가이던스 $58~61B | [StockTitan / CNBC / SeekingAlpha] |
| 04-29 (AH) | 미국 | **AMZN Q1 EPS** | $2.78 | $1.64 | **Beat (+69%)** | AH 강세 — AWS +28%(컨센 +26% 상회). 광고 +24%. Rev $181.5B(+17% YoY) | [StockTitan / CNBC] |
| 04-29 (AH) | 미국 | **GOOGL Q1 EPS** | $5.11 | $2.62 | **Beat (+95%)** | AH +4% — Cloud $20.03B(+63%, 컨센 $18.4B 대폭 상회). CapEx $180~190B(상향). "컴퓨팅 부족" 발언 | [9to5Google / Yahoo Finance / CNBC] |
| 04-29 (14:00 ET) | 미국 | **FOMC 통화정책** | 3.50~3.75% 동결 | 동결 100% 컨센 | **중립** (방향 컨센 부합. 단 8-4 분열 = 매파 서프라이즈) | 10Y +7bp(4.42%). 달러 소폭 강세. 시장 해석 = 완화 경로 지연 신호 | [CNBC / CNN / PBS] |
| 04-29 (비발표) | 미국 | **UAE OPEC+ 탈퇴** | 5/1 발효 공식화 | 예상 외 | **Miss (공급 충격 — 경제 서프라이즈 부정)** | WTI +$7(+6.96%/$106.88). Brent $120 근접. 에너지 인플레 재가속 = 미국 소비·생산 비용 충격 | [Al Jazeera / CNBC / Fortune] |

> **META 판정 주의:** EPS/Revenue 기준 Beat. 단 CapEx $125~145B(상향)은 단기 비용 증가 = 시장 반응 -7%(AH)이나 서프라이즈 판정 공식(실적 vs 컨센서스)상 Beat 처리. UAE 탈퇴는 기업 실적 이벤트 외 외부 충격으로 Miss 독립 집계.

---

### 04-29 빅테크 4종 실적 종합 분석

| 기업 | EPS | Revenue | AI 지표 | 시장 반응 | 핵심 메시지 |
|------|-----|---------|---------|---------|-----------|
| MSFT | $4.27(Beat +5.2%) | $82.9B(Beat) | Azure +40%(컨센 +37%), AI 연환산 $37B(+123%), Copilot 2천만 유료 시트 | AH 혼조 | AI 인프라 수요 확인. Q4 가이던스 소폭 하회가 단기 압박 |
| META | $7.31(Beat +9.9%) | $56.31B(Beat +33% YoY) | CapEx $125~145B(기존 $115~135B 상향), Q2 $58~61B | AH -7% | 매출 성장이나 CapEx 급증 = 단기 수익성 압박. 장기 AI 베팅 구조 |
| AMZN | $2.78(Beat +69%) | $181.5B(+17%) | AWS $37.6B(+28%, 컨센 +26%), 광고 $17.24B(+24%), CapEx $43.2B(분기) | AH 강세 | 가장 강력한 실적. 클라우드·광고 쌍끌이. CapEx 규모도 시장 수용 |
| GOOGL | $5.11(Beat +95%) | $109.9B(+22%) | Cloud $20.03B(+63%, 컨센 $18.4B), CapEx $180~190B, "컴퓨팅 부족" | AH +4% | Cloud 63% 성장이 핵심. AI 수요 > 공급 구조 명확화 |

**4종 종합 시사점:**
1. **AI 클라우드 수요 확인** — AWS +28%, Azure +40%, GOOGL Cloud +63% = AI 인프라 투자 수요 구조적 강세 재확인
2. **CapEx 가속화 역설** — AMZN $43.2B/분기, GOOGL $180~190B/연, META $125~145B/연 = AI 인프라 투자 경쟁 가속. 단기 비용 증가 vs 장기 플랫폼 경제성 관건
3. **MSFT Q4 가이던스 하회** — Azure 강세에도 Q4 가이던스 소폭 하회 = 성장 기대치 조정 신호. 5/1 정규장 변수
4. **META -7% AH** — CapEx 실망. 5/1 정규장 나스닥 방향 변수

---

### 04-29 FOMC 서프라이즈 분석

**판정: 방향 중립(동결 컨센 부합) + 매파 구조 서프라이즈**

| 항목 | 내용 | 서프라이즈 여부 |
|------|------|--------------|
| 정책 방향 | 3.50~3.75% 동결 | 중립 (100% 컨센 부합) |
| 표결 구조 | 8-4 (1992년 이후 최다 이견) | 매파 서프라이즈 — 반대 4인 중 3인이 완화 편향 성명 반대 |
| 파월 발언 | "4대 공급 쇼크(팬데믹·우크라·관세·이란·유가)" 명시 | 위험 인식 강화. 인하 경로 추가 지연 신호 |
| 파월 임기 | 의장 5/15 만료 → 이사로 잔류 | 정책 연속성 불확실 잠재 |
| 시장 반응 | 10Y +7bp(4.42%), 달러 소폭 강세, VIX 일시 완화 | 채권 시장만 매파 반응 즉각 |

---

### 전체 서프라이즈 이벤트 이력 (04-13~04-29 누적)

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
| **04-29 (AH)** | **미국** | **MSFT Q3 FY26 EPS** | $4.27 (+5.2%) | $4.06 | **Beat** | [CNBC / Gurufocus] |
| **04-29 (AH)** | **미국** | **META Q1 EPS** | $7.31 (+9.9%) | $6.65 | **Beat** | [StockTitan / CNBC] |
| **04-29 (AH)** | **미국** | **AMZN Q1 EPS** | $2.78 (+69%) | $1.64 | **Beat** | [StockTitan / CNBC] |
| **04-29 (AH)** | **미국** | **GOOGL Q1 EPS** | $5.11 (+95%) | $2.62 | **Beat** | [9to5Google / Yahoo Finance] |
| **04-29** | **미국** | **FOMC 표결 구조** | 8-4 분열 | 만장일치 컨센 | **Miss (매파 서프라이즈)** | [CNBC / CNN / PBS] |
| **04-29** | **글로벌** | **UAE OPEC+ 탈퇴** | WTI $107 | 예상 외 | **Miss (공급 쇼크)** | [Al Jazeera / CNBC] |

---

### "과거형 Beat vs 미래형 Miss" 구조 (04-30 모닝 갱신)

**현재 확인된 Beat 축 (실적 서프라이즈):**
- AMZN Q1 EPS $2.78(컨센 $1.64, +69%) / GOOGL Q1 EPS $5.11(컨센 $2.62, +95%) — 04-29 신규
- MSFT Q3 FY26 EPS $4.27(컨센 $4.06, +5.2%) / META Q1 EPS $7.31(컨센 $6.65, +9.9%) — 04-29 신규
- GE Aerospace Beat(+16.3%) / Intel Q1 EPS $0.29(컨센 $0.01, +2,800%)
- S&P Global PMI 4월 Composite 52.0(컨센 50.6)
- 한국 Q1 GDP +1.7% QoQ(컨센 +0.9% 상회)
- TSLA Q1 EPS $0.41(컨센 $0.37, +10.8%)
- 중국 Q1 GDP +5.0% / PMI 51.2 / 수출 +12%

**선행 Miss 축 (미래 부정 신호):**
- UAE OPEC+ 탈퇴(5/1 발효) — WTI $107, 에너지 쇼크 재가속 = 기업 비용·소비자 물가 상방
- FOMC 8-4 분열(매파 서프라이즈) — 완화 경로 추가 지연 신호. 파월 의장 임기 5/15 만료 불확실
- META CapEx $125~145B 상향 — 단기 수익성 압박 구조
- Honeywell Rev Miss — 자동화·소프트웨어 수요 약화 패턴(IBM·ServiceNow 동일)
- 미시간 소비심리 47.6(역대 최저급)
- 1Y 인플레기대 4.8%(+1.0%p 급등)
- GDP Q1 Advance + Core PCE 3월 미발표(4/30 08:30 ET) — WTI $107 환경 상방 리스크 최고조
- AAPL Q2 FY26 미발표(4/30 장후) — 관세 리스크·서비스 수익 방향 미확정

**판정:** "빅테크 Beat 강화이나 에너지 쇼크(UAE 탈퇴) + FOMC 매파 구조가 실적 호재를 잠식하는 이중 구조." AMZN/GOOGL 강력 Beat가 4/29 S&P 보합 유지의 배경이나 10Y +7bp(4.42%) + WTI $107 복합 = 4/30 Core PCE가 +0.4%+ 시 스태그플레이션 내러티브 직접 재발 리스크.

---

### 종합 판정 (2026-04-30 모닝 기준)

**미국: Beat 강화 (빅테크 AI 클라우드 Beat + 에너지 쇼크 역풍 이중 구조)** — 스코어 +0.56 (23 Beat / 4 Miss / 7 중립). MSFT/AMZN/GOOGL/META 4종 EPS Beat 추가로 Beat 절대 수 대폭 증가. 단 UAE OPEC 탈퇴(WTI $107) + FOMC 8-4 분열이 선행 리스크 구조 악화. 4/30 Core PCE + AAPL 실적이 방향 최종 판별.

**유로존: 소폭 개선 유지** — +0.17. ECB 4/30 25bp 인하 컨센서스. Brent $120 = 에너지 인플레 변수 극단화로 ECB 인하 속도 제약 리스크 증가.

**중국: 강력 Beat 유지** — +0.80. GDP+PMI+수출 3중 구조 변화 없음. 신규 지표 미발표.

**한국: 극Beat 강화 유지** — +0.86. KOSPI 6,690 신고가. Q1 GDP +1.7% 기저 구조 유지. UAE 쇼크(에너지 수입국 비용 부담) 잠재 변수.

**글로벌 종합: +0.60 (Beat 우세)** — 전일 +0.59 대비 소폭 상승(빅테크 4종 Beat 반영). 단 UAE 에너지 쇼크 + FOMC 매파 분열이 Beat 우세 구조를 잠식할 최대 변수. 4/30 08:30 ET GDP/PCE 동시 발표가 금일 최대 이벤트.

---

### 이번 주 주요 서프라이즈 이벤트 달력 (04-30~05-12)

| 날짜 | 이벤트 | 컨센서스 (추정) | 서프라이즈 리스크 | 시장 영향 |
|------|------|--------------|----------------|---------|
| **4/30 (수) 08:30 ET** | **GDP Q1 2026 Advance** | 컨센 ~2.1% (GDPNow 1.2%) | 극고 | <1.0% 시 침체 내러티브. WTI $107 = 스태그플레이션 경보 |
| **4/30 (수) 08:30 ET** | **Core PCE 3월** | ~+0.3% MoM | 극고 | +0.4%+ 시 Fed 인하 경로 붕괴. WTI $107 환경 = 에너지 CPI 상방 |
| **4/30 (수) 08:30 ET** | Employment Cost Index Q1 | — | 고 | 임금 인플레 확인 여부 |
| **4/30 (수) 14:15 ET** | **ECB 통화정책 결정** | 25bp 인하 컨센 | 고 | Brent $120 = 에너지 인플레 역풍 대응 메시지 |
| **4/30 (수) 장후** | **AAPL Q2 FY26** | 서비스 ~$26.7B / AI 전략 | 극고 | Tim Cook 마지막 주요 발표. 관세 리스크·서비스 수익 방향 |
| **4/30 (수) 장후** | Eli Lilly (LLY) Q1 | — | 고 | 비만치료제 수요 확인 |
| **4/30 (수) 장후** | Caterpillar (CAT) Q1 | — | 고 | 인프라·건설 수요 방향 |
| **5/1 (목) 정규장** | AMZN / GOOGL 강세 + META 약세 반영 | — | 극고 | AH 실적 정규장 반영 방향 |
| 5/08 (금) | **4월 NFP** | — | 극고 | 노동시장 에너지·관세 충격 반영 여부 |
| **5/12 (화)** | **4월 CPI** | — | **극고** | WTI $90~107 4월 구간 에너지 인플레 최종 판별 |

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
| 2026-04-24 | correlation-monitor (full) | 04-24 정기 갱신. 신규 확정 데이터 없음 — 스코어 변동 없음. 달력 04-24 기준 갱신. |
| 2026-04-26 | correlation-monitor (quick) | 04-26 모닝 갱신. PMI Beat(04-24) + Intel Beat(04-24 AH) + 한국 Q1 GDP Beat(04-24) 3건 추가. 미국 13→15 Beat, 스코어 +0.58→+0.59. 한국 5→6 Beat, 스코어 +0.83→+0.86. 실업청구 214K 중립 추가. 글로벌 +0.60 유지. |
| 2026-04-27 | correlation-monitor (이브닝, full) | 04-27 이브닝 full 갱신. 이란 특사 취소 + 신제안 혼조 서프라이즈 추가. KOSPI 6,615 + Nikkei 60,537 신고가 이벤트 기록. 4/29~4/30 초압축 이벤트 달력 갱신. |
| 2026-04-28 | correlation-monitor (이브닝, full) | 04-28 이브닝 full 갱신. UPS Beat + GM 중립(EBIT 상향) + GE Aerospace Beat(+16.3%) + Honeywell EPS Beat / Rev Miss 4종 반영. 미국 Beat 15→18(+3), Miss 2→3(+1), 중립 5→6(+1). 스코어 +0.59→+0.56(Honeywell Rev Miss 반영). 글로벌 +0.60→+0.59. |
| 2026-04-30 | correlation-monitor (모닝, full) | 04-29 빅테크 AH 4종 + FOMC + UAE 충격 반영. 미국 Beat 18→23(+5: MSFT/META/AMZN/GOOGL Beat), Miss 3→4(+1: UAE/FOMC 8-4 매파 서프라이즈), 중립 6→7(+1: FOMC 방향 중립). 스코어 +0.56 유지(Beat+5 / Miss+1 상쇄 구조). 글로벌 +0.59→+0.60(빅테크 Beat 우세). AMZN/GOOGL 강력 Beat(+69%/+95%) 분석 추가. CapEx 가속화 역설 구조 명시화. UAE 에너지 쇼크 + FOMC 매파 이중 역풍 분석. 4/30 GDP/PCE 극고 리스크 강조. |
