# Stage 0 proposal: Rebuild the data quality rules engine

Proposed slug: `data-quality-rules-engine`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 9 hours

Quality rules expressed in a small DSL must run over shuffled row batches, emitting violation records with row keys and rule IDs sorted canonically. The engine parses rules, evaluates predicates with null semantics from the contract, and writes summary counts.

Failed runs exit nonzero without altering a previous successful output set. Verification evaluates rules independently, compares violation bytes, and uses hidden batches with borderline null comparisons and conflicting rule priorities.

Rule engines appear in every warehouse; parsing plus null semantics supplies enough depth for a day’s work.
