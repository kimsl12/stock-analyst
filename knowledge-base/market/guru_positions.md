---
updated: 2026-08-22
valid_until: 2026-09-05
file: guru_positions
sources:
  [
    "13radar",
    "stockcircle",
    "gainify",
    "valuesider",
    "seekingalpha",
    "hedgefundalpha",
    "yahoo_finance",
    "motleyfool",
    "reuters",
    "fortune",
    "cnbc",
    "acquirersmultiple",
    "gurufocus",
    "thestreet",
    "tipranks",
    "insidermonkey",
    "nasdaq",
    "barchart",
    "247wallst",
    "bbae",
    "investorlens",
    "13finsight",
  ]
confidence: medium
last_synced_from_db: 2026-08-22
collection_status: PARTIAL
data_basis: "Q2 2026 13F (포지션일 2026-06-30, 공시 마감 2026-08-14). WebSearch로 Berkshire·Ackman·Druckenmiller·Tepper 4인 핵심 변동 확인(개별 종목 방향·규모 위주, Top10 전체 테이블은 미확보). Dalio·Wood·Marks 3인 Q2 동향 미확인(부분 성공). Burry는 2025-11 해산 지속. 2026-08-22 market-data-collector 주간리포트 보조 갱신."
---

# 거물 투자자 포지션 (Guru Positions)

> **쓰기 권한:** market-data-collector
> **읽기 권한:** briefing-lead, briefing-report-generator, 종목분석 9개 에이전트
> **갱신 빈도:** 분기 1회 (13F 공시 후) + 주간 동향 수시 반영
> **명단 정본:** `reference/guru_watchlist.md` 참조
>
> **중요 고지:** 13F 포지션 데이터는 분기 종료 후 최대 45일 시차 존재.
> 현재 포지션이 아닌 "기준 분기 마감 시점 포지션"임을 반드시 인지.
>
> **2026-08-22 상태:** Q2 2026 13F 공시 마감(8/14) 완료. Berkshire·Ackman·Druckenmiller·Tepper 4인 핵심 변동(종목·방향·규모) 확인 — WebSearch 스니펫 기반이라 Top10 전체 테이블·정밀 비중은 미확보(다음 갱신 시 전면 수집 권장). Dalio·Wood·Marks 3인 Q2 동향 미확인. **⚠️ 시차 고지: 포지션일 2026-06-30 → 공시 마감 2026-08-14(45일) → 본 수집 시점 2026-08-22(공시로부터 8일 경과, 포지션일로부터 53일 경과).**

---

## CURRENT -- Q2 2026 13F (포지션일 2026-06-30, 공시 마감 2026-08-14)

> **⚠️ [13F 고지] 기준일: 2026-06-30 / 공시 마감: 2026-08-14. 현재 시점(8/22)과 약 53일 시차(포지션일 기준). "현재 보유 중"이 아닌 6/30 시점 스냅샷.**
> **수집 방식**: WebSearch 뉴스 스니펫(hedgefundalpha/247wallst/bbae/Yahoo Finance/Seeking Alpha 등) 기반 핵심 변동 요약. 원본 13F 전체 Top10 테이블·정밀 비중(%)은 미확보 — confidence medium.

### 1. Warren Buffett (Berkshire Hathaway) -- Q2 2026 확인

포트폴리오 규모: **$299.3B** (Q1 2026 $263.10B 대비 +13.8%), 보유 종목: **29개** (Q1과 동일 — 추가 종목 정리 없이 규모만 확대)

**핵심 변동 — GOOGL/GOOG 대폭 추가매수(확정):**

| 종목                | 티커  | 이번 분기 매수 | 누적 보유        | 평가액(추정)                          |
| ------------------- | ----- | -------------- | ---------------- | ------------------------------------- |
| Alphabet Class A    | GOOGL | +24,541,369주  | 78,791,167주     | ~$28.16B                              |
| Alphabet Class C    | GOOG  | +23,603,218주  | 27,188,433주     | ~$9.61B                               |
| **GOOGL+GOOG 합산** | —     | —              | **~1억 594만주** | **~$37.77B (포트폴리오 대비 ~12.6%)** |

> 7/11 후속보도(3배 확대, ~~$16.6B, ~6.3%)가 시사했던 방향이 Q2 13F 원자료로 확정·추가 확대됐다. GOOGL+GOOG 합산 ~$37.77B는 AAPL(Top1, 비중 하락 추세)에 이은 명실상부 Top2~~3권 포지션으로 추정된다(정밀 순위는 미확보). AI 인프라 CapEx·클라우드 시장점유 베팅이 Q1보다 한층 강화된 것으로 해석.

