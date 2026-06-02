# analysis/\_history/ — 종목별 timeline 저장소

종목 1건 = 파일 1개 (`{ticker}_{name}_timeline.json`). 통합 timeline.json 은
의도적으로 만들지 않는다.

## 설계 의도

| 항목                                      | 이유                                                                                 |
| ----------------------------------------- | ------------------------------------------------------------------------------------ |
| **분산 저장**                             | 종목 추가/삭제 시 다른 종목 파일 무영향 — 동시 갱신 충돌 0                           |
| **통합 뷰는 build_bootstrap.mjs 가 담당** | 전체 aggregate → `session-bootstrap.md` 한 곳에서 통합 표시                          |
| **소비자 4곳**                            | build_bootstrap / cleanup_reanalysis / build_daily_pick / 재분석점검·재분석실행 명령 |
| **평균 2.6 버전 × 112 종목 = 292 entry**  | 단일 파일로 묶어도 1MB 미만 — 분산해도 lookup 비용 무의미                            |

## 갱신 흐름

```
종목 분석 (v 신규) → scorecard.md 작성
   ↓
cleanup_reanalysis.mjs --apply
   ↓
analysis/_history/{ticker}_{name}_timeline.json 갱신 (history append)
   ↓
build_bootstrap.mjs 가 112 파일 read → 통합 후 session-bootstrap.md 갱신
```

## P2-20 종결 메모 (2026-06-02 audit handoff)

audit 의 "통합 timeline.json 부재" 지적은 분산 저장 = 설계 의도임을 모르고
한 표면 관찰. build_bootstrap 가 이미 aggregate 역할 수행 중. 변경 불요.
