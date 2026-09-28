# Stage 0 proposal: Fix the incremental deduplication job

Proposed slug: `incremental-deduplication-job`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 7 hours

Streaming dedup state and new event shards must be merged so duplicates collapse by business key with earliest-seen wins unless a tombstone marker says otherwise. The job exports updated state, accepted events, and duplicate statistics.

Failed runs exit nonzero without altering a previous successful output set. Verification replays merges independently, checks tombstone precedence, and tests hidden shards with reshuffled duplicates and partial state files.

Dedup pipelines are common; difficulty is stable merge semantics across stages.
