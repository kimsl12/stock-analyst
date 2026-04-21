---
updated: 2026-04-21
version: v3.2
maintainer: wiki-linter (자동) + briefing-lead (수동)
lint_last_run: 2026-04-21
lint_mode: full
---

# Knowledge Base Index — Wiki Master Index

> **목적:** 에이전트가 이 파일 하나만 읽으면 전체 KB 구조, 핵심 인사이트, 건강 상태를 파악할 수 있어야 한다.
> **갱신 주체:** wiki-linter (자동 갱신, 주 1회) + briefing-lead (브리핑 종료 시 인사이트 append)
> **활용법:** 에이전트는 질의 전 이 파일을 먼저 읽고, 필요한 파일만 드릴다운한다. Glob 탐색 금지.

---

## P0 — 즉시 조치 필요 (FAILED / 만료)

> wiki-linter가 탐지한 긴급 항목. 브리핑 실행 전 반드시 확인.
> **최종 갱신: 2026-04-21 (market-data-collector)**

| 파일 | 상태 | 영향 모듈 | 조치 |
|------|------|----------|------|
| `portfolio/model_portfolios.md` | [P0] confidence:low — 전 항목 *(미수집)* N/A. 빈 테이블 | F-2~F-5 | `/모델포트폴리오` 실행 필요 |

> [P0 실질 긴급] portfolio/model_portfolios.md: confidence:low + 전 항목 미수집 상태 지속 (2026-04-07 이후 미갱신 12일). `/모델포트폴리오` 실행 필요.
> [INFO] 나머지 Market/Macro/Industry KB 전체 P1 이하 — 실행 가능 상태.

---

## P1 — 이번 주 조치 (탐지: 2026-04-21 full)

> wiki-linter P1 탐지 결과. 브리핑 실행 가능하나 이번 주 내 처리 권장.

| 파일 | 문제 | 심각도 | 권장 조치 |
|------|------|-------|---------|
| `industry/bio_pharma.md` | 파일 미존재 — industry/ 폴더에 없음. _index.md 테이블에는 등재. | HIGH | industry/bio_pharma.md 신규 생성 또는 index 등재 제거 |
| `semiconductor.md` (루트) | industry/semiconductor.md 미존재 — 루트 파일만 있음. index는 둘 다 언급. | MEDIUM | 루트→industry/ 이동 또는 industry/ 신규 생성 결정 필요 |
| `geopolitics.md` (루트) | valid_until 05-07 (갱신일 04-07) — redirect 파일이나 구 데이터 잔존 | LOW | macro/geopolitics.md(04-19) 사용 확인. 루트 파일 redirect 표시 갱신 |
| `global_risk_factors.md` (루트) | valid_until 05-07 (갱신일 04-07) — redirect 파일이나 구 데이터 잔존 | LOW | macro/global_risk_factors.md(04-19) 사용 확인 |
| `market/daily_snapshot.md` | valid_until 04-23 — 04-21 갱신 완료 (D-2) | LOW | 04-23 재실행 |
| `industry/ai.md` | valid_until 05-07 (갱신일 04-07) — 12일 미갱신. Anthropic 상황 변화 반영 필요 | MEDIUM | 다음 kb-updater 사이클에 갱신 요청 |
| `industry/auto.md` | valid_until 05-07 (갱신일 04-07) — 12일 미갱신. 관세 25% 영향 업데이트 필요 | MEDIUM | 다음 kb-updater 사이클에 갱신 요청 |
| `semiconductor.md` (루트) | valid_until 05-07 (갱신일 04-07) — 12일 미갱신 | MEDIUM | 다음 kb-updater 사이클에 갱신 요청 |

> [P1 고아파일] industry/bio_pharma.md — 파일 없음 확인. index에 등재된 내용(GLP-1 시장 700~800억달러, 삼성바이오 4공장)만 존재.
> [P1 구조] 루트 파일 중 redirect 파일(geopolitics.md, global_risk_factors.md, us_monetary_policy.md)은 구 데이터 잔존 상태이나 브리핑에는 macro/ SSOT 사용.
> [P1 정상] industry/ 전체 고아 파일 없음 (17개 파일 모두 _index.md 등재 확인). defense_industry.md(04-21) + crypto_bitcoin.md(04-20) + robotics.md(04-19) 신규 포함.
> [P1 정상] knowledge-db/ SSOT-only 파일 추가 확인 없음.

---

## ⚡ 최근 핵심 인사이트 (지난 7일 — briefing-lead append)

