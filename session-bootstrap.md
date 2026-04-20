# Session Bootstrap

> **갱신 주체:** stock-analyst-lead (매 작업 완료 후 자동 갱신)
> **읽기 시점:** 모든 세션의 첫 번째 행동으로 Read
> **목적:** 세션 간 연속성 확보

---

## 마지막 작업

| 항목 | 값 |
|------|-----|
| 마지막 종목분석 | 329180 HD현대중공업 - 2026-04-20, Buy 76.2점, 목표 620,000원, 손절 474,392원 |
| 마지막 브리핑 | 모닝브리핑 - 2026-04-20 |
| 마지막 KB 업데이트 | crypto_bitcoin - 2026-04-20 (신규) |
| 진행 중 작업 | 없음 (clean state) |

## analysis/ 유효 파일 (최근 30일)

| 폴더 | 날짜 | 스코어 | 상태 |
|------|------|--------|------|
| 329180_HD현대중공업 | 2026-04-20 | 76.2 Buy (B등급, 복합형, 조선 슈퍼사이클) | 유효 (신규) |
| 012450_한화에어로스페이스 | 2026-04-20 | 81.1 Strong Buy (조건부, K-방산 슈퍼사이클) | 유효 |
| 035420_NAVER | 2026-04-20 | 70.4 Buy (B등급, 복합형) | 유효 |
| ORCL_Oracle | 2026-04-20 | 68.0 Buy (B등급, 조건부) | 유효 (갱신, 4/14 대체) |
| MSTR_Strategy | 2026-04-20 | 49.8 Underweight (D, BTC treasury) | 유효 |
| TQQQ_ProSharesUltraProQQQ | 2026-04-20 | 67.0 Buy (조건부, 단기 전용) | 유효 (ETF) |
| 466100_클로봇 | 2026-04-19 | 73.5 Buy | 유효 |
| LLY_EliLilly | 2026-04-17 | 82.4 Strong Buy | 유효 |
| NVDA_NVIDIA | 2026-04-17 | 81.6 Strong Buy | 유효 |
| BA_Boeing | 2026-04-16 | 74.9 Buy | 유효 |
| KTOS_KratosDefense | 2026-04-16 | 64.0 Weak Buy | 유효 |
| 035720_카카오 | 2026-04-16 | 64.5 Hold | 유효 |
| 009150_삼성전기 | 2026-04-15 | 74.75 Buy | 유효 |
| AVGO_Broadcom | 2026-04-15 | 83.2 Strong Buy | 유효 |
| META_Meta | 2026-04-14 | 80.1 Strong Buy | 유효 |
| PLTR_Palantir | 2026-04-14 | 61.5 Hold | 유효 |
| 010120_LSELECTRIC | 2026-04-13 | 76.5 Buy | 유효 |
| SNDK_Sandisk | 2026-04-13 | 69.0 Buy | 유효 |
| 034020_두산에너빌리티 | 2026-04-13 | 68.0 Buy | 유효 |

## 현재 KB 상태 요약

- **P0 항목**: market/ 전체 FAILED (재수집 필요), us_monetary 중복 해결 예정
- **정상 Industry KB**: 12개 (semiconductor 부재 - advanced_materials, ai 대체 사용)
- **robotics.md 신규 확보** (2026-04-19, valid_until 2026-05-20, confidence high)
- **crypto_bitcoin.md 신규 확보** (2026-04-20, valid_until 2026-05-20, confidence high)
- **정상 Macro KB**: 4개 (us_economy, korea_economy, geopolitics, global_risk_factors)
- **미수집 Macro**: 3개 (political_cycle, tech_breakthrough, supply_chain)
- **방산(defense) 전용 KB 부재 확인** (2026-04-20 012450 분석 시) — space.md + geopolitics.md 간접 활용. 향후 kb-updater에서 defense_industry.md 신규 확보 권장
- **마지막 KB 갱신**: infrastructure 2026-04-13

## 파이프라인 버전

- 종목분석: v3.0 (Write 3턴 규칙 + 시스템 오버라이드 + 폴백 마커)
- KB 업데이트: v3.4 (미니사이클 + 마지막 사이클 통합 + git 리드 위임)
- fetch_price.py: 활성 (pykrx + yfinance)

## ⚠️ 환경 상태 (2026-04-20)

- `.git` HEAD 복구 완료 (HEAD=6ae9cb3, origin/main 동기화 정상)
- GitHub Actions 계정 단위 비활성화 상태(GitHub Support 티켓 #4287825 심사 중) — Pages 자동 배포 중단, push는 정상
- **Agent 도구(sub-agent 호출권) 환경별 가변**: 본 세션(012450)에서는 Task 도구 부재로 리드 직접 수행 모드 적용
- TQQQ 세션은 `af0de677659b6fc0f` 중단 재개 완료

## 012450 한화에어로스페이스 분석 핵심 결과

- 스코어 81.1 (Strong Buy 조건부)
- 목표가 ₩1,600,000 (+12.3%, Bull ₩2,000,000 +40.4%)
- 손절가 ₩1,269,142 (-10.94%, 2x ATR)
- 현재가 ₩1,425,000, 시총 73.2조원, 1Y +92.7%
- 핵심 투자포인트: K9 세계 1위(55%) + Redback 호주 승리 + OPM 20%+ + 미국 진출 옵션
- 단기 촉매: 4/28 Q1 실적, 5~6월 UAE+폴란드3차, 9월 XM30 Phase 2
- 리스크: 우크라 종전(30%), 미 XM30 탈락(45%), 부채비율 220%
- 컨센서스 평균 목표가 ₩1,858,000 (+30.4%), BUY 6/6

## TQQQ ETF 분석 핵심 결과

- 스코어 67.0 (Buy 조건부)
- 목표가 $67.63 (+15.4%, RR 1.8)
- 손절가 $53.57 (−8.6%, 2x ATR)
- 30일 EV −4.59% (A:38% +15.2% / B:42% −10.4% / C:20% −30.0%)
- 최대 보유 60일 (Volatility Decay 연 14.8% 수학적 필연)
- Total Cost of Carry 6.5%/년 (보수 0.84 + 롤오버 1.5 + 스왑금리 4.2)
- High-Risk 이벤트: 4/22 TSLA, 4/24 GOOGL, 4/29 FOMC, 4/30 MSFT+META, 5/1 AAPL+AMZN

---

> 이 파일은 자동 갱신됩니다. 수동 편집하지 마세요.
