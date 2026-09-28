# Stage 0 proposal: Restore the expression evaluator

Proposed slug: `expression-evaluator`

Category: Software

Subcategory: Languages  

Estimated expert time: 8 hours

A spreadsheet-like language supports integers, rationals, variables, and nested functions listed in the contract. The evaluator must parse expressions, resolve variables from environment shards, and export reduced rational results plus AST dumps.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes evaluations independently, checks divide-by-zero failures, and tests hidden expressions with variable shadowing.

Small language implementations are common interview and tooling tasks; AST and rational output make grading objective.