| 날짜 | 출처 | 인사이트 | 관련 KB | 제안 상태 |
|------|------|---------|--------|---------|
| 2026-04-13 | 이브닝브리핑 | 호르무즈 봉쇄 선언 — WTI $105 급등, 4/14 아시아 갭다운 -2~4% 경고. 위험등급 4→5 상향 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-13 | 이브닝브리핑 | Gold-DXY 역상관 약화 Z+1.8σ — Gold $4,724 구조적 Bull. 중앙은행 매수+재정적자=탈달러 수요 | `macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-13 | 이브닝브리핑 | WTI-인플레기대 동조화 Z+2.3σ — Core CPI 전이 2~3개월 시차. Fed 6월 인하 소멸 가능 | `macro/us_monetary_policy.md` | 진행중 |
| 2026-04-09 | ai_anthropic.md 신규 | Anthropic ARR $30B — OpenAI 최초 추월. 엔터프라이즈 LLM 점유율 40% | `industry/ai_anthropic.md` | — |
| 2026-04-07 | 모닝브리핑 | Gold Bull 중기 — 기축통화 균열 프리미엄, 중앙은행 매수 급증 | `macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-07 | 모닝브리핑 | SK하이닉스 Bull — HBM3E 대중 전면금지 → Tier1 한국 무제한 수혜 | `semiconductor.md §1 HBM` | 진행중 |
| 2026-04-07 | 모닝브리핑 | 한국 방산 Bull 장기 — 유럽 GDP 3% 방위비 + 우크라이나 재건 | `macro/geopolitics.md §5` | 진행중 |
| 2026-04-07 | 모닝브리핑 | 미국 장기국채(TLT) Bear — 관세 인플레 2차 효과 + 재정적자 | `macro/us_economy.md §8` | 진행중 |
| 2026-04-07 | 모닝브리핑 | CPI 베이스 시나리오 — 관세 전가율 50~70%, Core +0.5~1.5%p 상방 | `macro/us_monetary_policy.md` | 진행중 |
| 2026-04-13 | 주간리포트 | 위험등급 4->5 상향 — 호르무즈 봉쇄+CPI 3.3%+관세 삼중 인플레. 베이스 시나리오 WTI $100~115, S&P -3~5% | `market/daily_snapshot.md` | 진행중 |
| 2026-04-13 | 주간리포트 | KOSPI "코리아 프리미엄" 반전 리스크 — 원/달러 1,500+ 시 외국인 이탈+경상수지 적자 전환 가능 | `macro/korea_economy.md` | 진행중 |
| 2026-04-13 | 주간리포트 | 적중률 잠정 50%(3건 중 1.5건) — Gold Bull 적중, CPI 부분 적중, 시나리오 수정. 테일 리스크 가중치 상향 필요 | `performance/2026_recommendations.md` | -- |
| 2026-04-14 | 모닝브리핑 | VIX 19.12 "거짓 안정" — 소비심리 47.6(역대최저) vs VIX 괴리. 4~6주 내 25~30 재상승 경고 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-14 | 모닝브리핑 | DXY 98.34 구조적 약세 3년래 최저 — 재정적자+탈달러+Gold $4,781. 달러 표시 자산 실질가치 하락 | `macro/global_risk_factors.md` | 진행중 |
| 2026-04-14 | 모닝브리핑 | 호르무즈 봉쇄 Day 1 제한적 적용 — CENTCOM 비이란 통항 보장. 시장 "봉쇄 내성" 확인하나 2차효과 과소평가 | `macro/supply_chain.md` | 진행중 |
| 2026-04-14 | 내포트폴리오 | 미국주식 87.8% 극편중 진단 — 중립형 프로파일 vs 초공격형 실제. 채권1.1%/금0% 방어력 전무. 6개월 재조정 플랜 제시 | `portfolio/user_portfolio.md` | 진행중 |
| 2026-04-14 | 리밸런싱 | 달러현금 $705 즉시 활용(AGG $400+GLD $300) + 월적립 방향 전환. 6개월 목표: 미국72%/채권8%/금5%/크립토9% | `portfolio/rebalancing_history.md` | 진행중 |
| 2026-04-14 | 글로벌인텔리전스 | 4축 메가트렌드 "호르무즈-AI-탈달러 수렴" -- 지정학이 단기 3개월 압도적 동인. 호르무즈 해소 시점이 4축 전체 스위치포인트 | `macro/supply_chain.md, macro/geopolitics.md` | 진행중 |
| 2026-04-14 | 글로벌인텔리전스 | 숨은 테마 "비료-식량 인플레 2차 파동" -- 요소비료 +172% YoY, 한국 호르무즈 경유 38.4%. 6~7월 식품CPI +0.3~0.5%p. 시장 반영 10~20% | `macro/supply_chain.md` | 진행중 |
| 2026-04-14 | 글로벌인텔리전스 | TSMC N2 2nm GAA Q3 매출 N3/N5 추월 전망 -- Q1 $35.7B 사상최고. AI 초크포인트 집중도 심화. 대만 리스크 구조적 상존 | `macro/tech_breakthrough.md` | 진행중 |
| 2026-04-14 | 이브닝브리핑 | KOSPI 장중 6,000 돌파(6,026) 후 5,968 마감(+2.74%) -- 재협상 기대. 6,000 안착에는 호르무즈 해소 또는 Q2 반도체 실적 확인 필요 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-14 | 이브닝브리핑 | IEA/WB/IMF "봉쇄 해소해도 빠른 정상화 불가" 공동경고 -- War Risk Premium 구조화+IRGC 기뢰 21건+비료 복구 시차. 시장 과소평가 | `macro/supply_chain.md` | 진행중 |
| 2026-04-14 | 이브닝브리핑 | 정유 섹터 정제마진 $18(역대급) -- WTI $97+재고평가이익. S-Oil/SK이노 Q1 서프라이즈 가능하나 봉쇄 해소 시 반락 리스크 | `industry/energy.md` | 진행중 |
| 2026-04-15 | 이브닝브리핑 | Gold $4,869 신고가 (+2.67%) — WTI 급락에도 단절적 강세. "탈달러 구조적 수요"가 Gold로 쏠리며 BTC를 우회. Gold-DXY/Oil 상관관계 붕괴 | `macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-15 | 이브닝브리핑 | WTI -8.47% 급락 + KOSPI 6,141 안착 = 호르무즈 완화 시나리오 1단계 진입. 그러나 Gold 독립 강세는 "완화 랠리 소멸 후 남는 구조적 리스크"를 경고 | `macro/supply_chain.md §1-2` | 진행중 |
| 2026-04-15 | 이브닝브리핑 | VIX 18.36 vs 소비심리 47.6 괴리 극대화 — 재상승 예상 시점 4~6주에서 **2~4주로 단축**. NASDAQ-BTC 동조화 약화(BTC +0.23%)도 위험선호 편중 주의 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-16 | 모닝브리핑 | S&P 7,022·NASDAQ 24,016 동시 신고가 — 그러나 Dow -0.15% 홀로 약세 + 10Y 4.28% 반등 + VIX-MOVE 괴리 = **breadth 쇠퇴 4중 시그널**. 2000Q1·2007Q3·2021Q4 유사 "후반 사이클 정점" 패턴 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-16 | 모닝브리핑 | Gold $4,844 신고가 근접 유지 (3일 연속) — DXY 98.01 3년최저 갱신 + 리스크온 랠리에도 환매되지 않는 탈달러 수요. Dalio/Buffett현금/Druckenmiller 3인 "Gold/탈달러 컨버전스" 강화 | `macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-16 | 모닝브리핑 | 10Y 4.28% 반등 + S&P 신고가 동시 발생 = 리스크-프리미엄 수수께끼 재점화. 5/13 Core CPI + 4/20주 Q1 실적 **더블 체크포인트** 3~4주 시한. Core 인플레는 여전 | `macro/us_economy.md §3` | 진행중 |
| 2026-04-16 | 이브닝브리핑 | VIX 경고 승격 🟡→🔴 — VIX 18.17 vs 미시간 소비심리 47.6 역대급 괴리 + Dow 단독 약세 이브닝까지 지속 = 2018.02 VIXpocalypse 유사 구도. 예상 시점 2~4주→**2~3주 추가 단축**. 숏볼 극단 집중으로 서프라이즈 1건에 VIX 25~30 점프 갭 반등 리스크 | `market/correlation_matrix.md` + `global_risk_factors.md §2` | 진행중 |
| 2026-04-16 | 이브닝브리핑 | 트리플 체크포인트 2~3주 집중 — JPM/BAC Q1(4/20) + 파키스탄 휴전 만료(4/21) + 4월 CPI(5/13). 시나리오 B(조정) 확률 모닝 40%→이브닝 **45%로 추가 상향**. 1건 실패 -3~7% 조정, 2건 실패 -10~15% 민감 | `macro/us_economy.md §3, macro/geopolitics.md §2-1` | 진행중 |
| 2026-04-16 | 이브닝브리핑 | Gold-DXY 역상관 **구조화 완성** (3일 연속) — Dalio + Buffett 현금 $347B + Druckenmiller 추정 "탈달러 3인 컨버전스 4일 연속 강화". Gold $4,844 + DXY 98.01 유지. BTC는 정체 2일째로 "탈달러 수요 Gold로만 쏠림" 재확인 | `macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-17 | 모닝브리핑 | Dow +0.24% 반등 — 어제 "단독 약세 4중 시그널" 1건 **1일 만에 리버스**. 3대 지수 동시 신고가. 그러나 VIX 17.94(18선 붕괴, 4단계 극단) + 10Y 4.31%(4일 연속 반등) + Gold $4,813(첫 조정) + USD/KRW 1,481(재진입) **4건 대체 부상** — 경계 근거가 이동했을 뿐 총량은 증가 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-17 | 모닝브리핑 | 10Y 4.31% 4거래일 연속 반등 추세 확정 — 4.35% 돌파선 임박. "WTI 급락 디스인플레" 노이즈 해석 불가, **채권 시장의 구조적 메시지**. 5/13 CPI 단일 최대 이벤트. TLT 추가 하방 가속 | `macro/us_economy.md §3·§4` | 진행중 |
| 2026-04-17 | 모닝브리핑 | Gold $4,813 4일 Bull 후 첫 조정 — **48시간 구조 vs 노이즈 판별**. $4,800 지지 유지 시 $4,850→$5,000 유효. $4,780 이탈 시 단기 모멘텀 약화. DXY 98.21 되돌림 2주 지속 시 재평가 | `macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-17 | 이브닝브리핑 | 이란 "재협상 의지" 공식 표명 → WTI $104→$93.74 3일 -10% 급락. 호르무즈 통항 3척/일 미해제. **4/21 휴전 만료 D-4 단일 최대 분기점**. 시나리오 A/B 35%/35% 균등화 | `macro/geopolitics.md §2-1, macro/supply_chain.md` | 진행중 |
| 2026-04-17 | 이브닝브리핑 | 트럼프 파월 해임 위협 **신규 부상** — 05/15 임기 만료 후 이사직 해임 경고. DXY 98.19 + 10Y 4.31% 교차 "달러 신뢰 균열 + 구조적 인플레" 메시지 강화. Fed 독립성 리스크 | `macro/us_economy.md §3, macro/global_risk_factors.md` | 진행중 |
| 2026-04-17 | 이브닝브리핑 | BTC $75K **+5.9% 급등** + Gold ~$4,800 첫 조정 동시 발생 — "탈달러 자산 내 순환(Gold→BTC)" 가설. $75K 1일+ 유지 시 독립 강세 확정. 3일 탈동조화 박스 탈출 | `market/daily_snapshot.md, market/correlation_matrix.md` | 진행중 |
| 2026-04-17 | 이브닝브리핑 | VIX 17.94 **18선 붕괴 = 거짓 안정 4단계 극단** (4일 연속). S&P↔10Y 동반 상승 Z+1.8~2.2σ 🔴. 경계 근거 "이동했을 뿐 총량은 증가" — Dow 약세 1건 해소 vs 대체 경고 4건 부상 | `market/correlation_matrix.md, macro/global_risk_factors.md §2` | 진행중 |
| 2026-04-18 | 모닝브리핑 | 호르무즈 해협 **"완전 개방"** + 이스라엘-레바논 10일 휴전 — WTI $104→$84(-19% 4일). S&P 7,126 신고가. NASDAQ 13일 연승(1992년 이후 최장). **'전쟁 디스카운트' 완전 소멸**. 단, 이란 항구 봉쇄 유지+핵 미합의+10일 한시 = 꼬리 리스크 제거이나 기저 리스크 잔존 | `market/daily_snapshot.md, macro/geopolitics.md §2-1` | 진행중 |
| 2026-04-18 | 모닝브리핑 | Gold $4,849 **48시간 판별 결과: 구조적 Bull 재확정**. 첫 조정($4,813) 후 +1.34% 즉시 반등. DXY 98.23 호르무즈 해소에도 반등 없음 = 탈달러 구조적 약세 확인. BTC $77K 2일 연속 상회 = 크립토 독립 강세 구간 확정 | `market/daily_snapshot.md, macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-18 | 모닝브리핑 | VIX 17.48 **"거짓 안정 5단계"** 극단화. 소비심리 47.6 대비 **괴리 30pt(역대급)**. 호르무즈 해소로 "모든 리스크 소멸" 착각이 가격에 반영 중. 4/23 TSLA + 4/28 FOMC + 5/15 파월 만료 = 새로운 체크포인트 부상 | `market/correlation_matrix.md, macro/global_risk_factors.md §2` | 진행중 |
| 2026-04-18 | 주간리포트 | **NASDAQ 13일 연승 vs VIX 거짓 안정 5단계** — 시나리오 A "실적 랠리" 50%(상향). S&P 7,126 신고가이나 소비심리 47.6 괴리 역대급. 4/23 TSLA + 4/28 FOMC가 "진짜 시험". 조건부 환호 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-18 | 주간리포트 | **DXY 98.23 구조적 약세 확정** — 호르무즈 해소에도 달러 반등 없음. 재정적자+파월 해임 위협+중앙은행 Gold 매수=탈달러 불가역. Gold $4,878 S등급·BTC $77K 독립 강세. contrarian-card 핵심 | `macro/global_risk_factors.md §4, market/daily_snapshot.md` | 진행중 |
| 2026-04-18 | 주간리포트 | 잠정 적중률 **83%**(5/6, 표본 부족). Gold Bull·SK하이닉스·방산 순항. KOSPI 갭다운 오류(지정학 시장 내성 과소평가). 테일 리스크 시점 보수화 교훈 | `performance/2026_recommendations.md` | -- |
| 2026-04-19 | 모닝브리핑 | Gold $4,878 **구조적 Bull 확정** — 48시간 판별 통과. 호르무즈 해소에도 반등 없는 DXY 98.21 = "달러 신뢰 균열". Dalio/Druckenmiller/Buffett 3인 탈달러 컨버전스. JPM $5,055(4Q26E) | `market/correlation_matrix.md, macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-19 | 모닝브리핑 | **4/21 호르무즈 휴전 만료 = 30일 매크로 단일 최대 분기점.** 선언적 개방 vs 물리적 미완(기뢰 21건). 연장 시 WTI $80 안착+Fed 인하 경로 복원, 결렬 시 $100+ 재급등+스태그플레이션 부활 | `macro/supply_chain.md, macro/geopolitics.md` | 진행중 |
| 2026-04-19 | 모닝브리핑 | VIX 17.48 "거짓 안정 5단계" 5일 연속 극단 — 소비심리 47.6 괴리 30pt 역대급. 4/22 TSLA + 4/25 GDP + 4/28 FOMC 3중 트리거. 숏볼 극단 누적, 서프라이즈 1건에 VIX 25~30 갭 반등 리스크 | `market/correlation_matrix.md` | 진행중 |
| 2026-04-19 | 모닝브리핑 | 시나리오: A(낙관) 40% / B(조정) 40% / C(위기) 20%. 전주 A 50%에서 하향 — 4중 분기점(호르무즈/TSLA/GDP/FOMC) 집중으로 불확실성 재상승 | `analysis/briefing/global_macro_20260419.md` | 진행중 |
| 2026-04-18 | 이브닝브리핑 | Gold $4,878 **신고가 + DXY 보합 = Gold-DXY 역상관 구조 이탈 확정(Z+2.0~2.5σ 이상 승격)**. BTC $77,319 동시 상승 = "탈달러 쌍끌이 구조화" 신규 시그널. 아시아 전반 차익실현(KOSPI -0.55%, Nikkei -1.75%) | `market/daily_snapshot.md, market/correlation_matrix.md` | 진행중 |
| 2026-04-18 | 이브닝브리핑 | 리스크 **"총량 감소, 성격 전환"** — G-1 지정학(호르무즈) → G-2 정치축(파월 해임 5/15) 최대 동인 전환. 매크로 위험등급 4→3 하향. VIX 거짓 안정 5단계 5일 연속(Z+2.3~2.9σ 🔴). 시나리오 A 50→45%, B 35→40% | `macro/us_monetary_policy.md, market/correlation_matrix.md` | 진행중 |
| 2026-04-18 | 이브닝브리핑 | **4/23 TSLA 실적 = 단일 최대 체크포인트**. NASDAQ 13일 연승 마감 + VIX 압축 해제 트리거. 4/23 TSLA → 4/28 FOMC → 5/13 CPI → 5/15 파월만료 4중 체크포인트 3~4주 집중 | `market/daily_snapshot.md, market/economic_calendar.md` | 진행중 |
| 2026-04-19 | 이브닝브리핑 | 호르무즈 **24시간 번복(4/17 개방->4/18 재봉쇄)** -- 시장 S&P 7,126 신고가로 재봉쇄 미반영(주말 휴장). 4/21 개장 시 WTI +/-$10 양방향 변동. "개방 할인 조기 반영 -> 되돌림 비대칭" 핵심 리스크 | `macro/geopolitics.md §2-1, macro/supply_chain.md` | 진행중 |
| 2026-04-19 | 이브닝브리핑 | 시나리오 A 40->**38%**(하향) / B 40->**42%**(상향) / C 20% -- 호르무즈 번복으로 B 우세 전환. TSLA 4/22 Miss 시 B->50%+ 가속 | `analysis/briefing/lead_evening_20260419.md` | 진행중 |
| 2026-04-19 | 이브닝브리핑 | Druckenmiller **RSP(이퀄웨이트) $238M 신규** = Mag7 집중도 리스크 인지한 "breadth 확대" 포지셔닝. NASDAQ 13일 연승이 Mag7 주도라면, 거물은 이미 "다음 국면" 준비 | `market/guru_positions.md` | 진행중 |
| 2026-04-20 | 모닝브리핑 | 호르무즈 재봉쇄 "배가" + 미 해군 이란 선박 나포(투스카) + 이란 2차 협상 공식 거부 — **금요일 "개방 할인" 서사 72시간 내 완전 번복.** ES1 선물 7,103(-0.32%). 4/22 휴전 만료 D-2 = 30일 매크로 최대 분기점 지속 | `macro/geopolitics.md §2-1, macro/supply_chain.md` | 진행중 |
| 2026-04-20 | 모닝브리핑 | 시나리오 B(조정) **44% 우세 확립** (A 36% / B 44% / C 20%). 이란 "doubles down" + 나포 에스컬레이션 + 트리플 체크포인트(4/21~25) 집중 주간. 호르무즈 결렬 시 WTI $100+ + S&P -3~5% | `analysis/briefing/global_macro_20260420.md` | 진행중 |
| 2026-04-20 | 모닝브리핑 | 4/22 = **호르무즈 휴전 만료 + TSLA Q1 실적 동일 날 = 이중 트리거.** Miss + 결렬 동시 시 NASDAQ -5~8% + VIX 25~30 갭 반등. VIX 17.48 "거짓 안정 5단계" 주초 해소 시작 가능 | `market/daily_snapshot.md, market/economic_calendar.md` | 진행중 |
| 2026-04-20 | 모닝브리핑 | Gold $4,878 구조적 Bull + **호르무즈 재봉쇄 = 추가 상방 촉매.** Warsh 인사청문회(4/21) 인준 불확실 → Fed 리더십 공백 리스크 → DXY 추가 하방 → Gold $5,000 경로 강화 | `macro/global_risk_factors.md §4, market/guru_positions.md` | 진행중 |
| 2026-04-21 | 모닝브리핑 | 트럼프 "수요일 휴전 종료, 연장 극히 비개연"+이란 "재협상 없음" = **결렬 기본시나리오화.** WTI +5% 선물 급등 vs ES1 -0.3% 과소반응. "개방 할인 되돌림 비대칭 하방" 경고 | `macro/geopolitics.md §2-1, market/daily_snapshot.md` | 진행중 |
| 2026-04-21 | 모닝브리핑 | KOSPI 6,355 사상최고 — 반도체+WGBI 수급이 지정학 압도. 그러나 4/22 TSLA+휴전 만료 이중 트리거가 진짜 방향 설정. VIX 17.48 "거짓 안정 5단계" 해소 임박 | `market/daily_snapshot.md, market/economic_calendar.md` | 진행중 |
| 2026-04-21 | 모닝브리핑 | 소매판매 3월 +0.4% MoM (6개월 연속 증가) — 소비심리 47.6 vs 실지출 "사상 최대 괴리" 3개월째. 스태그 내러티브 1개월 추가 유예. 5월 세금환급 소멸이 진짜 전환점 | `macro/us_economy.md §1, market/economic_calendar.md` | 진행중 |
| 2026-04-21 | 이브닝브리핑 | VIX 17.48->**18.98(+8.58%) "거짓 안정 해제 1단계"** 공식 시작. NASDAQ 13일 연승 종료. 트럼프 "연장 unlikely"+이란 나포 에스컬레이션. 시나리오 B(조정) 47% 우세 심화 | `market/correlation_matrix.md, macro/geopolitics.md` | 진행중 |
| 2026-04-21 | 이브닝브리핑 | AAPL 팀 쿡->**존 터너스 CEO 교체**(9/1). 하드웨어 출신 = Vision Pro/Apple Silicon 가속. Buffett AAPL -4.3% 축소 이미 반영. $4T 기업 리더십 전환 | `market/guru_positions.md` | 진행중 |
| 2026-04-21 | 이브닝브리핑 | 소매판매 +0.4% Beat이나 **"시간차 함정"** -- 세금환급+관세 사전구매 일시효과. 소비심리 47.6이 Q2 소매판매 역전 선행. 행동(OK) vs 심리(붕괴) 디커플링 | `macro/us_economy.md, market/surprise_index.md` | 진행중 |

