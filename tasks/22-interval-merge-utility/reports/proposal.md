# Stage 0 proposal: Restore the interval merge utility

Proposed slug: `interval-merge-utility`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 4 hours

Calendar sync exported busy intervals from multiple sources as overlapping ranges with inclusive/exclusive boundary conventions mixed together. The utility must normalize boundaries, merge overlaps, subtract exceptions, and write a canonical free-busy timeline. Source order is meaningless.

Failed runs exit nonzero without altering a previous successful output set. The verifier recomputes merged intervals, checks boundary semantics, empty results, and invalid range rejection. Hidden fixtures vary timezone-neutral timestamps and nested exceptions.
