# Stage 0 proposal: Ledger Settlement Reconcile

Proposed slug: `ledger-settlement-reconcile`

Category: Science

Implementation language: Java 21 standard library

Estimated expert time: 12–16 hours

A synthetic merchant campaign recorded ledger postings and settlement batches
with T+n business-day lag, partial reversals, and multi-currency FX. The
settlement reconciliation package was partially lost during a migration. Naive
totals that ignore lag, pending status, reversal splits, or rounding rules leave
account balances untied.

The task is to rebuild the lost ledger kit package. The supplied campaign
contains currency definitions, rational FX rates, account registries, shuffled
CSV shards of ledger entries and settlement lines, and a reversal table. Row
order and shard names carry no matching meaning.

The solution begins by loading and validating the campaign. Exact duplicate rows
are collapsed, conflicting identifiers are rejected, and all entries are
normalized into a deterministic form.

Ledger postings are matched to settlement batches by entry reference. Settlement
dates follow T+n business-day scheduling with weekend and holiday calendars.
Partial reversals adjust net settlement amounts before reconciliation.

Foreign amounts convert to base currency using the latest FX rate on or before
each trade date. Rounding uses half-away-from-zero in minor units, including
negative ties. Posted settlements must tie to reversal-adjusted ledger totals
per account; pending lines are excluded from the tie.

The implementation emits independently graded products for normalized input,
normalized entries, settlement matches, settled batches, rounded base-currency
totals, reconciliation flags, the final account summary, and provenance. Staged
and complete runs must be byte-identical.

The task is clean-room: accounts, ledgers, settlement files, calendars, and
expected outputs are generated specifically for this project. Visible campaigns
demonstrate every rule; hidden campaigns rename, resize, and recombine those
behaviors, including a different holiday table and orphan settlement lines in
hidden-beta.

The long horizon comes from seven dependent stages—strict ingestion, entry
normalization, settlement matching, T+n scheduling, FX rounding, balance
reconciliation, and canonical export—rather than from oversized fixtures or
undocumented edge cases.

Success requires three deterministic Oracle rewards of 1.0, NOP and adversarial
rewards of 0.0, a clean Harbor/TB4 package, and an official Stage 2 median
above 80 assistant turns.
