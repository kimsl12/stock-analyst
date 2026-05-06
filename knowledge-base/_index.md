---
updated: 2026-05-06
version: v3.2
maintainer: wiki-linter (자동) + briefing-lead (수동)
lint_last_run: 2026-05-03
lint_last_post_fix: 2026-05-06
lint_mode: full
---

# Knowledge Base Index — Wiki Master Index

> **목적:** 에이전트가 이 파일 하나만 읽으면 전체 KB 구조, 핵심 인사이트, 건강 상태를 파악할 수 있어야 한다.
> **갱신 주체:** wiki-linter (자동 갱신, 주 1회) + briefing-lead (브리핑 종료 시 인사이트 append)
> **활용법:** 에이전트는 질의 전 이 파일을 먼저 읽고, 필요한 파일만 드릴다운한다. Glob 탐색 금지.

---

## P0 — 즉시 조치 필요 (FAILED / 만료)

> wiki-linter가 탐지한 긴급 항목. 브리핑 실행 전 반드시 확인.
> **최종 갱신: 2026-05-03 (wiki-linter full)**

| 파일 | 상태 | 영향 모듈 | 조치 |
|------|------|----------|------|

> [INFO] P0 항목 없음 — 2026-05-03 wiki-linter full 점검 결과 FAILED/만료/confidence:none/빈 테이블 탐지 없음. 브리핑 실행 가능.
> [INFO] market/daily_snapshot.md 2026-05-06 모닝 수집 완료 — 5/5 종가 확정: S&P 7,259.22(+0.81%), AMD Q1 어닝서프라이즈(EPS $1.37), ISM 서비스 PMI 53.6(가격 70.7), 이란 협상 대화 지속(데드라인 무사 통과), WTI $102.27(-3.9%). 아시아 5/6 재개장.

---

## P1 — 이번 주 조치 (탐지: 2026-05-03 full)

> wiki-linter P1 탐지 결과. 브리핑 실행 가능하나 이번 주 내 처리 권장.

| 파일 | 문제 | 심각도 | 권장 조치 |
|------|------|-------|---------|
| `macro/us_monetary_policy.md` | 2026-04-18 갱신 — 4/29 FOMC(4인 반대, 역사적 분열) + Warsh 5/15 취임 반영 안됨. valid_until 05-18이나 핵심 수치(Core PCE 3.0%→4.3%, 동결 확률 갱신 필요) 구버전 | 중간 | kb-updater에 재수집 위임. FOMC 4/29 결과·Core PCE 4.3%·Warsh 5/15 취임 반영 |
| `korea_economy.md` (루트) | 2026-04-07 데이터 — valid_until 2026-05-07(4일 후 만료 예정). 원/달러 1,410원 등 최신치 대비 구버전 | 중간 | `macro/korea_economy.md` SSOT 유지. 루트 파일 redirect 포인터 교체 또는 삭제 권장 |
| `market/surprise_index.md` | collection_status: PARTIAL — 일부 지수 미수집. updated 05-02이나 완전 수집 미달 | 낮음 | 다음 갱신 시 완전 수집 목표. 브리핑 사용 가능하나 주의 |
| `knowledge-db/` 미등재 파일 3종 | `quantum_2026.jsonl`(17건), `real_estate_2026.jsonl`(26건), `healthcare_service_2026.jsonl`(47건) — _index.md 시계열 DB 표 미등재 | 낮음 | _index.md 시계열 DB 섹션에 추가 ✅ 2026-05-03 완료 |
| `knowledge-db/` 레코드 수 불일치 5종 | `science_tech_2026.jsonl`(표기 435→실제 492, +57), `macro_2026.jsonl`(713→733, +20), `telecom_next_2026.jsonl`(147→158, +11), `insurance_2026.jsonl`(72→73, +1), `changelog_2026.jsonl`(92→95, +3) | 낮음 | _index.md 레코드 수 현행화 ✅ 2026-05-03 완료 |
| `market/daily_snapshot.md` | 2026-05-06 모닝 수집 완료. valid_until 2026-05-06 EOD | 없음 | 5/6 이브닝 갱신 권장 |

> [P1 해결완료 2026-04-21 오전] industry/bio_pharma.md 신규 생성, industry/semiconductor.md 신규 생성 + 루트 semiconductor.md 삭제(구조 통일), industry/ai.md + industry/auto.md 갱신 (kb-updater 4건 병렬).
> [P1 해결완료 2026-04-21 오후] 루트 redirect 파일 3종(geopolitics.md, global_risk_factors.md, us_monetary_policy.md) 본문 삭제 + SSOT 포인터 포맷 통일. 구 데이터 잔존 문제 해소 — 실제 브리핑·분석은 모두 macro/ SSOT 사용 중임을 전수 조사로 검증(lead_*.md 0건 루트 참조). wiki-linter 교차참조 맵은 유지(SSOT 대조 용도).
> [P1 정상] industry/ 전체 고아 파일 없음 (**27개** 파일 모두 _index.md 등재 확인). real_estate.md(04-26 등재) 포함.
> [P1 해결완료 2026-05-03] knowledge-db/ 미등재 파일 3종 + 레코드 불일치 5종 갱신 완료 (wiki-linter full).
> [P1 해결완료 2026-05-06 후속 복구] 5/3 wiki-linter 누락분 전부 복구 — (1) 교차참조 맵 7행 04-26→05-06 기준 재검증 (VIX 19.31→16.89, Gold $4,709→$4,614, 원달러 1,476→1,473.21, S&P 7,165→7,259.22 등), (2) macro/global_risk_factors.md last_updated 04-26→05-03, (3) Market KB 헤더 05-03→05-06 동기화. lint_last_post_fix 필드 추가.

---

## ⚡ 최근 핵심 인사이트 (지난 7일 — briefing-lead append)

