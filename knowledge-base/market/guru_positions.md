---
updated: 2026-04-07
valid_until: 2026-07-07
file: guru_positions
sources: []
confidence: none
last_synced_from_db: 2026-04-07
collection_status: FAILED
failure_reason: "외부 네트워크 차단 환경 — Dataroma, Gurufocus, SEC EDGAR 모든 소스에 TCP 403 Forbidden. 2회 재시도 후 중단. 또한 include_13f 플래그가 명시적으로 true로 전달되지 않아 분기 정규 갱신 대상인지 미확인."
---

# 거물 투자자 포지션 (Guru Positions)

> **쓰기 권한:** market-data-collector
> **읽기 권한:** briefing-lead, briefing-report-generator, 종목분석 9개 에이전트
> **갱신 빈도:** 분기 1회 (13F 공시 후)
> **명단 정본:** `reference/guru_watchlist.md` 참조 — Cathie Wood 4번 위치, Seth Klarman 미포함
>
> WARNING: 이 파일의 CURRENT 섹션은 2026-04-07 수집 시도에서 모든 데이터 수집에 실패했습니다.
> 네트워크 차단 환경으로 Dataroma, Gurufocus, SEC EDGAR 접근 불가.
>
> 중요 고지: 13F 포지션 데이터는 분기 종료 후 최대 45일 시차가 존재합니다.
> 현재 포지션이 아닌 "기준 분기 마감 시점의 포지션"임을 반드시 인지해야 합니다.

## ★ CURRENT ★

### 기준: 미정 — 데이터 수집 실패 (포지션일: 미수집, 공시일: 미수집)

### 추적 대상 8인 — 최근 분기 포지션 변화

> 명단: Warren Buffett / Ray Dalio / Michael Burry / Cathie Wood / Stanley Druckenmiller / Howard Marks / David Tepper / Bill Ackman

| 투자자 | 소속 | 포트폴리오 규모 | 신규 매수 Top 3 | 비중 확대 Top 3 | 비중 축소 Top 3 | 완전 매도 Top 3 | 출처 |
|--------|------|---------------|---------------|---------------|---------------|---------------|------|
| Warren Buffett | Berkshire Hathaway | N/A [네트워크 차단] | N/A | N/A | N/A | N/A | Dataroma — 접근 불가 |
| Ray Dalio | Bridgewater | N/A [네트워크 차단] | N/A | N/A | N/A | N/A | Dataroma — 접근 불가 |
| Michael Burry | Scion Asset Mgmt | N/A [네트워크 차단] | N/A | N/A | N/A | N/A | Dataroma — 접근 불가 |
| Cathie Wood | ARK Invest | N/A [네트워크 차단] | N/A | N/A | N/A | N/A | Dataroma — 접근 불가 |
| Stanley Druckenmiller | Duquesne Family Office | N/A [네트워크 차단] | N/A | N/A | N/A | N/A | Dataroma — 접근 불가 |
| Howard Marks | Oaktree Capital | N/A [네트워크 차단] | N/A | N/A | N/A | N/A | Dataroma — 접근 불가 |
| David Tepper | Appaloosa Mgmt | N/A [네트워크 차단] | N/A | N/A | N/A | N/A | Dataroma — 접근 불가 |
| Bill Ackman | Pershing Square | N/A [네트워크 차단] | N/A | N/A | N/A | N/A | Dataroma — 접근 불가 |

### 컨버전스 시그널 (2인 이상 동일 방향)

| 종목/ETF | 동일 방향 투자자 | 방향 | 해석 | 출처 |
|---------|---------------|------|------|------|
| N/A [네트워크 차단 — 미수집] | N/A | N/A | N/A | Dataroma — 접근 불가 |

**컨버전스 판정 규칙:**
- 2인 이상이 **동일 분기**에 동일 종목을 같은 방향(매수/매도)으로 움직인 경우만 포착
- 13F 시차 특성상 "이미 지난 신호"임을 반드시 명시
- 단순 보유 중복은 컨버전스 아님 — **변동(델타)** 일치만 유효

---

## 업데이트 로그

| 날짜 | 에이전트 | 변경 내용 |
|------|---------|----------|
| 2026-04-07 | market-data-collector | 수집 시도 — Dataroma/Gurufocus/SEC EDGAR 모두 네트워크 차단(TCP 403 Forbidden)으로 미수집. 2회 재시도 후 N/A 처리. include_13f 플래그 미수신. |