---

## 🏭 Industry KB (`knowledge-base/industry/`)

| 파일 | 핵심 수치 | 최신 인사이트 | 갱신일 | 유효기간 | 신뢰도 |
|------|---------|------------|-------|---------|-------|
| `semiconductor.md` | 삼성 2026E OP 45~65조, SK 23~30조, HBM4 H2 양산 | 관세 간접 타격 -5~10% 우려 추가. 삼성 파운드리 3nm 수율 60% 미만 지속 | 04-07 | 05-07 | medium |
| `ai.md` | 글로벌 AI 시장 3,300~3,800억달러, CapEx 합산 2,950~3,200억 | DeepSeek 쇼크 후 CapEx 오히려 상향. 추론(Inference) 60%+ 비중 전환 | 04-07 | 05-07 | medium |
| `ai_anthropic.md` | ARR $300억, 밸류 $3,800억, IPO 2026 Q4 목표 | OpenAI ARR 최초 추월. 엔터프라이즈 40% 점유. Pentagon 갈등 리스크 | 04-09 | 05-09 | high |
| `auto.md` | HMG 750만대(글로벌 3위), 미국 관세 25% 발효 | 조지아 30만대로 부분 완충. 관세로 연간 이익 1.5~2.5조 감소 우려 | 04-07 | 05-07 | medium |
| `energy.md` | WTI $84~94, Brent $90~96, JKM $16~19.2, 정제마진 $20 | 호르무즈 24시간 번복(4/17개방->4/18재봉쇄). 유가 극심 변동성. 정유4사 비축 4월말 한계. 석화 가동률 50~60%(5월 중순 셧다운 위기). OPEC+ 5월 206K 추가 증산. SPR 7,648만bbl(116일분). 원전 14GW(30년 최대) | 04-19 | 05-19 | high |
| `science_tech.md` | 한국 R&D/GDP **5.1%**(세계 1위), 글로벌 R&D 3.8조달러, 정부 R&D **35.3조**(+21.4%) | IonQ 포토닉 인터커넥트(양자네트워킹). 경구 Wegovy FDA승인. 빅테크 CapEx $7000억. PANW-CyberArk $250억. EDA AI에이전트전쟁. Optimus Gen3 자율보행. WIPO PCT 반도체+6.1% | 04-19 | 05-19 | high |
| `bio_pharma.md` | GLP-1 시장 700~800억달러 | 삼성바이오 4공장 풀가동, CDMO Top 4 | 04-07 | 05-07 | medium |
| `quantum.md` | IonQ FY2026 $225-245M, 양자센서 $984M, 양자주 3일 랠리 | NVIDIA Ising QEC AI 모델. IonQ $35-40(RPO $370M). D-Wave $24.6M(+179%). Meta PQC 전환. 양자센서 TRL7-8 | 04-19 | 05-19 | high |
| `space.md` | 우주경제 $468-626B, Starlink 10K기/1000만, RKLB $602M, 우주군 $26.3B+$13.8B | SpaceX F9 46회(4/15)+Starship V3 5월. Blue Origin NG-3 부스터 재사용. Amazon Kuiper 베타(4/8, 1500기). AST BlueBird 7 4/19 $1B계약. RKLB Neutron Q4. 한국 차세대발사체 5.6조. confidence medium->high 승격 | 04-19 | 05-19 | high |
| `smr.md` | TerraPower NRC 건설허가(03/04), Kairos Hermes 2 착공(04/17), CFS SPARC first plasma 2026, 두산 수주 14.3조, 빅테크 원자력 DC MS 2GW/Google 500MW/Amazon 5GW/Meta 6.6GW | TerraPower 비경수로 최초 NRC 건설허가. Kairos Gen IV 최초 착공. RR-SMR UK 정식 계약(04/13). Helion 1.5억도. 체코 26조. confidence medium->high 승격 | 04-19 | 05-19 | high |
| `telecom_next.md` | Starlink 1000만+/DTC 650기/T-Mobile DTC 300만+, Gartner 보안 $240B, PANW FY2026 $11.3B, CRWD ARR $5.25B | 3GPP Rel-20 Stage-2 2026.06/Rel-21 6G 2027.03. 5G Advanced 상용화. Starlink DTC 22국. AST BlueBird6 3배크기. Amazon Leo Globalstar $1.57B 인수. Gartner AI보안 2029 $160B. 인력부족 480만. confidence medium->high 승격 | 04-19 | 05-19 | high |
| `banking_capital.md` | 4대 금융지주 합산 순이익 18.4조(+11.4%) | KB·신한·하나·우리 사상 최대 실적. PE/VC 환경 개선 기대 | 04-13 | 05-13 | medium |
| `advanced_materials.md` | MicroLED 2026E 0.56~6.37B, Synopsys FY2026 $9.56~9.66B, GaN 4.83B, CoWoS 4배 증설 | Wolfspeed 파산. Synopsys Ansys 통합 +66%. Cadence ChipStack AI. STMicro SiC 200mm 수율75%. 페로브스카이트 탠덤 34.85% | 04-19 | 05-19 | medium |
| `battery.md` | 리튬 가격 동북아 $18,050/ton (Q1 2026) | 리튬 급등 후 조정. LFP 점유 확대 vs NCM 고성능 분화 | 04-13 | 05-13 | medium |
| `infrastructure.md` | 글로벌 건설 17.26조달러(+4.9%), 한국 수주 231.2조 | 현대건설·삼성물산 SMR EPC 추진. 데이터센터 전력망 수혜 | 04-13 | 05-13 | medium |
| `capex.md` | 하이퍼스케일러 5사 합산 $660-690B(2026E), 반도체 $200B, 에너지 $3.3T, 국방 $2.63T | 빅테크 AI CapEx 슈퍼사이클. TSMC $52-56B(+27-40%). 한국 장비투자 $29.7B 세계2위. 통신 -2% 정체. 배터리 한국3사 가동률 50% | 04-19 | 05-19 | high |
| `robotics.md` | 휴머노이드 2030E $4~39B 편차. Figure $39B밸류·BotQ 12K→50K대/년. Tesla Optimus Gen3 H2 양산+Shanghai 1M/년. Agility Digit 상업수익(GXO 100K totes). Harmonic Drive 85%. Jetson Thor 2,070 FP4 TFLOPS | 삼성(레인보우 35%)·현대(BD 80% $880M)·LG(Atlas비전+Axium)·두산로보·클로봇 생태계. EU AI Act 고위험 2026.08 발효. 클로봇 Q3 매출 +38.9%/레인보우 +117.6% | 04-19 | 05-20 | high |
| `crypto_bitcoin.md` | BTC $74,800~75,574, 시총 $1.51~1.54T, ATH $126,210(2025-10, -39%), Q1 -23.8%, 해시레이트 1.084 ZH/s, MSTR 780,897 BTC(3.9% 공급)·평균$75,577·전환사채$8.2B, IBIT AUM $70.6B, 스팟 BTC ETF Q1 유입 $18.7B, 스테이블코인 $320B+ | MSTR STRK $21B/STRF $2.1B/STRD 우선주 구조. Bitcoin Yield KPI = BTC-per-share. 채굴사 Q1 32K BTC 매도(BEP 이하). SEC Atkins Project Crypto·GENIUS Act(2025.07). EU MiCA 2026-07-01 전면집행. 한국 디지털자산기본법 4/8 진전 | 04-20 | 05-20 | high |
| `defense_industry.md` | **NDAA FY2026 $901B**(상원통과), 미 primes 백로그 합산 $1조+(LMT $194B/RTX $268B/NOC $95.7B/GD $118B/BA $545B+), K-방산 수출 2025 $15.4B→2026 $20B목표, 한국 방위력개선비 19.97조(+11.9%) | 한화에어로 Redback **XM30 Phase 2 탈락 확정**(Rheinmetall vs GDLS 2파이널 9월 결정). 현대로템 폴란드 K2 2차 9조+선수금 3조 조기수령. LIG넥스원 수주잔고 23.5조(중동 천궁-II 10.6조). KAI 2026 가이던스 매출 5.73조(+58%)·수주 10.44조(+63%) KF-21 인니 16대 MoU. Rheinmetall Lynx KF-41 €10B 확장. BAE Eurofighter GCAP까지 가득참. Dassault Rafale €46.6B 백로그 | 04-21 | 05-21 | high |

