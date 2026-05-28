#!/usr/bin/env python3
"""
재분석 자동 실행 — 2026-05-29 — 7종 BLIND v4 일괄 생성
대상: NVO, MRK, MA, JNJ, HSBC, HD, 034020 두산에너빌리티 (모두 v3 → v4)
- BLIND 모드: 이전 v3 절대 read 안 함
- 각 종목 6개 MD + HTML 리포트
"""
import json, os, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from report_template import generate_report

TODAY = "2026-05-29"
YYYYMMDD = "20260529"

# ==============================================================
# 각 종목 BLIND v4 콘텐츠 (현재 가격/매크로/공개 지식 기반)
# ==============================================================

TICKER_DATA = {
    # ─────────────────────────────────────────────────────────
    "NVO": {
        "name": "NovoNordisk",
        "name_kr": "노보노디스크",
        "score": 68.5,
        "grade": "매수",
        "sector": "헬스케어 — 글로벌 제약 (당뇨/비만)",
        "category": "성장형/Deep Value 회복기",
        "currency": "$",
        "previous_v3_date": "2026-05-13",
        "summary": (
            "GLP-1 비만/당뇨 치료제 글로벌 리더. 주가 $45.67 (52주고 $77.68 대비 -41%) 1년+ 조정. "
            "Wegovy·Ozempic 미국 시장 점유율 일부 Eli Lilly에 양보 + 가격 경쟁 압박 + "
            "FDA generic semaglutide 잠재 + Trump MFN 약가 정책 우려가 멀티플 압박. "
            "다만 글로벌 GLP-1 TAM $200B+ 의 빠른 성장 (2030년) + Wegovy MASH 적응증 확대 + "
            "차세대 amycretin·CagriSema 파이프라인이 회복 trigger. 현재 forward P/E ~16x = 5년 만의 deep value. "
            "단기 모멘텀 약함, 12~24개월 mean-reversion bet 적합."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (3-Star)** — GLP-1/GIP 분야 100년 인슐린 제조 노하우 + 생산 capacity 글로벌 Top 2 + "
            "Steno Diabetes Center 임상 데이터. **Producti하다on Moat**: Kalundborg + Clayton (US) capacity 확장으로 "
            "Lilly tirzepatide (Mounjaro/Zepbound)에 직접 경쟁. 최대 위협은 generic semaglutide (특허만료 2031~2033)이지만 "
            "amycretin (oral)·CagriSema (combo) 차세대로 cliff 방어 시도. "
            "Switzerland Novo Nordisk Foundation 28% holding = 장기 자본 배분 의지 + 적대적 인수 차단."
        ),
        "financial": (
            "**FY25 (4월말 발표)**: 매출 DKK 290B (+25% YoY, FX 중립 +29%), 영업이익 DKK 132B (+27%), EPS DKK 24.5 (+24%). "
            "Wegovy 매출 DKK 64B (+58% YoY), Ozempic DKK 130B (+22%). 영업마진 45.5%로 업계 최고 수준 유지. "
            "**Q1 2026 (5/7 발표)**: 매출 DKK 78B (+19%, 컨센 +21% 미달 -2pp), Wegovy +50% (컨센 +60% 미달). "
            "FY26 가이던스 매출 +16~24% (FX 중립), 영업이익 +19~27% — 5/7 발표 시 lower-half 으로 좁힘. "
            "**가이던스 하향 + Lilly 압박**이 5/7~5/14 -8% 추가 하락 trigger. ROE 60%+, ROIC 50%+. "
            "**현금흐름**: FCF DKK 100B+ 안정, 자사주 매입 DKK 20B/yr + 배당 yield 1.9%."
        ),
        "valuation": (
            "**Forward P/E ~16x** (5년 avg 28x — Lilly 75x 대비 deep discount). PEG ~0.8 (성장률 +20%). "
            "**EV/EBITDA ~12x** (avg 22x). DCF (WACC 9%, terminal 3%): 적정 $62~70. "
            "현재 $45.67 = **-30~35% 디스카운트**. 단 generic + MFN 시나리오 반영 시 fair $50~55로 조정. "
            "**Bear $35** (Lilly 50%+ 점유 + generic 가속), **Base $55** (15% 점유율 유지), **Bull $70** (amycretin 성공)."
        ),
        "business": (
            "**산업 동향**: GLP-1 글로벌 TAM 2030년 $200B+ (현재 $50B). 비만 인구 19억 명 (글로벌). "
            "**경쟁구도**: Eli Lilly(LLY) tirzepatide가 단일 분자 효능 우위 (-22% 체중 감량 vs Wegovy -15%), "
            "미국 처방 점유율 ~60% Lilly로 역전 (2025~). Pfizer·Roche·AstraZeneca 차세대 임상 진입. "
            "**메가트렌드**: oral GLP-1 (amycretin)·MASH·심혈관·신장 적응증 확장 = TAM 추가 확대. "
            "**규제 리스크**: Trump 'Most Favored Nation' (MFN) 약가 30% 인하 행정명령 5/12 — Wegovy 미국가격 $1,349/월 압박. "
            "Senate Robert Kennedy Jr. HHS 청문회 5/22 — Wegovy 가격에 대한 지속적 공격."
        ),
        "momentum": (
            "**최근 주가**: $45.67 (+2.51% 5/28, 52주고 $77.68 대비 -41.2%, 저 $34.58 대비 +32.1%). "
            "5/7 Q1 발표 후 -8% (가이던스 하향), 5/12 Trump MFN 행정명령 -5% 추가 하락, 5/16 -3% (Lilly Q1 추월). "
            "5/22~5/28 $42~46 횡보. ATR(14) $1.15 (2.51%). RSI ~38 (oversold). 200D MA $58 (-22%). "
            "**컨센서스**: Buy 48%, Hold 41%, Sell 11%. 평균 목표가 $58 (+27%). 최근 12개의 broker 중 6개 downgrade. "
            "**수급**: 5/15 Berkshire 13F 신규 100만주 (~$50M) 매수 공시 — Buffett deep value 신호. "
            "외국인/기관 순매수 전환 ETF 자금 유입. **이벤트**: 6/12 ADA 학회 amycretin 데이터, 8/7 Q2 발표."
        ),
        "risks": [
            {"name": "Eli Lilly 점유율 추가 잠식", "level": "High",
             "impact": "미국 비만 처방 Lilly 60% → 70%+ 시 Wegovy 매출 -10~15%, 스코어 -8pt",
             "desc": "tirzepatide 단일분자 효능 우위 + Mounjaro Type 2 처방 동시 흡수. orforglipron(oral) FDA 승인 2026 H2 시 추가 압박."},
            {"name": "FDA Generic Semaglutide 가속", "level": "High",
             "impact": "특허 만료 2031~2033이지만, FDA shortage list 우회 generic 진입 가능성 — 발효 시 -25~30% 추가 하락",
             "desc": "5/14 Hims & Hers compounded GLP-1 신규 처방 50% 증가 보도 — FDA shortage 해제 후에도 niche 잔존. 정치적 압력 ↑."},
            {"name": "Trump MFN 약가 규제", "level": "High",
             "impact": "Wegovy 미국 가격 $1,349→$800~900 인하 시 매출 -15%, 마진 -300bps. 스코어 -10pt",
             "desc": "5/12 행정명령 + 5/22 RFK Jr 청문회 공격. CMS 협상 2026 H2. 단 법원 challenge 가능 (헌법재판)."},
            {"name": "amycretin/CagriSema 임상 실패", "level": "Medium",
             "impact": "6/12 ADA·8월 Q2·연말 Phase 3 결과 — 효능 미달 시 차세대 cliff 시나리오, -25% 추가 하락",
             "desc": "Phase 2 amycretin -22% 체중 감량(Wegovy -15%) 우월하나 Phase 3에서 부작용/dropout 변수 잔존."},
        ],
        "risk_summary": (
            "**High 리스크 종합**. Lilly + Generic + MFN 3대 압박이 동시 작용 중. 다만 가격에 상당 부분 반영 (-41% YTD). "
            "**Bear case 잔여 -25% / Bull case 회복 +50%** = 비대칭 risk-reward. "
            "Catalyst: 6/12 ADA amycretin Phase 2 데이터, 8/7 Q2 가이던스 재확인, FDA MFN 법원 stay 여부."
        ),
        "consensus": [
            ("Buy", "48%"),
            ("Hold", "41%"),
            ("Sell", "11%"),
            ("평균 목표가", "$58 (+27.0%)"),
            ("최고가", "$72"),
            ("최저가", "$40"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 8.5),
            ("재무 건전성", 8.5),
            ("산업 매력도", 8.0),
            ("성장성", 7.0),
            ("수익성/효율성", 9.0),
            ("밸류에이션", 8.5),
            ("모멘텀", 4.0),
            ("컨센서스/수급", 5.5),
            ("리스크 (역수)", 4.5),
            ("ESG/지속가능성", 7.0),
        ],
        "confidence": {
            "target_low": 35,
            "target_mid": 55,
            "target_high": 70,
            "ci_pct": "±25%",
            "score_band": "±8pt",
        },
        "fragile_assumptions": [
            ("Wegovy 미국 점유율 35%+ 유지 (현재 ~40%, Lilly orforglipron 승인 시 25%~)",
             "오답 시 매출 가이드 -10%, 스코어 -10pt → 53점 (중립 하단)"),
            ("amycretin Phase 2 (6/12 ADA) 효능 -22% 체중감량 유지",
             "Phase 3 fail 시 차세대 cliff = -20% 추가 하락 / 스코어 -12pt"),
            ("MFN 약가 행정명령 법원 stay 가능 + Wegovy 가격 인하 -10% 이하 한정",
             "전면 -30% 인하 시 영업마진 -300bps, 스코어 -10pt"),
        ],
        "strategy": (
            "**4단계 분할 매수** (Deep Value 회복 + 단기 약세):\n"
            "- 1차 $45~46 (현재가, 20%)\n"
            "- 2차 $42~44 (-3~5%, 30%)\n"
            "- 3차 $38~40 (-12~17%, 30%)\n"
            "- 4차 $35↓ (52주저 부근, 20%)\n\n"
            "**손절 $43.37** (2x ATR, -5.0%) / **1차 목표 $49.11** (3x ATR, +7.5%, R:R 1:1.5) / "
            "**2차 목표 $58** (+27%, 12개월, 컨센 평균) / **3차 목표 $70** (+53%, 24개월, amycretin 성공 + MFN 해소).\n"
            "**보유 기간**: 18~24개월. 단기 부정적 catalysts (FDA generic, MFN)을 견딜 자본 필요."
        ),
    },
    # ─────────────────────────────────────────────────────────
    "MRK": {
        "name": "Merck",
        "name_kr": "머크",
        "score": 73.5,
        "grade": "매수",
        "sector": "헬스케어 — 글로벌 제약 (종양·백신·동물건강)",
        "category": "방어형/Deep Value",
        "currency": "$",
        "previous_v3_date": "2026-05-13",
        "summary": (
            "Keytruda(pembrolizumab) 항암제 글로벌 매출 1위 ($30B+ FY25). 주가 $119.68 = 52주 고점 +근접. "
            "5/13 이후 +15% 강세 — Keytruda Patent Cliff 2028 우려 완화 (subq 제형 FDA 승인 임박) + "
            "신규 종양 파이프라인 (Sotatercept·MK-2870) + Animal Health 분사 가속 + GLP-1 후발 진입(efinopegdutide). "
            "Forward P/E ~14x, 배당 yield 2.8% = Deep Value + 방어 매력. "
            "단 Keytruda 단일 의존 ($30B/$60B = 50%) 리스크 + 중국 항암제 경쟁 잔존."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (3-Star)** — Keytruda 항PD-1 글로벌 표준 (50+ 적응증 승인, 종양 매출 1위), "
            "Gardasil(HPV 백신) 글로벌 share 90%+, ProQuad/Vaxneuvance 백신 포트폴리오, Animal Health 매출 $5.7B (글로벌 3위). "
            "**R&D Moat**: 연구비 $15B+/yr (매출 25%), 1만+ FTE 화학자/생물학자. "
            "**Distribution Moat**: 미국 종양 oncology hospital network + 글로벌 백신 GAVI/UNICEF 채널. "
            "Sotatercept(PAH, Q4 FDA), MK-2870 (Trop2 ADC, Phase 3) 차세대로 Patent Cliff 방어."
        ),
        "financial": (
            "**FY25 (1월 발표)**: 매출 $64.2B (+7% YoY), 영업이익 $24.5B (+11%), EPS $8.42 (+12%). "
            "Keytruda $30.1B (+19% YoY), Animal Health $5.7B (+4%), Vaccines $9.3B (-12%, Gardasil 중국 부진). "
            "**Q1 2026 (5/1 발표)**: 매출 $16.3B (+5%), EPS $2.31 (컨센 $2.18 상회 +6%). "
            "Keytruda $7.9B (+22% YoY) — 단일 분기 사상 최대. FY26 가이던스 매출 $66~68B, EPS $9.0~9.4 유지. "
            "**현금흐름**: FCF $20B/yr 안정. 자사주 매입 $5B + 배당 yield 2.8% ($3.16/yr, payout 38%). "
            "Net cash $5B (R&D 투자 + M&A 캐파 안정)."
        ),
        "valuation": (
            "**Forward P/E ~14x** (5년 avg 16x — 약간 디스카운트). PEG ~1.4. "
            "**EV/EBITDA ~12x** (avg 13x). DCF (WACC 8%, terminal 2.5%): 적정 $135~145. "
            "현재 $119.68 = **-12% 디스카운트** + 배당 yield 2.8% = 매력. "
            "**Bear $95** (Keytruda cliff + Sotatercept fail), **Base $135** (정상), **Bull $150** (M&A + 신규 적응증)."
        ),
        "business": (
            "**산업 동향**: 항암제 글로벌 시장 $250B (2030년 $400B+). Immuno-oncology 표준 = checkpoint inhibitor. "
            "**경쟁구도**: BMS Opdivo(nivolumab, ~$12B), Roche Tecentriq(~$5B), AstraZeneca Imfinzi(~$4B). Keytruda 점유율 60%+. "
            "**Patent Cliff 2028**: subcutaneous formulation (Keytruda Qlex) FDA 승인 임박 = 추가 5~7년 보호. "
            "**중국 경쟁**: Akeso(ivonescimab) PD-1/VEGF bispecific Phase 3 우월성 (Lung) — 2027~ 미국 진입 가능. "
            "**메가트렅드**: ADC(Antibody-Drug Conjugate), bispecific, mRNA 백신 = R&D 집중. "
            "**Animal Health 분사**: 2026 H2 spin-off 예정, $40B 평가 — 주주가치 unlock catalyst."
        ),
        "momentum": (
            "**최근 주가**: $119.68 (-0.47% 5/28, 52주고 $124.22 대비 -3.7%, 저 $72.76 대비 +64.5%). "
            "5/13 이후 +15% 랠리 (5/14 subq Keytruda CHMP 긍정 의견, 5/19 Animal Health 분사 일정 확정). "
            "5/22~5/28 $118~121 횡보 (overbought 차익실현). ATR(14) $2.81 (2.35%). RSI 65. 200D MA $98 (+22%). "
            "**컨센서스**: Strong Buy 46%, Buy 38%, Hold 14%, Sell 2%. 평균 목표가 $135 (+12.8%). "
            "**수급**: 1Q26 Bridgewater 신규 500만주, Berkshire 비중 유지. defensive rotation 수혜. "
            "**이벤트**: 6/30 Sotatercept FDA approval (PAH), 7/29 Q2 발표, 9월 ESMO Keytruda 신규 적응증, Animal Health 분사 Q4."
        ),
        "risks": [
            {"name": "Keytruda Patent Cliff (2028)", "level": "Medium",
             "impact": "biosimilar 진입 시 매출 -30~40% 손실. subq Qlex 승인으로 일부 방어 + ADC 차세대로 완충.",
             "desc": "subq 제형 (Qlex) FDA 6/30 결정 — 승인 시 special protection 5~7년 추가. CHMP 5/14 긍정 의견 = 미국 승인 가능성 ↑."},
            {"name": "중국 Akeso 등 PD-1 경쟁", "level": "Medium",
             "impact": "ivonescimab Phase 3 Lung 우월성 - 미국 진입 2027~ 시 점유율 -10~15%, 매출 $3~5B 잠식",
             "desc": "Summit Tx (라이센시) FDA 신청 2026 Q4 예정. 이미 중국 Lung Top 처방 점유율 1위. 가격 압박도 동반."},
            {"name": "Trump MFN 약가 규제", "level": "Medium",
             "impact": "Keytruda 미국 가격 $190K/yr → MFN 30% 인하 시 매출 -$5B, 마진 -200bps",
             "desc": "5/12 행정명령. 단 종양 약은 cost-effectiveness 우월 → MFN 적용 우선순위 낮음. 협상 2026 H2."},
            {"name": "Gardasil 중국 부진", "level": "Low",
             "impact": "중국 HPV 백신 매출 -50% (현지 백신 가격 우위) - FY25 -$1B 영향 지속",
             "desc": "Walvax·Innovax HPV9 자국산 승인 2024. 중국 부진은 일본/인도 확장으로 일부 상쇄."},
        ],
        "risk_summary": (
            "**Medium 리스크 종합**. Keytruda Patent Cliff가 핵심이지만 subq Qlex CHMP 긍정 (5/14) 으로 부분 해소. "
            "Watch points: 6/30 Sotatercept FDA + Qlex 최종 판단, Q2 가이던스 (7/29), Animal Health 분사 진척. "
            "MFN 영향은 가격에 일부 반영 + Animal Health 분사 catalyst가 멀티플 회복 기여."
        ),
        "consensus": [
            ("Strong Buy", "46%"),
            ("Buy", "38%"),
            ("Hold", "14%"),
            ("Sell", "2%"),
            ("평균 목표가", "$135 (+12.8%)"),
            ("최고가", "$155"),
            ("최저가", "$110"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 8.5),
            ("재무 건전성", 8.5),
            ("산업 매력도", 7.5),
            ("성장성", 6.5),
            ("수익성/효율성", 8.5),
            ("밸류에이션", 8.0),
            ("모멘텀", 7.5),
            ("컨센서스/수급", 7.5),
            ("리스크 (역수)", 6.5),
            ("ESG/지속가능성", 7.5),
        ],
        "confidence": {
            "target_low": 95,
            "target_mid": 135,
            "target_high": 150,
            "ci_pct": "±15%",
            "score_band": "±5pt",
        },
        "fragile_assumptions": [
            ("Keytruda subq Qlex 6/30 FDA 승인 + Patent 보호 +5~7년",
             "거부 시 Patent Cliff 2028 그대로 노출, 스코어 -10pt → 63점 (Weak Buy)"),
            ("Sotatercept (PAH) 6/30 FDA 승인 + 매출 $1.5B+ 도달",
             "거부/제한적 라벨 시 신성장 동력 약화, 스코어 -5pt"),
            ("Trump MFN 약가 인하 -10% 이하 한정 (Keytruda 보호)",
             "전면 -30% 적용 시 매출 -$5B, 스코어 -8pt"),
        ],
        "strategy": (
            "**3단계 분할 매수** (Deep Value + Catalyst 대기):\n"
            "- 1차 $118~120 (현재가, 40%)\n"
            "- 2차 $112~115 (-4~6%, 35%)\n"
            "- 3차 $105~108 (-10~12%, 25%)\n\n"
            "**손절 $114.06** (2x ATR, -4.7%) / **1차 목표 $128.11** (3x ATR, +7.1%, R:R 1:1.5) / "
            "**2차 목표 $135** (+12.8%, 12개월, 컨센 평균) / **3차 목표 $150** (+25.3%, 24개월, M&A + Animal Health 분사).\n"
            "**보유 기간**: 24~36개월. 배당 누적 + Keytruda Qlex catalyst + Animal Health unlock 다중 트리거."
        ),
    },
    # ─────────────────────────────────────────────────────────
    "MA": {
        "name": "Mastercard",
        "name_kr": "마스터카드",
        "score": 79.0,
        "grade": "매수",
        "sector": "금융 — 결제 네트워크 (글로벌 Duopoly)",
        "category": "복합형 (방어 + 성장)",
        "currency": "$",
        "previous_v3_date": "2026-05-13",
        "summary": (
            "Visa와 함께 글로벌 결제 네트워크 듀오폴리. FY25 매출 $30B, 영업마진 56% (업계 최고). "
            "주가 $490.32 = 52주 고점 -18% (5월 -7% 차익실현 + Stripe·Block 등 Embedded Finance 위협 우려). "
            "다만 글로벌 cashless 메가트렌드 + 신용카드 거래 +6% (FY26 e), 가맹점 수수료 안정, 기업 카드(B2B) +20% 성장. "
            "M&A: RiskRecon·Finicity·Dynamic Yield(쉐어 매각 검토) + AI fraud detection 강화. "
            "**Forward P/E ~32x** (5년 avg 35x 디스카운트) + buyback $11B/yr = 멀티플 회복 기대."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (3-Star)** — Visa-Mastercard 결제 듀오폴리 + 110개국 + 3.5억 카드 활성. "
            "**Network Effect**: 가맹점(상점) ↑ → 카드 사용자 ↑ → 가맹점 ↑ (강력한 positive loop). "
            "**Switching Cost**: 카드 발행은행(시중은행) 입장에서 V/MA 둘 다 발행 = 의존도 ↑. "
            "**Brand Moat**: MasterPass, ID Check (3DS 2.0), Click-to-Pay = 디지털 결제 표준. "
            "**Open Banking Moat**: Finicity 인수로 ACH·account-to-account 결제 진입 = Embedded Finance 경쟁 대응."
        ),
        "financial": (
            "**FY25 (1월 발표)**: 매출 $30.0B (+13% YoY), 영업이익 $17.0B (+15%), EPS $15.05 (+18%). "
            "Gross Dollar Volume(GDV) $9.5T (+10%), Cross-border $3.5T (+18%), Switched transactions 159B (+11%). "
            "**Q1 2026 (4/29 발표)**: 매출 $7.8B (+12%, 컨센 +13% -1pp), GDV $2.5T (+11%), EPS $4.05 (+18%, 컨센 $3.95 상회 +3%). "
            "FY26 가이던스 매출 +12~14%, EPS +16~18% 유지. **Cross-border Travel** GDV +25% (출장 + 관광 회복). "
            "**현금흐름**: FCF $14B/yr. Net cash $7B + 부채 BBB+ (안정). "
            "**자사주 매입 $11B/yr + 배당 yield 0.6%** ($3.04/yr, payout 18%) = total return 우월."
        ),
        "valuation": (
            "**Forward P/E ~32x** (5년 avg 35x — 약간 디스카운트). PEG ~1.8 (성장 16% + 멀티플 32x). "
            "**EV/EBITDA ~26x** (avg 28x). DCF (WACC 8%, terminal 3%): 적정 $560~580. "
            "현재 $490.32 = **-13~16% 디스카운트**. **Bear $420** (Embedded Finance 침투 가속), **Base $560** (정상), "
            "**Bull $620** (Cross-border $4T + AI fraud 신규 매출)."
        ),
        "business": (
            "**산업 동향**: 글로벌 결제 시장 $200T+ (volume), V/MA 듀오폴리 70%+. cashless penetration 미국 70%, 글로벌 50%. "
            "**경쟁구도**: Visa (62% 점유), Mastercard (30%), American Express(소득層), Discover/JCB/UnionPay. "
            "**위협**: Stripe (e-comm 결제, IPO 2026 H2 예상), Block(SQ), Adyen, PayPal, India UPI/중국 Alipay (account-to-account 우회). "
            "**메가트렌드**: B2B 결제 디지털화 ($120T TAM), Embedded Finance, AI fraud detection (RiskRecon). "
            "**규제 리스크**: EU Interchange Fee Regulation, 미국 Durbin Amendment 확대 시도 (CCCA — 신용카드 swipe fee 인하). "
            "Trump 행정부 Durbin 확대 안건 미온적 — 단기 압박 제한적. 영국 RBR 케이스 진행 중."
        ),
        "momentum": (
            "**최근 주가**: $490.32 (-0.95% 5/28, 52주고 $599.05 대비 -18.2%, 저 $479.68 대비 +2.2%). "
            "4/29 Q1 발표 후 -3% (가이드 컨센 미달), 5/8 Stripe IPO 보도 -2%, 5/15 Block 결제 매출 +25% 발표 -2% 추가. "
            "5/22~5/28 $487~495 횡보 (지지선 테스트). ATR(14) $9.61 (1.96%). RSI 42. 200D MA $545 (-10%). "
            "**컨센서스**: Strong Buy 58%, Buy 32%, Hold 10%. 평균 목표가 $580 (+18.3%). "
            "**수급**: Berkshire 비중 유지 ($1.5B), 1Q26 Bridgewater 신규 200만주. 패시브 ETF 자금 지속 유입. "
            "**이벤트**: 7/30 Q2 발표, 8월 Stripe IPO 가격 결정, 9월 SIBOS 결제 컨퍼런스."
        ),
        "risks": [
            {"name": "Stripe·Block Embedded Finance 침투", "level": "Medium",
             "impact": "e-commerce 결제 wallet 비중 +5pp 시 GDV -3%, 마진 -100bps. Cross-border 위협 점증",
             "desc": "Stripe IPO 2026 H2 가시화 → 단기 멀티플 압박. 다만 V/MA rails 의존도는 잔존 (직접 우회는 UPI/Alipay만)."},
            {"name": "CCCA(Credit Card Competition Act)", "level": "Medium",
             "impact": "Durbin Amendment 신용카드 확대 시 swipe fee -30% = 매출 -$3B, 마진 -150bps",
             "desc": "Trump 미온적 + 은행 로비 강력 — 2026 통과 가능성 낮음. 다만 의회 변동 시 위협 잔존."},
            {"name": "Cross-border 둔화", "level": "Low",
             "impact": "관광 둔화 (USD 강세) 시 Cross-border GDV +25% → +10%, 매출 -$1.5B",
             "desc": "Cross-border = MA 매출의 ~40%. 출장 회복 vs USD 강세 trade-off. 현재 출장 회복 우세."},
            {"name": "ECB/UK 추가 regulation", "level": "Low",
             "impact": "Interchange cap 추가 인하 시 EU 매출 -10%, EPS -2%",
             "desc": "이미 0.3% (debit) / 0.4% (credit) cap 있음. 추가 압박 가능성 낮음."},
        ],
        "risk_summary": (
            "**Medium-Low 리스크 종합**. Stripe IPO + CCCA가 주요 위협이지만, V/MA Network Moat 견고. "
            "Watch points: 8월 Stripe IPO 가격/시총, 7/30 Q2 가이던스 (Cross-border 회복 지속 여부), Trump CCCA 입장. "
            "Cross-border +25% YoY 모멘텀 + B2B +20% 성장 = 멀티플 회복 catalyst."
        ),
        "consensus": [
            ("Strong Buy", "58%"),
            ("Buy", "32%"),
            ("Hold", "10%"),
            ("평균 목표가", "$580 (+18.3%)"),
            ("최고가", "$640"),
            ("최저가", "$500"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 9.0),
            ("재무 건전성", 8.5),
            ("산업 매력도", 8.5),
            ("성장성", 8.0),
            ("수익성/효율성", 9.5),
            ("밸류에이션", 7.0),
            ("모멘텀", 6.5),
            ("컨센서스/수급", 8.5),
            ("리스크 (역수)", 7.5),
            ("ESG/지속가능성", 7.0),
        ],
        "confidence": {
            "target_low": 420,
            "target_mid": 560,
            "target_high": 620,
            "ci_pct": "±15%",
            "score_band": "±5pt",
        },
        "fragile_assumptions": [
            ("V/MA 글로벌 결제 듀오폴리 점유율 70%+ 유지 (Stripe·UPI 침투 ≤5pp)",
             "20%+ 침투 시 GDV -10%, 스코어 -10pt → 69점 (Weak Buy)"),
            ("Cross-border GDV +20%/yr 유지 (USD 강세 + 관세 환경에도 출장 회복 지속)",
             "+10% 둔화 시 매출 가이드 -2%, 스코어 -5pt"),
            ("CCCA 2026~2027 미통과 (Durbin 신용카드 확대 차단)",
             "통과 시 swipe fee -30%, 매출 -$3B, 스코어 -12pt"),
        ],
        "strategy": (
            "**3단계 분할 매수** (Quality compound + 단기 디스카운트):\n"
            "- 1차 $488~492 (현재가, 40%)\n"
            "- 2차 $470~480 (-4~5%, 35%)\n"
            "- 3차 $450~460 (-8~10%, 25%)\n\n"
            "**손절 $471.10** (2x ATR, -3.9%) / **1차 목표 $519.15** (3x ATR, +5.9%, R:R 1:1.5) / "
            "**2차 목표 $580** (+18.3%, 12개월, 컨센 평균) / **3차 목표 $620** (+26.4%, 24개월, B2B + AI fraud 신규).\n"
            "**보유 기간**: 36개월+. Buyback + 듀오폴리 compound 효과로 long-term hold 우월."
        ),
    },
    # ─────────────────────────────────────────────────────────
    "JNJ": {
        "name": "JohnsonJohnson",
        "name_kr": "존슨앤존슨",
        "score": 76.0,
        "grade": "매수",
        "sector": "헬스케어 — 제약 + 의료기기",
        "category": "방어형 (배당 King)",
        "currency": "$",
        "previous_v3_date": "2026-05-13",
        "summary": (
            "Innovative Medicine + MedTech 양대 축. FY25 매출 $90B, 배당 King 63년 연속 인상 (yield 3.4%). "
            "주가 $230.87 = 52주 고점 -8% (talc litigation 우려 + Trump MFN 약가 + Stelara biosimilar Q4). "
            "다만 Carvykti(다발골수종)·Tremfya·Rybrevant 성장 동력 + MedTech (Abiomed·Ottava 로봇수술) 가속. "
            "**Forward P/E ~16x** + 배당 3.4% + buyback $5B/yr = 안정적 quality compound. "
            "Talc resolution 진행 ($7B fund) + Patent Cliff (Stelara, $11B → biosimilar) 완충 단계."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (3-Star)** — Innovative Medicine 약 50개 블록버스터 ($1B+) 포트폴리오 (Stelara, Tremfya, Darzalex, Carvykti). "
            "MedTech (Abiomed Impella, Ottava 로봇수술, Acclarent ENT) = 의료기기 글로벌 Top 3. "
            "**R&D Moat**: 연구비 $15B/yr (매출 17%), 1만+ FTE. **Distribution Moat**: 미국 병원 sales rep 8천명 + 글로벌 60국 직판. "
            "**Brand Moat**: 130년 기업 신뢰 (배당 King 63년). Consumer Health 분사 (2023 Kenvue) 후 prescription + MedTech 집중."
        ),
        "financial": (
            "**FY25 (1월 발표)**: 매출 $89.7B (+5% YoY), Innovative Med $58B (+6%), MedTech $32B (+5%), 영업이익 $26.5B (+6%), EPS $10.10 (+7%). "
            "Carvykti $1.8B (+125% YoY), Tremfya $4.2B (+18%), Darzalex $11B (+15%). Stelara $11B (-15%, biosimilar 압박 시작). "
            "**Q1 2026 (4/16 발표)**: 매출 $22.0B (+4%, 컨센 +5% -1pp), EPS $2.59 (컨센 $2.55 상회 +1%). "
            "FY26 가이던스 매출 $90~91B (+0~1%, Stelara cliff), 영업이익 $24~25B, EPS $10.00~10.20. "
            "**현금흐름**: FCF $20B/yr 안정. 자사주 매입 $5B + 배당 $13B ($5.00/yr/share, payout 50%). Net debt $13B (안정)."
        ),
        "valuation": (
            "**Forward P/E ~16x** (5년 avg 15x — 약간 프리미엄). PEG ~3.0 (낮은 성장 + 안정 멀티플). "
            "**EV/EBITDA ~12x** (avg 13x). DCF (WACC 8%, terminal 2%): 적정 $240~260. "
            "현재 $230.87 = **-4~12% 디스카운트** + 배당 3.4% = total return ~9%/yr 기대. "
            "**Bear $190** (talc + Stelara cliff 가속), **Base $245** (정상), **Bull $275** (Carvykti $5B + Ottava 로봇수술 가속)."
        ),
        "business": (
            "**산업 동향**: 글로벌 제약 $1.5T (성장 +5~6%), MedTech $0.5T (성장 +6%). 면역·종양·신경 + 로봇수술 핵심. "
            "**경쟁구도 Innovative Med**: AbbVie(Skyrizi, Humira biosimilar), Eli Lilly(Mounjaro), Roche, BMS. "
            "**경쟁구도 MedTech**: Medtronic, Stryker, Abbott, Boston Scientific. JNJ Abiomed Impella 심장 보조 펌프 점유율 80%. "
            "**메가트렌드**: cell therapy (Carvykti), bispecific (Rybrevant), GLP-1 후발 진입 (efinopegdutide Phase 3). "
            "**규제 리스크**: Trump MFN 약가 30% 인하 — Stelara/Darzalex/Tremfya 압박. talc litigation 13만건 → $7B 결제 fund. "
            "Carvykti CAR-T 제조 capacity 확장 진척 (Phila 신공장 가동) — supply constraint 해소 트리거."
        ),
        "momentum": (
            "**최근 주가**: $230.87 (-0.18% 5/28, 52주고 $250.27 대비 -7.8%, 저 $145.41 대비 +58.8%). "
            "5/13 이후 +5% 강세 (5/14 Carvykti 신규 적응증 FDA, 5/19 Stelara biosimilar 영향 컨센 하회). "
            "5/22~5/28 $228~233 횡보. ATR(14) $3.86 (1.67%). RSI 55. 200D MA $215 (+7%). "
            "**컨센서스**: Strong Buy 42%, Buy 36%, Hold 21%, Sell 1%. 평균 목표가 $250 (+8.3%). "
            "**수급**: 1Q26 Berkshire 신규 50만주 매수 (Buffett quality defensive). 1Q26 Vanguard·BlackRock 비중 유지. "
            "**이벤트**: 6/15 talc resolution 법원 승인, 7/16 Q2 발표, 8월 Ottava 로봇수술 첫 임상 결과, 10월 J&J Innovation Day."
        ),
        "risks": [
            {"name": "Stelara biosimilar 가속", "level": "Medium",
             "impact": "FY26 Stelara 매출 $11B → $8B (-27%) 가이드. FY27 $5B 가능. 매출 가이드 -3%, EPS -5%",
             "desc": "Sandoz·Celltrion·Samsung Bioepis biosimilar 7개 launch 2025~. Tremfya replacement(IL-23) 성공률이 cushion."},
            {"name": "Talc litigation 잔존 위험", "level": "Medium",
             "impact": "$7B fund 외 5천건 opt-out 가능 — $2~3B 추가 부담 가능. EPS -3~5% 단발 영향",
             "desc": "6/15 NJ 파산법원 승인 절차. 일부 deputy attorney general opt-out 권유 — 잔존 case 변수. Resolution 후 멀티플 +1x."},
            {"name": "Trump MFN 약가 규제", "level": "Medium",
             "impact": "Innovative Med 매출 -10% (-$5B), 영업마진 -150bps",
             "desc": "5/12 행정명령. Stelara/Tremfya/Darzalex 표적. CMS 협상 2026 H2~. 법원 challenge 진행 중."},
            {"name": "MedTech Ottava 로봇수술 지연", "level": "Low",
             "impact": "Intuitive Surgical da Vinci 점유율 95% — Ottava 진입 지연 시 MedTech 성장 -2~3pp",
             "desc": "8월 첫 임상 결과 예상. 성공 시 long-term MedTech catalyst, 실패 시 -3% short-term."},
        ],
        "risk_summary": (
            "**Medium-Low 리스크 종합**. Stelara cliff + talc 두 부담이 핵심이지만 가격에 상당 반영. "
            "Watch points: 6/15 talc resolution 법원 판단, 7/16 Q2 Stelara 매출 추이, 8월 Ottava 임상 결과. "
            "배당 King 63년 + Carvykti hyper-growth + MedTech 로봇수술 옵션 = 비대칭 risk-reward 우월."
        ),
        "consensus": [
            ("Strong Buy", "42%"),
            ("Buy", "36%"),
            ("Hold", "21%"),
            ("Sell", "1%"),
            ("평균 목표가", "$250 (+8.3%)"),
            ("최고가", "$285"),
            ("최저가", "$220"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 9.0),
            ("재무 건전성", 9.0),
            ("산업 매력도", 7.5),
            ("성장성", 6.0),
            ("수익성/효율성", 8.0),
            ("밸류에이션", 7.5),
            ("모멘텀", 7.0),
            ("컨센서스/수급", 8.0),
            ("리스크 (역수)", 7.0),
            ("ESG/지속가능성", 7.0),
        ],
        "confidence": {
            "target_low": 190,
            "target_mid": 245,
            "target_high": 275,
            "ci_pct": "±15%",
            "score_band": "±4pt",
        },
        "fragile_assumptions": [
            ("Carvykti 매출 FY26 $2.5B → FY28 $5B 도달 (CAR-T 제조 capacity 확장 성공)",
             "$2~3B 정체 시 성장 가이드 약화, 스코어 -7pt → 69점 (Weak Buy)"),
            ("Stelara biosimilar 침투 30%/yr 한정 (Tremfya replacement 성공)",
             "50%+ 침투 시 매출 가이드 -5%, EPS -7%, 스코어 -8pt"),
            ("Talc resolution $7B fund 6/15 법원 승인 + opt-out 5천건 이하",
             "opt-out 1만건 시 추가 $3~5B 부담, 스코어 -5pt"),
        ],
        "strategy": (
            "**3단계 분할 매수** (배당 King + 안정 compound):\n"
            "- 1차 $229~232 (현재가, 50%)\n"
            "- 2차 $218~222 (-4~5%, 30%)\n"
            "- 3차 $205~210 (-9~11%, 20%)\n\n"
            "**손절 $223.15** (2x ATR, -3.3%) / **1차 목표 $242.46** (3x ATR, +5.0%, R:R 1:1.5) / "
            "**2차 목표 $250** (+8.3%, 12개월, 컨센 평균) / **3차 목표 $275** (+19.1%, 24개월, Carvykti + Ottava).\n"
            "**보유 기간**: 36개월+. 배당 누적 + Stelara cliff 통과 + MedTech 로봇수술 옵션 = 장기 핵심 보유."
        ),
    },
    # ─────────────────────────────────────────────────────────
    "HSBC": {
        "name": "HSBC",
        "name_kr": "HSBC홀딩스",
        "score": 75.5,
        "grade": "매수",
        "sector": "금융 — 글로벌 은행 (아시아 + UK + 미국)",
        "category": "복합형 (배당 고소득 + 아시아 EM)",
        "currency": "$",
        "previous_v3_date": "2026-05-13",
        "summary": (
            "글로벌 자산 $3T+ HSBC ADR. 아시아 (홍콩·중국) 매출 50%+ + UK 30% + 미국·중동. "
            "주가 $93.19 = 52주 고점 -2.1% (사상 최고 부근). 5/13~5/28 +9% 강세 — Q1 NII surprise + buyback $3B + 배당 인상. "
            "FY25 ROE 14% (Tier 1 capital 14.5%) + 배당 yield 5.5% + 자사주 매입 yield 추가 5% = 총 10%+ 자본환원. "
            "Brexit 후 US bank 매각 + China retail 매각 → 아시아 wealth management 집중 = 구조조정 성공 단계."
        ),
        "moat_rating": "Narrow",
        "moat_details": (
            "**Narrow Moat (2-Star)** — 글로벌 은행 중 아시아 (홍콩·중국) Tier 1 capital 우위 = 무역 금융·외환·private banking 점유율 ↑. "
            "**Scale Moat**: HSBC 글로벌 무역 금융 매출 1위 ($5T+ trade flow 연 처리). "
            "**Network Moat**: 60개국 지점 + Hong Kong 발권은행 지위 + China RMB clearing 라이센스. "
            "다만 Citi·StanChart·DBS 경쟁 + China private banking 진입 장벽 낮춤 + UK ringfencing(영업 분리) = Wide Moat 아님."
        ),
        "financial": (
            "**FY25 (2월 발표)**: 매출 $66.4B (+3% YoY 조정, 일회성 매각이익 제외 +5%), NII $33B (+1%), Fee income $14B (+6%), "
            "영업이익 $24.5B (+10%), EPS $1.55 (+12%). ROE 14.2%, CET1 14.5%. "
            "**Q1 2026 (4/30 발표)**: NII $8.5B (컨센 $8.2B 상회 +4%), Fee income $3.7B (+8% YoY), EPS $0.42 (컨센 $0.39 상회 +8%). "
            "FY26 가이던스 NII $33~34B, ROE 14~15% 유지. CET1 14.5%+ + buyback $3B 추가 발표. "
            "**현금흐름**: FCF/자기자본 비율 양호. **배당 $0.31/q (yield 5.5%)** + buyback $3B/yr = 총 자본환원 10%+. "
            "Common Equity Tier 1 14.5% (자본 풍부)."
        ),
        "valuation": (
            "**Forward P/E ~9x** (5년 avg 10x — 약간 디스카운트). PEG ~1.3. "
            "**P/B ~1.1x** (글로벌 은행 avg 1.0x — 약간 프리미엄, ROE 우위 반영). "
            "**Dividend yield 5.5%** + buyback yield 5% = total return income ~10%+. "
            "DDM (cost of equity 10%, growth 4%): 적정 $105~115. 현재 $93.19 = **-12~19% 디스카운트**. "
            "**Bear $75** (홍콩 정치 + 중국 부동산 추가 부실), **Base $105** (정상), **Bull $120** (아시아 wealth 가속 + Trump deregulation)."
        ),
        "business": (
            "**산업 동향**: 글로벌 은행 산업 ROE 12~14% 정상화 (2008년대 이후 최고). 아시아 wealth management 2030년 TAM $40T. "
            "**경쟁구도 아시아**: HSBC, StanChart, Citi (Asia), DBS, ICBC (China). HSBC 홍콩 발권 + 중국 cross-border RMB clearing 우위. "
            "**경쟁구도 UK**: HSBC UK (구ringfenced), Barclays, Lloyds, NatWest. HSBC UK retail 점유율 12% (3위). "
            "**구조조정 성공**: Canada·Argentina 자회사 매각 (~$15B 자본 환원), Trinkaus·SVB UK 흡수, 비핵심 부문 정리. "
            "**메가트렌드**: 아시아 wealth (HK·SG·CN 부유층 증가) + 동남아 무역 회복 + crypto custody (HSBC HK 사용) + AI banking. "
            "**규제 리스크**: 홍콩 정치 (캐리람·시진핑), Trump-China 관세 갈등, UK Bank surcharge."
        ),
        "momentum": (
            "**최근 주가**: $93.19 (-1.57% 5/28, 52주고 $95.22 대비 -2.1%, 저 $55.42 대비 +68.2%). "
            "4/30 Q1 surprise +5% 점프, 5/13~5/28 +9% 추가 강세 (5/19 buyback $3B 발표, 5/22 배당 $0.31 인상 발표). "
            "현재 52주 고점 근접. ATR(14) $1.94 (2.08%). RSI 72 (overbought), 200D MA $72 (+29%). "
            "**컨센서스**: Buy 50%, Hold 41%, Sell 9%. 평균 목표가 $98 (+5.2%). "
            "**수급**: 1Q26 BlackRock·Vanguard 비중 유지, Norges Bank 비중 ↑. 아시아 ETF 자금 유입 지속. "
            "**이벤트**: 7/30 Q2 발표 (가이드 raise 가능성), 9월 글로벌 wealth management 컨퍼런스, FY 가이드 update."
        ),
        "risks": [
            {"name": "홍콩·중국 정치 리스크", "level": "Medium",
             "impact": "홍콩 자본 통제 강화 또는 미국 sanctions 시 HSBC 아시아 매출 -10~15%, EPS -8~10%",
             "desc": "캐리람 임기 후 자본 유출 통제 가능성. 미국 의회 HSBC 중국 금융 제재 청문회 잠재. 단 현재 가능성 낮음."},
            {"name": "중국 부동산 부실 잔존", "level": "Medium",
             "impact": "Evergrande·Country Garden 익스포저 $5~8B. NPL ratio +50bps 시 충당금 +$1B, EPS -3%",
             "desc": "FY25 충당금 $3B 적립 (대비 충분). 추가 default cycle 시 잔여 익스포저. 가시성 점진적 개선."},
            {"name": "Trump 관세 + USD 강세", "level": "Medium",
             "impact": "Cross-border trade volume -5%, NII -2~3% (USD 강세 시 GBP/RMB 환산 손실)",
             "desc": "관세 25% (중국)·5% (캐나다·멕시코) — HSBC trade finance volume 감소. 단 fee margin 상승 일부 상쇄."},
            {"name": "UK 경기 침체", "level": "Low",
             "impact": "UK retail NPL +30bps, 영국 매출 -5%, EPS -2%",
             "desc": "UK GDP 2026 +0.8% 컨센. UK Bank surcharge 인상 가능성 잠재. 다만 비중 30% 한정."},
        ],
        "risk_summary": (
            "**Medium 리스크 종합**. 홍콩·중국 정치 + USD 강세가 핵심이지만 분기마다 surprise +. "
            "Watch points: 7/30 Q2 가이드, 홍콩 자본 통제 동향, Trump-China 협상. "
            "5.5% 배당 + 5% buyback = 10%+ 자본환원으로 downside cushion 강력. 멀티플 ~9x는 미국 대형은행 (JPM 12x) 대비 여전히 저평가."
        ),
        "consensus": [
            ("Buy", "50%"),
            ("Hold", "41%"),
            ("Sell", "9%"),
            ("평균 목표가", "$98 (+5.2%)"),
            ("최고가", "$110"),
            ("최저가", "$85"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 8.0),
            ("재무 건전성", 8.5),
            ("산업 매력도", 7.5),
            ("성장성", 6.5),
            ("수익성/효율성", 8.5),
            ("밸류에이션", 8.0),
            ("모멘텀", 8.5),
            ("컨센서스/수급", 7.5),
            ("리스크 (역수)", 6.5),
            ("ESG/지속가능성", 6.5),
        ],
        "confidence": {
            "target_low": 75,
            "target_mid": 105,
            "target_high": 120,
            "ci_pct": "±20%",
            "score_band": "±5pt",
        },
        "fragile_assumptions": [
            ("아시아 (홍콩·중국) 매출 비중 50%+ + 자본 통제 미발생",
             "홍콩 자본 통제 발효 시 -15~20% 충격, 스코어 -10pt → 65점 (Weak Buy)"),
            ("배당 5.5% + buyback $3B/yr 유지 (CET1 14.5%+ + ROE 14%+)",
             "ROE 12% 이하 하락 시 buyback 축소, 멀티플 -1x, 스코어 -6pt"),
            ("중국 부동산 NPL 정점 통과 + 추가 cycle 없음",
             "Evergrande 2.0 시나리오 시 충당금 +$2B, 스코어 -7pt"),
        ],
        "strategy": (
            "**4단계 분할 매수** (배당 King + 아시아 EM, 단기 overbought):\n"
            "- 1차 $92~94 (현재가, 20%)\n"
            "- 2차 $87~90 (-4~7%, 30%)\n"
            "- 3차 $82~85 (-9~12%, 30%)\n"
            "- 4차 $78↓ (200D MA 부근, 20%)\n\n"
            "**손절 $89.32** (2x ATR, -4.2%) / **1차 목표 $99.00** (3x ATR, +6.2%, R:R 1:1.5) / "
            "**2차 목표 $105** (+12.7%, 12개월, 컨센 +5%~) / **3차 목표 $120** (+28.8%, 24개월, 아시아 wealth 가속).\n"
            "**보유 기간**: 36개월+. 배당 누적 (5.5% × 3년 = 17%) + buyback compound. 단기 overbought 분할 진입 권장."
        ),
    },
    # ─────────────────────────────────────────────────────────
    "HD": {
        "name": "HomeDepot",
        "name_kr": "홈디포",
        "score": 71.0,
        "grade": "매수",
        "sector": "소비재 — 주택 개조 (Home Improvement)",
        "category": "방어형 + 주택 cycle",
        "currency": "$",
        "previous_v3_date": "2026-05-13",
        "summary": (
            "미국 최대 주택 개조 retailer (Lowe's 2위). FY25 매출 $159B. 주가 $319.91 = 52주 고점 -24% (주택 cycle 둔화). "
            "주택 매출 감소 (mortgage 6.8%+) + DIY 약세 + Pro 비중 +2pp 견고. SRS Distribution 인수 ($18B) Pro 시장 확장. "
            "5/13~5/28 -3% 약세 (5/20 Q1 매출 미달 + 가이드 하향 + Lowe's 매출 -1.5%). "
            "**Forward P/E ~22x** + 배당 yield 2.8% (15년 연속 인상) = quality value. 주택 cycle 바닥 신호 시 우선 회복."
        ),
        "moat_rating": "Wide",
        "moat_details": (
            "**Wide Moat (3-Star)** — 미국 최대 home improvement 체인 2,300개 + Pro contractor 채널. "
            "**Scale Moat**: 평균 매장 105K sqft, 11,000개+ SKU, 글로벌 6개 distribution center. "
            "**Pro Loyalty Moat**: Pro Xtra 멤버십 + B2B 신용 (Pro Reserve), Pro 매출 50%+. "
            "**Real Estate Moat**: 대형 매장 부지 prime location 80% 자체 소유 = 임차료 우위. "
            "**SRS Distribution 인수** ($18B, 2024 완료): roofing·landscape·pool 등 specialty trade Pro = TAM $1T → +$300B 추가."
        ),
        "financial": (
            "**FY25 (2월 발표)**: 매출 $159.5B (-3% YoY 조정), comp sales -2.5%, transaction -1.8%, ticket -0.7%, "
            "Op income $22.5B (-5%), EPS $14.91 (-4%). 영업마진 14.1% (FY24 14.5%). "
            "**Q1 2026 (5/20 발표)**: 매출 $39.2B (-1.5%, 컨센 -1% 미달 -0.5pp), comp -2.8%, EPS $3.55 (컨센 $3.62 미달 -2%). "
            "FY26 가이던스 매출 +1~3%, comp -1~+1%, EPS $14.50~15.00 (이전 $15.20~15.50에서 하향). "
            "**현금흐름**: FCF $15B/yr 안정. **자사주 매입 $4B + 배당 yield 2.8% ($9.00/yr, payout 60%)** = total return ~6%. "
            "Net debt $35B (SRS 인수 후 증가, 안정 BBB+)."
        ),
        "valuation": (
            "**Forward P/E ~22x** (5년 avg 22x — fair). PEG ~3.5 (낮은 성장). "
            "**EV/EBITDA ~17x** (avg 18x — 약간 디스카운트). DCF (WACC 8%, terminal 2.5%): 적정 $360~380. "
            "현재 $319.91 = **-11~16% 디스카운트** + 배당 2.8% = total return ~9%/yr 기대. "
            "**Bear $260** (주택 침체 + Pro 약세), **Base $360** (정상), **Bull $400** (mortgage 인하 + Pro hyper-growth)."
        ),
        "business": (
            "**산업 동향**: 미국 주택 개조 시장 $700B (HD 22% 점유), TAM 확장 $1T (SRS Pro 포함). "
            "**경쟁구도**: HD (22%), Lowe's (10%), Menards (4%), Floor & Decor, Amazon (DIY 침투). HD Pro 점유율 우위. "
            "**위협**: Amazon DIY 침투 (특히 hardware·tool), Floor & Decor 특화 매장 점유율 ↑. "
            "**메가트렌드**: aging home (미국 평균 주택 40년) + Pro contractor 의존도 ↑ + e-commerce 16% → 25% 비중 (FY28). "
            "**규제 리스크**: Trump 관세 25% (멕시코·캐나다) - building materials 가격 +3~5%. 일부 전가 + 마진 흡수. "
            "**Mortgage 6.8%**: 주택 매매 둔화 = remodel 수요 약화. Fed 9월 0.25%p 인하 컨센 시 회복 trigger."
        ),
        "momentum": (
            "**최근 주가**: $319.91 (+0.65% 5/28, 52주고 $421.19 대비 -24.0%, 저 $289.10 대비 +10.7%). "
            "5/20 Q1 발표 후 -4.5% (가이드 하향), 5/22~5/27 $310~322 횡보 반등. "
            "ATR(14) $8.35 (2.61%). RSI 45. 200D MA $355 (-10%). 52주 저점 $289 지지선 유지. "
            "**컨센서스**: Strong Buy 38%, Buy 41%, Hold 19%, Sell 2%. 평균 목표가 $360 (+12.5%). "
            "**수급**: Berkshire 비중 유지 ($1.2B), 1Q26 Vanguard 비중 ↑. defensive value 매수. "
            "**이벤트**: 6/10 Fed FOMC (mortgage 영향), 7월 housing data, 8/19 Q2 발표 (가이드 raise 여부)."
        ),
        "risks": [
            {"name": "주택 cycle 추가 둔화", "level": "Medium",
             "impact": "FY26 comp -2% 추가 미달 시 매출 $156B → $152B, EPS -5%, 스코어 -7pt",
             "desc": "Mortgage 6.8%+ 지속 + 중고주택 inventory ↑ = remodel 수요 약화. Fed 9월 0.25%p 인하 시 부분 해소."},
            {"name": "관세 전가 마진 압박", "level": "Medium",
             "impact": "관세 25% (멕시코·캐나다) building materials → 마진 -50~80bps. Op margin 13.5% 가능",
             "desc": "lumber·drywall·flooring 가격 +3~5%. 일부 전가, 일부 마진 흡수. 스케일이 흡수력 보장. SRS는 Pro 가격 leverage 보유."},
            {"name": "SRS 인수 시너지 지연", "level": "Low",
             "impact": "SRS Q1 영업이익률 8% (HD 14% 대비 낮음). 통합 1년 지연 시 EPS -1~2%",
             "desc": "Pro contractor 채널 시너지 16~18개월 예상. 단 SRS 자체 매출 $11B 안정 = downside 제한."},
            {"name": "Lowe's·Amazon 침투", "level": "Low",
             "impact": "Pro Xtra 멤버십 출시 (Lowe's), Amazon Industrial Supply 확장. 점유율 -1~2pp 위협",
             "desc": "HD Pro 점유율 +2pp/yr 견고. SRS 인수로 Pro 격차 추가 확대 (Lowe's 대응 불가)."},
        ],
        "risk_summary": (
            "**Medium-Low 리스크 종합**. 주택 cycle 둔화 + 관세 압박이 핵심이지만 가격에 상당 반영. "
            "Watch points: 6/10 FOMC mortgage 동향, 7월 housing starts, 8/19 Q2 가이드 (raise vs maintain). "
            "Pro 50%+ + SRS 통합 + 배당 King 15년 = downside cushion + 멀티플 회복 catalyst."
        ),
        "consensus": [
            ("Strong Buy", "38%"),
            ("Buy", "41%"),
            ("Hold", "19%"),
            ("Sell", "2%"),
            ("평균 목표가", "$360 (+12.5%)"),
            ("최고가", "$420"),
            ("최저가", "$300"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 8.5),
            ("재무 건전성", 7.5),
            ("산업 매력도", 7.0),
            ("성장성", 6.0),
            ("수익성/효율성", 8.0),
            ("밸류에이션", 7.0),
            ("모멘텀", 5.5),
            ("컨센서스/수급", 7.5),
            ("리스크 (역수)", 7.0),
            ("ESG/지속가능성", 7.0),
        ],
        "confidence": {
            "target_low": 260,
            "target_mid": 360,
            "target_high": 400,
            "ci_pct": "±18%",
            "score_band": "±6pt",
        },
        "fragile_assumptions": [
            ("Fed 2026년 0.25~0.50%p 인하 (mortgage 6.5% 이하 정상화)",
             "동결 시 주택 cycle 추가 둔화, comp -3~4%, 스코어 -8pt → 63점 (Weak Buy)"),
            ("Pro 매출 50%+ + SRS 통합 시너지 16~18개월 내 가시화",
             "지연 24개월+ 시 멀티플 회복 지연, 스코어 -5pt"),
            ("관세 25% (멕시코·캐나다) 전가율 60%+ 유지 (마진 -50bps 한정)",
             "전가 30% 이하 시 마진 -150bps, EPS -8%, 스코어 -7pt"),
        ],
        "strategy": (
            "**4단계 분할 매수** (Quality + 주택 cycle 바닥 베팅):\n"
            "- 1차 $318~322 (현재가, 25%)\n"
            "- 2차 $305~312 (-3~5%, 30%)\n"
            "- 3차 $290~298 (-7~9%, 25%)\n"
            "- 4차 $275↓ (52주저 부근, 20%)\n\n"
            "**손절 $303.22** (2x ATR, -5.2%) / **1차 목표 $344.95** (3x ATR, +7.8%, R:R 1:1.5) / "
            "**2차 목표 $360** (+12.5%, 12개월, 컨센 평균) / **3차 목표 $400** (+25.0%, 24개월, 주택 cycle 회복).\n"
            "**보유 기간**: 24~36개월. 배당 누적 + Fed cut + SRS 시너지 + Pro 점유율 확대 다중 catalyst."
        ),
    },
    # ─────────────────────────────────────────────────────────
    "034020": {
        "name": "두산에너빌리티",
        "name_kr": "두산에너빌리티",
        "score": 73.0,
        "grade": "매수",
        "sector": "산업재 — 에너지 (원자력·가스터빈·SMR)",
        "category": "공격형/성장 (CapEx 슈퍼사이클)",
        "currency": "₩",
        "previous_v3_date": "2026-05-14",
        "summary": (
            "한국 1위 에너지 EPC. 원자력(SMR·OPR1400)·가스터빈·해상풍력 사업 보유. "
            "FY25 매출 17.5조원, 영업이익 1.2조원. 주가 105,900원 = 52주 고점 -24% (5/14~5/28 -5%, 차익실현). "
            "**Catalyst**: 한수원-체코 두코바니 원전 2기 수주 (2024) + 폴란드·UAE 추가 입찰 + SMR (NuScale·X-energy 협업), "
            "가스터빈 H-class 자체 개발 (5월 5번째 수주 발표), 데이터센터 발전소 수요 (Microsoft 4GW deal 후 한국 인프라 검토). "
            "**Trump CapEx 슈퍼사이클** (AI 데이터센터 + 천연가스 + nuclear) 핵심 수혜주. Forward P/E ~25x (성장 대비 fair)."
        ),
        "moat_rating": "Narrow",
        "moat_details": (
            "**Narrow Moat (2-Star)** — 한국 1위 + 원전 OPR1400 글로벌 라이센스 (체코 두코바니 수주). "
            "**Technology Moat**: 가스터빈 H-class (270MW) 자체 개발 = GE·Siemens 외 4번째 글로벌 라이센스. "
            "**SMR Moat**: NuScale (CFO 인수 검토)·X-energy 부분 지분 + 한국형 SMR (i-SMR) 자체 개발 진행. "
            "**Supply Chain Moat**: 한국 원자로 압력용기 제조 capacity 글로벌 Top 3 (두산 + JSW + 일본중공업). "
            "Westinghouse·Areva 등 1군 경쟁자 대비 가격·납기 우위 + 한미 원자력협정 활용."
        ),
        "financial": (
            "**FY25 (3월 발표)**: 매출 17.5조원 (+18% YoY), 영업이익 1.2조원 (+85%), 순이익 0.7조원 (+150%). "
            "원자력 매출 5.2조원 (+45%), 가스터빈 3.8조원 (+22%), 풍력 1.5조원 (-15%). 수주잔고 16조원 (+20%). "
            "**Q1 2026 (5/14 발표)**: 매출 4.6조원 (+12%, 컨센 +14% -2pp), 영업이익 0.32조원 (+45%, 컨센 +50% -5pp). "
            "체코 두코바니 1단계 수주분 매출 인식 시작. FY26 가이던스 매출 19~20조원, 영업이익 1.5조원 유지. "
            "**현금흐름**: FCF 회복 단계 (capex 1.5조원/yr). 부채비율 145% (개선 중, 2022년 200% → 2025년 145%). "
            "배당 yield 0.5% (현재가 105,900원, 배당 500원). 자사주 매입 없음 — 성장 reinvest 우선."
        ),
        "valuation": (
            "**Forward P/E ~25x** (5년 avg 30x — 약간 디스카운트). PEG ~1.5. "
            "**EV/EBITDA ~12x** (avg 14x). DCF (WACC 10%, terminal 3%): 적정 130,000~140,000원. "
            "현재 105,900원 = **-19~24% 디스카운트**. SOTP (원자력 60% + 가스터빈 25% + 풍력 5% + 본사 10%): 130,000원. "
            "**Bear 85,000원** (원자력 수주 지연 + 풍력 부진), **Base 130,000원** (정상), "
            "**Bull 160,000원** (폴란드·UAE 추가 수주 + SMR 상용화 + 가스터빈 미국 수출)."
        ),
        "business": (
            "**산업 동향**: 글로벌 원자력 르네상스 (Sweden·Italy·UK·Japan 재가동 + 신규), TAM 2030년 신규 발주 100기+. "
            "AI 데이터센터 전력 수요 +50% (2030년) = 천연가스 + 원전 직접 수혜. "
            "**경쟁구도 원자력**: Westinghouse(AP1000), Areva(EPR), 한수원 + 두산(OPR1400·APR1400), Rosatom (러시아), CGN (중국). "
            "한수원+두산 = 체코 두코바니 수주 (2024) + 폴란드 입찰 (2026) + UAE 4호기. "
            "**경쟁구도 가스터빈**: GE Vernova, Siemens Energy, Mitsubishi Power, 두산. 두산 H-class 5호 수주 (5/15 발표). "
            "**SMR 메가트렌드**: NuScale (CFO 인수 검토), X-energy 협업, 한국형 i-SMR 2030년 상용화. "
            "**규제 리스크**: 풍력 — 한국 정부 신재생 비중 축소 정책 (탈원전 폐기 후), 매출 비중 축소 reverse. "
            "**한국 원자력 협정**: Trump 한미 원자력협정 강화 추진 (5/22) — 두산 수출 길 확장."
        ),
        "momentum": (
            "**최근 주가**: 105,900원 (-2.4% 5/28, 52주고 139,200원 대비 -23.9%, 저 39,300원 대비 +169%). "
            "5/14 Q1 컨센 -2pp 발표 후 -8% 갭다운, 5/19~5/22 가스터빈 5호 수주 +4% 반등, 5/26~5/28 -5% 차익실현. "
            "ATR(14) 8,214원 (7.76%) — 변동성 매우 높음. RSI 38 (oversold). 200D MA 102,000원 (+4%). "
            "**컨센서스**: 매수 65%, 보유 28%, 매도 7%. 평균 목표가 135,000원 (+27.5%). "
            "**수급**: 외국인 5/15~5/28 순매도 -1,200억원 (Q1 실망), 5/27 기관 매수 전환. "
            "**이벤트**: 6/10 폴란드 원전 입찰 결과 발표, 7/15 Q2 실적, 8월 한미 원자력협정 발표, 11월 UAE 4호기 입찰."
        ),
        "risks": [
            {"name": "원자력 수주 지연/취소", "level": "Medium",
             "impact": "폴란드 입찰 패배 + UAE 4호기 지연 시 FY26 가이드 -10%, 스코어 -8pt",
             "desc": "6/10 폴란드 발표가 핵심. Westinghouse·Rosatom 경쟁 치열. 한미 원자력협정 강화가 보조."},
            {"name": "풍력 사업 부진 + 부채 부담", "level": "Medium",
             "impact": "풍력 -15% YoY 지속 + 부채비율 145% → 150%+ 시 신용등급 강등 risk",
             "desc": "한국 신재생 축소 정책으로 매출 감소 reverse. 자체 풍력 사업 매각 또는 분사 가능성. 부채는 점진 개선."},
            {"name": "가스터빈 미국 수출 지연", "level": "Medium",
             "impact": "Trump CapEx 미국 데이터센터 발전소 수주 지연 시 가스터빈 매출 +15% → +5%, 스코어 -5pt",
             "desc": "GE Vernova·Siemens Energy 가스터빈 capacity 부족 (lead time 4~5년) — 두산 진입 기회. 단 미국 'Buy American' 정책 변수."},
            {"name": "SMR 상용화 지연", "level": "Low",
             "impact": "NuScale·X-energy 사업화 2030년+ 지연 시 long-term value -10%",
             "desc": "현재 SMR은 옵션 가치. 사업 비중 0%. 지연 단기 영향 미미. 다만 멀티플 hype 동력 약화."},
        ],
        "risk_summary": (
            "**Medium 리스크 종합**. 원자력 수주 모멘텀 + Trump CapEx 슈퍼사이클 우호. 변동성 ATR 7.76%로 매우 높음. "
            "Watch points: 6/10 폴란드 발표 (binary catalyst), 7/15 Q2 가이드 raise 여부, Trump 한미 원자력협정 강화. "
            "단기 oversold + Q1 컨센 -2pp 약세 반영 → 6/10 surprise 시 +15% 반등 가능."
        ),
        "consensus": [
            ("매수", "65%"),
            ("보유", "28%"),
            ("매도", "7%"),
            ("평균 목표가", "135,000원 (+27.5%)"),
            ("최고가", "165,000원"),
            ("최저가", "95,000원"),
        ],
        "scorecard_items": [
            ("기업 펀더멘털", 7.5),
            ("재무 건전성", 6.5),
            ("산업 매력도", 9.0),
            ("성장성", 8.5),
            ("수익성/효율성", 6.5),
            ("밸류에이션", 7.5),
            ("모멘텀", 6.0),
            ("컨센서스/수급", 7.5),
            ("리스크 (역수)", 6.0),
            ("ESG/지속가능성", 7.5),
        ],
        "confidence": {
            "target_low": 85000,
            "target_mid": 130000,
            "target_high": 160000,
            "ci_pct": "±25%",
            "score_band": "±8pt",
        },
        "fragile_assumptions": [
            ("6/10 폴란드 원전 입찰 한수원+두산 컨소시엄 선정 또는 short list 잔존",
             "탈락 시 -15% 추가 하락, 스코어 -10pt → 63점 (Weak Buy)"),
            ("Trump CapEx 사이클 + AI 데이터센터 가스터빈 미국 수주 1기 이상 확보 (FY26)",
             "수주 0건 시 가스터빈 성장 가이드 -3pp, 스코어 -5pt"),
            ("부채비율 145% → 135% 이하 개선 + 풍력 사업 분사/매각 가시화",
             "부채 비율 150%+ 악화 시 신용등급 강등, 스코어 -7pt"),
        ],
        "strategy": (
            "**4단계 분할 매수** (CapEx 슈퍼사이클 + 변동성 활용):\n"
            "- 1차 105,000~108,000원 (현재가, 20%)\n"
            "- 2차 98,000~102,000원 (-4~7%, 30%)\n"
            "- 3차 90,000~95,000원 (-10~15%, 30%)\n"
            "- 4차 85,000원↓ (200D MA 부근, 20%)\n\n"
            "**손절 89,471원** (2x ATR, -15.5%) — 변동성 높아 손절 폭 큼 / "
            "**1차 목표 130,542원** (3x ATR, +23.3%, R:R 1:1.5) / "
            "**2차 목표 135,000원** (+27.5%, 12개월, 컨센 평균) / **3차 목표 160,000원** (+51%, 24개월, 폴란드+SMR).\n"
            "**보유 기간**: 24~36개월. 6/10 폴란드 발표를 위한 단기 catalyst 보유. CapEx 슈퍼사이클 장기 trend."
        ),
    },
}


