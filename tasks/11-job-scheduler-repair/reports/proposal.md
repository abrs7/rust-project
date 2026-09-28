# Stage 0 proposal: Fix the broken job scheduler

Proposed slug: `job-scheduler-repair`

Category: Software

Subcategory: Systems  

Estimated expert time: 6 hours

A batch platform lost its cron-style scheduler after a config migration. The solver rebuilds a Python package that reads a synthetic campaign of job definitions, dependency edges, and named resource pools with integer concurrency limits, then writes a deterministic execution plan. Scheduling is a fixed list policy defined entirely in the bundled contract and examples—not an optimization problem. Each job has an integer duration in minutes, an integer priority, and per-pool slot requirements. At each minute, ready jobs (all predecessors finished) are considered in descending priority, then ascending job ID; a job starts at the earliest minute where every required pool has a free slot, and finishes at start plus duration. The plan exports each job's start minute, assigned pools, parallelism groups for jobs sharing a start minute, and a provenance manifest in canonical JSON.

If the dependency graph contains a cycle, the run exits nonzero, records the cyclic job IDs in lexicographic order, and leaves any previous successful output directory byte-identical. Malformed definitions, unknown pools, negative durations, and references to missing jobs must fail the same way. Verification recomputes the schedule independently from the contract formulas, compares exact product bytes on visible and hidden campaigns with renamed IDs and tighter pool limits, and requires byte-identical reruns when definition shards are reshuffled or reordered. The six-hour estimate covers implementing the policy, resource accounting, cycle detection, and atomic output replacement; difficulty comes from keeping all of those semantics aligned under arbitrary input order, not from inventing heuristics.
