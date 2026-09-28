# Stage 0 proposal: Fix the HTML form accessibility report

Proposed slug: `html-form-accessibility-report`

Category: Software

Subcategory: Frontend  

Estimated expert time: 5 hours

A static multi-page form bundle ships without its accessibility checker. The tool must parse HTML fragments, evaluate label associations, tabindex order, and ARIA role rules from the bundled spec, and export violation lists with line references.

The verifier compares violation sets independently, checks hidden pages with duplicate IDs and missing labels, and rejects malformed HTML without altering prior reports.

Frontend engineers regularly run a11y audits; this packages common checks into deterministic output.