> 상세 드릴다운: 각 파일의 § 섹션 번호 참조. 에이전트는 이 표로 파일 선택 후 해당 파일만 Read.
> [v3.5 신규 등재 — 04-13 wiki-linter]: quantum, space, smr, telecom_next, banking_capital, advanced_materials, battery, infrastructure

---

## 🌍 Macro KB (`knowledge-base/macro/`)

| 파일 | 핵심 수치 | 핵심 리스크 | 갱신일 | 신뢰도 |
|------|---------|-----------|-------|-------|
| `us_economy.md` | **CPI 3.3%(에너지 주도), Core CPI 2.6%, ISM제조가격 78.3+서비스가격 70.7(양채널 극단), GDPNow Q1 +1.3%, Fed 3.50~3.75%, 10Y 4.26%, DXY 97.70, S&P 7,022(신고가), VIX 17.94, 침체확률 30~49%** | 3중 인플레 파이프라인(에너지+제조+서비스). 소비심리 47.6(역대최저) vs VIX 17.94 괴리. 트럼프 파월 해임 위협(4/15). 6월 인하 소멸(89.2%). Fed 리더십 전환 리스크(5/15) | 04-18 | ✅ high |
| `us_monetary_policy.md` | **Fed 3.50~3.75%(2연속 동결), CPI 3.3%(에너지 주도), Core CPI 2.6%, Core PCE 3.0%, QT 종료, 대차대조표 $6.7T, 10Y 4.31%, DXY 97.70, 침체확률 30~35%** | 트럼프 파월 05/15 해임 위협. 이란전쟁 에너지 인플레. 인하 하반기 후반 전망. Fed 독립성 리스크 | 04-18 | ✅ high |
| `geopolitics.md` | **IEEPA 위헌→실효 34.7%**. WTI $84, Brent $86~90. Gold $4,878. 리스크 5/5. **4.22 휴전 만료 D-3** | **이란전쟁·호르무즈 이중봉쇄**(극고). Section 301 4.28공청회. 북한 4월 3차 시험. NATO 5% 목표 | 04-19 | ✅ high |
| `korea_economy.md` | **수출 3월 $86.1B(+48.3%), 4월초순 $25.2B(+36.7%), 경상수지 2월 $23.2B(사상최대), KOSPI 6,226(+152% YoY, PBR 1.4배), 금리 2.50%(7연속 동결), 신현송 4/21 취임(매파), 원화 1,475원, WGBI 4/1 편입(2주 7.7조 유입), 삼성 Q1 OP 57.2조(역대최대), 추경 26.2조** | 신현송 매파 전환 리스크. 원화약세 패러독스(경상흑자에도 NPS 해외투자 70%). 외국인 3월 54.4조 순유출. 자동차 25% 관세. 반도체 관세 7월 확대 | 04-18 | ✅ high |
| `global_risk_factors.md` | **VIX 17.48(거짓안정5단계), F&G 62(Greed), DXY 97.70(3년최저), Gold $4,867(구조적Bull), Brent $90, WTI $84, 원달러 1,460, 소비심리 47.6(역대최저), IMF 3.1%(하향), 침체확률 30~49%** | 호르무즈 24시간 번복(개방->재봉쇄). 4/22 휴전만료. 미중 50% 추가위협. Gold-DXY 역상관 구조 이탈. 4중 체크포인트(4/23~5/15) | 04-19 | ✅ high |
| `political_cycle.md` | **Section 122 10%(07.24만료)+Section 301 대체 가속(4/28공청회), OBBB 시행, 파월 해임(5/15), 미중 정상회담(5/14~15), ECB 2.0%(4/29), NATO 5% 2035, 다카이치 122.3조엔, 미-인도 50→18%, 한국 대미$350B 특별법, AI규제(EU/US/한국), CHIPS Act 생산시대** | Section 301→국가·섹터별 차등관세 전환 리스크. 파월 해임 시 Fed 독립성·달러 시스템 리스크. 미중 정상회담 결과. ECB 인상 전환 가능성 | 04-19 | ✅ high |
| `tech_breakthrough.md` | **AI: Claude Opus 4.7(4/16), Agentic AI 97% 기업 배포(대중화 승격), EU AI Act 고위험 2027.12 연기. 반도체: TSMC N2 수율 65%·N2P H2, imec High-NA Q4 인증, Alphabet TPU CoWoS 병목. 에너지: CFS $863M 추가, Samsung SDI 전고체 파일럿. 양자: NVIDIA Ising QEC. 우주: NG-3 부스터 재사용. 바이오: 소형 CRISPR. 신소재: 그래핀-페로브스카이트 3,670h 안정성** | G-3 모듈 정상 운영. 8개 서브섹터 주간 갱신 완료 | 04-19 | ✅ high |
| `supply_chain.md` | **WCI $2,246(-3%), WTI $83/Brent $96, 구리 $12,630(관세50%), HBM 전량매진+HBM4양산, 요소비료 $640(-18%), TSMC 2nm양산+3nm 20만장, Section 232 확대(구리50%/제약100%), MATCH법안 발의** | **호르무즈 완전개방 선언(04/17, 실제 90% 미만)**. 4/21 휴전만료 최대 분기점. IEA SPR 400M bbl 방출. GS Brent $83. 삼중 인플레 약화 중 미완 | 04-18 | ✅ high |

