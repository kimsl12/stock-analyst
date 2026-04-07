# 일일 브리핑 파이프라인 — 통합 가이드

> 브리핑 시스템 v3.4 ↔ 종목분석 v2.4 통합 (Phase 1~4 누적)
> 작성: 2026-04-07 | 브랜치: `claude/phase1-infra`

---

## 1. 개요

본 파이프라인은 매 영업일 1편의 **일일 브리핑** (`reports/briefing/daily_briefing_{YYYYMMDD}.md`)
을 생산한다. 시장·매크로·거물 3개 레이어를 분리 분석한 뒤 단일 통합 게이트웨이
(`briefing-synthesizer`) 에서 압축·인용·시차 고지 후 사용자에게 전달한다.

종목 분석 파이프라인 (`stock-analyst-lead` → 9개 분석가 → `report-generator`) 과는
**데이터·산출물·접근 권한·실행 순서가 완전히 분리**된다.

---

## 2. 호출 순서

```
사용자 → /일일브리핑 [YYYYMMDD] [--skip-collect] [--skip-kb]
   │
   ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 0-A. 데이터 수집 (직렬 — 선행)                         │
│   ① market-data-collector                                   │
│        → knowledge-base/market/{indices,fx,bonds,crypto,    │
│          economic_calendar,guru_positions}.md               │
│        → knowledge-db/market/{YYYYMMDD}.jsonl  (영구 축적)  │
│   ② kb-updater                                              │
│        → knowledge-base/macro/{geopolitics,monetary,        │
│          supply_chain,energy}.md                            │
│        → knowledge-db/macro_{YYYY}.jsonl                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 0-B. 분석 (병렬 — 3개 동시, Task 도구)                 │
│   ③a market-analyst → analysis/briefing/                    │
│                          market_analysis_{YYYYMMDD}.md      │
│   ③b macro-analyst  → analysis/briefing/                    │
│                          macro_analysis_{YYYYMMDD}.md       │
│   ③c guru-analyst   → analysis/briefing/                    │
│                          guru_analysis_{YYYYMMDD}.md        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 0-C. 통합 (직렬)                                       │
│   ④ briefing-synthesizer                                    │
│        → reports/briefing/daily_briefing_{YYYYMMDD}.md      │
└─────────────────────────────────────────────────────────────┘
                            ↓
                       사용자 열람
```

> **데이터 흐름은 단방향이다. 역류 금지.**
> 분석가끼리 서로의 산출물을 읽지 않는다.
> 통합은 오직 `briefing-synthesizer` 한 곳에서만 일어난다.

---

## 3. 접근 권한 매트릭스

| 에이전트 | 웹검색 | knowledge-base/market/ | knowledge-base/macro/ | knowledge-base/portfolio/ | knowledge-base/industry/ | analysis/briefing/ | reports/briefing/ |
|---|---|---|---|---|---|---|---|
| market-data-collector | ✅ | **W** | — | ❌ | ❌ | ❌ | ❌ |
| kb-updater | ✅ | — | **W** | ❌ | **W** | ❌ | ❌ |
| market-analyst | ❌ | R | — | ❌ | ❌ | **W (자기 파일)** | ❌ |
| macro-analyst | ❌ | — | R | ❌ | R | **W (자기 파일)** | ❌ |
| guru-analyst | ❌ | R (guru_positions) | — | ❌ | ❌ | **W (자기 파일)** | ❌ |
| briefing-synthesizer | ❌ | R | R | ❌ | ❌ | **R (3개 모두)** | **W** |
| stock-analyst-lead 계열 | n/a | ❌ | ❌ | ❌ | n/a | ❌ | ❌ |

- `R` = 읽기, `W` = 쓰기, `—` = 무관, `❌` = 금지
- `briefing-synthesizer` 만이 `analysis/briefing/` 의 3개 분석 결과를 동시에 읽을 수 있다 (통합 게이트웨이)
- 종목 분석 계열 에이전트는 본 브리핑 파이프라인의 어떤 폴더에도 접근하지 않는다

