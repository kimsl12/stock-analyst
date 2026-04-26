---
updated: 2026-04-26
version: v3.2
maintainer: wiki-linter (자동) + briefing-lead (수동)
lint_last_run: 2026-04-26
lint_mode: full
---

# Knowledge Base Index — Wiki Master Index

> **목적:** 에이전트가 이 파일 하나만 읽으면 전체 KB 구조, 핵심 인사이트, 건강 상태를 파악할 수 있어야 한다.
> **갱신 주체:** wiki-linter (자동 갱신, 주 1회) + briefing-lead (브리핑 종료 시 인사이트 append)
> **활용법:** 에이전트는 질의 전 이 파일을 먼저 읽고, 필요한 파일만 드릴다운한다. Glob 탐색 금지.

---

## P0 — 즉시 조치 필요 (FAILED / 만료)

> wiki-linter가 탐지한 긴급 항목. 브리핑 실행 전 반드시 확인.
> **최종 갱신: 2026-04-26 (wiki-linter full)**

| 파일 | 상태 | 영향 모듈 | 조치 |
|------|------|----------|------|

> [INFO] P0 해제 — portfolio/model_portfolios.md 2026-04-21 갱신 완료 (confidence:high, F-1~F-7 전면 작성). 현재 전체 KB P0 항목 없음.
> [INFO] 전체 KB P1 이하 — 브리핑 실행 가능 상태. 상세 P1 항목은 아래 P1 섹션 참조.

---

## P1 — 이번 주 조치 (탐지: 2026-04-26 full)

> wiki-linter P1 탐지 결과. 브리핑 실행 가능하나 이번 주 내 처리 권장.

| 파일 | 문제 | 심각도 | 권장 조치 |
|------|------|-------|---------|
| `korea_economy.md` (루트) | 레거시 파일 2026-04-07 데이터 — 원/달러 1,410원 등 최신치(1,476원) 대비 구버전. valid_until 2026-05-07 | 중간 | `macro/korea_economy.md` SSOT 참조 유지. 루트 파일 수치 갱신 또는 redirect 포인터로 교체 권장 |
| `market/surprise_index.md` | collection_status: PARTIAL — 일부 지수 미수집 | 낮음 | 다음 갱신 시 완전 수집 목표. 브리핑 사용 가능하나 주의 필요 |
| `_index.md` 교차참조 맵 | 수치가 04-19 기준으로 구버전 (VIX 17.48→19.31, DXY 97.70→98.52, Gold $4,867→$4,709, 원달러 1,460→1,476) | 낮음 | 교차참조 맵 수치 현행화 (아래 갱신 완료) |
| `industry/real_estate.md` | _index.md Industry KB 테이블 미등재 (고아 파일) | 낮음 | _index.md Industry KB 표에 추가 (아래 갱신 완료) |


> [P1 해결완료 2026-04-21 오전] industry/bio_pharma.md 신규 생성, industry/semiconductor.md 신규 생성 + 루트 semiconductor.md 삭제(구조 통일), industry/ai.md + industry/auto.md 갱신 (kb-updater 4건 병렬).
> [P1 해결완료 2026-04-21 오후] 루트 redirect 파일 3종(geopolitics.md, global_risk_factors.md, us_monetary_policy.md) 본문 삭제 + SSOT 포인터 포맷 통일. 구 데이터 잔존 문제 해소 — 실제 브리핑·분석은 모두 macro/ SSOT 사용 중임을 전수 조사로 검증(lead_*.md 0건 루트 참조). wiki-linter 교차참조 맵은 유지(SSOT 대조 용도).
> [P1 정상] industry/ 전체 고아 파일 없음 (**19개** 파일 모두 _index.md 등재 확인). luxury.md(04-21 야간) + defense_industry.md(04-21) + semiconductor.md(04-21) + bio_pharma.md(04-21) + crypto_bitcoin.md(04-20) + robotics.md(04-19) 포함.
> [P1 정상] knowledge-db/ SSOT-only 파일 추가 확인 없음.
> [P1 해결완료 2026-04-24] market/daily_snapshot.md 04-24 갱신 완료 (valid_until→04-26). economic_calendar.md FOMC 의사록 오류 정정 + 04-23 결과 반영. IBM/ServiceNow/TI Q1, 한국 Q1 GDP +1.7% 반영.

---

## ⚡ 최근 핵심 인사이트 (지난 7일 — briefing-lead append)

| 날짜 | 출처 | 인사이트 | 관련 KB | 제안 상태 |
|------|------|---------|--------|---------|
| 2026-04-13 | 이브닝브리핑 | 호르무즈 봉쇄 선언 — WTI $105 급등, 4/14 아시아 갭다운 -2~4% 경고. 위험등급 4→5 상향 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-13 | 이브닝브리핑 | Gold-DXY 역상관 약화 Z+1.8σ — Gold $4,724 구조적 Bull. 중앙은행 매수+재정적자=탈달러 수요 | `macro/global_risk_factors.md §4` | 진행중 |
| 2026-04-13 | 이브닝브리핑 | WTI-인플레기대 동조화 Z+2.3σ — Core CPI 전이 2~3개월 시차. Fed 6월 인하 소멸 가능 | `macro/us_monetary_policy.md` | 진행중 |
| 2026-04-09 | ai_anthropic.md 신규 → ai.md 흡수(2026-04-21) | Anthropic ARR $30B — OpenAI 최초 추월. 엔터프라이즈 LLM 점유율 40% | `industry/ai.md §4` | — |
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
| 2026-04-24 | 모닝브리핑 | 소프트웨어 AI 검은 목요일 — IBM Beat에도 -10.3%, ServiceNow -18%. TI +10% 반도체 분열 → AI 인프라 vs SaaS 구조적 재편 시작 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-24 | 모닝브리핑 | 한국 Q1 GDP +1.7% q/q 대형 서프라이즈(5.5년 최고, 컨센 +0.9% 두 배) — 반도체 수출+설비투자 동반. KOSPI PER 디스카운트 재평가 여지 | `market/economic_calendar.md` | 진행중 |
| 2026-04-24 | 이브닝브리핑 | Intel Q1 EPS +2,800% 서프라이즈(AH +20%) + TI +10% = 반도체 2일 연속 대형 Beat. AI 인프라 슈퍼사이클 "7회 초~중반" 판정. 소프트웨어 AI 공포와 극명 대비 | `market/daily_snapshot.md, market/economic_calendar.md` | 진행중 |
| 2026-04-24 | 이브닝브리핑 | 트럼프 호르무즈 기뢰 격침 명령 + 이스라엘-레바논 휴전 3주 연장 = "에스컬레이션+휴전 병존" 모순. WTI $96/Brent $105(5일 연속). 4/25 Core PCE 최대 리스크 | `macro/geopolitics.md §2-1, market/daily_snapshot.md` | 진행중 |
| 2026-04-24 | 이브닝브리핑 | WTI↔BEI 이상 Z+2.0sigma 승격 -- 에너지 CPI 전이 시차 2~3개월. Fed 인하 완전 소멸 시나리오 확률 35~40%. Core PCE >3.2% 시 연내 인하 0회 | `market/correlation_matrix.md, macro/us_monetary_policy.md` | 진행중 |
| 2026-04-25 | 모닝브리핑 | Intel Q1 EPS +2,800% 서프라이즈(+24%) → AI 인프라 슈퍼사이클 레거시 확산 확인. Philly Sox 18거래일 연승(역대 최장). "AI 가위"(인프라↑ vs SaaS↓) 구도 선명 | `market/daily_snapshot.md, market/economic_calendar.md` | 진행중 |
| 2026-04-25 | 모닝브리핑 | PMI 입력비용 2022년 이후 최대 + WTI $96(5연속) — 4/30 GDP+PCE 동시 발표 최대 분기점. 스태그플레이션 내러티브 점검 구간 | `market/surprise_index.md, macro/us_economy.md` | 진행중 |
| 2026-04-25 | 모닝브리핑 | GDP Q1 Advance + Core PCE 3월 발표일 정정: 4/25 → **4/30** (BEA 공식 일정 확인). 기존 캘린더 오류 수정 | `market/economic_calendar.md` | — |
| 2026-04-25 | 이브닝브리핑 | S&P 7,165.08 확정 신고가(모닝 7,121 대비 +44pt) — 반도체가 S&P 12.8% 랠리의 40% 기여. 1990년대 인터넷 초기 유사 섹터 집중도. breadth 리스크 극대화 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-25 | 이브닝브리핑 | WTI↔BEI Z+2.0sigma 재확인 + PMI 입력비용 + ISM 78.3 = 2022년 3월 이후 최초 동시 발생. FOMC 4/28-29 "closely monitoring" 톤 변화 확률 40% | `market/correlation_matrix.md, macro/us_economy.md` | 진행중 |
| 2026-04-25 | 이브닝브리핑 | X-Energy(XE) IPO $23→$30.11(원자력 역대최대 $10B+) — AI DC 전력 수요 구조적 수혜 SMR 신규 테마. Marks/Druckenmiller 에너지전환 컨버전스 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-25 | 주간리포트 | "AI 가위" 주간 종합 — Philly Sox 18일 연승(역대 최장) + Intel +2,800% vs ServiceNow -18%/IBM -10.3%. AI 인프라↑/전통SaaS↓ 구조적 분열 공식화. PSR 프리미엄 체제 전환 시작 | `market/daily_snapshot.md, lead_weekly_20260425.md C-3.5` | 진행중 |
| 2026-04-25 | 주간리포트 | 4/30 "트리플 폭탄" 분기점 — GDP Q1 Advance(GDPNow 1.24%) + Core PCE 3월 + MSFT/META Q1 동시 발표. Bear 55% 가중: 선행(소비심리 49.8/WTI $96)이 후행(실적 81% Beat)을 4~8주 잠식 확률 우세 | `macro/us_economy.md, lead_weekly_20260425.md C-7` | 진행중 |
| 2026-04-25 | 주간리포트 | Gold $4,724 주간 -2% 조정 = 구조적 Bull 내 매수 기회(contrarian). Gold-실질금리 상관 붕괴(+0.18 vs 전통 -0.45) 4주째 지속. 중앙은행 1,000톤+/년 + JPM $5,055(4Q26E) | `macro/global_risk_factors.md §4, market/correlation_matrix.md` | 진행중 |
| 2026-04-26 | 모닝브리핑 | 트럼프 이란 특사 파견 취소(4/25 저녁) — 대면→전화 전환. 금요일 "평화회담 기대" 서사 번복. WTI $94.88 유지이나 월요일 반등 리스크. 오만 무스카트 대안 중재지 부상 | `macro/geopolitics.md §2-1, market/daily_snapshot.md` | 진행중 |
| 2026-04-26 | 모닝브리핑 | WTI↔BEI "서비스 인플레 고착" 구조 전환 최초 포착 — WTI 하락(-1.24%)에도 10Y 상승(+2bp). 에너지→서비스 인플레 동력 이동 시사. 4/30 Core PCE 최종 판별자 | `market/correlation_matrix.md, macro/us_economy.md` | 진행중 |
| 2026-04-26 | 모닝브리핑 | 4/29~30 "48시간 결정전" — FOMC(파월 톤 40%) + 빅테크 4건(MSFT/META/AMZN/GOOGL AI CapEx) + GDP Q1(GDPNow 1.24%) + Core PCE + ECB + AAPL. 골디락스 vs 스태그 분기 | `market/economic_calendar.md` | 진행중 |
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
| 2026-04-22 | 모닝브리핑 | **이란 무기한 휴전 연장**(Trump 04-21 장후 발표) — "30일 최대 분기점" 낙관 해소. WTI $87.88→$86. VIX 18.98→17.48 "거짓 안정 5단계" **재귀적 복귀**. 리스크 봉인이지 소멸 아님(IRGC 기뢰 21건 미해제) | `macro/geopolitics.md §2-1, market/daily_snapshot.md` | 진행중 |
| 2026-04-22 | 모닝브리핑 | KOSPI **6,388.47 사상 최고 종가 신기록**(+2.72%). SK하이닉스 **120만원 돌파**(+4.97%). JPMorgan KOSPI 목표 8,500. Tepper EWY $286M 한국 베팅 수익 확인 | `market/daily_snapshot.md, market/guru_positions.md` | 진행중 |
| 2026-04-22 | 모닝브리핑 | Gold **$4,782 — $4,800 지지선 이탈**. 호르무즈 완화 반사 하락이나 DXY 98.3 구조적 약세 불변 → 탈달러 수요 손상 없음. 48시간 $4,800 재탈환 시 구조적 Bull 재확정. contrarian: 매수 기회 | `macro/global_risk_factors.md §4, market/correlation_matrix.md` | 진행중 |

