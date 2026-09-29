# Horizon 001: revision-3 instruction + 1–2/8 target

## Goal

Align task 9 with [`INSTRUCTION-AUTHORING-RULE.md`](../../../proposals/INSTRUCTION-AUTHORING-RULE.md) and [`STAGE2_DIFFICULTY.md`](../../../docs/STAGE2_DIFFICULTY.md): self-contained semantics for Stage 0, solvability for **1–2 / 8**, seven-stage pipeline for **> 80** turns.

## Changes (iteration 002)

| Change | Why |
|--------|-----|
| Revision-3 proposal — policies, outputs, verifier, interacting difficulty | Stage 0 Well-specified without deferring to spec alone |
| Six-paragraph instruction — T+n, reverse-then-convert, trade-date FX, half-away, pending exclusion | G06 IT02 mapping; wrong orderings named for horizon |
| Named nine JSON products mapped to settlement batch / totals / flags / dispositions | Agents know graded surface without a step list |
| Smoke command retained | Avoid 0/8 from missing validation loop |

## Unchanged

- Oracle pipeline, frozen expected bytes, hidden campaigns
- Seven Java stages and artifact graph in `/app/spec`

## Expected Stage 2 outcome

- **difficulty:** 1–2 / 8 (interacting payment-ops traps; strong rollouts with reconciliation experience may finish)
- **long_horizon:** seven dependent stages + spec discovery; measure on first rollout
