# Stage 0 proposal: Restore the materialized view refresher

Proposed slug: `materialized-view-refresher`

Category: Software

Subcategory: Databases  

Estimated expert time: 9 hours

Materialized view definitions and change feeds arrive as CSV shards. The refresher computes incremental updates using timestamp windows and primary-key upserts, then exports refreshed view rows and a refresh manifest. Feed order is meaningless until normalized.

Failed runs exit nonzero without altering a previous successful output set. The verifier recomputes view contents independently, checks window boundaries, duplicate keys, and hidden feeds with out-of-order timestamps.

Incremental view maintenance is realistic warehouse work; difficulty is combining normalization, upsert semantics, and deterministic export.
