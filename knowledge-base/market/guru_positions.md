---
updated: 2026-04-17
valid_until: 2026-07-07
file: guru_positions
sources: ["InsiderMonkey", "Dataroma(접근불가)", "Bloomberg", "AcquirersMultiple", "WhalesBook", "TheStreet"]
confidence: low
last_synced_from_db: 2026-04-17
collection_status: PARTIAL
failure_reason: "13F 포지션(Dataroma/Gurufocus/SEC EDGAR) 직접 접근 불가. MCP 웹검색으로 최근 코멘트 및 방향성 부분 수집. include_13f 플래그 미수신으로 정규 분기 갱신 미실시. PARTIAL 처리."
---

# 거물 투자자 포지션 (Guru Positions)

> **쓰기 권한:** market-data-collector
> **읽기 권한:** briefing-lead, briefing-report-generator, 종목분석 9개 에이전트
> **갱신 빈도:** 분기 1회 (13F 공시 후)
> **명단 정본:** `reference/guru_watchlist.md` 참조
>
> **중요 고지:** 13F 포지션 데이터는 분기 종료 후 최대 45일 시차 존재.
> 현재 포지션이 아닌 "기준 분기 마감 시점 포지션"임을 반드시 인지.
>
> **2026-04-17 이브닝 상태:** 13F 직접 수집 불가 (Dataroma 접근 차단). MCP 웹검색으로 최근 공개 코멘트/방향성만 수집. PARTIAL.

---

## CURRENT — 최근 공개 코멘트 및 포지션 방향 (2026-04-17 기준)

> ⚠️ 아래는 13F 공식 데이터가 아닌 언론 보도/인터뷰 기반 방향성 정보입니다.
> 13F 기준: Q4 2025 (포지션일: 2025-12-31, 공시일: 2026-02-14 전후 추정)

### 거물 8인 — 최근 코멘트 및 방향성

| 투자자 | 소속 | 최근 방향성 | 핵심 코멘트/포지션 | 수집 신뢰도 | 출처 |
|--------|------|-----------|----------------|-----------|------|
| Warren Buffett | Berkshire Hathaway | 방어적 현금 축적 | 현금 $347B 유지. UnitedHealth 매수 (Burry·Tepper와 동일). 금 비선호 원칙 유지. | low | [InsiderMonkey, 2026-04] |
| Ray Dalio | Bridgewater | 탈달러·Gold 강세 | "달러 표시 부채 보유자·미국 상호 불신". 포트폴리오 Gold 비중 15% 추천. 2026 AI 버블+달러 약세 경고. | low | [WhalesBook, Bloomberg 2026-Q1] |
| Michael Burry | Scion Asset Mgmt | 방어적 | 중국 주식 비중 축소 (Tepper·Dalio 동일). UnitedHealth 매수 (Buffett·Tepper와 동일). | low | [InsiderMonkey, 2026-04] |
| Cathie Wood | ARK Invest | AI·테크 강세 | AI 낙관론 유지. 구체적 코멘트 미수집. | none | 미수집 |
| Stanley Druckenmiller | Duquesne Family Office | 매크로 복잡. AI 경고 | "AI 연계 주식 '불안할 정도로 과열'". Teva Pharma(제네릭→바이오시밀러, PER 6배) 관심. 커런시·상품 디스로케이션 탐색. | low | [AcquirersMultiple, 2026-03] |
| Howard Marks | Oaktree Capital | 고금리·크레딧 환경 경계 | 구체적 코멘트 미수집. | none | 미수집 |
| David Tepper | Appaloosa Mgmt | 방어적 + UNH | 중국 주식 비중 대폭 축소 (Dalio·Burry 동일). UnitedHealth 매수. | low | [InsiderMonkey, 2026-04] |
| Bill Ackman | Pershing Square | — | 구체적 코멘트 미수집. | none | 미수집 |

---

### 컨버전스 시그널 (2인 이상 동일 방향 — 언론 보도 기반)

| 종목/테마 | 동일 방향 투자자 | 방향 | 해석 | 신뢰도 |
|---------|---------------|------|------|-------|
| UnitedHealth (UNH) | Buffett + Burry + Tepper (3인) | 매수 | 헬스케어 방어주 공통 관심. 주가 부진 구간에서 매집. | low — 13F 기준 미확인 |
| 중국 주식 | Dalio + Burry + Tepper (3인) | 비중 축소 | 미중 디커플링 + 지정학 리스크 회피. | low |
| Gold/탈달러 | Dalio 주도. Buffett 현금 보유(간접) + Druckenmiller 달러 약세 편승 | 탈달러 구조 | DXY 98선 + Gold $4,800대. 브리핑-리드 "3인 컨버전스" 판단과 일치 | low |

**컨버전스 판정 규칙:**
- 2인 이상이 **동일 분기**에 동일 종목을 같은 방향(매수/매도)으로 움직인 경우만 포착
- 13F 시차 특성상 "이미 지난 신호"임을 반드시 명시
- 단순 보유 중복은 컨버전스 아님 — **변동(델타)** 일치만 유효

---

## 13F 공식 데이터 현황

| 분기 | 포지션 기준일 | 공시 마감 | 수집 상태 | 비고 |
|------|------------|---------|---------|------|
| Q4 2025 | 2025-12-31 | 2026-02-14 | FAILED | Dataroma 접근 불가 |
| Q1 2026 | 2026-03-31 | 2026-05-15 | 미도래 | 5월 중순 공시 예정 |

> ⚠️ Q1 2026 13F 공시 예정: 2026-05-15 전후. include_13f=true 플래그와 함께 `/시장데이터수집 13F` 재실행 필요.

---

## 업데이트 로그

| 날짜 | 에이전트 | 변경 내용 |
|------|---------|----------|
| 2026-04-07 | market-data-collector | 수집 시도 — 전 항목 네트워크 차단. 2회 재시도 후 N/A 처리. |
| 2026-04-17 | market-data-collector | 이브닝 재수집 — MCP 웹검색으로 최근 코멘트/방향성 부분 수집. 13F 직접 수집 불가. PARTIAL 처리. confidence:low. |
