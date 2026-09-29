# Horizon 001: gamma-spectrum-calibration

## Stage 2 failure (iteration 005, v5 ZIP)

| Predicate | Required | Observed | Result |
|-----------|----------|----------|--------|
| difficulty | full credit ≤ 2 of 8 | 0 of 8 | PASS |
| long_horizon | median assistant turns > 80 | 11 | FAIL |

All eight rollouts scored 0.0 with 5–14 assistant turns. Agents were not
engaging long enough to reach the horizon bar even though difficulty (0 solves)
passed.

## Root cause

The agent-facing surface spelled out the full pipeline:

- `instruction.md` listed every CLI stage name and the exact `python -m gammacal run` command.
- `examples/README.md` narrated what each fixture demonstrated (rounding, saturation, dead time).
- `environment/gammacal/exact.py` shipped a working `round_half_away`, removing one implementation step.

Strong agents could read `contract.json` + `api-contract.md` and attempt a
single-shot implementation; weak agents hit `NotImplementedError` and stopped
within a dozen turns.

## Horizon tightening (iteration 007)

1. **instruction.md** — removed the stage-name cookbook and the canned run
   command; behavior must be recovered from `/app/spec/api-contract.md` and
   `/app/spec/output-schema.json`.
2. **examples/README.md** — filenames only; no algorithm hints.
3. **environment/gammacal/exact.py** — stub; agents implement rounding from
   contract + `rounding.json`.
4. **campaign/inventory.txt** — shard counts only (telemetry-array pattern).

Contracts, frozen products, verifier, and oracle are unchanged. Spec files
remain complete so 1–2/8 solves stay achievable for agents that work through
the full stage graph.

## TB4 compliance check (pre-upload)

| Rule | Status |
|------|--------|
| `name = "terminal-bench/gamma-spectrum-calibration"` (≤3 slug words) | OK |
| `[agent] timeout_sec = 28800` | OK |
| instruction.md closing line + blank line before it | OK |
| README four `##` sections, human prose | refreshed |
| instruction.md absolute `/app/...` paths only | OK |
| metadata author, category, subcategory, tags, expert_time | OK |
| Oracle 1.0 / NOP 0.0 | re-run before upload |
| G06 requirement/test mapping | unchanged from passing v5 |

## Target after upload

- **long_horizon:** median > 80 assistant turns (expect longer exploration before
  first full pass; not guaranteed until Stage 2 reruns).
- **difficulty:** 1–2 of 8 full credit (avoid sustained 0/8 client rejection).
