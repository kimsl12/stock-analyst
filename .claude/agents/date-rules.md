# 날짜 참조 규칙 (Date Handling SSOT) [v3.10.1]

> **적용 대상**: kb-updater, briefing-lead, global-macro-analyst, market-data-collector,
> stock-analyst-lead, 기타 모든 서브에이전트 (Read/Write/Edit 시 날짜 필드 취급)
>
> 이 파일은 SSOT다. 각 에이전트는 이 규칙을 참조하며, 규칙 본문은 중복 정의 금지.

---

## ⚠️ 최우선 규칙: 현재 날짜는 반드시 Bash `date`로 확정

**모든 파일 Write/Edit 전에 현재 날짜를 Bash 명령으로 확인하고, 그 값만 사용한다.**

```bash
TODAY=$(date +%Y-%m-%d)
```

이후 파일에 쓰는 모든 날짜 필드는 `$TODAY` 또는 그에서 파생된 값만 사용한다.

### 사용처 예시

| 사용처 | 값 |
|-------|---|
| YAML frontmatter `updated:` | `$TODAY` |
| YAML frontmatter `valid_until:` | `$TODAY + 30일` (업데이트 주기에 따라 조정) |
| YAML frontmatter `last_synced_from_db:` | `$TODAY` |
| jsonl 레코드 `date` 필드 | `$TODAY` (수집 시점 기준) |
| changelog 레코드 `date` 필드 | `$TODAY` |
| HTML 리포트 분석일 | `$TODAY` |
| 커밋 메시지 날짜 | `$TODAY` |
| session-bootstrap.md 갱신 항목의 "마지막 작업" 날짜 | `$TODAY` |

### `valid_until` 계산 예시

```bash
TODAY=$(date +%Y-%m-%d)
VALID_UNTIL=$(date -j -v+30d -f "%Y-%m-%d" "$TODAY" "+%Y-%m-%d" 2>/dev/null || \
              date -d "$TODAY + 30 days" "+%Y-%m-%d")
# macOS/Linux 둘 다 동작
```

---

## ❌ 금지 사항 (2026-04-22 사고 재발 방지)

1. **세션 컨텍스트·session-bootstrap.md의 과거 날짜를 "이어서" 추론 금지**
   - ❌ "마지막 KB 갱신: 2026-04-21 이니까 오늘은 2026-04-22다" — 잘못된 추론
   - ✅ `date +%Y-%m-%d` 결과만 신뢰

2. **Claude 내부 knowledge로 "오늘 날짜 추정" 금지**
   - ❌ "훈련 데이터 기준 2026년 초니까..." — 현재 시점 반영 불가
   - ✅ 시스템 명령어 결과만 사용

3. **이전 파일의 날짜를 "복사" 금지**
   - ❌ 다른 KB 파일의 `updated: 2026-04-21` 패턴을 그대로 베끼기
   - ✅ 매번 새로 `date` 실행

4. **시스템 reminder의 "Today's date is X"에만 의존 금지**
   - 이 reminder는 항상 표시되지 않음. 보조용이고, **Bash 검증이 우선**.

---

## 데이터 자체 날짜 vs 수집 날짜 구분

| 필드 | 의미 | 값 |
|------|-----|----|
| jsonl 레코드 `date` | 에이전트가 **수집한 날짜** | `$TODAY` |
| jsonl 레코드 `body`·`headline`·`numbers` 안의 날짜 | **데이터 원본의 발표일** | 원본 출처 날짜 그대로 (예: "2026-04-16 Freddie Mac 발표") |
| jsonl 레코드 `sources_detail` 안의 날짜 | 소스 원문 날짜 | 원본 그대로 |

→ 본문 내부의 "2026-04-16 발표" 같은 사실 데이터는 그대로 유지. **메타 `date` 필드만** `$TODAY` 로 통일.

---

## 강제 검증 (Phase 3 종료 검증 확장) [v3.9+]

파일 Write 완료 후 리드 에이전트는 아래 검증을 수행한다:

```bash
TODAY=$(date +%Y-%m-%d)
# 방금 Write한 파일의 updated 필드가 $TODAY와 일치하는지 확인
grep "^updated:" knowledge-base/industry/{파일명}.md | head -1
# → "updated: $TODAY" 이어야 함

# jsonl 파일의 date 필드도 $TODAY로 시작하는지 확인
head -1 knowledge-db/{파일명}_2026.jsonl | grep -o '"date":"[^"]*"'
# → "\"date\":\"$TODAY\"" 이어야 함
```

불일치 시 **즉시 수정** (sed 또는 Edit) 후 재커밋.

---

## 재발 사례 로그

| 날짜 | 사례 | 원인 |
|------|-----|------|
| 2026-04-22 (실제 2026-04-24) | kb-updater가 real_estate + consumer_retail 신규 생성 시 64개 `date` 필드에 2026-04-22 오기 | `date` 미실행, 세션 컨텍스트 추론 |

향후 사례 발생 시 이 표에 append — 패턴 분석용.
