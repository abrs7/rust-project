# Stage 0 proposal: Recover the string suffix array builder

Proposed slug: `suffix-array-builder`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 8 hours

Bioinformatics tooling indexed synthetic reference strings split across fragments with duplicated substrings. The suffix array builder must concatenate fragments in manifest order, build a suffix array with stable lexicographic tie rules, and export rank tables. Fragment names are decoys.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes suffix arrays for moderate-length strings, checks rank invariants, and tests hidden references with repeated motifs. Memory limits fit the stated resource envelope using standard library structures only.

Experienced engineers who have worked with indexing can finish in a day; the task tests careful string handling rather than research-grade suffix array theory.
