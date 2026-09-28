# Stage 0 proposal: Repair the rate limiter config compiler

Proposed slug: `rate-limiter-config-compiler`

Category: Software

Subcategory: Systems  

Estimated expert time: 7 hours

An edge proxy reads human-authored limit rules that compile into JSON policy bundles. The compiler was partially overwritten during a refactor. The solver restores compilation of token-bucket and fixed-window rules, including precedence when paths overlap, and emits compiled policy plus diagnostics.

Failed runs exit nonzero without altering a previous successful output set. The verifier independently compiles rules, compares bundle bytes, and tests hidden campaigns with overlapping prefixes, zero burst values, and invalid durations that must fail cleanly.

Rate limiting is common infrastructure; the task difficulty is expressing precedence and window math precisely enough for byte-level grading.
