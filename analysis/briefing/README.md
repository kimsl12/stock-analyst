# analysis/briefing/

브리핑 시스템 v3.4 ↔ 종목분석 v2.4 통합 파이프라인의 **중간 산출물 저장소**.

## 역할

`market-analyst` / `macro-analyst` / `guru-analyst` 3개 분석가가 각자의 결과를
하나씩 이 폴더에 저장한다. `briefing-synthesizer` 만이 이 3개를 동시에 읽어
`reports/briefing/daily_briefing_{YYYYMMDD}.md` 한 편으로 통합한다.

## 저장 파일 (각 1편 / 일)

```
analysis/briefing/market_analysis_{YYYYMMDD}.md   ← market-analyst
analysis/briefing/macro_analysis_{YYYYMMDD}.md    ← macro-analyst
analysis/briefing/guru_analysis_{YYYYMMDD}.md     ← guru-analyst
```

## 접근 권한 매트릭스

| 에이전트 | 읽기 | 쓰기 |
|---|---|---|
| market-analyst | 자신의 파일 | `market_analysis_{YYYYMMDD}.md` |
| macro-analyst | 자신의 파일 | `macro_analysis_{YYYYMMDD}.md` |
| guru-analyst | 자신의 파일 | `guru_analysis_{YYYYMMDD}.md` |
| briefing-synthesizer | **3개 모두** | ❌ (reports/briefing/ 만 쓰기) |
| 그 외 모든 에이전트 | ❌ | ❌ |

> **데이터 역류 금지:** 분석가끼리 서로의 산출물을 읽지 않는다. 통합은 오직
> `briefing-synthesizer` 한 곳에서만 일어난다.

## 생명주기

- **생성:** 매 영업일, 3개 분석가가 각자 1편씩 작성
- **유지:** 시계열 누적 (덮어쓰지 않음 — 날짜별 파일 분리)
- **Git:** 커밋하지 않음 (`.gitignore` 또는 작업 파일로 취급). `.gitkeep` 만 추적
- **정리:** 별도 정리 정책 없음 — 디스크 용량 이슈 시 90일 이전 파일 수동 삭제 가능