---

## 📊 Market KB (`knowledge-base/market/`) — 부분 재수집 필요

| 파일 | 상태 | 갱신 빈도 | 영향 브리핑 모듈 | 재수집 명령 |
|------|------|----------|---------------|-----------|
| `daily_snapshot.md` | ✅ SUCCESS (04-21) valid_until 04-23 confidence:medium-high | 매 거래일 | A-1, B-2, B-3 | 04-23 재실행 |
| `economic_calendar.md` | ✅ SUCCESS (04-21) valid_until 04-28 confidence:medium | 주 1회 | A-4, B-1, C-6 | — |
| `surprise_index.md` | ✅ SUCCESS (04-21) valid_until 04-28 | 매일 | B-4 | — |
| `correlation_matrix.md` | ✅ SUCCESS (04-21) valid_until 04-28 | 주 1회 | B-5 | — |
| `guru_positions.md` | ✅ SUCCESS (04-18) valid_until 07-18 confidence:high | 분기 1회 | A-5, B-7, C-4 | Q1 2026은 05-15 이후 |

> **재수집 순서 권장:** economic_calendar → surprise_index → correlation_matrix → guru_positions (13F)
> daily_snapshot은 fetch_price.py --market --save로 매일 자동 갱신

---

## 💰 Portfolio KB (`knowledge-base/portfolio/`)

