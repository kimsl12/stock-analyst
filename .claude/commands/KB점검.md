---
description: 🔍 전체 KB 건강 점검. P0~P2 탐지 + 자동 수정 + _index.md 갱신. wiki-linter full 모드 실행.
agent: wiki-linter
---

**KB 전체 건강 점검**을 실행해줘.

## 명령 정보

- **에이전트:** wiki-linter (full 모드)
- **범위:** knowledge-base/ 전체 + knowledge-db/ 정합성 + _index.md 갱신
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

- wiki-linter는 KB 파일을 **읽기 + _index.md 수정**만 수행
- KB 본문 수정은 kb-updater에 위임 (재수집 명령 제안만)
- git commit/push는 리드가 처리
