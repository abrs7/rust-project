# Stage 0 proposal: Fix the sitemap generator

Proposed slug: `sitemap-generator`

Category: Software

Subcategory: Frontend  

Estimated expert time: 4 hours

Marketing sites store route metadata in YAML shards with changefreq and priority fields. The generator must merge shards, resolve canonical URLs, drop duplicates by path, and write a sorted sitemap XML file plus a collision report.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes XML bytes independently, checks URL normalization, and tests hidden shards with trailing-slash conflicts.

Simple but real frontend infra; experts finish quickly if URL normalization rules are followed precisely.
