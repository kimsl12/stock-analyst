---
description: 🔍 전체 KB 건강 점검. P0~P2 탐지 + 자동 수정 + _index.md 갱신. wiki-linter full 모드 실행.
agent: wiki-linter
---

**KB 전체 건강 점검**을 실행해줘.

## 명령 정보

- **에이전트:** wiki-linter (full 모드)
- **범위:** knowledge-base/ 전체 + knowledge-db/ 정합성 + \_index.md 갱신
- **독립성:** 브리핑·종목분석 파이프라인과 별개. 순수 KB 품질 점검 전용

## wiki-linter에 전달할 컨텍스트

```
mode: full
trigger: manual (/KB점검)
scope:
  - P0: FAILED / 만료 / confidence:none / 빈 테이블 탐지
  - P1: 7일 내 만료 / 고아 파일 / KB 간 수치 모순 / analysis/ 아카이브
  - P2: 30일 미갱신 / confidence:low 과다 인용 / 미피드백 scorecard
actions:
  - 자동 수정 가능 항목은 즉시 처리
  - _index.md P0 섹션 갱신
  - 교차 참조 맵 검증
  - session-bootstrap.md 유효 파일 목록 갱신
  - lint_report 생성 및 사용자 보고
```

## 워크플로

```
Step 1: Read _index.md (현재 상태 파악)
Step 2: Read reference/rules_and_constraints.md
Step 3: P0 점검 — FAILED / 만료 / confidence:none
Step 4: P1 점검 — 7일 만료 / 고아 / 모순 / analysis/ 아카이브
Step 5: P2 점검 — 30일 미갱신 / low 과다 인용
Step 6: 자동 수정 실행
Step 7: _index.md P0 섹션 갱신
Step 8: lint_report 출력
Step 9-A: knowledge-db/_lint_history.jsonl append (1행, mode=full)
Step 9-B: node web/scripts/build_readme.mjs --apply (README fence 자동 갱신)
```

## Fallback — wiki-linter agent maxTurns 중단 시 메인 의무 [v3.22 — 2026-05-29 5/17·5/25·5/29 3회 재발 차단]

wiki-linter agent 가 maxTurns 도달 후 메인 (claude code session) 이 핸드오프 받은 경우, 메인은 다음 3종을 **반드시 직접 수행한 뒤 commit/push** 한다. 미수행 시 본 명령은 실패.

```bash
# 1. _lint_history.jsonl append (실존 파일 — 절대 "미존재 convention" 으로 skip 금지)
ls -la knowledge-db/_lint_history.jsonl  # 4행+ 정상
# 마지막 행 형식 참조 후 1행 append:
#   {"date":"YYYY-MM-DD","mode":"full","trigger":"scheduled","p0":N,"p1":N,"p2":N,
#    "auto_fixed":N,"missed":[],"notes":"agent maxTurns 중단 후 메인 핸드오프 마무리"}

# 2. README.md fence 영역 자동 갱신 (build_readme.mjs)
node web/scripts/build_readme.mjs --apply
# fence: <!-- BEGIN AUTOGEN: recent-briefing --> + <!-- BEGIN AUTOGEN: counts -->
# 호출 누락 = 5/17·5/25·5/29 3회 재발 사고와 동일 패턴

# 3. session-bootstrap.md fence 자동 갱신 (build_bootstrap.mjs)
node web/scripts/build_bootstrap.mjs --apply
# fence: <!-- BEGIN AUTOGEN: analyses -->
```

**메인 핸드오프 시 절대 금지**:

- "\_lint_history.jsonl 미존재" 판단 (5/29 사고 — 실제 4행 보유)
- build_readme.mjs / build_bootstrap.mjs 호출 skip (agent 가 안 했어도 메인이 자동 스크립트 호출 의무)
- "안전장치 #7" missed 배열 비워두기 (실패 사실 jsonl 에 기록 안 하면 다음 회차에서 재발 감지 불가)

**검증 의무 (commit 직전)**:

```bash
git diff --stat | grep -E "(README\.md|_lint_history\.jsonl|session-bootstrap\.md)"
# 3종 모두 변경 표시되지 않으면 위 fallback 누락 — commit 보류 후 즉시 보완
```

## 사용자 보고 형식

```
🔍 KB 건강 점검 완료

🔴 P0 (즉시 조치): {N}건
  → [파일명]: {문제} — {권장 조치}

⚠️ P1 (이번 주): {N}건
  → [파일명]: {문제}

📋 P2 (모니터링): {N}건

✅ 자동 수정: {N}건
  → {수정 내용}

📊 KB 전체 현황:
  - 정상: {N}개 / 경고: {N}개 / 실패: {N}개
  - knowledge-db 총 레코드: {N}건
```

## 주의사항

- wiki-linter는 KB 파일을 **읽기 + \_index.md 수정**만 수행
- KB 본문 수정은 kb-updater에 위임 (재수집 명령 제안만)
- git commit/push는 리드가 처리
