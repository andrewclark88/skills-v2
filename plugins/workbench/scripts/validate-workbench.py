#!/usr/bin/env python3
"""Validate a project's canonical Workbench substrate."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path
from typing import Any


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)
ALLOWED_KINDS = {"epic", "feature", "story"}
ALLOWED_STATUSES = {"active", "blocked"}
LEGACY_PATHS = (
    ".work/bin",
    ".work/active/epics",
    ".work/active/features",
    ".work/active/stories",
    ".work/archive",
)


def scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
        except (ValueError, SyntaxError):
            return [part.strip().strip("\"'") for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    result: dict[str, Any] = {}
    current_list: str | None = None
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")) and current_list and raw.strip().startswith("- "):
            result[current_list].append(scalar(raw.strip()[2:]))
            continue
        current_list = None
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        if not key:
            continue
        if value.strip() == "":
            result[key] = []
            current_list = key
        else:
            result[key] = scalar(value)
    return result


def validate(project: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    work = project / ".work"
    conventions = work / "CONVENTIONS.md"

    if not conventions.is_file():
        return (["missing .work/CONVENTIONS.md"], warnings)

    config = parse_frontmatter(conventions)
    if config.get("owner") != "workbench":
        errors.append(".work/CONVENTIONS.md must declare owner: workbench")
    if config.get("schema") != 1:
        errors.append(".work/CONVENTIONS.md must declare schema: 1")
    completed_items = config.get("completed_items")
    if completed_items not in {"summarize", "discard"}:
        errors.append("completed_items must be summarize or discard")

    for required in ("active", "backlog"):
        directory = work / required
        if not directory.is_dir():
            errors.append(f"missing .work/{required}/")
        elif not (directory / ".gitkeep").is_file():
            errors.append(f"missing .work/{required}/.gitkeep")
    if completed_items == "summarize":
        for required in ("completed", "releases"):
            directory = work / required
            if not directory.is_dir():
                errors.append(f"missing .work/{required}/ for summarized completion")
            elif not (directory / ".gitkeep").is_file():
                errors.append(f"missing .work/{required}/.gitkeep")

    for legacy in LEGACY_PATHS:
        if (project / legacy).exists():
            errors.append(f"superseded workflow path remains: {legacy}")
    allowed_work_dirs = {"active", "backlog", "completed", "releases"}
    for child in sorted(path for path in work.iterdir() if path.is_dir()):
        if child.name not in allowed_work_dirs:
            errors.append(f"noncanonical work directory: {child.relative_to(project)}")

    agents = project / "AGENTS.md"
    if not agents.is_file():
        errors.append("missing canonical AGENTS.md")
    else:
        agents_text = agents.read_text(encoding="utf-8")
        starts = agents_text.count("<!-- workbench:start -->")
        ends = agents_text.count("<!-- workbench:end -->")
        if starts != 1 or ends != 1:
            errors.append("AGENTS.md must contain one complete Workbench managed section")
        if "<!-- agile-workflow:start -->" in agents_text:
            errors.append("superseded agile-workflow managed section remains in AGENTS.md")

    active_dir = work / "active"
    backlog_dir = work / "backlog"
    completed_dir = work / "completed"
    active_files = sorted(active_dir.glob("*.md")) if active_dir.is_dir() else []
    backlog_files = sorted(backlog_dir.glob("*.md")) if backlog_dir.is_dir() else []
    completed_files = (
        sorted(completed_dir.glob("*.md")) if completed_dir.is_dir() else []
    )
    for directory in (active_dir, backlog_dir, completed_dir, work / "releases"):
        if directory.is_dir():
            for child in sorted(path for path in directory.iterdir() if path.is_dir()):
                errors.append(
                    f"noncanonical nested work directory: {child.relative_to(project)}"
                )
    active_ids = {path.stem for path in active_files}
    all_item_files = active_files + backlog_files + completed_files
    id_paths: dict[str, Path] = {}
    for path in all_item_files:
        item_id = parse_frontmatter(path).get("id", path.stem)
        if isinstance(item_id, str) and item_id in id_paths:
            errors.append(
                f"{path.relative_to(project)}: duplicate id {item_id} also used by "
                f"{id_paths[item_id].relative_to(project)}"
            )
        elif isinstance(item_id, str):
            id_paths[item_id] = path

    for path in active_files:
        rel = path.relative_to(project)
        data = parse_frontmatter(path)
        required = {
            "id",
            "kind",
            "status",
            "tags",
            "parent",
            "blocked_by",
            "related_to",
            "research_refs",
            "mock_refs",
            "created",
            "updated",
        }
        for key in sorted(required - data.keys()):
            errors.append(f"{rel}: missing {key}")
        item_id = data.get("id")
        if item_id != path.stem:
            errors.append(f"{rel}: id must match filename")
        if data.get("kind") not in ALLOWED_KINDS:
            errors.append(f"{rel}: invalid kind {data.get('kind')!r}")
        if data.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{rel}: invalid status {data.get('status')!r}")
        for key in ("tags", "blocked_by", "related_to", "research_refs", "mock_refs"):
            if key in data and not isinstance(data[key], list):
                errors.append(f"{rel}: {key} must be a list")
        parent = data.get("parent")
        if parent and parent not in active_ids:
            errors.append(f"{rel}: unresolved parent {parent}")
        for key in ("blocked_by", "related_to"):
            values = data.get(key, [])
            if isinstance(values, list):
                for target in values:
                    if target not in active_ids:
                        errors.append(f"{rel}: unresolved {key} target {target}")
        if data.get("status") == "blocked":
            blocked_by = data.get("blocked_by", [])
            body = path.read_text(encoding="utf-8")
            if not blocked_by and not re.search(r"(?m)^## Blocker\s*$", body):
                errors.append(
                    f"{rel}: blocked status requires blocked_by or ## Blocker"
                )
        refs = data.get("research_refs", [])
        if isinstance(refs, list):
            for ref in refs:
                if (
                    not isinstance(ref, str)
                    or not ref.startswith(".research/")
                    or ".." in Path(ref).parts
                    or not (project / ref).is_file()
                ):
                    errors.append(f"{rel}: unresolved research ref {ref}")
        mock_refs = data.get("mock_refs", [])
        if isinstance(mock_refs, list):
            for ref in mock_refs:
                if (
                    not isinstance(ref, str)
                    or not ref.startswith(".mockups/")
                    or ".." in Path(ref).parts
                    or not (project / ref).is_file()
                ):
                    errors.append(f"{rel}: unresolved mock ref {ref}")

    for path in backlog_files:
        rel = path.relative_to(project)
        data = parse_frontmatter(path)
        for key in ("id", "tags", "created", "updated"):
            if key not in data:
                errors.append(f"{rel}: missing {key}")
        if data.get("id") != path.stem:
            errors.append(f"{rel}: id must match filename")
        if "tags" in data and not isinstance(data["tags"], list):
            errors.append(f"{rel}: tags must be a list")

    for path in completed_files:
        rel = path.relative_to(project)
        data = parse_frontmatter(path)
        if not data.get("id"):
            errors.append(f"{rel}: missing id")
        elif data.get("id") != path.stem:
            errors.append(f"{rel}: id must match filename")

    for path in work.rglob("*.md"):
        if path.parent in {active_dir, backlog_dir, completed_dir}:
            continue
        if path.name.lower() in {"done.md", "completed.md"}:
            warnings.append(f"suspicious completion artifact: {path.relative_to(project)}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".", help="Project root")
    args = parser.parse_args()
    project = Path(args.project).resolve()
    errors, warnings = validate(project)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Workbench validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"Workbench validation passed: {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
