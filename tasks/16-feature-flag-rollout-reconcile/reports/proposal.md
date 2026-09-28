# Stage 0 proposal: Reconcile the feature flag rollout state

Proposed slug: `feature-flag-rollout-reconcile`

Category: Software

Subcategory: Systems  

Estimated expert time: 6 hours

Release engineering stored flag definitions, audience rules, and observed evaluation logs in CSV shards after a partial export. The solver rebuilds a reconciler that computes effective flag states per environment, flags stale definitions, and exports a canonical rollout snapshot. Row and file order carry no meaning.

The verifier recomputes effective states, checks audience matching, stale detection, and byte-identical outputs on reshuffled logs. Hidden fixtures add conflicting rules, empty audiences, and environments missing from the registry that must error without clobbering prior snapshots.

Feature-flag reconciliation is everyday platform work; the task is hard because several independent rules interact and must be graded exactly.
