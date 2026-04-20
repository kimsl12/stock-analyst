# ORCL (Oracle Corporation) — 데이터 시드

> **수집일**: 2026-04-20 | **주가 기준일**: 2026-04-17 종가
> **티커**: ORCL (NYSE) | **본사**: Austin, Texas (2020 이전 실리콘밸리)
> **CEO**: Safra Catz | **CTO/공동 창업자**: Larry Ellison (회장)
> **주의**: 본 파일은 2026-04-20 재분석으로 갱신됨. 이전 4/14 버전 대체.

## 실시간 가격 데이터 (fetch_price.py, 2026-04-20 KST 15:07 수집)

| 항목 | 값 |
|------|-----|
| 현재가 | **$175.06** |
| 전일비 | -1.84% |
| 52주 고가 | $343.01 (ATH 대비 **-49.0%**) |
| 52주 저가 | $120.04 |
| 시가총액 | **$503.5B** |
| 거래량 | 45.1M |
| ATR(14) | $8.44 (4.82%) |
| 2×ATR 손절가 | $158.17 (-9.6%) |
| 3×ATR 목표가 | $200.39 (+14.5%) |

## 주가 맥락 (재분석 트리거)

- **52주 고점 $343에서 약 -49% 하락** 상태
- 2025년 가을 Stargate·xAI 등 메가딜 공시로 급등 → 2026 Q1 매크로 리스크·Mag7 조정에서 가장 크게 피해
- 현재가는 52주 저점 $120 대비 +45.8%
- 4월 중순 이후 AI 클라우드 재평가 구간 진입 (Meta·Amazon AI capex 축소 우려)

## 사업 구성 (FY2025 기준)

- **Cloud Services + License Support**: ~75%
  - OCI (Oracle Cloud Infrastructure) — AI 추론·학습 핵심
  - Fusion Cloud (ERP/HCM SaaS)
  - NetSuite (중소기업 SaaS)
- **Hardware + Services**: ~15%
- **Cloud License + On-Premise**: ~10%

## AI 인프라 피벗 핵심 지표

- **OCI 매출 성장률**: 분기 +50%+ YoY 대기 (Stargate 효과)
- **Stargate 프로젝트** (OpenAI-Oracle-SoftBank-MGX): $500B 4년 계획, Texas Abilene 1차 캠퍼스
- **RPO (Remaining Performance Obligations)**: $130B+ 수준 추정 (기록적)
- **xAI 계약**: Colossus 2 슈퍼컴퓨터 인프라 일부 제공
- **GPU 확보**: NVIDIA H100/H200/Blackwell 수십만 대
- **Meta·ByteDance** AI 클라우드 고객 (13F 및 공시 기반)

## 재무 스냅샷

- 연매출 FY2025: ~$57B
- Operating Margin: ~30% (Non-GAAP)
- Net Debt: $75B+ (매우 높음, AI capex 조달)
- Capex: FY2025 $25B+ → FY2026 $40B+ 가이드
- FCF 압박: AI 투자로 단기 FCF 축소 불가피

## 경쟁 구도

- **AI 클라우드 Big-4**: AWS, Azure, GCP, **OCI** (후발 그러나 가성비 + AI 특화)
- **DB 경쟁**: Snowflake(SNOW), Databricks(비상장), PostgreSQL 오픈소스
- **SaaS ERP**: SAP, Workday(WDAY)
- **SMB SaaS**: Microsoft Dynamics, Salesforce

## 매크로 거시 맥락 (2026-04-20)

- 4/21 호르무즈 휴전 만료 리스크
- 4/22 TSLA Q1 (VIX 트리거)
- 4/28 FOMC (금리경로)
- VIX 17.48 "거짓 안정 5단계"
- 30일 시나리오: A 38% / B 42% / C 20% (B 조정 우세)

## 참조 KB

- `knowledge-base/industry/ai.md` (valid until 2026-05-07)
- `knowledge-base/industry/capex.md` (valid until 2026-05-19)
- `knowledge-base/industry/telecom_next.md` (클라우드 인프라 연관)

## Phase 0 완료 체크

- [x] KB 유효성 확인 (ai·capex 최신)
- [x] fetch_price.py 실시간 주가 수집
- [x] 데이터 시드 작성 완료
- [ ] Phase 1 병렬 분석 대기 (5개 동시, SINGLE MESSAGE)
