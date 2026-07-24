"""Small frontmatter parser shared by Workbench Research scripts."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)


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


def parse(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    data: dict[str, Any] = {}
    current_list: str | None = None
    current_object: dict[str, Any] | None = None
    current_block: str | None = None
    block_lines: list[str] = []
    fold_block = False

    for raw in match.group(1).splitlines():
        stripped = raw.strip()
        indent = len(raw) - len(raw.lstrip())
        if current_block is not None:
            if indent:
                block_lines.append(raw.lstrip())
                continue
            separator = " " if fold_block else "\n"
            data[current_block] = separator.join(block_lines).strip()
            current_block = None
            block_lines = []
            fold_block = False
        if not stripped or stripped.startswith("#"):
            continue
        if indent and current_list:
            if stripped.startswith("- "):
                item = stripped[2:].strip()
                if ":" in item and not item.startswith(("http://", "https://")):
                    key, value = item.split(":", 1)
                    current_object = {key.strip(): scalar(value)}
                    data[current_list].append(current_object)
                else:
                    current_object = None
                    data[current_list].append(scalar(item))
                continue
            if current_object is not None and ":" in stripped:
                key, value = stripped.split(":", 1)
                current_object[key.strip()] = scalar(value)
                continue
        current_list = None
        current_object = None
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        if not key:
            continue
        if value.strip() == "":
            data[key] = []
            current_list = key
        elif value.strip() in {"|", ">"}:
            data[key] = ""
            current_block = key
            fold_block = value.strip() == ">"
        else:
            data[key] = scalar(value)
    if current_block is not None:
        separator = " " if fold_block else "\n"
        data[current_block] = separator.join(block_lines).strip()
    return data, text[match.end() :]


def first_heading(body: str) -> str | None:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None