| 파일 | 상태 | 갱신 주체 | 비고 |
|------|------|---------|------|
| `model_portfolios.md` | ⚠️ 전 항목 미수집 | briefing-lead | `/모델포트폴리오` 실행 필요 |
| `rebalancing_history.md` | ✅ 첫 이력 등록 (04-14) | briefing-lead | 미국주식 87.8%→72%(6개월 목표) |
| `user_portfolio.md` | ✅ 갱신 완료 (04-14) confidence:high | briefing-lead | 총 2,820만원, 미국주식 87.8% |

---

## 📈 성과 추적 (`knowledge-db/performance/`)

| 파일 | 상태 | 데이터 | 갱신 주기 |
|------|------|-------|---------|
| `2026_recommendations.md` | 🟢 운영 중 | 제안 6건 (전부 진행중) | 매 브리핑 append |
| `2026_hit_rate.md` | ⚠️ 미등록 | — | `/성과리뷰` 첫 실행 시 생성 |
| `2026_scenario_tracking.md` | ⚠️ 미등록 | — | `/글로벌인텔리전스` 첫 실행 시 생성 |

---

## 🗄️ 시계열 원본 DB (`knowledge-db/`)

| 파일 | 레코드 수 | 갱신 주체 |
|------|---------|---------|
| `semiconductor_2026.jsonl` | 71건 | kb-updater |
| `ai_2026.jsonl` | 88건 (Anthropic 34건 포함) | kb-updater |
| `auto_2026.jsonl` | 46건 | kb-updater |
| `energy_2026.jsonl` | 106건 | kb-updater |
| `geopolitics_2026.jsonl` | 66건 | kb-updater |
| `science_tech_2026.jsonl` | 330건 (quantum/space/smr subtag 포함) | kb-updater |
| `bio_pharma_2026.jsonl` | 34건 | kb-updater |
| `macro_2026.jsonl` | 436건 | kb-updater |
| `banking_capital_2026.jsonl` | 38건 | kb-updater |
| `advanced_materials_2026.jsonl` | 83건 | kb-updater |
| `battery_2026.jsonl` | 40건 | kb-updater |
| `infrastructure_2026.jsonl` | 23건 | kb-updater |
| `capex_2026.jsonl` | 20건 | kb-updater |
| `telecom_next_2026.jsonl` | 62건 | kb-updater |
| `robotics_2026.jsonl` | 29건 (신규 생성 2026-04-19) | kb-updater |
| `crypto_bitcoin_2026.jsonl` | 48건 (신규 생성 2026-04-20) | kb-updater |
| `defense_2026.jsonl` | 25건 (신규 생성 2026-04-21) | kb-updater |
| `changelog_2026.jsonl` | 50건 | kb-updater |
| `market/2026_daily_prices.md` | 93줄 (archive) | market-data-collector |
| `market/2026_economic_indicators.md` | 26줄 (부분 수집) | market-data-collector |
| `market/2026_guru_changes.md` | 95줄 (Q4 2025 13F 8인 수집) | kb-updater |
| `market/2026_correlation_log.md` | 36줄 | correlation-monitor |