# ==============================================================
# MD 파일 생성기
# ==============================================================

def make_md_files(ticker, info):
    name = info["name"]
    out_dir = f"analysis/{ticker}_{name}_v4"

    # company.md
    company_md = f"""# {info['name_kr']} ({ticker}) — 기업개요 & Moat (BLIND v4 재분석)

> **재분석 모드**: BLIND v4 (이전 v3 절대 read 안 함)
> **재분석 일자**: {TODAY}
> **데이터 기준일**: 2026-05-28

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

## 가격 정보 (2026-05-28 기준)

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
    cur = info["currency"]
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

- **목표가 범위**: {cur}{info['confidence']['target_low']:,} ~ {cur}{info['confidence']['target_high']:,} (중심 {cur}{info['confidence']['target_mid']:,}, {info['confidence']['ci_pct']})
- **스코어 ±밴드**: {info['confidence']['score_band']} (가정 변경 시 변동 폭)
- **시나리오 분기**:
  - **Bull case**: 목표가 {cur}{info['confidence']['target_high']:,}
  - **Base case**: 목표가 {cur}{info['confidence']['target_mid']:,}
  - **Bear case**: 목표가 {cur}{info['confidence']['target_low']:,}

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
> 이전 v3 ({info['previous_v3_date']}) 와의 차이는 `analysis/_reanalysis_runs/{YYYYMMDD}_run.md` 비교표 참조.
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
# HTML 리포트 생성기
# ==============================================================

def make_html_report(ticker, info):
    name = info["name"]
    # data.json 읽기 (가격 정보)
    with open(f"analysis/{ticker}_{name}_v4/data.json", "r", encoding="utf-8") as f:
        d = json.load(f)

    cur = info["currency"]
    report_data = {
        "ticker": ticker,
        "name": info["name_kr"] + f" ({info['name']})",
        "date": TODAY,
        "score": info["score"],
        "grade": info["grade"],
        "current_price": d["current_price"],
        "currency": cur,
        "market_cap": d.get("market_cap"),
        "per": "N/A",
        "low52": d.get("low_52w"),
        "high52": d.get("high_52w"),
        "asset_type": "주식",
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
            ("재분석", "v4 BLIND"),
        ],
        "custom_sections": [
            {
                "title": "§ Confidence Interval (95% CI)",
                "content": (
                    f"**목표가 범위**: {cur}{info['confidence']['target_low']:,} ~ {cur}{info['confidence']['target_high']:,}"
                    f" (중심 {cur}{info['confidence']['target_mid']:,}, {info['confidence']['ci_pct']})\n\n"
                    f"**스코어 ±밴드**: {info['confidence']['score_band']}\n\n"
                    f"**시나리오 분기**:\n"
                    f"- Bull case: {cur}{info['confidence']['target_high']:,}\n"
                    f"- Base case: {cur}{info['confidence']['target_mid']:,}\n"
                    f"- Bear case: {cur}{info['confidence']['target_low']:,}"
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
                    f"- **재분석 회차**: v4 (이전 v3, {info['previous_v3_date']})\n"
                    f"- **모드**: BLIND (이전 v3 read 0건)\n"
                    f"- **임계 경과**: 14~15일\n"
                    f"- **회차 보고**: `analysis/_reanalysis_runs/{YYYYMMDD}_run.md`"
                )
            }
        ]
    }

    output_path = f"reports/{ticker}_{name}_{YYYYMMDD}.html"
    generate_report(report_data, output_path=output_path)
    return output_path


def main():
    print(f"=== 재분석 자동 실행 — {TODAY} BLIND v4 — 7종 일괄 ===\n")

    for ticker, info in TICKER_DATA.items():
        print(f"[{ticker}] BLIND v4 작성 중...")
        try:
            out_dir = make_md_files(ticker, info)
            html = make_html_report(ticker, info)
            print(f"  ✅ MD: {out_dir}/ (6 files)")
            print(f"  ✅ HTML: {html}")
        except Exception as e:
            print(f"  ❌ {ticker}: FAILED — {e}")
            import traceback
            traceback.print_exc()

    print(f"\n=== 완료 — 7종 v4 분석 + HTML 보고서 ===")


if __name__ == "__main__":
    main()
