# Stage 0 proposal: Restore the convex hull exporter

Proposed slug: `convex-hull-exporter`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 7 hours

A CAD preprocessor collected 2-D point clouds from CSV shards with duplicate and collinear points. The hull builder must deduplicate by contract rules, emit vertices in counterclockwise order starting from the lowest-left point, and write area and perimeter as reduced fractions.

Failed runs exit nonzero without altering a previous successful output set. The verifier recomputes hulls independently, checks collinear handling, empty inputs, and hidden clouds with many duplicates on one line.

Computational geometry basics; experts can implement Graham scan or monotone chain within hours given exact tie rules in the spec.
