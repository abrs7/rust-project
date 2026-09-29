# Stage 0 proposal: Ledger Settlement Reconcile

Proposed slug: `ledger-settlement-reconcile`

Category: Software Engineering

Subcategory: backend-development

Implementation language: Java 21 standard library

Estimated expert time: 14 hours

---

## Submission text

A merchant payments campaign is supplied as shuffled CSV shards of ledger postings and settlement lines, an account registry, currency definitions with dated FX rates as exact rationals, a reversal table, and business-day calendars. Settlement runs on a T+n business-day schedule against those calendars; some postings were partially reversed after settlement was scheduled; and foreign-currency amounts must be converted and rounded into base minor units before anything ties. The settlement reconciliation kit was lost in a migration, and the surviving account balances do not tie. Rebuild the Java 21 package `/app/ledgerkit` so `/app/output/` holds nine canonical JSON products from those CSV inputs: `settlement-schedule.jsonl` (settled batch for every ledger entry), `reconciliation.json` and `final-report.jsonl` (reversal-adjusted base-currency totals and a reconciliation flag per account), `exceptions.jsonl` (a disposition for every input row including unmatched entries and orphan settlement lines), plus the pipeline intermediates `normalized-input.json`, `normalized-entries.jsonl`, `matched-pairs.jsonl`, `rounded-amounts.jsonl`, and `provenance.json` defined in `/app/spec/output-schema.json`. Shard names, row order, and file identifiers carry no matching meaning.

Fixed policies, not heuristics: expected settle date is trade date plus n business days skipping Saturday, Sunday, and listed holidays; drift is the signed business-day count from expected to reported settle date. Partial reversals subtract from the linked settlement line net and from the linked ledger entry effective amount before base conversion. Base conversion uses the latest FX rate with as_of_date on or before trade date (not settlement date): base_minor = roundHalfAway(signed_native × rate_num × 10^base_exp, rate_den × 10^from_exp), with ties rounded away from zero including negative ties. Only posted settlements enter settlement totals; pending lines are reported but excluded from the tie. Exact duplicate rows collapse; conflicting duplicates on the same identifier reject the run rather than merge. JSON is UTF-8, sort-key ordered, two-space indent for JSON objects, compact JSONL, LF terminated, integer money only, no paths in products.

The verifier compares against frozen values computed from the generator's own parameters, independently of the reference solution. It checks each entry's settlement date and batch; per-account reversal-adjusted totals in minor units, rounded half away from zero including negative ties; every row's disposition and reason; and the reconciliation flags. Duplicate rows must be collapsed and conflicting identifiers rejected rather than merged. Pending lines are excluded from the tie and must be reported as such. Two runs must produce byte-identical output. Hidden campaigns vary the seed, holiday calendar, T+n value, account and currency counts, which entries are partially reversed, and the presence of orphan settlement lines; visible campaigns exhibit every behaviour at least once. Empty output, a constant summary, a solution that settles on calendar days, one that converts before applying reversals, and one that rounds half-up all score zero.

The difficulty is that each of these rules individually produces a plausible result and only their interaction ties. Rounding a converted amount before subtracting a reversal differs from subtracting first by a single minor unit on a minority of accounts; applying the FX rate dated on the settlement date rather than the trade date shifts a different subset; and treating a holiday as a business day moves an entry into the wrong batch without making any row look malformed. Each wrong choice leaves a small, self-evident residual: balances that should tie exactly do not. This is the work a payments operations team does after a migration, and getting it to the minor unit is the entire point. A working reference solution uses Java 21 and the standard library only; someone who has reconciled settlement files should need about fourteen hours.
