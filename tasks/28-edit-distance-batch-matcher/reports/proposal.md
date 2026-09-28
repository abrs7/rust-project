# Stage 0 proposal: Rebuild the edit distance batch matcher

Proposed slug: `edit-distance-batch-matcher`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 6 hours

Data quality tooling compares identifier lists from two shuffled CSV shards and must pair rows by minimum Levenshtein distance with deterministic tie-breaking when distances collide. The tool exports pairings, unmatched rows, and a summary manifest.

Failed runs exit nonzero without altering a previous successful output set. The verifier recomputes distances with the contract cost model, validates tie rules, and tests hidden lists with many equidistant candidates.

Dynamic programming at small scale; experts know the algorithm—the work is encoding ties and unmatched handling exactly.
