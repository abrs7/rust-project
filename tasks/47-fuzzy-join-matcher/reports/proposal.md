# Stage 0 proposal: Rebuild the fuzzy join matcher

Proposed slug: `fuzzy-join-matcher`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 9 hours

Two shuffled entity tables must join on composite keys with optional phonetic normalization rules from the contract. The matcher exports paired rows, unmatched lists, and similarity scores as reduced fractions.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes joins and scores independently, checks normalization tables, and tests hidden tables with symmetric ties broken lexicographically.

Record linkage shows up in real pipelines; difficulty is exact normalization and tie-breaking, not ML.
