# Stage 0 proposal: Fix the B-tree page validator

Proposed slug: `btree-page-validator`

Category: Software

Subcategory: Databases  

Estimated expert time: 9 hours

An educational storage engine stores synthetic B-tree pages as binary shards. The validator must verify key order, child pointers, occupancy bounds, and free space accounting, then export a validation report and flattened key listing. Page order in the campaign is shuffled.

The verifier recomputes structural invariants independently, checks underflow detection, and tests hidden trees with intentional pointer corruption that must fail without altering prior reports.

Index structure validation is core database internals work; experts with storage background can complete it in about a day given explicit page layouts.
