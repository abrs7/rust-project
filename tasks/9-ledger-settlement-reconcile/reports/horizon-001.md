# Long horizon design: 9-ledger-settlement-reconcile

Target: median **>80** assistant turns at Stage 2.

## Forcing exploration

- Seven stages; settle/reconcile cannot reread raw ledger shards.
- Sparse examples (rounding ties, T+n calendar) — no settlement policy manual.
- Multi-currency with half-away-from-zero FX in minor units.
- T+n business-day lag with weekend/holiday calendar.
- Partial reversals split across settlement batches.
- Hidden-beta uses different holiday table and orphan lines.

## Estimated solver path

1. Ingest + normalize ledger entries (~15 turns)
2. Match postings to settlement batches (~20 turns)
3. T+n calendar and lag application (~20 turns)
4. FX rounding per contract (~15 turns)
5. Reconcile balances vs settlement files (~15 turns)
6. Hidden calendar/reversal traps (~25 turns)

**Total:** ~110 turns with failed runs.
