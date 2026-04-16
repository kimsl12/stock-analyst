import sys, os

# 절대경로 기반 import
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _root)

# report_template.py 존재 확인
_tmpl = os.path.join(_root, 'report_template.py')
if not os.path.exists(_tmpl):
    raise FileNotFoundError(
        f"report_template.py를 찾을 수 없습니다: {_tmpl}\n"
        f"현재 작업 디렉토리: {os.getcwd()}\n"
        f"현재 브랜치를 확인하세요 (main이어야 함)."
    )

from report_template import generate_report

data = {
    # 필수
    "ticker": "ASTS",
    "name": "AST SpaceMobile",
    "date": "2026-04-16",
    "asset_type": "개별주식 (성장주)",
    "score": 71.35,
    "grade": "Buy",
    "current_price": 86.91,
    "currency": "$",

    # KPI
    "market_cap": 33.2e9,
    "per": "N/M (적자)",
    "low52": 20.26,
    "high52": 129.89,
    "extra_kpis": [("PSR(2026E)", "190배"), ("ATR(14)", "10.22%")],

    # 손절/목표
    "stop_loss": 69.15,
    "target_price": 99.00,
    "atr": 8.88,

    # 스코어카드 (10항목, 0~10점)
    "scorecard_items": [
        ("매출 성장성", 9.5),
        ("산업 성장성(TAM)", 9.0),
        ("경쟁우위(Moat)", 7.5),
        ("모멘텀·컨센서스", 6.5),
        ("수익성 가시성", 5.5),
        ("재무 건전성", 6.5),
        ("경영진·실행력", 6.5),
        ("밸류에이션", 4.0),
        ("리스크", 4.0),
        ("ESG·거버넌스", 6.5),
    ],

    # 텍스트 섹션
    "executive_summary": (
        "AST SpaceMobile(ASTS)은 일반 스마트폰을 별도 단말 없이 LEO 위성에 직접 연결하는 세계 유일의 광대역(5G급) "
        "Direct-to-Device(D2D) 위성통신망 구축 기업이다. 셀당 120Mbps 처리용량으로 경쟁사 Starlink DTC(10Mbps) 대비 "
        "12배 우위를 보유하며, AT&T·Verizon·Vodafone·Rakuten 등 40+ 통신사를 락인한 파트너십이 핵심 해자다. "
        "FY2024 매출 $4.4M에서 FY2026E $175M, FY2028E $1.45B으로 폭발적 성장 컨센서스가 형성되어 있으나, "
        "PSR 190배라는 극단적 밸류에이션과 2026년 45~60기 발사 실행 리스크, Starlink V2 위협이 병존한다. "
        "종합 스코어 71.35/100(Buy), 12개월 목표가 $99(현재가 대비 +14%). "
        "ATR 10.22% 극고변동성으로 분할매수·손절선($69.15) 엄수 전제로 포트폴리오 3~5% 비중 매수 권고."
    ),

    "company_overview": (
        "AST SpaceMobile은 2021년 SPAC 합병으로 NASDAQ에 상장된 위성통신 기업으로, 텍사스주 미들랜드에 본사를 두고 있다. "
        "창업자이자 CEO인 Abel Avellan이 36% 지분을 보유하며, Vodafone·Rakuten·AT&T·Google 등이 주요 전략 주주다. "
        "핵심 제품은 BlueBird 위성 시리즈(2,400 sq ft 대형 어레이)와 자체 개발 AST5000 ASIC 베이스밴드 프로세서이며, "
        "특허 3,600건+ 포트폴리오를 보유한다. 사업 모델은 통신사 매출 분배(Wholesale) + 정부·국방 계약 + B2B IoT로 구성된다. "
        "2024년 BlueBird 1~5기 발사, 2025년 BlueBird 6기 발사에 성공하였으며, 2026~2027년 168기 완성 후 "
        "글로벌 연속 커버리지 확보 및 흑자전환(2028E)을 목표로 한다. "
        "D2D 시장 CAGR 16%, 잠재 시장(글로벌 무선통신 미커버리지 인구) 28억명이 투자 매력도의 근거다."
    ),

    "moat_rating": "Narrow → Wide 이행 중 (조건부)",

    "moat_details": (
        "ASTS의 해자는 ① 특허 3,600건+(Direct-to-Cell 핵심 기술) ② AT&T·Verizon·Vodafone 독점 장기 계약(통신사 전환비용 高) "
        "③ 3GPP NTN Rel-17/18 표준 형성 기여 ④ 광대역 D2D 시장의 효율적 규모(주파수·궤도 슬롯·통신사 슬롯 제한 → 1~2개 사업자만 생존 가능) "
        "에 기반한다. 현재는 위성 10기 수준으로 Narrow Moat 단계이며, 2027년 168기 완성 + Starlink 추격 격차 유지 시 Wide Moat 격상 가능하다. "
        "Starlink가 T-Mobile 단일 의존인 반면, ASTS는 40+ 통신사 파트너로 가입자 풀 우위를 보유한다. "
        "단, Starlink V2 광대역 D2D 출시(2027E) 전에 시장을 충분히 선점하지 못하면 Moat 약화 가능성이 최대 리스크다."
    ),

    "financial_analysis": (
        "FY2024 매출 $4.4M에서 FY2025E $42M(+855%), FY2026E $175M(+317%)으로 폭발적 성장 궤도에 진입한다. "
        "영업손실은 FY2025E -$320M 정점 후 FY2026E -$300M으로 축소 시작하며, FY2027E EBITDA 흑자전환, FY2028E 영업이익 +22% 달성 컨센서스다. "
        "재무 건전성은 우수 — 순현금 $1.08B(부채비율 11%), 유동비율 4.5배, 런웨이 약 22개월(2027 Q4까지). "
        "단, FY2026 CAPEX $450M 포함 FCF -$670M으로 2027년 추가 자금조달(신주 발행) 가능성이 60% 수준이다. "
        "DCF Base 적정주가 $92 ≈ 현재가 $86.91(fair value 근접). "
        "PSR 190배(현행)는 동종 대비 극단적이나, 2028E 매출 $1.45B 기준 PSR 22배로 정상화된다."
    ),

    "valuation": (
        "DCF(Base, 2030 매출 $4.5B, WACC 11%): 적정주가 $92(가중치 35%). "
        "SOTP(2027E 통신사+정부+IoT 분할가치): 적정주가 $100(가중치 35%). "
        "컨센서스 평균(5개사): $107(가중치 30%). "
        "가중평균 12개월 목표주가: $99(현재가 $86.91 대비 +14%). "
        "Bull 시나리오 $135(+55%) / Base $99(+14%) / Bear $65(-25%). "
        "컨센서스 분포: B. Riley $135(Buy) → Cantor $120(OW) → Barclays $105(OW) → Deutsche Bank $95(Hold) → Scotiabank $80(SP)."
    ),

    "momentum": (
        "52주 저점 $20.26(2025.04~05) → 52주 고점 $129.89(2025.12) → 현재 $86.91(2026.04). "
        "Kerrisdale 공매도 보고서(2026.03) 이후 고점 대비 -33% 조정, 4월 AT&T FirstNet 베타 발표로 반등 시작. "
        "기술적 지표: RSI 약 45(중립권), 50일 이평($90) 하회·200일 이평($75) 상회, 장기 상승 추세 유지. "
        "수급: 내부자 36%, 기관 28%, 전략 파트너 12%. 공매도 비율 18~22%(+5%p 급증) → 숏스퀴즈 가능성 병존. "
        "단기 Catalyst: BlueBird 7~10 발사, 2026 Q2 실적, 신규 통신사 계약. "
        "컨센서스 평균 목표가 $107(현재 대비 +23%), 의견 분기 $80~$135로 크고 수렴 추세."
    ),

    "business_analysis": (
        "D2D 위성통신 시장(CAGR 16.2%, 2026E $4.49B → 2030E $8.1B)의 광대역 세그먼트 단독 사업자. "
        "5G/LTE 표준(3GPP NTN) 통합, 정부·국방 수요 폭증, 6G 인프라 필수화 등 산업 트렌드가 우호적이다. "
        "Starlink와의 정면 대결에서 ASTS의 핵심 우위는 셀당 처리용량(120Mbps vs 10Mbps), 40+ 통신사 멀티 파트너(Starlink는 T-Mobile 단일). "
        "통신사들이 Starlink를 '자사 매출을 위협하는 경쟁자'로 인식하는 반면, ASTS는 통신사 인프라 보완 파트너로 포지셔닝 — 이것이 장기 구조적 우위. "
        "Base 시나리오: 2027년 168기 완성 후 매출 CAGR 125%(2026~2030), 2028E 흑자전환. "
        "2026년 45~60기 발사 계획 실현 가능성이 사업 전망의 핵심 변수다."
    ),

    "risk_summary": (
        "1. Starlink V2 광대역 추격(확률 45%, 영향 치명): 2027 중반 Starlink V2 광대역 D2D 출시 시 ASTS 시총 -45% 위험. "
        "2. BlueBird 위성 발사·궤도 진입 실패(확률 25%, 영향 치명): 2026년 45기+ 발사 계획 중 실패 시 주가 -30~50%. "
        "3. 신주 발행 희석(확률 60%, 영향 심각): 2027년 추가 자금조달 시 EPS 13% 희석 우려. "
        "4. 컨센서스 매출 하회(확률 45%, 영향 심각): FY2026 매출 $175M 대비 -20% 하회 시 -15~25% 하락. "
        "5. 추가 공매도 보고서(확률 35%, 영향 중간): Kerrisdale 후속 보고서 시 -15~20% 단기 충격."
    ),

    "strategy": (
        "종합 스코어 71.35/100(Buy) — 고변동성 성장주 매수 권고(포트폴리오 3~5%).\n\n"
        "진입 전략(3회 분할):\n"
        "  1차: $86~88(현재가, 비중 1.5%)\n"
        "  2차: $80~82(-7%, 비중 1.5%)\n"
        "  3차: $72~76(-15%, 비중 1.0%) → 평단 약 $80\n\n"
        "손절가: $69.15(-20%, 2×ATR) — 도달 시 전량 매도.\n\n"
        "익절 전략:\n"
        "  1차: $99(Base 목표가, 50% 매도)\n"
        "  2차: $113.56(3×ATR, 30% 매도)\n"
        "  3차: $135(Bull, 잔여 20% 또는 장기 보유)\n\n"
        "보유 기간: 12~36개월. 매월 위성 발사 진척 + 분기 통신사 매출 분배 모니터링 필수."
    ),

    # 재무 테이블
    "financials_table": {
        "headers": ["항목", "FY2024A", "FY2025E", "FY2026E", "FY2027E", "FY2028E"],
        "rows": [
            ["매출($M)", "$4.4", "$42", "$175", "$620", "$1,450"],
            ["영업손실($M)", "-$225", "-$320", "-$300", "-$20", "+$320E"],
            ["EBITDA 마진", "N/M", "N/M", "-149%", "+5%", "+28%"],
            ["EPS(조정)", "-$1.58", "-$1.60", "-$1.10", "-$0.40", "+$0.55E"],
            ["FCF($M)", "-$420", "-$660", "-$670", "N/M", "+흑자"],
        ],
    },

    # 컨센서스 테이블
    "consensus_table": {
        "headers": ["증권사", "투자의견", "목표가", "현재가 대비"],
        "rows": [
            ["B. Riley Securities", "Buy", "$135", "+55%"],
            ["Cantor Fitzgerald", "Overweight", "$120", "+38%"],
            ["Barclays", "Overweight", "$105", "+21%"],
            ["Deutsche Bank", "Hold", "$95", "+9%"],
            ["Scotiabank", "Sector Perform", "$80", "-8%"],
            ["컨센서스 평균", "Buy 우세", "$107", "+23%"],
        ],
    },

    # 리스크 히트맵
    "risks": [
        {"name": "Starlink V2 광대역 추격", "level": "고", "impact": "치명", "desc": "2027 중반 출시 시 시총 -45%"},
        {"name": "위성 발사·궤도 진입 실패", "level": "중", "impact": "치명", "desc": "주가 -30~50%"},
        {"name": "신주 발행 희석", "level": "고", "impact": "심각", "desc": "EPS 13% 희석 가능"},
        {"name": "컨센서스 매출 하회", "level": "고", "impact": "심각", "desc": "FY2026 $140M 하회 시"},
        {"name": "추가 공매도 보고서", "level": "중", "impact": "중간", "desc": "단기 -15~20%"},
        {"name": "거시 금리 상승", "level": "고", "impact": "중간", "desc": "PSR 190배 멀티플 압축"},
    ],

    # 실적 바차트
    "fin_years": ["FY2024A", "FY2025E", "FY2026E", "FY2027E", "FY2028E"],
    "revenue_data": [4.4, 42, 175, 620, 1450],
    "op_income_data": [-225, -320, -300, -20, 320],
    "fin_unit": "M",
    "estimates_from": 2,
}

output_path = os.path.join(_root, "reports", "ASTS_ASTSpaceMobile_20260416.html")
generate_report(data, output_path)
