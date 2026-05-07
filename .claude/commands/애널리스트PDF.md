---
argument-hint: [--no-deploy]
description: 📄 애널리스트 PDF 처리 — reports/analyst/incoming/ 드롭존의 PDF를 읽고 메타·요약·인덱스 생성. 사용자가 입수한 IB·증권사 정식 리포트 처리용.
agent: analyst-scraper
---

$ARGUMENTS 인자로 **PDF 모드 처리**를 실행해줘.

## 명령 정보

- **모드:** PDF 모드 (analyst-scraper)
- **입력:** `reports/analyst/incoming/*.pdf` (사용자가 직접 드롭한 파일)
- **산출물:** `reports/analyst/items/{id}/{meta.json, source.pdf, summary.html}` + `reports/analyst/index.html` 갱신

## 인자 해석

- 인자 없음 → incoming/ 의 모든 PDF 처리, deploy 자동 실행
- `--no-deploy` → deploy 스크립트 호출 생략 (메타·요약·인덱스만 갱신)

## analyst-scraper 에 전달할 컨텍스트

```
mode: pdf
deploy: true (--no-deploy 없으면)
workflow:
  1. Glob reports/analyst/incoming/*.pdf (대상 발견)
  2. 각 PDF Read → 메타데이터 추출:
     - source / source_full / source_type / license_note=user_upload
     - date (발행일) / analyst / target / target_name / target_kind
     - title / rating / target_price / period / source_url
     - summary_bullets (5개)
     - tags
  3. item_id 결정 (analyst-scraper 가이드 참조)
  4. items/{id}/ 생성 + meta.json Write
  5. .venv/bin/python scripts/process_analyst_pdf.py commit \
       --item-id {id} --pdf reports/analyst/incoming/<file.pdf>
  6. 모두 처리 후:
     a. .venv/bin/python scripts/build_analyst_index.py (자동 호출됨, 재호출 무해)
     b. (deploy=true) bash scripts/deploy_cloudflare.sh
required_extras:
  - 처리 결과 보고 (item_id 리스트 + 각 항목 1줄 요약)
  - PDF 인식 실패 시 사용자에게 명시 (파일명 + 사유)
  - 중복 item_id 발견 시 skip + 알림
```

PDF 파일이 없으면 사용자에게 "incoming/ 비어있음" 알리고 종료.
