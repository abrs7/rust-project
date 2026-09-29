# Proposal revision guide (Stage 0 feedback)

Use when a proposal returns **Uncertain** on Well-specified, Solvable, or Difficult.

## Revision 3 pattern (accepted for task 11)

The reviewer only sees the proposal—not `instruction.md` or bundled contracts. **Every rule that affects bytes must appear in the proposal text.**

**Agent instructions:** follow [`INSTRUCTION-AUTHORING-RULE.md`](INSTRUCTION-AUTHORING-RULE.md) — same semantics as the proposal, plus TB4 footer, smoke command, and G06 test mapping.

### Paragraph 1 — domain + inputs + core semantics

- Opening: what broke, what language (stdlib-only), what the package consumes/produces.
- Name every input type and field (cron fields, frame layout, INI sections, etc.).
- State **fixed policy, not optimization**.
- Define interacting rules that cascade (DST + deps + capacity; line boundaries + gzip generations; etc.).

### Paragraph 2 — outputs + canonical format

- Name each output file and sort order inside it.
- Pin **canonical JSON** byte-for-byte: UTF-8, sorted keys, `,` and `:` without spaces, integer/bool typing, trailing newline; JSONL per-line same rules.
- For non-JSON outputs, pin line endings, section order, merge rules.

### Paragraph 3 — failure + verification + time

- **Exit 2** on invalid; diagnostic to **separate report path**; prior output directory **byte-identical**.
- List every invalid condition explicitly (duplicates, cycles, malformed fields, unknown IDs).
- Define cycle/diagnostic structure (SCC list, lex order)—not vague “cyclic job IDs.”
- Verification: independent reference, hidden campaigns with named traps, reshuffle identity, atomic replacement after success.
- Expert time reflects **interacting semantics**, not “reading the contract.”

## Avoid

- “Rules are in the bundled contract/examples” as the primary spec
- “Infer from examples”
- Unspecified optimal/best behavior
- Agent step lists (outcome-verified criterion)
- Underspecified ready-queue behavior, canonical JSON, or failure atomicity

## Category / subcategory

- **Category:** Software
- **Subcategory:** Systems | Algorithms | Databases | Data engineering | Frontend | Languages
