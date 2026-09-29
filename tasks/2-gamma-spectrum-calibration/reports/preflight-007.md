# Preflight 007: 2-gamma-spectrum-calibration

## Verdict

READY TO UPLOAD (Stage 2 horizon retry)

## Stage 2 failure addressed (v5 / iteration 005)

| Predicate | Required | v5 observed |
|-----------|----------|-------------|
| difficulty | ≤2 full credit / 8 | 0 / 8 ✓ |
| long_horizon | median turns > 80 | **11** ✗ |

## Horizon tightening (this iteration)

1. **instruction.md** — removed stage-name cookbook and canned `run` command; agents recover CLI/API from `/app/spec/`.
2. **examples/README.md** — filenames only (no algorithm narration).
3. **environment/gammacal/exact.py** — stub; implement `round_half_away` from contract + `rounding.json`.
4. **campaign/inventory.txt** — shard counts only.

## Reverted broken local drift

Iteration 006 had added `background_width` / `pause_gap_us` to the oracle without
updating `campaign.toml` or frozen fixtures (oracle exit 2 locally). Restored
`solution/gammacal/pipeline.py` from the passing v5 ZIP (005-rejected archive).

## TB4 compliance

| Check | Status |
|-------|--------|
| `name = "terminal-bench/gamma-spectrum-calibration"` (3 slug words) | ✓ |
| `[agent] timeout_sec = 28800` | ✓ |
| instruction.md blank line + exact closing sentence | ✓ (298 words) |
| README.md four `##` sections | ✓ refreshed |
| Absolute `/app/...` paths in instruction | ✓ |
| metadata author, category, subcategory, tags, expert_time | ✓ |
| Pinned Python base image digest | ✓ unchanged |
| Verifier isolated from agent | ✓ |

## Local checks

| Check | Result |
|-------|--------|
| `python3 test_outputs.py` | 21 pass, 1 skip (test_21 container-only) |
| Harbor oracle | **1.0** |
| Harbor NOP | **0.0** |

## Upload artifact

```text
tasks/2-gamma-spectrum-calibration/iterations/007-pending/2-gamma-spectrum-calibration.zip
SHA-256: 7439160f16c630e155d718493c28fb86ac15e3e35e284b4068a2d12499564345
```

## Open risks

- **long_horizon** is unproven until Stage 2 reruns; horizon edits aim for >80
  median turns via reduced hand-holding, not guaranteed.
- **difficulty** at 0/8 passed v5; client prefers **1–2/8** — spec remains
  complete in `/app/spec` for strong agents.
- Do **not** reintroduce oracle-only fields absent from agent-visible material
  (iteration 006 lesson).
