# Stage 0 proposal: Fix the topological sort builder

Proposed slug: `topological-sort-builder`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 5 hours

Build pipelines express task dependencies as shuffled edge lists with optional soft dependencies that may be ignored when flagged. The solver rebuilds a sorter that emits a canonical build order, cycle diagnostics, and a manifest of skipped soft edges. Nothing in node labels reveals layers.

Failed runs exit nonzero without altering a previous successful output set. Verification independently topologically sorts with the same soft-edge rules, rejects cycles with stable reporting, and checks byte-identical orders on renamed nodes. Hidden graphs introduce cycle/near-cycle combinations.

Standard CI dependency resolution; experts solve it quickly if they read the soft-edge contract carefully.
