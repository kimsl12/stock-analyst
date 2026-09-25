#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재분석 v{N} _report_data.json 정규화·검증 — 2026-09-26 (/재분석실행 7 20->cap10, stock_update-2 슬롯).
스키마 드리프트 방어: 에이전트 산출 _report_data.json 을 렌더 직전 멱등 정규화.
  - score: 문자열/실수 → 정수, scorecard.md `**종합 점수: N / 100**` 과 교차검증(불일치 시 scorecard 우선)
  - target_price: "$40"/"40" → 숫자
  - scorecard_items: [["라벨",숫자],...] 10개 보장
  - risks: list[dict{name,level,impact,desc}] 보장
  - thesis: dict 보장, custom_sections: list 보장
  - current_price/atr/stop_loss/low52/high52/market_cap: data.json 실측으로 강제 동기화(에이전트 오타 방어)
출력: 각 폴더 _report_data.json 덮어쓰기(정규화) + 검증 리포트 stdout.
"""
import json, os, re, sys

ROOT = "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
# ticker -> (folder(name만), next_v)
PLAN = {
    "005930": ("삼성전자",        17),
    "207940": ("삼성바이오로직스",  10),
    "329180": ("HD현대중공업",     18),
    "AAPL":   ("Apple",          10),
    "ABBV":   ("AbbVie",         16),
    "AMD":    ("AMD",            10),
    "AMZN":   ("Amazon",         17),
    "C":      ("Citigroup",      17),
    "CAT":    ("Caterpillar",    17),
    "HOOD":   ("Robinhood",      17),
}
STD_ITEMS = ["성장성","수익성","재무건전성","밸류에이션","해자/경쟁력",
             "모멘텀/수급","산업매력도","리스크","ESG/지배구조","촉매/이벤트"]


def to_num(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return x
    s = str(x)
    m = re.search(r"-?[0-9][0-9,]*\.?[0-9]*", s.replace(",", ""))
    if not m:
        return None
    v = float(m.group().replace(",", ""))
    return int(v) if v == int(v) else v


def parse_scorecard_score(md_path):
    """scorecard.md 의 `**종합 점수: N / 100**` 정수 추출 (파서 호환 형식)."""
    if not os.path.exists(md_path):
        return None
    txt = open(md_path, encoding="utf-8").read()
    m = re.search(r"종합\s*점수[^0-9\-]*([0-9]+)\s*/\s*100", txt)
    return int(m.group(1)) if m else None


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else list(PLAN.keys())
    issues = []
    for tk in only:
        folder, nv = PLAN[tk]
        d = f"{ROOT}/analysis/{tk}_{folder}_v{nv}"
        rp = f"{d}/_report_data.json"
        sc = f"{d}/scorecard.md"
        dj = f"{d}/data.json"
        if not os.path.exists(rp):
            issues.append(f"❌ {tk}: _report_data.json 없음"); continue
        try:
            data = json.load(open(rp, encoding="utf-8"))
        except Exception as e:
            issues.append(f"❌ {tk}: JSON 파싱 실패 {e}"); continue

        dat = json.load(open(dj, encoding="utf-8")) if os.path.exists(dj) else {}
        q = dat.get("quote", {})

        # score 교차검증
        sc_score = parse_scorecard_score(sc)
        rd_score = to_num(data.get("score"))
        if sc_score is not None:
            if rd_score != sc_score:
                issues.append(f"⚠️ {tk}: score 불일치 scorecard={sc_score} rd={rd_score} → scorecard 우선 적용")
            data["score"] = sc_score
        elif rd_score is not None:
            data["score"] = int(rd_score)
            issues.append(f"⚠️ {tk}: scorecard.md 종합점수 파싱 실패 → rd score {rd_score} 사용 (형식 점검 필요)")
        else:
            issues.append(f"❌ {tk}: score 없음")

        # target_price 숫자화
        data["target_price"] = to_num(data.get("target_price"))
        if data["target_price"] is None:
            issues.append(f"⚠️ {tk}: target_price 파싱 실패")

        # 실측값 강제 동기화 (에이전트 오타 방어)
        sync = {
            "current_price": q.get("current_price"),
            "market_cap": q.get("marketCap"),
            "low52": q.get("fiftyTwoWeekLow"),
            "high52": q.get("fiftyTwoWeekHigh"),
            "atr": q.get("atr_14"),
            "stop_loss": q.get("stop_loss_2atr"),
        }
        for k, v in sync.items():
            if v is not None:
                old = data.get(k)
                if to_num(old) != to_num(v):
                    issues.append(f"ℹ️ {tk}: {k} {old}→{v} (data.json 실측 동기화)")
                data[k] = v

        # scorecard_items 정규화
        items = data.get("scorecard_items")
        norm_items = []
        if isinstance(items, list):
            for it in items:
                if isinstance(it, (list, tuple)) and len(it) >= 2:
                    norm_items.append([str(it[0]), to_num(it[1])])
                elif isinstance(it, dict):
                    norm_items.append([str(it.get("name", it.get("label", "?"))), to_num(it.get("score", it.get("value")))])
        if len(norm_items) != 10:
            issues.append(f"⚠️ {tk}: scorecard_items {len(norm_items)}개 (10 기대)")
        data["scorecard_items"] = norm_items if norm_items else [[l, None] for l in STD_ITEMS]

        # risks 정규화
        risks = data.get("risks")
        nr = []
        if isinstance(risks, list):
            for r in risks:
                if isinstance(r, dict):
                    nr.append({
                        "name": str(r.get("name", r.get("title", ""))),
                        "level": str(r.get("level", "중간")),
                        "impact": str(r.get("impact", r.get("effect", "중"))),
                        "desc": str(r.get("desc", r.get("detail", r.get("description", "")))),
                    })
                elif isinstance(r, str):
                    nr.append({"name": r, "level": "중간", "impact": "중", "desc": ""})
        data["risks"] = nr
        if not nr:
            issues.append(f"⚠️ {tk}: risks 비어있음")

        # thesis / custom_sections 타입 보장
        if not isinstance(data.get("thesis"), dict):
            issues.append(f"⚠️ {tk}: thesis dict 아님 → 빈 dict")
            data["thesis"] = {}
        if not isinstance(data.get("custom_sections"), list):
            issues.append(f"⚠️ {tk}: custom_sections list 아님 → []")
            data["custom_sections"] = []

        # 필수 문자열 필드 기본값
        for k in ["ticker","name","date","asset_type","currency","grade","per",
                  "executive_summary","company_overview","moat_rating","moat_details",
                  "financial_analysis","valuation","momentum","business_analysis",
                  "risk_summary","strategy"]:
            if data.get(k) is None:
                data[k] = ""
        if not data.get("date"):
            data["date"] = "2026-09-26"
        if not data.get("currency"):
            data["currency"] = "$"

        json.dump(data, open(rp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[{tk}] OK v{nv} score={data['score']} grade={data.get('grade')} tp={data.get('target_price')} "
              f"items={len(data['scorecard_items'])} risks={len(data['risks'])} cs={len(data['custom_sections'])}")

    print("\n=== 검증 이슈 ===")
    if issues:
        for i in issues:
            print(" ", i)
    else:
        print("  (없음 — 전종목 정상)")


if __name__ == "__main__":
    main()