| 날짜 | 출처 | 인사이트 | 관련 KB | 제안 상태 |
|------|------|---------|--------|---------|
| 2026-05-06 | 주간리포트 | "골디락스 표면, 스태그플레이션 이면" — GDP +2.3% Beat + Core PCE MoM 0.0% vs FOMC 8-4 분열 + ISM 가격 84.6%(4년 최고). 이중 구조 고착. 5/12 CPI가 최종 판별자 | `market/daily_snapshot.md, macro/us_economy.md` | 진행중 |
| 2026-05-06 | 주간리포트 | 적중률 77.8%(7/9) 첫 산정 — TLT Bear·SK하이닉스 Bull·반도체 ETF Bull·IGV Bear 적중. VIX 단기 예측·트리플 폭탄 Bear 오류. 중기 구조적 판단 > 단기 이벤트 예측 교훈 | `performance/2026_hit_rate.md` | — |
| 2026-05-06 | 주간리포트 | 시나리오 #6(트리플 폭탄) 종결: A(골디락스) 실현(확률 30% 과소평가 → 오류 판정). 신규 #7(5/12 CPI) 설정: A 25%/B 50%/C 25%. ISM 84.6% 선행 경고 | `performance/2026_scenario_tracking.md` | — |
| 2026-05-06 | 주간리포트 | UAE OPEC 탈퇴(5/1) 3차 효과 미반영 — 호르무즈 정상화+UAE 증산 동시 시 Brent $70대 급락 시나리오. 에너지 수입국(한국/일본) 교역조건 극적 개선 가능 | `macro/supply_chain.md, market/daily_snapshot.md` | 진행중 |
| 2026-05-06 | 주간리포트 | Fed 이원 권력 구조 확정 — 파월 이사직 잔류(2028)+Warsh 5/11 인준. FOMC마다 정책 서프라이즈 확률 구조적 상승. 국채 변동성 확대 리스크 | `macro/us_monetary_policy.md` | 진행중 |
| 2026-05-05 | 이브닝브리핑 | WTI $92→$103 당일 반등으로 "시장의 과도 낙관 선반영" 즉일 검증 — 구조적 $80+ 바닥 확인. 에너지 풋백 매수 기회 유효. 데드라인 불발 시 $110+ 즉시 복귀 리스크 | `market/daily_snapshot.md, macro/geopolitics.md` | 진행중 |
| 2026-05-05 | 이브닝브리핑 | 5/6 아시아 동시 재개장 galp 가능성 과소평가 — 4~8일 공백(빅테크 Beat+이란 협상+WTI 하락+BTC $80K) 일시 반영. KOSPI 7,000 돌파+항셍 +1~2% 갭업 확률 중간~높음 (이란 타결 시 높음) | `market/daily_snapshot.md, macro/geopolitics.md` | 진행중 |
| 2026-05-05 | 이브닝브리핑 | BTC $80,894 — 200DMA($82,228) 돌파 시 7개월 만 첫 추세 전환 시그널. ETF 유입 $1.6B/4월+선물 OI $61B+DXY 98 약세 복합 지지. 리스크온 유지 조건부 $85K~90K 목표 | `market/daily_snapshot.md, market/correlation_matrix.md` | 진행중 |
| 2026-05-05 | 모닝브리핑 | 이란 교전→협상 24시간 급반전: 5/4 미군 보트 7척 격침+UAE 피격(WTI $106) → 5/5 Trump 8pm ET 데드라인+이란 30일 제안(WTI $92, -7%). 시장은 시나리오 A(30%)를 50%+ 과도 선반영. 호르무즈 기뢰 6개월 불변. $80 이하 복귀 2026년 내 구조적 어려움 | `market/daily_snapshot.md, macro/geopolitics.md` | 진행중 |
| 2026-05-05 | 모닝브리핑 | "스태그플레이션 vs AI 예외론" 5~6월 지배 내러티브 확정 — Fed 4명 분열+Core PCE 3.2%+ISM 가격 84.6 = 스태그플레이션 초기. 유가 급락에도 Q1 데이터 번복 불가(시차 2~3개월). AI CapEx(+8.7%)가 GDP 하방 방어 유일 축. 위험등급 4/5(조건부 하향) | `macro/us_economy.md, macro/us_monetary_policy.md` | 진행중 |
| 2026-05-05 | 모닝브리핑 | WTI↔BEI 이상 해소 급전환(Z+2.0→+0.5~1.0σ) — 단일일 -13.5% 급락. 그러나 US10Y +3bp(BEI 미반응) = 에너지 디스인플 채권 전달 3~7거래일 시차. ISM 서비스 가격 독립 고착. 협상 결렬 시 재급등 위험 | `market/correlation_matrix.md, market/surprise_index.md` | 진행중 |
| 2026-05-04 | 이브닝브리핑 | KOSPI 5/4 재개장 6,936.99(+5.12%) 사상 최고가 — SK하이닉스 +12.52% 시총 1000조 돌파. 외인 3.0조+기관 1.9조 순매수. 빅테크 AI 실적 연휴 소화 후 폭발적 매수. KOSPI 7,000 저항선 목전 | `market/daily_snapshot.md` | 진행중 |
| 2026-05-04 | 이브닝브리핑 | 이란 교전 보도 급출현(5/4 야간) — 이란 미디어 "美 순찰선 피격+US warship 호르무즈 회항" → S&P선물 -0.1%/WTI +2.87%(.90)/Brent +3.35%(.79). 미 당국 부인. 5/5 미국 개장 변동성 최대 촉매 | `market/daily_snapshot.md, macro/geopolitics.md` | 진행중 |
| 2026-05-04 | 이브닝브리핑 | BTC F&G 지수 정정 — 39(Fear). 기존 "Daily Greed 진입" 표현 수정. 26(5/1)→39(5/4) 개선 중이나 아직 Fear 구간. BTC ,190/ETH ,302. 도미넌스 58.5% 60% 저항 테스트 | `market/daily_snapshot.md` | 정정 |
| 2026-05-04 | 모닝브리핑 | Trump "Project Freedom" 호르무즈 구출작전 5/4 개시 — 미 해군 억류 선박(~2만 명) 안내. 이란 의회 "휴전 위반" 경고. 시나리오 B(제한적 대응+교착) 40% 가장 유력. WTI $100~115 변동성 극대화. 5/4 선물 개장가가 분기 첫 신호 | `market/daily_snapshot.md, macro/geopolitics.md` | 진행중 |
| 2026-05-04 | 모닝브리핑 | Trump-Xi 베이징 정상회담 5/14 확정(8년만 첫 방중) — 5/12 CPI가 정상회담 결과 간접 결정. CPI 3.5%+ 시 관세 인하 카드 제한. Section 301 공청회(5/5)가 선행 이벤트 | `market/economic_calendar.md, macro/geopolitics.md` | 진행중 |
| 2026-05-04 | 모닝브리핑 | BTC F&G Fear 26→Greed 급반전 + 선물 OI $61B(수개월 최고) + 4월 ETF 순유입 $1.6B. 기관 축적 구조 재확인. $80K 돌파+ETF 재가속=NASDAQ↔BTC 재동조화 트리거 | `market/daily_snapshot.md, market/correlation_matrix.md` | 진행중 |
| 2026-05-04 | 모닝브리핑 | ISM 가격 84.6%+Core PCE 0.0% 역사적 괴리 contrarian — 선례 2회(2008 Q3, 2015 Q1) 모두 6개월 내 에너지 급락→헤드라인 자연 소멸. ISM 고용 46.4%는 AI/자동화 대체 가속 첫 사이클 가능성 | `market/surprise_index.md, macro/us_economy.md` | 진행중 |
| 2026-05-03 | 이브닝브리핑 | 이란 14개조 평화안 트럼프 거부 — 호르무즈 교착 구조화 확정. WTI $101.94(-3.26%) 차익실현이나 $100 지지선. 기뢰 6개월(펜타곤). ISM 가격 84.6%+WTI 4월 $105=5/12 CPI 헤드라인 3.5~3.8% Base Case | `market/daily_snapshot.md, macro/geopolitics.md` | 진행중 |
| 2026-05-03 | 이브닝브리핑 | ISM 고용지수 46.4%(2026년 최저) + 가격 84.6%(4년 최고) 동시 발생 — "비용 상승+고용 축소" 구조는 AI/자동화 대체 가속 첫 사이클 가능성. 2022년 이후 첫 동시 발생 | `market/surprise_index.md` | 진행중 |
| 2026-05-03 | 이브닝브리핑 | 버크셔 $397.4B 현금 역대 최고 + Abel 첫 CEO 주재. "단기 고평가 경고 / 중기 기회 대기" 이중 해석. S&P Fwd PER 22.5x(+2σ). 5/15 Q1 13F 공시가 방향 확인 | `market/guru_positions.md` | 진행중 |
| 2026-04-30 | 모닝브리핑 | FOMC 8-4 분열(1992년 이후 최다) + UAE OPEC+ 탈퇴(5/1 발효) = "이중 쇼크". WTI $106.88(+6.96%), 10Y 4.42%(+7bp). 4/30 Core PCE 3.2%+ 시 연내 인하 0회 확정 | `market/daily_snapshot.md, macro/us_monetary_policy.md` | 진행중 |
| 2026-04-30 | 모닝브리핑 | 빅테크 4사 AH: AMZN +69%/GOOGL +94% Beat 강세, META -7%(CapEx $125~145B 상향 실망), MSFT 혼조. "AI 가위" 구도 심화 — 인프라 수혜 극도 집중, SaaS 파괴 가속 | `market/economic_calendar.md, market/daily_snapshot.md` | 진행중 |
| 2026-04-30 | 모닝브리핑 | 매크로 위험등급 4/5 유지 — 지정학(이란+UAE) 5등급, 통화정책+미국경제 4등급. 30일 시나리오: Bull 15%/Base 50%/Bear 35%. Bear 확률 기존 18%→35% 대폭 상향 | `macro/global_risk_factors.md` | 진행중 |
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
| 2026-04-29 | 이브닝브리핑 | FOMC "risks of higher inflation persist" 신규 삽입 = 3월 대비 매파 시프트. 6월 인하 20~25%로 축소. WTI $99+UAE OPEC 탈퇴+Core PCE 3.0%+ 시 연내 인하 0회 가능 | `macro/us_monetary_policy.md, market/economic_calendar.md` | 진행중 |
| 2026-04-29 | 이브닝브리핑 | 빅테크 "80초의 심판" D-Day — MSFT/META/AMZN/GOOGL 장후 동시. AI CapEx $600~645B 정당성 최대 검증. OpenAI 미스 직후라 가이던스가 핵심. AMZN 4거물 컨버전스 실시간 검증 | `market/economic_calendar.md, market/guru_positions.md` | 진행중 |
| 2026-04-29 | 이브닝브리핑 | Gold $4,577 구조적 Bull 내 최적 매수 구간(contrarian) — 중앙은행 585톤/분기+JPM $5,200+Dalio/Druckenmiller/Marks 3거물 확신 vs 실질금리 단기 상승 | `macro/global_risk_factors.md §4, market/correlation_matrix.md` | 진행중 |
| 2026-04-25 | 주간리포트 | Gold $4,724 주간 -2% 조정 = 구조적 Bull 내 매수 기회(contrarian). Gold-실질금리 상관 붕괴(+0.18 vs 전통 -0.45) 4주째 지속. 중앙은행 1,000톤+/년 + JPM $5,055(4Q26E) | `macro/global_risk_factors.md §4, market/correlation_matrix.md` | 진행중 |
| 2026-04-26 | 모닝브리핑 | 트럼프 이란 특사 파견 취소(4/25 저녁) — 대면→전화 전환. 금요일 "평화회담 기대" 서사 번복. WTI $94.88 유지이나 월요일 반등 리스크. 오만 무스카트 대안 중재지 부상 | `macro/geopolitics.md §2-1, market/daily_snapshot.md` | 진행중 |
| 2026-04-26 | 모닝브리핑 | WTI↔BEI "서비스 인플레 고착" 구조 전환 최초 포착 — WTI 하락(-1.24%)에도 10Y 상승(+2bp). 에너지→서비스 인플레 동력 이동 시사. 4/30 Core PCE 최종 판별자 | `market/correlation_matrix.md, macro/us_economy.md` | 진행중 |
| 2026-04-26 | 모닝브리핑 | 4/29~30 "48시간 결정전" — FOMC(파월 톤 40%) + 빅테크 4건(MSFT/META/AMZN/GOOGL AI CapEx) + GDP Q1(GDPNow 1.24%) + Core PCE + ECB + AAPL. 골디락스 vs 스태그 분기 | `market/economic_calendar.md` | 진행중 |
| 2026-04-28 | 이브닝브리핑 | WTI 장중 $100.10 터치(2022.06 이후 최초) — 종가 $98.97. Brent $111.57. 이란 교착 시 $100~110 레인지 연말 고착. Core PCE 3.2%+ 시 연내 인하 완전 소멸 | `market/daily_snapshot.md, macro/geopolitics.md` | 진행중 |
| 2026-04-28 | 이브닝브리핑 | "Beat but No Raise" 패턴 — GE Aerospace EPS +16.3% Beat에도 -4%(가이던스 동결). 빅테크 4/29 실적에 확산 시 P/E 멀티플 구조적 상한 제한 | `market/economic_calendar.md` | 진행중 |
| 2026-04-28 | 이브닝브리핑 | S&P↔10Y 동반 변동 14일(역대 2위) — 2022.3~4 15일 후 동반 급락 전환 전례. 4/30 Core PCE가 구조 해소 vs 붕괴 최종 판별 | `market/correlation_matrix.md` | 진행중 |
| 2026-04-28 | 이브닝브리핑 | KOSPI 6,666(+0.77% 신고가) vs KOSDAQ -1.40% — 대형/소형 분열 시작. 닷컴 피크(1,238.80) 근접 후 KOSDAQ 차익실현 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-27 | 이브닝브리핑 | 이란 "순환 교착" 구조화 — 신제안(호르무즈+핵 분리) 미국 수용 불투명 + 아라그치 모스크바(러시아 개입). 유가 $90~100 연말 고착 베이스 시나리오 격상 | `macro/geopolitics.md §2-1, market/daily_snapshot.md` | 진행중 |
| 2026-04-28 | 모닝브리핑 | 파월 마지막 FOMC 주재 — Warsh 후임 확정 임박. 성명문 "upside risks" 등장 시 연내 인하 완전 소멸. 유산 메시지 + 정책 전환 시그널 동시 관전 | `macro/us_monetary_policy.md` | 진행중 |
| 2026-04-28 | 모닝브리핑 | 트럼프 이란 신제안 "much better" 평가이나 핵 포기 요구 불변 — 부분 합의 확률 미세 상향(20~25%). 아라그치 모스크바(러시아 중재 공식화) | `macro/geopolitics.md, market/daily_snapshot.md` | 진행중 |
| 2026-04-28 | 모닝브리핑 | S&P 7,174+10Y 4.34% 동반 상승 14일 연속(2022.3~4 이후 최장) — VIX 18 "거짓 안정 4주째". 4/30 Core PCE가 구조 해소 vs 역전 최종 판별 | `market/correlation_matrix.md` | 진행중 |
| 2026-04-27 | 이브닝브리핑 | 아시아 "동시 신고가 러시" — 닛케이 60,537(역대 60K 최초) + KOSPI 6,615(+2.15%). "아시아 반도체 슈퍼사이클" 글로벌 확산. 에너지 수입국이 반도체로 유가 충격 흡수 | `market/daily_snapshot.md` | 진행중 |
| 2026-04-27 | 이브닝브리핑 | 매크로 위험등급 3→4(위험) 상향 — 이란 순환 교착 + Brent $107+(2022.06 이후 최고) + 쿼드러플 이벤트 직전 + 협상 채널 3원화 | `macro/global_risk_factors.md` | 진행중 |
| 2026-04-27 | 이브닝브리핑 | "서비스 인플레 잠복기 후반" 판정 — ISM 서비스 가격 70.7 = 에너지→서비스 비용 전이 초기 진입. WTI 하락만으로 인플레 자동 해소 불가. 4/30 Core PCE 최종 판별 | `market/correlation_matrix.md, macro/us_economy.md` | 진행중 |
| 2026-04-27 | 이브닝브리핑 | AMZN 거물 컨버전스 4인(Ackman 신규 + Wood $71.5M + Druckenmiller + Dalio) — 4/29 빅테크 슈퍼 수요일 직접 검증 | `market/guru_positions.md` | 진행중 |
| 2026-04-26 | 이브닝브리핑 | 이란 평화회담 파키스탄→오만 이동, 대면 채널 격하 확정. 이란 "봉쇄 해제 전 협상 불가" 공식화. 호르무즈 기뢰 6개월 구조적 유가 충격 연말 고착 가능성 | `macro/geopolitics.md §2-1, market/daily_snapshot.md` | 진행중 |
| 2026-04-26 | 이브닝브리핑 | 4/29 빅테크 슈퍼 수요일 — 거물 3인(Ackman META $1.76B / Druckenmiller AMZN +69% / Tepper MU +200%) 대형 베팅 직접 검증. AI CapEx 가이던스 "유지/확대" vs "에너지 비용 부담" 분기 | `market/economic_calendar.md, market/guru_positions.md` | 진행중 |
| 2026-04-26 | 이브닝브리핑 | VIX 18선 "거짓 안정 최종 단계" 경고 — F&G 70 vs 소비심리 49.8 괴리 + 4/29~30 이벤트 6개 집중 + 숏볼 극단. VIX 22~25 스파이크 확률 35~40% | `market/correlation_matrix.md, macro/global_risk_factors.md` | 진행중 |
| 2026-04-26 | 글로벌인텔리전스 | 4축 동인 판정 갱신: 단기 "지정학 ≥ 기술" (격차 축소). "AI 가위" 공식화(SOX 18일/Intel +2,800% vs SaaS -18%)로 기술 축 영향력 상향. 중기 이후 기술 > 정치 ≥ 지정학 | `lead_global_intelligence_20260426.md` | 진행중 |
| 2026-04-26 | 글로벌인텔리전스 | 숨은 테마 ★ "서비스 인플레 고착" — WTI 하락에도 10Y 상승 최초 포착. 에너지→서비스 인플레 동력 구조 전환. ISM 서비스가격 70.7(2022.10 이후 최고). 4/30 Core PCE 최종 판별자 | `lead_global_intelligence_20260426.md, market/correlation_matrix.md` | 진행중 |
| 2026-04-26 | 글로벌인텔리전스 | 숨은 테마 ★ "SMR-AI DC 전력 수렴" — X-Energy IPO $10B+(원자력 역대최대). Marks/Druckenmiller 에너지전환 컨버전스. 빅테크 5사 직접 SMR 발주(MS 2GW/Google 500MW/Amazon 5GW/Meta 6.6GW). 변압기 128~144주 납기→SMR 직결 | `lead_global_intelligence_20260426.md, macro/tech_breakthrough.md` | 진행중 |
| 2026-04-26 | 글로벌인텔리전스 | 시나리오 #6 신규 등록: "4/30 트리플 폭탄"(GDP+PCE+빅테크). 골디락스 30%/혼조 45%/스태그 25%. Fed 리더십 갈림길 해소(DOJ 종료)로 교체. 호르무즈+스태그 동시 시 S&P -10~15% | `knowledge-db/performance/2026_scenario_tracking.md` | 진행중 |
| 2026-04-26 | 글로벌인텔리전스 | 대만 리스크 🟡→🟠 격상 — 랴오닝 해협 통과(4/20), 라이칭더 영공차단(역사상 첫), 17명 군간첩 적발, 봉쇄돌파훈련. 일본 이카즈치 통과+살상무기 규제 완화. "다축 에스컬레이션" | `macro/geopolitics.md, lead_global_intelligence_20260426.md` | 진행중 |
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
| `energy.md` | **Brent ~$108, WTI $101.94**, 04-30 $126.41(전쟁기간 최고). JKM low-$15s~$17s, 정제마진 **~$43.50**(역대급 유지), Henry Hub $2.78 | **UAE OPEC 탈퇴(5/1)**. 트럼프 적대행위 종결 선언(실질 미해소). 호르무즈 90%+ 감소 지속. GS 연평균 Brent $85(상향). **한화솔 Q1 OP 926억(전사 흑자전환)**. S-Oil Q1 OP 1조+/5/4 재가동. KEPCO OP 20조(원전 이용률 89%). 두산엔 수주 14.3조. BESS 600GWh(2026E). 그린수소 보조금 $1/kg 달성 | 05-03 | 06-02 | high |
| `science_tech.md` | 한국 R&D/GDP **5.1%**(OECD 2위), 글로벌 R&D 3.8조달러, 정부 R&D **35.5조**(+19.9%) | **양자**: IBM Heron R2 QEC 10x+IonQ FT 99.99%+PQC $29.95B(2034E). **바이오**: Lilly Foundayo 경구GLP-1 FDA승인(04월)+Insilico $2.75B. **우주**: Falcon9 600착+Starship V3 점화. **로보틱스**: Optimus V3 중반 데뷔(04-23)+Figure02 BMW 30K+Agibot 1만대. **핵융합**: CFS SPARC late2026~2027(소폭후퇴)+Helion 외부연구$4M. **EDA**: Siemens Fuse 3파전+AI EDA $4.27B. **CapEx**: $635~665B(+67~74%). 전고체 QS Eagle+SDI 500Wh/kg | 04-26 | 05-26 | high |
| `bio_pharma.md` | **LLY 2026E $80~83B 가이던스(컨센 $77.6B 상회)** Zepbound/Mounjaro $36.5B(+45%), orforglipron 경구 GLP-1 2026.04.01 FDA 승인. NVO -5~-13% 가이던스 쇼크 + 경영진 교체 | **삼성바이오 207940** 2025FY 4.55조(+30%), 2026E 5조+, OPM 40%중반. 5공장(18만L) + BIOSECURE Act 반사이익. 트럼프 관세 2026.07.31 발효(브랜드약 100%, **한국 15%**, 록빌 공장 6만L 프리미엄). 목표주가 224.7만(Strong Buy 25인) | 04-21 | 05-21 | high |
| `quantum.md` | IonQ FY2026 $225-245M(+81%), **SkyWater $1.8B FTC 2차요청**(04-24), Quantinuum IPO mid-2026($20B+, $1B조달), 양자센서 $502M-984M(국방40%), **CISA PQC 연방의무화** | IBM Poughkeepsie 확장(Heron 16x/25x)+Starling 511K. Rigetti Cepheus-1-108Q GA(04-07). **Cloudflare PQC 2029 합류**(65%트래픽PQ). Q-Day 가속 3논문(JVG 5K큐빗). SandboxAQ $5.3B. Infleqtion DARPA HARQ $2M. 한국 양자클러스터 5개 08월 지정 | 05-02 | 06-02 | high |
| `space.md` | 우주경제 $626B(2025), Starlink **10,020기+**/1,000만, SpaceX **$1.75T IPO SEC S-1 제출**, Falcon 9 51회(4/30), RKLB $602M(Q1 5/7), 우주군 $26B+Golden Dome **$185B**, KASA R&D 9,495억, LUNR $800M Lanteris 인수 | Starship V3 IFT-12 **5/12 발사 목표**. SpaceX IPO 6월 Nasdaq $75B+ 조달. Blue Origin FAA 비행정지 지속(12회 발사 차질). Amazon Leo **302기**(FCC 미달 24개월 연장 미결정). Starlink Mobile 리브랜딩(DTC 600만+, 2500만 목표). AST BB 8~10 출하 대기(BB32까지 생산). **Artemis III 지구궤도 테스트로 변경**(달착륙->Artemis IV 2028). Golden Dome SBI 비용 논란. True Anomaly $650M. LUNR FY26E $900M~$1B | 05-02 | 06-02 | high |
| `smr.md` | TerraPower **4/23 착공**(2031 완공), X-energy IPO **$1.02B**(원자력 역대최대, XE +27%), NRC Part53/Part57 규제혁신, CFS SPARC 자석설치(18기 중반완료), 두산 Q1 OP 2,335억(+63.9%)/수주잔고 24.1조(+46%), 빅테크 7사 Ratepayer Protection Pledge | NuScale 리스크 심화(Fluor 전량매각 $2.43B/Citi TP $9/ENTRA1 $532M손실). BWXT PCG 인수+$174M 해군계약. RR-SMR £599M 정부대출/DAC 2026말. Oklo $72.70(+182% YoY)+NVIDIA-LANL. Helion 150M°C D-T(민간최초). 중국 Linglong One 2026가동. 달원자로 100kW 확대+SR-1 핵추진우주선. Part57 마이크로리액터 함대일괄승인(심사1년미만) | 05-02 | 06-02 | high |
| `telecom_next.md` | **6개 서브섹터 확장**(6G/5G-Adv/Open RAN/위성통신/NTN/AI-RAN). ITU TPR 20개 확정(2026.02), AI-RAN $3.81B(CAGR 29%), Open RAN 5%->28%(2029), Starlink 1180만(04월), AI-RAN Alliance 130+사, **Nokia Q1 EUR4.5B(+4%)/Ericsson Q1 유기적+6%** | 3GPP Rel-21 2026.06 타임라인 결정점. Starlink IPO 초안(04.29). **NVIDIA Nokia $1B+Marvell $2B 투자**. AT| `telecom_next.md` | **6개 서브섹터 확장**(6G/5G-Adv/Open RAN/위성통신/NTN/AI-RAN). ITU TPR 20개 확정(2026.02), AI-RAN $3.81B(CAGR 29%), Open RAN 5%->28%(2029), Starlink Mobile 2500만 목표, Starlink 1000만+, T-Mobile DTC 300만+, AI-RAN Alliance 100+사 | 3GPP Rel-21 2026.06 타임라인 결정점. **AST BlueBird7 궤도실패**(04.19). Amazon Leo 베타 라이브(04.08) FCC 미달. SKT-삼성 AI-RAN 공동연구. SKT MWC2026 AI 네이티브 선언. 한국 6G 예산 1067억 증액. Nokia QKD 인수. NVIDIA Aerial 오픈소스. 6G 표준 fork 리스크. 5G SA 의무화 | 04-25 | 05-25 | high |T Open RAN 50% 트래픽. Qualcomm X105 Rel-19 모뎀. Amazon Leo 302기. **KT 해킹(01월) 가입자 23만 이탈**. T-Mobile AI-RAN 필드 트라이얼 예정. 3GPP-O-RAN 6G 공동 워크숍 | 05-02 | 06-02 | high |
| `banking_capital.md` | **KB 1Q26 1.8924조 확정 +11.5% (분기 역대 최대, 4/23 발표)·4대 합산 컨센 5.2371조(+6.2%, 1Q 첫 5조 돌파)·KB 2.9조 자사주 소각(업계 최대)·NH증권 Q1 OP 6,367억 record(+120.3%)**. 글로벌 M&A Q1 $1.2조(+42% YoY record), GS Advisory $1.49B(+89%) 1위 $267B·GS 2026-04-23 Buy 83.9 A- 분석 완료. BLK AUM $13.9T·EPS $12.53 Beat | JPM EPS $5.94 Beat (NII가이던스 $104.5B→$103B 하향)·BAC NII 가이던스 +5~6%→+6~8% 상향·C 순익 +42%·WFC 미달. MS IB +36%. USB/PNC CRE 11분기 감소 후 복귀. Blackstone $1.3T record(+12%). KKR/APO 2026-02 -10%+ AI SaaS 충격. **Basel III Endgame 2026-03-19 재공표, 6/18 의견수렴, Q4 최종안 예상, $250B 이하 면제**. 미 CRE Wall $1.5조 2026 만기. BOK 2.50% 7연속 동결, 신현송 인상 시사(중동 2차파급). 한국 ETF 400조 돌파(4/15). 카카오페이 매출 +30% OP +491% | 04-24 | 05-24 | high |
| `advanced_materials.md` | **6개 서브섹터 주간 갱신**(CNT/그래핀/초전도체/SiC-GaN-세라믹/희토류/정책). OCSiAl SWCNT 1,000t 목표(2배 확대). Nd $215/kg(+45% YTD), Dy $931/kg(+100%+). 상압 Tc 151K 신기록. Wolfspeed Ch11 탈출(91일). REBCO 테이프 생산 3배. 48D 25→35% 인상 | Adisyn 저온 그래핀 인터커넥트 시연. Paragraf 6인치 그래핀 웨이퍼. 그래핀스퀘어 CVD 양산공장 세계최초 준공. SPARC 2027 first plasma. onsemi SiC JFET $115M 인수. Navitas GTC 800V. MP Nevada HREE 2026 후반. Lynas TX 불확실. Cyclic Materials 리사이클링. EU CRM 센터 설립. Advanced Materials Act Q4 2026 | 05-02 | 06-02 | high |
| `battery.md` | **리튬 $20,684/ton CIF(2026-04-01, +66.7% in 3M)** — 2026.01 $26,278 고점 후 조정. **K-3사 합산 OP -3.2조**(LGES +83%, SDI 적자전환 -1.42조, SK온 -0.49조), 가동률 50%초, 글로벌 점유 **15% 붕괴**(SNE Jan-Feb: CATL 42.1%/BYD 13.4%/LGES 8.7%/SK 3.8%/SDI 2.5%). **auto.md 정합 100%** | Ford BlueOval 해산 Tennessee 67GWh 단독. CATL 헝가리·인도네시아 가동, Qilin 2nd Gen. BYD Blade 2.0(3/5). LFP 2026E 65% 도달. 전고체 Toyota 2027~28 첫 EV. 코발트 $56,290(+67% YoY). AI DC ESS 2030 $6B | 04-21 | 05-21 | high |
| `infrastructure.md` | **현대건설 Q1 OP 1,734억 + 홀텍 SMR EPC 4~5조**, 대우 18조/GS 17.8조/DL 12.5조, 삼성물산 EPC 10조+·평택 P5 착공. **변압기 납기 128~144주(DC 50%+ 지연)** — 효성중공업 13.85조·HD현대일렉 12.48조 수주잔고, Vertiv $15B·Eaton $12B | 우크라이나 재건 $523.6B·NEOM 재조정·중동 재건 $140B·CHIPS 팹 1.5조 달러. smr/capex/defense/banking_capital 정합 확인 (SMR 두산 14.3조·DC CAPEX $660-690B·방위력 19.97조·PF 금리 6.1%) | 04-21 | 05-21 | high |
| `capex.md` | Q1 실적 반영: 하이퍼스케일러 4사 $695-725B(기존 $635-665B **+$60B**), 5사 $745-775B(기존 $660-690B). MSFT $190B(대폭상향). GOOGL Cloud $20B(+63%), 백로그 $460B+. AWS $37.6B(+28%). AI ARR $37B(+123%). TSMC 2nm 3월 매출시작. ASML EUR36-40B 상향. 유틸리티 $1.4T | SK하이닉스 OP 37.6조(OPM 72%, HBM 3년완판). Samsung DS OP 53.7조, HBM4 최초양산. AMZN FCF -95%. 부품비 +$25-50B 가이던스 상향 주도. DC 자체발전 30%. SMR NRC 건설허가 2026. GS 2026-2031 $7.6T. 2027 $1T+(CNBC). HBM $54.6B(+58%) | 05-02 | 06-02 | high |
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
> [2026-05-03 wiki-linter]: KB 건강점검 full 모드. P0 0건 / P1 6건 (us_monetary_policy 구버전 + korea_economy 만료임박 + knowledge-db 미등재 3종 + 레코드 불일치 5종). knowledge-db 표 8행 자동 수정. 교차참조 맵·README·lint_report 미갱신은 2026-05-06 후속 복구.
> [2026-05-06 후속 복구]: 5/3 wiki-linter 누락분 일관성 복구 — 교차참조 맵 7행 04-26→05-06 기준 재검증, global_risk_factors.md last_updated 04-26→05-03, Market KB 헤더 05-03→05-06 동기화.

