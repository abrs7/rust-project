# Stage 0 proposal: Rebuild the LRU cache simulator

Proposed slug: `lru-cache-simulator`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 6 hours

Performance tuning recorded cache access traces as shuffled event shards. The simulator must model a fixed-capacity LRU with explicit tie-breaking on eviction and produce hit/miss statistics plus the final cache state dump. Trace order is not temporal until sorted by the contract clock field.

Failed runs exit nonzero without altering a previous successful output set. The verifier replays traces independently, compares statistics and final state bytes, and uses hidden traces with capacity-one edge cases and duplicate timestamps.

Cache simulation is textbook material made practical; difficulty is deterministic replay semantics, not algorithm novelty.
