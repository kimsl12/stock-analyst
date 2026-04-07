---
updated: 2026-04-07
category: reference
type: static
---

# 거물 투자자 추적 대상 8인 (Guru Watchlist)

> **성격:** 변경 드문 정적 명단. 포지션 데이터는 `knowledge-base/market/guru_positions.md` 참조.
> **읽기 권한:** market-data-collector, briefing-lead, briefing-report-generator, global-macro-analyst
> **데이터 소스:** Dataroma, Gurufocus, ValueInvestorsClub, SEC EDGAR 13F

## 추적 대상 8인 (상시 모니터링)

| # | 투자자 | 소속 | 특징 | 주요 스타일 |
|---|--------|------|------|----------|
| 1 | **Warren Buffett** | Berkshire Hathaway | 가치투자 장기 포지션 | 우량 대형주·캐시카우·독점력 |
| 2 | **Ray Dalio** | Bridgewater | 매크로·헤지 전략 | All Weather·리스크 패리티 |
| 3 | **Michael Burry** | Scion Asset Management | 역발상 포지션 | 버블 숏·이벤트 드리븐 |
| 4 | **Cathie Wood** | ARK Invest | 혁신·성장 테마 | 파괴적 혁신·고성장·장기 |
| 5 | **Stanley Druckenmiller** | Duquesne Family Office | 매크로 타이밍 | 집중 베팅·전환점 포착 |
| 6 | **Howard Marks** | Oaktree Capital | 크레딧·리스크 관리 | 수익 안정성·사이클 관리 |
| 7 | **David Tepper** | Appaloosa Management | 경기순환 포지셔닝 | 디스트레스·전환국면 베팅 |
| 8 | **Bill Ackman** | Pershing Square | 집중투자·행동주의 | 소수 종목 대량 보유·현금흐름 |

---

## 거물 투자자 × 모델 포트폴리오 레퍼런스 매핑

> MODULE F(모델 포트폴리오) 제안 시 대가 전략을 레퍼런스로 활용하기 위한 매핑.

| 포트폴리오 유형 | 레퍼런스 투자자/전략 | 참조 요소 |
|---------------|-------------------|---------|
| 🛡️ 안전형 | Harry Browne (Permanent Portfolio) + Ray Dalio (All Weather) | 자산 간 균형·리스크 패리티·인플레이션 헤지 |
| ⚖️ 중립형 | David Swensen (Yale Model) + Warren Buffett (장기 가치) | 대체자산 편입·지역 분산 + 미국 대형 우량주 집중 |
| 🔥 공격형 | Cathie Wood (혁신) + Druckenmiller (집중 베팅) + Burry (역발상) | 파괴적 혁신·확신 종목 집중·역발상 발굴 |
| 💰 배당형 | Buffett (캐시카우) + Howard Marks (수익 안정성) + Ackman (현금흐름) | 연속 배당 증가·FCF 커버리지·안정적 현금 흐름 |

> **주의:** Harry Browne, David Swensen은 역사적 레퍼런스로만 사용 (현역 13F 추적 대상 아님).
> 현역 추적 대상 8인과 구분하여 MODULE F 작성 시 명시할 것.

---

## 컨버전스 시그널 판정 규칙

- **유효 조건:** 2인 이상이 **동일 분기 13F**에서 동일 종목을 같은 방향(매수/매도)으로 움직인 경우
- **무효 조건:** 단순 보유 중복 (변동 없음)은 컨버전스가 아님
- **필수 명시:** 13F 시차 특성상 "이미 지난 신호"임을 반드시 명시 (금지사항 #28)
- **포지션 크기 가중:** 포트폴리오 내 비중 3% 이상인 경우만 시그널로 인정

## 소스 태그 규칙 (13F 인용 시)

```
[Dataroma 13F, 기준: 2026-Q1, 포지션일: 2026-03-31, 공시일: 2026-05-15]
```
