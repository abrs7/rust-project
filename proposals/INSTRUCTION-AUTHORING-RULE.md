# Instruction authoring rule (use on every task)

Apply this to **`instruction.md`** (agent-facing) and mirror the same semantics in **Stage 0 proposals** (reviewer-facing). The reviewer and the agent only see what you write—never assume they will infer rules from `/app/spec` alone.

## Instruction template (copy every time)

Write `instruction.md` as **six prose paragraphs** (plus the TB4 footer), in this order:

1. **Opening** — what broke, language/stdlib, package path, input roots (`/app/campaign`, `/app/examples`, `/app/spec`), determinism note (shard order meaningless).
2. **Self-contained semantics (Rule 1)** — every input shape and fixed policy that affects graded bytes: schedules, rounding, tie-breaking, duplicate handling, inclusion/exclusion (e.g. pending lines).
3. **Interacting difficulty (Rule 2)** — 2–3 plausible wrong orderings and why only the full interaction ties exactly.
4. **Outputs + canonical format (Rule 3)** — `/app/output/`, name every graded artifact (or map conceptual deliverables to named files), pin UTF-8 / JSON / JSONL / LF / integer typing; point to `output-schema.json` only for sort keys and stage graph.
5. **Verification + failure (Rules 4 & 6 partial)** — what the verifier recomputes independently, adversarial zeros, byte-identical reruns, exit without clobbering prior success.
6. **Discovery (Rule 5)** — stage names in `api-contract.md`, one visible smoke command, do-not-modify inputs/spec; no step-by-step agent recipe.

Then a blank line and the exact TB4 footer (Rule 6). Keep ≤ **1,500 words** (Rule 7).

## Rule 1 — Self-contained semantics

State every rule that affects graded bytes **in the instruction prose**:

- Input shapes (CSV columns, binary frames, cron fields, etc.)
- **Fixed policies** (never “optimize” or “infer from examples”)
- Tie-breaking, rounding, ordering, and date arithmetic
- What counts as invalid vs collapsed duplicate
- Which rows are included or excluded from totals (e.g. pending settlements)

You may point to `/app/spec/contract.json` for **field-level product schemas**, but the instruction must already pin the behaviors that wrong implementations get wrong.

## Rule 2 — Interacting difficulty

Include at least one paragraph (or sentences) explaining **why** small mistakes compound:

- Name 2–3 plausible wrong orders (FX before reversal, calendar day vs business day, etc.)
- State that each alone looks reasonable but only the full interaction ties exactly

This supports Stage 0 **Difficult** and Stage 2 **long_horizon** without listing agent steps.

## Rule 3 — Outputs and canonical format

- Name the **output directory** (`/app/output/`) and **every graded artifact** (or say “exactly the N products listed in `/app/spec/output-schema.json`” **and** name them if fewer than twelve).
- Pin serialization: UTF-8, JSON sort keys, indent vs compact JSONL, LF, integer money, no paths in products.

## Rule 4 — Verification contract (brief)

One short paragraph on what the verifier checks **independently** of the reference solution:

- Frozen byte comparison, recomputed invariants, hidden campaign traps
- Behaviors that must score zero (empty output, wrong rounding mode, wrong date basis, etc.)
- Byte-identical reruns; failure must not clobber prior successful output

Do not expose hidden test paths or reward channels.

## Rule 5 — Discovery vs cookbook

**Do not** enumerate step-by-step agent procedures (outcome-verified criterion).

**Do** provide:

- Package path and language (`/app/ledgerkit`, Java 21 stdlib, etc.)
- Pointers to `api-contract.md` and `output-schema.json` for stage names and artifact graph
- One **visible smoke command** for the shipped campaign (validation loop)
- Note that hidden verifier campaigns reuse the same rules with different seeds/traps

## Rule 6 — TB4 footer (required)

End with a blank line, then exactly:

```text
You have 28800 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
```

Also required elsewhere (not in instruction body):

- `[agent] timeout_sec = 28800` in `task.toml`
- Absolute paths only (`/app/...`), never `./` or `../`
- README.md four `##` sections: Difficulty explanation, Solution explanation, Verification explanation, Relevant experience
- `name = "terminal-bench/<slug>"` with at most three hyphen-separated words

## Rule 7 — Word limit

Keep `instruction.md` at most **1,500 words** (`len(content.split())`). Prefer dense prose over bullet lists.

## Checklist before upload

- [ ] Every instruction requirement has a matching acceptance test (G06 IT02)
- [ ] Formats match `output-schema.json` and verifier (G06 IT04)
- [ ] Oracle 1.0 / NOP 0.0 locally
- [ ] No “see bundled contract” as the **only** definition of core behavior
- [ ] Visible smoke command present
- [ ] Failure preservation stated
- [ ] Determinism (shard order, locale, etc.) stated if graded

## Proposal ↔ instruction

| Proposal section | Instruction section |
|------------------|---------------------|
| Domain + inputs + policies | Paragraphs 1–2 |
| Outputs + canonical bytes | Paragraph 3 (outputs) |
| Verifier + hidden traps + adversarial zeros | Paragraph 4 (verification) |
| Expert time + interacting difficulty | README Difficulty + proposal closing |

Proposals may be longer than instructions; instructions must still carry the graded semantics, not defer them entirely to spec files.

## Stage 2 target (every task)

Platform requires **≤ 2 / 8** full-credit rollouts **and** median **> 80** assistant turns. Client guidance prefers **1–2 / 8**, not sustained **0 / 8**.

| Risk | Symptom | Authoring lever |
|------|---------|-----------------|
| Too hard | 0 / 8, low turns | Smoke command, working stubs, semantics in instruction (Rules 1–5) |
| Too easy | > 2 / 8 | Remove transcribable maps from examples; keep hidden traps |
| Too short | long_horizon fail | Multi-stage pipeline; fragment visible evidence; no step list |

Full playbook: [`docs/STAGE2_DIFFICULTY.md`](../docs/STAGE2_DIFFICULTY.md).
