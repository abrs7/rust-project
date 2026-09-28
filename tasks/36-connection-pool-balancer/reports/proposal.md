# Stage 0 proposal: Recover the connection pool balancer

Proposed slug: `connection-pool-balancer`

Category: Software

Subcategory: Databases  

Estimated expert time: 6 hours

A pool manager assigns database connections to waiting clients under max pool size, idle timeouts, and fairness rules documented in TOML campaigns. The solver rebuilds the allocator to produce assignment traces and final pool state dumps for each replay.

Failed runs exit nonzero without altering a previous successful output set. The verifier replays request logs independently, checks fairness tie-breaking, timeout eviction, and hidden logs with burst traffic and zero pool size errors.

Connection pooling is everyday backend work; the task tests precise replay semantics.
