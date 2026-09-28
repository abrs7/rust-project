#!/usr/bin/env python3
"""Mark a pending task iteration with its immutable platform result."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from task_paths import resolve_task_dir  # noqa: E402


FINAL_STATES = ("passed", "failed", "rejected")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "task",
        help="numbered folder (1-ctd-cast-processing), Harbor slug, or task number",
    )
    parser.add_argument("number", type=int)
    parser.add_argument("status", choices=FINAL_STATES)
    parser.add_argument("--note", action="append", default=[])
    args = parser.parse_args()

    workspace = Path(__file__).resolve().parents[1]
    task_dir = resolve_task_dir(workspace / "tasks", args.task)
    iterations = task_dir / "iterations"
    matches = list(iterations.glob(f"{args.number:03d}-*"))
    if len(matches) != 1:
        parser.error("iteration number is missing or ambiguous")
    current = matches[0]
    metadata_path = current / "metadata.json"
    if not metadata_path.is_file():
        parser.error("iteration metadata is missing")
    target = iterations / f"{args.number:03d}-{args.status}"
    if target != current and target.exists():
        parser.error(f"target already exists: {target}")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("status") not in {"pending", args.status}:
        parser.error("only a pending iteration can be finalized")
    metadata["status"] = args.status
    metadata["finalized_at"] = datetime.now(timezone.utc).isoformat()
    platform = metadata.setdefault("platform", {})
    platform.setdefault("notes", []).extend(args.note)
    metadata_path.write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    if target != current:
        current.rename(target)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
