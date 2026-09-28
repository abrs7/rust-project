# Stage 0 proposal: Recover the slow-changing dimension merger

Proposed slug: `scd-dimension-merger`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 10 hours

SCD type-2 history for synthetic customers lives in CSV shards with overlapping effective dates. The merger must close and open rows by contract rules, collapse exact duplicates, and export current and historical tables plus a change manifest.

Failed runs exit nonzero without altering a previous successful output set. The verifier recomputes histories independently, checks date boundary semantics, and tests hidden inputs with overlapping intervals that must error.

Dimensional modeling is standard BI work; experts know the patterns—precision in date logic is what makes it hard.
