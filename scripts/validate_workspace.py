#!/usr/bin/env python3
"""Validate the per-task iteration workspace layout."""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from task_paths import archive_name, harbor_slug, parse_task_dir  # noqa: E402


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    workspace = Path(__file__).resolve().parents[1]
    tasks = workspace / "tasks"
    errors: list[str] = []
    known_archives: set[Path] = set()

    readme_sections = (
        "## Difficulty explanation",
        "## Solution explanation",
        "## Verification explanation",
        "## Relevant experience",
    )

    for task in sorted(path for path in tasks.iterdir() if path.is_dir()):
        try:
            number, slug = parse_task_dir(task.name)
        except ValueError:
            errors.append(f"{task.name}: invalid task folder name")
            continue
        label = task.name
        if number is None:
            errors.append(
                f"{label}: workspace folder must be numbered (example: 1-ctd-cast-processing)"
            )
        for required in ("README.md", "source", "iterations", "reports", "tooling", "runs"):
            if not (task / required).exists():
                errors.append(f"{label}: missing {required}")
        source = task / "source"
        task_toml = source / "task.toml"
        source_readme = source / "README.md"
        tb4_required = number is not None and 1 <= number <= 4
        if task_toml.is_file() and tb4_required:
            try:
                import tomllib

                config = tomllib.loads(task_toml.read_text(encoding="utf-8"))
                name = config.get("task", {}).get("name", "")
                expected = f"terminal-bench/{slug}"
                if name != expected:
                    errors.append(
                        f"{label}: task.toml name is {name!r}; expected {expected!r} (TB4 G02)"
                    )
            except Exception as exc:
                errors.append(f"{label}: unreadable task.toml: {exc}")
        if tb4_required and source.is_dir() and not source_readme.is_file():
            errors.append(f"{label}: missing source/README.md (TB4 G02)")
        elif source_readme.is_file():
            try:
                readme = source_readme.read_text(encoding="utf-8")
            except OSError as exc:
                errors.append(f"{label}: unreadable source/README.md: {exc}")
            else:
                for section in readme_sections:
                    if section not in readme:
                        errors.append(f"{label}: source/README.md missing {section}")
        pending = 0
        expected_archive = archive_name(task)
        for iteration in sorted((task / "iterations").iterdir()):
            if not iteration.is_dir():
                errors.append(f"{label}: unexpected iteration entry {iteration.name}")
                continue
            try:
                number_text, state = iteration.name.split("-", 1)
                iteration_number = int(number_text)
            except ValueError:
                errors.append(f"{label}: invalid iteration directory {iteration.name}")
                continue
            if state not in {"draft", "pending", "passed", "failed", "rejected"}:
                errors.append(f"{label}: invalid state {state}")
            pending += state == "pending"
            metadata_path = iteration / "metadata.json"
            archive = iteration / expected_archive
            legacy = iteration / "submission.zip"
            if legacy.is_file() and not archive.is_file():
                errors.append(
                    f"{label}: iteration {iteration_number:03d} uses submission.zip; "
                    f"rename to {expected_archive}"
                )
                archive = legacy
            if not metadata_path.is_file() or not archive.is_file():
                errors.append(f"{label}: iteration {iteration_number:03d} is incomplete")
                continue
            known_archives.add(archive.resolve())
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{label}: invalid metadata: {exc}")
                continue
            if (
                metadata.get("task") != slug
                or metadata.get("iteration") != iteration_number
                or metadata.get("status") != state
            ):
                errors.append(f"{label}: metadata disagrees with {iteration.name}")
            if metadata.get("archive") not in {expected_archive, "submission.zip"}:
                errors.append(
                    f"{label}: metadata archive {metadata.get('archive')!r} "
                    f"should be {expected_archive!r}"
                )
            actual = digest(archive)
            if metadata.get("sha256") != actual:
                errors.append(f"{label}: checksum mismatch in {iteration.name}")
            try:
                with zipfile.ZipFile(archive) as bundle:
                    roots = {
                        name.split("/", 1)[0]
                        for name in bundle.namelist()
                        if name and not name.startswith("/")
                    }
            except zipfile.BadZipFile:
                errors.append(f"{label}: invalid ZIP in {iteration.name}")
                continue
            if roots != {slug}:
                errors.append(
                    f"{label}: archive root is {sorted(roots)}, expected [{slug}]"
                )
        if pending > 1:
            errors.append(f"{label}: more than one pending iteration")

    for archive in workspace.rglob("*.zip"):
        if archive.resolve() not in known_archives:
            errors.append(f"misplaced ZIP: {archive.relative_to(workspace)}")

    if errors:
        print("\n".join(f"ERROR {message}" for message in errors))
        return 1
    print("workspace layout valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