**전략 해석:** Greg Abel 체제 2번째 분기. 종목 수는 29개로 동결(추가 단순화 없음), 포트폴리오 규모는 재평가 효과+신규자금 유입으로 $263B→$299B 확대. GOOGL/GOOG 공격적 추가매수가 이번 분기 최대 시그널. [Yahoo Finance/247wallst(2026-08-17), hedgefundalpha "Q2 2026 13F Roundup"(2026-08월)]

---

### 2. Bill Ackman (Pershing Square) -- Q2 2026 확인

포트폴리오 규모: **$19.47B** (Q4 2025 $15.53B 대비 +25.4%), 보유 종목: **10 → 14개**로 확대

| 구분          | 종목                                                    | 비고                                                                                     |
| ------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **신규 매수** | Visa, Mastercard, S&P Global, Netflix                   | 4개 신규 편입 — 결제/데이터/스트리밍 우량 프랜차이즈 이동                                |
| **전량 청산** | **Alphabet (GOOGL)**                                    | ⚠️ Berkshire·Druckenmiller·Tepper와 정반대 방향 — Q1(95%+ 청산)에 이어 Q2 완전 청산 확정 |
| **추가 매도** | UMG(Universal Music Group)                              | 인수 제안 거절 후 지분 처분                                                              |
| **비중 확대** | Uber, Microsoft, Howard Hughes, Restaurant Brands, Meta | 핵심 컨빅션 종목 집중도 강화                                                             |

> **해석:** Ackman은 GOOGL을 Q1에 이어 Q2에도 완전히 등지며 "AI 인프라 경제성은 클라우드(Buffett)가 아닌 엔터프라이즈 유통(MSFT)·플랫폼(META/UBER) 쪽"이라는 기존 베팅을 재확인·강화했다. 동시에 Visa·Mastercard·S&P Global·Netflix 등 우량 캐시카우형 신규 편입으로 포트폴리오를 10→14종목으로 소폭 분산. [Seeking Alpha "Tracking Bill Ackman's Pershing Square 13F — Q2 2026 Update", bbae.com "13F Highlights Q2 2026"(2026-08월)]

---

### 3. Stanley Druckenmiller (Duquesne Family Office) -- Q2 2026 확인

**분기 중 매매 매우 활발**: 신규 48종목 진입 + 23종목 전량 매도

| 구분                     | 종목                                                       | 비고                                                                  |
| ------------------------ | ---------------------------------------------------------- | --------------------------------------------------------------------- |
| **크립토 vehicle 교체**  | ETHB 전량 청산($294M) → IBIT(spot Bitcoin ETF) 신규($264M) | Bitcoin ETF 상품 자체를 선물/파생 연계형에서 현물(spot) 기반으로 교체 |
| **반도체·빅테크 확대**   | TSM(+$114M), STM(+$142M), AMZN(+$187M)                     | AI 밸류체인 노출 확대                                                 |
| **헬스케어 확대**        | NTRA(+$252M), INSM(+$107M, +140%)                          | 기존 Top1(NTRA) 컨빅션 유지·강화                                      |
| **신규 진입**            | CDW($140M), **GOOGL($120M, 336,300주)**                    | GOOGL은 Buffett·Tepper와 동일 방향 컨버전스                           |
| **Top Picks(보도 기준)** | Bitdeer, Hyperliquid                                       | hedgefundalpha "Q2 2026 13F Roundup" 제목 언급 — 세부 규모 미확보     |

> **해석:** 48종목 신규·23종목 청산이라는 이례적으로 높은 회전율. 크립토 익스포저를 파생형에서 현물형으로 교체한 점, GOOGL 신규 진입으로 Buffett·Tepper와 궤를 같이한 점이 특징. [hedgefundalpha "Q2 2026 13F Roundup: Berkshire's Alphabet Surge; Druckenmiller's Top Picks Are Bitdeer & Hyperliquid"(2026-08월)]

---

### 4. David Tepper (Appaloosa) -- Q2 2026 부분 확인

| 항목                                  | 내용                                                                                                                                                     |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Berkshire Hathaway 대상 신규 베팅** | "새로운 베팅(against)" 보도 — 숏/풋 등 방향·규모 미확보(confidence low)                                                                                  |
| **Alphabet(GOOGL/GOOG) 매수**         | Yahoo Finance headline "Billionaires ... Tepper All Are Loading into Alphabet Stock" — Buffett·Druckenmiller와 동일 방향 컨버전스 확인, 정밀 수량 미확보 |

