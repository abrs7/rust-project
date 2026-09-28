# Preflight 005: 1-ctd-cast-processing

## Verdict

READY TO UPLOAD

## Platform failure addressed (iteration 004)

**G06 IT02** — remaining gaps in `instruction.md:46-49`:

| Requirement | Fix |
|-------------|-----|
| Missing definitions (`cast.toml`, `profiles/`) | Added to `test_05` with output preservation |
| Malformed cast definitions | Invalid `cast.toml` rejected in `test_05` |
| Do not modify campaign/examples/spec | `test_21` snapshots trees before/after successful run |

Also fixed `test_19` to restore `survey-tie-points.csv` so later tests are isolated.

## Upload artifact

```text
tasks/1-ctd-cast-processing/iterations/005-pending/1-ctd-cast-processing.zip
```

## Local checks

- `test_outputs.py`: 21/21 pass
- Harbor oracle: reward 1.0
