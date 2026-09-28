# Stage 0 proposal: Repair the design token compiler

Proposed slug: `design-token-compiler`

Category: Software

Subcategory: Frontend  

Estimated expert time: 6 hours

Design tokens live in JSON with alias references and math expressions using rational numbers. The compiler resolves aliases, evaluates expressions, and exports flattened token files for color, spacing, and typography scales.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes token values independently, detects alias cycles, and uses hidden tokens with division rounding traps.

Design ops teams use token pipelines; exact rational math makes naive float shortcuts fail grading.
