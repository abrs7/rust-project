# Horizon 003: balance 1–2/8 and median > 80

## Stage 2 failure (iteration 008, v6 ZIP)

| Predicate | Required | Observed | Result |
|-----------|----------|----------|--------|
| difficulty | full credit ≤ 2 of 8 | **3 of 8** | FAIL |
| long_horizon | median assistant turns > 80 | **76.5** | FAIL |

Rollouts: rewards `[0,0,0,1,1,1,0,0]`; turns `[90,63,69,98,80,79,74,70]`.

Iteration 008 restored solvability (0/8 → 3/8) but overshot difficulty and remained
3.5 turns below the horizon bar.

## Changes (iteration 009)

| Change | Horizon | Difficulty |
|--------|---------|------------|
| Six-paragraph instruction with pinned policies, no contract-section cookbook | More spec reading | Slightly harder |
| `examples/README.md` — filenames only, no contract cross-links | +exploration | −1 shortcut |
| `pipeline.py` stubs — bare `NotImplementedError`, no section pointers | +exploration | −1 shortcut |
| Pin histogram reject rules; add duplicate-channel summation test | G06 IT02/TQ05 | — |
| `require_failure` checks concise stderr (no traceback) | G06 IT06 | — |
| **Keep** working `exact.py`, smoke command, full `contract.json` | Solvability guard | Avoid 0/8 |

## Target

- **difficulty:** 1–2 / 8 (drop one borderline solve at 79–80 turns)
- **long_horizon:** median > 80 (expect +5–10 turns from reduced shortcuts)

## Unchanged

- Frozen expected bytes, hidden campaigns, oracle pipeline
