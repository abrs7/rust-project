# Long horizon design: 8-units-library-reconcile

Target: median **>80** assistant turns at Stage 2.

## Forcing exploration

- Seven stages; merge/validate cannot reread raw dataset shards.
- Sparse examples only — no unit conversion cheat sheet.
- Two conventions for the same symbol (`lbf`/`lb_f`, `cal`/`calorie`) across sources.
- Conservation constraints fail unless conversions use the correct convention map.
- Hidden campaigns swap which source uses which convention.

## Estimated solver path

1. Registry + shard ingestion (~15 turns)
2. Parse unit strings into base dimensions (~15 turns)
3. Build conversion graph with missing edges (~20 turns)
4. Convert each dataset to SI (~15 turns)
5. Merge + conservation validation (~20 turns)
6. Hidden convention trap debugging (~25 turns)

**Total:** ~110 turns with failed runs.
