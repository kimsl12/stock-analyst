#!/usr/bin/env python3
"""
사용자 입수 PDF → reports/analyst/items/{id}/ 항목 생성.

워크플로 (Claude Code 안에서):
  1. 사용자가 reports/analyst/incoming/foo.pdf 드롭
  2. Claude 가 Read 툴로 PDF 직접 읽고 메타데이터 (item_id 포함) 추론
  3. Claude 가 items/{id}/meta.json 을 Write 툴로 작성
  4. 본 스크립트 호출:
       python3 scripts/process_analyst_pdf.py \\
           --pdf reports/analyst/incoming/foo.pdf \\
           --item-id 20260507_GS_NVDA_Note
     → PDF 를 items/{id}/source.pdf 로 이동 + summary.html 렌더 + index 갱신

옵션 --dump: PDF 텍스트만 출력 (메타 작성 참고용, 파일 이동 X).

옵션 --no-pdf-required: 메타만 생성 (PDF 본문은 추후 첨부).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyst_lib import (
    ANALYST_DIR,
    ITEMS_DIR,
    install_pdf_into_item,
    make_item_dir,
    render_summary_html,
    write_meta,
)


def extract_text(pdf_path: Path, max_pages: int | None = None) -> str:
    import pdfplumber

    out: list[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            if max_pages is not None and i >= max_pages:
                break
            text = page.extract_text() or ""
            out.append(f"\n=== Page {i + 1} ===\n{text}")
    return "\n".join(out)


def cmd_dump(args: argparse.Namespace) -> int:
    pdf = Path(args.pdf)
    if not pdf.exists():
        print(f"[err] PDF not found: {pdf}", file=sys.stderr)
        return 2
    print(extract_text(pdf, max_pages=args.max_pages))
    return 0


def cmd_commit(args: argparse.Namespace) -> int:
    item_id: str = args.item_id
    pdf_arg = Path(args.pdf) if args.pdf else None
    item_dir = ITEMS_DIR / item_id
    if not item_dir.exists():
        print(f"[err] item dir missing: {item_dir} (먼저 meta.json 을 작성해야 합니다)", file=sys.stderr)
        return 2

    meta_path = item_dir / "meta.json"
    if not meta_path.exists():
        print(f"[err] meta.json missing: {meta_path}", file=sys.stderr)
        return 2

    with meta_path.open(encoding="utf-8") as f:
        meta = json.load(f)

    if pdf_arg and pdf_arg.exists():
        install_pdf_into_item(pdf_arg, item_dir)
        meta["has_pdf"] = True
    elif (item_dir / "source.pdf").exists():
        meta["has_pdf"] = True
    else:
        meta.setdefault("has_pdf", False)

    write_meta(item_dir, meta)
    render_summary_html(item_dir, meta)

    # 인덱스 갱신
    import subprocess

    repo = ANALYST_DIR.parent.parent
    subprocess.run(
        [sys.executable, str(repo / "scripts" / "build_analyst_index.py")],
        check=True,
    )

    print(f"[ok] committed item: {item_id}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyst PDF processor")
    sub = ap.add_subparsers(dest="cmd", required=False)

    p_dump = sub.add_parser("dump", help="PDF 텍스트만 출력")
    p_dump.add_argument("pdf")
    p_dump.add_argument("--max-pages", type=int, default=None)
    p_dump.set_defaults(func=cmd_dump)

    p_commit = sub.add_parser("commit", help="meta.json + PDF 로 항목 확정")
    p_commit.add_argument("--item-id", required=True)
    p_commit.add_argument("--pdf", default=None)
    p_commit.set_defaults(func=cmd_commit)

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