---

## 🌍 Macro KB (`knowledge-base/macro/`)

| 파일 | 핵심 수치 | 핵심 리스크 | 갱신일 | 신뢰도 |
|------|---------|-----------|-------|-------|
| `us_economy.md` | **CPI 3.3%(에너지 주도), Core CPI 2.6%, ISM제조가격 78.3+서비스가격 70.7(양채널 극단), GDPNow Q1 +1.24%(추가하향), Fed 3.50~3.75%, 10Y 4.30%, DXY 98.53, S&P 7,165(신고가), VIX 18.53, 침체확률 30~49%, 소매판매3월 +1.7%, 미시간심리 49.8(최종/역대최저)** | 3중 인플레 파이프라인 지속. DOJ 파월수사 종료(4/24)+Warsh 인준 경로 개통. WTI $97+ 재급등(호르무즈 이중봉쇄). 4/30 Core PCE+GDP 더블이벤트. 소비심리 49.8 vs VIX 18.53 괴리 지속 | 04-25 | ✅ high |
| `us_monetary_policy.md` | **Fed 3.50~3.75%(2연속 동결), CPI 3.3%(에너지 주도), Core CPI 2.6%, Core PCE 3.0%, QT 종료, 대차대조표 $6.7T, 10Y 4.31%, DXY 97.70, 침체확률 30~35%** | 트럼프 파월 05/15 해임 위협. 이란전쟁 에너지 인플레. 인하 하반기 후반 전망. Fed 독립성 리스크 | 04-18 | ✅ high |
| `geopolitics.md` | **IEEPA 위헌→실효 34.7%**. WTI ~$101, Brent ~$108. 리스크 5/5. **트럼프 이란전쟁 종결 선언이나 호르무즈 통항 90%↓ 지속** | **이란 형식 종전·실질 교착**(극고). 5.5 Section 301 과잉생산 공청회 D-2. 5.14~15 미중 베이징 정상회담 D-11. 북한 IAEA 핵능력 강화 경고. 대만 특별국방예산 5.6 협상 | 05-03 | ✅ high |
| `korea_economy.md` | **Q1 GDP +1.7%(5.5년최고 서프라이즈, YoY +3.6%), GDI +7.5%(38년최고), 4월1-20일 수출 $50.4B(+49.4% 역대최대), 반도체 $18.3B(+182.5%), 경상수지 2월 $23.2B(사상최대)+3월 초과 전망, KOSPI 6,481(4월+20%), 금리 2.50%(7연속동결), 신현송 4/21 취임(매파 유연), 원화 1,480~1,486, WGBI 3주 8.5조 유입, 삼성 Q1 OP 57.2조+SK하이닉스 37.6조(OPM 72%), 외국인 4월 순매수전환(5.8조), 현대+기아 Q1 관세부담 1.62조, KTB 10Y 3.816%** | 신현송 매파 전환(ING 7월 인상 가능). 원화약세 패러독스(경상흑자에도 NPS 해외투자). 외국인 3월 40.35조 순매도→4월 반전. 자동차 25% 관세(부품 4/30 발효). 반도체 관세 7월 확대 검토 | 04-25 | ✅ high |
| `global_risk_factors.md` | **VIX 16.89(거짓 안정 재진입), F&G 70(Greed심화), DXY ~98(반등), Gold $4,614(IB 전원 $5K+ 목표: JPM $5~6K/GS $5.4K/UBS $5.9K), Brent $108, WTI $101.94, 원달러 1,476, 소비심리 49.8(최종/역대최저), IMF 3.1%(하향), 침체확률 27~35%(하향), 10Y 4.30%, BTC $78K** | 호르무즈: 트럼프 5/1 적대행위 종결 선언이나 이란 14개조 불만족·통항 90%↓·기뢰 분실. 스태그플레이션: Core PCE 3.2% + ISM가격 84.6 + GDP Q1 +2.0%. FOMC 4명 반대(1992 이후 최다). 미중 5/14~15 정상회담. Gold IB 전원 $5K+. 희토류 유예 중 | 05-03 | ✅ high |
| `political_cycle.md` | **FOMC 4/29 4인 반대(1992년이후최다), FFR 3.50~3.75% 동결, GDP Q1 2.0%/Core PCE 4.3% 스태그플레이션, Warsh 상원위통과+본회의5/11+5/15취임, 파월 이사직잔류, 이란 적대행위종료선언(호르무즈90%↓지속), 중간선거 민주 Generic Ballot +10pp(Emerson), 상원 메인73%/오하이오59%/알래스카67% 민주승리, 한국 지지율64%(갤럽5/1), KOSPI 6598(4월+30.61% 28년최대), 고유가지원금107만명/6094억지급, 지방선거 민주9~13곳, ECB 동결+인플레3.0%+6월인상전망, BOJ 6대3분열+CPI2.8%상향+GDP0.5%반감, 미중5/14~15 사전조율완료, 인도FDI$90B+India-EU FTA체결, NATO 유럽$864B(+14%사상최대)** | Core PCE 4.3%→연내인하0회 기본시나리오. Warsh QT가속→유동성축소. 이란 형식종전·호르무즈실질봉쇄. ��국 민주압승+밸류업→KOSPI 7000 근접. ECB/BOJ 6월 동시인상 가능성. 스태그플레이션 글로벌 확산 | 05-03 | ✅ high |
| `tech_breakthrough.md` | **AI: GLM-4.7 NVIDIA 없이 프론티어(중국 독자), Blackwell 토큰비용 2센트/M(15x↓), 에이전틱 $10.8B(+42%,Gartner 40%), EU AI Act 8/2 집행 발효. 반도체: TSMC A12/A13 High-NA 미채택(5/1), 2nm 2팹 솔드아웃, Samsung SF2 수율50-60%, Intel 18A 수율55%. 에너지: Helion 1.5억도C 플라즈마, Linglong One 2026H1 상업, Donut Lab SSB 400Wh/kg. 바이오: Intellia in vivo Phase 3 최초 성공(4/27), CHOP 맞춤형 CRISPR. 양자: Google Quantum Echoes 13Kx, Quantinuum 94논리큐빗 beyond break-even. 로봇: Tesla 댈러스·휴스턴 로보택시(56%할인), Unitree $610M IPO, 중국90%. 우주: 2026 1000번째 Starlink(4/14), FCC D2D 248위성. 신소재: 탠덤35%+ 파일럿출하, Wolfspeed 10kV SiC MOSFET** | Disruption Map +3행(중국AI자립, TSMC High-NA 미채택, CRISPR Phase 3). 8개 서브���터 주간 갱신(+20 DB) | 05-03 | ✅ high |
SUPPLY_CHAIN_PLACEHOLDER

