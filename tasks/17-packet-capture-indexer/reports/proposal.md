# Stage 0 proposal: Fix the packet capture indexer

Proposed slug: `packet-capture-indexer`

Category: Software

Subcategory: Systems  

Estimated expert time: 8 hours

Network diagnostics saved pcap slices split across arbitrarily named files. The indexer that builds flow summaries and conversation indexes was corrupted. The solver restores a tool that merges slices, deduplicates by five-tuple and sequence, and writes flow statistics and an index manifest with deterministic ordering.

Verification recomputes flow counts and byte totals from raw packets, validates duplicate handling, and checks hidden captures with overlapping flows and malformed headers that must fail without mutating prior indexes.

Experienced SREs regularly build similar tooling; difficulty is in exact aggregation semantics and stable ordering, not raw data volume.
