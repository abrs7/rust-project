# Horizon 002: solvability tuning (target 1/8)

## Goal

Stage 2 **difficulty** allows ≤2 full-credit rollouts per 8. Client guidance
prefers **1–2 solves**, not sustained **0/8** (rejection risk). Iteration 007
horizon edits alone still target 0/8 with low turn counts.

## Changes (iteration 008)

| Change | Why |
|--------|-----|
| Restore working `environment/gammacal/exact.py` | Removes a common early blocker; agents focus on the seven-stage pipeline |
| Per-stage `pipeline.py` stubs with contract pointers | Clear implementation units without copying algorithms into instruction |
| `examples/README.md` cross-links to contract sections | Edge-case fixtures become usable without guessing semantics |
| Visible smoke command in instruction | Gives a validation loop like telemetry-frame-recovery; hidden campaigns still required for full credit |
| Keep stage graph out of instruction prose | Algorithms stay in `/app/spec`; reduces single-shot transcription |

## Unchanged

- Frozen products, verifier, oracle pipeline (v5-restored)
- Hidden campaigns and byte-exact grading
- TB4 metadata and closing line

## Expected Stage 2 outcome

- **difficulty:** 1–2 / 8 full credit (platform predicate: ≤2)
- **long_horizon:** still requires median > 80 turns; seven-stage implementation should lengthen successful paths; rerun needed to measure
