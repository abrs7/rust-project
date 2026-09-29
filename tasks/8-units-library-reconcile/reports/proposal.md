# Stage 0 proposal: Units Library Repair

Proposed slug: `units-library-reconcile`

Category: Science

Subcategory: chemistry

Implementation language: Java 21 standard library

Estimated expert time: 12 hours

---

## Submission text

A measurement campaign merged observations from several instruments, each reporting a magnitude and a unit symbol. The solver is given a unit registry with conversion factors and offsets as exact rationals, a set of conservation constraints the merged series must satisfy, and shuffled CSV shards of observations from the different instruments. The registry lists alias groups where the same physical unit is spelled more than one way, and the spellings are not equivalent across every instrument: at least one source uses a convention that differs from the registry's default, and nothing in the data records which source that is. Rebuild the Java 21 package `/app/unitlib` so `/app/output/` holds nine canonical JSON products from those CSV inputs: `converted-observations.jsonl` (SI-normalised observations), `convention-map.json` (the convention each source was actually using within each alias group), `merged-series.jsonl` (merged series by quantity and timestamp), `conservation-report.json`, `rejections.jsonl` (disposition for every rejected input row including unparseable units), plus `normalized-input.json`, `parsed-units.json`, `conversion-graph.json`, and `provenance.json` defined in `/app/spec/output-schema.json`. Shard names, row order, and identifiers carry no source or convention meaning.

Fixed policies, not heuristics: each row's unit symbol must resolve through the registry; within a convention group, `campaign.toml` `canonical_units` names the canonical `unit_id` for that group and `convention-map.json` lists which `source_id` values appear with which alias symbols. SI magnitudes use exact reduced rationals with `si_magnitude = magnitude * si_factor + si_offset`; apply `roundHalfAway` only where the API contract requires integer rounding, with ties away from zero including negative ties. Merged series sum converted SI magnitudes by timestamp and quantity; conservation compares those sums to each rule's tolerance. Exact duplicate rows collapse; conflicting duplicates on the same identifier reject the run rather than merge. JSON is UTF-8, sort-key ordered, two-space indent for JSON objects, compact JSONL, LF terminated, no paths in products.

The verifier compares against frozen values computed from the generator's own parameters, independently of the reference solution. It checks the convention assigned to each source group; per-row SI magnitudes as exact reduced fractions; merged series values; conservation report entries; and each rejected row's disposition and reason. Duplicate rows must be collapsed and conflicting identifiers rejected rather than merged. Two runs must produce byte-identical output. Hidden campaigns vary the seed, which sources use which convention, the registry's alias groups and factors, instrument and quantity counts, and the placement of unparseable rows; visible campaigns exhibit every behaviour at least once. Empty output, a constant series, a solution that applies the registry default to every source without group resolution, and one that resolves aliases per row instead of per source all score zero.

The difficulty is that the wrong alias convention produces per-row magnitudes that are entirely plausible — right order of magnitude, right sign, nothing malformed — and only the merged series betrays it, because quantities that must sum to a conserved total come up short by a consistent factor on the affected source alone. The convention cannot be read from any field; it has to be inferred from which assignment makes the conservation constraints close, and offset-carrying units make that assignment order-dependent rather than a simple scale test. This is the first thing that goes wrong when instrument feeds from different vendors are merged, and the conservation law is how a metrology group catches it. A working reference solution uses Java 21 and the standard library only; someone who has merged multi-instrument datasets should need about twelve hours.
