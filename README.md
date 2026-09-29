# rustLabs task workspace

Every task is isolated under a **numbered folder** in `tasks/`. Task sources,
submitted ZIPs, reports, tooling, trajectories, and local runs must not be
stored at the workspace root.

Each task uses this layout:

```text
tasks/1-ctd-cast-processing/
  README.md
  source/                 current editable Harbor task
  iterations/
    002-pending/
      1-ctd-cast-processing.zip   upload artifact (name matches folder)
      metadata.json               checksum and lifecycle result
  reports/                proposals and preflight reports
  tooling/                fixture generators and attack candidates
  trajectories/           downloaded Stage 2 trajectory bundles
  runs/                   local Harbor jobs and logs
```

**Numbering:** `{number}-{harbor-slug}` (example: `1-ctd-cast-processing`). The
upload ZIP must use the same basename (`1-ctd-cast-processing.zip`). The Harbor
slug inside the ZIP stays unprefixed (`ctd-cast-processing/`). See
`docs/TASK_NUMBERING.md` and `scripts/task_registry.py`.

Iteration states are `draft`, `pending`, `passed`, `failed`, or `rejected`.
Never replace an iteration ZIP. After platform feedback, rename the iteration
directory to its final state, update `metadata.json`, and package the next
number from `source/`. Once an iteration passes all stages, mark it `passed`
and stop creating iterations for that slug.

Create a new immutable iteration with:

```bash
python scripts/package_iteration.py 1-ctd-cast-processing 3
# or: python scripts/package_iteration.py ctd-cast-processing 3
# or: python scripts/package_iteration.py 1 3
```

Record its final platform outcome without overwriting the ZIP:

```bash
python scripts/finalize_iteration.py 1-ctd-cast-processing 3 passed \
  --note "platform result"
```

Validate the entire workspace:

```bash
python scripts/validate_workspace.py
```

Before every upload, confirm TB4 Stage 1 G02 inside `source/`:

- `task.toml`: `[task] name = "terminal-bench/<slug>"` (not `rustlabs/…`)
- `README.md` beside `task.toml` with `## Difficulty explanation`, `## Solution explanation`, `## Verification explanation`, and `## Relevant experience`

The workspace `tasks/1-<slug>/README.md` is not packaged; only `source/README.md`
goes in the ZIP. See `docs/PREFLIGHT_INSTRUCTIONS.md`.

## Task registry

| # | Folder | Harbor slug |
|---|--------|-------------|
| 1 | `1-ctd-cast-processing` | `ctd-cast-processing` |
| 2 | `2-gamma-spectrum-calibration` | `gamma-spectrum-calibration` |
| 3 | `3-seismic-clock-catalog` | `seismic-clock-catalog` |
| 4 | `4-telemetry-array-rebuild` | `telemetry-array-rebuild` |
| 5 | `5-telemetry-frame-recovery` | `telemetry-frame-recovery` (legacy) |
| 6 | `6-django-cors-broken` | `django-cors-broken` (legacy) |
| 7 | `7-kafka-ingest-reconcile` | `kafka-ingest-reconcile` (Java) |
| 8 | `8-units-library-reconcile` | `units-library-reconcile` (Java) |
| 9 | `9-ledger-settlement-reconcile` | `ledger-settlement-reconcile` (Java) |
| 10 | `10-measurement-wal-recover` | `measurement-wal-recover` (Go) |

## Current upload candidates

```text
tasks/1-ctd-cast-processing/iterations/009-pending/1-ctd-cast-processing.zip
tasks/2-gamma-spectrum-calibration/iterations/009-pending/2-gamma-spectrum-calibration.zip   ← Stage 2 priority (v6 failed 3/8 + 76.5 turns)
tasks/3-seismic-clock-catalog/iterations/002-pending/3-seismic-clock-catalog.zip
tasks/4-telemetry-array-rebuild/iterations/005-pending/4-telemetry-array-rebuild.zip
tasks/7-kafka-ingest-reconcile/iterations/001-pending/7-kafka-ingest-reconcile.zip
tasks/8-units-library-reconcile/iterations/001-pending/8-units-library-reconcile.zip
tasks/9-ledger-settlement-reconcile/iterations/002-pending/9-ledger-settlement-reconcile.zip
tasks/10-measurement-wal-recover/iterations/002-pending/10-measurement-wal-recover.zip
```

Shared platform guidance is in `docs/`. Stage 2 target (**1–2 / 8** difficulty + **> 80** median turns): [`docs/STAGE2_DIFFICULTY.md`](docs/STAGE2_DIFFICULTY.md).
