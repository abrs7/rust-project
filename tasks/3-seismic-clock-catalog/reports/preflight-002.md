# Preflight 002: seismic-clock-catalog

## Verdict

READY TO UPLOAD (TB4 Stage 1 G02 fixes)

## Changes from 001

| Issue | Fix |
|-------|-----|
| `HARBOR.TASK_CONFIG_INVALID` | `[task] name` → `terminal-bench/seismic-clock-catalog` |
| `README.MISSING` | Added `source/README.md` with four required `##` sections |
| `TB3.CANARY_ADVISORY` | Added canary to all `clockrecover/*.py` stubs and solution modules |

## Upload artifact

```text
tasks/seismic-clock-catalog/iterations/002-pending/submission.zip
SHA-256: 0ccdd15b7ca7cca7a0d5ba2b4de3b9041a96f7e04dd85ef53b699567946b798b
```

## Note on 001-passed

001 passed Stage 2 on the pre-TB4 package (`rustlabs/` namespace, no README). Platform Stage 1 now requires TB4 G02; use iteration 002 for re-upload.
