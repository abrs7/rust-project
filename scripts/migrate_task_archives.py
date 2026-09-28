#!/usr/bin/env python3
"""Rename iteration submission.zip files to match numbered task folder names."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from task_paths import archive_name, harbor_slug, parse_task_dir


def main() -> int:
    workspace = Path(__file__).resolve().parents[1]
    tasks_root = workspace / "tasks"
    for task_dir in sorted(path for path in tasks_root.iterdir() if path.is_dir()):
        try:
            parse_task_dir(task_dir.name)
        except ValueError:
            continue
        slug = harbor_slug(task_dir)
        iterations = task_dir / "iterations"
        if not iterations.is_dir():
            continue
        for iteration in sorted(path for path in iterations.iterdir() if path.is_dir()):
            legacy = iteration / "submission.zip"
            named = iteration / archive_name(task_dir)
            if legacy.is_file() and not named.exists():
                shutil.copy2(legacy, named)
            if named.is_file() and legacy.is_file() and legacy != named:
                legacy.unlink()
            metadata_path = iteration / "metadata.json"
            if not metadata_path.is_file() or not named.is_file():
                continue
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["task"] = slug
            metadata["folder"] = task_dir.name
            metadata["archive"] = named.name
            metadata_path.write_text(
                json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
            )
            print(f"updated {iteration.relative_to(workspace)} -> {named.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
