# Long horizon design: 10-measurement-wal-recover

Target: median **>80** assistant turns at Stage 2.

## Forcing exploration

- Seven stages; scan/dedup/merge cannot reread raw WAL shards after ingest.
- Sparse examples only — no frame-layout cheat sheet beyond CRC and dedup rules.
- Torn shard tails, decoy magic bytes, duplicate sequences, and CRC failures.
- Hidden campaigns change `max_gap_ns` and shard sizing.

## Estimated solver path

1. Recorder + shard ingestion (~15 turns)
2. Frame scan + CRC validation (~15 turns)
3. Sequence dedup tie-breaking (~15 turns)
4. Timestamp merge + validation (~15 turns)
5. Gap reporting + export (~15 turns)
6. Hidden fixture debugging (~20+ turns)

**Total:** ~95 turns with failed runs.
