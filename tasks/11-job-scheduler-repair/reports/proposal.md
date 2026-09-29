# Stage 0 proposal: Fix the broken job scheduler

Proposed slug: `job-scheduler-repair`

Category: Software

Subcategory: Systems

Estimated expert time: 12 hours

Revision: 3 — accepted pattern (self-contained, exact-byte, interacting semantics)

---

## Submission text

A batch platform's cron-style scheduler stopped producing usable plans after a config migration, and the solver rebuilds the Python (stdlib-only) package that turns a synthetic campaign into a deterministic execution plan. A campaign holds job definitions, dependency edges, resource pools with integer base capacities and dated maintenance windows that lower capacity, a planning horizon, and a list of UTC offset transitions for the site's local time. Each job has a five-field cron expression (*, lists, ranges, steps; when both day-of-month and day-of-week are restricted, a minute matches if either field matches), an integer duration of at least one minute, an integer priority, and per-pool slot needs. Nominal fire times are evaluated in local wall time: a local minute skipped by a forward offset jump fires once at the first valid minute after the gap, and a local minute repeated by a backward jump fires only on its first occurrence. An occurrence of job B depends, for each predecessor A, on the latest occurrence of A whose nominal time is at or before B's; if A has none, that edge is satisfied. Occurrences of the same job never overlap.

Scheduling is a fixed list policy defined in the bundled contract, not an optimization problem. Time advances in whole UTC minutes from the horizon start. At each minute, occurrences finishing at that minute release their slots first. Every ready occurrence (nominal time reached, all dependency occurrences and the job's previous occurrence finished) is then considered once, in descending priority, then ascending nominal time, then ascending job ID. An occurrence starts if every required pool has enough free slots for every minute of [start, start + duration) under the maintenance-reduced capacity; each start claims its slots immediately. An occurrence that does not fit stays ready, and lower-ranked occurrences may still start that minute. Occurrences not started before the horizon ends are reported as unscheduled. The run writes plan.json (each occurrence's job ID, nominal time, start, finish, and pools, ordered by start, then job ID, then nominal time), groups.json (occurrences sharing a start minute), and manifest.json (SHA-256 of every input shard and output file). All three use canonical JSON: UTF-8, keys sorted, separators , and : with no spaces, integers only, non-ASCII kept unescaped, one trailing newline.

Any invalid campaign makes the run exit 2, write a canonical JSON diagnostic to the separate report path given on the command line, and leave any previous output directory byte-identical. Invalid means a malformed or out-of-range cron field, a duplicate job ID, an unknown pool, a slot need above a pool's base capacity, a non-positive duration, an edge naming a missing job, or a dependency cycle. Duplicate identical edges are collapsed, not rejected. For cycles, the diagnostic lists every strongly connected component with more than one job or with a self-edge, with IDs sorted lexicographically within each component and components ordered by their first ID. Verification recomputes every plan with an independent reference implementation of the contract. It compares exact bytes on visible and hidden campaigns that use renamed IDs, tighter pools, offset transitions inside the horizon, and overlapping maintenance windows. It requires identical output after input shards are reshuffled and reordered, and it checks atomic replacement by running invalid campaigns after a successful run. The twelve-hour estimate reflects the interacting semantics: cron expansion across offset transitions, occurrence-level dependency matching, time-varying capacity, and per-job non-overlap. Any one rule applied slightly wrong shifts later starts and breaks exact-byte comparison.
