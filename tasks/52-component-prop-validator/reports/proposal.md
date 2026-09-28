# Stage 0 proposal: Rebuild the component prop validator

Proposed slug: `component-prop-validator`

Category: Software

Subcategory: Frontend  

Estimated expert time: 7 hours

A design system ships JSON component schemas and example usage files. The validator checks required props, enum values, and mutually exclusive prop groups, exporting diagnostics sorted by component and prop name.

Failed runs exit nonzero without altering a previous successful output set. The verifier evaluates schemas independently, checks hidden examples with subtle mutual exclusion violations, and ensures failed runs do not mutate prior diagnostics.

Design-system tooling is common in frontend platform teams; difficulty is exhaustive rule coverage, not UI rendering.
