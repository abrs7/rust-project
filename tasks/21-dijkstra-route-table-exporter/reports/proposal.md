# Stage 0 proposal: Reconstruct the Dijkstra route table exporter

Proposed slug: `dijkstra-route-table-exporter`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 6 hours

A network planning tool must read weighted directed graphs from edge list shards, collapse parallel edges by minimum weight, run shortest-path tree construction from a declared root, and export route tables with tie-broken next hops. Shard order and node naming are arbitrary.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes distances and next hops with the same tie rules, checks unreachable node handling, and validates hidden graphs with negative-weight traps that must be rejected. Outputs must be byte-identical across shuffled edge files.

Classic graph algorithms appear in many codebases; an algorithms-minded engineer can implement this in a few hours given explicit tie-breaking contracts.