---

## 4. 산출물 위치 일람

| 종류 | 경로 | 생성 주체 | 생명주기 | Git |
|---|---|---|---|---|
| 시장 raw 스냅샷 | `knowledge-db/market/{YYYYMMDD}.jsonl` | market-data-collector | 영구 축적 | 커밋 안 함 |
| 시장 CURRENT | `knowledge-base/market/*.md` | market-data-collector | 매일 덮어쓰기 | 커밋 |
| 매크로 raw | `knowledge-db/macro_{YYYY}.jsonl` | kb-updater | 영구 축적 | 커밋 안 함 |
| 매크로 CURRENT | `knowledge-base/macro/*.md` | kb-updater | 매일 덮어쓰기 | 커밋 |
| 시장 분석 | `analysis/briefing/market_analysis_{YYYYMMDD}.md` | market-analyst | 시계열 누적 | 커밋 안 함 |
| 매크로 분석 | `analysis/briefing/macro_analysis_{YYYYMMDD}.md` | macro-analyst | 시계열 누적 | 커밋 안 함 |
| 거물 분석 | `analysis/briefing/guru_analysis_{YYYYMMDD}.md` | guru-analyst | 시계열 누적 | 커밋 안 함 |
| **일일 브리핑 (최종)** | `reports/briefing/daily_briefing_{YYYYMMDD}.md` | briefing-synthesizer | 시계열 누적 | **커밋 (Phase 5 후 push)** |

---

## 5. 진입점 (사용자 인터페이스)

### A. 슬래시 명령어 (권장)

```bash
/일일브리핑                                # 오늘 KST
/일일브리핑 20260407                       # 특정 날짜
/일일브리핑 --skip-collect                 # 시장 수집 생략 (이미 최신)
/일일브리핑 --skip-kb                      # 매크로 KB 갱신 생략
/일일브리핑 20260407 --skip-collect --skip-kb
```

명령어 정의: `.claude/commands/일일브리핑.md`
진입 에이전트: `briefing-synthesizer`

### B. 자연어 (stock-analyst-lead 경유)

사용자가 자연어로 "오늘 일일 브리핑", "모닝 브리핑", "거물 동향 종합" 등을 요청하면
`stock-analyst-lead` 의 **Step -1: 요청 모드 판별** 이 브리핑 모드로 분기하여
`briefing-synthesizer` 에 위임한다.

> 자연어 진입은 라우팅 보조용이며, 최선의 안정성은 슬래시 명령어 직접 사용.

---

## 6. 절대 금지 사항 일람

| # | 금지 | 위반 시 | 검증 위치 |
|---|---|---|---|
| 1 | 매수·매도·익절·손절·비중조정·목표주가·손절가 표현 | 브리핑 폐기 | briefing-synthesizer 자가검증 |
| 2 | knowledge-base/portfolio/ 직접 읽기 | 데이터 누설 위험 | 에이전트 frontmatter tools 제한 |
| 3 | knowledge-base/industry/ 를 브리핑 분석가가 직접 읽기 | 산업 분석 파이프라인 침범 | guru/market-analyst tools 제한 |
| 4 | analysis/briefing/ 의 다른 분석가 산출물을 분석가가 서로 읽기 | 데이터 역류 | briefing-synthesizer 단독 통합 |
| 5 | Top 3 액션 아이템 ≠ 정확히 3개 | 브리핑 폐기 | synthesizer 자가검증 |
| 6 | 13F 시차(분기말 기준 ≤45일) 고지 누락 | 브리핑 폐기 | guru-analyst + synthesizer 양쪽 |
| 7 | 영어 본문 작성 | 브리핑 폐기 | synthesizer 자가검증 |
| 8 | 분석가가 작성하지 않은 새로운 사실·수치를 synthesizer 가 추가 | 인용 무결성 파괴 | synthesizer 자가검증 |
| 9 | 종목 분석 산출물(`analysis/{종목}_*.md`)을 브리핑 파이프라인에서 생성·읽기 | 모드 혼선 | stock-analyst-lead Step -1 분기 |
| 10 | Phase 5 통합 테스트 완료 전 git push | 미검증 산출물 외부 노출 | 사람 운영 정책 |