---

## 📊 Market KB (`knowledge-base/market/`) — 2026-05-06 최신

| 파일 | 상태 | 갱신 빈도 | 영향 브리핑 모듈 | 재수집 명령 |
|------|------|----------|---------------|-----------|
| `daily_snapshot.md` | ✅ SUCCESS (05-06) valid_until 05-06 EOD confidence:medium-high | 매 거래일 | A-1, B-2, B-3 | 05-07 재실행 |
| `economic_calendar.md` | ✅ SUCCESS (05-02) valid_until 05-09 confidence:high | 주 1회 | A-4, B-1, C-6 | — |
| `surprise_index.md` | ⚠️ PARTIAL (05-02) valid_until 05-31 confidence:medium | 매일 | B-4 | 완전 수집 목표 |
| `correlation_matrix.md` | ✅ SUCCESS (05-03) valid_until 05-31 confidence:medium | 주 1회 | B-5 | — |
| `guru_positions.md` | ✅ SUCCESS (04-28) valid_until 07-18 confidence:high | 분기 1회 | A-5, B-7, C-4 | Q1 2026은 05-15 이후 |

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
| `energy_2026.jsonl` | 156건 (+24 @2026-05-03) | kb-updater |
| `geopolitics_2026.jsonl` | 117건 (+26 @2026-05-03) | kb-updater |
| `science_tech_2026.jsonl` | 492건 (quantum/space/smr/biotech/eda/cybersecurity subtag 포함, +57 @2026-05-03 갱신) | kb-updater |
| `bio_pharma_2026.jsonl` | 72건 (+38 @2026-04-21) | kb-updater |
| `macro_2026.jsonl` | 733건 (+20 @2026-05-03) | kb-updater |
| `banking_capital_2026.jsonl` | 95건 (+31 @2026-04-24, Q1 2026 실적 반영) | kb-updater |
| `advanced_materials_2026.jsonl` | 185건 (+43 @2026-05-02 주간 갱신) | kb-updater |
| `battery_2026.jsonl` | 110건 (+70 @2026-04-21) | kb-updater |
| `infrastructure_2026.jsonl` | 63건 (+39 @2026-04-21) | kb-updater |
| `capex_2026.jsonl` | 54건 (+14 @2026-05-02 Q1 실적 갱신) | kb-updater |
| `smr_2026.jsonl` | 45건 (+45 @2026-05-02 신규 생성) | kb-updater |
| `telecom_next_2026.jsonl` | 158건 (+22 @2026-05-02 주간 갱신) | kb-updater |
| `robotics_2026.jsonl` | 29건 (신규 생성 2026-04-19) | kb-updater |
| `crypto_bitcoin_2026.jsonl` | 48건 (신규 생성 2026-04-20) | kb-updater |
| `defense_2026.jsonl` | 25건 (신규 생성 2026-04-21) | kb-updater |
| `luxury_2026.jsonl` | 52건 (신규 생성 2026-04-21 야간) | kb-updater |
| `consumer_retail_2026.jsonl` | 31건 (신규 생성 2026-04-22) | kb-updater |
| `logistics_2026.jsonl` | 29건 (신규 생성 2026-04-24) | kb-updater |
| `food_agriculture_2026.jsonl` | 57건 (신규 생성 2026-04-24) | kb-updater |
| `insurance_2026.jsonl` | 73건 (신규 생성 2026-04-24) | kb-updater |
| `education_2026.jsonl` | 42건 (신규 생성 2026-04-24) | kb-updater |
| `changelog_2026.jsonl` | 95건 (+3 @2026-05-03) | kb-updater |
| `quantum_2026.jsonl` | 17건 (신규 등재 2026-05-03, industry/quantum.md SSOT) | kb-updater |
| `real_estate_2026.jsonl` | 26건 (신규 등재 2026-05-03, industry/real_estate.md SSOT) | kb-updater |
| `healthcare_service_2026.jsonl` | 47건 (신규 등재 2026-05-03, industry/healthcare_service.md SSOT) | kb-updater |
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
| 미국 Fed 금리 | `us_monetary_policy.md` (루트): redirect 포인터 (수치 없음) | `macro/us_monetary_policy.md`: 3.50~3.75% (04-18 갱신, FOMC 4/29 4인 반대 미반영) | 05-06 | ⚠️ macro/us_monetary_policy.md 재수집 권장 (Core PCE 4.3%·Warsh 5/15 취임 미반영) |
| VIX | `macro/global_risk_factors.md`: 16.89 (05-03 갱신, "거짓 안정 재진입") | `market/daily_snapshot.md`: 미확정 (05-05 종가, 수집 누락) | 05-06 | ⚠️ daily_snapshot.md VIX 수치 미수집 — 다음 갱신 시 보완 |
| DXY | `macro/global_risk_factors.md`: ~98 (05-03 갱신) | `market/daily_snapshot.md`: ~98 구간 (05-05 ET) | 05-06 | ✅ 일치 (구간 일치, 정확 수치 SSOT 보완 권장) |
| 원/달러 | `macro/korea_economy.md`: 1,480~1,486원 (04-25, 구버전) | `market/daily_snapshot.md`: 1,473.21 오픈 / 1,467.90~1,477.18 (05-06 KST 오전) | 05-06 | ⚠️ korea_economy.md 갱신 권장 (시점차 11일, 1% 갭) |
| S&P 500 | `macro/us_economy.md`: 7,165 (04-25 신고가) | `market/daily_snapshot.md`: 7,259.22 (05-05 ET 종가) | 05-06 | ⚠️ us_economy.md 갱신 권장 (10일 시점차, +1.31% 누적) |
| WTI | `industry/energy.md`: $101.94 (05-03 갱신, 05-02 종가) | `macro/geopolitics.md`: ~$101 (05-03 갱신) / `market/daily_snapshot.md`: $102.27 (05-05 ET 종가, -3.9%) | 05-06 | ✅ 일치 (SSOT 3종 동기화, 다음 갱신 시 5/5 $102.27 반영) |
| Gold | `macro/global_risk_factors.md §4`: $4,614 (05-03 갱신) | `market/daily_snapshot.md`: $4,518~$4,533 (05-05 종가, 이란 협상 헷지 수요 감소) | 05-06 | ⚠️ -2% 차이 (시점차 — global_risk 05-03, snapshot 05-05) |

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
| 2026-05-03 | `macro/tech_breakthrough.md` | **8개 서브섹터 주간 갱신(18회 검색, +20 DB 레코드)** -- AI: GLM-4.7 NVIDIA 없이 프론티어(중국 독자HW), Blackwell GB200 토큰비용 2센트/M(15x절감), 에이전틱 $10.8B(+42%/Gartner 40%/ROI 171%), EU AI Act 8/2 GPAI 집행 발효. 반도체: TSMC A12/A13(2029) High-NA 미채택(TrendForce 5/1)→ASML 영향, 2nm 2팹 솔드아웃, Samsung SF2 수율50-60%/Exynos2600 양산, Intel 18A 수율55%/18A-P 2026H2. 에너지: Helion 1.5억도C 플라즈마+건설 앞당김, Linglong One 2026H1 상업운전, Samsung SDI+BMW+Solid Power SSB, Donut Lab 400Wh/kg 5분충전. 바이오: Intellia in vivo CRISPR Phase 3 최초 성공(4/27)+FDA 롤링서브미션, CHOP 맞춤형 CRISPR 세계 최초, Foundayo CNPV. 양자: Google Quantum Echoes 13,000x, Quantinuum 94논리큐빗 beyond break-even/S-1 제출, IonQ 원격 광자 인터커넥트 시연. 로봇: Tesla 댈러스·휴스턴 로보택시(56%할인/안드로이드앱), Unitree $610M IPO/335%성장, 중국90%장악. 우주: 2026 1,000번째 Starlink(4/14), FCC D2D 248위성인가, BlueBird 7 궤도미달. 신소재: 탠덤35%+ 파일럿 미국·독일·한국 출하, 유연33.6%(Nature), Wolfspeed 10kV SiC MOSFET(시스템비용30%↓), Cs도핑 26.61%. Disruption Map +3행(중국AI자립, TSMC High-NA 미채택, CRISPR in vivo Phase 3) | +20 |
| 2026-05-03 | `industry/energy.md` | **에너지 섹터 주간 갱신(16회 검색)** -- Brent 04-30 $126.41(전쟁기간 최고)->05-02 ~$108. WTI $101.94. **UAE OPEC 탈퇴(5/1, 점유율 30% 미만 최초)**. 트럼프 적대행위 종결 선언(호르무즈 90%↓ 지속). GS 연평균 Brent $85(상향). 이란 14개조 평화안 검토. 한화솔루션 Q1 OP 926억(전 사업부 흑자전환 확정). S-Oil Q1 OP 1조+/5/4 사우디 얀부유 90%+ 재가동. KEPCO OP 20조/원전이용률 89%. 두산에너빌리티 수주 14.3조(원자력 5.8조+가스 5.3조). BESS 글로벌 108GW(+40%)/600GWh(2026E). 그린수소 보조금 $1/kg 달성. XLE +45.67%(12M, 유일 양수 섹터) | +24 |
| 2026-05-03 | `macro/global_risk_factors.md` | **글로벌 리스크 맵 주간 갱신(19회 검색)** -- 호르무즈: 트럼프 5/1 적대행위 종결 선언(War Powers 회피)이나 이란 14개조 불만족+IRGC 재개 경고+통항 90%↓+기뢰 분실. 4/30 Brent $126(역대고)→5/2 WTI $101.94/Brent $108. 스태그플레이션: Core PCE 3.2%(2023.11 최고)+ISM가격 84.6+GDP Q1 +2.0%(컨센↓)+디플레 4.5%. FOMC 4명 반대(1992 이후 최다)+파월 이사직 잔류(의장 5/15 종료). 미중: 5/14~15 정상회담 확정(8년만 방중). 대만: 호르무즈 봉쇄 교훈 학습+라오닝 통과. Gold $4,614(IB 전원 $5K+: JPM $5~6K/GS $5.4K/UBS $5.9K). 희토류 유예 중(2H26 재시행 가능). WEF 사이버 64%. 러-북 2027~31 군사협력. VIX 16.89(거짓 안정 재진입) | +22 |
| 2026-05-03 | `macro/political_cycle.md` | **정치사이클 주간 갱신(16회 검색)** -- FOMC 4/29 4인반대(1992년이후최다)+GDP Q1 2.0%/Core PCE 4.3% 스태그플레이션+연내인하0회 기본시나리오. Warsh 상원위통과+본회의5/11+5/15취임. 파월 이사직잔류. 이란 적대행위종료선언(호르무즈90%↓지속). 중간선거 민주 Generic Ballot +10pp, 상원 메인73%/오하이오59%/알래스카67% 민주. 한국 지지율64%(갤럽5/1)+KOSPI 6598(+30.61%)+지원금107만명/6094억+지방선거 민주9~13곳. ECB 동결+인플레3.0%+6월인상전망. BOJ 6대3분열+CPI2.8%상향+GDP0.5%반감. 미중5/14~15 사전조율. 인도FDI$90B+India-EU FTA체결. NATO 유럽$864B(+14%사상최대) | +16 |
| 2026-05-03 | `macro/geopolitics.md` | **지정학 4개 서브섹터 주간 갱신(17회 검색)** -- 미중관세: 강제노동 공청회(4.28~5.1) 완료+과잉생산 공청회(5.5~8) D-2. Section 122 15% 인상 미시행+24개주 위헌소송 판결 대기. 트럼프-시 베이징 정상회담(5.14~15) D-11 확정(36시간 체류, Board of Trade 논의). 대만: ADIZ 169회(감소 추세)+펑후 해군 배치. 특별국방예산 5.6 4차 협상 예정(KMT 내부 분열). PRC 유럽 7개사 수출통제+공급망 안보법 서명. 중동: 트럼프 5.2 이란전쟁 공식 종결 선언(War Powers 회피). 이란 14개조 평화안 제출이나 트럼프 불만족. IRGC 전쟁 재개 대비 경고. 호르무즈 통항 90%↓(UK Royal Navy 공식). 4.30 Brent $126 역대고. WTI ~$101/Brent ~$108(5.2). $8.6B 중동 무기 긴급판매. 북한: IAEA 핵능력 강화 경고(4.15). 핵보유국 인정 요구. 러시아 잠수함 추진체계 공급 의혹. 트럼프 김정은 면담 희망이나 구체 계획 미확인 | +26 |
| 2026-05-02 | `industry/smr.md` | **SMR/핵융합 정기 갱신(15회 검색)** -- TerraPower **4/23 착공**(인력1,600명/2031완공). X-energy IPO $1.02B(원자력 역대최대/XE첫날+27%/TRISO-X 50년만 최초 연료제조 NRC 라이선스). NRC Part53 최종승인(03/25)+Part57 마이크로리액터 함대일괄(04/27, 심사1년미만, 절감$3.76~11.84B). NuScale 리스크 심화(Fluor 전량매각$2.43B+Citi TP$9+ENTRA1$532M손실). BWXT PCG인수+$174M해군+Q1E $818.6M(+20%). RR-SMR £599M정부대출/DAC 2026말/FID 2029. Oklo $72.70(+182%YoY/NVIDIA-LANL). CFS SPARC 자석설치(18기 중반완료/first plasma late2026). Helion 150M°C D-T(민간최초)+Orion 착공. TAE-TMTG 부지선정 개시. 두산 Q1 OP 2,335억(+63.9%)/수주잔고24.1조(+46%)/TP 89K~150K. i-SMR K-ARDP 2.5조+규제연구반. 빅테크 7사 Ratepayer Pledge. 중국 Linglong One 2026가동. 달원자로 100kW+SR-1 핵추진우주선 | +45 |
| 2026-05-02 | `industry/telecom_next.md` | **6개 서브섹터 주간 갱신** -- Starlink 1180만(SpaceX IPO 초안 04.29), Nokia Q1 EUR4.5B(+4%,AI&Cloud+49%)/Ericsson Q1 유기적+6%, NVIDIA Nokia $1B+Marvell $2B 투자, AI-RAN Alliance 130+사/T-Mobile 필드 트라이얼 예정, AT&T Open RAN 50% 트래픽/Samsung-Vodafone vRAN 음성 성공/Samsung-Rakuten 계약, Qualcomm X105 Rel-19 모뎀(DL14.8Gbps), Amazon Leo 302기 발사/FCC 24개월 연장 미결정, 3GPP TR38.914 60% 완료/TR22.870 승인, KT 해킹(01월) 가입자 23만 이탈/LGU+ 반사이익+8.1%, O-RAN SCAS 보안규격/3GPP-O-RAN 6G 공동 워크숍 | +22 |
| 2026-05-02 | `industry/advanced_materials.md` | **6개 서브섹터 주간 갱신(16회 검색)** -- CNT: OCSiAl 2026 생산 2배→1,000t 목표(TUBALL 전고체 배터리 분산액 포트폴리오), CNT 배터리분산액 시장 $0.81B(CAGR 12%), 글로벌 생산 11,479t·$61K/t, 비용 40% 절감. 그래핀: Adisyn 저온(450C) ALD 그래핀 인터커넥트 시연(04-20), Paragraf 6인치 웨이퍼 상업생산, 그래핀스퀘어 CVD양산공장 세계최초 준공(2025.11), 전자기기시장 $6.39B(2030E). 초전도체: 상압Tc 151K 신기록(휴스턴대, 기존 135K 경신), REBCO 테이프 생산 3배(수요 초과 지속), SPARC 2027 first plasma, 한국-CERN 초전도 선재 공동연구. SiC: Wolfspeed Ch11 91일 탈출(부채$4.6B 제거)+FQ2 $168M 미스, onsemi SiC JFET $115M 인수, SiC 모듈 CAGR 29.2%. GaN: Navitas GTC 800V DC-DC+매출$38M→$122M(2028E), Infineon 8" GaN 650V 가격 압도. 희토류: Nd $215/kg(+45% YTD)/Dy $931/kg(+100%+)/중국외 Dy $1,200-1,500, MP Materials 네바다 HREE+DoD 최대주주, Lynas TX 불확실, Cyclic Materials 리사이클링 C$31M. 정책: 48D 25→35%(OBBB)+BASIC Act 연장 제안, EU CRM센터 2026초 설립, Advanced Materials Act Q4 2026 | +43 |
|------|------|------|-------|
| 2026-05-02 | `industry/quantum.md` | **양자 4개 서브섹터 주간 갱신(12회 검색)** -- IonQ Q1 가이던스 $48-51M+SkyWater FTC 2차요청(04-24). IBM Poughkeepsie 확장(04-29) Heron 16x/25x+Starling 511K sqft 신시설. Rigetti Cepheus-1-108Q GA(04-07) 99.1% 2큐빗. Quantinuum IPO mid-2026+CFO 임명+$1B조달. Cloudflare PQC 2029 합류(Google과 동시 목표). Q-Day 3논문 가속(JVG 5K큐빗). SandboxAQ $5.3B 밸류. Infleqtion DARPA HARQ $2M(Multistaq)+SPAC $1.8B. 한국 양자클러스터 5개 08월 최종지정 | +17 |
| 2026-05-02 | `industry/capex.md` | **Q1 2026 빅테크 실적(4/29) 반영 CapEx 대폭 상향** -- 4사 합산 $695-725B(기존 $635-665B +$60B), 5사 $745-775B(기존 $660-690B). MSFT $190B(기존 $110-150B, 부품비 $25B). GOOGL $180-190B(Cloud $20B +63%, 백로그 $460B+). META $125-145B(+33% 매출, AH-7%). AMZN $200B(AWS $37.6B +28%, FCF-95%). 2027 $1T+(CNBC). TSMC 2nm 3월 매출시작+Arizona Phase3 착공. SK하이닉스 OP 37.6조(OPM72%, HBM 3년완판). Samsung DS OP 53.7조+HBM4 최초양산. ASML EUR36-40B 상향. DC 자체발전 30%. SMR NRC 건설허가 2026. GS 2026-2031 $7.6T | +14 |
| 2026-05-02 | `industry/space.md` | **우주산업 주간 갱신(14회 검색)** -- Falcon 9 51회(4/30), Starship V3 IFT-12 5/12 발사목표(FAA 대기), SpaceX IPO SEC S-1 4/1 제출+6월 Nasdaq $75B+($1.75T). Starlink Mobile 리브랜딩(DTC 600만+/2500만 목표). Amazon Leo 302기(FCC 24개월 연장 미결정). AST BB 8~10 출하대기(BB32생산). Blue Origin FAA 비행정지 12회계획 차질. Artemis III 지구궤도 테스트로 변경(달착륙->IV 2028). Golden Dome $185B(SBI 비용논란). True Anomaly $650M. LUNR Lanteris $800M 인수(FY26E $900M~$1B). 누리호 5차 단조립 착수 검토 완료 | +11 |
| 2026-04-26 | `industry/science_tech.md` | **과학기술 메타 섹터 deep 갱신(16회 검색)** -- 양자: IBM Heron R2 QEC 10x(1년 앞당김)+IonQ FT 99.99%+PQC $29.95B(2034E)+Xanadu +51%. 바이오: Lilly Foundayo 경구GLP-1 FDA승인(04월)+Insilico-Lilly AI신약 $2.75B. 우주: Falcon9 600착(04-19)+Starship V3 정적점화+2026 250회 궤도발사. 로보틱스: Optimus V3 중반데뷔 확정(04-23)+Figure02 BMW 30K차 1,250hr+Agibot 1만대. SMR/핵융합: CFS SPARC late2026~2027(소폭후퇴)+Helion 외부연구$4M(25개프로젝트). EDA: Siemens Fuse AI Agent 3파전+AI EDA $4.27B. 사이버보안: Glasswing 40개+기관 확대+04-10 섹터 7~14%급락. CapEx: $635~665B(+67~74%) 구체화. 디스플레이: OLED $76.82B+UDC 청색PHOLED. 전고체: QS Eagle Line+SDI 500Wh/kg. R&D: 한국 35.5조(+19.9%)+OECD GBARD -4.1% | +18 |
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
