---
file: 2026_recommendations
type: append-only
created: 2026-04-07
write_owner: briefing-lead
read_owners: [briefing-lead, briefing-report-generator, global-macro-analyst]
---

# 투자 제안 기록 — 2026

> **목적:** 모든 브리핑 모듈(모닝/이브닝/주간/리밸런싱/크립토/모델포트폴리오/글로벌인텔리전스)에서 산출된
> 신규 투자 아이디어·자산군 방향·시나리오 분기를 단일 파일에 누적.
>
> **갱신 주체:** briefing-lead 가 매 브리핑 종결 시 (Step 8.5) 자동 append.
> **소비 주체:** `/성과리뷰`, `/주간리포트` C-9 가 본 파일을 읽어 적중률 계산.
>
> ⚠️ **수정·삭제 절대 금지** — append only.
> 정정 필요 시 새 행 추가 + 기존 행의 status 만 변경.

---

## 형식 (Markdown 표 — 한 줄 = 한 제안)

| 제안일 | 모듈 | 카테고리 | 대상 자산/티커 | 방향 | 시간축 | 확신 | 근거 (1줄) | 출처 산출물 | status |
|---|---|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | morning/evening/weekly/crypto/portfolio/global/rebalancing | 종목/ETF/토큰/자산군/시나리오/이벤트 | 티커 또는 명칭 | Bull/Bear/중립 | 단기/중기/장기 | 높음/중간/낮음 | ... | reports/briefing/...html | 진행중/적중/오류/만료 |

### 카테고리 정의
- **종목**: 개별 주식 (티커 명시)
- **ETF**: 상장 펀드 (티커 명시)
- **토큰**: 디지털 자산 (BTC/ETH/SOL 등)
- **자산군**: 자산군 수준 방향 (예: "10Y 국채 상승 베팅")
- **시나리오**: G-8 시나리오 플래닝 분기
- **이벤트**: 거시 이벤트 (FOMC, 실적 등) 시장 반응 예측

### 시간축
- **단기**: 1~3개월
- **중기**: 3~12개월
- **장기**: 1~5년

### status (`/성과리뷰` 단계에서 갱신)
- **진행중**: 평가 시점 미도래 (시간축 종료 전)
- **적중**: 방향 일치 + 변동률 > 1% (briefing-lead 가 실측 대조)
- **오류**: 부호 반대 + 변동률 > 1%
- **만료**: 시간축 종료 + 변동률 ≤ 1% (방향성 약함)

---

## 누적 (briefing-lead 가 자동 append)

