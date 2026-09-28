# Stage 2 result — iteration 001

Sealed result: **FAIL** on `long_horizon`. Difficulty passed.

- Full-credit rollouts: 0 / 8 (required ≤ 2)
- Median assistant turns: 44.5 (required > 80)
- Elapsed: 6h 13m
- Package SHA-256: `35a4ca5ea52df935f43d4cf28788e076968f088e0140f83332fdf41a41b22e0b`

## Cause

Iteration 001 kept six reconstruction stages internally, but four candidate-visible
logs stated the fragment header, every transport dialect, payload layouts, and
the clock/calibration equations. Agents transcribed a decoder, tested the
visible collection, and stopped. They still failed exact hidden products, so
difficulty held while the turn count did not.

## Iteration 002 response

Remove those protocol manuals. Replace them with split worked examples and a
staged public API whose later commands cannot reread the fragment directory.
Keep the same scientific traps and hidden campaigns.
