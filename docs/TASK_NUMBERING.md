# Task numbering convention

Every workspace task lives under a **numbered folder** in `tasks/`:

```text
tasks/
  1-ctd-cast-processing/
  2-gamma-spectrum-calibration/
  3-seismic-clock-catalog/
  4-telemetry-array-rebuild/
  ...
```

## Rules

1. **Folder name** — `{number}-{harbor-slug}` (example: `1-ctd-cast-processing`). Use a hyphen after the number, not `1)`.
2. **Upload ZIP name** — must match the folder basename: `1-ctd-cast-processing.zip` inside `iterations/NNN-pending/`.
3. **Harbor slug inside the ZIP** — unchanged (`ctd-cast-processing/` at the archive root; `[task] name = "terminal-bench/ctd-cast-processing"` in `task.toml`).
4. **Stable numbers** — assign the next free integer in `scripts/task_registry.py` when adding a task; never renumber after a platform upload.
5. **Scripts** — accept the numbered folder, Harbor slug, or task number:

```bash
python scripts/package_iteration.py 1-ctd-cast-processing 3
python scripts/package_iteration.py ctd-cast-processing 3
python scripts/package_iteration.py 1 3
```

## Registry

Canonical numbers live in `scripts/task_registry.py`.