---

## 🏭 Industry KB (`knowledge-base/industry/`)

| 파일 | 핵심 수치 | 최신 인사이트 | 갱신일 | 유효기간 | 신뢰도 |
|------|---------|------------|-------|---------|-------|
| `industry/semiconductor.md` | HBM 점유 SK하이닉스 62% + Micron 21% > Samsung 17%(첫 역전). NAND **+70~75% QoQ 폭등** 2026 사전 완판(기존 "약세" 예측 전면 역전). HBM4 SK 세계 최초 2025-09 양산. NVIDIA Blackwell Ultra GB300 2026.01 조기 출하 | TSMC N2 2nm 수율 65%, 2026 capex $52-56B+애리조나 Phase 2/3. 삼성 파운드리 3nm 수율 60% 미만 지속. 하이퍼스케일러 CapEx $660-690B(기존 $420-480B 대폭 상향). MS Azure $80B 전력 병목. Huawei Ascend 910C 600K. 트럼프 Section 232 25% 칩 관세 | 04-21 | 05-21 | high |
| `ai.md` | **Anthropic ARR $30B로 OpenAI $25B 최초 추월**, 밸류 $380B→$800B 오퍼, Claude 4.7/Code $2.5B run-rate. OpenAI $852B 펀딩(SoftBank 주도, MS 지분 $135B). Gemini 3.1+TPU v7 Ironwood GA. Meta Llama 5(4/8) 프론티어 오픈 | NVIDIA Blackwell Ultra GB300 2026.01 조기 출하(60K랙, +129% YoY). DRAM Q1 +90% 메모리 병목. EU AI Act 2026.08.02 고위험 D-103. Computer Use/Operator 실전 전환. Upstage 유니콘, SKT AIDC +53% | 04-21 | 05-21 | high |
| `auto.md` | **한국 관세 15% 유지**(2025.11 인하, 트럼프 2026.04 25% 재인상 압박 중). HMG 관세비용 7.4조(15% 기준), 재인상 시 11조. HMGMA 포함 미국 현지 100만대 체제. Tesla Q1 + Robotaxi 무인 개시(2026.04.18 Dallas·Houston) | Apollo Go 주당 30만회·20개 도시·RT6 $30K. K-배터리 3사 가동률 50% 초반, 글로벌 점유 12%, 합산 적자 -3.2조. 삼성SDI 적자전환, LG엔솔만 OP +83%. 전고체 Solid Power/QuantumScape 상용화 지연 | 04-21 | 05-21 | high |
| `energy.md` | **Brent $105+, WTI $94~97**, JKM low-$16s, 정제마진 **$44.9**(역대급), Henry Hub $2.52(최저) | 트럼프 특사 취소(4/25 협상 결렬). 호르무즈 사실상 폐쇄(일5척). IEA 역대최대 공급차질(-10.1Mbpd). **SPR 22.46Mbl 방출(정책전환)+스왑20M+bl**. 정유 가동률 65~70%. 석화 불가항력 지속(마진 회복 조짐). X-Energy IPO $1.02B(원자력 역대최대). 한화솔 OP 6,157~8,829억. 두산엔 OP 1.1조 | 04-26 | 05-26 | high |
| `science_tech.md` | 한국 R&D/GDP **5.1%**(OECD 2위), 글로벌 R&D 3.8조달러, 정부 R&D **35.5조**(+19.9%) | **양자**: IBM Heron R2 QEC 10x+IonQ FT 99.99%+PQC $29.95B(2034E). **바이오**: Lilly Foundayo 경구GLP-1 FDA승인(04월)+Insilico $2.75B. **우주**: Falcon9 600착+Starship V3 점화. **로보틱스**: Optimus V3 중반 데뷔(04-23)+Figure02 BMW 30K+Agibot 1만대. **핵융합**: CFS SPARC late2026~2027(소폭후퇴)+Helion 외부연구$4M. **EDA**: Siemens Fuse 3파전+AI EDA $4.27B. **CapEx**: $635~665B(+67~74%). 전고체 QS Eagle+SDI 500Wh/kg | 04-26 | 05-26 | high |
| `bio_pharma.md` | **LLY 2026E $80~83B 가이던스(컨센 $77.6B 상회)** Zepbound/Mounjaro $36.5B(+45%), orforglipron 경구 GLP-1 2026.04.01 FDA 승인. NVO -5~-13% 가이던스 쇼크 + 경영진 교체 | **삼성바이오 207940** 2025FY 4.55조(+30%), 2026E 5조+, OPM 40%중반. 5공장(18만L) + BIOSECURE Act 반사이익. 트럼프 관세 2026.07.31 발효(브랜드약 100%, **한국 15%**, 록빌 공장 6만L 프리미엄). 목표주가 224.7만(Strong Buy 25인) | 04-21 | 05-21 | high |
| `quantum.md` | IonQ FY2026 $225-245M(+81%), **SkyWater $1.8B 수직통합**, Quantinuum IPO S-1($20B+), 양자센서 $502M-984M(국방40%), **CISA PQC 연방의무화** | IonQ 포토닉인터커넥트(DARPA HARQ). QuEra 2:1 QEC(04-20). Google 중성원자듀얼트랙. 양자주 7거래일 IonQ+72%(P/S 106x). Google PQC 2029+Meta 프레임워크. 한국 양자클러스터 공모(04-17) | 04-25 | 05-25 | high |
| `space.md` | 우주경제 $626B(2025), Starlink **11,856기**/1,000만, SpaceX **$1.75T IPO**, RKLB $602M, 우주군 $26B+Golden Dome $40B, KASA R&D 9,495억 | **Artemis II 성공**(4/1~11, 50년 만에 유인 달 비행). Starship V3 IFT-12 5월 목표. Blue Origin NG-3 부스터 재사용 성공이나 **BlueBird 7 궤도이탈**(AST -$2B). Amazon Leo 241기 FCC 미달(2년 연장). Golden Dome 12개사 $3.2B(4/24). OneWeb Gen2 440기. Astroscale ELSA-M 2026 발사 | 04-25 | 05-25 | high |
| `smr.md` | TerraPower NRC 건설허가(03/04), Kairos Hermes 2 착공(04/17), CFS SPARC first plasma 2026, 두산 수주 14.3조, 빅테크 원자력 DC MS 2GW/Google 500MW/Amazon 5GW/Meta 6.6GW | TerraPower 비경수로 최초 NRC 건설허가. Kairos Gen IV 최초 착공. RR-SMR UK 정식 계약(04/13). Helion 1.5억도. 체코 26조. confidence medium->high 승격 | 04-19 | 05-19 | high |
| `telecom_next.md` | **6개 서브섹터 확장**(6G/5G-Adv/Open RAN/위성통신/NTN/AI-RAN). ITU TPR 20개 확정(2026.02), AI-RAN $3.81B(CAGR 29%), Open RAN 5%->28%(2029), Starlink Mobile 2500만 목표, Starlink 1000만+, T-Mobile DTC 300만+, AI-RAN Alliance 100+사 | 3GPP Rel-21 2026.06 타임라인 결정점. **AST BlueBird7 궤도실패**(04.19). Amazon Leo 베타 라이브(04.08) FCC 미달. SKT-삼성 AI-RAN 공동연구. SKT MWC2026 AI 네이티브 선언. 한국 6G 예산 1067억 증액. Nokia QKD 인수. NVIDIA Aerial 오픈소스. 6G 표준 fork 리스크. 5G SA 의무화 | 04-25 | 05-25 | high |
| `banking_capital.md` | **KB 1Q26 1.8924조 확정 +11.5% (분기 역대 최대, 4/23 발표)·4대 합산 컨센 5.2371조(+6.2%, 1Q 첫 5조 돌파)·KB 2.9조 자사주 소각(업계 최대)·NH증권 Q1 OP 6,367억 record(+120.3%)**. 글로벌 M&A Q1 $1.2조(+42% YoY record), GS Advisory $1.49B(+89%) 1위 $267B·GS 2026-04-23 Buy 83.9 A- 분석 완료. BLK AUM $13.9T·EPS $12.53 Beat | JPM EPS $5.94 Beat (NII가이던스 $104.5B→$103B 하향)·BAC NII 가이던스 +5~6%→+6~8% 상향·C 순익 +42%·WFC 미달. MS IB +36%. USB/PNC CRE 11분기 감소 후 복귀. Blackstone $1.3T record(+12%). KKR/APO 2026-02 -10%+ AI SaaS 충격. **Basel III Endgame 2026-03-19 재공표, 6/18 의견수렴, Q4 최종안 예상, $250B 이하 면제**. 미 CRE Wall $1.5조 2026 만기. BOK 2.50% 7연속 동결, 신현송 인상 시사(중동 2차파급). 한국 ETF 400조 돌파(4/15). 카카오페이 매출 +30% OP +491% | 04-24 | 05-24 | high |
| `advanced_materials.md` | **6개 서브섹터 전면 재구성**(CNT/그래핀/초전도체/SiC-GaN-세라믹/희토류/정책). CNT 4.85~8.8B(2026E), GaN파워 CAGR 44%, Nd YoY+107%, 그래핀 반도체 FET 시연, HTS 핵융합 30만km 수요 | Wolfspeed 파산(6" SiC $1,500->중국 $500). 중국 희토류 12원소 수출통제(유예~2026.11). Georgia Tech 그래핀 FET. LG화학 CNT 6,100t. EU Advanced Materials Act 2026 입법. 한국 소부장 국산화율 소재30%/장비10% | 04-25 | 05-25 | high |
| `battery.md` | **리튬 $20,684/ton CIF(2026-04-01, +66.7% in 3M)** — 2026.01 $26,278 고점 후 조정. **K-3사 합산 OP -3.2조**(LGES +83%, SDI 적자전환 -1.42조, SK온 -0.49조), 가동률 50%초, 글로벌 점유 **15% 붕괴**(SNE Jan-Feb: CATL 42.1%/BYD 13.4%/LGES 8.7%/SK 3.8%/SDI 2.5%). **auto.md 정합 100%** | Ford BlueOval 해산 Tennessee 67GWh 단독. CATL 헝가리·인도네시아 가동, Qilin 2nd Gen. BYD Blade 2.0(3/5). LFP 2026E 65% 도달. 전고체 Toyota 2027~28 첫 EV. 코발트 $56,290(+67% YoY). AI DC ESS 2030 $6B | 04-21 | 05-21 | high |
| `infrastructure.md` | **현대건설 Q1 OP 1,734억 + 홀텍 SMR EPC 4~5조**, 대우 18조/GS 17.8조/DL 12.5조, 삼성물산 EPC 10조+·평택 P5 착공. **변압기 납기 128~144주(DC 50%+ 지연)** — 효성중공업 13.85조·HD현대일렉 12.48조 수주잔고, Vertiv $15B·Eaton $12B | 우크라이나 재건 $523.6B·NEOM 재조정·중동 재건 $140B·CHIPS 팹 1.5조 달러. smr/capex/defense/banking_capital 정합 확인 (SMR 두산 14.3조·DC CAPEX $660-690B·방위력 19.97조·PF 금리 6.1%) | 04-21 | 05-21 | high |
| `capex.md` | 하이퍼스케일러 4��� 합산 $635-665B(+67~74%), 5사 $660-690B, TSMC Q1 $35.9B(GM66%/OPM58%), 반도체장비 $139-145B, 유틸리티 $1.4T | MSFT $110-150B(CRPO $625B). GOOGL Cloud백로그 $240B. Intel 18A HVM $15B백로그. SK하이닉스 19조 패키징. 한국4대 800조 공약. AI ROI GS $1T필요 vs 컨센$450B. 전력병목 24-72개월 | 04-25 | 05-25 | high |
| `robotics.md` | 휴머노이드 2030E $4~39B 편차. Figure $39B밸류·BotQ 12K→50K대/년. Tesla Optimus Gen3 H2 양산+Shanghai 1M/년. Agility Digit 상업수익(GXO 100K totes). Harmonic Drive 85%. Jetson Thor 2,070 FP4 TFLOPS | 삼성(레인보우 35%)·현대(BD 80% $880M)·LG(Atlas비전+Axium)·두산로보·클로봇 생태계. EU AI Act 고위험 2026.08 발효. 클로봇 Q3 매출 +38.9%/레인보우 +117.6% | 04-19 | 05-20 | high |
| `crypto_bitcoin.md` | BTC $74,800~75,574, 시총 $1.51~1.54T, ATH $126,210(2025-10, -39%), Q1 -23.8%, 해시레이트 1.084 ZH/s, MSTR 780,897 BTC(3.9% 공급)·평균$75,577·전환사채$8.2B, IBIT AUM $70.6B, 스팟 BTC ETF Q1 유입 $18.7B, 스테이블코인 $320B+ | MSTR STRK $21B/STRF $2.1B/STRD 우선주 구조. Bitcoin Yield KPI = BTC-per-share. 채굴사 Q1 32K BTC 매도(BEP 이하). SEC Atkins Project Crypto·GENIUS Act(2025.07). EU MiCA 2026-07-01 전면집행. 한국 디지털자산기본법 4/8 진전 | 04-20 | 05-20 | high |
| `defense_industry.md` | **NDAA FY2026 $901B**(상원통과), 미 primes 백로그 합산 $1조+(LMT $194B/RTX $268B/NOC $95.7B/GD $118B/BA $545B+), K-방산 수출 2025 $15.4B→2026 $20B목표, 한국 방위력개선비 19.97조(+11.9%) | 한화에어로 Redback **XM30 Phase 2 탈락 확정**(Rheinmetall vs GDLS 2파이널 9월 결정). 현대로템 폴란드 K2 2차 9조+선수금 3조 조기수령. LIG넥스원 수주잔고 23.5조(중동 천궁-II 10.6조). KAI 2026 가이던스 매출 5.73조(+58%)·수주 10.44조(+63%) KF-21 인니 16대 MoU. Rheinmetall Lynx KF-41 €10B 확장. BAE Eurofighter GCAP까지 가득참. Dassault Rafale €46.6B 백로그 | 04-21 | 05-21 | high |
| `luxury.md` | **2026 K자 양극화 고착**: Gucci 2025 -26%(로고 15년래 최대 축소)·Burberry -17% vs **Hermès +6% CER·Cucinelli +10%·Bottega Q1 +17.9%**. LVMH Q1 €19.1B(-6%)·F&L 유기 -2%. Trump 15% 관세 재부과 위협(EU €93B 보복), 2026-02 IEEPA 불법 판결. 한국 면세 따이공→FIT 전환 확정, 춘제 면세 +90% YoY | **한국 수혜 순위**: 1순위 현대백화점(069960, TP 110K), 2순위 호텔신라(008770, TP 58K, DF1 철수 OP +800억), 3순위 아모레(090430). 회피: LG생활건강(051900, 더후 부진 장기화). Quiet Luxury 승자(Hermès·Cucinelli·Bottega)·패자(Gucci·Burberry) 구조 고착 | 04-21 | 05-21 | high |
| `consumer_retail.md` | **미국 Core PCE 3.0%·CB Consumer Confidence 91.8(Expectations 70.9↓)·UMich 54.0(YoY-20%)·소매판매 MoM 0.1%(관세직격)·한국 CPI 2.2%. WMT Q4 FY26 US comp +4.6%·e-comm +24%·매출 $700B 첫 돌파. COST Executive 39.7M(+9.1% YoY, 매출 74.3% 기여)·Kirkland $90B. 이마트 2025 OP 3,225억(+584.8%). 쿠팡 2025 49.12조(+14%)·Wow 15M·Q4 OP-97%(개인정보 유출)** | CU(BGF) 2026 Q2 GS25 매출 역전(BGF 상장 이래 최초), 18,711개/8.88조. K-뷰티 Q1 $31억(+19%), 미국 $6.2억(+40.9% 3년 1위). K-Food+ $33.5억, 라면 $4.35억(+26.4%). Trump 중국관세 145%+de minimis 폐지→Temu 미 직배송 중단·로컬셀러 전환, Shein 터키·멕시코·브라질 공장. 미 PB $283B(Great Value 86% 침투). Quick Commerce 2029E $55.5B. **Costco(COST) 2026-04-22 Buy 81.0 분석 완료** | 04-22 | 05-22 | high |
| `logistics.md` | **SCFI 1,826.77p(W13)·Drewry WCI $2,246/40ft(-3%)·BDI 2,523p·호르무즈 VLCC $87,711/d·보험료 1% hull(4배)·Long Beach 2026E 9M TEU·부산 24.4M·CJ대한통운 2025 OP 5,081억→2026E 5,630억(+14%, 쿠팡 반사)·HMM 2025 OP 1.46조(SCFI YoY-37% 방어), 2026 공급과잉 SCFI 1,000~1,500·팬오션 2026E OP 5,260억·Symbotic Backlog $22.5B·FedEx Q1 FY26 $22.2B(+3%)·UPS Amazon-50%·UNP/CSX Q1 upcycle·창고자동화 $34.17B** | 2M 해체→Gemini(Maersk+HL)/Ocean(CMA CGM+Evergreen+COSCO 9.5M TEU)/Premier(ONE+HMM+YM 3.8M)/MSC 독자. ILA 2030-09-30까지 임금 +61.5% 타결. 파나마 Gatun 수위 회복 but 32 slots(pre-drought 36-38 미복구), NOAA El Niño Watch 4월 재가뭄 리스크. 수에즈 Houthi 봉쇄 지속. 트럼프 관세 컨테이너 中→美 -16%, Laredo 국경 트럭 +14% YoY, 멕시코 FDI 2026E $40-45B(Kearney 19위 승격). IMO 2030 -40% CO2·암모니아 2037 경제적·최종 가이드 2026-05. 콜드체인 Healthcare 3PL $49.49B·Biopharma CAGR 10.98% | 04-24 | 05-24 | high |
| `healthcare_service.md` | **UNH Q1 2026 매출 $111.7B·Adj EPS $7.23(컨센 상회)·FY26 가이던스 >$18.25 상향·MBR 83.9%·MA 시니어 Q1 -965K. HUM 2026 MA +25% but EPS $9 쇼크(컨센 $12). ELV FY26 EPS >=$19.85 하향($935M CMS 부채). ISRG Q1 +23% YoY·da Vinci procedures +16%·FY26 +13.5~15.5% 상향. EW Q1 +12.7%·가이던스 +9~11% 상향. BSX 가이던스 +7.25% 하향. 삼성바이오 Q1 1.2571조(+26%)·OP 5,808억(+35%)·OPM 46.2% Lonza 2배. 셀트리온 Q1 1.1292조(+34.1%)·트룩시마 US 35.8% 1위(시밀러 관세 제외)** | **2027 MA rate +0.09%** Trump 제안→HUM/UNH -20% 폭락(2026-01). BIOSECURE Act 2025-12-18 Trump 서명(WuXi 2032 grandfather, $10-20B/yr 전환). IRA Part D 협상약 2026-01-01 발효 10개($6B/yr 절감). Trump MFN EO 2026-04-02 pharma 관세·16개사 자발 합의. BBBB Act Medicaid 삭감 CFO 1순위(66%) Safety-net -25~-30% 마진. HCA Q1 $19.1B 컨센(+4.3%)·가동률 73.2%(전년 76.9%). GEHC FY26 +3~4%·관세 영향 <$0.45. Tempus AI FY26 $1.59B(+25%)·Medtronic ALERT trial. 루닛 2025 831억(+53.4%)·뷰노 348억(+35%). Amazon Pharmacy 2026 미국인 45% 접근·현 19.7% | 04-24 | 05-24 | high |
| `food_agriculture.md` | **USDA WASDE 2026-04-09 옥수수 $4.15/bu·대두 $10.30/bu·밀 $5.00/bu 모두 상향·CBOT 밀 YoY+9.8%·옥수수 <$4.5/bu 4주최저. Cocoa 2024-12 $12,646/ton peak→2026E -6%·Arabica -13%·Sugar 공급과잉. Deere Q1 FY26 EPS $2.42(컨센 $1.92 beat, YoY-24%)·장비매출 $8B(+17.5%)·FY26 net income $4.5-5B 상향·관세 $1.2B·'사이클 바닥' 선언. CNH 2025 순익 $505M(-60%)·AGCO 상반기 underproduction. CF Q1 2026 EPS $2.08(상향)·MOS 브라질 EBITDA +190%·NTR potash 세계 1위. CTVA 2026 EPS $3.45-3.70·Bayer $610M 종자합의 면화진출. Bayer Roundup $7.25B 합의(21년 분할, 61K건 계류, 2026-04 대법원). Tyson Q1 FY26 $14.3B(+5.1%)·EPS $0.97 miss. GIS Q1 FY26 -7%·KHC -2.4% 가이던스 하향. K-Food 2025 수출 $12.3B 사상최고(+21.4% YoY, 라면 $1.38B)·삼양식품 3Q 누적 OP 3,850억 사상최대·농심 2.63조·라면 수출 60% 삼양. 한국 곡물자급률 19.5% 20% 마지노선 붕괴·밀 0.5%/옥수수 0.7%/대두 6.6%. 미중 2026-2028 대두 연 2,500만톤 구매 합의(10% 관세 유지)** | 2025 1~8월 미국→중국 대두 -78%·옥수수 -99% 붕괴. 브라질 대두 85Mt+ 중국 90% 점유. 인도 4년 밀 수출금지 해제(2026-02, 원밀 250만톤+제품 50만톤+설탕 50만톤). ENSO 2026-05~07 엘니뇨 61% 확률(IRI 70%)→인도 몬순 약화 리스크. 정밀농업 2031E $17.29B(CAGR 10.5%)·자율농기계 CAGR 15%+·DE LEAP 배터리전기 자율트랙터 2026 배치. 수직농장 2025 파산 14건·Plenty($1B) Ch11→2025-05 exit·Bowery($700M) 셧다운. BYND 2025 -15.6% $275.5M·자본잠식 -$784M·Nasdaq 상장폐지 경고 vs Oatly 첫 흑자 $862.5M. IPCC 농업 GHG 22%·No-tillage CO2 -47%·ICVCM 지속가능농업 탄소크레딧 첫 승인. FDA MAHA 2026 UPF 통일 정의·Front-of-pack 영양표시 의무화→GIS/KHC/MDLZ 규제압박. USDA 2026 net farm income $153.4B(-0.7% YoY). USDA 농산물 수출 2026E -$9B 적자 | 04-24 | 05-24 | high |
| `education.md` | **글로벌 에듀테크 2026 $404B·CAGR 16.3%(HolonIQ)·북미 38%/APAC 32%·K-12 40%·AI교육 +42% 최속. DUOL Q4 2025 $1.04B(+39%)·DAU 52.7M(+30%)·Paid 12.2M(+28%)·FY26 $1.20~1.22B(+15~18% 둔화)·2026 DAU 최우선 피벗 $50M 감수·1월 -20% 폭락. COUR Q1 2026 신규 7.6M 신기록 but FY26 $805~815M 재확인 주가 급락. CHGG 2025 매출 -36.7%·Q1 2025 subscribers -31%·2025-10 45%(388명) 감원·주가 2021 대비 -99%·$1 미만. LRN Q1 FY26 $620.9M(+13%)·Adj EPS $1.52(+39.4%)·FY26 $2.480~2.555B. 웅진씽크빅 2025 7,973억(-8.1%)·OP -104억 적자전환·2026 스마트올 AI+북스토리 B2G. 메가스터디 2026 매출·OP 회복·고등온라인 ASP 상승** | Trump 하버드 $2.3B 동결 2025-09 위법판결·세금면제 위협. 교육부 해체 EO 2025-03-20·학생대출 $1.7T 재무부 이관·SAVE plan 종료 7.5M 2026-07-01 90일내 RAP 전환·PSLF 해체. ChatGPT Edu 35+ 공립대·70만 라이선스·Cal State $17M·CU $2M·대학생 1/3 정기사용. Khanmigo GPT-4·Claude for Education·Gemini×Classroom 2026-02. 2U 2024-07 Ch11 파산 $800M edX+Trilogy 부채·OPM 약세·Coursera+Udemy 합병 2026H2. 한국 학령인구 47만·지방대 6:1 미만·등록금 190교 중 125교(65.8%) 인상 사립 80.8% vs 국공립 7.7%·의대 지역인재 강제. 패스트캠퍼스 기업출강 60% AI교육. Wiley Q3 FY26 EPS $0.97 beat·AI 매출 YTD $42M 전년초과·Pearson×AWS 2026-04-13. 엔터프라이즈 Upskilling Big3: LinkedIn Learning(21K 강좌) vs Coursera+Udemy 통합(2026H2) | 04-24 | 05-24 | high |
| `insurance.md` | **TRV Q1 2026 Beat(Core EPS $7.71 vs $7.07·CR 88.6%·Core ROE 19.7%·$2.2B 환원·배당 14% 인상 22년 연속)·PGR Q1 EPS $4.80(+10%)·CR 86.4%·Chubb Core EPS $6.82·CR 84%·TBVPS +21.5%·NA Casualty 가격 +9.6%. MET Q1 컨센 $2.21(+12.8%) 5/6 발표·PRU $3.34+1.5% 5/5 발표·POJ 사건 -$300~350M FY26 영향. 삼성화재(000810) 2025FY 2조183억 1위·Q1 2026 6,090억·CSM 14.33조·2028 주주환원율 50% 목표·DPS 19,000원 수익률 4.38%. DB Q1 4,027억(-28.4%, LA 산불)·현대해상 1,759억(-66.9%)·KB손보 CSM 9.4조 K-ICS 188%. 삼성생명 2025FY 2조3,028억(+9.3%, 역대최대)·보유CSM 13.2조·신계약 건강보험 75%(2024 58%→). Munich Re €13.7B(-7.8%)·Swiss Re P&C Re $15.3B(+6%) 소프트닝 사이클. Cat bond 2025 FY $25.6B(+45%) 사상최고·2025말 outstanding $61.3B·Q1 2026 $6.7B·UCITS펀드 $20B+. Cyber 2026E $16.4B(Swiss Re)~$23B(S&P)·CAGR 10%+ 2030. LMND Q1 4/29·FY26 IFP +30%·Adj EBITDA 흑자 Q4 목표·OSCR Q1 $850M+11%·MLR 82.5%** | **캘리포니아 산불 $30B+ 보험손실**(Palisades·Altadena)·State Farm $5B 지급·신규 중단·FAIR Plan $5~10K. 플로리다 4개사 축소. **NOAA/CSU 2026 대서양 허리케인 평균 이하**(13/6/2, El Niño 지배)→2027 재보험 추가 완화 가능. **1/1 갱신 소프트닝** Munich Re 가격 -2.5%·Swiss Re Net -4.6%, 4/1 추가 하락. **Trump ACA Marketplace Integrity Rule: 1.8M 커버리지 상실·2026 +3.4M/2027 +7.5M/2028 +8.7M 무보험자·2027 catastrophic coverage 본인부담 $27K 제안·2M 추가 포기**. **한국 기본자본 K-ICS 2026 도입**(EU Sol II/CA LICAT 50% 유력)·손해율 가이드라인 2026 Q2. Swiss Re sigma: Global premium 2026E +2.3%·Non-life +1.7%·Life +2.5%. Chubb CEO "dumb property softening" Casualty 하드닝 +9.6% vs Property -2.6% 분화. Korean Re(003690) 시총 $1.48B·목표 12,300원·1년 수익률 +65% | 04-24 | 05-24 | high |
| `real_estate.md` | **미국 Case-Shiller 20-City YoY +1.2%(2026-01, 2023-07 이후 최약세), 30Y FRM 6.30%, 기존주택 414만호(-2.4%), 신규착공 150만호(+11.2%), 공실률 오피스 22.5%(역대최고)/물류 8.2%(역대최고). 한국 BOK 2.50%(7연속동결), 서울아파트 +0.05%(17주 연속↑), PF연체율 4.25%(역대최고)·자기자본비율 7.1%, WGBI편입 채권유입** | 미국 CRE $1.5조 2026 만기(Wall). 오피스 공실 장기구조화 + AI 원격근무. 한국 PF 1차 옥석가리기→2차 지방부실 잔존. 고금리 장기화 → 거래절벽 지속. 서울 DSR·대출규제 vs WGBI 유입 | 04-22 | 05-22 | high |

> 상세 드릴다운: 각 파일의 § 섹션 번호 참조. 에이전트는 이 표로 파일 선택 후 해당 파일만 Read.
> [v3.5 신규 등재 — 04-13 wiki-linter]: quantum, space, smr, telecom_next, banking_capital, advanced_materials, battery, infrastructure
> [v3.6 재정비 — 04-21]: ai/auto/semiconductor/bio_pharma/defense_industry 5건 오전 + banking_capital/battery/infrastructure 3건 오후 갱신. ai_anthropic.md ai.md 흡수 삭제. 루트 redirect 3종 포맷 통일.
> [v3.7 신규 — 04-21 야간]: luxury.md 신규 (명품·면세 섹터 공백 해소). 총 industry KB 19개 체제.
> [v3.8 신규 — 04-22]: consumer_retail.md 신규 (소비재·유통·이커머스·편의점·K-뷰티·K-Food 공백 해소). 총 industry KB 20개 체제.
> [v3.9 신규 — 04-24]: logistics.md 신규 (해운·항만·물류자동화·콜드체인·트럭킹 공백 해소). 총 industry KB 21개 체제.
> [v3.10 신규 — 04-24]: healthcare_service.md 신규 (건강보험·병원·의료기기·디지털헬스·CRO/CDMO·정책 공백 해소). 총 industry KB 22개 체제.
> [v3.10.1 신규 — 04-24]: food_agriculture.md 신규 (곡물·비료·농기계·AgTech·식품가공·식량안보 공백 해소). 총 industry KB 23개 체제.
> [2026-04-24 신규]: education.md 신규 (에듀테크·온라인교육·대학·직업훈련·AI교육·교육출판 공백 해소). Industry KB 24 → 25개 체제.
> [2026-04-24 신규]: insurance.md 신규 (생명·손해·재보험·인슈어테크·Cat bond·Cyber·Trump ACA 공백 해소). Industry KB 25 → 26개 체제.
> [2026-04-26 wiki-linter]: real_estate.md 고아→등재 (부동산·REITs·PF·모기지). Industry KB 26 → 27개 체제.

---

## 🌍 Macro KB (`knowledge-base/macro/`)

| 파일 | 핵심 수치 | 핵심 리스크 | 갱신일 | 신뢰도 |
|------|---------|-----------|-------|-------|
| `us_economy.md` | **CPI 3.3%(에너지 주도), Core CPI 2.6%, ISM제조가격 78.3+서비스가격 70.7(양채널 극단), GDPNow Q1 +1.24%(추가하향), Fed 3.50~3.75%, 10Y 4.30%, DXY 98.53, S&P 7,165(신고가), VIX 18.53, 침체확률 30~49%, 소매판매3월 +1.7%, 미시간심리 49.8(최종/역대최저)** | 3중 인플레 파이프라인 지속. DOJ 파월수사 종료(4/24)+Warsh 인준 경로 개통. WTI $97+ 재급등(호르무즈 이중봉쇄). 4/30 Core PCE+GDP 더블이벤트. 소비심리 49.8 vs VIX 18.53 괴리 지속 | 04-25 | ✅ high |
| `us_monetary_policy.md` | **Fed 3.50~3.75%(2연속 동결), CPI 3.3%(에너지 주도), Core CPI 2.6%, Core PCE 3.0%, QT 종료, 대차대조표 $6.7T, 10Y 4.31%, DXY 97.70, 침체확률 30~35%** | 트럼프 파월 05/15 해임 위협. 이란전쟁 에너지 인플레. 인하 하반기 후반 전망. Fed 독립성 리스크 | 04-18 | ✅ high |
| `geopolitics.md` | **IEEPA 위헌→실효 34.7%**. WTI $97, Brent $105. Gold $4,700. 리스크 5/5. **무기한 휴전이나 나포전+기뢰 6개월** | **이란전쟁·호르무즈 봉쇄 장기화**(극고). 4.28 Section 301 공청회 당일. 북한 4월 4회(7번째). 대만 다축 에스컬레이션. 5.14~15 미중 정상회담 | 04-26 | ✅ high |
| `korea_economy.md` | **Q1 GDP +1.7%(5.5년최고 서프라이즈, YoY +3.6%), GDI +7.5%(38년최고), 4월1-20일 수출 $50.4B(+49.4% 역대최대), 반도체 $18.3B(+182.5%), 경상수지 2월 $23.2B(사상최대)+3월 초과 전망, KOSPI 6,481(4월+20%), 금리 2.50%(7연속동결), 신현송 4/21 취임(매파 유연), 원화 1,480~1,486, WGBI 3주 8.5조 유입, 삼성 Q1 OP 57.2조+SK하이닉스 37.6조(OPM 72%), 외국인 4월 순매수전환(5.8조), 현대+기아 Q1 관세부담 1.62조, KTB 10Y 3.816%** | 신현송 매파 전환(ING 7월 인상 가능). 원화약세 패러독스(경상흑자에도 NPS 해외투자). 외국인 3월 40.35조 순매도→4월 반전. 자동차 25% 관세(부품 4/30 발효). 반도체 관세 7월 확대 검토 | 04-25 | ✅ high |
| `global_risk_factors.md` | **VIX 19.31(거짓안정 일부해소), F&G 70(Greed심화), DXY 98.52(반등), Gold $4,709(구조적Bull 조정), Brent $105, WTI $97(+15%w), 원달러 1,476, 소비심리 49.8(최종/역대최저), IMF 3.1%(하향), 침체확률 27~35%(하향), 10Y 4.32%, SOX 18일연승(역대최장), BTC $78K** | 호르무즈 기뢰전 격상(나포31척+격침명령+펜타곤6개월). 4/30 트리플폭탄(GDP+PCE+MSFT/META). Section 301 공청회 4/28. 대만 다축에스컬레이션. 사이버리스크 히트맵 추가 | 04-26 | ✅ high |
| `political_cycle.md` | **Section 122 10%(07.24만료)+Section 301 이중조사(강제노동4/28+과잉설비5/5), Warsh 인준 전진(DOJ 수사 종료 4/24), FOMC 3.50~3.75%(동결99.5%), 이란 협상 교착(특사 취소4/25), 한국 지지율65.5%/지방선거 민주압승/고유가지원금4/27개시, KOSPI 6475(4월+26.4% G20 1위), 밸류업590사+99사소각, 미중 Daines방중5/1+정상회담5/14~15, ECB 인상50%혼조(4/29), BOJ 7월1.0%, 인도FDI+22%/한-인도$50B, EU AI Act 8/2시행, CHIPS Act TSMC 12팹확장, 재정적자$1.853T/X-date 8월** | Section 301 이중공청회 결과→차등관세 체제 전환. Warsh QT가속 선호→유동성 축소 리스크. 이란 협상 교착→호르무즈 장기화. 한국 민주 압승+밸류업 실행→KOSPI 지속 상승. ECB 인상 전환 가능성 50% | 04-26 | ✅ high |
| `tech_breakthrough.md` | **AI: Claude Opus 4.7(4/16), Agentic AI 97% 기업 배포(대중화 승격), EU AI Act 고위험 2027.12 연기. 반도체: TSMC N2 수율 65%·N2P H2, imec High-NA Q4 인증, Alphabet TPU CoWoS 병목. 에너지: CFS $863M 추가, Samsung SDI 전고체 파일럿. 양자: NVIDIA Ising QEC. 우주: NG-3 부스터 재사용. 바이오: 소형 CRISPR. 신소재: 그래핀-페로브스카이트 3,670h 안정성** | G-3 모듈 정상 운영. 8개 서브섹터 주간 갱신 완료 | 04-19 | ✅ high |
| `supply_chain.md` | **WCI $2,232(-1%), WTI $97(주간+17%)/Brent $105, 구리 $13,200(관세50%), DDR5 +63%/NAND +75%(Q2), HBM4양산+VeraRubin독점, 요소비료 $702(재봉쇄반등YTD+82%), Gartner 반도체 $1.3T(+26%), MATCH법안 외교위통과(4/22), Section 301 대체구도(7/24 전 완료), 제약100%** | **호르무즈 이중봉쇄 해군대치(4/17~23, 이란 선박나포, 통항 8척/일)**. 삼중 인플레 재강화. Section 301 공청회 4/28. 사이버공격 5년4배. 한국 요소비축방출+핵심광물기금 2,500억 | 04-25 | ✅ high |

---

## 📊 Market KB (`knowledge-base/market/`) — 2026-04-21 전면 갱신 완료

| 파일 | 상태 | 갱신 빈도 | 영향 브리핑 모듈 | 재수집 명령 |
|------|------|----------|---------------|-----------|
| `daily_snapshot.md` | ✅ SUCCESS (04-26) valid_until 04-28 confidence:high | 매 거래일 | A-1, B-2, B-3 | 04-28 재실행 |
| `economic_calendar.md` | ✅ SUCCESS (04-26) valid_until 05-02 confidence:high | 주 1회 | A-4, B-1, C-6 | — |
| `surprise_index.md` | ✅ SUCCESS (04-26) valid_until 05-26 | 매일 | B-4 | — |
| `correlation_matrix.md` | ✅ SUCCESS (04-26) valid_until 05-26 | 주 1회 | B-5 | — |
| `guru_positions.md` | ✅ SUCCESS (04-18) valid_until 07-18 confidence:high | 분기 1회 | A-5, B-7, C-4 | Q1 2026은 05-15 이후 |

> **재수집 순서 권장:** economic_calendar → surprise_index → correlation_matrix → guru_positions (13F)
> daily_snapshot은 fetch_price.py --market --save로 매일 자동 갱신

---

## 💰 Portfolio KB (`knowledge-base/portfolio/`)

| 파일 | 상태 | 갱신 주체 | 비고 |
|------|------|---------|------|
| `model_portfolios.md` | ✅ 갱신 완료 (04-21) confidence:high | briefing-lead | F-1 환경진단+F-2~F-5 비중·종목+F-6 비교표+F-7 면책 전면 작성. 다음 갱신: `/주간리포트` 실행 시 |
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
| `semiconductor_2026.jsonl` | 107건 (+36 @2026-04-21) | kb-updater |
| `ai_2026.jsonl` | 120건 (+26 @2026-04-21) | kb-updater |
| `auto_2026.jsonl` | 78건 (+32 @2026-04-21) | kb-updater |
| `energy_2026.jsonl` | 132건 (+26 @2026-04-26) | kb-updater |
| `geopolitics_2026.jsonl` | 91건 (+25 @2026-04-26) | kb-updater |
| `science_tech_2026.jsonl` | 435건 (quantum/space/smr/biotech/eda/cybersecurity subtag 포함, +18 @2026-04-26 deep) | kb-updater |
| `bio_pharma_2026.jsonl` | 72건 (+38 @2026-04-21) | kb-updater |
| `macro_2026.jsonl` | 436건 | kb-updater |
| `banking_capital_2026.jsonl` | 95건 (+31 @2026-04-24, Q1 2026 실적 반영) | kb-updater |
| `advanced_materials_2026.jsonl` | 141건 (+58 @2026-04-25 전면 재구성) | kb-updater |
| `battery_2026.jsonl` | 110건 (+70 @2026-04-21) | kb-updater |
| `infrastructure_2026.jsonl` | 62건 (+39 @2026-04-21) | kb-updater |
| `capex_2026.jsonl` | 40건 (+19 @2026-04-25 deep 갱신) | kb-updater |
| `telecom_next_2026.jsonl` | 125건 (+62 @2026-04-25 deep 갱신) | kb-updater |
| `robotics_2026.jsonl` | 29건 (신규 생성 2026-04-19) | kb-updater |
| `crypto_bitcoin_2026.jsonl` | 48건 (신규 생성 2026-04-20) | kb-updater |
| `defense_2026.jsonl` | 25건 (신규 생성 2026-04-21) | kb-updater |
| `luxury_2026.jsonl` | 52건 (신규 생성 2026-04-21 야간) | kb-updater |
| `consumer_retail_2026.jsonl` | 31건 (신규 생성 2026-04-22) | kb-updater |
| `logistics_2026.jsonl` | 29건 (신규 생성 2026-04-24) | kb-updater |
| `food_agriculture_2026.jsonl` | 57건 (신규 생성 2026-04-24) | kb-updater |
| `insurance_2026.jsonl` | 72건 (신규 생성 2026-04-24) | kb-updater |
| `education_2026.jsonl` | 42건 (신규 생성 2026-04-24) | kb-updater |
| `changelog_2026.jsonl` | 66건 (+1 @2026-04-25: quantum deep 갱신) | kb-updater |
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
| 미국 Fed 금리 | `us_monetary_policy.md` (루트): redirect 포인터 (수치 없음) | `macro/us_monetary_policy.md`: 3.50~3.75% (04-18 갱신) | 04-26 | SSOT 일치 |
| VIX | `macro/global_risk_factors.md`: 19.31 (04-26 갱신) | `market/daily_snapshot.md`: ~18.71 (04-25 기준) | 04-26 | ✅ 일치 (시점차 허용범위 — daily_snapshot 04-25, global_risk 04-24 기준) |
| DXY | `macro/global_risk_factors.md`: 98.52 (04-26 갱신) | `market/daily_snapshot.md`: ~98.51 (04-25 기준) | 04-26 | ✅ 일치 (차이 0.01, 허용범위 이내) |
| 원/달러 | `macro/korea_economy.md`: 1,480~1,486원 (04-25) | `macro/global_risk_factors.md §2`: 1,476원 (04-26) | 04-26 | ✅ 일치 (시점차 허용범위 이내) |
| S&P 500 | `macro/us_economy.md`: 7,165(신고가, 04-25) | `market/daily_snapshot.md`: 7,165.08 (04-25 확정) | 04-26 | ✅ 일치 (동일 수치) |
| WTI | `industry/energy.md`: $94.88 (04-26 갱신) | `macro/geopolitics.md`: $97 (04-26 주간 최고) | 04-26 | ✅ 일치 (daily_snapshot 04-25 기준 $94.88, 범위 내) |
| Gold | `macro/global_risk_factors.md §4`: $4,709 (04-26 갱신) | `market/daily_snapshot.md`: ~$4,708.8 (04-25 기준) | 04-26 | ✅ 일치 (차이 $0.2, 허용범위 이내) |

---

## 🏗️ 섹터-종목 빠른 매핑

| 종목/테마 | 1차 KB | 2차 KB (맥락) |
|---------|-------|-------------|
| 삼성전자, SK하이닉스, 한미반도체 | `industry/semiconductor.md` | `macro/geopolitics.md §1`, `macro/korea_economy.md §5-1` |
| NVIDIA, AMD, 브로드컴 | `industry/ai.md §2` | `industry/semiconductor.md §3` |
| Anthropic, OpenAI, Google AI, Meta AI | `industry/ai.md §4` (Anthropic 섹션 포함) | `macro/geopolitics.md §1-2` |
| 현대차, 기아 | `industry/auto.md §3-2` | `macro/geopolitics.md §1-1` (관세) |
| LG에너지솔루션, 삼성SDI, SK온 | `industry/auto.md §6` | `macro/korea_economy.md §5-3` |
| 한화에어로(012450), 현대로템(064350), LIG넥스원(079550), KAI(047810) | `industry/defense_industry.md §2` | `macro/geopolitics.md §4, §5, §8`, `industry/space.md` |
| LMT, RTX, NOC, GD, BA, KTOS | `industry/defense_industry.md §3` | `macro/political_cycle.md`, `macro/geopolitics.md` |
| Rheinmetall, BAE Systems, Dassault, Leonardo | `industry/defense_industry.md §4` | `macro/geopolitics.md` (NATO 3%) |
| 두산에너빌리티, 한수원 | `industry/smr.md §2, §4` | `industry/energy.md §7` |
| 클로봇, 레인보우로보틱스, 두산로보틱스, Figure AI, Tesla Optimus, Agility, 1X | `industry/robotics.md §2, §4` | `industry/ai.md §2` (NVIDIA Jetson), `macro/korea_economy.md` (정부지원) |
| LVMH, Kering, Hermès, Richemont, Burberry | `industry/luxury.md §2, §3` | `macro/us_economy.md §1` (소비), `macro/geopolitics.md §1-2` (중국/관세) |
| 호텔신라(008770), 롯데쇼핑(023530), 현대백화점(069960), 신세계(004170), 신세계인터(031430), 아모레퍼시픽(090430), LG생활건강(051900) | `industry/luxury.md §4` | `macro/korea_economy.md §5-4` (내수·관광) |
| Estée Lauder(EL), Tapestry(TPR), Capri(CPRI), Ralph Lauren(RL), 시세이도(4911.T) | `industry/luxury.md §3, §5` | `macro/us_economy.md §1` |
| Walmart(WMT), Costco(COST), Target(TGT), Procter&Gamble(PG), Coca-Cola(KO), Amazon(AMZN) | `industry/consumer_retail.md §2` | `macro/us_economy.md §1` (소비), `macro/geopolitics.md §1-2` (관세) |
| 이마트(139480), 롯데쇼핑(023530), 신세계(004170), CJ제일제당(097950), 농심(004370), 삼양식품, 오리온(271560) | `industry/consumer_retail.md §3, §4` | `macro/korea_economy.md §5-4` (내수·유통) |
| BGF리테일(282330, CU), GS리테일(007070, GS25), 세븐일레븐, 이마트24 | `industry/consumer_retail.md §6` | `macro/korea_economy.md §5-4` |
| 쿠팡(CPNG), Shein, Temu(PDD), Alibaba 알리익스프레스 | `industry/consumer_retail.md §5` | `macro/geopolitics.md §1` (중국 관세 145%) |
| 코스알엑스, VT, 아누아, 파우더룸 (K-뷰티), LG생활건강(051900), 아모레(090430) | `industry/consumer_retail.md §7.1` | `industry/luxury.md §4`, `macro/korea_economy.md §5-4` |
| HMM(011200), 팬오션(028670), 대한해운(005880) | `industry/logistics.md §1.4` | `macro/supply_chain.md`, `industry/energy.md`, `macro/geopolitics.md` (호르무즈) |
| CJ대한통운(000120), 한진(002320), 대한항공 화물(003490) | `industry/logistics.md §6, §9` | `industry/consumer_retail.md §5` (쿠팡), `macro/korea_economy.md §5` |
| Symbotic(SYM), KION Group, Daifuku(6383.JP), Amazon Robotics | `industry/logistics.md §5` | `industry/robotics.md`, `industry/ai.md` |
| FedEx(FDX), UPS, DHL, Union Pacific(UNP), CSX, NSC, ODFL, JBHT, XPO | `industry/logistics.md §3, §4, §7` | `macro/political_cycle.md` (관세), `macro/supply_chain.md` |
| 삼성바이오, 셀트리온 | `industry/bio_pharma.md` | `macro/korea_economy.md §5-5` |
| UnitedHealth(UNH), Elevance(ELV), Humana(HUM), Centene(CNC), CVS Health(CVS) | `industry/healthcare_service.md §1` | `macro/political_cycle.md` (BBBB·MFN), `macro/us_economy.md §3` |
| HCA Healthcare(HCA), Tenet(THC), Universal Health(UHS) | `industry/healthcare_service.md §2` | `macro/political_cycle.md` (Medicaid 삭감), `macro/us_economy.md` |
| Intuitive Surgical(ISRG), Stryker(SYK), Edwards(EW), Boston Scientific(BSX), GE HealthCare(GEHC), Medtronic(MDT), Abbott(ABT) | `industry/healthcare_service.md §3` | `industry/robotics.md` (수술로봇), `industry/ai.md` (AI 진단) |
| Hims&Hers(HIMS), Teladoc(TDOC), Doximity(DOCS), Tempus AI(TEM), Veeva(VEEV) | `industry/healthcare_service.md §4` | `industry/ai.md §2` (Tempus EHR 통합) |
| IQVIA(IQV), Labcorp(LH), Quest(DGX), Lonza, Catalent, 삼성바이오(207940), 셀트리온(068270) | `industry/healthcare_service.md §6` | `industry/bio_pharma.md`, `macro/geopolitics.md §1` (BIOSECURE) |
| 루닛(328130), 뷰노(338220) | `industry/healthcare_service.md §3.6` | `industry/ai.md`, `macro/korea_economy.md §5-5` |
| Duolingo(DUOL), Coursera(COUR), Chegg(CHGG), Stride(LRN), Udemy(UDMY) | `industry/education.md §2` | `industry/ai.md §2` (ChatGPT·Claude 영향), `macro/us_economy.md §3` |
| 메가스터디(215200), 웅진씽크빅(095720), 대교(019680) | `industry/education.md §3` | `macro/korea_economy.md §5` (학령인구), `industry/ai.md` (AI 학습지) |
| ChatGPT Edu(OpenAI), Claude for Education(Anthropic), Khanmigo, Gemini×Classroom(GOOG) | `industry/education.md §7` | `industry/ai.md §1` (LLM 경쟁), `industry/ai.md §4` |
| LinkedIn Learning(MSFT), Coursera for Business, Udemy Business, 패스트캠퍼스 | `industry/education.md §6` | `macro/political_cycle.md` (Trump 학자금 정책), `industry/ai.md` |
| Wiley(WLY), Pearson(PSON), McGraw Hill | `industry/education.md §8` | `industry/ai.md §2` (AI 콘텐츠 라이선싱) |
| Gold, TLT, IAU | `macro/global_risk_factors.md §4` | `macro/us_monetary_policy.md` |
| BTC, ETH, SOL | `industry/crypto_bitcoin.md §1, §6` | `macro/global_risk_factors.md §2`, `market/daily_snapshot.md` |
| MSTR (Strategy), COIN, HOOD, MARA, RIOT, CLSK | `industry/crypto_bitcoin.md §2, §4, §8` | `industry/ai.md` (MARA AI DC 피벗), `macro/us_monetary_policy.md` |
| NuScale, Oklo, BWXT | `industry/smr.md §2` | `macro/tech_breakthrough.md §5` |
| 빅테크 CapEx, TSMC, ASML | `industry/capex.md §1, §2` | `industry/ai.md §3`, `industry/semiconductor.md` |

---

## 📝 KB 업데이트 이력 (최근 10건)

| 날짜 | 파일 | 변경 | 레코드 |
|------|------|------|-------|
| 2026-04-26 | `industry/science_tech.md` | **과학기술 메타 섹터 deep 갱신(16회 검색)** -- 양자: IBM Heron R2 QEC 10x(1년 앞당김)+IonQ FT 99.99%+PQC $29.95B(2034E)+Xanadu +51%. 바이오: Lilly Foundayo 경구GLP-1 FDA승인(04월)+Insilico-Lilly AI신약 $2.75B. 우주: Falcon9 600착(04-19)+Starship V3 정적점화+2026 250회 궤도발사. 로보틱스: Optimus V3 중반데뷔 확정(04-23)+Figure02 BMW 30K차 1,250hr+Agibot 1만대. SMR/핵융합: CFS SPARC late2026~2027(소폭후퇴)+Helion 외부연구$4M(25개프로젝트). EDA: Siemens Fuse AI Agent 3파전+AI EDA $4.27B. 사이버보안: Glasswing 40개+기관 확대+04-10 섹터 7~14%급락. CapEx: $635~665B(+67~74%) 구체화. 디스플레이: OLED $76.82B+UDC 청색PHOLED. 전고체: QS Eagle Line+SDI 500Wh/kg. R&D: 한국 35.5조(+19.9%)+OECD GBARD -4.1% | +18 |
| 2026-04-26 | `macro/tech_breakthrough.md` | **8개 서브섹터 주간 갱신** -- AI: GPT-5.5 출시(4/23, 옴니모달/SOTA 14개), Claude Mythos Preview(SWE-bench 93.9%), 토큰비용 1,000x 하락, Agentic AI $10.91B(ROI 171%). 반도체: TSMC N2 수율 70%, Intel 18A High-NA 프로덕션, Samsung 2nm High-NA 2대 배치. 에너지: CFS SPARC 자석설치/2027 Q>1, Helion 발전소 건설, Linglong One SMR 상업운전. 바이오: Foundayo 경구GLP-1 FDA승인(4/1), CRISPR-GLP1 전임상 돌파(오사카대). 양자: IonQ $130M/$225-245M, Quantinuum $20B IPO. 로봇: 중국+94%/AgiBot 10K, Figure03 24/7자율. 우주: Starship V3 5월지연, FCC D2D인가(4/22). 신소재: 그래핀-페로브스카이트 30.6%/Wolfspeed 300mm SiC | +29 |
| 2026-04-26 | `industry/energy.md` | **에너지 섹터 deep 갱신** -- Brent $105+(4일연속), WTI $94.88. Brent-WTI 스프레드 $10~15 확대. 트럼프 특사 취소(4/25 협상 결렬). IEA 역대최대 공급차질(-10.1Mbpd)+수요 -80Kbpd(팬데믹 이후 첫). SPR 22.46Mbl 방출(정책전환)+스왑20M+bl(4~5월). 정유 가동률 65~70%. 정제마진 $44.9(역대급). 석화 불가항력 지속(마진 회복 조짐). Henry Hub $2.52(최저). LNG +10% YoY(Golden Pass 첫생산+NFE). X-Energy IPO $1.02B(원자력 역대최대). SMR 파이프라인 45GW. 한화솔 OP 6,157~8,829억(흑자전환). 두산엔 OP 컨센 1.1조+첫계약3,200억. 에너지 대전환 추진계획(4/6) | +26 |
| 2026-04-26 | `macro/political_cycle.md` | **정치 사이클 주간 deep 갱신** -- Section 301 공청회 일정 정정(강제노동4/28, 과잉설비5/5). Warsh 인준 전진(DOJ 수사 종료 4/24). FOMC 동결99.5%. 이란 협상 교착(특사 취소4/25). 한국 지지율65.5%(최고)/지방선거 민주압승/고유가지원금4/27개시/밸류업590사+99사소각/KOSPI 6475(+26.4% G20 1위). 미중 Daines방중5/1. ECB 인상50%혼조. BOJ 7월1.0%. 인도FDI+22%/한-인도$50B. EU AI Act 8/2시행. CHIPS Act TSMC 12팹확장. 재정적자$1.853T/X-date 8월. OBBB실질효과 상쇄 | +22 |
| 2026-04-26 | `macro/global_risk_factors.md` | **글로벌 리스크 맵 주간 deep 갱신** -- 호르무즈 기뢰전 격상(나포31척+격침명령+6개월장기화). WTI $97/Brent $105(+15~17%w). VIX 19.31(거짓안정 일부해소). F&G 70(탐욕심화). 소비심리 49.8 최종(역대최저). DXY 98.52. 원달러 1,476. 10Y 4.32%(5일연속상승). Gold $4,709(-3.2%w, 구조적Bull, 3대IB $5K+). BTC $78K. GDPNow 1.24%. 침체확률 하향(27~35%). SOX 18일연승(역대최장). Intel +24%. 대만 다축에스컬레이션. 사이버리스크 히트맵 추가. 4/30 트리플폭탄 분기점 | +24 |
| 2026-04-26 | `macro/geopolitics.md` | **4개 서브섹터 deep 갱신**(미중관세/대만/중동/북한) -- 4.21 무기한 휴전 연장이나 4.22 나포전+4.24 기뢰 격침 명령. WTI $97(+17%w)/Brent $105(+16%w). 펜타곤 기뢰 제거 6개월. IEEPA 환급 CAPE 4.20 가동. Section 122 합헌성 4.10 심리. 4.28 강제노동 공청회 당일. Bessent 7월 IEEPA 수준 301 복원 발언. 5.14~15 미중 정상회담 확정. 랴오닝 4.20 대만해협 통과+라이칭더 영공차단(역사상 첫)+간첩17명+봉쇄돌파훈련+일본 살상무기 규제완화. TSMC Q1 $35.9B(+40.6%)+CapEx $56B. 북한 4월 4회(2026 7번째) 집속탄+EMP+구축함. 러 파병 15K. 김주애 후계자 시그널. 리스크 5/5 극고 유지 | +19 |
| 2026-04-25 | `industry/capex.md` | **5개 서브섹터 deep 갱신**(빅테크AI/반도체/통신/에너지유틸리티/한국대기업+CapEx사이클) -- 하이퍼스케일러4사 $635-665B(+67~74%, 기존 5사 $660-690B 유지). MSFT FY26 $110-150B(Q2 $37.5B, Azure+39%, CRPO $625B+110%, 미이행$80B). GOOGL $175-185B(Cloud백로그$240B, +50%+). META $115-135B(미국$600B/2028, FCF-90%). TSMC Q1 $35.9B 실적(GM66.2%/OPM58.1%/순익+58%) CapEx $56B상단. Intel 18A HVM진입 $15B백로그+Tesla Terafab+CHIPS $8.9B+Q1 EPS+2800%. SK하이닉스 19조패키징(+30%)+HBM4 70%. 삼성 110조+(TSMC초과)+HBM50%증산. 한국4대그룹 800조 공약. 유틸리티$1.4T(+27%). DC전력 신규50%. GS AI ROI $1T필요 vs $450B컨센. 부채$1.5T. DC지연24-72개월 | +19 |
| 2026-04-25 | `industry/advanced_materials.md` | **6개 서브섹터 전면 재구성**(CNT/그래핀/초전도체/SiC-GaN-세라믹/희토류/첨단소재정책) -- 기존 MicroLED/EDA/반도체소재 구조에서 탈피. CNT 시장 4.85~8.8B(LG화학 6,100t/금호 360t/OCSiAl SWCNT 90%). 그래핀 1.96~2.91B(Georgia Tech FET 전자이동도 Si 10배/그래핀스퀘어 EUV 펠리클 2027). 초전도체 8.16~10.6B(LK-99 반박 확정/핵융합 HTS 30만km/한국 16T 시험시설 2026.06). SiC 5.32~6.16B(Wolfspeed 파산·중국 $500 덤핑/Infineon 200mm). GaN파워 CAGR 44%(Infineon 8" 전환/Navitas Q1+58%). 희토류 Nd YoY+107%·Dy FOB+67%(중국 12원소 통제 유예~2026.11/MP Materials DoD $400M+Apple $500M/EU RESourceEU). 정책: CHIPS Act 48D 만료예정/EU CRM Act+Advanced Materials Act 2026/한국 소부장 2030 자립 50% | +58 |
| 2026-04-25 | `industry/telecom_next.md` | **6개 서브섹터 deep 갱신**(6G/5G Advanced/Open RAN/위성통신-NTN/AI-RAN/한국통신사투자) -- ITU IMT-2030 TPR 20개 확정(2026.02), 3GPP Rel-21 2026.06 타임라인 결정점, Starlink Mobile 리브랜딩(월 1000만/연말 2500만), AST BlueBird7 궤도실패(04.19 New Glenn), Amazon Leo 엔터프라이즈 베타(04.08) FCC 1618기 의무 미달(~241기), AI-RAN $3.81B 시장(CAGR 29%), NVIDIA Aerial 오픈소스+AI-RAN Alliance 100+사(MWC2026 33개 데모 26개 NVIDIA), Open RAN 5%->28%(2029) AT&T-Ericsson $14B+Samsung-Vodafone 53K사이트, 5G SA 의무화+주파수 재할당 3.1조, SKT-삼성 AI-RAN 공동연구+SKT AI 네이티브 선언+SKT-도코모 백서, 한국 6G 예산 1067억 증액+K-OTIC 인증체계, Nokia QKD 인수, 6G 표준 fork 리스크 현실화(중국 vs 서방), Deutsche Telekom Starlink Mobile 유럽 10국 계약 | +62 |
| 2026-04-25 | `industry/quantum.md`, `industry/science_tech.md` | **양자 4개 서브섹터 deep 갱신** -- IonQ SkyWater $1.8B 인수(수직통합), Quantinuum IPO S-1 Honeywell 확인($20B+), CISA PQC 연방조달 의무화, Google PQC 2029 타임라인, Meta 6단계 PQC 프레임워크, QuEra 2:1 QEC(04-20), 양자주 7거래일 IonQ+72%(P/S 경고), 한국 양자클러스터 공모(04-17), 양자센서 국방 40.25% | +23 |

```
질문 유형별 1차 참조 파일:

"삼성전자 실적은?" → industry/semiconductor.md §2 한국 반도체
"Fed 금리 전망?" → macro/us_monetary_policy.md
"오늘 시장 상황?" → market/daily_snapshot.md ✅ 2026-04-21 갱신
"미중 관세 영향?" → macro/geopolitics.md §1-1
"AI 투자 동향?" → industry/ai.md §3 CapEx
"Anthropic 현황?" → industry/ai.md §4 Anthropic (ai_anthropic.md는 2026-04-21 ai.md로 흡수 삭제)
"한국 방산 투자?" → macro/geopolitics.md §4, §5, §8
"지정학 리스크?" → macro/global_risk_factors.md §1 Top5
"포트폴리오 구성?" → portfolio/model_portfolios.md ⚠️ 현재 미수집
"SMR/원자력 투자?" → industry/smr.md §2 기업현황, §5 빅테크 DC
"두산에너빌리티?" → industry/smr.md §4 한국 관련
"설비투자/CapEx?" → industry/capex.md §1 빅테크, §2 반도체, §7 한국
"명품·면세 투자?" → industry/luxury.md §2 글로벌 4대, §4 한국 면세 (008770/069960 수혜)
"에듀테크·AI교육 투자?" → industry/education.md §2 미국 상장사 (DUOL/COUR/CHGG/LRN), §7 AI기반 교육
"한국 에듀테크·학령인구?" → industry/education.md §3 한국 (메가스터디/웅진씽크빅), §5 한국 대학·지방대 구조조정
"Trump 교육정책·학자금?" → industry/education.md §4.3 교육부 해체 EO, §4.4 SAVE plan 종료
"중국 소비 둔화 영향?" → industry/luxury.md §5 중국 (LVMH/Kering 타격 vs Hermès 방어), §6 메가트렌드
```

> **에이전트 원칙:** 이 인덱스로 대상 파일 특정 → 해당 파일만 Read → 분석 완료 후 인사이트를 "최근 핵심 인사이트" 섹션에 1줄 append (briefing-lead만).
