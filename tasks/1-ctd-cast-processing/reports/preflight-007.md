# Preflight 007: 1-ctd-cast-processing

## Verdict

READY TO UPLOAD

## Platform failure addressed (iteration 006)

**G06 IT02** — two material requirements in `instruction.md:40-43` lacked acceptance tests:

1. **Create the output directory when needed** — `output()` pre-created directories via `directory()`, so no test exercised absent output paths.
2. **Locale invariance** — `test_04` covered shard order and hash seed only; no test varied `LC_ALL`/`LANG`.

## Fix

- `output()` now returns a path without creating it; `prepared_output()` keeps pre-seeded failure fixtures.
- **`test_22_creates_output_directory_when_absent`** — runs against a nested path that does not exist, then asserts the directory and frozen products.
- **`test_23_products_are_locale_invariant`** — runs the visible campaign under `C`, `C.UTF-8`, `en_US.UTF-8`, and `de_DE.UTF-8`; compares byte-identical products.
- `Candidate.invoke()` accepts a `locale` parameter for explicit locale control.
- Added canary comments to `tests/hidden/hidden-alpha/cast.toml` and `hidden-beta/cast.toml` (G02 advisory).

## Upload artifact

```text
tasks/1-ctd-cast-processing/iterations/007-pending/1-ctd-cast-processing.zip
```

## Local checks

- `python3 test_outputs.py`: **23/23 OK**
- Harbor oracle: reward **1.0**
- Harbor NOP: reward **0.0**
- Docker verifier: `test_22` and `test_23` pass in oracle job
