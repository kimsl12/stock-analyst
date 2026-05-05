#!/usr/bin/env python3
"""
sync_portfolio_to_supabase.py — 사용자 포트폴리오 로컬 md → Supabase 동기화

PLAN.md §3, §7.1 기반.
SSoT는 항상 로컬 knowledge-base/portfolio/user_portfolio.md.
Supabase는 웹(read-only) 미러.

설치:
    pip install -r scripts/requirements.txt
    # 또는: pip install supabase python-dotenv

사용법:
    python scripts/sync_portfolio_to_supabase.py
    python scripts/sync_portfolio_to_supabase.py --dry-run    # 파싱 결과만 stdout 출력

환경변수 (web/.env.local 자동 로드):
    PUBLIC_SUPABASE_URL          (필수)
    SUPABASE_SERVICE_KEY         (필수, RLS 우회 키)
    ALLOWED_EMAIL                (필수, 사용자 이메일)

종료 코드:
    0: 성공 또는 graceful skip (환경변수 미설정/SDK 미설치)
    1: 실패 (파싱 오류, Supabase 호출 실패 등)

briefing-lead `/내포트폴리오` Phase 4-후 자동 호출. 실패해도 briefing 결과는 영향 없음.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# 경로 상수
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PORTFOLIO_MD = PROJECT_ROOT / "knowledge-base" / "portfolio" / "user_portfolio.md"
ENV_LOCAL = PROJECT_ROOT / "web" / ".env.local"


# ---------------------------------------------------------------------------
# 환경 로드 (graceful)
# ---------------------------------------------------------------------------
def load_env() -> None:
    """web/.env.local 우선, 없으면 OS 환경변수 그대로 사용."""
    try:
        from dotenv import load_dotenv  # type: ignore
    except ImportError:
        return  # OS 환경변수만 사용
    if ENV_LOCAL.exists():
        load_dotenv(ENV_LOCAL, override=False)


def warn(msg: str) -> None:
    print(f"WARN: {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(msg)


# ---------------------------------------------------------------------------
# 마크다운 표 파서
# ---------------------------------------------------------------------------
TABLE_LINE = re.compile(r"^\s*\|(.+)\|\s*$")
SEP_LINE = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")


def split_row(line: str) -> list[str]:
    """`| a | b | c |` → ['a', 'b', 'c']. 양 끝 빈 토큰 제거."""
    inner = line.strip().strip("|")
    return [c.strip() for c in inner.split("|")]


def find_table(lines: list[str], start: int) -> tuple[list[str], list[list[str]], int] | None:
    """start 이후 첫 번째 마크다운 표를 찾아 (header, rows, end_idx) 반환."""
    i = start
    n = len(lines)
    while i < n - 1:
        if TABLE_LINE.match(lines[i]) and SEP_LINE.match(lines[i + 1]):
            header = split_row(lines[i])
            rows: list[list[str]] = []
            j = i + 2
            while j < n and TABLE_LINE.match(lines[j]) and not SEP_LINE.match(lines[j]):
                rows.append(split_row(lines[j]))
                j += 1
            return header, rows, j
        i += 1
    return None


def find_table_after_heading(lines: list[str], heading_re: re.Pattern[str]) -> tuple[list[str], list[list[str]]] | None:
    for i, line in enumerate(lines):
        if heading_re.match(line):
            res = find_table(lines, i + 1)
            if res:
                header, rows, _ = res
                return header, rows
    return None


# ---------------------------------------------------------------------------
# 값 정규화
# ---------------------------------------------------------------------------
def _strip_md(s: str) -> str:
    """마크다운 굵은체(**) 제거 + 양 끝 공백 제거."""
    return s.replace("**", "").strip()


def clean_money(s: str) -> float | None:
    """'$15,987.16' / '**$17,484.47**' → 15987.16, '—' → None."""
    if not s or _strip_md(s) in ("—", "-", ""):
        return None
    cleaned = _strip_md(s).replace("$", "").replace(",", "").replace("원", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def clean_qty(s: str) -> float | None:
    """'24.469743주' → 24.469743, '—' → None."""
    if not s or _strip_md(s) in ("—", "-", ""):
        return None
    cleaned = _strip_md(s).replace("주", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def clean_pct(s: str) -> float | None:
    """'+7.4%' → 7.4, '-0.4%' → -0.4, '—' → None."""
    if not s or _strip_md(s) in ("—", "-", ""):
        return None
    cleaned = _strip_md(s).replace("%", "").replace("+", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# user_portfolio.md 파싱
# ---------------------------------------------------------------------------
def extract_current_section(md_text: str) -> str:
    """## ★ CURRENT ★ 부터 다음 ## 헤딩 직전까지."""
    m = re.search(
        r"^##\s*★\s*CURRENT\s*★\s*$(.*?)(?=^---\s*$|^##\s+\S)",
        md_text,
        re.DOTALL | re.MULTILINE,
    )
    if not m:
        raise ValueError("★ CURRENT ★ 섹션을 찾을 수 없음")
    return m.group(1)


