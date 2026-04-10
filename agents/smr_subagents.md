SMR 섹터용 서브에이전트 구성 (설계)

- **Market-Agent (시장 수집):** IAEA, DOE, ITER, 정부 프로그램, 정책·규제·시장 데이터 수집
- **Company-Agent (기업 수집, 병렬):** NuScale, Rolls‑Royce SMR, KHNP/KAERI, Terrestrial Energy, X‑Energy, private fusion firms 등 기업별 IR·보도자료·계약공고 수집
- **Document-Agent (헤드리스 다운로드):** 보도자료·IR·PDF 자동 다운로드, 쿠키/JS 처리, OCR 적용(스캔 PDF) 후 텍스트 추출
- **Aggregator (병합·검증):** 수집 결과 병합, 중복 제거, confidence 산정, `knowledge-db/{sector}_{YYYY}.jsonl` 및 `knowledge-base/industry/{sector}.md` 생성, `knowledge-db/changelog_2026.jsonl` 업데이트, git 커밋·푸시
- **운영 정책:** 자동 수집 실패(Incapsula/Cloudflare/페이월)는 `blocked_sources`로 기록하고 헤드리스 재시도 → 수동 검증 절차로 전환
