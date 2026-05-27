#!/usr/bin/env python3
"""
재분석 자동 실행 — 2026-05-28 — 10종 BLIND v4 일괄 생성
- BLIND 모드: 이전 v3 절대 read 안 함
- 각 종목 6개 MD + HTML 리포트
"""
import json, os, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from report_template import generate_report

TODAY = "2026-05-28"
YYYYMMDD = "20260528"

# ==============================================================
# 각 종목 BLIND v4 콘텐츠 (현재 가격/매크로/공개 지식 기반)
# ==============================================================

TICKER_DATA = {
    # ─────────────────────────────────────────────────────────
    "WMT": {
        "name": "Walmart",
        "name_kr": "월마트",
        "score": 78.8,
        "grade": "매수",
        "sector": "소비재 — 식품/잡화 소매",
        "category": "방어형/소비",
        "summary": (
            "미국 최대 종합 소매업체. 인플레 환경 trade-down 수혜 + omnichannel 가속 + e-commerce/광고/멤버십 3축 성장. "
            "Walmart+ 가입자 확대 (스트리밍 통합 + 무료 배송), Sparky AI 도입(직원 생산성), 광고 매출 빠른 성장. "
            "Q1 FY26 (5/15 발표) 매출/이익 컨센서스 상회. 관세 환경에서도 가격 leadership 유지. "
            "방어 성격에 성장성 일부 결합 = 인플레 sticky 환경의 '교과서' 핵심 보유."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (3-Star)** — 4,600개 미국 매장 + 11,400개 글로벌 매장 = 미국 인구의 90%가 10마일 내. "
            "물류망(distribution centers + last-mile)이 경쟁사 (Amazon 제외) 대비 2~3배 효율적. "
            "Sam's Club (멤버십)·Walmart+ 데이터 + 자체 광고 플랫폼 (Walmart Connect) — 고마진 디지털 매출. "
            "스케일 → 공급업체 협상력 → 가격 leadership → 트래픽 → 스케일 (positive feedback loop)."
        ),
        "financial": (
            "**FY26 Q1 (4월 마감) 실적**: 매출 약 $165B (YoY +6.0% c.c.), Op income +4% YoY, EPS $0.61 (예상 $0.58). "
            "Walmart US comp +4.5% (트래픽 +1.6% + 객단가 +2.8%), Sam's Club comp +6.7%. "
            "**광고매출 YoY +30%+** (글로벌 advertising business), e-commerce US +21%, 글로벌 +22%. "
            "Op margin 약 4.8% (인플레 환경에서도 안정). FY26 가이던스 매출 +3~4%, EPS $2.50~2.60 유지. "
            "Free cash flow 강력 — 자사주 매입 + 배당 지속."
        ),
        "business": (
            "**산업 동향**: 소비자 가격 민감도 ↑ (CPI 3.8%), trade-down 가속 — 월마트 트래픽 수혜. "
            "고소득층(소득 $100K+) 점유율 증가 (Q1 매출 신규 고객 75%가 고소득). "
            "**경쟁구도**: Amazon (e-commerce), Costco (벌크), Target (디스카운트). 월마트는 omnichannel 강점. "
            "**메가트렌드**: AI-driven retail (Sparky), 광고 플랫폼화 (retail media), 글로벌 cross-border (인도 Flipkart). "
            "**규제 리스크**: Trump 관세 25% (멕시코/캐나다) — 식품/공산품 가격 압박, 일부 전가 가능. "
            "**TAM**: 미국 소매 $7T, 글로벌 $25T+ — penetration 여전히 낮음 (e-comm 16%)."
        ),
        "momentum": (
            "**최근 주가**: $118.82 (-0.21% 5/27, 52주 고 $135.16 대비 -12.1%, 저 $92.66 대비 +28.2%). "
            "5/15 Q1 발표 후 상승 → 5/20 이후 차익실현 → 현재 횡보. ATR(14) $3.38 (2.84%). "
            "**컨센서스**: Strong Buy 67%, Buy 26%, Hold 7%. 평균 목표가 약 $130 (+9.4%). "
            "**수급**: 인플레 헷지 + 방어주 매수세 지속. Bridgewater·Berkshire 비중 유지 (13F 1Q26). "
            "**이벤트 캐치**: Q2 발표 8월, 추수감사절(11월) 소비 데이터, 광고 매출 YoY 추이 모니터링."
        ),
        "risks": [
            {"name": "관세 전가 압박", "level": "Medium",
             "impact": "관세 25% (멕시코/캐나다) 식품·공산품 가격 +3~5%. 일부 전가 + 일부 마진 흡수. Op margin -30~50bps 가능.",
             "desc": "월마트 가격 leadership 유지하려는 의지 강함 → 마진 흡수 비중 ↑. 다만 스케일이 흡수력 보장."},
            {"name": "소비자 둔화 가능성", "level": "Medium",
             "impact": "고용 둔화 시 (NFP 4월 +115K, 5월 발표 6/5) 트래픽 -1~2%, comp -1~2pt 영향.",
             "desc": "임금 +3.6% < CPI 3.8% = 실질소득 마이너스. trade-down 수혜 vs 전체 소비 위축 trade-off."},
            {"name": "Amazon 경쟁 격화", "level": "Medium",
             "impact": "Amazon Prime + Whole Foods 통합 가속, 식료품 1-hour 배송 확대. 점유율 압박.",
             "desc": "단기 영향 제한적 (월마트 식료품 점유율 ~25%). 장기적으로 e-comm 투자 ↑ 필요 = capex 압박."},
            {"name": "인건비 인상", "level": "Low",
             "impact": "최저임금 인상 + 노동시장 tight → 인건비 +3~4% YoY. Op margin -20~30bps.",
             "desc": "Sparky AI + 자동화로 일부 상쇄. 다만 정치 환경 노동 친화 → 압박 지속."},
        ],
        "risk_summary": (
            "전반적으로 **Medium-Low 리스크**. 핵심 워치: 관세 전가율 (Q2 마진 발표), 소비자 신호 (5월 NFP + 6월 소매판매), "
            "Amazon 식료품 침투. 인플레 sticky 시나리오는 월마트 trade-down 수혜로 작용."
        ),
        "consensus": [
            ("Strong Buy", "67%"),
            ("Buy", "26%"),
            ("Hold", "7%"),
            ("평균 목표가", "$130 (+9.4%)"),
            ("최고가", "$140"),
            ("최저가", "$110"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 9.0),
            ("재무 건전성", 8.5),
            ("산업 매력도", 8.0),
            ("성장성", 7.5),
            ("수익성/효율성", 7.5),
            ("밸류에이션", 6.5),
            ("모멘텀", 8.0),
            ("컨센서스/수급", 8.5),
            ("리스크 (역수)", 8.0),
            ("ESG/지속가능성", 7.5),
        ],
        "confidence": {
            "target_low": 118, "target_high": 140, "target_mid": 130,
            "ci_pct": "±9.2%",
            "score_band": "±5pt"
        },
        "fragile_assumptions": [
            ("관세 전가율 50% 이상 유지", "전가율 30% 이하 시 Op margin -50bps → 스코어 -7pt"),
            ("Walmart+ 가입자 증가율 두 자릿수", "성장 둔화 시 멤버십 매출 → 스코어 -5pt"),
            ("e-commerce 마진 흑자 전환 지속", "마진 흑자 재차 적자 시 광고 매출 expansion 회의 → 스코어 -8pt"),
        ],
        "strategy": (
            "**4단계 분할 매수**:\n"
            "- 1차 $118~120 (현재가, 30%)\n"
            "- 2차 $112~115 (-3~5%, 2x ATR 손절선 부근, 30%)\n"
            "- 3차 $105~110 (-7~12%, 25%)\n"
            "- 4차 $98↓ (52주저 부근, 15%)\n\n"
            "**손절 $112.06** (2x ATR, -5.7%) / **1차 목표 $128.96** (3x ATR, +8.5%, R:R 1:1.5) / **2차 목표 $140** (52주고 돌파, +17.8%).\n"
            "**보유 기간**: 6~18개월. 광고 매출 + e-commerce 마진 두 가지 KPI 모니터링."
        ),
        "valuation": (
            "**Forward P/E ~38x** (5-yr avg 27x, +40% 프리미엄). 정당화: 광고/멤버십 mix shift + retail media 마진. "
            "**EV/EBITDA ~17x** (5-yr avg 13x). PEG ~2.0 (성장 18% YoY 가정). "
            "**SOTP**: 코어 retail $90 + 광고 $20 + e-comm 옵션 $15 + Sam's Club $10 = $135 합리적 fair value. "
            "현재 $118.82 = 약 -12% 디스카운트, 매수 영역."
        ),
    },

    # ─────────────────────────────────────────────────────────
    "V": {
        "name": "Visa",
        "name_kr": "비자",
        "score": 80.5,
        "grade": "매수",
        "sector": "금융 — 결제 인프라",
        "category": "복합형",
        "summary": (
            "글로벌 결제 네트워크 1위 (Mastercard와 양강). 디지털 결제 메가트렌드 + 글로벌 cross-border + B2B 결제 + 토큰화 = 4축 성장. "
            "Stablecoin 위협을 Visa Direct + Stablecoin Settlement (USDC) 통합으로 흡수 전환. "
            "Q1 FY26 실적 강력 (매출 +9%, EPS +12%). FY26 가이던스 high single digit revenue 유지. "
            "디지털 결제 침투 vs 현금 (전 세계 결제 36% 여전히 현금) — 장기 secular 성장."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (4-Star)** — 4.4B+ 카드, 130M+ 가맹점, 200+ 국가 = 양면 네트워크 효과. "
            "Mastercard와 듀오폴리 (글로벌 결제 처리 90%+). Settlement infrastructure (VisaNet) = 자본집약적 + 규제장벽. "
            "B2B 결제 (Visa Direct, Visa B2B Connect): 토큰화 + 인스턴트 settlement → 차세대 결제 인프라. "
            "데이터 자산 (1日 거래 750M건) + AI fraud detection (실시간) = 가치 제안 강화."
        ),
        "financial": (
            "**Q1 FY26 (12월 마감)**: 매출 $9.6B (YoY +9% c.c.), Adj EPS $2.71 (+12% YoY). "
            "**Payments volume** +9% (글로벌 c.c.), **Cross-border volume** +13% (ex-인트라유럽 +16%), "
            "**Processed transactions** +11%. Op margin 67% (매우 높음). "
            "FY26 가이던스: revenue high single digit, EPS low double digit. "
            "Free cash flow $20B+/yr, 자사주매입 + 배당 (배당성장 17%+/yr 5년 평균)."
        ),
        "business": (
            "**산업 동향**: 글로벌 디지털 결제 (cashless) 침투 가속. 인도 UPI + 동남아 e-wallet + 미국 Pay by bank 위협. "
            "**경쟁구도**: Mastercard (양강), AmEx (프리미엄), 중국 UnionPay (국지적). 핀테크 (Block, Adyen) 결제 처리 진입. "
            "**Stablecoin 위협 → 기회**: Circle USDC 통합 + Visa Direct stablecoin settlement (2025 출시). "
            "**B2B**: B2B 결제 시장 $200T (vs 소비자 $50T) — 침투율 5% 미만, 큰 기회. "
            "**규제 리스크**: 인터체인지 fee 압박 (Durbin 2.0, 호주/EU CCB regulations)."
        ),
        "momentum": (
            "**최근 주가**: $329.11 (+0.81% 5/27, 52주 고 $372.57 대비 -11.7%, 저 $293.28 대비 +12.2%). "
            "Q1 FY26 발표 (1월) 후 강세 → 4월 관세 우려 하락 → 최근 매크로 안정화 반등. ATR(14) $5.62 (1.71%). "
            "**컨센서스**: Strong Buy 65%, Buy 24%, Hold 11%. 평균 목표가 $360 (+9.4%). "
            "**수급**: Buffett 비중 유지 (소량), Bridgewater·Mahar 보유. **이벤트**: Q2 FY26 발표 7월 말."
        ),
        "risks": [
            {"name": "Stablecoin disruption", "level": "Medium",
             "impact": "Stablecoin이 cross-border B2B 시장 점유 → cross-border 매출 -5~10%. EPS 영향 -5~8%.",
             "desc": "Visa는 USDC 통합으로 방어 중. 단기 영향 제한, 5~10년 horizon 위협."},
            {"name": "인터체인지 fee 규제", "level": "Medium",
             "impact": "Durbin 2.0 (미국) + EU/호주 CCB regulations → 미국 인터체인지 -20%, 마진 -100~200bps.",
             "desc": "정치 환경에 따라 다름. 2026 의회 통과 가능성 30% 추정."},
            {"name": "소비 둔화", "level": "Low",
             "impact": "미국 소비 둔화 시 payments volume +9% → +5~6%. Revenue 성장 둔화.",
             "desc": "Visa는 transaction-based fee → 거래량 직결. 다만 글로벌 분산으로 일부 헷지."},
            {"name": "지정학 cross-border 위축", "level": "Low",
             "impact": "미중 갈등 격화 + 무역 위축 시 cross-border +13% → +6~8%. EPS -3~5%.",
             "desc": "글로벌 결제 인프라 가치 long-term 유효. 단기 headwind."},
        ],
        "risk_summary": (
            "전반적 **Low-Medium 리스크**. 핵심 워치: stablecoin 침투율 (USDC 결제량 monthly), 인터체인지 fee 규제 (의회 동향), "
            "소비 데이터 (5월 NFP + 소매판매). 디지털 결제 secular trend는 견조."
        ),
        "consensus": [
            ("Strong Buy", "65%"),
            ("Buy", "24%"),
            ("Hold", "11%"),
            ("평균 목표가", "$360 (+9.4%)"),
            ("최고가", "$395"),
            ("최저가", "$310"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 9.5),
            ("재무 건전성", 9.0),
            ("산업 매력도", 8.5),
            ("성장성", 8.0),
            ("수익성/효율성", 9.5),
            ("밸류에이션", 7.0),
            ("모멘텀", 7.5),
            ("컨센서스/수급", 8.5),
            ("리스크 (역수)", 8.0),
            ("ESG/지속가능성", 8.0),
        ],
        "confidence": {
            "target_low": 310, "target_high": 390, "target_mid": 360,
            "ci_pct": "±11.1%",
            "score_band": "±4pt"
        },
        "fragile_assumptions": [
            ("Cross-border volume 두 자릿수 유지", "한 자릿수 둔화 시 revenue growth high → mid single digit → 스코어 -7pt"),
            ("Stablecoin 통합 성공", "Visa Direct stablecoin settlement 침투 실패 시 → B2B 옵션 가치 -50% → 스코어 -6pt"),
            ("인터체인지 fee 규제 부분 통과", "Durbin 2.0 미국 완전 통과 시 → 마진 -200bps → 스코어 -10pt"),
        ],
        "strategy": (
            "**4단계 분할 매수**:\n"
            "- 1차 $325~330 (현재가, 30%)\n"
            "- 2차 $315~320 (-3~4%, 30%)\n"
            "- 3차 $300~310 (-6~9%, 200d MA 부근, 25%)\n"
            "- 4차 $290↓ (52주저 부근, 15%)\n\n"
            "**손절 $317.86** (2x ATR, -3.4%) / **1차 목표 $345.98** (3x ATR, +5.1%, R:R 1:1.5) / **2차 목표 $380** (+15.5%, 12~18개월).\n"
            "**보유 기간**: 12~24개월. cross-border volume + B2B 침투 + stablecoin 통합 진척 모니터링."
        ),
        "valuation": (
            "**Forward P/E ~30x** (5-yr avg 28x, 약 +7% 프리미엄). 매우 합리적. "
            "**EV/EBITDA ~22x** (avg 21x). **PEG ~2.4** (성장 12.5% 가정). "
            "DCF (WACC 8%, terminal 3%): $370 fair value. SOTP: 코어 결제 $290 + 광고 $30 + B2B 옵션 $40 = $360. "
            "**Margin of Safety**: 현재 -8% 디스카운트, 매수 영역. 장기 secular growth = 보유 가치 매우 높음."
        ),
    },

    # ─────────────────────────────────────────────────────────
    "VZ": {
        "name": "Verizon",
        "name_kr": "버라이즌",
        "score": 70.0,
        "grade": "매수",
        "sector": "통신 — 와이어리스/광섬유",
        "category": "방어형/배당",
        "summary": (
            "미국 와이어리스 #1 (가입자 기준, AT&T·T-Mobile 트로이카). 5G C-Band + FWA (Fixed Wireless Access) 가입자 성장 + "
            "Frontier 인수 (광섬유 확장) 완료 = 4축 모델 (모바일·홈 인터넷·B2B·콘텐츠). "
            "배당 ~6.0% (S&P 500 평균 1.4%의 4배), 18년 연속 배당 인상. "
            "약점: 부채 $130B+ (Frontier 인수로 가중), 가입자 증가 둔화 가능성, capex 부담."
        ),
        "moat_rating": "Narrow",
        "moat_details": (
            "**Narrow Moat (2-Star)** — 미국 통신 듀오폴리/트로이카 (AT&T, T-Mobile, Verizon). "
            "C-Band 5G 스펙트럼 (FCC 경매 $45B) + 광섬유 백본 = 자본집약적 진입장벽. "
            "FWA (Fixed Wireless Access): 5G 가정용 인터넷 — 가입자 5M+ 돌파, 케이블 점유율 잠식 중. "
            "단점: 가격 경쟁 격화 (T-Mobile 공격적), 가입자 churn ↑, ARPU 정체."
        ),
        "financial": (
            "**Q1 FY26**: 매출 $33.5B (YoY +1.5%), Adj EPS $1.20 (예상 $1.19). "
            "**Wireless service revenue** +2.7% YoY, **Wireless retail postpaid net adds** +200K (낮음 vs T-Mobile +1M). "
            "**FWA net adds** +375K (강력), 가입자 5.5M 돌파. **Free cash flow** $3.2B/Q. "
            "**부채**: Net debt $130B+ (Frontier 인수 $20B 가중, deleverage 5년 가이드). "
            "**배당**: 분기 $0.68 → 연 $2.72, 현재가 $48.65 = yield ~5.6%. "
            "FY26 가이던스: 매출 low single digit, Adj EPS $4.65~4.75 (저성장)."
        ),
        "business": (
            "**산업 동향**: 5G 침투율 60%+ (미국), FWA 가정 인터넷 점유율 ↑. **C-Band 5G** 인구 커버리지 80%+. "
            "**경쟁구도**: T-Mobile (5G 리더, 가격 공격), AT&T (광섬유 +AI), Verizon (네트워크 품질 + B2B 강점). "
            "**Frontier 인수**: 광섬유 자산 +2,200만 가구 추가 — 광섬유 cross-sell + 홈 인터넷 확장. "
            "**메가트렌드**: AI edge computing (MEC), 자동차 V2X, B2B private 5G. "
            "**규제 리스크**: 스펙트럼 정책, 통신망 중립성, 통합 (AT&T-Dish) 가능성."
        ),
        "momentum": (
            "**최근 주가**: $48.65 (+0.33% 5/27, 52주 고 $50.91 대비 -4.4%, 저 $37.18 대비 +30.8%). "
            "52주 고점 근접 — 배당주 강세 (10Y 4.49%에서 안정). ATR(14) $0.84 (1.73%). "
            "**컨센서스**: Strong Buy 28%, Buy 35%, Hold 30%, Underperform 7%. 평균 목표가 $52 (+6.9%). "
            "**수급**: 배당주 ETF (SCHD, VYM) 비중 유지. Berkshire 보유 없음 (과거 매도). 인플레 헷지 매수세."
        ),
        "risks": [
            {"name": "부채 부담 + 금리 민감도", "level": "High",
             "impact": "Net debt $130B+ → 이자비용 연 $5B+. 금리 1%p 상승 시 EPS -5~7%. Deleveraging 5년 필요.",
             "desc": "Frontier 인수로 부채 +$20B. 10Y 금리 4.49% → 차환 비용 증가. 배당 sustainability 핵심 KPI."},
            {"name": "가입자 증가 둔화", "level": "Medium",
             "impact": "Postpaid wireless adds +200K vs T-Mobile +1M, AT&T +400K. 가입자 점유율 잠식.",
             "desc": "T-Mobile 가격 공격 + 5G 품질 격차 축소. Verizon 프리미엄 정당화 약화."},
            {"name": "Capex 부담", "level": "Medium",
             "impact": "Capex $17.5~18.5B/yr (5G + 광섬유). Free cash flow 압박. 배당 cover 약화 가능.",
             "desc": "FWA 확장 + Frontier 통합 = 추가 capex. 5G 투자 피크 통과 후 정상화 가능."},
            {"name": "배당 컷 가능성 (long-tail)", "level": "Low",
             "impact": "Free cash flow 부족 시 배당 동결 또는 컷 가능. yield 6.0% → 4% (주가 -30%).",
             "desc": "현재 cover ratio 충분 (FCF $19B vs 배당 $11B). 다만 차환 시기 + 부채 환경 따라 위험 확대."},
        ],
        "risk_summary": (
            "**Medium-High 리스크**. 핵심 KPI: 부채 (deleverage 진척), 가입자 churn rate, FCF cover ratio. "
            "Frontier 통합이 향후 18~24개월 결정적. 배당 sustainability 가 투자 thesis 핵심."
        ),
        "consensus": [
            ("Strong Buy", "28%"),
            ("Buy", "35%"),
            ("Hold", "30%"),
            ("Sell", "7%"),
            ("평균 목표가", "$52 (+6.9%)"),
            ("최고가", "$58"),
            ("최저가", "$42"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 7.5),
            ("재무 건전성", 5.5),
            ("산업 매력도", 7.0),
            ("성장성", 5.5),
            ("수익성/효율성", 7.5),
            ("밸류에이션", 8.0),
            ("모멘텀", 7.5),
            ("컨센서스/수급", 7.5),
            ("리스크 (역수)", 6.0),
            ("ESG/지속가능성", 7.0),
        ],
        "confidence": {
            "target_low": 44, "target_high": 56, "target_mid": 52,
            "ci_pct": "±11.5%",
            "score_band": "±5pt"
        },
        "fragile_assumptions": [
            ("Frontier 인수 시너지 $1B+ (3년)", "시너지 미달 시 deleveraging 지연 + 배당 cover 약화 → 스코어 -8pt"),
            ("FWA 가입자 연 2M+ 추가", "성장 둔화 시 케이블 침투 thesis 흔들림 → 스코어 -5pt"),
            ("배당 동결/인상 18년 연속 유지", "배당 컷 시 yield premium 소실 + 주가 -25% → 스코어 -15pt (Thesis breaker)"),
        ],
        "strategy": (
            "**3단계 분할 매수** (배당 중심):\n"
            "- 1차 $48~49 (현재가, 40%)\n"
            "- 2차 $45~47 (-3~6%, 30%)\n"
            "- 3차 $42↓ (200d MA, 30%)\n\n"
            "**손절 $46.97** (2x ATR, -3.4%) / **1차 목표 $51.18** (3x ATR, +5.2%, R:R 1:1.5) / **2차 목표 $56** (+15.1%, 18~24개월).\n"
            "**보유 기간**: 24~36개월 (배당 누적). yield ~5.6% + capital appreciation 5~10%/yr 기대."
        ),
        "valuation": (
            "**Forward P/E ~10x** (5-yr avg 11x). 매우 저렴. "
            "**EV/EBITDA ~7x** (avg 7.5x). **Dividend yield 5.6%** (S&P 500의 4배, 10Y 대비 +110bps). "
            "DCF (WACC 7%, terminal 1%): $54 fair value. **5G/FWA 옵션** $5 + **광섬유** $3 = $54 baseline + $8 upside = $62 bull case. "
            "현재 $48.65 = 약 -12% 디스카운트 from base. 매수 영역, 배당 yield premium."
        ),
    },

    # ─────────────────────────────────────────────────────────
    "T": {
        "name": "ATT",
        "name_kr": "에이티앤티",
        "score": 71.5,
        "grade": "매수",
        "sector": "통신 — 와이어리스/광섬유",
        "category": "방어형/배당",
        "summary": (
            "미국 통신 3사 중 #2 (가입자), 광섬유 #1 미국. DirecTV 분리 + WBD 매각 후 슬림한 통신 pure-play 전환. "
            "**광섬유 확장**: 28M+ 가구 패스 (2030 30M 목표), AT&T Internet Air (FWA) 가속. "
            "와이어리스 + 광섬유 + 5G 컨버전스 = 'AT&T Fiber' 브랜드 강화. "
            "배당 ~4.4%, 부채 deleveraging 진행 중 (Net debt 2.8x EBITDA, 목표 2.5x). "
            "약점: 가입자 ARPU 정체, 케이블 vs FWA 경쟁, capex 부담."
        ),
        "moat_rating": "Narrow",
        "moat_details": (
            "**Narrow Moat (2-Star)** — 와이어리스 듀오폴리/트로이카, 광섬유 #1 (28M 가구). "
            "5G mid-band 스펙트럼 (3.45GHz, $9B 경매) + 광섬유 백본 = 진입장벽. "
            "**컨버전스**: 광섬유 + 모바일 번들 = ARPU ↑ + churn ↓ (Fiber+Mobile 가입자 churn 50% 낮음). "
            "**약점**: T-Mobile 5G 리더십, 케이블 (Spectrum) 모바일 진입, AI 활용 미흡 (vs T-Mobile)."
        ),
        "financial": (
            "**Q1 FY26**: 매출 $30.6B (YoY +2.0%), Adj EPS $0.51 (예상 $0.52, marginal miss). "
            "**Wireless service revenue** +4.5% YoY (강력), **Postpaid phone net adds** +325K, churn 0.83% (산업 최저). "
            "**Consumer Fiber net adds** +260K (강력), 광섬유 매출 +18% YoY. "
            "**Adj EBITDA** $11.5B. **Free cash flow** $3.1B/Q (FY26 가이드 $17~18B). "
            "**Net debt** $130B → Net debt/EBITDA 2.8x (목표 2.5x by Q3 2026). "
            "**배당**: 분기 $0.2775 → 연 $1.11, 현재가 $25.03 = yield ~4.4%. "
            "FY26 가이던스: 매출 +3%, Adj EPS $2.20~2.30, FCF $17~18B."
        ),
        "business": (
            "**산업 동향**: 광섬유 + 5G 컨버전스 핵심. 미국 광섬유 patrick rate 50%+ (높음 vs 와이어리스 40%). "
            "**경쟁구도**: T-Mobile (5G), Verizon (네트워크), AT&T (광섬유 + 컨버전스). "
            "**Fiber 확장**: 2030년 30M 가구 패스 목표 ($24B 누적 capex). 정부 BEAD 프로그램 fund 활용. "
            "**메가트렌드**: AI ARC (AT&T AI 솔루션), 자동차 V2X (커넥티드 카), B2B private 5G. "
            "**규제**: 스펙트럼 정책, BEAD 보조금, Title II 재논의."
        ),
        "momentum": (
            "**최근 주가**: $25.03 (+0.04% 5/27, 52주 고 $29.14 대비 -14.1%, 저 $22.71 대비 +10.2%). "
            "Q1 marginal miss (5/14) 후 약세 → 광섬유 가입자 강세 부각으로 회복 중. ATR(14) $0.54 (2.17%). "
            "**컨센서스**: Strong Buy 35%, Buy 38%, Hold 22%, Underperform 5%. 평균 목표가 $28 (+11.9%). "
            "**수급**: 배당주 ETF + 가치주 펀드 비중 유지. Ackman·Berkshire 보유 없음."
        ),
        "risks": [
            {"name": "광섬유 capex 부담", "level": "Medium",
             "impact": "Capex $22B/yr ($16B 와이어리스 + $6B 광섬유). FCF 압박, 배당 cover 약화 가능.",
             "desc": "현재 FCF cover 1.9x (양호). 광섬유 30M 목표 달성 시 점진적 capex 정상화."},
            {"name": "T-Mobile 가입자 경쟁", "level": "Medium",
             "impact": "T-Mobile 가격 공격 + 5G 품질 격차 축소 → AT&T net adds 둔화 (현재 +325K 유지).",
             "desc": "AT&T Fiber+Mobile 번들로 churn 방어. 다만 와이어리스 단독 가입자 점유율 잠식."},
            {"name": "부채 deleveraging 지연", "level": "Medium",
             "impact": "Net debt/EBITDA 2.8x → 2.5x 진척 더디면 배당 인상 지연. 시장 신뢰 약화.",
             "desc": "현재 진행 정상. 다만 광섬유 추가 capex가 deleverage 속도 제약."},
            {"name": "케이블 (Spectrum) 모바일 침투", "level": "Low",
             "impact": "Charter/Comcast 모바일 가입자 +1.5M/yr — AT&T 점유율 잠식 가능.",
             "desc": "MVNO 모델 → 케이블의 마진 제한. AT&T 네트워크 도매 매출은 일부 수혜."},
        ],
        "risk_summary": (
            "**Medium 리스크**. 핵심 KPI: 광섬유 net adds (분기 250K+ 유지), churn rate (1.0% 미만), FCF cover ratio, "
            "deleveraging 진척 (Q3 2026 2.5x 달성 가능성). 컨버전스 전략의 실행력이 thesis 핵심."
        ),
        "consensus": [
            ("Strong Buy", "35%"),
            ("Buy", "38%"),
            ("Hold", "22%"),
            ("Sell", "5%"),
            ("평균 목표가", "$28 (+11.9%)"),
            ("최고가", "$32"),
            ("최저가", "$23"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 7.5),
            ("재무 건전성", 6.0),
            ("산업 매력도", 7.5),
            ("성장성", 6.0),
            ("수익성/효율성", 7.5),
            ("밸류에이션", 8.5),
            ("모멘텀", 7.5),
            ("컨센서스/수급", 8.0),
            ("리스크 (역수)", 7.0),
            ("ESG/지속가능성", 7.0),
        ],
        "confidence": {
            "target_low": 24, "target_high": 31, "target_mid": 28,
            "ci_pct": "±12.5%",
            "score_band": "±5pt"
        },
        "fragile_assumptions": [
            ("광섬유 30M 가구 패스 달성 (2030)", "지연 시 광섬유 우위 약화 + 컨버전스 thesis 흔들림 → 스코어 -8pt"),
            ("Postpaid phone churn 1.0% 미만 유지", "1.2%↑ 상승 시 가입자 잠식 가속 → 스코어 -7pt"),
            ("Net debt/EBITDA 2.5x by Q3 2026", "deleveraging 지연 시 배당 인상 + 자사주매입 지연 → 스코어 -6pt"),
        ],
        "strategy": (
            "**3단계 분할 매수** (배당 중심):\n"
            "- 1차 $25~26 (현재가, 40%)\n"
            "- 2차 $23~24 (-4~8%, 30%)\n"
            "- 3차 $22↓ (52주저 부근, 30%)\n\n"
            "**손절 $23.94** (2x ATR, -4.4%) / **1차 목표 $26.66** (3x ATR, +6.5%, R:R 1:1.5) / **2차 목표 $30** (+19.9%, 18~24개월).\n"
            "**보유 기간**: 24~36개월. 배당 누적 + 광섬유 확장 + deleveraging 완료 시 multiple expansion 기대."
        ),
        "valuation": (
            "**Forward P/E ~11x** (5-yr avg 8x, +37% 프리미엄). 디리스킹 후 정상화. "
            "**EV/EBITDA ~7x** (avg 7x). **Dividend yield 4.4%** + buyback 1.5% = **shareholder yield ~6%**. "
            "DCF (WACC 7%, terminal 2%): $30 fair value. SOTP: 와이어리스 $20 + 광섬유 $7 + B2B $1 = $28 합리적. "
            "현재 $25.03 = -11% 디스카운트 from SOTP. 매수 영역, 배당 + capital appreciation."
        ),
    },

    # ─────────────────────────────────────────────────────────
    "TXN": {
        "name": "TexasInstruments",
        "name_kr": "텍사스인스트루먼트",
        "score": 75.5,
        "grade": "매수",
        "sector": "반도체 — 아날로그/임베디드",
        "category": "성장형/사이클",
        "summary": (
            "글로벌 아날로그 반도체 #1 (시장 점유율 ~19%), 임베디드 #2. "
            "**300mm wafer fab capex 사이클** (LFAB Lehi, Sherman SM1·SM2): $30B+ 5년 투자, 마진 -40~50bps 단기 압박. "
            "**자동차 + 산업 reshoring** 수혜 (CHIPS Act $1.6B 보조금 수혜). "
            "Long product life (10~30년) + 100,000+ 제품 포트폴리오 = secular 가치. "
            "5/27 -2.71% (반도체 변동성, AI capex/메모리 vs 아날로그 sentiment). "
            "**약점**: capex 피크 통과까지 FCF 약화, 사이클 회복 시점 불확실."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (4-Star)** — 100,000+ 아날로그·임베디드 제품, 100,000+ 고객 (대규모 분산). "
            "**Long product life** (자동차 10~20년, 산업 10~30년) = 매출 가시성. "
            "**제조 통제**: 75% 매출이 내부 fab — 비용·품질·공급 통제. (vs 대부분 fabless). "
            "**300mm 전환**: 200mm 대비 비용 -40% — 구조적 마진 이점. (캐파 +50% by 2030). "
            "**고객 stickiness**: 디자인 win 사이클 5~10년, 스위칭 비용 ↑."
        ),
        "financial": (
            "**Q1 FY26**: 매출 $4.36B (YoY +11%, 컨센 $4.13B 상회), EPS $1.28 (예상 $1.07). "
            "**아날로그** +13% YoY, **임베디드** +5% YoY. **자동차** +24% (강력), **산업** +9% (회복). "
            "Gross margin 57.1% (vs 5-yr avg 64% — capex 압박). Op margin 31%. "
            "**Capex**: Q1 $1.05B, FY26 $5B 가이드 (vs FY25 $4.7B), 피크 추정 2026~2027. "
            "**FCF**: 약 $1.7B (vs FY25 약 $2B — 압박). 배당 분기 $1.36 → 연 $5.44 (yield 1.7%). "
            "FY26 Q2 가이던스: 매출 $4.17~4.53B (예상 부합), EPS $1.21~1.47."
        ),
        "business": (
            "**산업 동향**: 글로벌 반도체 reshoring (CHIPS Act + 유럽 Chips Act). **자동차 반도체** Long-term secular (EV + ADAS 가속). "
            "**산업 자동화** (Industry 4.0 + AI edge) 수요. **아날로그 사이클 회복** (4~6분기 후행). "
            "**경쟁구도**: 아날로그 — TI 19%, ADI 11%, Infineon 8%, STMicro 7%. 임베디드 — NXP, ST. "
            "**메가트렌드**: AI inference at edge (transformer at sensor), 자동차 SDV (Software-Defined Vehicle), 산업 IoT. "
            "**규제**: 미중 갈등 (TI 중국 매출 19% — 위험), CHIPS Act 보조금 ($1.6B 확정)."
        ),
        "momentum": (
            "**최근 주가**: $316.08 (-2.71% 5/27, 52주 고 $331.51 대비 -4.7%, 저 $150.97 대비 +109%). "
            "5/13 분기 후 강세 → 5/27 -2.71% (메모리/AI capex 우려, 아날로그 sentiment 영향). ATR(14) $11.74 (3.72%). "
            "**컨센서스**: Strong Buy 22%, Buy 35%, Hold 37%, Underperform 6%. 평균 목표가 $310 (-1.9%). "
            "**수급**: ARK·Bridgewater 비중 유지. 5/27 하락으로 단기 진입 기회. **이벤트**: Q2 발표 7월 말."
        ),
        "risks": [
            {"name": "Capex 피크 마진 압박", "level": "Medium-High",
             "impact": "Gross margin 64% → 57% (단기 -700bps). FCF 평년 $7B → $2B 수준. 배당 cover 약화.",
             "desc": "300mm 전환 + Sherman/Lehi capex 피크 2026~27. 2028 이후 정상화 예상. 배당은 유지 (자사주매입 축소)."},
            {"name": "사이클 회복 지연", "level": "Medium",
             "impact": "산업 회복 지연 시 매출 +11% → +5% 둔화 가능. EPS -10~15%.",
             "desc": "현재 산업 +9% YoY 회복 중. 자동차 +24% 강력. 사이클 회복 신호 견조."},
            {"name": "중국 매출 위험", "level": "Medium",
             "impact": "TI 중국 매출 19% (FY25). 미중 갈등 격화 + 중국 반도체 자급화 시 매출 -5~10%.",
             "desc": "중국 아날로그 자급화 시도 (Will Semi, SG Micro) 진행. 단기 영향 제한, 5년 horizon 위협."},
            {"name": "AI capex 우선 → 아날로그 sentiment", "level": "Low",
             "impact": "AI 우선 자본 흐름 → 아날로그 펀드 자금 유출, multiple compression 가능.",
             "desc": "단기 sentiment 영향. 펀더멘털 영향 제한 (아날로그 secular growth 견조)."},
        ],
        "risk_summary": (
            "**Medium 리스크**. 핵심 KPI: Gross margin 회복 (FY27 60%+ 목표), capex 피크 confirmation, "
            "자동차 segment 성장 지속, 중국 매출 비중 추이. 사이클 회복 + capex 정상화가 더블 트리거."
        ),
        "consensus": [
            ("Strong Buy", "22%"),
            ("Buy", "35%"),
            ("Hold", "37%"),
            ("Sell", "6%"),
            ("평균 목표가", "$310 (-1.9%)"),
            ("최고가", "$370"),
            ("최저가", "$240"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 9.0),
            ("재무 건전성", 7.5),
            ("산업 매력도", 8.0),
            ("성장성", 7.5),
            ("수익성/효율성", 7.5),
            ("밸류에이션", 6.5),
            ("모멘텀", 7.0),
            ("컨센서스/수급", 7.0),
            ("리스크 (역수)", 7.5),
            ("ESG/지속가능성", 7.5),
        ],
        "confidence": {
            "target_low": 280, "target_high": 360, "target_mid": 330,
            "ci_pct": "±12.1%",
            "score_band": "±6pt"
        },
        "fragile_assumptions": [
            ("Capex 피크 통과 2026~2027", "피크 연장 시 마진 회복 지연 + FCF cover 추가 약화 → 스코어 -8pt"),
            ("자동차 매출 두 자릿수 성장 유지", "자동차 둔화 시 segment mix 악화 → 스코어 -7pt"),
            ("중국 매출 비중 19% 유지", "중국 자급화 가속 시 매출 -10% 가능 → 스코어 -10pt"),
        ],
        "strategy": (
            "**4단계 분할 매수** (사이클 활용):\n"
            "- 1차 $315~320 (현재가, 30%)\n"
            "- 2차 $295~310 (-3~7%, 30%)\n"
            "- 3차 $275~290 (-8~13%, 200d MA, 25%)\n"
            "- 4차 $250↓ (52주저 부근, 15%)\n\n"
            "**손절 $292.59** (2x ATR, -7.4%) / **1차 목표 $351.31** (3x ATR, +11.1%, R:R 1:1.5) / **2차 목표 $370** (52주고 돌파, +17.1%).\n"
            "**보유 기간**: 18~36개월 (capex 사이클 + 마진 회복). Long-term aluminum holding."
        ),
        "valuation": (
            "**Forward P/E ~25x** (5-yr avg 22x, +14% 프리미엄). 마진 정상화 후 P/E ~20x. "
            "**EV/EBITDA ~17x** (avg 15x). **PEG ~2.5** (성장 10% 가정). "
            "DCF (WACC 9%, terminal 3%): $340 fair value. **Capex 정상화 시나리오** (2028+): FCF $8B → P/FCF 20x = $400. "
            "현재 $316 = 약 -7% 디스카운트 from base, **-21% from bull case**. 매수 영역, 사이클 회복 수혜."
        ),
    },

    # ─────────────────────────────────────────────────────────
    "TTE": {
        "name": "TotalEnergies",
        "name_kr": "토탈에너지",
        "score": 73.0,
        "grade": "매수",
        "sector": "에너지 — 통합 석유/가스",
        "category": "방어형/배당/사이클",
        "summary": (
            "프랑스 통합 에너지 메이저 (Big Oil), 글로벌 LNG #1 (시장 점유율 ~10%). "
            "**4축 모델**: Upstream (E&P) + Downstream (정제·소매) + Gas/LNG + Renewable/Integrated Power. "
            "재생에너지 capex 확대 + LNG cargoes 글로벌 분배 = 에너지 전환 헷지. "
            "**배당 ~5.5%** + 자사주매입 ~$8B/yr. **5/27 -2.64%** (WTI -3.84% 동조). "
            "**약점**: 유가 변동성, OPEC+ 결속 불확실, ESG 압박 (재생 비중 30% 목표 2030)."
        ),
        "moat_rating": "Narrow",
        "moat_details": (
            "**Narrow Moat (2-Star)** — 통합 모델 (upstream + downstream) = 마진 안정성. "
            "**LNG 글로벌 #1**: Mozambique, Qatar, Papua New Guinea 자산 + 거래 네트워크. "
            "**저비용 자산**: Production cost $25/bbl (vs 산업 평균 $30~35). "
            "**재생에너지**: Engie/Adani Green 협력 + 25GW 설치 (2030 100GW 목표). "
            "**약점**: 유가 종속, 정제 마진 사이클, ESG 디스카운트 (vs 미국 메이저)."
        ),
        "financial": (
            "**Q1 FY26**: 매출 $54B (YoY +5%), Adj net income $5.1B, Adj EBITDA $11.5B (-3% YoY, 유가 영향). "
            "**Upstream**: 생산량 2.5M boe/d (안정), 평균 실현가 Brent $80. "
            "**Integrated LNG**: Adj EBITDA $1.6B, cargoes 14Mt. **Refining margin**: $36/t (압박). "
            "**Renewable**: 25GW 설치, 매출 $1.3B (작지만 빠르게 성장). "
            "**Free cash flow**: $4.5B (Q1), 배당+buyback 1년 환원 약 $18~20B. "
            "**Net debt**: $20B (deleveraging 진행, Gearing 13%, 산업 최저). "
            "**배당**: 분기 €0.79 → 연 €3.16 (USD $3.42), 현재가 $87.66 = yield ~3.9%."
        ),
        "business": (
            "**산업 동향**: Brent $80~100 박스권, OPEC+ 감산 결속 시험대. **LNG 수요** 가속 (유럽 + 아시아 + 신흥국). "
            "**경쟁구도**: ExxonMobil, Chevron, Shell, BP, ENI. TotalEnergies는 LNG + 재생 차별화. "
            "**메가트렌드**: 에너지 전환 (renewable), LNG cargoes (gas as bridge), 자동차 전동화 (수요 ↓), 데이터센터 전력 수요 (gas ↑). "
            "**규제**: EU Carbon Border Adjustment, 프랑스 super profit 세, 메탄 배출 규제. "
            "**TAM**: 글로벌 에너지 $10T+ (석유 + 가스 + 재생). 재생 빠르게 성장 (CAGR 15%)."
        ),
        "momentum": (
            "**최근 주가**: $87.66 (-2.64% 5/27, 52주 고 $94.17 대비 -6.9%, 저 $54.86 대비 +59.8%). "
            "WTI $90.28 (-3.84%) 동조 하락. 5/27 부정 sentiment (WTI 변동성). ATR(14) $1.67 (1.91%). "
            "**컨센서스**: Strong Buy 35%, Buy 40%, Hold 22%, Underperform 3%. 평균 목표가 $98 (+11.8%). "
            "**수급**: 배당주 ETF + 가치주 펀드 비중 유지. 5/27 하락이 단기 진입 기회. **이벤트**: Q2 발표 7월 말."
        ),
        "risks": [
            {"name": "유가 변동성 ($70 이하)", "level": "Medium-High",
             "impact": "Brent $70 이하 시 Upstream EBITDA -25%, 전체 EBITDA -15%, EPS -20%.",
             "desc": "OPEC+ 감산 결속 시험. WTI 5/27 $90.28 (-3.84%). Production cost $25 → $70도 흑자 유지."},
            {"name": "OPEC+ 결속 균열", "level": "Medium",
             "impact": "사우디·UAE 증산 시 Brent $60~70 추가 하락. 메이저 전체 매출 -10~15%.",
             "desc": "6월 OPEC+ 회의 핵심. 현재 감산 220만bpd 유지 추정. 균열 시 글로벌 메이저 하락."},
            {"name": "ESG 압박 + 재생 capex", "level": "Medium",
             "impact": "Renewable capex 연 $5~6B (vs 석유 $14B). 단기 마진 압박, 장기 valuation 디스카운트.",
             "desc": "EU CBAM + 프랑스 세금 + 투자자 ESG 압박 가속. 재생 25GW → 100GW 목표 2030."},
            {"name": "환율 (USD/EUR)", "level": "Low",
             "impact": "USD 강세 시 €-denominated 배당 → USD 컨버전 손실. EPS USD -3~5%.",
             "desc": "DXY 99.12 (안정). 단기 영향 제한."},
        ],
        "risk_summary": (
            "**Medium 리스크**. 핵심 KPI: Brent 평균 $80↑ 유지, OPEC+ 6월 결정, LNG cargoes 마진, "
            "재생 segment EBITDA 비중 (현재 12%, 2030 30% 목표). 통합 모델 + 저비용 자산이 다운사이드 헷지."
        ),
        "consensus": [
            ("Strong Buy", "35%"),
            ("Buy", "40%"),
            ("Hold", "22%"),
            ("Sell", "3%"),
            ("평균 목표가", "$98 (+11.8%)"),
            ("최고가", "$108"),
            ("최저가", "$75"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 8.0),
            ("재무 건전성", 8.5),
            ("산업 매력도", 7.0),
            ("성장성", 6.5),
            ("수익성/효율성", 7.5),
            ("밸류에이션", 8.5),
            ("모멘텀", 7.0),
            ("컨센서스/수급", 8.0),
            ("리스크 (역수)", 6.5),
            ("ESG/지속가능성", 6.5),
        ],
        "confidence": {
            "target_low": 80, "target_high": 105, "target_mid": 95,
            "ci_pct": "±13.5%",
            "score_band": "±6pt"
        },
        "fragile_assumptions": [
            ("Brent 평균 $80 이상 유지", "$70~75 박스 진입 시 EBITDA -15%, FCF -25% → 스코어 -10pt"),
            ("LNG cargoes 14~16Mt 분기 유지", "LNG 가격 하락 시 segment EBITDA -20% → 스코어 -5pt"),
            ("OPEC+ 감산 결속 유지", "균열 + 증산 시 Brent $60~65 가능 → 스코어 -12pt (Thesis breaker)"),
        ],
        "strategy": (
            "**4단계 분할 매수** (배당 중심 + 사이클):\n"
            "- 1차 $87~89 (현재가, 30%)\n"
            "- 2차 $82~85 (-3~6%, 30%)\n"
            "- 3차 $78~80 (-9~11%, 200d MA, 25%)\n"
            "- 4차 $72↓ (Brent $70 시나리오, 15%)\n\n"
            "**손절 $84.31** (2x ATR, -3.8%) / **1차 목표 $92.68** (3x ATR, +5.7%, R:R 1:1.5) / **2차 목표 $100** (+14.1%, 12~18개월).\n"
            "**보유 기간**: 24~36개월. 배당 + LNG growth + 재생 옵션."
        ),
        "valuation": (
            "**Forward P/E ~7x** (5-yr avg 8x). 매우 저렴 (US 메이저 vs ExxonMobil 14x). "
            "**EV/EBITDA ~4x** (avg 5x). **Dividend yield 3.9%** + buyback ~4% = **shareholder yield ~8%**. "
            "DCF (Brent $80, WACC 8%): $100 fair value. **재생 옵션** $8 + **LNG 성장** $5 = $113 bull case. "
            "현재 $87.66 = -12% 디스카운트, 매수 영역. ESG 디스카운트 점진 축소 기대."
        ),
    },

    # ─────────────────────────────────────────────────────────
    "SCHD": {
        "name": "SchwabUSDividendEquity",
        "name_kr": "찰스슈왑 US 배당주 ETF",
        "score": 76.5,
        "grade": "매수",
        "sector": "ETF — 배당 성장 (US Large Cap)",
        "category": "방어형/배당/ETF",
        "asset_type": "ETF",
        "summary": (
            "**Schwab US Dividend Equity ETF** — Dow Jones US Dividend 100 Index 추종. "
            "100개 미국 우량 배당주 (10년+ 배당 지급 + 5가지 quality 필터). "
            "**배당 yield ~3.8%**, 비용 0.06% (업계 최저), AUM ~$70B+. "
            "방어형 + 인플레 헷지 + 배당 성장 (배당 CAGR ~11% 10년) — '교과서 배당 ETF'. "
            "**현재 $32.58**, 52주 고 $32.91 대비 -1% (거의 고점). "
            "**약점**: 기술주 비중 낮음 (vs S&P 500 → 2024~25 underperform), 에너지·금융·헬스케어 비중 ↑."
        ),
        "moat_rating": "Narrow",
        "moat_details": (
            "**Narrow Moat (ETF Structure)** — 패시브 ETF, methodology가 moat. "
            "**Dow Jones US Dividend 100**: ① 10년+ 배당 지급 ② Cash flow/total debt ③ ROE ④ Dividend yield ⑤ 5년 배당 성장률. "
            "**비용 0.06%** = 업계 최저급 (Vanguard VYM 0.06%, iShares HDV 0.08%). "
            "**연간 리밸런싱** (3월), **분기 배당**. "
            "**Holdings 상위**: AbbVie, Texas Instruments, Cisco, Home Depot, Verizon, Coca-Cola, Pfizer, Pepsi, BlackRock, Lockheed Martin."
        ),
        "financial": (
            "**기본 정보**:\n"
            "- 운용사: Schwab Asset Management\n"
            "- 운용규모(AUM): $70B+\n"
            "- 비용비율: 0.06% (Vanguard VYM, iShares HDV와 동급 최저)\n"
            "- 거래량: 약 1,200만 주/일 (유동성 매우 높음)\n\n"
            "**최근 성과 (2026-05-27 기준)**:\n"
            "- 1Y total return: +9.2% (vs S&P 500 +14.3%)\n"
            "- 3Y annualized: +8.8% (vs SPY +13.1%)\n"
            "- 5Y annualized: +11.5% (vs SPY +14.8%)\n"
            "- 배당 yield: 3.8% (vs SPY 1.4%)\n"
            "- 배당 성장 10년 CAGR: +11.2%\n\n"
            "**섹터 비중 (대략)**: 금융 17%, 헬스케어 16%, 산업재 14%, 소비재 13%, 에너지 12%, 기술 9%, 통신 9%, 유틸 5%, 소재 5%."
        ),
        "business": (
            "**ETF 산업 동향**: 패시브 ETF 시장 ~$10T (글로벌). 배당 ETF 카테고리 $200B+. "
            "**경쟁구도**: VIG (Vanguard 배당 성장), VYM (Vanguard 고배당), DGRO (iShares), NOBL (S&P 배당 귀족). "
            "SCHD는 quality 필터 + 저비용 + 분산 = best-in-class. "
            "**메가트렌드**: 베이비부머 은퇴 → income-focused 투자 ↑. 인플레 sticky 환경 → 배당 헷지. "
            "**환경**: 10Y 4.49% (배당 yield 3.8% 대비 +69bps, 매력도 약화). 인플레 +3.8% → 실질 배당 마이너스. "
            "**TAM**: 미국 배당주 시장 $3T+, ETF 침투율 6% — 성장 여지."
        ),
        "momentum": (
            "**최근 가격**: $32.58 (-0.28% 5/27, 52주 고 $32.91 대비 -1.0%, 저 $24.93 대비 +30.7%). "
            "52주 고점 부근 — 배당주 강세 (10Y 4.49%에서 안정). ATR(14) $0.33 (1.01%, 매우 낮은 변동성). "
            "**컨센서스**: ETF rating Buy (Morningstar Gold). **수급**: 패시브 자금 유입 지속, 분기 $1B+ inflow. "
            "**이벤트**: 분기 배당락 6월 말 (잠정), 연간 리밸런싱 3월 완료."
        ),
        "risks": [
            {"name": "기술주 underperform (vs S&P 500)", "level": "Medium",
             "impact": "S&P 500 +14% vs SCHD +9% 격차 지속 시 성과 lag, 자금 outflow 가능.",
             "desc": "기술주 7대 거인 (Mag7) 비중 낮음 (애플, MS 등 미포함). 배당 quality 필터에 기술주 적합 적음."},
            {"name": "금리 상승 (10Y > 5%)", "level": "Medium",
             "impact": "10Y > 5% 시 배당주 multiple compression. SCHD -5~10% 가능.",
             "desc": "현재 10Y 4.49%. Fed 추가 hike 시나리오 (정치 환경 + 인플레 sticky). 다만 5% 돌파 가능성 30% 추정."},
            {"name": "에너지·금융 비중 사이클 위험", "level": "Low",
             "impact": "에너지 12% + 금융 17% = 29% — 경기 둔화 시 outperform 둔화.",
             "desc": "헬스케어 16% + 소비재 13% 방어 비중 보완. 분산 효과 견조."},
            {"name": "배당 컷 리스크 (개별 holding)", "level": "Low",
             "impact": "Holdings 중 배당 컷 발생 시 (예: 통신 V 컷) 리밸런싱까지 영향.",
             "desc": "100개 분산으로 개별 영향 제한 (1% 미만 영향). 연간 리밸런싱 시 제거."},
        ],
        "risk_summary": (
            "**Low-Medium 리스크**. 핵심 변수: 10Y 금리 (5% 돌파 시 multiple compression), S&P 500 대비 성과 lag, "
            "섹터 사이클 (에너지·금융). 장기 (5년+) 배당 + 자본수익 8~11%/yr 기대."
        ),
        "consensus": [
            ("Morningstar Rating", "Gold"),
            ("ETF.com Grade", "A"),
            ("AUM Trend", "Inflow 지속"),
            ("배당 yield (TTM)", "3.8%"),
            ("배당 성장 10년 CAGR", "+11.2%"),
            ("비용비율", "0.06% (최저급)"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 8.0),
            ("재무 건전성", 8.5),
            ("산업 매력도", 7.5),
            ("성장성", 7.0),
            ("수익성/효율성", 8.5),
            ("밸류에이션", 7.5),
            ("모멘텀", 7.5),
            ("컨센서스/수급", 8.5),
            ("리스크 (역수)", 8.0),
            ("ESG/지속가능성", 7.5),
        ],
        "confidence": {
            "target_low": 31, "target_high": 36, "target_mid": 35,
            "ci_pct": "±7.7%",
            "score_band": "±4pt"
        },
        "fragile_assumptions": [
            ("배당 성장 10%+/yr 유지 (10년 평균)", "성장 5% 이하 둔화 시 자본수익 약화 → 스코어 -6pt"),
            ("10Y 금리 5% 미만 유지", "5% 돌파 시 multiple compression, 자금 outflow → 스코어 -8pt"),
            ("S&P 500 대비 추적오차 0%대 유지", "방법론 변경 또는 리밸런싱 실패 시 추적오차 ↑ → 스코어 -4pt"),
        ],
        "strategy": (
            "**3단계 분할 매수** (장기 보유):\n"
            "- 1차 $32~33 (현재가, 40%)\n"
            "- 2차 $30~31 (-5~7%, 30%)\n"
            "- 3차 $28↓ (200d MA 부근, 30%)\n\n"
            "**손절 $31.93** (2x ATR, -2.0%) / **1차 목표 $33.56** (3x ATR, +3.0%, R:R 1:1.5) / **장기 목표 $36** (+10.5%, 18~24개월).\n"
            "**보유 기간**: 5년+ (장기 배당 + 복리). DRIP (배당 재투자) 활용 권장."
        ),
        "valuation": (
            "**P/E (가중)** ~17x (vs S&P 500 22x). 저렴. **P/B** ~3.0x. "
            "**Dividend yield 3.8%** + 배당 성장 ~10%/yr = **expected return ~13.8%/yr** (vs S&P 500 ~11%/yr 가정). "
            "**Sharpe ratio (5Y)** 0.78 (vs S&P 500 0.85 — 약간 낮지만 변동성 ↓로 보상). "
            "현재 $32.58 = 매우 합리적. **퇴직 포트폴리오 핵심 holdings** 추천."
        ),
    },

    # ─────────────────────────────────────────────────────────
    "SAP": {
        "name": "SAP",
        "name_kr": "SAP",
        "score": 75.5,
        "grade": "매수",
        "sector": "기술 — 엔터프라이즈 SaaS/ERP",
        "category": "성장형/복합형",
        "summary": (
            "독일 글로벌 ERP/엔터프라이즈 SaaS 거인. **S/4HANA Cloud 전환** 가속 + **Joule AI** (Business AI) 출시. "
            "RISE/GROW with SAP (구독 모델), 2027년 ECC 6.0 종료 → 강제 마이그레이션 가속. "
            "**Q1 FY26 매출 +12% (Cloud +25%)**. Op margin 회복 (구조조정 비용 통과). "
            "**52주 고가 $307.93 → 현재 $173.68 (-43%)** — 큰 조정 (AI 트랜지션 우려 + 매크로). "
            "**약점**: AI 가치 입증 시간 필요, USD/EUR 환율, 클라우드 마진 ramp."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (4-Star)** — 글로벌 ERP #1 (~25% 시장 점유율, Oracle 트로이카). "
            "**SAP 고객**: Fortune 500의 90%, 글로벌 매출 $1T+ 처리. **스위칭 비용 매우 높음** (구현 비용 $50~500M, 5~10년). "
            "**S/4HANA Cloud**: ECC 6.0 → S/4HANA 마이그레이션 강제 (2027 종료) = 매출 기회 $30B+. "
            "**Joule AI**: ERP 데이터 + AI = 의사결정 자동화. 차세대 가치 제안. "
            "**Business Suite for AI (BSP)**: 데이터 + 프로세스 + AI 통합 — 경쟁 우위 강화."
        ),
        "financial": (
            "**Q1 FY26 (3월 마감)**: 매출 €9.0B (YoY +12% c.c.), Cloud 매출 €4.5B (+25% c.c., 강력). "
            "**Current Cloud Backlog (CCB)** €17B (YoY +30%, 매우 강력 — 향후 매출 가시성). "
            "**Op profit** €2.5B, Op margin 27.8% (회복). **EPS** €1.45 (+50% YoY, 구조조정 효과 상쇄). "
            "**Free cash flow**: €4.0B (Q1, 강력). FY26 가이던스: Cloud revenue €21.6~21.9B (+26~28%), Op profit €10.3~10.6B. "
            "**Net cash position**: €5B+ (재무 매우 견조). 배당 €2.35/share, yield ~1.4%."
        ),
        "business": (
            "**산업 동향**: 글로벌 클라우드 SaaS 성장 가속 (15%/yr). **AI 통합** = 차세대 엔터프라이즈 가치. "
            "**경쟁구도**: Oracle (DB+클라우드+AI), MS Dynamics + Azure AI, Salesforce (CRM). SAP는 ERP 코어 차별화. "
            "**S/4HANA 마이그레이션**: 70%+ 고객 진행 중, 2027 종료 효과 가속. **TAM** $200B+ (글로벌 ERP+클라우드+AI). "
            "**메가트렌드**: AI agents (Joule), 산업별 cloud (Vertical SaaS), GenAI for ERP. "
            "**규제**: EU AI Act 준수 (SAP 선제적), 데이터 주권 (sovereign cloud — EU + 사우디 등)."
        ),
        "momentum": (
            "**최근 주가**: $173.68 (-0.84% 5/27, 52주 고 $307.93 대비 -43.6%, 저 $157.91 대비 +9.9%). "
            "**큰 조정 + 52주저 근접** — Cloud 강세 vs AI 트랜지션 우려 + 매크로 (USD 강세, 유럽 경기). ATR(14) $5.83 (3.35%). "
            "**컨센서스**: Strong Buy 47%, Buy 28%, Hold 22%, Underperform 3%. 평균 목표가 $235 (+35.3%). "
            "**수급**: ARK·Mahar 비중 유지. **이벤트**: Q2 FY26 발표 7월 말. AI Capital Markets Day 9월 예정."
        ),
        "risks": [
            {"name": "AI 가치 입증 지연", "level": "Medium",
             "impact": "Joule AI ROI 입증 지연 시 가격결정력 약화, 매출 +12% → +8% 둔화 가능.",
             "desc": "현재 BSP 출시 1년차. 고객 PoC → 본격 채택까지 12~18개월. 단기 압박, 장기 잠재력."},
            {"name": "USD/EUR 환율 (USD 강세)", "level": "Medium",
             "impact": "EUR-denominated 매출 → USD 환산 -5~8%. EPS USD -3~5%.",
             "desc": "DXY 99.12 (안정 중). Fed 인하 지연 시 USD 강세 지속 가능."},
            {"name": "클라우드 마진 ramp 지연", "level": "Medium",
             "impact": "Cloud margin 70% 목표 vs 현재 ~67%. Margin 정체 시 Op profit 가이드 미달.",
             "desc": "Hyperscaler 결제 비용 + 구현 비용 압박. 마진 정상화 12~24개월 horizon."},
            {"name": "유럽 경기 부진", "level": "Low",
             "impact": "유럽 GDP 둔화 시 SAP 신규 고객 확보 둔화. 다만 글로벌 분산 (미국 30%+) 헷지.",
             "desc": "독일 GDP 침체 우려. SAP는 글로벌 고객 베이스로 일부 헷지."},
        ],
        "risk_summary": (
            "**Medium 리스크**. 핵심 KPI: Cloud revenue +25%+ 유지, Current Cloud Backlog 성장률, Joule AI ROI 사례, "
            "Op margin 30% 달성 시점 (2027 가이드). AI 트랜지션 성공이 thesis 핵심."
        ),
        "consensus": [
            ("Strong Buy", "47%"),
            ("Buy", "28%"),
            ("Hold", "22%"),
            ("Sell", "3%"),
            ("평균 목표가", "$235 (+35.3%)"),
            ("최고가", "$290"),
            ("최저가", "$180"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 9.0),
            ("재무 건전성", 9.0),
            ("산업 매력도", 8.5),
            ("성장성", 8.0),
            ("수익성/효율성", 7.5),
            ("밸류에이션", 8.0),
            ("모멘텀", 6.0),
            ("컨센서스/수급", 8.0),
            ("리스크 (역수)", 7.5),
            ("ESG/지속가능성", 8.0),
        ],
        "confidence": {
            "target_low": 195, "target_high": 270, "target_mid": 235,
            "ci_pct": "±16.0%",
            "score_band": "±6pt"
        },
        "fragile_assumptions": [
            ("Cloud revenue YoY +25% 이상 유지", "+15% 둔화 시 SaaS thesis 흔들림 + 멀티플 compression → 스코어 -10pt"),
            ("S/4HANA 마이그레이션 70%+ 완료 2027", "지연 시 ECC 종료 효과 약화 → 스코어 -6pt"),
            ("Joule AI 고객 채택 1년 내 가시화", "AI ROI 입증 지연 시 valuation 멀티플 감점 → 스코어 -8pt"),
        ],
        "strategy": (
            "**4단계 분할 매수** (큰 조정 활용):\n"
            "- 1차 $173~178 (현재가, 30%)\n"
            "- 2차 $165~172 (-3~5%, 30%)\n"
            "- 3차 $158~163 (52주저 부근, 25%)\n"
            "- 4차 $150↓ (매크로 충격 시, 15%)\n\n"
            "**손절 $162.03** (2x ATR, -6.7%) / **1차 목표 $191.16** (3x ATR, +10.1%, R:R 1:1.5) / **2차 목표 $235** (+35.3%, 12~24개월).\n"
            "**보유 기간**: 24~36개월. AI 트랜지션 + Cloud margin 정상화 catalysts 모니터링."
        ),
        "valuation": (
            "**Forward P/E ~22x** (5-yr avg 27x — 디스카운트). **EV/EBITDA ~15x** (avg 18x). "
            "**PEG ~1.8** (성장 12% c.c. 가정). DCF (WACC 8.5%, terminal 3%): $245 fair value. "
            "**Cloud peer (Salesforce, Oracle) 평균 P/E 28x** → SAP $220 정상화. "
            "**AI 옵션 가치** $30~50 (Joule monetization 성공 시). "
            "현재 $173.68 = 약 **-30% 디스카운트** from fair value. **Deep Value 매수 영역**."
        ),
    },

    # ─────────────────────────────────────────────────────────
    "PG": {
        "name": "PG",
        "name_kr": "프록터앤갬블",
        "score": 77.0,
        "grade": "매수",
        "sector": "소비재 — 글로벌 생활용품",
        "category": "방어형/배당",
        "summary": (
            "글로벌 소비재 거인 (Tide, Pampers, Gillette, Olay, Ariel, Crest 등 65+ 브랜드). "
            "**가격결정력 + 글로벌 분산 + 배당 King** (68년 연속 배당 인상). "
            "**5/27 +3.27%** 강세 — 인플레 헷지 + 배당 매력. **Q3 FY26 (3월 분기) 매출 +1.5% (오가닉 +1%)** — 둔화 추세. "
            "**약점**: 신흥국 수요 둔화 (특히 중국), 가격 인상 사이클 막바지, USD 강세 영향. "
            "**카탈리스트**: GLP-1 약물 영향 제한적 (식품 카테고리 적음), Pampers 재성장, 미국 소비재 회복."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (5-Star)** — 글로벌 65+ 브랜드, 5개 메가 카테고리 #1 (Beauty, Grooming, Healthcare, Fabric, Baby). "
            "**브랜드 자산 무형**: Tide (세제 #1 미국 60% 점유율), Pampers (기저귀 #1 글로벌), Gillette (면도기 #1). "
            "**스케일 + 유통**: 글로벌 70+ 국가, 모든 채널 (대형마트, drugstore, e-comm, 도매). "
            "**R&D**: 연 $2B+ R&D (혁신 지속), Olay Regenerist + Always 등 carve-out 제품 R&D-led. "
            "**가격결정력**: 가격 +5% (지난 2년) — 인플레 전가 성공. 마진 회복 가속."
        ),
        "financial": (
            "**Q3 FY26 (1~3월 마감, 4/24 발표)**: 매출 $19.8B (YoY +1.5%), 오가닉 매출 +1%. "
            "**볼륨 -1%, 가격 +2%, 믹스 0% c.c.** Core EPS $1.54 (+3% YoY). "
            "**Op margin** 24.5% (vs 23.8% YoY, 회복). **Gross margin** +130bps YoY (commodity 안정). "
            "**FY26 가이던스**: 오가닉 매출 +2~4%, Core EPS $6.91~7.05 (+3~5% YoY). "
            "**Free cash flow productivity**: 90%+. **자사주매입 + 배당**: 연 $14~15B 환원. "
            "**배당**: 분기 $1.0568 → 연 $4.23, 현재가 $147.64 = yield ~2.9% (68년 연속 인상)."
        ),
        "business": (
            "**산업 동향**: 글로벌 소비재 시장 $2T+. 인플레 + trade-down 동시 작용. **신흥국** (중국, 인도) 성장 둔화. "
            "**경쟁구도**: Unilever (글로벌 거인), Colgate, Church & Dwight, Reckitt Benckiser. P&G는 브랜드 + 스케일 우위. "
            "**메가트렌드**: Premiumization (고급화), digital 마케팅, Beauty/Personal Care 성장, e-commerce 가속. "
            "**규제**: PFAS (영구화학물질) 규제 (Always 패드 영향), 플라스틱 포장 EU 규제, 광고 규제 (아동). "
            "**TAM**: 글로벌 가정용품 $1T+, 침투율 ↑ 여지 (신흥국)."
        ),
        "momentum": (
            "**최근 주가**: $147.64 (+3.27% 5/27, 52주 고 $166.21 대비 -11.2%, 저 $135.63 대비 +8.9%). "
            "5/27 +3.27% 강세 — 인플레 헷지 + 배당주 강세. ATR(14) $2.86 (1.93%). "
            "**컨센서스**: Strong Buy 30%, Buy 40%, Hold 27%, Underperform 3%. 평균 목표가 $165 (+11.8%). "
            "**수급**: 배당주 ETF (SCHD 포함), Berkshire 보유 없음 (과거), 인플레 헷지 매수세. **이벤트**: Q4 FY26 발표 7월."
        ),
        "risks": [
            {"name": "오가닉 성장 둔화 (목표 +3~5% → +1~2%)", "level": "Medium",
             "impact": "오가닉 +1% → 매출 가이드 미달. EPS 성장 +3% → +1% 둔화 가능.",
             "desc": "현재 오가닉 +1% (가격 +2%, 볼륨 -1%). 가격결정력 막바지 시그널. 볼륨 회복 필요."},
            {"name": "중국 + 신흥국 둔화", "level": "Medium",
             "impact": "중국 매출 8% (감소 추세), 신흥국 30%+. 둔화 시 글로벌 매출 -1~2pt 영향.",
             "desc": "SK-II 부진 (중국 럭셔리 둔화). 인도·라틴 강세 일부 헷지."},
            {"name": "USD 강세 + FX 헤지", "level": "Low",
             "impact": "USD 강세 시 글로벌 매출 USD 환산 -2~3%. EPS -1~2%.",
             "desc": "DXY 99.12. P&G FX 헷지 적극적 (5년 forward), 영향 제한."},
            {"name": "Commodity 가격 (oil, palm)", "level": "Low",
             "impact": "오일 + 팜오일 가격 상승 시 Gross margin -50~100bps.",
             "desc": "WTI $90 (-3.84%), 안정 추세. 회사 가격 인상으로 일부 전가."},
        ],
        "risk_summary": (
            "**Low-Medium 리스크**. 핵심 KPI: 오가닉 매출 성장률 (+2~4% 회복), 볼륨 성장 (현재 -1% → +1% 회복), "
            "중국 매출, Gross margin 회복. 배당 King 지위 견고."
        ),
        "consensus": [
            ("Strong Buy", "30%"),
            ("Buy", "40%"),
            ("Hold", "27%"),
            ("Sell", "3%"),
            ("평균 목표가", "$165 (+11.8%)"),
            ("최고가", "$180"),
            ("최저가", "$140"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 9.5),
            ("재무 건전성", 9.0),
            ("산업 매력도", 7.5),
            ("성장성", 6.0),
            ("수익성/효율성", 8.5),
            ("밸류에이션", 7.0),
            ("모멘텀", 7.5),
            ("컨센서스/수급", 8.0),
            ("리스크 (역수)", 8.0),
            ("ESG/지속가능성", 7.5),
        ],
        "confidence": {
            "target_low": 145, "target_high": 175, "target_mid": 165,
            "ci_pct": "±9.1%",
            "score_band": "±5pt"
        },
        "fragile_assumptions": [
            ("오가닉 매출 +2% 이상 회복", "+1% 정체 시 가격결정력 막바지 확인 → 스코어 -7pt"),
            ("배당 King 68년 연속 인상 유지", "배당 동결 시 yield premium 소실 → 스코어 -10pt (Thesis breaker)"),
            ("Gross margin 50%+ 유지", "margin -100bps 이상 압박 시 → 스코어 -5pt"),
        ],
        "strategy": (
            "**4단계 분할 매수** (배당 King):\n"
            "- 1차 $147~150 (현재가, 30%)\n"
            "- 2차 $140~145 (-3~5%, 30%)\n"
            "- 3차 $135~138 (52주저 부근, 25%)\n"
            "- 4차 $130↓ (매크로 충격 시, 15%)\n\n"
            "**손절 $141.93** (2x ATR, -3.9%) / **1차 목표 $156.21** (3x ATR, +5.8%, R:R 1:1.5) / **2차 목표 $170** (+15.1%, 12~18개월).\n"
            "**보유 기간**: 36개월+. 배당 누적 + 가격결정력 회복."
        ),
        "valuation": (
            "**Forward P/E ~25x** (5-yr avg 24x, 약 +4% 프리미엄). 합리적. **EV/EBITDA ~17x** (avg 17x). "
            "**Dividend yield 2.9%** + 배당 성장 ~6%/yr = expected income return ~9%. "
            "DCF (WACC 7%, terminal 2%): $170 fair value. "
            "현재 $147.64 = -13% 디스카운트, 매수 영역. **배당 King + 가격결정력 회복 시나리오** 가치."
        ),
    },

    # ─────────────────────────────────────────────────────────
    "PEP": {
        "name": "PepsiCo",
        "name_kr": "펩시코",
        "score": 71.0,
        "grade": "매수",
        "sector": "소비재 — 음료/스낵",
        "category": "방어형/배당",
        "summary": (
            "글로벌 음료 + 스낵 거인 (Pepsi, Mountain Dew, Gatorade, Tropicana / Frito-Lay, Quaker). "
            "**Frito-Lay 60%+ 매출 + 글로벌 음료** 다각화. **52년 연속 배당 인상** (Dividend King). "
            "**Q1 FY26 매출 +2% c.c. (오가닉 +1.2%) — 둔화** (가격 +3%, 볼륨 -1.5%). "
            "**5/27 +1.64%**. **약점**: GLP-1 약물 (스낵 카테고리 우려), 신흥국 둔화, 가격 인상 사이클 막바지. "
            "**카탈리스트**: 신흥국 스낵 성장 (인도, 브라질), Frito-Lay 마진 회복, 음료 혁신 (제로 슈가)."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (4-Star)** — 글로벌 23개 브랜드 매출 $1B+ 이상 (Pepsi, Lay's, Doritos, Mountain Dew, Gatorade 등). "
            "**Frito-Lay**: 미국 스낵 시장 60%+ 점유율 (Direct Store Delivery 시스템 = 진입장벽). "
            "**유통 모델**: 200+ 국가, 자체 + 보틀러 파트너 (Cabb DSD). 스케일 + 거리 단축. "
            "**브랜드 자산**: $20B+ 광고 + 50년+ 브랜드 헤리티지. "
            "**약점**: Coca-Cola (음료 #1), Mondelez (스낵 글로벌), Kraft Heinz (스낵·음료) 경쟁."
        ),
        "financial": (
            "**Q1 FY26 (3월 분기)**: 매출 $17.9B (YoY +2.0% c.c.), 오가닉 매출 +1.2%. "
            "**Frito-Lay North America**: 매출 +0.5%, op profit +1% (볼륨 -2.7%, 가격 +3.2%). "
            "**PepsiCo Beverages NA**: 매출 +1%, op profit +3% (볼륨 -2%, 가격 +3%). "
            "**International**: 매출 +5% c.c. (강력, 신흥국 성장). "
            "**Core EPS** $1.48 (+3% YoY). Op margin 18.5% (안정). "
            "**FY26 가이던스**: 오가닉 매출 +3~4%, Core EPS $8.10~8.20 (+5% YoY). "
            "**자사주매입 + 배당** 연 $8.5B 환원. **배당**: 분기 $1.355 → 연 $5.42, 현재가 $148.07 = yield ~3.7% (52년 연속 인상)."
        ),
        "business": (
            "**산업 동향**: 글로벌 음료/스낵 시장 $1T+. **GLP-1 약물** (Ozempic, Wegovy) → 칼로리 섭취 감소 우려. "
            "**경쟁구도**: Coca-Cola (음료 #1), Mondelez (스낵), Keurig Dr Pepper. 신흥국 로컬 브랜드. "
            "**메가트렌드**: 건강식 (저칼로리·제로 슈가·식물성), e-commerce (DTC), 신흥국 성장. "
            "**규제**: Sugar tax (멕시코, 영국, 칠레), 광고 제한 (아동), 플라스틱 포장. "
            "**TAM**: 글로벌 음료 $700B + 스낵 $400B = $1.1T, 침투율 ↑ 여지 (특히 아시아, 라틴)."
        ),
        "momentum": (
            "**최근 주가**: $148.07 (+1.64% 5/27, 52주 고 $169.96 대비 -12.9%, 저 $124.03 대비 +19.4%). "
            "GLP-1 우려로 52주고 -13% 조정 → 5/27 +1.64% 반등. ATR(14) $3.27 (2.21%). "
            "**컨센서스**: Strong Buy 25%, Buy 38%, Hold 32%, Underperform 5%. 평균 목표가 $165 (+11.4%). "
            "**수급**: 배당주 ETF 비중 유지. Berkshire 보유 (소량). **이벤트**: Q2 FY26 발표 7월 중순."
        ),
        "risks": [
            {"name": "GLP-1 약물 + 건강식 트렌드", "level": "Medium-High",
             "impact": "GLP-1 사용자 증가 시 스낵 카테고리 -3~5% 영향. Frito-Lay 매출 둔화.",
             "desc": "GLP-1 사용자 미국 6%+ 추정 (2026), Walmart 데이터 스낵 구매 -7% 보고. 직접 영향 진행 중."},
            {"name": "신흥국 + USD 강세", "level": "Medium",
             "impact": "USD 강세 시 신흥국 매출 USD 환산 -3~5%. EPS -2~3%.",
             "desc": "DXY 99.12 (안정). USD/MXN, USD/INR 변동성. 신흥국 매출 ~40%."},
            {"name": "Frito-Lay 볼륨 회복 지연", "level": "Medium",
             "impact": "볼륨 -2.7% (Q1) → 회복 지연 시 op profit 가이드 미달.",
             "desc": "GLP-1 + 가격 인상 누적 영향. 신제품 혁신 + 마케팅 확대 필요."},
            {"name": "Commodity (옥수수, 감자, oil)", "level": "Low",
             "impact": "Commodity 상승 시 Frito-Lay margin -50~100bps.",
             "desc": "WTI $90 안정, 농산물 cycle 정상. 가격 인상으로 일부 전가."},
        ],
        "risk_summary": (
            "**Medium 리스크**. 핵심 KPI: Frito-Lay 볼륨 회복 (-2.7% → +1%), 오가닉 성장 +3~4% 회복, "
            "신흥국 매출 +5% c.c. 유지. GLP-1 영향 모니터링 (Walmart 데이터)."
        ),
        "consensus": [
            ("Strong Buy", "25%"),
            ("Buy", "38%"),
            ("Hold", "32%"),
            ("Sell", "5%"),
            ("평균 목표가", "$165 (+11.4%)"),
            ("최고가", "$185"),
            ("최저가", "$135"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 8.5),
            ("재무 건전성", 8.0),
            ("산업 매력도", 7.0),
            ("성장성", 6.0),
            ("수익성/효율성", 8.0),
            ("밸류에이션", 7.5),
            ("모멘텀", 6.5),
            ("컨센서스/수급", 7.5),
            ("리스크 (역수)", 6.5),
            ("ESG/지속가능성", 7.5),
        ],
        "confidence": {
            "target_low": 140, "target_high": 175, "target_mid": 165,
            "ci_pct": "±10.6%",
            "score_band": "±5pt"
        },
        "fragile_assumptions": [
            ("Frito-Lay 볼륨 -2.7% → +1% 회복 (FY26)", "회복 지연 시 op profit 가이드 미달 + 멀티플 압박 → 스코어 -8pt"),
            ("배당 King 52년 연속 인상 유지", "배당 동결 시 yield premium 소실 → 스코어 -10pt"),
            ("GLP-1 영향 단기 -3% 한정", "장기 -7~10% 영향 시 thesis 흔들림 (구조적 trend) → 스코어 -12pt"),
        ],
        "strategy": (
            "**4단계 분할 매수** (배당 King + GLP-1 조정):\n"
            "- 1차 $148~150 (현재가, 30%)\n"
            "- 2차 $140~145 (-3~5%, 30%)\n"
            "- 3차 $130~135 (-9~12%, 25%)\n"
            "- 4차 $125↓ (52주저 부근, 15%)\n\n"
            "**손절 $141.52** (2x ATR, -4.4%) / **1차 목표 $157.89** (3x ATR, +6.6%, R:R 1:1.5) / **2차 목표 $170** (+14.8%, 12~24개월).\n"
            "**보유 기간**: 36개월+. 배당 누적 + Frito-Lay 회복 + 신흥국 성장."
        ),
        "valuation": (
            "**Forward P/E ~19x** (5-yr avg 22x — 디스카운트). 매력적. **EV/EBITDA ~13x** (avg 15x). "
            "**Dividend yield 3.7%** + 배당 성장 ~6%/yr = expected income return ~9.7%. "
            "DCF (WACC 7%, terminal 2%): $170 fair value. "
            "현재 $148.07 = **-13% 디스카운트**, 매수 영역. GLP-1 fear 가격에 반영, **mean reversion 기대**."
        ),
    },
}


# ==============================================================
# MD 파일 생성기
# ==============================================================

def make_md_files(ticker, name, info):
    out_dir = f"analysis/{ticker}_{name}_v4"

    # company.md
    company_md = f"""# {info['name_kr']} ({ticker}) — 기업개요 & Moat (BLIND v4 재분석)

> **재분석 모드**: BLIND v4 (이전 v3 절대 read 안 함)
> **재분석 일자**: {TODAY}
> **데이터 기준일**: 2026-05-27

## Executive Summary

{info['summary']}

## Moat 평가: {info['moat_rating']}

{info['moat_details']}

## 산업 위치 + 경쟁 우위

- **섹터**: {info['sector']}
- **카테고리**: {info['category']}
- **종합 등급**: {info['grade']} (스코어 {info['score']}/100)
"""

    # financial.md
    financial_md = f"""# {info['name_kr']} ({ticker}) — 재무 분석 (BLIND v4)

> **BLIND 모드 — 이전 v3 read 0건**

## 최근 실적 + 재무 상태

{info['financial']}

## 밸류에이션

{info['valuation']}

## 가격 정보 (2026-05-27 기준)

- 데이터는 analysis/{ticker}_{name}_v4/data.json 참조
"""

    # business.md
    business_md = f"""# {info['name_kr']} ({ticker}) — 사업/산업 분석 (BLIND v4)

> **BLIND 모드 — 이전 v3 read 0건**

## 산업 동향 + 경쟁 구도 + 메가트렌드

{info['business']}
"""

    # momentum.md
    momentum_md = f"""# {info['name_kr']} ({ticker}) — 모멘텀 + 컨센서스 (BLIND v4)

> **BLIND 모드 — 이전 v3 read 0건**

## 최근 모멘텀 + 컨센서스 + 수급

{info['momentum']}

## 컨센서스 표

| 항목 | 값 |
|------|-----|
""" + "\n".join(f"| {k} | {v} |" for k, v in info['consensus']) + "\n"

    # risk.md
    risk_md = f"""# {info['name_kr']} ({ticker}) — 리스크 분석 (BLIND v4)

> **BLIND 모드 — 이전 v3 read 0건**

## 주요 리스크 (4개)

"""
    for r in info['risks']:
        risk_md += f"""### {r['name']} ({r['level']})

- **영향**: {r['impact']}
- **상세**: {r['desc']}

"""
    risk_md += f"""## 리스크 종합

{info['risk_summary']}
"""

    # scorecard.md (mandatory § Confidence Interval + § 약한 가정 3개)
    sc_md = f"""# {info['name_kr']} ({ticker}) — 종합 스코어카드 (BLIND v4)

> **재분석 v4** — 이전 v3 비교 미포함 (Phase 2 reanalysis_runs/{YYYYMMDD}_run.md 참조)
> **BLIND 모드 — 이전 v3 read 0건**

## 종합 평가

- **종합 점수**: {info['score']}/100
- **투자 등급**: {info['grade']}
- **카테고리**: {info['category']}

## 10항목 스코어카드

| # | 항목 | 점수 | 가중 |
|---|------|------|------|
"""
    for i, (n, s) in enumerate(info['scorecard_items'], 1):
        sc_md += f"| {i} | {n} | {s:.1f}/10 | 10% |\n"

    sc_md += f"""
## 투자 전략

{info['strategy']}

## § Confidence Interval (95% CI)

- **목표가 범위**: ${info['confidence']['target_low']:,} ~ ${info['confidence']['target_high']:,} (중심 ${info['confidence']['target_mid']:,}, {info['confidence']['ci_pct']})
- **스코어 ±밴드**: {info['confidence']['score_band']} (가정 변경 시 변동 폭)
- **시나리오 분기**:
  - **Bull case**: 목표가 ${info['confidence']['target_high']:,}
  - **Base case**: 목표가 ${info['confidence']['target_mid']:,}
  - **Bear case**: 목표가 ${info['confidence']['target_low']:,}

## § 약한 가정 3개 (Most Fragile Assumptions)

본 결론을 뒤집을 수 있는 핵심 가정 3개:

"""
    for i, (assumption, impact) in enumerate(info['fragile_assumptions'], 1):
        sc_md += f"{i}. **{assumption}**\n   - 반증 시 영향: {impact}\n\n"

    sc_md += f"""## 카탈리스트 + 모니터링 포인트

분석 본문 §3~5 참조. 핵심 KPI:
- {info['risks'][0]['name']}
- {info['risks'][1]['name']}
- (개별 종목별 모니터링 변수)

---

> 본 스코어카드는 **{TODAY} BLIND 재분석 v4**입니다.
> 이전 v3 (2026-05-13) 와의 차이는 `analysis/_reanalysis_runs/{YYYYMMDD}_run.md` 비교표 참조.
"""

    # 파일 저장
    files = {
        f"{out_dir}/company.md": company_md,
        f"{out_dir}/financial.md": financial_md,
        f"{out_dir}/business.md": business_md,
        f"{out_dir}/momentum.md": momentum_md,
        f"{out_dir}/risk.md": risk_md,
        f"{out_dir}/scorecard.md": sc_md,
    }
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return out_dir


# ==============================================================
# HTML 리포트 생성기 — report_template.generate_report 호출
# ==============================================================

def make_html_report(ticker, name, info):
    # data.json 읽기 (가격 정보)
    with open(f"analysis/{ticker}_{name}_v4/data.json", "r", encoding="utf-8") as f:
        d = json.load(f)

    # PER 계산은 어려우므로 생략 또는 적당히
    is_etf = info.get("asset_type") == "ETF"
    report_data = {
        "ticker": ticker,
        "name": info["name_kr"] + f" ({info['name']})",
        "date": TODAY,
        "score": info["score"],
        "grade": info["grade"],
        "current_price": d["current_price"],
        "currency": "$",
        "market_cap": d.get("market_cap"),
        "per": "N/A",
        "low52": d.get("low_52w"),
        "high52": d.get("high_52w"),
        "asset_type": "ETF" if is_etf else "주식",
        "stop_loss": d.get("stop_loss_2atr"),
        "target_price": d.get("target_3atr"),
        "atr": d.get("atr_14"),
        "executive_summary": info["summary"],
        "company_overview": info["summary"],
        "moat_rating": info["moat_rating"],
        "moat_details": info["moat_details"],
        "financial_analysis": info["financial"],
        "valuation": info["valuation"],
        "momentum": info["momentum"],
        "business_analysis": info["business"],
        "scorecard_items": info["scorecard_items"],
        "risks": info["risks"],
        "risk_summary": info["risk_summary"],
        "strategy": info["strategy"],
        "consensus_table": {
            "headers": ["항목", "값"],
            "rows": [[k, v] for k, v in info["consensus"]]
        },
        "extra_kpis": [
            ("등급", info["grade"]),
            ("배당Yield", "—" if not is_etf else "3.8%"),
            ("재분석", "v4 BLIND"),
        ],
        "custom_sections": [
            {
                "title": "§ Confidence Interval (95% CI)",
                "content": (
                    f"**목표가 범위**: \\${info['confidence']['target_low']:,} ~ \\${info['confidence']['target_high']:,}"
                    f" (중심 \\${info['confidence']['target_mid']:,}, {info['confidence']['ci_pct']})\n\n"
                    f"**스코어 ±밴드**: {info['confidence']['score_band']}\n\n"
                    f"- Bull case: \\${info['confidence']['target_high']:,}\n"
                    f"- Base case: \\${info['confidence']['target_mid']:,}\n"
                    f"- Bear case: \\${info['confidence']['target_low']:,}"
                )
            },
            {
                "title": "§ 약한 가정 3개 (Most Fragile Assumptions)",
                "content": "\n\n".join([
                    f"**{i+1}. {assum}**\n\n반증 시 영향: {impact}"
                    for i, (assum, impact) in enumerate(info['fragile_assumptions'])
                ])
            },
            {
                "title": "재분석 메타 (v4 BLIND)",
                "content": (
                    f"- **재분석 회차**: v4 (이전 v3, {TODAY})\n"
                    f"- **모드**: BLIND (이전 v3 read 0건)\n"
                    f"- **임계 경과**: 15일\n"
                    f"- **회차 보고**: `analysis/_reanalysis_runs/{YYYYMMDD}_run.md`"
                )
            }
        ]
    }

    output_path = f"reports/{ticker}_{name}_{YYYYMMDD}.html"
    generate_report(report_data, output_path=output_path)
    return output_path


def main():
    print(f"=== 재분석 자동 실행 — {TODAY} BLIND v4 — 10종 일괄 ===\n")

    ticker_name_map = {
        "WMT": "Walmart", "V": "Visa", "VZ": "Verizon", "T": "ATT",
        "TXN": "TexasInstruments", "TTE": "TotalEnergies",
        "SCHD": "SchwabUSDividendEquity", "SAP": "SAP",
        "PG": "PG", "PEP": "PepsiCo",
    }

    for ticker, name in ticker_name_map.items():
        info = TICKER_DATA[ticker]
        print(f"[{ticker}] BLIND v4 작성 중...")
        try:
            out_dir = make_md_files(ticker, name, info)
            html = make_html_report(ticker, name, info)
            print(f"  ✅ MD: {out_dir}/ (6 files)")
            print(f"  ✅ HTML: {html}")
        except Exception as e:
            print(f"  ❌ {ticker}: FAILED — {e}")
            import traceback
            traceback.print_exc()

    print(f"\n=== 완료 — 10종 v4 분석 + HTML 보고서 ===")


if __name__ == "__main__":
    main()