def parse_profile(section_lines: list[str]) -> dict[str, Any]:
    res = find_table_after_heading(section_lines, re.compile(r"^###\s+투자자\s*프로파일"))
    if not res:
        raise ValueError("투자자 프로파일 표 미발견")
    header, rows = res
    profile: dict[str, str] = {}
    for row in rows:
        if len(row) < 2:
            continue
        key = row[0].strip()
        val = row[1].strip().replace("**", "").strip()
        if key:
            profile[key] = val
    return profile


def parse_holdings(section_lines: list[str]) -> list[dict[str, Any]]:
    res = find_table_after_heading(
        section_lines, re.compile(r"^###\s+보유\s*종목")
    )
    if not res:
        raise ValueError("보유 종목 표 미발견")
    header, rows = res
    out: list[dict[str, Any]] = []
    for row in rows:
        if len(row) < 8:
            # 표 형식이 예상과 다름 — 스킵 (graceful)
            continue
        ticker, name, asset_type, market, qty, value_usd, weight, ret = (
            c.strip() for c in row[:8]
        )
        if not ticker or ticker.startswith("---"):
            continue
        # cash 행 처리: ticker '달러현금' / 유형 '현금'
        is_cash = "현금" in asset_type or "현금" in ticker
        norm_type = (
            "CASH" if is_cash
            else asset_type.upper() if asset_type and asset_type != "—"
            else None
        )
        norm_market = market if market and market != "—" else None
        qty_val = clean_qty(qty) or (0.0 if is_cash else None)
        value_val = clean_money(value_usd)
        weight_val = clean_pct(weight)
        ret_val = clean_pct(ret)
        # current_price 추정: 평가금/수량 (cash 제외)
        current_price = (
            value_val / qty_val
            if (qty_val and qty_val > 0 and value_val is not None)
            else None
        )
        if qty_val is None:
            # NOT NULL 제약 — 스킵
            continue
        out.append(
            {
                "ticker": ticker,
                "name": name or ticker,
                "asset_type": norm_type,
                "market": norm_market,
                "quantity": qty_val,
                "avg_buy_price": None,  # md에 없음
                "current_price": current_price,
                "current_value_usd": value_val,
                "weight_pct": weight_val,
                "return_pct": ret_val,
            }
        )
    return out


def parse_totals(section_lines: list[str]) -> dict[str, float | None]:
    """포트폴리오 총액 표에서 총액 USD + 환율 추출."""
    res = find_table_after_heading(section_lines, re.compile(r"^###\s+포트폴리오\s*총액"))
    total_usd: float | None = None
    if res:
        _, rows = res
        for row in rows:
            if len(row) < 2:
                continue
            label = row[0].replace("**", "").strip()
            if "총액" in label:
                total_usd = clean_money(row[1])
                break

    # 환율 라인: "환율 기준: 확인 필요 (2026-04-18, 이전 1,479.80원)"
    fx: float | None = None
    fx_line = next(
        (line for line in section_lines if "환율" in line and "원" in line), None
    )
    if fx_line:
        m = re.search(r"([\d,]+\.\d+)\s*원", fx_line)
        if m:
            fx = clean_money(m.group(1))

    total_krw = total_usd * fx if (total_usd and fx) else None
    return {"total_value_usd": total_usd, "exchange_rate": fx, "total_value_krw": total_krw}


def parse_user_portfolio(md_path: Path) -> dict[str, Any]:
    text = md_path.read_text(encoding="utf-8")
    current = extract_current_section(text)
    section_lines = current.splitlines()
    return {
        "profile": parse_profile(section_lines),
        "holdings": parse_holdings(section_lines),
        **parse_totals(section_lines),
    }