---

## 📚 참조 파일 (`reference/`)

| 파일 | 내용 | 에이전트 참조 시점 |
|------|------|----------------|
| `source_registry.md` | 37개 소스 + 접근성 등급 | data-collector, market-data-collector |
| `rules_and_constraints.md` | 금지사항 31개 | 모든 에이전트 (세션 시작 시) |
| `guru_watchlist.md` | 거물 투자자 8인 명단 | market-data-collector (13F 수집 시) |

---

## 🔄 KB 간 교차 참조 맵 (모순 감지용)

> wiki-linter가 주간 점검 시 이 맵 기준으로 수치 일관성 검증.

| 수치 | 파일 A | 파일 B | 마지막 검증 | 상태 |
|------|-------|-------|-----------|------|
| 미국 Fed 금리 | `us_monetary_policy.md` (루트): redirect 포인터 (수치 없음) | `macro/us_monetary_policy.md`: 3.50~3.75% (04-18 갱신) | 04-19 | SSOT 일치 |
| VIX | `global_risk_factors.md`: 17.48 (04-19) | `market/daily_snapshot.md`: 18.98 (04-21) | 04-21 | ✅ 일치 (daily_snapshot 최신, 시점차 +1.50, 허용범위 — 거짓안정 해제 반영) |
| DXY | `global_risk_factors.md`: 97.70 (04-19) | `us_economy.md §9`: 97.70 (04-17) | 04-19 | ✅ 일치 (동일 수치) |
| 원/달러 | `korea_economy.md`: 1,475원 (04-18) | `global_risk_factors.md §2`: 1,460원 (04-19) | 04-19 | ✅ 일치 (global_risk 최신, 시점차 -15원, 허용범위 2%) |
| S&P 500 | `us_economy.md §9`: 7,022 (04-17 신고가) | `market/daily_snapshot.md`: 04-19 기준 | 04-19 | ✅ 일치 (daily_snapshot 최신) |
| WTI | `industry/energy.md`: $84~94 (04-19) | `macro/geopolitics.md`: $83.85/bbl (04-17 종가) | 04-19 | ✅ 일치 (energy 최신, 범위 내 포함) |
| Gold | `macro/global_risk_factors.md §4`: $4,867 (04-19) | `market/daily_snapshot.md`: $4,878 (04-19) | 04-19 | ✅ 일치 (daily_snapshot 최신, 시점차 +11, 허용범위) |

---

## 🏗️ 섹터-종목 빠른 매핑

| 종목/테마 | 1차 KB | 2차 KB (맥락) |
|---------|-------|-------------|
| 삼성전자, SK하이닉스, 한미반도체 | `semiconductor.md` | `macro/geopolitics.md §1`, `macro/korea_economy.md §5-1` |
| NVIDIA, AMD, 브로드컴 | `industry/ai.md §2` | `semiconductor.md §4` |
| Anthropic, OpenAI, Google AI | `industry/ai_anthropic.md`, `industry/ai.md §4` | `macro/geopolitics.md §1-2` |
| 현대차, 기아 | `industry/auto.md §3-2` | `macro/geopolitics.md §1-1` (관세) |
| LG에너지솔루션, 삼성SDI, SK온 | `industry/auto.md §6` | `macro/korea_economy.md §5-3` |
| 한화에어로(012450), 현대로템(064350), LIG넥스원(079550), KAI(047810) | `industry/defense_industry.md §2` | `macro/geopolitics.md §4, §5, §8`, `industry/space.md` |
| LMT, RTX, NOC, GD, BA, KTOS | `industry/defense_industry.md §3` | `macro/political_cycle.md`, `macro/geopolitics.md` |
| Rheinmetall, BAE Systems, Dassault, Leonardo | `industry/defense_industry.md §4` | `macro/geopolitics.md` (NATO 3%) |
| 두산에너빌리티, 한수원 | `industry/smr.md §2, §4` | `industry/energy.md §7` |
| 클로봇, 레인보우로보틱스, 두산로보틱스, Figure AI, Tesla Optimus, Agility, 1X | `industry/robotics.md §2, §4` | `industry/ai.md §2` (NVIDIA Jetson), `macro/korea_economy.md` (정부지원) |
| 삼성바이오, 셀트리온 | `industry/bio_pharma.md` | `macro/korea_economy.md §5-5` |
| Gold, TLT, IAU | `macro/global_risk_factors.md §4` | `macro/us_monetary_policy.md` |
| BTC, ETH, SOL | `industry/crypto_bitcoin.md §1, §6` | `macro/global_risk_factors.md §2`, `market/daily_snapshot.md` |
| MSTR (Strategy), COIN, HOOD, MARA, RIOT, CLSK | `industry/crypto_bitcoin.md §2, §4, §8` | `industry/ai.md` (MARA AI DC 피벗), `macro/us_monetary_policy.md` |
| NuScale, Oklo, BWXT | `industry/smr.md §2` | `macro/tech_breakthrough.md §5` |
| 빅테크 CapEx, TSMC, ASML | `industry/capex.md §1, §2` | `industry/ai.md §3`, `semiconductor.md` |

---

## 📝 KB 업데이트 이력 (최근 10건)

