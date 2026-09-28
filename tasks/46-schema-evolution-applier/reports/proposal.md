# Stage 0 proposal: Restore the schema evolution applier

Proposed slug: `schema-evolution-applier`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 8 hours

Event streams ship with embedded schema version markers and companion evolution scripts. The applier must choose the correct script chain, upgrade row shapes, and export upgraded events plus an evolution log. Order of files is decoy data.

Failed runs exit nonzero without altering a previous successful output set. The verifier replays evolution independently, checks incompatible skips, and uses hidden streams requiring multi-hop upgrades.

Schema evolution pipelines reward careful versioning; synthetic fixtures keep the task self-contained.
