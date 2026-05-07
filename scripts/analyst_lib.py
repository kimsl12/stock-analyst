"""
Analyst Reports 공통 라이브러리.

- 메타 스키마 검증
- items/{id}/ 폴더 생성
- summary.html 렌더링
- source.html (자동 스크랩 원문) 렌더링

PDF 처리(process_analyst_pdf.py) 와 웹 스크랩(scrape_analyst_web.py) 양쪽이 사용.
"""
from __future__ import annotations

import html
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parent.parent
ANALYST_DIR = REPO / "reports" / "analyst"
ITEMS_DIR = ANALYST_DIR / "items"
INCOMING_DIR = ANALYST_DIR / "incoming"

REQUIRED_META_FIELDS = ("item_id", "source", "date", "target", "title")

ALLOWED_SOURCE_TYPES = {
    "ib_official",
    "media",
    "korea_brokerage",
    "youtube",
    "user_upload",
}
ALLOWED_LICENSE = {
    "user_upload",
    "public_official",
    "media_quote_only",
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(s: str) -> str:
    """Convert 임의 문자열 to ASCII safe slug for item_id."""
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s or "Unknown"


def make_item_id(date: str, source: str, target: str, slug: str | None = None) -> str:
    """date YYYY-MM-DD, source/target/slug 영문화. 결과: YYYYMMDD_Source_Target[_Slug]"""
    d = date.replace("-", "")
    parts = [d, slugify(source), slugify(target)]
    if slug:
        parts.append(slugify(slug))
    return "_".join(parts)


def validate_meta(meta: dict) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_META_FIELDS:
        if not meta.get(field):
            errors.append(f"missing field: {field}")
    st = meta.get("source_type")
    if st and st not in ALLOWED_SOURCE_TYPES:
        errors.append(f"invalid source_type: {st}")
    lic = meta.get("license_note")
    if lic and lic not in ALLOWED_LICENSE:
        errors.append(f"invalid license_note: {lic}")
    return errors


def make_item_dir(item_id: str) -> Path:
    item_dir = ITEMS_DIR / item_id
    item_dir.mkdir(parents=True, exist_ok=True)
    return item_dir


def write_meta(item_dir: Path, meta: dict) -> None:
    meta.setdefault("collected_at", now_iso())
    errors = validate_meta(meta)
    if errors:
        raise ValueError(f"meta validation failed: {errors}")
    (item_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ───────── HTML 렌더링 ─────────

_SUMMARY_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — {source_full}</title>
<style>
:root{{--bg:#0F1923;--card:#1A2733;--text:#E8EAED;--sub:#9AA0A6;--blue:#42A5F5;--buy:#26A69A;--sell:#EF5350;--hold:#FFA726;--border:#2D3A45;--accent:#7C4DFF;--ai:#FFB74D}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:24px;max-width:880px;margin:0 auto;line-height:1.55}}
.back{{display:inline-block;color:var(--blue);font-size:13px;margin-bottom:12px;text-decoration:none}}
.back:hover{{text-decoration:underline}}
header{{border-bottom:1px solid var(--border);padding-bottom:16px;margin-bottom:20px}}
.tag{{display:inline-block;background:var(--card);border:1px solid var(--border);padding:3px 10px;border-radius:12px;font-size:11px;color:var(--sub);margin-right:6px}}
.tag.src{{color:var(--blue);border-color:rgba(66,165,245,0.4)}}
.tag.date{{color:var(--sub)}}
h1{{font-size:22px;margin:10px 0 6px;line-height:1.3}}
.target{{font-size:15px;color:var(--sub)}}
.target b{{color:var(--text);font-size:16px}}
.target .code{{color:var(--sub);font-size:12px;margin-left:4px;font-family:ui-monospace,Menlo,monospace}}
.priceline{{margin-top:10px;display:flex;flex-wrap:wrap;gap:14px;font-size:13px}}
.priceline .item{{background:var(--card);border:1px solid var(--border);padding:6px 12px;border-radius:6px}}
.priceline .item .lbl{{color:var(--sub);font-size:11px;display:block}}
.rating{{font-size:12px;padding:2px 10px;border-radius:10px;background:#2D3A45}}
.rating.buy{{background:rgba(38,166,154,0.2);color:var(--buy)}}
.rating.sell{{background:rgba(239,83,80,0.2);color:var(--sell)}}
.rating.hold{{background:rgba(255,167,38,0.2);color:var(--hold)}}
section{{margin-bottom:24px}}
h2{{font-size:15px;color:var(--blue);margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid var(--border)}}
ul{{padding-left:20px}}
ul li{{margin-bottom:8px;font-size:14px}}
.bullets li::marker{{color:var(--blue)}}
/* 사후 평가 섹션 */
.oc-block{{background:rgba(66,165,245,0.04);border:1px solid var(--border);border-left:3px solid var(--blue);padding:14px 18px;border-radius:6px;margin-bottom:24px}}
.oc-block h2{{color:var(--blue);border-bottom:none;padding-bottom:0;margin-bottom:12px;display:flex;align-items:center;gap:6px;font-size:15px}}
.oc-row{{display:flex;align-items:center;gap:10px;margin-bottom:8px;font-size:14px;flex-wrap:wrap}}
.oc-label{{display:inline-block;color:var(--sub);font-size:12.5px;min-width:140px}}
.oc-badge{{display:inline-block;padding:2px 12px;border-radius:10px;font-size:12px;font-weight:700}}
.oc-badge.hit{{background:rgba(38,166,154,0.22);color:var(--buy)}}
.oc-badge.miss{{background:rgba(239,83,80,0.22);color:var(--sell)}}
.oc-badge.progress{{background:rgba(255,167,38,0.22);color:var(--hold)}}
.oc-thesis{{font-size:12px;padding:2px 9px;border-radius:9px;background:#2D3A45;color:var(--sub)}}
.oc-thesis.thesis-correct{{background:rgba(38,166,154,0.16);color:var(--buy)}}
.oc-thesis.thesis-partial{{background:rgba(255,167,38,0.16);color:var(--hold)}}
.oc-thesis.thesis-incorrect{{background:rgba(239,83,80,0.16);color:var(--sell)}}
.oc-notes{{margin-top:10px;padding-top:10px;border-top:1px dashed var(--border);font-size:13px;line-height:1.6;color:var(--text)}}
/* AI 해석 섹션 */
.ai-block{{background:linear-gradient(135deg,rgba(255,183,77,0.06),rgba(124,77,255,0.04));border:1px solid var(--border);border-left:3px solid var(--ai);padding:14px 18px;border-radius:6px;margin-bottom:24px}}
.ai-block h2{{color:var(--ai);border-bottom:none;padding-bottom:0;margin-bottom:12px;display:flex;align-items:center;gap:6px}}
.ai-block h2::before{{content:"🤖";font-size:16px}}
.ai-block .ai-row{{margin-bottom:10px;font-size:14px;line-height:1.6}}
.ai-block .ai-row:last-child{{margin-bottom:0}}
.ai-block .ai-label{{display:inline-block;font-weight:700;color:var(--text);min-width:88px;padding-right:8px;font-size:13px}}
.ai-block .ai-row.context .ai-label{{color:var(--blue)}}
.ai-block .ai-row.agreement .ai-label{{color:var(--buy)}}
.ai-block .ai-row.divergence .ai-label{{color:var(--hold)}}
.ai-block .ai-row.insight{{padding-top:10px;margin-top:10px;border-top:1px dashed var(--border);font-style:italic;color:var(--text)}}
.ai-block .ai-row.insight .ai-label{{color:var(--ai);font-style:normal}}
.ai-disclaimer{{font-size:11px;color:var(--sub);margin-top:10px;padding-top:8px;border-top:1px dashed var(--border)}}
.notice{{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--accent);padding:10px 14px;border-radius:4px;font-size:12px;color:var(--sub);margin:14px 0}}
.notice b{{color:var(--text)}}
.source-link{{display:inline-block;margin-top:6px;font-size:13px;color:var(--blue);text-decoration:none}}
.source-link:hover{{text-decoration:underline}}
.full-link{{display:inline-block;margin-top:8px;background:var(--card);border:1px solid var(--border);padding:8px 14px;border-radius:6px;font-size:13px;color:var(--text);text-decoration:none;transition:border-color 0.2s}}
.full-link:hover{{border-color:var(--blue);color:var(--blue)}}
.pdf-frame{{width:100%;height:75vh;border:1px solid var(--border);border-radius:6px;margin-top:12px;background:#fff}}
footer{{margin-top:30px;padding-top:14px;border-top:1px solid var(--border);font-size:11px;color:var(--sub);font-family:ui-monospace,Menlo,monospace}}
@media(max-width:700px){{body{{padding:12px}}.ai-block .ai-label{{display:block;min-width:auto;margin-bottom:2px}}}}
</style>
</head>
<body>
<a class="back" href="../../index.html">← Analyst Reports 인덱스</a>
<header>
  <div>
    <span class="tag src">{source_full}</span>
    <span class="tag date">{date}</span>
    {analyst_tag}
    {rating_tag}
  </div>
  <h1>{title}</h1>
  <div class="target"><b>{target_name}</b><span class="code">{target_code}</span></div>
  {priceline}
</header>

<section>
  <h2>핵심 메시지</h2>
  <ul class="bullets">
    {bullets_html}
  </ul>
</section>

{outcome_section}

{ai_section}

{original_section}

<div class="notice">
  <b>출처 / 인용 안내:</b> 본 페이지는 {source_full} 의 {date} 자료를 정리한 것입니다.
  원본 저작권은 발행처에 있으며 본 정리는 비영리 개인 학습 / 연구 목적입니다.
  {source_link_html}
</div>

<footer>
  item_id: {item_id} · source_type: {source_type} · license: {license_note} · collected: {collected_at}
</footer>
</body>
</html>
"""


def _bullet_li(text: str) -> str:
    return f"<li>{html.escape(text)}</li>"


def _priceline_block(meta: dict) -> str:
    pieces: list[str] = []
    tp = meta.get("target_price")
    cur = meta.get("target_currency") or ""
    period = meta.get("period")
    if tp is not None:
        pieces.append(
            f'<div class="item"><span class="lbl">목표가</span>{html.escape(str(cur))}{html.escape(str(tp))}</div>'
        )
    prior = meta.get("prior_target_price")
    if prior is not None:
        pieces.append(
            f'<div class="item"><span class="lbl">직전 목표가</span>{html.escape(str(cur))}{html.escape(str(prior))}</div>'
        )
    if period and period != "N/A":
        pieces.append(
            f'<div class="item"><span class="lbl">기간</span>{html.escape(str(period))}</div>'
        )
    if not pieces:
        return ""
    return f'<div class="priceline">{"".join(pieces)}</div>'


# 평가 등급 → 한글 매핑 (표시용. 메타 스키마 보존)
RATING_KO = {
    "Buy": "매수",
    "Strong Buy": "적극 매수",
    "Hold": "보유",
    "Sell": "매도",
    "Strong Sell": "적극 매도",
    "Overweight": "비중확대",
    "Underweight": "비중축소",
    "Equal Weight": "중립",
    "Neutral": "중립",
    "Bullish": "강세",
    "Bearish": "약세",
    "N/A": "평가 없음",
}


def rating_korean(rating: str | None) -> str:
    if not rating:
        return ""
    return RATING_KO.get(rating, rating)


def _outcome_section(meta: dict) -> str:
    """사후 평가 섹션 — meta.outcome 이 있으면 렌더, 없으면 빈 문자열."""
    oc = meta.get("outcome")
    if not oc or not isinstance(oc, dict):
        return ""
    if not oc.get("evaluated_at"):
        return ""

    hit = oc.get("hit")
    if hit is True:
        hit_badge = '<span class="oc-badge hit">적중</span>'
    elif hit is False:
        hit_badge = '<span class="oc-badge miss">미적중</span>'
    else:
        hit_badge = '<span class="oc-badge progress">진행 중</span>'

    thesis = oc.get("thesis_validity", "")
    thesis_label = {
        "logic_chain_correct": "논리 정확",
        "logic_chain_partial": "논리 부분 적중",
        "logic_chain_incorrect": "논리 부정확",
    }.get(thesis, thesis or "—")
    thesis_class = (
        "thesis-correct" if thesis == "logic_chain_correct"
        else "thesis-partial" if thesis == "logic_chain_partial"
        else "thesis-incorrect" if thesis == "logic_chain_incorrect"
        else ""
    )

    actual = oc.get("actual_price")
    actual_str = ""
    cur = meta.get("target_currency") or ""
    if actual is not None:
        actual_str = f"{cur}{actual:,}" if isinstance(actual, (int, float)) else str(actual)
    error = oc.get("error_pct")
    error_str = f"{error:+.2f}%" if isinstance(error, (int, float)) else "—"

    notes = oc.get("notes", "")
    evaluated_at = oc.get("evaluated_at", "")

    rows = [
        f'<div class="oc-row"><span class="oc-label">판정</span>{hit_badge}'
        f'<span class="oc-thesis {thesis_class}">{html.escape(thesis_label)}</span></div>',
    ]
    if actual_str:
        rows.append(
            f'<div class="oc-row"><span class="oc-label">실제 가격 ({html.escape(evaluated_at)})</span>'
            f'<b>{html.escape(actual_str)}</b></div>'
        )
    if isinstance(error, (int, float)):
        rows.append(
            f'<div class="oc-row"><span class="oc-label">목표가 대비 오차</span>'
            f'<b>{html.escape(error_str)}</b></div>'
        )
    if notes:
        rows.append(
            f'<div class="oc-notes">{html.escape(notes)}</div>'
        )

    return (
        '<section class="oc-block">'
        '<h2>📊 사후 평가</h2>'
        + "".join(rows) +
        '</section>'
    )


def _ai_section(meta: dict) -> str:
    """AI 해석 섹션 — meta.ai_assessment 가 있으면 렌더, 없으면 빈 문자열."""
    aa = meta.get("ai_assessment")
    if not aa or not isinstance(aa, dict):
        return ""
    rows: list[str] = []
    if aa.get("context"):
        rows.append(
            f'<div class="ai-row context"><span class="ai-label">시장 컨텍스트</span>'
            f'{html.escape(aa["context"])}</div>'
        )
    if aa.get("agreement"):
        rows.append(
            f'<div class="ai-row agreement"><span class="ai-label">동의 / 타당</span>'
            f'{html.escape(aa["agreement"])}</div>'
        )
    if aa.get("divergence"):
        rows.append(
            f'<div class="ai-row divergence"><span class="ai-label">이견 / 위험</span>'
            f'{html.escape(aa["divergence"])}</div>'
        )
    if aa.get("key_insight"):
        rows.append(
            f'<div class="ai-row insight"><span class="ai-label">핵심 시사점</span>'
            f'{html.escape(aa["key_insight"])}</div>'
        )
    if not rows:
        return ""
    body = "\n".join(rows)
    assessed_at = aa.get("assessed_at", "")
    disclaimer_extra = (
        f' · 평가 시점 {html.escape(assessed_at)}' if assessed_at else ""
    )
    return (
        '<section class="ai-block">'
        '<h2>AI 해석 / 의견</h2>'
        f'{body}'
        '<div class="ai-disclaimer">'
        '※ 이 평가는 분석 에이전트가 KB 매크로/시장 데이터 + 사용자 분석 누적을 참고하여 작성한 것이며, '
        f'원 발행처 의견과 다를 수 있습니다. 투자 판단은 본인 책임{disclaimer_extra}.'
        '</div>'
        '</section>'
    )


def _original_section(item_dir: Path, meta: dict) -> str:
    """원문 섹션 — has_pdf 면 iframe 임베드, has_full_html 이면 링크."""
    blocks: list[str] = []
    if meta.get("has_pdf") and (item_dir / "source.pdf").exists():
        blocks.append(
            '<section><h2>원문</h2>'
            '<a class="full-link" href="source.pdf" target="_blank">PDF 새 탭에서 열기 ↗</a>'
            '<iframe class="pdf-frame" src="source.pdf"></iframe>'
            "</section>"
        )
    if meta.get("has_full_html") and (item_dir / "source.html").exists():
        blocks.append(
            '<section><h2>원문 (스크랩 텍스트)</h2>'
            '<a class="full-link" href="source.html" target="_blank">전체 보기 ↗</a>'
            "</section>"
        )
    return "\n".join(blocks)


def render_summary_html(item_dir: Path, meta: dict) -> None:
    """meta.json + (PDF/full HTML 존재 여부)로 summary.html 작성."""
    bullets = meta.get("summary_bullets") or ["요약이 아직 작성되지 않았습니다."]
    bullets_html = "\n    ".join(_bullet_li(b) for b in bullets)

    rating = meta.get("rating") or ""
    rating_class = ""
    rl = rating.lower()
    if rl in ("buy", "overweight", "strong buy", "bullish"):
        rating_class = "buy"
    elif rl in ("sell", "underweight", "strong sell", "bearish"):
        rating_class = "sell"
    elif rl in ("hold", "equal weight", "neutral"):
        rating_class = "hold"
    rating_ko = rating_korean(rating)
    rating_tag = (
        f'<span class="tag rating {rating_class}">{html.escape(rating_ko)}</span>'
        if rating else ""
    )

    analyst = meta.get("analyst")
    analyst_tag = f'<span class="tag">{html.escape(analyst)}</span>' if analyst else ""

    src_url = meta.get("source_url")
    source_link_html = (
        f'<a class="source-link" href="{html.escape(src_url)}" target="_blank">{html.escape(src_url)}</a>'
        if src_url else ""
    )

    body = _SUMMARY_TEMPLATE.format(
        lang=meta.get("language", "ko"),
        title=html.escape(meta.get("title", meta.get("item_id", ""))),
        source_full=html.escape(meta.get("source_full") or meta.get("source", "")),
        date=html.escape(meta.get("date", "")),
        target_name=html.escape(meta.get("target_name") or meta.get("target", "")),
        target_code=html.escape(meta.get("target", "")),
        analyst_tag=analyst_tag,
        rating_tag=rating_tag,
        priceline=_priceline_block(meta),
        bullets_html=bullets_html,
        outcome_section=_outcome_section(meta),
        ai_section=_ai_section(meta),
        original_section=_original_section(item_dir, meta),
        source_link_html=source_link_html,
        item_id=html.escape(meta.get("item_id", "")),
        source_type=html.escape(meta.get("source_type", "")),
        license_note=html.escape(meta.get("license_note", "")),
        collected_at=html.escape(meta.get("collected_at", "")),
    )
    (item_dir / "summary.html").write_text(body, encoding="utf-8")


# ───────── 헬퍼 ─────────

def install_pdf_into_item(pdf_src: Path, item_dir: Path) -> None:
    target = item_dir / "source.pdf"
    if pdf_src.resolve() == target.resolve():
        return
    shutil.move(str(pdf_src), str(target))


def write_full_html(item_dir: Path, title: str, body_text: str, source_url: str | None = None) -> None:
    """자동 스크랩 원문 텍스트를 보존용 source.html 로 저장."""
    safe_title = html.escape(title)
    src_block = (
        f'<p class="src"><a href="{html.escape(source_url)}" target="_blank">원본 출처: {html.escape(source_url)}</a></p>'
        if source_url else ""
    )
    paragraphs = "\n".join(
        f"<p>{html.escape(p.strip())}</p>"
        for p in body_text.split("\n\n")
        if p.strip()
    )
    page = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>{safe_title}</title>
<style>
body{{background:#0F1923;color:#E8EAED;font-family:-apple-system,sans-serif;padding:24px;max-width:880px;margin:0 auto;line-height:1.7}}
.back{{color:#42A5F5;text-decoration:none;font-size:13px;display:inline-block;margin-bottom:12px}}
h1{{font-size:20px;margin-bottom:8px}}
.src{{color:#9AA0A6;font-size:13px;margin-bottom:16px}}
.src a{{color:#42A5F5}}
p{{margin-bottom:14px}}
</style></head><body>
<a class="back" href="summary.html">← 요약 페이지로</a>
<h1>{safe_title}</h1>
{src_block}
{paragraphs}
</body></html>
"""
    (item_dir / "source.html").write_text(page, encoding="utf-8")


def discover_incoming_pdfs() -> Iterable[Path]:
    if not INCOMING_DIR.exists():
        return []
    return sorted(INCOMING_DIR.glob("*.pdf"))
