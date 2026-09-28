# Stage 0 proposal: Measurement WAL Recover

Proposed slug: `measurement-wal-recover`

Category: Science (physics)

Implementation language: Go 1.22 standard library

Estimated expert time: 12–16 hours

A laboratory recorder wrote append-only measurement WAL shards with CRC-protected
frames. After storage migration, torn pages, duplicate sequence numbers, and bad
CRC frames leave the naive reader with checksum failures and a broken time
series.

The task is to rebuild the lost WAL recovery package. The supplied campaign
contains recorder metadata, a shard index, and shuffled binary WAL files. Shard
names and on-disk order carry no semantic meaning.

The solution begins by loading and validating the campaign. Shard payloads are
normalized into a deterministic ingest artifact, frames are scanned with CRC
validation, duplicate sequences are resolved with stable tie-breaking, and the
accepted measurements are merged by timestamp.

Gap reporting flags timestamp jumps above the configured threshold. The
implementation emits independently graded products for normalized input, frame
index, dedup manifest, merged series, validation report, gap report, and
provenance. Staged and complete runs must be byte-identical.

The task is clean-room: recorder rules, shards, traps, and expected outputs are
generated specifically for this project. Visible campaigns demonstrate every
rule; hidden campaigns rename, resize, and recombine those behaviors.

The long horizon comes from seven dependent stages—strict ingestion, frame
scanning, CRC filtering, sequence deduplication, series merge, monotonicity
validation, gap reporting, and canonical export—rather than from oversized
fixtures or undocumented edge cases.

Success requires three deterministic Oracle rewards of 1.0, NOP and adversarial
rewards of 0.0, a clean Harbor/TB4 package, and an official Stage 2 median
above 80 assistant turns.
