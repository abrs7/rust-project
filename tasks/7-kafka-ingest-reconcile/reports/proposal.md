# Stage 0 proposal: Kafka Ingest Reconcile

Proposed slug: `kafka-ingest-reconcile`

Category: Science

Implementation language: Java 21 standard library

Estimated expert time: 12–16 hours

A synthetic telemetry pipeline recorded Kafka-style messages to on-disk shards
and committed-offset snapshots. The consumer that maintained aggregate counts
 mishandled offset commits and deduplicated on offset instead of payload
identity. Its totals disagree with the producer sequence ledger.

The task is to rebuild the lost ingest repair package. The supplied campaign
contains topic definitions, committed-offset snapshots, shuffled CSV message
shards, a producer ledger, and the broken consumer aggregates. Shard names and
row order carry no semantic meaning.

The solution begins by loading and validating the campaign. Conflicting payload
hashes are rejected, messages are normalized into a deterministic order, and
latest committed offsets are derived per topic and partition.

Eligible messages are those at or above the committed offset under
`next_to_consume` semantics. Among eligible rows, payload-hash identity
defines exactly-once acceptance: the lowest offset wins and later duplicates
are rejected. Replays below the committed offset are rejected separately.

Accepted messages are assigned to keys with monotonic sequence numbers. The
solver aggregates counts per topic, partition, and key, then reconciles them
against the producer ledger and documents every broken-consumer discrepancy.

The implementation emits independently graded products for normalized input,
offset state, dedup manifest, key assignments, aggregate counts, sequence
reconciliation, exactly-once counts, rejections, and provenance. Staged and
complete runs must be byte-identical.

The task is clean-room: topics, offsets, payloads, ledgers, and expected
outputs are generated specifically for this project. Visible campaigns
demonstrate every rule; hidden campaigns only rename, resize, and recombine
those behaviors.

The long horizon comes from seven dependent stages—strict ingestion, offset
recovery, payload deduplication, key assignment, aggregation, ledger
reconciliation, and canonical export—rather than from oversized fixtures or
undocumented edge cases.

Success requires three deterministic Oracle rewards of 1.0, NOP and adversarial
rewards of 0.0, a clean Harbor/TB4 package, and an official Stage 2 median
above 80 assistant turns.
