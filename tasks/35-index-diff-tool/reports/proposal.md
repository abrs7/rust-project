# Stage 0 proposal: Repair the index diff tool

Proposed slug: `index-diff-tool`

Category: Software

Subcategory: Databases  

Estimated expert time: 7 hours

Two index snapshots from synthetic tables arrive as sorted key dumps in CSV shards. The diff tool must emit added, removed, and changed keys with old/new values, using deterministic ordering independent of shard names.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes diffs independently, checks value equality semantics, and tests hidden snapshots with reorder-only shards that must not appear as changes.

Table diffing is routine; exact output formatting and stable ordering make it suitable for automated grading.