> **해석:** Berkshire 대상 신규 베팅의 방향(숏 vs 헤지)이 불명확해 해석에 주의가 필요하다 — 다음 갱신 시 원자료 확인 우선순위. GOOGL 매수는 3인 컨버전스의 세 번째 축으로 확인. [Yahoo Finance/247wallst(2026-08-17), "Billionaires Stanley Druckenmiller, Seth Klarman, and David Tepper All Are Loading into Alphabet Stock. Buffett's Berkshire Is Also Buying."]

---

### 5~8. Ray Dalio · Cathie Wood · Howard Marks · Michael Burry — Q2 2026 미수집

| 투자자        | 기관        | Q2 2026 수집 상태        | Q1 2026 마지막 확인 포지션                        |
| ------------- | ----------- | ------------------------ | ------------------------------------------------- |
| Ray Dalio     | Bridgewater | 미확인                   | Q4 2025 기준: SPY/IVV Top2, NVDA +54%, ORCL +361% |
| Cathie Wood   | ARK         | 미확인(Q1도 주간 동향만) | Q4 2025 기준: TSLA Top1(-19%), CoreWeave +311%    |
| Howard Marks  | Oaktree     | 미확인                   | Q4 2025 기준: EXE Top1(에너지), TRMD, AU 금광     |
| Michael Burry | Scion       | N/A (2025-11 해산 지속)  | —                                                 |

> 다음 정기 갱신 시 4인 Q2 13F 전면 수집 필요(`/시장데이터수집 13F` 재실행 권장).

---

## 컨버전스 시그널 — Q2 2026 13F 신규 (포지션일 2026-06-30)

| 종목/테마                            | 동일 방향 투자자                                                                                                          | 방향           | 신뢰도                                                       |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------ |
| **Alphabet(GOOGL/GOOG) 대규모 매수** | **Buffett(+$37.8B 누적)** + **Druckenmiller(신규 $120M)** + **Tepper(매수, 규모 미확인)** — 감시대상 8인 중 3인 동일 방향 | 강력 매수      | high (Buffett·Druckenmiller 원자료 확인, Tepper는 보도 기반) |
| **Alphabet(GOOGL) 다이버전스**       | **Ackman(전량 청산, Q1·Q2 연속)** — 위 3인과 정반대                                                                       | 매도           | high                                                         |
| **비트코인 익스포저 vehicle 전환**   | Druckenmiller(ETHB 청산→IBIT 신규)                                                                                        | 파생→현물 전환 | medium(1인만 확인)                                           |
| **결제·데이터 우량주 신규편입**      | Ackman(Visa·Mastercard·S&P Global 신규)                                                                                   | 매수           | medium(1인만 확인)                                           |

> ⚠️ **핵심 다이버전스**: Berkshire·Druckenmiller·Tepper(3인)가 GOOGL을 공격적으로 사들이는 동안, Ackman은 정반대로 완전 청산했다. "AI 인프라 승자"를 두고 클라우드/검색(Alphabet) 베팅과 엔터프라이즈 유통·플랫폼(MSFT/META/UBER) 베팅이 8인 감시대상 내에서도 뚜렷하게 갈리고 있다 — 이는 7/11 갱신 시점부터 관찰된 다이버전스가 Q2 원자료로 재확인·강화된 것.
> Q4 2025 기준 컨버전스 시그널(AMZN·META·MU 등)은 아래 HISTORY 섹션 참조.

---

## 주간 동향 (2026-07-06~07-11) -- 이전 (Q1 13F 후속 보도 기반)

> 원본 13F 재수집이 아닌, Q1 2026 13F(포지션일 2026-03-31, 공시 2026-05-15)에 대한 **사후 후속 보도** 기반이었다. Q2 13F 원자료(위 CURRENT 섹션)로 대체·확정됨.

