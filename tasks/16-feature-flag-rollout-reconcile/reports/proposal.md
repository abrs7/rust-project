# Stage 0 proposal: Reconcile the feature flag rollout state

Proposed slug: `feature-flag-rollout-reconcile`

Category: Software

Subcategory: Systems

Estimated expert time: 11 hours

---

## Submission text

Release engineering lost the reconciler that turns flag definitions and evaluation logs into effective rollout state, and the solver rebuilds the Python (stdlib-only) package that processes a synthetic campaign. Definitions shard lists flag_key, integer version, default_enabled boolean, and audience rules: each rule has environment name, integer priority, enabled boolean, and a predicate as AND of clauses; each clause is OR of conditions field op value where field is user attribute from the registry, op is one of eq ne lt le gt ge in, and value is string or sorted string list for in. Evaluation logs shard rows: timestamp UTC seconds, environment, flag_key, user_id, observed_enabled boolean. User registry shard maps user_id to attribute JSON objects. Row and shard order are meaningless; duplicate log rows identical in all fields collapse to one keeping the row from the lexicographically smaller shard path.

Effective state is a fixed policy, not ML. For each environment and flag_key present in definitions, take the highest-priority rule whose environment matches and whose predicate matches the user from the latest log row for that triple (timestamp, user, env, flag_key); if none match, use default_enabled. Stale flags have definition version strictly greater than the maximum version seen in any evaluation log row for that flag_key and environment, or no log rows while version exceeds zero. rollout.json lists environments sorted, then flag_key sorted, each entry: effective_enabled bool, winning_rule_priority or null, stale bool, definition_version int. stale_flags.jsonl lists stale entries sorted by environment then flag_key. manifest.json SHA-256 covers all shards and outputs with canonical JSON: UTF-8, sorted keys, separators , and : without spaces, booleans and integers typed, one trailing newline; stale_flags.jsonl one object per line with the same serialization.

Any invalid campaign exits 2, writes a canonical JSON diagnostic to the separate report path, and leaves any previous output directory byte-identical. Invalid means duplicate flag_key within same definition version group, unknown op, in with empty list, evaluation referencing unknown user_id, or conflicting definition versions for same flag_key without strictly increasing version handling (two rows same flag_key different version both marked current). Verification recomputes effective flags with an independent reference, compares exact bytes on visible and hidden campaigns with renamed keys, overlapping priorities resolved by higher priority only, empty audiences, stale detection with partial logs, and in clauses on multi-value attributes. It requires identical output after log reshuffle and checks atomic replacement after success. The eleven-hour estimate reflects predicate evaluation, latest-log selection, priority ties, and stale logic interacting; one wrong winner changes rollout.json bytes for every dependent flag.