| 제안일 | 모듈 | 카테고리 | 대상 | 방향 | 시간축 | 확신 | 근거 | 출처 | status |
|---|---|---|---|---|---|---|---|---|---|
| 2026-04-07 | morning | 이벤트 | 2026-04-10 美 3월 CPI (Core) | Bear (인플레 재점화 우세) | 단기 | 중간 | 관세 전가율 50~70%, Core 2026Q2 +0.5~1.5%p 상방 압력 추정 [us_economy.md §3] | reports/briefing/morning_20260407.html | 진행중 |
| 2026-04-07 | morning | 자산군 | Gold (Spot, IAU/GLD) | Bull (기축통화 균열 프리미엄) | 중기 | 중간 | Gold↔DXY 역상관 약화 + 중앙은행 매수 급증 + 미 재정적자 GDP 대비 -6.5~-7.0% [global_risk_factors.md §4, us_economy.md §8] | reports/briefing/morning_20260407.html | 진행중 |
| 2026-04-07 | morning | 자산군 | 미국 장기 국채 (TLT) | Bear (요구수익률 상방 압력) | 중기 | 중간 | MOVE 120~130 채권 변동성 고조 + 관세 인플레 2차 효과 + 재정적자 구조 [global_risk_factors.md §2, us_economy.md §8] | reports/briefing/morning_20260407.html | 진행중 |
| 2026-04-07 | morning | 종목 | SK하이닉스 (055930.KS) | Bull (HBM·Tier 1 수혜 구조) | 중기 | 중간 | HBM3E+ 대중 全禁 + Tier 1 한국 무제한 + 2026 한국 반도체 수출 +10~15% YoY 전망 [geopolitics.md §1-2, korea_economy.md §5-1] | reports/briefing/morning_20260407.html | 진행중 |
| 2026-04-07 | morning | 자산군 | 한국 방산 (한화에어로·LIG넥스원·KAI) | Bull (지정학 다중 수혜) | 장기 | 높음 | 우크라이나 재건 + 유럽 방위비 GDP 3% + 북한 도발 [geopolitics.md §4·§5·§8] | reports/briefing/morning_20260407.html | 진행중 |
| 2026-04-07 | morning | 시나리오 | 30일 매크로 베이스 시나리오 (위험등급 4 유지) | 중립 (확률 ~55%) | 단기 | 중간 | 4월 FOMC 동결 + 관세 유지 + 브렌트 70~78 박스 + 원/달러 1,410~1,460 [macro_20260407.md §3] | reports/briefing/morning_20260407.html | 진행중 |
| 2026-04-13 | evening | ETF | Energy Select Sector SPDR (XLE) | Bull (호르무즈 봉쇄 수혜) | 단기~중기 | 높음 | 호르무즈 봉쇄 -> WTI $105+ + SPR 방출 한계 + OPEC 감산 유지 [Bloomberg 보도, CNBC] | reports/briefing/evening_20260413.html | 진행중 |
| 2026-04-13 | evening | 종목 | 한화에어로스페이스 (012450.KS) | Bull (방산 구조적 상승) | 장기 | 높음 | 중동 분쟁 장기화 + 유럽 NATO GDP 3% + 한국 방산 수출 파이프라인 [geopolitics.md §4, §5] | reports/briefing/evening_20260413.html | 진행중 |
| 2026-04-13 | evening | 자산군 | Gold (GLD/IAU) | Bull (구조적 상승) | 중기~장기 | 높음 | Gold-DXY 역상관 약화 Z+1.8sigma + 중앙은행 연 1,000톤+ 매수 + 미 재정적자 GDP -6.5~-7.0% [us_economy.md §8, global_risk_factors.md §4] | reports/briefing/evening_20260413.html | 진행중 |
| 2026-04-13 | evening | 시나리오 | 30일 매크로 베이스: 봉쇄 2~4주 지속 + 부분 완화 (위험등급 5) | Bear (확률 45%) | 단기 | 중간 | WTI $100~115 유지, S&P -3~5%, VIX 25~30, 원/달러 1,500+ [Bloomberg, CNBC] | reports/briefing/evening_20260413.html | 진행중 |
| 2026-04-13 | evening | 이벤트 | 4/14(월) 아시아 개장 갭다운 | Bear (KOSPI -2~4% 예상) | 단기(1일) | 높음 | 호르무즈 봉쇄 주말 발표 미반영 + 에너지 수입국 직격 + 원/달러 1,500 돌파 위험 [CNBC, Bloomberg] | reports/briefing/evening_20260413.html | 진행중 |
| 2026-04-13 | weekly | 종목 | NVDA | Bull (AI 추론 수요 폭발) | 중기 | 중간 | AI 추론 비용 280x 하락->수요 폭증 + TSMC CoWoS 13만wpm 확장 + 2nm GAA 수혜 [tech_breakthrough.md, Gartner] | reports/briefing/weekly_20260413.html | 진행중 |
| 2026-04-13 | weekly | ETF | SHY (iShares 1-3Y Treasury) | 방어적 Bull | 단기~중기 | 높음 | 금리 3.81% 확보 + 듀레이션 리스크 최소 + 봉쇄 장기화 시 안전지대 [us_monetary_policy.md, CNBC] | reports/briefing/weekly_20260413.html | 진행중 |
| 2026-04-13 | weekly | 시나리오 | KOSPI "코리아 프리미엄" 반전 리스크 | Bear (조건부) | 중기 | 중간 | 원/달러 1,500+ 시 외국인 이탈 + 경상수지 적자 전환 + BOK 인하 후퇴 [korea_economy.md, contrarian-card] | reports/briefing/weekly_20260413.html | 진행중 |
| 2026-04-14 | morning | 이벤트 | VIX "거짓 안정" — 4~6주 내 25~30 재상승 | Bear (VIX 상방) | 단기 | 중간 | 소비심리 47.6(역대최저) vs VIX 19.12 괴리. 2022 우크라이나 패턴 반복. Q2 실적쇼크 수렴 가능 [Michigan Survey, CBOE 과거데이터] | reports/briefing/morning_20260414.html | 진행중 |
| 2026-04-14 | morning | 이벤트 | 오늘 PPI — Core PPI +3.2% 상회 시 스태그플레이션 확률 상승 | Bear (인플레 상방) | 단기 | 중간 | CPI 3.3% 에너지 +10.9%의 도매단 전이 여부 확인. Core PPI Miss 시 Fed 6월 인하 완전 소멸 [BLS, Kiplinger] | reports/briefing/morning_20260414.html | 진행중 |
| 2026-04-14 | morning | 자산군 | DXY 구조적 약세 — 98.34, 3년래 최저 | Bear (달러 하방) | 중기 | 중간 | 재정적자 GDP -6.5~-7.0% + 중앙은행 Gold 매수(달러 대체) + 글로벌 탈달러 [FRED, global_risk_factors.md] | reports/briefing/morning_20260414.html | 진행중 |
| 2026-04-14 | global | 시나리오 | 호르무즈 봉쇄 베이스: 장기 대치 2~4개월 (시나리오 B) | Bear (S&P -3~7%, WTI $90~110) | 중기 | 중간 | 미 해군 봉쇄 발효+파키스탄 회담 결렬. 비이란 통항 보장이 완충. 확률 45% [CNN, NPR, CNBC] | reports/briefing/global_intelligence_20260414.html | 진행중 |
| 2026-04-14 | global | 시나리오 | 비료-식량 인플레 2차 파동 (숨은 테마) | Bear (CPI +0.3~0.5%p 추가) | 중기 | 중간 | 비료 +172% YoY + 한국 호르무즈 경유 38.4% + FAO 식품지수 128.5pt. 2~3개월 시차 전이 [supply_chain.md, FAO] | reports/briefing/global_intelligence_20260414.html | 진행중 |
| 2026-04-14 | global | 자산군 | Gold (GLD/IAU) 구조적 Bull 강화 | Bull ($5,000+ 전망) | 중기~장기 | 높음 | DXY 98.34+재정적자+중앙은행 매수 확산+지정학 삼중 지지. JPM $5,055(4Q26E) [J.P. Morgan, World Gold Council, SSGA] | reports/briefing/global_intelligence_20260414.html | 진행중 |
| 2026-04-14 | global | 자산군 | SMR/원자력 인프라 | Bull (AI 전력 수요 구조적 수혜) | 장기 | 중간 | Southern Co $26.5B 원자력 대출+EU SMR 17~53GW 목표+데이터센터 전력 직접 연계 [ASME, EU Commission] | reports/briefing/global_intelligence_20260414.html | 진행중 |
| 2026-04-14 | evening | 종목 | 한화에어로스페이스 (012450.KS) | Bull (3중 구조적 수혜) | 장기 | 높음 | KOSPI 6,000 주도+유럽 ReArm EUR 800B+호르무즈/북한 3중 모멘텀. 방산 수출 파이프라인 가속 [geopolitics.md §4~8, 세계일보] | reports/briefing/evening_20260414.html | 진행중 |
| 2026-04-14 | evening | 종목 | S-Oil (010950.KS) / SK이노베이션 | Bull (정제마진 서프라이즈) | 단기~중기 | 중간 | WTI $97+정제마진 $18(역대급)+재고평가이익. Q1~Q2 실적 서프라이즈 가능. 봉쇄 해소 시 반락 리스크 [energy.md §1, geopolitics.md §9] | reports/briefing/evening_20260414.html | 진행중 |
| 2026-04-14 | evening | 시나리오 | KOSPI 6,000 안착 조건 | Bull (조건부) | 단기~중기 | 중간 | 장중 6,026 터치 후 5,968 마감. 안착 조건: (1) 호르무즈 해소 또는 (2) Q2 반도체 실적 확인. 미충족 시 5,800~6,000 박스 [세계일보, 헤럴드경제] | reports/briefing/evening_20260414.html | 진행중 |
| 2026-04-14 | evening | 이벤트 | IEA/WB/IMF "빠른 정상화 불가" -- 2차 인플레 리스크 | Bear (인플레 상방) | 중기 | 중간 | 3개 국제기관 동시 경고. 비료+연료 가격 구조적 고착. War Risk Premium+IRGC 기뢰(21건). 식품 CPI +0.3~0.5%p 추가 가능 [NBC News, supply_chain.md, FAO] | reports/briefing/evening_20260414.html | 진행중 |
| 2026-04-15 | evening | ETF | GLD (SPDR Gold Shares) / IAU | Bull (구조적 탈달러) | 중기~장기 | 높음 | Gold $4,869 (+2.67%) 신고가 — WTI 급락에도 단절적 강세. DXY 98.13 3년최저 + 중앙은행 매수 + Gold-DXY/Oil 상관관계 붕괴 [daily_snapshot, global_risk_factors §4, J.P. Morgan 보도] | reports/briefing/evening_20260415.html | 진행중 |
| 2026-04-15 | evening | 종목 | 삼성전자 (005930.KS) | Bull (KOSPI 6,141 안착 주도) | 중기 | 중간 | 반도체 수출 3월 $18.7B(+163.9%) + HBM4 H2 양산 + HBM3E 대중 금지 Tier1 한국 수혜 + 외국인 매수 복귀 [산업부, semiconductor.md §1, geopolitics §1-2] | reports/briefing/evening_20260415.html | 진행중 |
| 2026-04-15 | evening | 시나리오 | 호르무즈 완화 1단계 진입 — WTI $85~95 박스 | 중립→Bull (유가 하방) | 단기 | 중간 | 트럼프 재협상 시그널 + 파키스탄 중재 + 비이란 통항 보장 반영. 그러나 IEA/WB/IMF "빠른 정상화 불가" 유효 [daily_snapshot, supply_chain §1-2] | reports/briefing/evening_20260415.html | 진행중 |
| 2026-04-15 | evening | 자산군 | BTC "디지털 금" 내러티브 균열 가능성 | Bear (탈달러 수요 Gold 쏠림) | 단기~중기 | 중간 | NASDAQ +1.96% 리스크온에도 BTC +0.23% 정체. Gold +2.67% vs BTC +0.23% = 탈달러 수요가 BTC 우회. NASDAQ-BTC 동조화 약화 [CoinGecko, Yahoo Finance] | reports/briefing/evening_20260415.html | 진행중 |
| 2026-04-15 | evening | 이벤트 | VIX 18.36 vs 소비심리 47.6 괴리 극대화 — 2~4주 내 25~30 재상승 | Bear (VIX 상방) | 단기 | 중간 | 전일 4~6주 경고에서 단축 갱신. "완화 랠리 소멸 이벤트"(PPI 상방, 호르무즈 재격화, 5월 미중 결렬) 시 반등 폭 확대 [global_risk_factors §2] | reports/briefing/evening_20260415.html | 진행중 |
| 2026-04-16 | morning | 시나리오 | S&P 7,000·NASDAQ 24,000 돌파 후 "후반 사이클 정점" 리스크 | Bear (확률 40% 상향) | 단기~중기 | 중간~높음 | Dow -0.15% 단독 약세 + 10Y 4.28% 반등 + VIX-MOVE 괴리 + BTC 정체 = breadth 쇠퇴 4중 시그널. 2000Q1·2007Q3·2021Q4 유사 패턴 [Yahoo Finance, global_risk_factors §2] | reports/briefing/morning_20260416.html | 진행중 |
| 2026-04-16 | morning | 자산군 | 10Y 국채 금리 4.30% 돌파 시 TLT 추가 하방 | Bear (장기국채) | 중기 | 중간 | 4/15 4.26→4.28 반등. "WTI 급락 = 디스인플레" 서사에 균열. Core CPI/ISM가격 78.3 지속. 5/13 4월 CPI 체크포인트 [us_economy §3, daily_snapshot] | reports/briefing/morning_20260416.html | 진행중 |
| 2026-04-16 | morning | ETF | GLD/IAU 구조적 Bull 3일 연속 확인 | Bull (탈달러 구조) | 중기~장기 | 높음 | Gold $4,844 신고가 근접 유지 + DXY 98.01 3년최저 갱신. 리스크온 랠리에도 환매되지 않는 탈달러 수요 3일 연속 [daily_snapshot, global_risk_factors §4, J.P. Morgan 보도] | reports/briefing/morning_20260416.html | 진행중 |
| 2026-04-16 | morning | 이벤트 | Q1 실적 시즌(4/20주~) — Mag7 Beat 지속 여부가 NASDAQ 24K 방어 핵심 | 중립 (분기점) | 단기 | 중간 | JPM/BAC → MSFT/GOOGL/META/AAPL 순. Beat 지속 시 완화 랠리 3단계, Miss 1건 시 -3~7% 민감. Breadth 쇠퇴 구도에서 실적 서프라이즈 가중치 극대화 [us_economy §2, market consensus] | reports/briefing/morning_20260416.html | 진행중 |
| 2026-04-16 | morning | 종목 | 삼성전자 (005930.KS) | Bull (KOSPI 6,150 재도전 주도) | 중기 | 중간 | NASDAQ 24,000 + 반도체 랠리 동조 + 외국인 매수 지속 + HBM4 H2 양산. 원/달러 1,474 안정 [산업부, semiconductor.md, korea_economy §5-1] | reports/briefing/morning_20260416.html | 진행중 |

---

## 자동 append 절차 (briefing-lead Step 8.5 — 워크플로 통합)

매 브리핑 작성 시 산출물 Write 직후:

```
[Step 8.5] knowledge-db/performance/2026_recommendations.md 에 본 브리핑의
           모든 신규 제안을 위 형식 1행씩 append.

           - 신규 아이디어 (B-6, E-5)            → 카테고리 종목/ETF/토큰
           - 시나리오 (G-8)                       → 카테고리 시나리오
           - 자산군 방향 (A-6, B-8, C-10, D-3)    → 카테고리 자산군
           - 거물 컨버전스 (B-7 추적 종목)         → 카테고리 종목 (방향 추정)
           - 매크로 이벤트 시장 반응 예측 (A-7, B-9) → 카테고리 이벤트

           초기 status 는 항상 "진행중".
```

---

## 검수 결과 F-03 — 본 파일은 기존 부재 상태에서 신규 생성됨.
