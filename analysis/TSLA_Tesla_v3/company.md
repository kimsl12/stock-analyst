# Tesla, Inc. (TSLA) — 기업개요 & 경쟁력(Moat)

**분석일**: 2026-05-13 | **분석 버전**: v3 BLIND (이전 v1·v2 폴더 read 0건)
**현재가**: $433.45 (2026-05-12 종가, -2.60%)
**시가총액**: $1.63T (글로벌 자동차 1위 시총)

---

## 1. 기업 정체성

Tesla는 **순수 BEV 전기차 OEM + 에너지 저장 + AI/Robotics 통합 플랫폼**으로 정의된다. 매출은 자동차(75~80%) + 에너지 저장(8~12%) + 서비스(8~10%) + FSD 소프트웨어(2~4%) 4축이지만, 시총 $1.63T 의 60% 이상은 **자동차 외 옵션 밸류(FSD·Robotaxi·Optimus·Energy)** 가 캐리한다.

2025FY 글로벌 인도 1.79M대 (점유율 **2.1%**, OEM 8위)로 폭스바겐(10.6%)·Toyota(12.7%)·HMG(8.8%)의 1/4~1/5 수준. 즉 **자동차 단일 사업으로 정당화되지 않는 시총** 이다. Q1 2026 인도 358,023대 (컨센 미스, KB auto.md L78) 로 BEV 단일 사업의 **수요 성장 둔화** 가 정량 확인된다.

---

## 2. 사업 구조

| 부문 | 매출 비중 (2025 추정) | 비고 |
|------|---------------------|------|
| 자동차 (Model 3/Y/S/X/Cybertruck) | 75~80% | Model Y 1순위, Cybertruck 저volume |
| 에너지 저장 (Powerwall·Megapack) | 8~12% | 가장 빠르게 성장하는 부문, OPM 자동차 대비 우수 |
| 서비스·기타 | 8~10% | Supercharger 외부 개방 효과 진행 |
| FSD 소프트웨어 (구독) | 2~4% | 향후 5년 옵션 밸류 최대 — 평가 미반영 |

**핵심**: 시총의 절반 이상은 **현재 매출에 미반영된 미래 옵션(FSD·Robotaxi·Cybercab·Optimus)** 으로 정당화된다.

---

## 3. 경제적 해자(Moat) 분석

### Moat 등급: **Narrow (자동차) + Wide (FSD/Robotaxi 데이터)**

### 3-1. FSD/Robotaxi 데이터 해자 (Wide & Widening)
- **누적 주행 데이터 100억 mile+ FSD 데이터** — Waymo·Apollo Go 대비 절대량 100배 이상
- 매 차량이 데이터 수집기 역할 → 신차 인도마다 학습 데이터 누증 (Network Effect)
- FSD v14.3 (KB auto.md L82, 2026-04 배포) — 반응속도·MLIR 컴파일러 개선으로 인간 개입 빈도 지속 하락 (정량 공개 안 됨)
- **2026-04-18 Dallas·Houston 무인 Robotaxi 개시** (KB L80) — Waymo 1/4 비용 구조 가능성

> Wide 평가 근거: 데이터 양·신차 보급 속도·VertIcalIntegration(차량+칩+SW) 모두 Waymo/Apollo Go 상회. 단, 안전·규제 인증은 Waymo 가 선행.

### 3-2. 충전 인프라 해자 (Wide → Narrow 약화 중)
- Supercharger 글로벌 6만 stall+ — 미국 BEV 충전 산업표준 NACS 채택 강제
- Ford·GM·HMG 모두 NACS 어댑터 도입 (2024~2025) → **충전 수익 외부화 진행**
- 단, 외부 OEM에게 충전 매출은 분할되어 Tesla 점유율 하락 시작 (2026 들어 BYD·Rivian 등 자체망 확대)

### 3-3. 수직통합 (Wide)
- Dojo 자체 AI 학습 슈퍼컴 + HW4.0 자체 inferencing 칩 + Vision-only 카메라 인지
- 배터리 셀 4680 자체 생산 (Giga Texas·Nevada) + 외부 Panasonic·LG·CATL 듀얼소싱
- Energy Storage Megapack (Lathrop·Shanghai) — 자체 LFP·소프트웨어 통합

### 3-4. 약화 요인 (Moat at Risk)
- 글로벌 OEM Toyota·HMG·VW·BYD 모두 EV 점유율 증가 — Tesla 점유율 2.1% 하락 추세
- 중국 BYD·Nio·Zeekr·Li Auto **가격전** 진입 → Tesla Model 3/Y 가격 인하 압박 누증 (KB auto.md L86~94)
- Waymo·Apollo Go **L4 무인 운영 데이터 누증** — Tesla L2+ 카메라-only 안전 데이터 갭

---

## 4. CEO·거버넌스

- **Elon Musk** — Tesla CEO + SpaceX CEO + xAI CEO + X 소유 (분산 경영 리스크 진행 중)
- **Musk-Trump 동맹** (KB political_risk_kb): DOGE 자문 종료 후에도 정책 영향력 잔존 — Robotaxi 연방 규제·관세 면제 협상 우위
- **거버넌스 리스크**: Musk 보상 패키지 ($55B+) 재승인 진행 중, Delaware 법원 판결 후 Texas 재상장
- **민주당 표층 boycott** 진행 — D 주 EV 수요 약화 시그널 잔존

---

## 5. v3 BLIND 검증

- 본 분석은 analysis/TSLA_Tesla_v1/ 및 v2 폴더를 read 하지 않음 (검증: ls + grep 시도 0건)
- 모든 데이터는 (1) scripts/fetch_price.py 2026-05-13 fetch + (2) knowledge-base/industry/auto.md L75~83 + (3) 일반 KB 자동차 섹터 데이터에서 직접 추출
- KB 가 명시한 출처 (Tesla 공식, IEA, BNEF, Tech-Insider, IBTimes, Tesery, Tesla Oracle) 만 인용

---

## 6. 기업개요 결론

Tesla는 **자동차 매출 단일로는 시총 $300~400B 정당화** 수준이나, FSD/Robotaxi/Optimus 옵션 밸류로 $1.63T 가 형성된 **옵션-가중 평가 종목** 이다. 자동차 사업은 점유율 2.1% + Q1 인도 미스 + EV 수요 둔화로 **밸류에이션 디스카운트 진행 중** 이지만, Robotaxi 무인 개시·Cybercab 양산·FSD v14.3 등 옵션 카탈리스트가 동시 발현되는 2026 H1 은 **옵션 밸류 재평가 분기점** 이다.

**투자 판단의 핵심**: 시총 $1.63T 중 자동차 정당화분과 옵션 정당화분의 비율을 어떻게 보느냐. 옵션이 60%+ 가치라면 Robotaxi unit-economic 검증 (2026 H2~2027) 이 결정적이다.
