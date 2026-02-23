"""Normalize line endings for CRCBAC_code Python files.

Some files in the repo appear to use CR-only (\r) line endings, which can make them look like a
single line in some tools and may cause syntax errors depending on how they're copied.

Usage:
  python fix_newlines.py /path/to/CRCBAC_code/CRBAC_GRT_dataset_code_result/CODE
"""

from __future__ import annotations

import sys
from pathlib import Path


def normalize_file(p: Path) -> None:
    data = p.read_bytes()
    # First turn CRLF into LF, then CR into LF.
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    p.write_bytes(data)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python fix_newlines.py <CODE_DIR>")
        return 2

    code_dir = Path(sys.argv[1]).expanduser().resolve()
    if not code_dir.exists() or not code_dir.is_dir():
        print(f"Directory not found: {code_dir}")
        return 2

    py_files = sorted(code_dir.glob("*.py"))
    if not py_files:
        print(f"No .py files found in {code_dir}")
        return 1

    for p in py_files:
        normalize_file(p)
        print(f"OK: normalized {p.name}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
