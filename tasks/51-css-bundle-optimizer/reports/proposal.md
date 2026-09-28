# Stage 0 proposal: Restore the CSS bundle optimizer

Proposed slug: `css-bundle-optimizer`

Category: Software

Subcategory: Frontend  

Estimated expert time: 6 hours

Stylesheets arrive as shuffled partials with variables and imports. The optimizer must flatten imports, resolve custom properties, deduplicate selectors by contract precedence, and emit a canonical CSS file plus an unused-rule report.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes flattened CSS bytes independently, checks import cycles that must fail, and tests hidden partials with conflicting custom properties.

Build-tool authors know this problem; graders enforce precedence exactly so shortcuts fail.
