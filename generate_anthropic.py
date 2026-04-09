#!/usr/bin/env python3
"""
generate_anthropic.py - Anthropic(엔트로픽) 비상장 AI 기업 종합 분석 리포트 생성
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_template import generate_report

data = {
    "ticker": "ANTHROPIC",
    "name": "Anthropic (엔트로픽)",
    "date": "2026-04-09",
    "asset_type": "비상장 (Pre-IPO)",
    "score": 80.4,
    "grade": "Strong Buy (적극 매수)",
    "current_price": None,
    "market_cap": 380e9,
    "per": "비상장",
    "low52": None,
    "high52": None,
    "currency": "$",

    "extra_kpis": [
        ("ARR (2026.04)", "$30B"),
        ("YoY 성장률", "+1,400%"),
        ("최신 밸류", "$380B"),
        ("PSR", "12.7x"),
        ("누적 조달", "$67.3B"),
        ("IPO 예정", "2026.10"),
        ("엔터프라이즈 점유율", "40% (#1)"),
        ("FCF 흑자 전환", "2027E"),
    ],

    "executive_summary": (
        "Anthropic은 AI 산업 역사상 가장 빠른 성장을 기록 중인 비상장 기업이다. "
        "ARR $300억으로 OpenAI를 추월하며 엔터프라이즈 AI 시장 1위(40%)를 확립했다. "
        "Constitutional AI 기반 안전성 리더십과 Amazon($80억)+Google($30억+, 100만 TPU) 양대 전략적 파트너십이 핵심 경쟁 우위. "
        "2026년 10월 IPO 예정(Goldman Sachs/JPMorgan 주관), 예상 밸류 $400~500B.<br><br>"
        "<strong>핵심 강점</strong>: 초고속 성장(YoY +1,400%), 엔터프라이즈 지배력, AI 안전 리더십, Claude Code 성장 엔진<br>"
        "<strong>핵심 리스크</strong>: Pentagon 갈등, 밸류에이션 지속 가능성, 적자 지속, AI 버블 리스크<br>"
        "<strong>카탈리스트</strong>: Claude 5 출시(Q2~Q3), IPO(2026.10), 2027 FCF 흑자 전환"
    ),

    "scorecard_items": [
        ("Moat", 7.5),
        ("수익성", 4.0),
        ("성장성", 10.0),
        ("재무건전성", 8.0),
        ("밸류에이션", 6.0),
        ("모멘텀", 9.5),
        ("리스크", 6.0),
        ("산업트렌드", 9.5),
        ("경영진", 9.0),
    ],

    "company_overview": (
        "Anthropic, PBC(Public Benefit Corporation)는 2021년 OpenAI 핵심 연구진 7인이 "
        "'AI 안전성 최우선'을 기치로 설립한 AI 연구/서비스 기업이다. "
        "CEO Dario Amodei(전 OpenAI VP of Research)와 사장 Daniela Amodei가 공동 창업·경영.<br><br>"
        "<strong>핵심 제품:</strong><br>"
        "• <strong>Claude 모델 패밀리</strong>: Opus 4.6(최고 지능, $5/$25/MTok), Sonnet 4.6(균형, $3/$15), Haiku 4.5(최고속, $1/$5)<br>"
        "• <strong>Claude Code</strong>: 에이전트형 CLI 코딩 도구, ARR $25억(2026.02)<br>"
        "• <strong>MCP (Model Context Protocol)</strong>: 오픈소스 에이전트 프로토콜 표준<br>"
        "• <strong>Project Glasswing + Mythos Preview</strong>: 방어적 사이버보안 AI(2026.04, 11개 빅테크 참여)<br>"
        "• <strong>API 비용 최적화</strong>: Prompt Caching(90% 절감) + Batch API(50% 할인) = 최대 95% 절감"
    ),
    "moat_rating": "Narrow → Wide Moat",
    "moat_details": (
        "<strong>1. 기술 리더십 (강함)</strong>: Constitutional AI, SWE-bench 1위, 1M 토큰 컨텍스트, OpenAI 학습 비용 1/4<br>"
        "<strong>2. 전략적 투자자 네트워크 (매우 강함)</strong>: Amazon $80억 + Google $30억+ 동시 파트너십, 경쟁사가 복제 불가<br>"
        "<strong>3. 엔터프라이즈 침투 (강함)</strong>: LLM 지출 점유율 40%(1위), B2B 30만+, $1M+/연 고객 1,000+<br>"
        "<strong>4. 인재 해자 (강함)</strong>: 전 OpenAI 핵심 연구진, PBC 미션으로 가치 지향 인재 유인<br>"
        "<strong>약점</strong>: 소비자 브랜드 약함 (ChatGPT/Gemini 대비), 오픈소스 LLM commoditization 리스크"
    ),

    "financials_table": {
        "headers": ["항목", "2024", "2025", "2026E", "비고"],
        "rows": [
            ["ARR", "$1B", "$9B", "$30B+", "YoY +1,400%"],
            ["ARR 성장률", "—", "~900%", "~233%", "초고속 → 고속 전환"],
            ["밸류에이션", "비공개", "$61.5→183B", "$380B", "12개월 6배↑"],
            ["PSR", "—", "~20x", "~12.7x", "성장 반영 정상화"],
            ["누적 조달", "~$12B", "~$37B", "$67.3B", "Series G $30B 포함"],
            ["수익성", "적자", "적자", "적자", "2027 FCF 흑자 전망"],
            ["Gross Margin", "—", "~55%E", "~60%E", "규모의 경제 개선"],
        ]
    },
    "financial_analysis": (
        "Anthropic은 15개월 만에 ARR을 $1B에서 $30B으로 30배 성장시켰다. "
        "이는 AI 기업 역사상 전례 없는 수치로, OpenAI($25B)를 추월하여 매출 기준 세계 1위 AI 기업이 되었다. "
        "엔터프라이즈 API 중심 전략이 높은 ARPU($1M+/연 고객 1,000+)를 형성하며, "
        "Claude Code($25억 ARR)가 신규 성장 엔진으로 부상.<br><br>"
        "밸류에이션 $380B는 PSR 12.7x로, AI 섹터 고성장 기업(10~20x) 범위 내 합리적. "
        "다만 현재 적자 지속 중이며, 대규모 인프라 투자(100만 TPU 등)로 2027년 FCF 흑자 전환이 핵심 마일스톤."
    ),
    "revenue_data": [1, 9, 30],
    "op_income_data": [-3, -5, -4],
    "fin_years": ["2024", "2025", "2026E"],
    "fin_unit": "$B",
    "estimates_from": "2026E",

    "valuation_table": {
        "headers": ["방법론", "적정 가치", "현재 대비", "비고"],
        "rows": [
            ["PSR 10x (보수적)", "$300B", "-21%", "성장 둔화 반영"],
            ["PSR 12.7x (현재)", "$380B", "0%", "현재 밸류 유지"],
            ["PSR 15x (낙관적)", "$450B", "+18%", "IPO 프리미엄 반영"],
            ["IPO 컨센서스", "$400~500B", "+5~32%", "Goldman/JPMorgan 추정"],
            ["역산 (2027E ARR $50B×10x)", "$500B", "+32%", "성장 지속 시"],
        ]
    },
    "valuation": (
        "현재 $380B 밸류에이션은 ARR $30B 대비 PSR 12.7x로, AI 섹터 동종 기업 대비 합리적 범위. "
        "2026.10 IPO 시 $400~500B(+5~32%) 예상. "
        "Bull Case($500B+)는 Claude 5 성공과 AI 투자 열기 지속 시, "
        "Bear Case($250~300B)는 AI 버블 우려와 규제 역풍 시나리오."
    ),

    "momentum": (
        "<strong>모멘텀 등급: 극강 (9.5/10)</strong><br><br>"
        "• ARR 15개월 30x 성장 → OpenAI 최초 추월<br>"
        "• 밸류에이션 12개월 6배 상승 ($61.5B → $380B)<br>"
        "• Claude 4.6 시리즈 + Claude Code GA로 제품 모멘텀 최상<br>"
        "• Google 100만 TPU + Project Glasswing으로 인프라/보안 확장<br>"
        "• IPO S-1 제출(2026 여름) → 상장(2026.10) 카탈리스트 대기<br>"
        "• Claude 5(AGI 근접 추론, 2026 Q2~Q3) 출시 임박"
    ),
    "consensus_table": {
        "headers": ["경쟁사", "매출 모멘텀", "제품 모멘텀", "투자 모멘텀", "종합"],
        "rows": [
            ["Anthropic", "★★★★★", "★★★★★", "★★★★★", "15/15"],
            ["OpenAI", "★★★★", "★★★★", "★★★★", "12/15"],
            ["Google DeepMind", "★★★", "★★★★", "★★★", "10/15"],
            ["xAI", "★★★", "★★★", "★★★", "9/15"],
            ["Meta AI", "★★", "★★★", "★★", "7/15"],
        ]
    },

    "business_analysis": (
        "<strong>산업: 생성형 AI / 엔터프라이즈 LLM</strong><br><br>"
        "<strong>TAM</strong>: Generative AI 전체 시장 ~$250B(2026E) → $1.3T(2030E)<br>"
        "<strong>SAM</strong>: Enterprise AI Software ~$100B(2026E)<br>"
        "<strong>SOM</strong>: Anthropic ~$30B(2026, SAM의 30%)<br><br>"
        "<strong>차별화 전략:</strong><br>"
        "1. <strong>API-First, Enterprise-First</strong>: ChatGPT 같은 소비자 앱 대신 B2B API 집중 → 높은 ARPU, 고객 lock-in<br>"
        "2. <strong>AI 안전성 = 경쟁 우위</strong>: 규제 강화 시 선제적 대응 포지션<br>"
        "3. <strong>양대 클라우드 전략</strong>: AWS + GCP 동시 파트너십 → 클라우드 중립성<br>"
        "4. <strong>Claude Code + MCP</strong>: AI 에이전트 생태계 표준화 주도"
    ),
    "competition_table": {
        "headers": ["기업", "주요 모델", "ARR/매출", "밸류에이션", "엔터프라이즈 점유율"],
        "rows": [
            ["Anthropic", "Claude Opus 4.6", "$30B ARR", "$380B", "40% (#1)"],
            ["OpenAI", "GPT-4o, o3", "~$25B ARR", "~$300B+", "27% (#2)"],
            ["Google DeepMind", "Gemini 2.0", "수십억$ (추정)", "Alphabet 내", "21% (#3)"],
            ["Meta AI", "Llama 3.1+", "간접 매출", "Meta 내", "—"],
            ["xAI", "Grok", "비공개", "~$50B+", "—"],
        ]
    },

    "risks": [
        {"name": "Pentagon 공급망 리스크 지정", "level": "중", "impact": "고",
         "desc": "자율 타겟팅·시민 감시 거부로 트럼프 행정부 갈등. 소송 패소(2026.04). 정부 계약 제한 가능"},
        {"name": "AI 규제 강화 / RSP 갈등", "level": "중", "impact": "고",
         "desc": "EU AI Act 시행, RSP 변경 논란(CNN 2026.02). 안전 원칙과 정부 요구 충돌 리스크"},
        {"name": "밸류에이션 버블 리스크", "level": "중", "impact": "고",
         "desc": "$380B 밸류, PSR 12.7x. AI 투자 열기 냉각 시 급락 가능. 15개월 30x 성장은 지속 불가능한 궤적"},
        {"name": "경쟁 심화 (모델 Commoditization)", "level": "고", "impact": "중",
         "desc": "Llama 오픈소스 추격, OpenAI/Google 가격 전쟁. LLM 자체의 commodity화 리스크"},
        {"name": "수익성 불확실 (대규모 적자)", "level": "중", "impact": "중",
         "desc": "100만 TPU 운영비 등 연간 수십억$ 비용. 2027 FCF 흑자 전환 전망이나 보장 아님"},
        {"name": "IPO 불확실성", "level": "중", "impact": "중",
         "desc": "SEC 매출 회계 판단, AI 시장 변동, OpenAI 동시 IPO 시 자금 분산"},
    ],
    "risk_summary": (
        "최대 리스크는 정치적/규제 리스크(Pentagon 분쟁, AI 안전 갈등)와 밸류에이션 지속 가능성. "
        "다만 초강력 매출 성장($30B ARR)과 양대 클라우드 파트너십이 상당한 리스크 버퍼 제공. "
        "IPO 성공 시 리스크 프로파일 크게 개선 전망."
    ),

    "strategy": (
        "<strong>투자 의견: Strong Buy (적극 매수) — 80.4/100</strong><br><br>"
        "Anthropic은 비상장이므로 일반 투자자의 직접 투자는 제한적. 아래 전략 참고:<br><br>"
        "<strong>1. 간접 투자 (현재 가능)</strong><br>"
        "• <strong>Amazon (AMZN)</strong>: 최대 투자자($80억). AWS+Anthropic 시너지<br>"
        "• <strong>Alphabet (GOOGL)</strong>: $30억+ 투자 + 100만 TPU 공급. GCP AI 경쟁력 강화<br>"
        "• AI ETF (BOTZ, ROBO, ARKQ): 간접 노출(제한적)<br><br>"
        "<strong>2. IPO 참여 전략 (2026.10 예정)</strong><br>"
        "• 공모 청약: Goldman Sachs/JPMorgan 주관, 기관 배정 기대<br>"
        "• 예상 IPO 밸류: $400~500B (+5~32% 업사이드)<br>"
        "• 상장 초기 1~2주 변동성 활용 / Lock-up 해제(6개월 후) 재진입<br><br>"
        "<strong>3. 시나리오별 대응</strong><br>"
        "• 🟢 Bull ($500B+, 30%): Claude 5 성공 + AI 투자 열기 지속 → 장기 보유<br>"
        "• 🟡 Base ($400~450B, 50%): 계획대로 IPO → 핵심 포지션 유지<br>"
        "• 🔴 Bear ($250~300B, 20%): AI 버블/규제 역풍 → AMZN/GOOGL 간접 투자 유지"
    ),

    "custom_sections": [
        {
            "title": "투자 유치 타임라인",
            "content": (
                '<table><thead><tr><th>라운드</th><th>시기</th><th>조달액</th><th>밸류에이션</th><th>주요 투자자</th></tr></thead><tbody>'
                '<tr><td>Series A</td><td>2021</td><td>$124M</td><td>비공개</td><td>Jaan Tallinn, Google, Spark Capital</td></tr>'
                '<tr><td>Series B</td><td>2022</td><td>$580M</td><td>비공개</td><td>Google, Spark, Salesforce</td></tr>'
                '<tr><td>Series C</td><td>2023.05</td><td>$450M</td><td>비공개</td><td>Spark(리드), Google, Salesforce</td></tr>'
                '<tr><td>Amazon</td><td>2023~24</td><td><strong>$8B</strong></td><td>—</td><td>Amazon (커스텀칩+DC)</td></tr>'
                '<tr><td>Google</td><td>2023~26</td><td><strong>$3B+</strong></td><td>—</td><td>Google (+100만 TPU 별도)</td></tr>'
                '<tr><td>Series E</td><td>2025.03</td><td>$3.5B</td><td><strong>$61.5B</strong></td><td>Lightspeed, Bessemer, Fidelity</td></tr>'
                '<tr><td>Series F</td><td>2025.09</td><td><strong>$13B</strong></td><td><strong>$183B</strong></td><td>비공개 (6개월 밸류 3x)</td></tr>'
                '<tr><td style="color:#42A5F5;font-weight:700">Series G</td><td>2026.02</td><td style="color:#26A69A;font-weight:700">$30B</td><td style="color:#26A69A;font-weight:700">$380B</td><td>Coatue, GIC, D.E. Shaw, Founders Fund</td></tr>'
                '</tbody></table>'
                '<p style="color:var(--sub);font-size:13px;margin-top:8px">총 누적 조달: $67.3B (17회). Series G = 테크 역대 2번째 최대 민간 펀딩.</p>'
            )
        },
        {
            "title": "IPO 전망 (2026.10 예정)",
            "content": (
                '<div class="kg">'
                '<div class="ki"><div class="kl">목표 시기</div><div class="kv" style="font-size:16px">2026.10 (Q4)</div></div>'
                '<div class="ki"><div class="kl">S-1 제출</div><div class="kv" style="font-size:16px">2026 여름</div></div>'
                '<div class="ki"><div class="kl">예상 밸류</div><div class="kv up" style="font-size:16px">$400~500B</div></div>'
                '<div class="ki"><div class="kl">주관사</div><div class="kv" style="font-size:16px">GS / JPM</div></div>'
                '</div>'
                '<p style="margin-top:12px">Goldman Sachs와 JPMorgan Chase가 공동 주관, Wilson Sonsini 법률 자문. '
                'Anthropic 공식 입장은 "결정 사항 없음"이나 복수 매체에서 2026년 10월 상장을 기정사실화. '
                'OpenAI도 2026년 IPO 검토 중으로 AI 기업 동시 상장 시 시장 자금 분산 리스크 존재.</p>'
            )
        },
        {
            "title": "AI 안전성 연구 & Constitutional AI",
            "content": (
                '<p><strong>Constitutional AI (헌법적 AI)</strong>: 사전 정의 윤리 원칙("헌법")으로 AI 행동 지도. '
                '인간 레이블 없이 자기개선 학습. 범용 탈옥 방어 시스템(Constitutional Classifiers) 배치.</p>'
                '<p style="margin-top:10px"><strong>Responsible Scaling Policy (RSP) v3.0</strong>: '
                'ASL-3 보안 조치(2025.05 발동), Provable Inference 프로토타입(2026.09 목표). '
                '2026.05.11 신규 목표 발표 예정.</p>'
                '<p style="margin-top:10px"><strong>Project Glasswing + Mythos Preview (2026.04)</strong>: '
                '방어적 사이버보안 AI. 수만 건 취약점 탐지 능력. 악용 위험으로 공개 출시 보류. '
                '11개 빅테크 참여 (AWS, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorgan, '
                'Linux Foundation, Microsoft, Nvidia, Palo Alto Networks). '
                'Anthropic $100M 크레딧 + $4M 오픈소스 기부.</p>'
            )
        },
    ],
}

if __name__ == "__main__":
    output = "reports/ANTHROPIC_Anthropic_20260409.html"
    generate_report(data, output)
    print("Anthropic 종합 분석 리포트 생성 완료!")
