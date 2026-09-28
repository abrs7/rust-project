# Stage 0 proposal: Fix the metric rollup compiler

Proposed slug: `metric-rollup-compiler`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 7 hours

Raw counter shards must roll up to hourly and daily aggregates using explicit timezone-neutral bucketing and max/last/sum policies per metric name. The compiler writes rollup tables and a policy manifest.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes buckets independently, checks policy selection, and validates hidden metrics with irregular sampling intervals.

Metrics rollups are everyday observability tasks; graders focus on bucket boundaries and policy maps.