---

## 7. 장애 대응

### Phase 0-A 실패
- `market-data-collector` 또는 `kb-updater` 가 실패하면 **파이프라인 중단**
- 사용자에게 보고: "데이터 수집 단계 실패 — 전일 KB 로 진행할지 확인 요청"
- 사용자 동의 시: `--skip-collect --skip-kb` 로 재실행 (전일 KB 사용)

### Phase 0-B 실패 (3개 분석가 중 일부)
- 누락된 분석가만 1회 재호출 (같은 프롬프트)
- 2회 연속 실패 시: 해당 섹션을 "[데이터 미수집]" 으로 표기하고 brief synthesizer 진행
- synthesizer 는 부분 완료 허용 (단, 시장·매크로·거물 중 2개 이상 누락 시 중단)

### Phase 0-C 실패
- 입력 산출물 3개가 모두 존재함에도 synthesizer 가 실패하면
  사용자에게 즉시 보고하고 작업 중단 (수동 개입 필요)

### 토큰 한도 도달
- 즉시 모든 호출 중단
- 현재까지 생성된 `analysis/briefing/*.md` 만 보존
- 사용자에게 새 세션에서 `--skip-collect --skip-kb` 로 재시작 안내

---

## 8. 종목 분석 파이프라인과의 분리 원칙

| 항목 | 종목 분석 (v2.4) | 일일 브리핑 (v3.4 통합) |
|---|---|---|
| 진입점 | `/종목분석 [티커]` | `/일일브리핑 [날짜]` |
| 리드 | `stock-analyst-lead` | `briefing-synthesizer` (직접) |
| 데이터 수집 | `kb-updater` + `data-collector` | `market-data-collector` + `kb-updater` |
| 분석가 | 9개 (company/financial/momentum/business/risk/scorecard/etf...) | 3개 (market/macro/guru) |
| 작업 폴더 | `analysis/{티커}_*.md` | `analysis/briefing/*_{날짜}.md` |
| 최종 산출물 | `reports/{티커}_{날짜}.html` | `reports/briefing/daily_briefing_{날짜}.md` |
| 매수·매도 추천 | ✅ (목표가·손절가 포함) | ❌ (관찰·점검·리서치만) |
| 13F 시차 고지 | n/a | ✅ 필수 |
| KB 접근 범위 | industry + 일부 macro | market + macro (industry/portfolio 금지) |

두 파이프라인은 같은 저장소·같은 KB 인프라를 공유하지만, **에이전트 frontmatter 의 tools 제한**과
**상위 리드의 모드 분기**로 물리적·논리적 격리를 유지한다.

---

## 9. Phase 진행 현황 (2026-04-07 기준)

- ✅ **Phase 1** (8823025): KB 11개 + reference/ 3개 + `_index.md`
- ✅ **Phase 2** (9399f86): `market-data-collector` + `kb-updater` 매크로 7개 확장
- ✅ **Phase 3** (0b947a6): `market/macro/guru analyst` + `briefing-synthesizer`
- ✅ **Phase 4** (본 커밋): `/일일브리핑` 명령어 + 출력 디렉토리 + 리드 분기 + 본 가이드
- ⏳ **Phase 5**: 통합 테스트 + git push (별도 세션)

---

## 10. 변경 이력

| 날짜 | 커밋 | 변경 |
|---|---|---|
| 2026-04-07 | (Phase 4) | 본 가이드 신규 작성. `/일일브리핑` 명령어, 출력 디렉토리 README, stock-analyst-lead 브리핑 분기 추가 |