| 투자자             | 기관            | 행동                                         | 세부 내용                                                                                                                                                                                                                        | 출처                                                   |
| ------------------ | --------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **Warren Buffett** | Berkshire       | **GOOGL 지분 3배 확대 — Top5 근접/진입**     | Q1 2026 13F 후속 분석: Alphabet 지분을 약 3배 확대해 약 5,780만주(~~$16.6B, 포트폴리오 대비 ~6.3%)로 확대. 2026년 AI 인프라 CapEx($175~~185B) 클라우드 점유 베팅으로 해석. → **Q2 13F 원자료로 추가 확대 확정(위 CURRENT 참조)** | Barchart/Nasdaq/The Globe and Mail [2026-07 상순 보도] |
| **Bill Ackman**    | Pershing Square | **GOOGL 95%+ 청산 → MSFT 재배치**            | Q1 2026 13F 후속 분석: Alphabet 포지션 95% 이상 매도. → **Q2 13F 원자료로 전량 청산 확정(위 CURRENT 참조)**                                                                                                                      | Barchart/Nasdaq [2026-07 상순 보도]                    |
| **Cathie Wood**    | ARK Invest      | AI·디지털자산·차세대 헬스케어 비중 확대 지속 | Q1 13F 미수집, Q2도 미수집(2026-08-22 기준)                                                                                                                                                                                      | GuruFocus [6월 말 보도]                                |

---

## HISTORY -- Q1 2026 13F 포지션 (기준일 2026-03-31, 공시 2026-05-15)

### 1. Warren Buffett (Berkshire Hathaway) -- Q1 2026 $263.10B, 29종목

포트폴리오 규모: $263.10B (Q4 2025 $274.16B 대비 -4.0%)

| 순위 | 종목             | 티커 | 비중   | Q1 변동      | Q4 2025 비중 |
| ---- | ---------------- | ---- | ------ | ------------ | ------------ |
| 1    | Apple            | AAPL | 21.99% | 지속 축소 중 | 22.60%       |
| 2    | American Express | AXP  | 17.43% | 소폭 변동    | 20.46%       |
| 3    | Coca-Cola        | KO   | 11.56% | 유지         | 10.20%       |
| 4    | Bank of America  | BAC  | 9.52%  | 지속 축소 중 | 10.38%       |
| 5    | Chevron          | CVX  | 6.64%  | 소폭 변동    | 7.24%        |

**Q1 2026 핵심 변화:**

- 포트폴리오 종목 수 42 → 29 (-13개): 대규모 포지션 정리
- 전체 규모 $274B → $263B (-$11B): 현금 비중 추가 확대 추정
- AAPL Top1 유지하나 비중 소폭 하락 (22.60% → 21.99%)
- AXP 비중 하락 (20.46% → 17.43%): 이익실현 추정
- KO 비중 상승 (10.20% → 11.56%): 방어주 강화
- GOOGL 지분 3배 확대(~$16.6B) — Q2 13F로 추가 확대 확정(위 CURRENT 참조)

**전략 해석:** Greg Abel 체제 첫 분기(Buffett 2025-12-31 CEO 은퇴). 종목 수 대폭 축소(42→29) = 포트폴리오 단순화·방어화. [valuesider Q1 2026 13F, 2026-05-15]

---

### 2~8. 나머지 7인 Q1 2026 13F — 요약

| 투자자                | 기관            | Q1 2026 수집 상태        | 핵심 메모                                                                               |
| --------------------- | --------------- | ------------------------ | --------------------------------------------------------------------------------------- |
| Ray Dalio             | Bridgewater     | 미수집                   | Q4 2025 데이터 최신 유지                                                                |
| Michael Burry         | Scion           | N/A (2025-11 해산)       | Q3 2025 최종 데이터                                                                     |
| Cathie Wood           | ARK             | 미수집(주간 동향만 확인) | Q4 2025 데이터 최신 유지                                                                |
| Stanley Druckenmiller | Duquesne        | 미수집                   | Q4 2025 데이터 최신 유지 → **Q2 13F로 GOOGL 신규 확인(위 CURRENT 참조)**                |
| Howard Marks          | Oaktree         | 미수집                   | Q4 2025 데이터 최신 유지                                                                |
| David Tepper          | Appaloosa       | 미수집                   | Q4 2025 데이터 최신 유지 → **Q2 13F로 GOOGL 매수·Berkshire 베팅 확인(위 CURRENT 참조)** |
| Bill Ackman           | Pershing Square | 미수집(주간 동향만 확인) | Q4 2025 데이터 최신 유지 → **Q2 13F로 GOOGL 전량청산 확정(위 CURRENT 참조)**            |

---

## HISTORY -- Q4 2025 13F 포지션 (기준일 2025-12-31, 공시 2026-02-17)

### 1. Warren Buffett (Berkshire Hathaway) -- Q4 2025 $274.16B, 42종목

