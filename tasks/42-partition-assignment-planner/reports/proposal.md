# Stage 0 proposal: Restore the partition assignment planner

Proposed slug: `partition-assignment-planner`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 6 hours

Kafka-style topics arrive with partition counts, key hash rules, and consumer group members. The planner assigns partitions to members for balanced load with deterministic tie-breaking when weights equal.

Failed runs exit nonzero without altering a previous successful output set. The verifier recomputes assignments independently, checks balance metrics, unknown topic rejection, and hidden groups with uneven member capacities.

Partition assignment is familiar to streaming engineers; the task is bounded and fully synthetic.
