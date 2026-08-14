#!/usr/bin/env python3
"""Create a new weekly diary entry from template."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "weeks" / "_template.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new week entry")
    parser.add_argument("week", help="Week id, e.g. 2026-W34")
    args = parser.parse_args()

    target_dir = ROOT / "weeks" / args.week
    target_file = target_dir / "README.md"

    if target_file.exists():
        print(f"Exists: {target_file}")
        return 0

    template_text = TEMPLATE.read_text(encoding="utf-8")
    rendered = template_text.replace("YYYY-Www", args.week)

    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(rendered, encoding="utf-8")
    print(f"Created: {target_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
