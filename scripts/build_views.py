#!/usr/bin/env python3
"""Build lightweight markdown index views from experiment front matter."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = ROOT / "experiments"
VIEWS_DIR = ROOT / "views"

FM_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_front_matter(text: str) -> dict[str, str | list[str]]:
    match = FM_PATTERN.match(text)
    if not match:
        return {}

    data: dict[str, str | list[str]] = {}
    for raw in match.group(1).splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip() for item in value[1:-1].split(",") if item.strip()]
            data[key] = items
        else:
            data[key] = value
    return data


def load_experiments() -> list[dict[str, str | list[str]]]:
    items = []
    for readme in sorted(EXPERIMENTS_DIR.glob("*/README.md")):
        text = readme.read_text(encoding="utf-8")
        meta = parse_front_matter(text)
        if not meta:
            continue
        meta["path"] = f"../{readme.relative_to(ROOT).as_posix()}"
        meta.setdefault("experiment_id", readme.parent.name)
        items.append(meta)
    return items


def write_week_view(experiments: list[dict[str, str | list[str]]]) -> None:
    by_week: dict[str, list[dict[str, str | list[str]]]] = defaultdict(list)
    week_links: dict[str, str] = {}
    for exp in experiments:
        week = str(exp.get("week", "unknown"))
        by_week[week].append(exp)
        weekly_note = exp.get("weekly_note")
        if isinstance(weekly_note, str) and weekly_note:
            week_links[week] = f"../{weekly_note}"
        else:
            week_links.setdefault(week, f"../weeks/{week}/README.md")

    lines = ["# Experiments by Week", ""]
    for week in sorted(by_week):
        lines.append(f"- [{week}]({week_links.get(week, f'../weeks/{week}/README.md')})")
        for exp in sorted(by_week[week], key=lambda x: str(x.get("experiment_id", ""))):
            lines.append(f"  - [{exp['experiment_id']}]({exp['path']})")
    lines.append("")
    (VIEWS_DIR / "experiments-by-week.md").write_text("\n".join(lines), encoding="utf-8")


def write_project_view(experiments: list[dict[str, str | list[str]]]) -> None:
    by_project: dict[str, list[dict[str, str | list[str]]]] = defaultdict(list)
    for exp in experiments:
        project = str(exp.get("project", "unknown") or "unknown")
        by_project[project].append(exp)

    lines = ["# Experiments by Project", ""]
    for project in sorted(by_project):
        lines.append(f"- **{project}**")
        for exp in sorted(by_project[project], key=lambda x: str(x.get("experiment_id", ""))):
            lines.append(f"  - [{exp['experiment_id']}]({exp['path']})")
    lines.append("")
    (VIEWS_DIR / "experiments-by-project.md").write_text("\n".join(lines), encoding="utf-8")


def write_tag_view(experiments: list[dict[str, str | list[str]]]) -> None:
    by_tag: dict[str, list[dict[str, str | list[str]]]] = defaultdict(list)
    for exp in experiments:
        tags = exp.get("tags", [])
        if isinstance(tags, list):
            values = tags
        else:
            values = [str(tags)] if tags else []
        for tag in values:
            by_tag[str(tag)].append(exp)

    lines = ["# Tag Index", ""]
    for tag in sorted(by_tag):
        lines.append(f"- **{tag}**")
        for exp in sorted(by_tag[tag], key=lambda x: str(x.get("experiment_id", ""))):
            lines.append(f"  - [{exp['experiment_id']}]({exp['path']})")
    if not by_tag:
        lines.append("_No tags indexed yet._")
    lines.append("")
    (VIEWS_DIR / "tag-index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    experiments = load_experiments()
    write_week_view(experiments)
    write_project_view(experiments)
    write_tag_view(experiments)
    print("Updated views/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
