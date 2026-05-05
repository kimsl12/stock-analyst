"""
KST (Asia/Seoul, UTC+9) 시간 헬퍼.

모든 시각 표기는 한국 시간(KST) 기준. utcnow() / timezone.utc 사용 금지.
"""
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9), name="KST")


def now_kst() -> datetime:
    """현재 시각 KST datetime."""
    return datetime.now(KST)


def now_kst_iso() -> str:
    """KST ISO 8601 (예: '2026-05-06T18:30:00+09:00')."""
    return now_kst().isoformat(timespec="seconds")


def today_kst() -> str:
    """KST 기준 오늘 (YYYY-MM-DD)."""
    return now_kst().strftime("%Y-%m-%d")


def today_kst_ymd() -> str:
    """KST 기준 오늘 (YYYYMMDD)."""
    return now_kst().strftime("%Y%m%d")
