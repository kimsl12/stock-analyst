# Analyst Reports — 디렉토리 + 메타데이터 스키마

## 디렉토리 구조

```
reports/analyst/
├── incoming/                     # 사용자 PDF 드롭존 (처리 후 비워짐)
├── items/                        # 모든 항목 (각 폴더 = 1 리포트)
│   └── {item_id}/
│       ├── meta.json             # 메타데이터 (필수)
│       ├── source.pdf            # 원본 PDF (PDF 입력 시)
│       ├── source.html           # 원본 텍스트 (자동 스크랩 시)
│       └── summary.html          # 요약 페이지 (필수, 인덱스에서 링크)
├── _schema.md                    # 본 문서
└── index.html                    # 자동 생성 (build_analyst_index.py)
```

## item_id 명명 규칙

`{YYYYMMDD}_{Source}_{Target}[_{Slug}]`

- `YYYYMMDD`: 발행일 (8자리)
- `Source`: 영문/숫자만, 첫글자 대문자. 예: `GS`, `JPM`, `MS`, `BoA`, `BlackRock`, `Samsung`, `KIWoom`, `MiraeAsset`, `Bloomberg`, `CNBC`, `Reuters`, `YouTube`
- `Target`: 종목 티커 또는 주제 영문화. 예: `NVDA`, `SP500`, `Semis`, `KOSPI`, `Macro`, `Energy`, `BTC`
- `Slug`: 선택. 동일 Source+Target 중복 시 구분용 (예: `Note`, `Outlook`, `Initiation`)

**예시**:
- `20260507_GS_NVDA_Note`
- `20260507_Samsung_Semis`
- `20260507_Bloomberg_SP500_Kolanovic`
- `20260507_YouTube_Macro_TomLee`

## meta.json 스키마

```json
{
  "item_id": "20260507_GS_NVDA_Note",
  "source": "GS",
  "source_full": "Goldman Sachs",
  "source_type": "ib_official | media | korea_brokerage | youtube | user_upload",
  "date": "2026-05-07",
  "analyst": "David Kostin",
  "target": "NVDA",
  "target_name": "NVIDIA",
  "target_kind": "stock | etf | sector | macro | crypto",
  "title": "NVIDIA — 1분기 실적 후 매수 유지 (한글 번역 권장, 영문 fallback OK)",
  "rating": "Buy | Hold | Sell | Overweight | Equal Weight | Underweight | N/A",
  "target_price": 1450,
  "target_currency": "USD",
  "prior_target_price": 1380,
  "period": "12M | 6M | EOY | N/A",
  "source_url": "https://...",
  "language": "ko",
  "summary_bullets": [
    "1분기 EPS 컨센서스 +12% 상회 (한글 번역 우선, 의미 변질 없는 선)",
    "데이터센터 매출 전년比 +85%",
    "5개 bullet 권장 (각 30~80자, 핵심 메시지 + 목표가 변동 + 핵심 논거 + 핵심 위험 + 결론)"
  ],
  "tags": ["semis", "ai", "datacenter"],
  "has_pdf": true,
  "has_full_html": false,
  "collected_at": "2026-05-07T13:30:00+09:00",
  "license_note": "user_upload | public_official | media_quote_only",
  "ai_assessment": {
    "context": "수집 시점 시장/매크로 컨텍스트 (S&P/VIX/Fed/주요 이벤트 — knowledge-base/market 참고). 1~2 문장.",
    "agreement": "본 리포트의 어느 부분이 우리 분석/매크로 view 와 정합하는가? (구체 종목 v2 분석·브리핑 인용 권장)",
    "divergence": "어느 부분이 어긋나는가? 어느 위험을 간과하는가? 우리 view 와 충돌하면 어떤 근거로?",
    "key_insight": "투자 판단에 가장 의미 있는 한 줄 — 사용자가 이 리포트를 어떻게 활용하면 좋은지.",
    "assessed_at": "YYYY-MM-DD"
  },
  "outcome": null
}
```

### ai_assessment 작성 가이드

**필수 4 필드**: context, agreement, divergence, key_insight. 각 1~3 문장.
- **context**: KB 매크로 (`knowledge-base/market/`, `knowledge-base/macro/`) 와 직전 모닝/이브닝 브리핑 참조. 수집 시점의 지수·VIX·Fed·이벤트.
- **agreement**: 우리 종목 v2 분석 / 브리핑과 정합하는 부분. 구체 evidence 포함 (예: "5/6 IWM v2 78.0과 일치").
- **divergence**: 충돌하는 부분 + 그 이유. 단순 반대 X, 매크로 환경·정책 mismatch 등 구체 근거.
- **key_insight**: 한 줄. 사용자가 어떻게 활용? "tactical bull case" / "logic chain 참고" / "진입 보류" 등.

### outcome (사후 평가용)

발행일로부터 충분한 시간 경과 후 (목표 기간의 50%+) 채움. 데이터 누적 시 /analyst/scoreboard 가 활용.

```json
"outcome": {
  "evaluated_at": "2026-08-07",
  "actual_price": 7820,
  "hit": true,
  "error_pct": 0.26,
  "notes": "12M target 7,800 → 실제 8월 7,820 도달, +0.26% 오차 적중.",
  "thesis_validity": "logic_chain_correct | logic_chain_partial | logic_chain_incorrect"
}
```

## 입력 경로별 처리

| 입력 | 출처 | source_type | license_note |
|------|------|-------------|--------------|
| 사용자 PDF 드롭 | `incoming/*.pdf` → `items/{id}/source.pdf` | user_upload | user_upload |
| GS/JPM/MS 공식 | WebFetch → HTML | ib_official | public_official |
| Bloomberg/CNBC | WebSearch + WebFetch | media | media_quote_only |
| 한국 증권사 PDF | WebFetch (PDF download) | korea_brokerage | public_official |
| YouTube | WebSearch (제목·설명) | youtube | media_quote_only |

## 자동 생성 산출물

- `summary.html`: 헤드라인 + 5-bullet + 목표가 표 + 원본 링크 + (PDF 임베드 또는 full HTML 링크)
- `index.html`: 모든 items/ 의 meta.json 읽고 카드 그리드 렌더 (필터: 날짜·Source·target_kind)

## 쓰기 규칙

- `items/{id}/` 폴더는 한 번 생성하면 불변 — 수정 필요시 새 item_id 발급 (re-issued, addendum 등 Slug)
- `incoming/` 의 PDF는 처리 후 `items/{id}/source.pdf` 로 이동, incoming/ 에서 삭제
- `meta.json` 의 `summary_bullets`, `target_price` 등은 LLM/사용자가 채움 — 자동 추출 실패 시 빈 값 허용
