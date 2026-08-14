#!/usr/bin/env python3
"""Create a new weekly diary entry from template."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "weeks" / "_template.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new week entry")
    parser.add_argument("year", help="Year, e.g. 2026")
    parser.add_argument("month", help="3-letter uppercase month, e.g. AUG")
    parser.add_argument("week_in_month", type=int, help="Week number in month, e.g. 1")
    args = parser.parse_args()

    target_dir = ROOT / "weeks" / args.year
    file_name = f"{args.month.upper()}_WEEK{args.week_in_month}.md"
    target_file = target_dir / file_name

    if target_file.exists():
        print(f"Exists: {target_file}")
        return 0

    template_text = TEMPLATE.read_text(encoding="utf-8")
    rendered = (
        template_text.replace("{YEAR}", args.year)
        .replace("{MONTH}", args.month.upper())
        .replace("{WEEK_IN_MONTH}", str(args.week_in_month))
    )

    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(rendered, encoding="utf-8")
    print(f"Created: {target_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
