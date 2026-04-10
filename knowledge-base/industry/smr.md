---
updated: 2026-04-10
valid_until: 2026-05-10
sector: smr
sources: [IAEA, NEA, US DOE, ITER, World Nuclear Association, NuScale, Rolls-Royce, KAERI, KHNP, CFS, TAE, Helion]
confidence: medium
last_synced_from_db: 2026-04-10
---

# SMR / 핵융합 Knowledge Base

## ★ CURRENT (에이전트는 이 파일의 데이터를 그대로 사용) ★

---

### 요약
- SMR(소형모듈원전)과 상용·파일럿 핵융합은 저탄소 분산전원과 에너지 안보 수요로 관심이 증가하고 있습니다 (IAEA, NEA, US DOE, ITER).
- SMR은 설계별로 모듈당 출력(예: 최대 ~300 MWe)·표준화·검증 수준이 상이하며, 상용화 후보로 NuScale(미국), Rolls‑Royce(UK) 등과 한국의 KAERI/KHNP 사례가 있습니다 (IAEA; NuScale; Rolls‑Royce; KAERI).
- 핵융합 분야는 ITER 중심의 국제 협력과 민간 기업의 파일럿 개발이 병행되며, 상업적 데모 시점은 기술·규제·자금에 따라 상이합니다 (ITER; CFS; TAE; Helion).

### 주요 출처
- IAEA SMR topic: https://www.iaea.org/topics/small-modular-reactors
- NEA / OECD SMR Dashboard (2025): https://www.oecd-nea.org/upload/docs/application/pdf/2025-09/web_-_smr_dashboard_-_third_edition.pdf
- US DOE Office of Nuclear Energy (SMR): https://www.energy.gov/ne/nuclear-reactor-technologies/small-modular-reactors
- ITER Newsline (fusion progress): https://www.iter.org/newsline
- World Nuclear Association (SMR primer): https://www.world-nuclear.org/information-library/nuclear-fuel-cycle/nuclear-power-reactors/small-nuclear-power-reactors.aspx
- NuScale news: https://www.nuscalepower.com/news
- Rolls‑Royce press releases: https://www.rolls-royce.com/media/press-releases

---

### 핵심 지표
| 항목 | 수치/상태 | 기준/설명 | 출처 |
|------|----------|----------|------|
| IAEA SMR 정의 및 설계 수 | up to ~300 MWe/module; >80 designs(요약) | IAEA 정의·설계 카탈로그 | https://www.iaea.org/topics/small-modular-reactors |
| NEA SMR Dashboard(2025) | 기술·경제 지표 요약 | OECD-NEA 보고서(대시보드) | https://www.oecd-nea.org/upload/docs/application/pdf/2025-09/web_-_smr_dashboard_-_third_edition.pdf |
| 미국 DOE 프로그램 | 자금·데모 지원·규제 engagement | DOE Office of Nuclear Energy 자료 | https://www.energy.gov/ne |
| NuScale 상태 | 규제·배치 진행 중(미국 사례) | 기업 보도자료·규제 제출 문서 | https://www.nuscalepower.com/news |
| Rolls‑Royce SMR | UK 컨소시엄·파일럿 계획 | 기업·영국 정부 문서 | https://www.rolls-royce.com/media/press-releases |
| 핵융합(ITER) 진행 | 건설·시운전 마일스톤 | ITER 공식 업데이트 | https://www.iter.org/newsline |
| 민간 핵융합사 | 파일럿·자금 진행(예: CFS, TAE, Helion) | 기업 뉴스·보도자료 | https://cfs.energy/, https://tae.com/, https://www.helionenergy.com/ |

---

### SMR 수집 스냅샷 (2026-04-10)
- Playwright 수집: `scripts/collect_smr_playwright.py` 실행 — 결과: `artifacts/smr_playwright_20260410_163618/smr_playwright_results.json` (HTML/PDF 아티팩트 및 차단/수동목록 포함).
- 자동 파서로 후보 14건이 `knowledge-db/smr_2026.jsonl`에 추가되었습니다(후보 상세: `artifacts/smr_playwright_20260410_163618/smr_parsed_candidates.json`).

### 권장 작업
- (우선) 핵심 PDF/IR에서 핵심 수치(설계출력, 라이선싱 단계, 계약·금액, 데모 타임라인)를 추출하여 표로 정리하고 각 수치에 출처 링크를 연결하세요 (우선순위: NEA, IAEA, DOE, 기업 IR).
- 자동 정규화: 숫자·단위(예: MWe, MW, MWe/module), 날짜(ISO) 표준화 스크립트 적용.
- 신뢰도 설정: `confidence` 필드 자동 산출 규칙 적용(원본 유형·직접다운로드 여부·중복 교차 검증).
- 검토 워크플로우: 자동 후보(CSV/MD) 생성 → 담당자(인간) 검토 → 승인된 레코드만 `knowledge-db/*.jsonl`에 merge 후 changelog 기록.

---

### 변경 이력 / 참고
- 자동 수집·파서 결과 및 KB 레코드는 `knowledge-db/smr_2026.jsonl`와 `knowledge-db/changelog_2026.jsonl`에 기록되어 있습니다.

