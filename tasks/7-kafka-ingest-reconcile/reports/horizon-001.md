# Long horizon design: 7-kafka-ingest-reconcile

Target: median **>80** assistant turns at Stage 2.

## Forcing exploration

- Seven mandatory stages; later stages cannot reread `campaign/shards/`.
- Sparse `/app/examples` only (hash rule, conflicting-hash row) — no offset/dedup manuals.
- Adversarial shard names (`packet-7585.csv`, `z-last.csv`, `00-first.csv`).
- Four committed-offset snapshots per partition; solver must pick latest valid snapshot.
- Duplicate payload_hash vs duplicate (topic,partition,key,seq) traps.
- Hidden-alpha and hidden-beta use different consumer groups and ledger gaps.

## Estimated solver path

1. Explore campaign layout and spec contract (~15 turns)
2. Implement ingest + normalize (~20 turns)
3. Offset snapshot selection and partition state (~15 turns)
4. Dedup + assign lattice (~20 turns)
5. Aggregate vs producer ledger reconciliation (~15 turns)
6. Staged debugging on hidden failures (~20+ turns)

**Total:** ~105 turns with failed runs.