| 순위 | 종목             | 티커  | 비중   | 시장가치 | 주식 수 | Q4 변동          |
| ---- | ---------------- | ----- | ------ | -------- | ------- | ---------------- |
| 1    | Apple            | AAPL  | 22.60% | $61.96B  | 227.92M | -4.3% (-10.3M주) |
| 2    | American Express | AXP   | 20.46% | $56.09B  | 151.61M | 유지             |
| 3    | Bank of America  | BAC   | 10.38% | $28.45B  | 517.3M  | -8.9% (-50.8M주) |
| 4    | Coca-Cola        | KO    | 10.20% | $27.96B  | 400M    | 유지             |
| 5    | Chevron          | CVX   | 7.24%  | $19.84B  | 130.16M | +6.6% (+8.1M주)  |
| 6    | Moody's          | MCO   | 4.60%  | $12.6B   | 24.67M  | 유지             |
| 7    | Occidental       | OXY   | 3.97%  | $10.89B  | 264.94M | 유지             |
| 8    | Chubb            | CB    | 3.90%  | $10.69B  | 34.25M  | +9.3% (+2.9M주)  |
| 9    | Kraft Heinz      | KHC   | 2.88%  | $7.9B    | 325.63M | 유지             |
| 10   | Alphabet         | GOOGL | 2.04%  | $5.59B   | 17.85M  | 유지             |

**신규 매수:** NYT, Liberty Live Holdings | **추가:** CVX, CB, DPZ | **축소:** AAPL, BAC, AMZN(-77%)

---

### 2. Ray Dalio (Bridgewater Associates) -- Q4 2025 $27.42B, 1,040종목

Top10: SPY(11.1%), IVV(10.5%), NVDA(+54%), LRCX, CRM, GOOGL(-40%), MSFT, AMZN(+73%), ADBE, GEV
핵심 변동: ORCL +361%, NVDA +54%, MU 대폭추가 / GOOGL -40%, META -46%, UBER -64%

---

### 3. Michael Burry (Scion Asset Management) -- 해산 (2025-11-10 SEC 등록 해지)

Q3 2025 최종: PLTR 풋 + NVDA 풋 = 96.72% ($1.099B). AI 버블 베팅 후 해산.

---

### 4. Cathie Wood (ARK) -- Q4 2025 $15.07B, 196종목

Top10: TSLA(8.7%), SHOP(4.3%), ROKU(-20%), COIN(추가), PLTR(-20%), CRSP(추가), AMD, HOOD, TER, TEM
핵심 변동: CRWV +311%(신규), COIN/CRSP/TEM 추가 / TSLA-19%, ROKU-20%, PLTR-20%

---

### 5. Stanley Druckenmiller (Duquesne) -- Q4 2025 $4.49B, 62종목

Top10: NTRA(12.3%), XLF(신규6.8%), RSP(신규5.6%), WWD, INSM, TSM(-29%), TEVA, AMZN(+69%), BE(신규), EWZ(신규)
핵심 변동: GOOGL +277%, AMZN +69%, SE +244% / TEVA -65%, INSM -39%, TSM -29%

---

### 6. Howard Marks (Oaktree) -- Q4 2025 $7.03B, 172종목

Top10: EXE(7.95%), TRMD(-35%), AU, GTX(-46%), INDV, VNOM(추가), TDS, B, TLN, CORZ(+31%)
핵심 변동: VNOM/CORZ 추가 / TRMD -35%, GTX -46% / 완전매도: EchoStar, Nabors, Sea

---

### 7. David Tepper (Appaloosa) -- Q4 2025 $6.85B, 38종목

Top10: BABA(-20%), MU(+200%), GOOG(+29%), AMZN(-13%), TSM(+7%), META(+62%), NVDA(-11%), EWY(신규), NRG, GLW
핵심 변동: MU +200%(HBM AI 베팅), EWY 신규(한국 반도체), META +62% / BABA -20%

---

### 8. Bill Ackman (Pershing Square) -- Q4 2025 $15.53B, 11종목

Top10: BN(18.2%), UBER(15.9%), AMZN(+65%), GOOG(12.5%), META(신규$1.76B), QSR, HHH, HLT
핵심 변동: META 신규 $1.76B, AMZN +65% / CMG 완전매도(-$844M), GOOGL(A) -86%

---

## 컨버전스 시그널 (Q4 2025 13F 기준 -- 포지션일 2025-12-31)

