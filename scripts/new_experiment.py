#!/usr/bin/env python3
"""Create a new experiment note from template."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "experiments" / "_template.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new experiment entry")
    parser.add_argument("experiment_id", help="e.g. 2026-W34-cub200-aug-ablation")
    parser.add_argument("--week", required=True, help="Week id, e.g. 2026-W34")
    parser.add_argument("--project", default="", help="Project id")
    parser.add_argument("--dataset", default="", help="Dataset id")
    args = parser.parse_args()

    exp_dir = ROOT / "experiments" / args.experiment_id
    readme = exp_dir / "README.md"
    plots_dir = exp_dir / "plots"

    if readme.exists():
        print(f"Exists: {readme}")
        return 0

    content = TEMPLATE.read_text(encoding="utf-8")
    content = content.replace("YYYY-Www-project-short-purpose", args.experiment_id)
    content = content.replace("YYYY-Www", args.week, 1)
    content = content.replace("week: YYYY-Www", f"week: {args.week}")
    content = content.replace("project:\n", f"project: {args.project}\n")
    content = content.replace("dataset:\n", f"dataset: {args.dataset}\n")

    exp_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    readme.write_text(content, encoding="utf-8")
    print(f"Created: {readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
