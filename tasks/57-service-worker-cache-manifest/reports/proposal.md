# Stage 0 proposal: Fix the service worker cache manifest

Proposed slug: `service-worker-cache-manifest`

Category: Software

Subcategory: Frontend  

Estimated expert time: 5 hours

PWA assets are listed in JSON shards with cache busting hashes and route patterns. The manifest builder merges shards, applies pattern specificity rules, and writes a canonical precache list.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes merge results independently, checks specificity ties, and validates hidden shards with overlapping patterns.

Progressive web app caching is practical frontend systems work with clear gradable outputs.
