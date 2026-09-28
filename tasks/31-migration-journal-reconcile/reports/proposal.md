# Stage 0 proposal: Reconcile the migration journal

Proposed slug: `migration-journal-reconcile`

Category: Software

Subcategory: Databases  

Estimated expert time: 10 hours

A Postgres-style migration runner crashed mid-deploy, leaving SQL journals, applied markers, and pending scripts in inconsistent shards. The solver rebuilds a reconciler that computes the exact apply order, detects split-brain markers, and exports a recovery plan plus normalized journal state. File order is arbitrary.

Failed runs exit nonzero without altering a previous successful output set. Verification independently derives apply order from markers, checks idempotency tokens, rejects conflicting checksums, and ensures failed analysis does not mutate prior successful exports. Hidden campaigns rename scripts and include forked marker histories.

Database operators handle this class of problem regularly; difficulty is multi-file consistency rather than exotic SQL.
