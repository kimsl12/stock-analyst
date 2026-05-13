---
title: "SEC Staff Statement (4/13) — 셀프 호스팅 지갑 인터페이스 브로커 미해당"
sector: fintech
topic: sec_self_custody_wallet_broker
date_published: 2026-04-13
date_collected: 2026-05-12
last_updated: 2026-05-12
source_type: Policy
source: "US SEC — Division of Trading and Markets Staff Statement"
url: https://www.sec.gov/newsroom/speeches-statements/peirce-041326-interfacing-our-inner-demons-comments-division-trading-markets-statement-certain-user-interfaces
citation: "📄 [Policy] SEC Staff Statement (2026-04-13) — '셀프 호스팅 지갑 인터페이스 브로커 미해당'"
key_finding: "SEC가 셀프 호스팅(self-custody) 지갑 인터페이스 소프트웨어는 미국 증권법상 broker 정의에 해당하지 않는다는 staff statement 발표 — 디파이·온체인 지갑 사업자 진입 장벽 완화, 3/17 SEC+CFTC 공동 token taxonomy + Atkins 의장 '10년 불확실성 해소' 발언과 연속선, COIN·HOOD·crypto ETF 자금 흐름 채널 확장"
---

# SEC Staff Statement (2026-04-13) — 셀프 호스팅 지갑 broker 미해당

## 핵심 발견 (5건)

- SEC Division of Trading and Markets 가 4/13 staff statement (**"Staff Statement Regarding Broker-Dealer Registration Requirements for Certain User Interfaces Utilized in Connection with Digital Asset Transactions"**) 로 **"Covered User Interface" 제공자는 1934년 증권거래법 broker-dealer 등록 의무에서 면제** 명시.
- **"Covered User Interface" 정의**: 사용자의 **self-custodial 지갑**을 통해 crypto asset securities 거래에 참여하도록 돕는 웹사이트·브라우저 확장·소프트웨어 어플리케이션 (지갑 임베디드 또는 독립 다운로드 형태). 거래소·custodial 지갑은 제외.
- **비-broker 분류 조건 5건+** (Dechert/Carlton Fields/Baker Botts 요약):
  1. **보상 구조**: 거래당 정액 또는 정률 (product-/route-/counterparty-agnostic) — payment for order flow 금지
  2. **default transaction parameter** 정기 재평가 (객관적 factor 기반)
  3. **거래 venue 평가 및 시장 데이터 정확성 audit** 정책 수립
  4. **명시적 disclosure**: SEC 미등록·미규제 사실, 수수료·이해상충·사이버보안·venue 통합 관련 material facts 사용자에게 공개
  5. **특정 거래 권유·투자 추천 금지**, **재량권 행사 금지**
  6. **사용자 자금·증권·스테이블코인 보관·처분·접근 금지**
- **Sunset clause**: 본 statement 는 즉시 효력 발효되나 **5년 한정 (2031-04-14 자동 철회)**, SEC 별도 조치 없을 시. 또한 staff guidance 로 binding rule 아님.
- **3/17 SEC+CFTC 공동 5분류 token taxonomy** + 4/13 본 statement = 미국 디지털 자산 규제 명확화 패턴 — Atkins 의장 (Trump 2기) "10년 불확실성 해소" 정책 방향 일관. SEC v. Coinbase (S.D.N.Y. 2024) 의 self-custodial wallet 비-broker 판결 라인 연장.
- 영향 채널: **COIN** (Coinbase Wallet self-custody 비즈니스 명확화), **HOOD** (crypto self-custody 신규 진입 부담 ↓), 디파이 프로토콜 일반 (Uniswap·Aave 등 프론트엔드 사업자 — staff statement 본문은 특정 platform 명시 X, 일반적 DeFi interface 포함), crypto ETF (IBIT·FBTC·ETHA) 자금 흐름 채널 확장.

## 데이터·근거

| 항목 | 본 staff statement (4/13) 이전 | 이후 |
|---|---|---|
| 셀프 호스팅 지갑 broker 규제 | 모호 (SEC v. Coinbase 2023 케이스 영향) | 명확 (broker 미해당) |
| 디파이 프론트엔드 enforcement 리스크 | 잠재적 (Uniswap 2024 Wells Notice 케이스) | 완화 (단순 UI 는 broker X) |
| 신규 self-custody 진입 장벽 | 높음 (broker 등록 + AML/KYC 부담) | 낮음 (소프트웨어 사업자 일반 규제만) |
| 미국 거래소 self-custody 채널 | COIN 기존 + Robinhood 신규 추진 중 | COIN + HOOD + 신규 진입 가능 |

