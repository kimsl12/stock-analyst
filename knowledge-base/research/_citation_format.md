---
title: Research KB — 인용 표준 형식
description: 모든 분석 에이전트가 research KB 인용 시 따르는 표준 형식. 본문·debate-card·contrarian-card 공통.
created: 2026-05-12
last_updated: 2026-05-12
---

# Research KB — 인용 표준 형식

> 모든 에이전트 (business-analyst, momentum-analyst, risk-analyst, global-macro-analyst, briefing-lead) 가 research KB 인용 시 본 형식 강제.

## 기본 형식

```
📄 [유형분류] 출처/저자 (YYYY-MM) — "제목" §섹션 → 핵심 발견(1줄)
```

대괄호 분류로 출처 신뢰도·성격 즉시 인식 가능.

## 유형 분류 8종

| 분류 태그 | 적용 출처 | 예시 |
|---|---|---|
| `[Working Paper]` | NBER, BIS, SSRN, Fed FEDS, 학술 preprint | `[Working Paper] BIS #1183 (2026-03)` |
| `[Journal]` | Nature, NEJM, Lancet, Cell, peer-reviewed journals | `[Journal] Nature Medicine (2026-04)` |
| `[Preprint]` | arXiv, bioRxiv, medRxiv | `[Preprint] arXiv:2603.12345 (2026-03)` |
| `[Conference]` | ISSCC, ASCO, Jackson Hole, Money 20/20 | `[Conference] ISSCC 2026` |
| `[White Paper]` | IEA WEO, BP Outlook, IIF Capital Flows | `[White Paper] IEA WEO 2026 Ch.4` |
| `[Think Tank]` | McKinsey, BCG, CSIS, Brookings | `[Think Tank] McKinsey GI (2026-03)` |
| `[Policy]` | Fed/ECB/BOJ statements, NRC/FDA approvals, BIS reports | `[Policy] FDA Guidance (2026-02)` |
| `[Filing]` | SEC 10-K/13F, DART, 회사 공시 | `[Filing] SEC 13F Q1 2026` |

## 예시 (도메인별)

### 반도체
```
📄 [Conference] ISSCC 2026 — Samsung/Hynix joint "HBM4 16-Hi TSV"
   → yield 78% 달성, 2027 Q1 양산 가시

📄 [Working Paper] NBER #34521 (2026-02) — "Memory Pricing Cycles" §4
   → 공급사 ≥3사 진입 시 24개월 내 마진 -15~20%p
```

### 에너지
```
📄 [White Paper] IEA WEO 2026 Ch.4 — "DC Power Demand Forecast"
   → 2030년 DC 전력 945 TWh, 미국 5개 주 전력 부족

📄 [Policy] US NRC SECY-26-0042 (2026-04) — "SMR Licensing Reform"
   → SMR ESP 결정 기준 단축 18→9개월, 2026 H2 5~10기 결정 예정
```

### 매크로
```
📄 [Working Paper] BIS WP #1247 (2026-03) — "Sticky Inflation in Service Sectors"
   → 서비스물가 끈적함 24개월 지속 시 Fed 정책 금리 +75bp 누적 추가 가능성

📄 [Policy] FOMC Statement (2026-03-19) — Dot Plot revision
   → 2026 말 정책금리 중간값 3.625% (12월 3.875% 대비 -25bp)
```

### 바이오
```
📄 [Journal] NEJM (2026-04) — "Phase 3 SURMOUNT-OSA Trial"
   → GLP-1 비만치료제 OSA 환자 AHI 50%↓, 2026 H2 추가 적응증 가시

📄 [Policy] FDA Press Release (2026-03-22) — Tirzepatide expanded label
   → 비만+OSA 복합 승인, 처방 코드 확대 → 시장 +$8B 추정
```

### 핀테크
```
📄 [Working Paper] BIS WP #1198 (2026-03) — "Stablecoin Reserve Quality"
   → 미국 단기국채 보유 비중 84% — 신규 수요 채널, 차환금리 영향 -3~5bp

📄 [Policy] US SEC Rule 2026-05 — "Crypto Custody"
   → 등록 거래소 의무 분리 보관, 비등록 거래소 진입 장벽 ↑
```

## 인용 위치 룰

### 본문 인용
- 문장 끝에 직접 첨부:
  ```
  HBM4 양산 일정은 ISSCC 2026 발표 기준 2027 Q1 가시화 (📄 [Conference] ISSCC 2026 — yield 78%).
  ```

### debate-card / contrarian-card
- 카드 본문에 출처를 별도 줄로:
  ```markdown
  ## Debate Card: HBM4 양산 시점
  🟢 Bull (2027 Q1): yield 78%, EUV 캐파 확보
     출처: 📄 [Conference] ISSCC 2026 — Samsung/Hynix joint
  🔴 Bear (2028 H1): TSV 양산 라인 EUV 캐파 6개월 지연
     출처: 📄 [Working Paper] TrendForce Q1 백서 (2026-03)
  ```

### 표 안 인용
- 표 마지막 컬럼 또는 표 아래 출처 블록:
  ```markdown
  | 항목 | 데이터 | 출처 |
  |---|---|---|
  | HBM 시장 2030 | $185B | 📄 [Think Tank] McKinsey GI (2026-03) |
  ```

## 자가 검증 룰

분석 에이전트는 산출물 Write 후 자체 grep:
```bash
grep -E "📄 \[(Working Paper|Journal|Preprint|Conference|White Paper|Think Tank|Policy|Filing)\]" {산출물.md}
```

- ≥ 2건 매치 → OK
- 1건 → 권장 기준 미달, "research KB 인용 부족" 마커
- 0건 → "research KB 부재 (해당 섹터 L2 요약 0건)" 명시 후 OK
- 0건이지만 마커 없음 → 위반, 추가 인용 시도

## 환각 방지 룰

- 인용한 URL/페이지/문서는 **본 세션에서 실제 fetch 한 것만** 허용
- WebFetch 실패 → 인용 X (조작 금지)
- KB 에 없는 출처를 "기억"으로 인용 X → 반드시 KB read 또는 WebFetch 후 인용
- 발견 가능한 인용 위반:
  - 페이지/섹션 번호가 부정확
  - URL 가 404
  - 저자명·발행일이 검색 안 됨
  → research-curator 가 분기 1회 인용 검증 수행 (Phase 6 통합 테스트 포함)
