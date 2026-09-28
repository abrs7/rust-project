# Stage 0 proposal: Repair the union-find connectivity reporter

Proposed slug: `union-find-connectivity-reporter`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 5 hours

Incident response grouped hosts into connectivity components from undirected edge shards with lexicographic component IDs required in output. The union-find implementation must use union-by-rank and path compression while still emitting components in the contract’s canonical order.

Failed runs exit nonzero without altering a previous successful output set. Verification rebuilds components independently, checks canonical IDs, rejects self-loops where forbidden, and validates hidden graphs with star and chain topologies.

Standard disjoint-set work; moderate difficulty comes from output ordering requirements, not from the core algorithm.
