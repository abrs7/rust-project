# Stage 0 proposal: Recover the markdown static site builder

Proposed slug: `markdown-static-site-builder`

Category: Software

Subcategory: Frontend  

Estimated expert time: 8 hours

Markdown posts and layout templates must compile into HTML pages with front matter parsing, relative link rewriting, and deterministic asset hashing. The builder was partially deleted.

Failed runs exit nonzero without altering a previous successful output set. The verifier compares generated HTML bytes, checks link targets, missing template errors, and hidden posts with ambiguous front matter keys.

Static site generators are familiar; challenge is canonical HTML and link rewriting without a browser.