| 날짜 | 파일 | 변경 | 레코드 |
|------|------|------|-------|
| 2026-04-21 | `industry/defense_industry.md` | **신규 생성** -- 국방·방산 산업 KB (012450 한화에어로 등 K-방산 4사 + 미 primes 6사 + EU 3사 종목분석 지원). K-방산 수출 2025 $15.4B→2026 $20B 목표. 미 primes 백로그 합산 $1조+. NDAA FY2026 $901B(상원 12/17). 한국 방위력개선비 19.97조(+11.9%). 한화 Redback **XM30 Phase 2 탈락 확정**(원 요청 45%가 아닌 100%, Rheinmetall vs GDLS 2파이널). 현대로템 폴란드 K2 2차 9조+선수금 3조 조기수령. LIG넥스원 중동 천궁-II 10.6조(UAE 2.6+사우디 4.25+이라크 3.7). KAI 2026 가이던스 매출 5.73조(+58%)·수주 10.44조(+63%) KF-21 인니 16대 MoU. Rheinmetall €12-13B 2026 매출·155mm 리투아니아 2026중반·Lynx KF-41 €10B 확장. BAE £84B 백로그 Eurofighter GCAP까지. Dassault Rafale €46.6B·2026 28대. ITA/XAR/PPA 연환산 16.66/18.33/18.20%. 우크라 종전 30%·한화 부채 220% 리스크 | +25 |
| 2026-04-20 | `industry/crypto_bitcoin.md` | **신규 생성** -- 크립토/비트코인 섹터 KB. MSTR 종목분석 지원. BTC $74,800·시총 $1.51T·ATH $126,210(2025-10, -39%)·Q1 -23.8%(2018 이후 최악). 네트워크 해시레이트 1.084 ZH/s, 난이도 135.59T. MSTR 780,897 BTC(공급 3.9%)·평균$75,577·총코스트 $59B·전환사채 $8.2B(쿠폰 0.421%)·Q1 미실현 -$14.46B. 우선주 4계층(STRK $21B ATM 8%/STRF $2.1B 10%/STRD 비누적). Bitcoin Yield KPI(BTC-per-share). BlackRock IBIT ~782K BTC·AUM $70.6B·일거래 $16~18B(Binance 경쟁). Q1 스팟 BTC ETF 유입 $18.7B, 총 AUM $128B+. 공개채굴사 Q1 32K BTC 매도($2.4B), 평균 생산비 $80K(BEP 이하). ETH $2,361 +8.6%, SOL $93, DeFi TVL $95.4B(ETH 68%). 스테이블코인 $320B+(USDT $185B/USDC $79B). SEC Atkins Project Crypto, SEC-CFTC MOU 3/11, GENIUS Act(2025.07). EU MiCA 2026-07-01 전면집행. 한국 디지털자산기본법 4/8 국회 진전. LTH 78%+ 역사최고 | +48 |
| 2026-04-19 | `industry/robotics.md` | **신규 생성** -- 로봇 섹터 KB. Physical AI(Figure $39B·BotQ 12K대, Tesla Optimus Gen3 Shanghai 1M/년, Agility Digit GXO 100K totes 상업수익, 1X EQT 10K대, Unitree 2026 물량 완판). 시장 $4~39B 편차(2030). 4강 FANUC 17%·ABB 13%·Yaskawa 12%·KUKA Top5. 한국: 클로봇(466100) 삼성(레인보우35%)·현대(BD $880M)·LG Atlas비전+Axium·두산로보. Harmonic Drive 85% 과점. Jetson Thor 2,070 TFLOPS. 4차 지능형로봇 기본계획 2024-28 3조원·100만대 | +29 |
| 2026-04-19 | `industry/science_tech.md` | **주간 갱신** -- 한국 정부R&D 35.3조 확정(+21.4%). 경구 Wegovy FDA승인(월$149)+Lilly orforglipron Q2. IonQ 포토닉 인터커넥트(양자네트워킹 최초). 빅테크 CapEx $7000억(+60%). PANW-CyberArk $250억. Synopsys AgentEngineer vs Cadence ChipStack AI 에이전트전쟁. Optimus Gen3 자율보행+상하이 양산. WIPO PCT 2025 한국 28년 연속 성장. 반도체+디지털통신 +6.1% 최고 성장 | +35 |
| 2026-04-19 | `macro/tech_breakthrough.md` | **주간 갱신** -- AI: Claude Opus 4.7(4/16), Agentic AI 97% 기업 배포(대중화 승격), EU AI Act Digital Omnibus 고위험 2027.12 연기. 반도체: TSMC N2 수율 65%·N2P H2 양산, imec High-NA Q4 인증, ASML 패키징 진출, Alphabet TPU CoWoS 병목. 에너지: CFS $863M 추가 펀딩, Samsung SDI 전고체 파일럿 프로토타입 납품. 양자: NVIDIA Ising QEC AI, QuEra Tsim. 로봇: Figure 03 BotQ 12K대/년. 우주: Blue Origin NG-3 부스터 재사용(4/19), Starship V3 지연. 바이오: 소형 CRISPR(NIH). 신소재: 그래핀-페로브스카이트 3,670h 안정성(Science), 유연 페로브스카이트 25.09% 기록 | +27 |
| 2026-04-19 | `macro/geopolitics.md` | **주간 갱신** -- 호르무즈 4.17개방→4.18재봉쇄(24시간 번복). 4.22 휴전만료 D-3 최대분기점. WTI $97→$84 급락. Section 301 4.28공청회 개시(한국 반박 의견서 제출). 북한 4월 3차 시험(구축함+탄도미사일). NATO GDP 5% 목표 합의. TSMC $1,650억 투자확대. 이스라엘-레바논 10일 휴전 | +14 |
| 2026-04-19 | `macro/global_risk_factors.md` | **주간 갱신** -- 호르무즈 24시간 번복(4.17개방->4.18재봉쇄). IMF WEO 글로벌 3.3%->3.1% 하향. VIX 17.48 거짓안정5단계. F&G 62(탐욕전환). DXY 97.70(3년최저). Gold $4,867 구조적Bull(Gold-실질금리 상관 붕괴). WTI $84/Brent $90(재봉쇄 변동). 원달러 1,460(원화강세전환). BTC-NASDAQ 상관 붕괴. 침체확률 30~49%. 미 부채 $38.4조. 4중 체크포인트(4/23~5/15) | +12 |
| 2026-04-19 | `industry/capex.md` | **신규 생성** -- 글로벌 설비투자 트래커. 빅테크AI 5사 합산 $660-690B. 반도체 총 $200B. 장비시장 $139-145B. 에너지 $3.3T. 국방 $2.63T. CHIPS Act $31B+민간$400B | +20 |
| 2026-04-19 | `industry/advanced_materials.md` | **전면 갱신** -- MicroLED/EDA/소재 전면 데이터 | +48 |
| 2026-04-19 | `industry/telecom_next.md` | **전면 갱신** -- 6G/위성/보안 3개 서브섹터 | +33 |
| 2026-04-19 | `industry/smr.md` | **전면 갱신** -- TerraPower/Kairos/RR-SMR/CFS/Helion/두산 | +16 |
| 2026-04-19 | `industry/space.md` | **전면 갱신** -- SpaceX/Blue Origin/RKLB/Starlink/AST/우주군 | +13 |
| 2026-04-19 | `industry/quantum.md` | **전면 갱신** -- NVIDIA Ising/IonQ/D-Wave/PsiQuantum/Meta PQC | +13 |
---

## 🤖 에이전트 활용 가이드

```
질문 유형별 1차 참조 파일:

"삼성전자 실적은?" → semiconductor.md §3 컨센서스
"Fed 금리 전망?" → macro/us_monetary_policy.md (루트 파일)
"오늘 시장 상황?" → market/daily_snapshot.md ⚠️ 현재 FAILED
"미중 관세 영향?" → macro/geopolitics.md §1-1
"AI 투자 동향?" → industry/ai.md §3 CapEx
"Anthropic 현황?" → industry/ai_anthropic.md §3 ARR, §6 IPO
"한국 방산 투자?" → macro/geopolitics.md §4, §5, §8
"지정학 리스크?" → macro/global_risk_factors.md §1 Top5
"포트폴리오 구성?" → portfolio/model_portfolios.md ⚠️ 현재 미수집
"SMR/원자력 투자?" → industry/smr.md §2 기업현황, §5 빅테크 DC
"두산에너빌리티?" → industry/smr.md §4 한국 관련
"설비투자/CapEx?" → industry/capex.md §1 빅테크, §2 반도체, §7 한국
```

> **에이전트 원칙:** 이 인덱스로 대상 파일 특정 → 해당 파일만 Read → 분석 완료 후 인사이트를 "최근 핵심 인사이트" 섹션에 1줄 append (briefing-lead만).
