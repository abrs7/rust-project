# Stage 0 proposal: Restore the JSX import graph linter

Proposed slug: `jsx-import-graph-linter`

Category: Software

Subcategory: Frontend  

Estimated expert time: 7 hours

A monorepo exports a shuffled list of synthetic JSX modules with import statements. The linter must detect unused imports, circular dependencies, and forbidden cross-package imports per a rules table, exporting violations in canonical order.

Failed runs exit nonzero without altering a previous successful output set. The verifier rebuilds import graphs independently and tests hidden modules with re-export cycles and alias paths.

Frontend platform linting is everyday work; graph analysis supplies enough depth for automated verification.
