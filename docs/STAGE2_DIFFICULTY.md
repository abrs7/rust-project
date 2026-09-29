# Stage 2 target: 1–2 / 8 difficulty + long horizon

Project Thanos tasks must pass **both** Stage 2 predicates after Stage 1:

| Predicate | Platform rule | Client preference |
|-----------|---------------|-------------------|
| **difficulty** | ≤ 2 of 8 rollouts score full credit | **1–2 / 8**, not sustained **0 / 8** |
| **long_horizon** | Median assistant turns **> 80** (including failed runs) | Same |

See **[docs/STAGE2_DIFFICULTY.md](docs/STAGE2_DIFFICULTY.md)** for the 1–2/8 + horizon balance, per-task status, and iteration playbook.

Satisfying only one gate fails Stage 2. The authoring direction below balances them.

## Why 0 / 8 is as bad as 8 / 8

- **0 / 8** — platform may pass the ≤2 predicate, but the client treats sustained zero solves as **too hard or broken** (missing smoke path, oracle drift, over-thinned instruction).
- **3+ / 8** — task is too easy; difficulty gate fails.
- **1–2 / 8** — one or two strong rollouts finish with full credit; the rest fail on hidden traps or partial pipelines. This is the design target.

## The tension

| Pull toward **1–2 solves** | Pull toward **> 80 turns** |
|-----------------------------|------------------------------|
| Visible smoke command | No step-by-step agent recipe |
| Working stubs (`exact.py`, stage shells) | Algorithms stay in `/app/spec`, not instruction |
| Self-contained semantics in instruction | Fragment visible evidence (no field maps in examples) |
| Cross-linked `examples/` + contract | Multi-stage pipeline (7+ stages) |
| Restored oracle helpers agents can call | Hidden campaigns required for full credit |

**Over-tighten for horizon** (iteration 007 gamma: thinned instruction, broken stub) → **0 / 8** and **~11 turns**.

**Over-loosen for solvability** (full decoder maps in examples) → **> 80 turns** risk drops; difficulty may exceed 2 / 8.

## Authoring stack (use on every task)

1. **[INSTRUCTION-AUTHORING-RULE.md](../proposals/INSTRUCTION-AUTHORING-RULE.md)** — six-paragraph `instruction.md` + TB4 footer; mirror semantics in Stage 0 proposal (revision 3).
2. **[PROPOSAL-REVISION-GUIDE.md](../proposals/PROPOSAL-REVISION-GUIDE.md)** — proposal paragraphs: domain + policies → outputs + canonical bytes → verification + time.
3. **Horizon report** — `tasks/<n>-<slug>/reports/horizon-NNN.md` before each Stage 2 upload: what changed, expected difficulty band, long_horizon hypothesis.

## Instruction shape (every task)

```
P1  Opening — migration loss, package path, inputs, shard order meaningless
P2  Self-contained semantics — every graded policy in prose (not “see contract only”)
P3  Interacting difficulty — 2–3 wrong orderings; only full interaction ties
P4  Outputs — /app/output/, every artifact named, canonical JSON/bytes pinned
P5  Verification — frozen recompute, adversarial zeros, byte-identical reruns, failure preservation
P6  Discovery — api-contract stage names, one smoke command, do-not-modify spec/campaign
    TB4 footer (exact)
```

## Solvability checklist (avoid 0 / 8)

- [ ] Oracle 1.0 / NOP 0.0 locally, three deterministic oracle runs
- [ ] Smoke command in instruction matches visible campaign
- [ ] Environment includes callable reference helpers where appropriate (`Exact.roundHalfAway`, `exact.py`, etc.)
- [ ] Per-stage stubs with contract pointers, not empty throws
- [ ] `examples/` cross-links to contract sections; exhibits every visible trap once
- [ ] No oracle drift — graded fields match instruction + `campaign.toml` / spec

## Horizon checklist (avoid < 80 turns)

- [ ] Seven-ish dependent stages (or equivalent chained deliverables)
- [ ] No complete algorithm or field map transcribable from instruction alone
- [ ] Examples show edge cases, not full decoder tables
- [ ] Hidden campaigns vary seeds, calendars, traps — visible set does not encode answers
- [ ] Preflight naive solution fails decisive tests; note `LONG_HORIZON_RISK` if path is < ~15 steps

## Task status (2026-09-29)

| # | Slug | Stage 2 notes | Next upload |
|---|------|---------------|-------------|
| 1 | ctd-cast-processing | Multiple failed iterations; G06 fixes in 009 | `iterations/009-pending` |
| 2 | gamma-spectrum-calibration | v5 passed difficulty 0/8; v7 horizon fail (11 turns); **008 solvability tuning** | `iterations/008-pending` — **priority Stage 2 rerun** |
| 3 | seismic-clock-catalog | **Stage 2 passed** (iter 001) | iter 002 only if authoring changes |
| 4 | telemetry-array-rebuild | Horizon tightening (003); passed Stage 1+2 per author notes | `iterations/005-pending` |
| 5 | telemetry-frame-recovery | High Stage 2 risk in preflight | Monitor after upload |
| 7–10 | kafka, units, ledger, wal | First iterations; apply instruction rule before Stage 2 | Repackage after instruction/proposal edits |

## Iteration playbook after Stage 2 failure

| Failure | Likely cause | Fix |
|---------|--------------|-----|
| **0 / 8** + low turns | Over-thinned instruction, broken stubs, no smoke path | Restore solvability checklist; keep semantics in instruction |
| **0 / 8** + high turns | Genuinely too hard or verifier/oracle bug | Preflight naive path; simplify one trap, not all |
| **> 2 / 8** | Examples or instruction leak algorithm | Remove field maps; fragment evidence |
| **long_horizon fail** | Single-shot transcribable spec | Remove cookbook; add stages; thin examples |
| **long_horizon fail** + **0 / 8** | Broken middle (gamma 007) | Solvability first, then re-tighten examples only |

## References

- `tasks/2-gamma-spectrum-calibration/reports/horizon-001.md` — 0/8 + 11 turns diagnosis
- `tasks/2-gamma-spectrum-calibration/reports/horizon-002.md` — solvability tuning for 1–2/8
- `tasks/4-telemetry-array-rebuild/reports/horizon-003.md` — fragment evidence without decoder maps
- `tasks/3-seismic-clock-catalog` — passed Stage 2; dense instruction + spec split