| 종목/테마            | 동일 방향 투자자                                                 | 방향      | 신뢰도 |
| -------------------- | ---------------------------------------------------------------- | --------- | ------ |
| **AMZN 추가매수**    | Ackman +65% + Druckenmiller +69% + Dalio +73% (3인)              | 강력 매수 | high   |
| **META 대규모 진입** | Ackman 신규 $1.76B + Tepper +62% (2인)                           | 매수      | high   |
| **GOOGL 추가**       | Druckenmiller +277% + Tepper +29% (2인)                          | 매수      | high   |
| **MU (HBM/반도체)**  | Tepper +200% + Dalio 대폭추가 (2인)                              | 강력 매수 | high   |
| **Gold/금광 유지**   | Marks(AU+B) + Dalio(Gold 15% 추천) (2인)                         | 강세 유지 | high   |
| **에너지/전력**      | Marks(EXE/VNOM/TLN) + Buffett(CVX/OXY) + Druckenmiller(BE) (3인) | 유지/추가 | high   |
| **한국/EWY**         | Tepper 신규 $286M (1인)                                          | 신규 매수 | medium |

> Q2 2026 컨버전스 재집계는 위 "컨버전스 시그널 — Q2 2026 13F 신규" 섹션 참조.

---

## 13F 공식 데이터 현황

| 분기    | 포지션 기준일 | 공시 마감  | 수집 상태   | 비고                                                                                                                       |
| ------- | ------------- | ---------- | ----------- | -------------------------------------------------------------------------------------------------------------------------- |
| Q4 2025 | 2025-12-31    | 2026-02-17 | **SUCCESS** | 7인 완료 + Burry 해산                                                                                                      |
| Q1 2026 | 2026-03-31    | 2026-05-15 | **PARTIAL** | Berkshire만 확인. 나머지 7인 미수집                                                                                        |
| Q2 2026 | 2026-06-30    | 2026-08-14 | **PARTIAL** | Berkshire·Ackman·Druckenmiller·Tepper 4인 핵심 변동 확인(뉴스 스니펫 기반, Top10 전체 미확보). Dalio·Wood·Marks 3인 미수집 |

> Q2 2026 나머지 3인 + 4인의 Top10 전체 테이블 수집: `/시장데이터수집 13F` 재실행 권장.

---

## 업데이트 로그

| 날짜           | 에이전트                                    | 변경 내용                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-07     | market-data-collector                       | 수집 시도 -- 전 항목 네트워크 차단. 2회 재시도 후 N/A 처리.                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 2026-04-17     | market-data-collector                       | 이브닝 재수집 -- PARTIAL.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 2026-04-18     | kb-updater                                  | Q4 2025 13F 전면 수집 완료. 7인 + Burry 해산.                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 2026-04-28     | market-data-collector                       | 주간 동향 반영 -- Wood AMD 매도+AMZN 매수, Ackman AMZN 코멘트, Druckenmiller GOOGL 추가.                                                                                                                                                                                                                                                                                                                                                                                                             |
| 2026-05-20     | market-data-collector (모닝)                | Q1 2026 13F 공시 마감(5/15) 반영. Berkshire Q1 확인($263B, 29종목, AAPL Top1 유지). 나머지 7인 미수집(예산 소진). Q4 2025 데이터 HISTORY 섹션으로 이동. collection_status: PARTIAL.                                                                                                                                                                                                                                                                                                                  |
| 2026-07-11     | market-data-collector (이브닝)              | 주간 동향 갱신(원자료 아닌 후속보도 기반) — Berkshire GOOGL 지분 3배 확대(~$16.6B, Top5 근접), Ackman GOOGL 95%+ 청산→MSFT 재배치 확인. Q1 13F 나머지 7인 여전히 미수집.                                                                                                                                                                                                                                                                                                                             |
| **2026-08-22** | **market-data-collector (주간리포트 보조)** | **Q2 2026 13F(포지션일 6/30, 공시마감 8/14) 원자료 반영. Berkshire GOOGL+GOOG 추가매수 확정(합산 ~$37.77B, 7/11 후속보도 방향 재확인·확대), Druckenmiller GOOGL 신규진입($120M)+ETHB→IBIT 전환, Tepper GOOGL 매수+Berkshire 대상 신규베팅(방향미상), Ackman GOOGL 전량청산+Visa/Mastercard/S&P Global/Netflix 신규편입 확인. → GOOGL 3인(Buffett·Druckenmiller·Tepper) 매수 vs Ackman 1인 매도의 뚜렷한 다이버전스 신규 컨버전스 시그널로 등재. Dalio·Wood·Marks 3인 Q2 동향 미수집(PARTIAL 유지).** |
