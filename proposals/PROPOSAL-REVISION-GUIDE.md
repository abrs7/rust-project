# Proposal revision guide (Stage 0 feedback)

Use this when a proposal returns **Uncertain** on Well-specified, Solvable, or Difficult.

## Always state in prose (paragraph 1–2)

1. **Fixed policy, not optimization** — name the deterministic rule (tie order, rounding, scheduling policy). Never say the solver must “infer semantics from examples.”
2. **Units and representations** — integers, rationals, minutes, byte formats, canonical JSON, etc.
3. **Failure semantics** — exit nonzero; list what triggers failure; **preserve prior successful output bytes** on failure.
4. **Determinism** — invariant to shard names, row order, locale, hash seed (as applicable).
5. **Verification** — independent recomputation, hidden campaigns, frozen byte comparison.

## Avoid

- “Infer from examples rather than a prose walkthrough”
- Unspecified “optimal” or “best” schedules/plans/matchings
- Step lists for the agent (outcome-verified criterion)
- Vague “repair the tool” without naming deliverable artifacts

## Paragraph shape (2–3 paragraphs)

1. Goal + inputs/outputs + **explicit core semantics**
2. Verification + failures + determinism + hidden fixtures
3. Expert time + why non-trivial (optional; can merge into §2)

## Category / subcategory

- **Category:** Software
- **Subcategory:** Systems | Algorithms | Databases | Data engineering | Frontend | Languages
