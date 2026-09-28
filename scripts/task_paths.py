"""Resolve numbered workspace task directories."""

from __future__ import annotations

import re
from pathlib import Path

from task_registry import NUMBER_TO_SLUG, TASK_NUMBERS

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+){0,2}$")
TASK_DIR_RE = re.compile(r"^(\d+)-([a-z0-9]+(?:-[a-z0-9]+){0,2})$")


def parse_task_dir(name: str) -> tuple[int | None, str]:
    match = TASK_DIR_RE.fullmatch(name)
    if match:
        return int(match.group(1)), match.group(2)
    if SLUG_RE.fullmatch(name):
        return None, name
    raise ValueError(f"invalid task directory name: {name}")


def folder_name(number: int, slug: str) -> str:
    return f"{number}-{slug}"


def archive_name(task_dir: Path) -> str:
    return f"{task_dir.name}.zip"


def resolve_task_dir(tasks_root: Path, ref: str) -> Path:
    direct = tasks_root / ref
    if direct.is_dir():
        return direct

    if ref.isdigit():
        number = int(ref)
        slug = NUMBER_TO_SLUG.get(number)
        if slug is None:
            raise FileNotFoundError(f"unknown task number: {number}")
        candidate = tasks_root / folder_name(number, slug)
        if candidate.is_dir():
            return candidate

    if SLUG_RE.fullmatch(ref):
        number = TASK_NUMBERS.get(ref)
        if number is not None:
            numbered = tasks_root / folder_name(number, ref)
            if numbered.is_dir():
                return numbered
        legacy = tasks_root / ref
        if legacy.is_dir():
            return legacy

    raise FileNotFoundError(f"task not found: {ref}")


def harbor_slug(task_dir: Path) -> str:
    _, slug = parse_task_dir(task_dir.name)
    return slug
