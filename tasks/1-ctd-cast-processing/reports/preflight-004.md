# Preflight 004: 1-ctd-cast-processing

## Verdict

READY TO UPLOAD

## Platform failure addressed (iteration 003)

**G06 IT02** — material instruction requirements at `instruction.md:46-49` lacked acceptance tests:

| Requirement | Fix |
|-------------|-----|
| Empty downcast | `test_18` + oracle rejects when no prefix reaches max pressure |
| Non-unique latitude diagnosis | `test_19` + oracle rejects tied candidate scores |
| Output replacement failure | `test_20` + atomic `_write_atomic` with rollback |

Also aligned `contract.json` downcast rule with instruction (no fallback prefix when max is unreachable).

## Upload artifact

```text
tasks/1-ctd-cast-processing/iterations/004-pending/1-ctd-cast-processing.zip
```

## Local checks

- `test_outputs.py`: 20/20 pass
- Harbor oracle: reward 1.0
