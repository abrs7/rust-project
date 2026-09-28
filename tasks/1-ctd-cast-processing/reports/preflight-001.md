# Preflight 001: ctd-cast-processing

## Verdict

READY TO UPLOAD (local Harbor checks)

## Oracle / NOP

| Run | Reward | Runtime |
|-----|--------|---------|
| oracle (`ctd-oracle-001`) | 1.0 | ~58s |
| nop (`ctd-nop-001`) | 0.0 | ~40s |
| local `test_outputs.py` | 17/17 | ~7s |

## Design notes

- Seven-stage `ctdproc` pipeline: ingest → split → depth → derive → bin → qc → export.
- Latitude-dependent exact depth conversion and UNESCO-style density.
- hidden-beta header latitude lie; inferred via survey tie RMS + density QC.
- Examples mirrored under `source/tests/examples/` for Harbor verifier access.

## Upload artifact

```text
tasks/ctd-cast-processing/iterations/001-pending/submission.zip
SHA-256: ca4439189f404d72317636c4c122dbb0b9bc23671ec046d91cad20133da7f03e
```
