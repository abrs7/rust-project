# Stage 0 proposal: Restore the regex token parser

Proposed slug: `regex-token-parser`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 8 hours

A small pattern matcher supports a documented subset of regex syntax for log filtering. Its tokenizer and postfix converter were lost. The solver rebuilds parsing to emit token streams and syntax trees for valid patterns, with precise error locations for invalid ones.

Failed runs exit nonzero without altering a previous successful output set. The verifier compares token and tree bytes for visible and hidden patterns, including nested groups, escaped literals, and empty alternations that must fail. No full engine is required—only parse artifacts.

Parsing tasks reward careful grammar handling; an expert compiler-adjacent engineer can finish within a day given the bundled grammar tables.