본 statement 는 staff level 이지만 **enforcement priority 결정에 직접 영향** — SEC 가 셀프 호스팅 지갑 broker 미등록 enforcement 진행 X. 단, **fraud / market manipulation** 적용은 별도 영역 (anti-fraud 규정은 여전 적용).

(SEC.gov 4/13 Commissioner Peirce statement "Interfacing with our Inner Demons" + Dechert OnPoint 2026-04 + Carlton Fields/Baker Botts/WilmerHale 클라이언트 알러트 5월 종합)

## 분석가 활용 가이드 — Bull / Bear / Contrarian

- **Bull case (COIN · HOOD · crypto ETF · 디파이 프론트엔드)**: 셀프 호스팅 채널 명확화 = self-custody 수요 → COIN Wallet 신규 사용자 ARPU 격상. HOOD 의 crypto self-custody 진입 가속. crypto ETF (IBIT·FBTC) self-custody 인출 옵션 확대 → AUM 채널 추가. 디파이 TVL 회복 가능 (2024년 정점 $250B → 2026 5월 ~$180B).
- **Bear case (기존 custodial 채널)**: 셀프 호스팅 채널 확대 시 거래소 custodial 수수료 채널 일부 잠식 — COIN custody 수수료 매출 압력 (단, COIN 의 Wallet 비즈니스 동시 보완 — 전체 효과는 net positive). 또한 self-custody 사고 (개인 키 분실, 피싱) 증가 시 소비자 보호 차원 역풍 가능성.
- **Contrarian (rulemaking 미완 + 정권 교체 리스크)**: 본 staff statement 는 공식 rule 아님 → 차기 SEC 의장 (2028 정권 교체 시) 이 staff guidance 철회 가능성. 또한 **AML/CFT (자금세탁방지)** 측면에서 FinCEN 이 self-custody 지갑 보고 의무 강화 시 효과 일부 상쇄. 디파이 프론트엔드 사업자가 enforcement 안전지대로 인식하기에는 여전히 위험.

## 한계

- staff statement 는 공식 SEC rule 아님 → 법적 구속력 (binding) 미달. 차기 정부·차기 의장 시 철회 가능. 5년 자동 sunset (2031-04-14) — SEC 추가 조치 없을 시 자동 철회.
- 본 statement 는 **broker 정의** 만 다루며, **dealer / exchange / clearing agency** 정의는 별도. 디파이 자동화 마켓메이커 (AMM) 가 exchange 정의에 해당할 가능성 별도 검토 필요.
- 정확한 SEC 본문 URL (staff statement PDF) 은 SEC newsroom 디렉토리 — 본 KB는 Commissioner Peirce 부속 statement URL 인용. Dechert/Carlton Fields/Baker Botts 법률 alert 5월 발행본 7건이 보강 출처.
- 무력화: 2026 Q3-Q4 SEC 공식 rulemaking proposal 발표 시 본 staff statement 내용이 rule 로 정착 (강화) 또는 변경 (약화) 가능.

## 인용 (Citation)

📄 [Policy] SEC Staff Statement (2026-04-13) — "셀프 호스팅 지갑 인터페이스 브로커 미해당" → self-custody 지갑 소프트웨어는 broker 규제 트리거 X = 디파이·온체인 지갑 사업자 진입 장벽 완화

URL: https://www.sec.gov/newsroom/speeches-statements/peirce-041326-interfacing-our-inner-demons-comments-division-trading-markets-statement-certain-user-interfaces (Commissioner Peirce 4/13 부속 코멘트 statement — Division 본문 게재 newsroom 디렉토리)
보조 출처: Dechert OnPoint 2026-04 "SEC Staff Provides Relief for Crypto Wallet Interfaces", Carlton Fields 2026-05 "SEC Staff Clarifies Broker-Dealer Status of Self-Custody Wallet Interface Providers", Baker Botts 2026-05, WilmerHale 2026-04-17 클라이언트 알러트
관련: `knowledge-base/research/fintech/sec_cftc_token_taxonomy_202603.md` (3/17 SEC+CFTC 공동 5분류 token taxonomy), `knowledge-base/research/fintech/stablecoin_bis_papers_170_202605.md` (BIS 글로벌 시각과 미국 규제 명확화의 비대칭), `knowledge-base/industry/financial_services.md`
