# Preflight 001: gamma-spectrum-calibration

## Verdict

READY TO UPLOAD (local Harbor checks)

## Oracle / NOP

| Run | Reward | Runtime |
|-----|--------|---------|
| oracle (`gamma-oracle-001`) | 1.0 | ~51s |
| nop (`gamma-nop-001`) | 0.0 | ~54s |
| local `test_outputs.py` | 18/18 | ~5s |

## Design notes

- Seven-stage `gammacal` pipeline with sparse examples (no protocol manuals).
- Saturated calibration line excluded on FWHM/plateau evidence.
- Dead-time correction derived from timestamp gaps.
- Visible + hidden-alpha + hidden-beta frozen products.

## Upload artifact

```text
tasks/gamma-spectrum-calibration/iterations/001-pending/submission.zip
SHA-256: 0b5d2fcbbed07a527230b24d096602fa01c403e379a8692d6080ccba6738ee73
```
