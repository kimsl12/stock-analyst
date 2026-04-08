---
argument-hint: <섹터|토픽> [서브섹터1, 서브섹터2, ...]
description: 📚 지정 섹터·토픽의 knowledge-base 를 웹검색으로 갱신. kb-updater 가 knowledge-db/ 에 append + knowledge-base/ CURRENT 덮어쓰기. 브리핑·종목분석과 독립.
agent: kb-updater
---

$ARGUMENTS 를 대상으로 **KB 업데이트** 를 실행해줘.

## 명령 정보

- **에이전트:** kb-updater (Opus)
- **데이터 흐름:** 웹검색 → `knowledge-db/{topic}_YYYY.jsonl` (append, 영구) → `knowledge-base/{industry|macro}/{topic}.md` (CURRENT 덮어쓰기)
- **독립성:** 브리핑 파이프라인·종목분석 파이프라인과 별개. 본 명령은 순수 데이터 축적 전용

## 인자 형식

```
/KB업데이트 <토픽키> [서브섹터 힌트 자유 기술]
```

**예시:**
```
/KB업데이트 quantum (양자컴퓨팅, 양자통신, 양자센서, PQC)
/KB업데이트 space (우주발사체, 위성통신, 우주인터넷, 우주탐사)
/KB업데이트 SMR (SMR/핵융합)
/KB업데이트 semiconductor (HBM4, 2나노, 파운드리, 장비, 소재)
/KB업데이트 ai (LLM, 추론칩, AI에이전트, 엔터프라이즈 도입)
/KB업데이트 battery (리튬가격, EV정책, 고체전지, LFP 점유율)
/KB업데이트 bio_pharma (FDA, GLP-1, ADC, 바이오시밀러)
/KB업데이트 geopolitics (미중 관세, 대만, 중동, 북한)
/KB업데이트 us_economy (CPI, 고용, 소비, Fed 발언)
/KB업데이트 korea_economy (수출, 환율, 금리, 산업동향)
```

## 토픽 키 → 대상 파일 매핑

| 토픽 키 | knowledge-base 대상 | knowledge-db 축적 파일 |
|---|---|---|
| `semiconductor` | `semiconductor.md` (루트) | `semiconductor_{YYYY}.jsonl` |
| `ai` | `industry/ai.md` | `ai_{YYYY}.jsonl` |
| `auto` | `industry/auto.md` | `auto_{YYYY}.jsonl` |
| `energy` | `industry/energy.md` | `energy_{YYYY}.jsonl` |
| `battery` | `industry/battery.md` | `battery_{YYYY}.jsonl` (없으면 생성) |
| `bio_pharma` | `industry/bio_pharma.md` | `bio_pharma_{YYYY}.jsonl` |
| `science_tech` | `industry/science_tech.md` | `science_tech_{YYYY}.jsonl` |
| `quantum` | `industry/science_tech.md` §양자 | `science_tech_{YYYY}.jsonl` (subtag=quantum) |
| `space` | `industry/science_tech.md` §우주 | `science_tech_{YYYY}.jsonl` (subtag=space) |
| `SMR` | `industry/science_tech.md` §SMR/핵융합 | `science_tech_{YYYY}.jsonl` (subtag=smr) |
| `us_economy` | `macro/us_economy.md` | `macro_{YYYY}.jsonl` (tag=us) |
| `us_monetary_policy` | `macro/us_monetary_policy.md` | `macro_{YYYY}.jsonl` (tag=fed) |
| `korea_economy` | `macro/korea_economy.md` | `macro_{YYYY}.jsonl` (tag=kr) |
| `geopolitics` | `macro/geopolitics.md` | `geopolitics_{YYYY}.jsonl` |
| `global_risk_factors` | `macro/global_risk_factors.md` | `macro_{YYYY}.jsonl` (tag=risk) |
| `political_cycle` | `macro/political_cycle.md` | `macro_{YYYY}.jsonl` (tag=politics) |
| `tech_breakthrough` | `macro/tech_breakthrough.md` | `macro_{YYYY}.jsonl` (tag=tech) |
| `supply_chain` | `macro/supply_chain.md` | `macro_{YYYY}.jsonl` (tag=supply) |

> 토픽 키가 위 표에 없으면 kb-updater 가 `industry/{key}.md` 로 간주하고 파일·jsonl 이 없으면 **신규 생성** 한다.

## kb-updater 에 전달할 컨텍스트

kb-updater.md 의 "수동 호출" 규약에 맞춰 다음 형식으로 전달:

```
call_type: manual
sector: {첫 번째 인자 — 위 매핑 표 토픽 키}
sub_sectors: {괄호 안 텍스트를 콤마로 분리한 리스트 — 없으면 빈 배열}
macro_tags: {해당 매핑 표의 tag/subtag — 없으면 빈 배열}
ticker: null
target_year: {오늘 연도 KST}
search_depth: deep   # 15~20회 웹검색
output_targets:
  - knowledge-db/{topic}_{YYYY}.jsonl  (append, subtag 포함)
  - knowledge-base/{industry|macro}/{topic}.md  (CURRENT 덮어쓰기)
  - knowledge-db/changelog_{YYYY}.jsonl  (이 업데이트 1행 기록)
required_quality:
  - 모든 수치·팩트에 [소스] 태그 필수
  - 최소 2개 소스 교차 검증
  - 미수집 항목은 "N/A [사유]" 로 명시
```

## 워크플로 (kb-updater)

1. 토픽 키 → 대상 파일 결정 (위 매핑 또는 신규 생성)
2. 기존 `knowledge-base/{대상}.md` Read → 기존 섹션 구조 파악
3. 서브섹터 힌트를 우선순위로 웹검색 15~20회 (source_registry.md 🟢 등급 우선)
4. 수집 데이터 → `knowledge-db/{topic}_{YYYY}.jsonl` append (날짜·소스·subtag 포함)
5. 최신값 추출 → `knowledge-base/{대상}.md` CURRENT 섹션 덮어쓰기
6. 변경 리포트 1행 → `knowledge-db/changelog_{YYYY}.jsonl`
7. 사용자 보고: 수집 건수, 갱신된 섹션, 실패 항목, 다음 제안

## 실패 처리

- 특정 소스 403/파싱 실패 시 1차/2차 폴백 (market-data-collector 와 동일 규칙)
- 모든 소스 실패 시 해당 서브섹터만 `"N/A [수집실패: 사유]"` 로 표기하고 나머지는 계속 진행
- **브리핑 B 방식과 동일**: 작업 중 사용자 응답 대기 없이 자동 진행, 최종 보고에 실패 내역만 명시

## 사용자 보고 형식

```
📚 KB 업데이트 완료 — {topic_key}

✅ 갱신된 섹션:
- {섹션 1}: {웹검색 N회, 교차검증 M건}
- {섹션 2}: ...

📊 knowledge-db 축적:
- {topic}_{YYYY}.jsonl: +{N}행 (총 {M}행)
- changelog_{YYYY}.jsonl: +1행

⚠️ 수집 실패 (있을 경우):
- {서브섹터}: {사유}

📄 수정 파일:
- [knowledge-base/{industry|macro}/{topic}.md]({절대경로})
- [knowledge-db/{topic}_{YYYY}.jsonl]({절대경로})

🔗 커밋: {git rev-parse --short HEAD}
```

자동 commit/push 는 kb-updater 가 직접 수행 (briefing-lead 경유 금지).
