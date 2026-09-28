# Stage 0 proposal: Repair the checkpoint manifest validator

Proposed slug: `checkpoint-manifest-validator`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 6 hours

Spark-style job checkpoints list partial RDD manifests across shards. The validator verifies hash chains, missing parts, and lineage completeness, then exports a consolidated manifest or a structured error report.

The verifier rebuilds hash chains independently, detects broken lineage, and ensures failed validation preserves prior good manifests.

Checkpoint validation is practical batch-processing hygiene; experts can finish in an afternoon.
