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
