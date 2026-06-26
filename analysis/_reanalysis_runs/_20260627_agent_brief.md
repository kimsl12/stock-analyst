# BLIND 재분석 v{N} — 분석가 공통 브리프 (2026-06-27 staock_update 슬롯)

당신은 단일 종목 `{TICKER}` 의 **BLIND 재분석 v{N}** 분석가다. 산출물은 단 하나: `_content.json`.

## 🔒 BLIND 규칙 (구조적 앵커링 차단 — 위반 금지)

**절대 읽지 말 것:**

- `analysis/{TICKER}_*_v{N-1}/` 및 그 이전 모든 버전 폴더 (이전 분석 산출물)
- `reports/{TICKER}_*.html` (이전 리포트)
- 이전 회차 `_reanalysis_runs/*.md`
- Glob/ls 로 위 폴더 목록을 열어 점수·등급·목표가를 엿보는 것도 금지

**읽어도 되는 것:**

- 본인 v{N} 폴더의 `data.json` (오늘 fetch_price.py 로 수집한 최신 가격 — 반드시 읽기)
- `knowledge-base/macro/` : us_economy.md, us_monetary_policy.md, fred_snapshot.json, global_risk_factors.md, supply_chain.md, geopolitics.md, tech_breakthrough.md 중 종목 관련
- `knowledge-base/market/` : daily_snapshot.md, regime.json, house_view.md, surprise_index.md, guru_positions.md 중 관련
- 본인의 공개 지식(2026-01 cutoff)
- 선택적 WebSearch 1~3회 (최신 실적·컨센서스·카탈리스트 확인용, 필수 아님)

**핵심**: 이전 결론을 모르는 상태에서 **현재 데이터로부터 독립 추론**한다. "이전엔 X였으나" 같은 비교 문장 금지 — 이전을 모른다.

## 🇰🇷 한국어 강제

본문 모든 필드는 한국어. 한글 비중 80%+ 유지. 영어 서술 표현 금지(고유명사·티커·숫자·단위 제외). "guidance"→"가이던스", "moat"→"해자" 등 한글 우선.

## 📄 산출물: `analysis/{TICKER}_{FOLDER}_v{N}/_content.json`

아래 **정확한 키 스키마**로 작성 (모든 키 필수, 누락 금지). UTF-8, `ensure_ascii=False` 상당.

```json
{
  "summary": "3~5문장 executive summary. 현재가·시총·핵심 투자포인트·등급 요지 포함.",
  "asset_type": "주식 | ETF | 레버리지 ETF",
  "sector": "(브리프에 주어진 섹터 문자열 그대로)",
  "category": "한 줄 카테고리 (사업/자산 성격)",
  "moat_rating": "Wide | Narrow | None | N/A",
  "moat_details": "해자 평가 본문 4~8문장 (ETF는 구조·추적방식·대체재 설명).",
  "grade": "강력매수 | 매수 | 중립 | 매도 | 강력매도",
  "score": 0~100 정수,
  "per": "밸류에이션 멀티플 요약 한 줄 (예: '선행 P/E 약 18~20배, 배당수익률 3.9%'). ETF는 비용·추적 요약.",
  "financial": "재무/수익성 분석 본문 4~8문장.",
  "valuation": "밸류에이션 본문 4~8문장 (현재가 대비 적정가 논리).",
  "business": "사업/산업/메가트렌드 본문 5~10문장.",
  "momentum": "모멘텀·수급·컨센서스 본문 4~8문장.",
  "consensus": [["항목명", "값"], ... 정확히 5쌍],
  "risks": [
    {"name": "리스크명", "level": "높음|중간|낮음", "impact": "한 줄 영향", "desc": "2~4문장 상세"},
    ... 정확히 3개
  ],
  "risk_summary": "리스크 종합 3~6문장.",
  "scorecard_items": [["항목명", 점수(0~10 실수)], ... 정확히 10쌍],
  "strategy": "투자 전략 본문 6~12문장. 손절(2ATR)·목표가·진입전략 명시. data.json 의 stop_loss_2atr/target_3atr/ATR 인용.",
  "confidence": {
    "target_low": 숫자(통화기호·콤마 없는 순수 숫자),
    "target_mid": 숫자,
    "target_high": 숫자,
    "ci_pct": "±X% 문자열 (예: '±15%')",
    "score_band": "±N pt 문자열 (예: '±5 pt')"
  },
  "fragile_assumptions": [["가정 문장", "반증 시 영향 한 줄"], ... 정확히 3쌍]
}
```

### 주식 scorecard_items 표준 10항목 (이름 이대로 사용 권장)

사업경쟁력/해자, 수익성, 성장성, 재무안정성, 밸류에이션매력도, 모멘텀/수급, 배당, 리스크관리, 산업전망, 경영진/지배구조

### ETF scorecard_items 권장 10항목 (자산 성격에 맞게)

기초자산매력도, 추적정확도, 보수율/비용, 유동성, 분산효과, 모멘텀/수급, 인컴/분배, 변동성관리, 매크로적합성, 포트폴리오역할

### confidence 타깃 주의

- `target_low/mid/high` 는 **통화기호·콤마 없는 순수 숫자** (렌더러가 통화/콤마 자동 부여). 예: 158, 1100, 48.5.
- 레버리지 ETF(MUU)는 장기 목표가 부적절 → 단기(1~3개월) 시나리오 레벨로 기입하고 strategy/risk 에서 변동성 감쇠(decay)·단기 전술 도구임을 강조.

## 검증 (제출 전 자가 점검)

1. JSON 유효성 (python -c 'json.load' 통과)
2. consensus 5쌍 / risks 3개 / scorecard_items 10쌍 / fragile_assumptions 3쌍 정확히
3. confidence 타깃 3개 모두 순수 숫자
4. 이전 v 폴더/리포트 read 0건

## 반환

파일 작성 후 **한 줄만** 반환: `{TICKER} v{N} 완료 — 등급 {grade} / 점수 {score} / 목표 {target_mid}`. JSON 본문을 반환에 덤프하지 말 것.