# ---------------------------------------------------------------------------
# Supabase upsert (idempotent)
# ---------------------------------------------------------------------------
def get_user_id(sb: Any, email: str) -> str | None:
    """auth.admin.list_users로 이메일 매치."""
    try:
        users = sb.auth.admin.list_users()
    except Exception as e:  # pragma: no cover - SDK 버전 차이
        warn(f"auth.admin.list_users 실패: {e}")
        return None
    # supabase-py v2: list of User 객체. v1: dict. 둘 다 호환.
    for u in users:
        u_email = getattr(u, "email", None) or (u.get("email") if isinstance(u, dict) else None)
        if u_email and u_email.lower() == email.lower():
            return getattr(u, "id", None) or (u.get("id") if isinstance(u, dict) else None)
    return None


def upsert_portfolio(sb: Any, user_id: str, parsed: dict[str, Any]) -> tuple[str, int]:
    """포트폴리오 + 보유 종목을 idempotent하게 upsert. (portfolio_id, holdings_count) 반환."""
    # KST = UTC+9 (한국 시간). Supabase timestamptz는 +09:00 인식.
    KST = timezone(timedelta(hours=9), name="KST")
    now_iso = datetime.now(KST).isoformat(timespec="seconds")
    portfolio_payload = {
        "user_id": user_id,
        "profile": parsed["profile"],
        "total_value_usd": parsed["total_value_usd"],
        "total_value_krw": parsed["total_value_krw"],
        "exchange_rate": parsed["exchange_rate"],
        "updated_at": now_iso,
        "source": "local_md",
    }

    # 기존 portfolio 조회
    existing = (
        sb.table("portfolios")
        .select("id")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )
    if existing.data:
        portfolio_id = existing.data[0]["id"]
        sb.table("portfolios").update(portfolio_payload).eq("id", portfolio_id).execute()
    else:
        res = sb.table("portfolios").insert(portfolio_payload).execute()
        if not res.data:
            raise RuntimeError("portfolios insert 결과가 비어있음")
        portfolio_id = res.data[0]["id"]

    # holdings 전량 삭제 → 재삽입 (transactional approximation)
    sb.table("holdings").delete().eq("portfolio_id", portfolio_id).execute()
    holdings_payload = [
        {**h, "portfolio_id": portfolio_id, "updated_at": now_iso}
        for h in parsed["holdings"]
    ]
    if holdings_payload:
        sb.table("holdings").insert(holdings_payload).execute()
    return portfolio_id, len(holdings_payload)


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------
def main() -> int:
    dry_run = "--dry-run" in sys.argv

    if not PORTFOLIO_MD.exists():
        warn(f"user_portfolio.md 없음: {PORTFOLIO_MD}")
        return 0  # graceful

    try:
        parsed = parse_user_portfolio(PORTFOLIO_MD)
    except Exception as e:
        warn(f"파싱 실패: {e}")
        return 1

    if dry_run:
        # 보안: holdings/profile은 stdout 가능 (개인 데이터 노출은 로컬 터미널 한정)
        info(json.dumps(parsed, ensure_ascii=False, indent=2, default=str))
        return 0

    load_env()
    url = os.environ.get("PUBLIC_SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    email = os.environ.get("ALLOWED_EMAIL")
    if not (url and key and email):
        warn(
            "Supabase 환경변수 미설정 (PUBLIC_SUPABASE_URL/SUPABASE_SERVICE_KEY/ALLOWED_EMAIL) — sync 스킵"
        )
        return 0  # graceful

    try:
        from supabase import create_client  # type: ignore
    except ImportError:
        warn("supabase-py 미설치 — sync 스킵 (`pip install supabase` 후 재시도)")
        return 0  # graceful

    try:
        sb = create_client(url, key)
        user_id = get_user_id(sb, email)
        if not user_id:
            warn(f"Supabase에 사용자({email}) 미등록 — Authentication → Users 확인 필요")
            return 1
        portfolio_id, n_holdings = upsert_portfolio(sb, user_id, parsed)
    except Exception as e:
        warn(f"Supabase 호출 실패: {e}")
        return 1

    info(f"OK: portfolio synced (id={portfolio_id}, {n_holdings} holdings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
