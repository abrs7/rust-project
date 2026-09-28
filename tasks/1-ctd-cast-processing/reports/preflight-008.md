# Preflight 008: 1-ctd-cast-processing

## Verdict

READY TO UPLOAD

## Why 008 exists

Version 7 was reviewed twice. Both reviews left G06 blocked on
`REVIEW.COVERAGE_UNMAPPED`, which the platform classes `BLOCKED · PLATFORM`.
The two reviews otherwise disagreed sharply, because G06 is an LLM reviewer
(`gpt-6-luna · policy g06-package-quality.v32`) and is not deterministic:

| | Review 1 (`d909793b48ed`) | Review 2 (`114b7d7c3c71`) |
|---|---|---|
| Warnings | 6 | 2 |
| G06 criteria passed | 25 | 30 |
| IQ03, IT03, IT04, AD03, AD06 | warning (RMS vs MSE) | pass |
| IT02 (`/app/output`) | **warning** | **warning** |
| Unmapped requirement | **R012** | **R013** |
| G02 canary advisory | `tests/spec/api-contract.md` | `tests/spec/api-contract.md` |

Two findings reproduced across both independent reviews, and those are the ones
008 is built to clear:

1. **IT02** — the deliverable at `/app/output` is declared in `artifacts[]` and
   required by `instruction.md`, but no test asserted it. Review 2 stated it
   precisely: "it does not read or assert generated products at /app/output, so
   the artifact entry does not establish coverage."
2. **G02 canary advisory** on `tests/spec/api-contract.md`.

The RMS-vs-MSE cluster appeared in review 1 only, but it is a real defect
independent of whether a given review pass reports it: `contract.json:76`
specified root-mean-square while `pipeline.py` returned `round_half_away(sq,
used)` — a mean of squares, no square root — and the frozen fixtures encoded
the mean-squared value. A solver implementing the published contract scored 0.
Fixed here regardless of review 2's silence.

## Changes from 007

### Contract and reference now state one metric

Renamed throughout: `survey_tie_rms` -> `survey_tie_mse`,
`minimize_survey_tie_rms_micro` -> `minimize_survey_tie_mse_micro`,
`survey_tie_rms_micro` -> `survey_tie_mse_micro`, `_survey_rms` ->
`_survey_mse`. Contract prose now reads "Mean of squared (predicted_density -
tie_density) ... rounded half away from zero".

The spec was corrected to match the code rather than the reverse: a square root
would have required defining exact integer-sqrt rounding in a task built on
exact integer arithmetic, trading one finding for a worse one. Because the
square root is monotonic, no winner or ordering changes. Verified across all
three campaigns:

| Campaign | scores identical | winner |
|---|---|---|
| visible | yes | 45/1 unchanged |
| hidden-alpha | yes | 52/1 unchanged |
| hidden-beta | yes | 47/1 unchanged |

Fixtures were regenerated rather than text-substituted because
`provenance.json`'s `product_sha256` hashes the diagnosis object.

### `/app/output` is now graded (IT02, R013)

`test_24_delivered_output_artifact_matches_frozen_products` asserts the
collected `/app/output` against the frozen visible products, via a
`delivered_output` resolver in `setUpClass` with a `CTDPROC_DELIVERED_OUTPUT`
override for local runs. Verified it discriminates:

| Delivered `/app/output` | Result |
|---|---|
| correct products | pass |
| empty (NOP's state) | fail |
| absent | fail |

It is load-bearing, not decorative: it is one of NOP's failures in the
container, confirmed on the packaged ZIP.

### Previously hidden threshold documented

`I64_MAX` (9223372036854775807) was the "no applicable tie rows" sentinel,
present only in `pipeline.py`. It is now stated in the contract. Review 2 did
not flag it; the guidebook's Stage 3 rule on hidden thresholds does.

### Canary

Added to `tests/spec/api-contract.md`, the path both reviews cited. Both
`contract.json` mirrors were left alone: strict JSON cannot carry a comment,
and breaking the parse costs more than one advisory.

## Files changed from 007

13 files: `environment/spec/contract.json`, `tests/spec/contract.json`,
`tests/spec/api-contract.md`, `environment/examples/README.md`,
`tests/examples/README.md`, `solution/ctdproc/pipeline.py`,
`tests/test_outputs.py`, and `latitude-diagnosis.json` + `provenance.json` for
visible, hidden-alpha and hidden-beta.

`instruction.md`, `task.toml`, both Dockerfiles, `solve.sh`, and every campaign
and hidden fixture are untouched.

## Local checks

| Check | Result |
|---|---|
| `python3 tests/test_outputs.py` | 24 tests, 23 pass + test_24 skipped outside container |
| Harbor oracle x3 (working tree) | 1.0 / 1.0 / 1.0, deterministic |
| Harbor NOP (working tree) | 0.0 |
| Harbor oracle (extracted ZIP) | 1.0, 24 tests, test_24 ok |
| Harbor NOP (extracted ZIP) | 0.0, test_24 FAIL |
| Stale `rms` references | none |
| Spec mirrors | `contract.json` byte-identical |
| Canary | all core and spec doc files |
| CRLF | none, LF only |
| instruction.md | 397 words, closing line intact, unchanged from 007 |
| ZIP | single root `ctd-cast-processing/`, 70 files, 75% compression, no strays |

## Upload artifact

```text
tasks/1-ctd-cast-processing/iterations/008-pending/1-ctd-cast-processing.zip
SHA-256: 4ad79b445a2162c1b3a2d5e1245d7d4af80b6c36875017eed085903df3c3b0c5
```

Distinct from version 7 (`b680974a...`), so it will not trip "File hash already
exists".

## Open risks

- **`COVERAGE_UNMAPPED` may not clear.** The platform states no ZIP change
  clears it. The reason to expect otherwise is circumstantial but consistent:
  across both reviews the single unmapped requirement was the `/app/output`
  deliverable, and `test_24` maps it. If 008 blocks the same way, the protocol
  is the Bugs thread with task ID `5916d7deca5b3db70414a893fd2270c6` and the
  version and evaluation numbers, not a version 9.
- **Stage 2 has never run on this slug.** Eight versions have gone to Stage 1
  mechanics. The long-horizon predicate (median > 80 assistant turns) kills
  ~92% of tasks and is unmeasured here; `reports/` holds no `horizon-*.md` for
  this task.
- **Version economy.** 008 is the eighth upload; the three-version bonus is
  long gone.
