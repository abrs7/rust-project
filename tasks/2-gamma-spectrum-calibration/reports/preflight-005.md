# Preflight 005: 2-gamma-spectrum-calibration

## Verdict

READY TO UPLOAD

## What iteration 004 got wrong

### 1. The stated calibration model was mathematically wrong (blocking)

`environment/spec/contract.json` declared:

```
energy_mkeV = round_half_away_from_zero(
    (slope_num * channel + intercept_num * slope_den) / (slope_den * intercept_den))
```

The slope term is missing `* intercept_den`, so the channel contribution is
divided by an extra factor of `intercept_den`. With the visible campaign's
fitted coefficients that formula returns 9723-9728 mkeV across the whole
spectrum instead of 299939-899958 — it is not a calibration at all.

The package then used **two different models**:

| Site | Model | Correct |
|------|-------|---------|
| `contract.json` calibration_fit.model | slope term missing `intercept_den` | no |
| `pipeline.py` `_fit_cal_value` residual | same mis-stated model | no |
| `pipeline.py` `_energy_at_channel` | full model | yes |
| `pipeline.py` `_integrate_value` inversion | full model | yes |
| `tests/test_outputs.py` invariants | full model | yes |

So `calibration-fit.json` froze `residual_sum_sq_mkeV2 = 1789961603067`
(residuals of ~290000 mkeV on energies of ~300000 mkeV) while
`corrected-spectrum.jsonl` froze correct energies from the same coefficients.
No single consistent reading of the spec could produce both products: a solver
implementing the contract literally fails the spectrum, and one implementing
real OLS fails the fit. This is the IQ03 / IT03 / AD03 / AD06 cluster, and the
same defect class that G06 flagged on 1-ctd-cast-processing.

**Fix:** corrected the model in both `contract.json` mirrors, documented
`residual_sum_sq_mkeV2` explicitly, and changed `_fit_cal_value` to evaluate
the residual with the full model. Regenerated the frozen fixtures.

Residual after the fix: visible 12774, hidden-alpha 6981, hidden-beta 50342.

### 2. FWHM convention was undiscoverable (AD06)

`saturation_evidence.fwhm` said only "Full width at half maximum measured on
populated channels". Both the reference and the verifier compute
`right - left`, so the natural `right - left + 1` reading fails the frozen
comparison. The value decides nothing — the saturated line (VL03) is excluded
under either convention at `saturation_fwhm_min = 12`, since the values are
8 and 16 — so the ambiguity only excluded correct solutions.

**Fix:** stated the walk and the subtraction exactly in `contract.json`. No
code or fixture change; emitted values are unchanged.

### 3. `/app/output` was declared but never graded (IT02, unmapped requirement)

`task.toml` declares `/app/output` in `artifacts[]` and `instruction.md`
requires the products left in place, but every acceptance run wrote to a
temporary candidate-root directory. Nothing inspected the collected artifact.
This is the exact finding G06 raised as R012 on 1-ctd-cast-processing.

**Fix:** `test_21_delivered_output_artifact_matches_frozen_products` grades the
collected `/app/output`. Verified it discriminates:

| Delivered `/app/output` | Result |
|---|---|
| correct products | pass |
| empty (NOP's state) | fail |
| absent | fail |

### 4. Locale invariance was claimed but untested (IT02)

`instruction.md` requires byte-identical products "regardless of shard names,
row order, creation order, locale, or hash seed". Shard names, row order and
hash seed had coverage; locale had none, and `Candidate.invoke` hard-coded
`LC_ALL=C`. This is the finding that cost 1-ctd-cast-processing iteration 006.

**Fix:** `locale` parameter on `Candidate.invoke`, plus
`test_22_products_are_locale_invariant` over `C`, `C.UTF-8`, `en_US.UTF-8`,
`de_DE.UTF-8`.

### 5. Self-reported residual was only byte-compared (TQ04)

The verifier checked slope and intercept independently but took
`residual_sum_sq_mkeV2` on trust from the frozen fixture.

**Fix:** `check_invariants` now recomputes the residual from the fitted
coefficients and the matched pairs.

### 6. Dead code narrating the rule (AD03 / Stage 3 style)

`_peak_shape` computed a plateau width its only caller discarded, capped at
offsets 1-5, behind the comment
`# plateau uses counts >= peak - plateau_delta; computed later with campaign`.
A self-documenting seam and a maintenance hazard.

**Fix:** `_peak_shape` returns `(height, fwhm)`; the dead branch and comment
are gone. No behaviour change.

### 7. Undocumented tie-breaks (IT03)

`peak_detection.merge_rule` and `integration.search` did not state their
tie-breaking. The code keeps the lower channel in both cases.

**Fix:** stated both in `contract.json`. No code or fixture change.

### 8. Canary advisory (G02)

Four eligible text files lacked the canary: both `spec/api-contract.md`
mirrors and both `examples/README.md`.

**Fix:** canary comment added to all four.

## Files changed from 004

15 files: `environment/spec/contract.json`, `tests/spec/contract.json`,
`environment/spec/api-contract.md`, `tests/spec/api-contract.md`,
`environment/examples/README.md`, `tests/examples/README.md`,
`solution/gammacal/pipeline.py`, `tests/test_outputs.py`,
`tests/verifier_utils.py`, and `calibration-fit.json` + `provenance.json` for
visible, hidden-alpha and hidden-beta.

`instruction.md`, `task.toml`, both Dockerfiles, `solve.sh`, the campaign and
hidden fixtures, and all other frozen products are untouched.

## Local checks

| Check | Result |
|---|---|
| `python3 tests/test_outputs.py` | 22 tests, 21 pass + test_21 skipped outside container |
| Harbor oracle x3 (working tree) | 1.0 / 1.0 / 1.0, deterministic |
| Harbor NOP (working tree) | 0.0, 15 failures |
| Harbor oracle (extracted ZIP) | 1.0 |
| Harbor NOP (extracted ZIP) | 0.0 |
| test_21 / test_22 in container | both ran, not skipped; both fail under NOP |
| Harbor / Docker | harbor 0.23.0, Docker OK |
| ZIP | single root `gamma-spectrum-calibration/`, 88 files, 78% compression |
| Stray members | none (no `jobs/`, `__pycache__`, `.git`, `.DS_Store`) |
| Canary | all core and doc files |
| CRLF | none, LF only |
| instruction.md | 393 words, closing line intact, unchanged from 004 |
| Spec mirrors | `contract.json` byte-identical across `environment/` and `tests/` |

## Upload artifact

```text
tasks/2-gamma-spectrum-calibration/iterations/005-pending/2-gamma-spectrum-calibration.zip
SHA-256: 9fe30a3cbe0f941bb1d4f7017d46c5e2efacc936b47fb85e603ff1939e29875f
```

## Open risks

- **Stage 2 is unproven.** 004 and its predecessors never returned a recorded
  Stage 2 verdict, and `metadata.json` for 002 and 003 carries no platform
  notes. The long-horizon predicate (median > 80 assistant turns) has never
  been measured for this slug, and no `horizon-*.md` exists for it.
- **Version economy.** 005 is the fifth upload for this slug, past the
  three-version bonus limit.
- Before 004 the task had no consistent energy model, so any earlier Stage 2
  difficulty signal is not evidence about the current package.
