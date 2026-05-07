#!/usr/bin/env python3
"""
자동 스크랩 결과 → reports/analyst/items/{id}/ 항목 생성 헬퍼.

워크플로 (analyst-scraper 에이전트가 호출):
  1. 에이전트가 WebSearch/WebFetch 로 IB 공식·미디어·한국 증권사·YouTube 수집
  2. 에이전트가 각 항목별로:
       a) items/{id}/meta.json 을 Write 로 작성
       b) (텍스트 본문 있으면) items/{id}/source.html 을 Write 로 작성
       c) (한국 증권사 PDF 등) URL 다운로드 필요 시 본 스크립트의 download-pdf 호출
       d) commit 호출 → summary.html + 인덱스 갱신

서브커맨드:
  download-pdf  URL → items/{id}/source.pdf 다운로드
  commit        meta.json + 본문 자료로 summary.html + 인덱스 갱신
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyst_lib import ANALYST_DIR, ITEMS_DIR, render_summary_html, write_meta


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"


def cmd_download_pdf(args: argparse.Namespace) -> int:
    item_dir = ITEMS_DIR / args.item_id
    if not item_dir.exists():
        item_dir.mkdir(parents=True, exist_ok=True)

    target = item_dir / "source.pdf"
    req = urllib.request.Request(args.url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
    except Exception as exc:
        print(f"[err] PDF download failed ({args.url}): {exc}", file=sys.stderr)
        return 2
    if len(data) < 1024:
        print(f"[warn] PDF too small ({len(data)} bytes) — likely error page", file=sys.stderr)
    target.write_bytes(data)
    print(f"[ok] downloaded {len(data)} bytes → {target}")
    return 0


def cmd_commit(args: argparse.Namespace) -> int:
    item_dir = ITEMS_DIR / args.item_id
    meta_path = item_dir / "meta.json"
    if not meta_path.exists():
        print(f"[err] meta.json missing: {meta_path}", file=sys.stderr)
        return 2

    with meta_path.open(encoding="utf-8") as f:
        meta = json.load(f)

    # has_pdf / has_full_html 자동 갱신 (실제 파일 존재로 판정)
    meta["has_pdf"] = (item_dir / "source.pdf").exists()
    meta["has_full_html"] = (item_dir / "source.html").exists()

    write_meta(item_dir, meta)
    render_summary_html(item_dir, meta)

    import subprocess

    repo = ANALYST_DIR.parent.parent
    subprocess.run(
        [sys.executable, str(repo / "scripts" / "build_analyst_index.py")],
        check=True,
    )

    print(f"[ok] committed: {args.item_id} (pdf={meta['has_pdf']}, html={meta['has_full_html']})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyst web-scrape commit helper")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_dl = sub.add_parser("download-pdf", help="URL → items/{id}/source.pdf")
    p_dl.add_argument("--item-id", required=True)
    p_dl.add_argument("--url", required=True)
    p_dl.set_defaults(func=cmd_download_pdf)

    p_commit = sub.add_parser("commit", help="summary.html + 인덱스 갱신")
    p_commit.add_argument("--item-id", required=True)
    p_commit.set_defaults(func=cmd_commit)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
