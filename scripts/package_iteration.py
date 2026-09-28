#!/usr/bin/env python3
"""Create an immutable Harbor task iteration archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from task_paths import archive_name, harbor_slug, resolve_task_dir  # noqa: E402


EXCLUDED_PARTS = {".git", "__pycache__", "jobs", ".pytest_cache"}
EXCLUDED_NAMES = {".DS_Store"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "task",
        help="numbered folder (1-ctd-cast-processing), Harbor slug, or task number",
    )
    parser.add_argument("number", type=int)
    args = parser.parse_args()

    if args.number < 1:
        parser.error("invalid iteration number")

    workspace = Path(__file__).resolve().parents[1]
    task_dir = resolve_task_dir(workspace / "tasks", args.task)
    slug = harbor_slug(task_dir)
    source = task_dir / "source"
    if not (source / "task.toml").is_file():
        parser.error(f"missing Harbor source at {source}")

    iteration = task_dir / "iterations" / f"{args.number:03d}-pending"
    if iteration.exists():
        parser.error(f"iteration already exists: {iteration}")
    iteration.mkdir(parents=True)
    archive = iteration / archive_name(task_dir)

    files = [
        path
        for path in source.rglob("*")
        if path.is_file()
        and not any(part in EXCLUDED_PARTS for part in path.relative_to(source).parts)
        and path.name not in EXCLUDED_NAMES
    ]
    with zipfile.ZipFile(
        archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as output:
        for path in sorted(files, key=lambda item: item.as_posix()):
            output.write(path, Path(slug) / path.relative_to(source))

    metadata = {
        "task": slug,
        "folder": task_dir.name,
        "iteration": args.number,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "archive": archive.name,
        "sha256": digest(archive),
        "platform": {
            "stage_1": None,
            "stage_2": None,
            "stage_3": None,
            "notes": [],
        },
    }
    (iteration / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(archive)
    print(metadata["sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
