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
