# Stage 0 proposal: Restore the query plan serializer

Proposed slug: `query-plan-serializer`

Category: Software

Subcategory: Databases  

Estimated expert time: 8 hours

An optimizer emits intermediate plan trees as JSON fragments split across files. The serializer must merge fragments, resolve node IDs, topologically sort operators, and write a canonical plan document plus cost summary using rational arithmetic from the contract.

Failed runs exit nonzero without altering a previous successful output set. Verification rebuilds plans from fragments, compares serialized bytes, and uses hidden plans with duplicate IDs and missing roots that must error cleanly.

Query-plan tooling is familiar to database engineers; challenge lies in canonical JSON and ID resolution rules.
