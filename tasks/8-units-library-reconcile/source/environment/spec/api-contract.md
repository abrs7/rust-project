# Unitlib API contract

Java 21 and the standard library are the only runtime requirements.

## Command line

Each command takes `CAMPAIGN OUTPUT`:

```text
java -cp /app unitlib.Main ingest CAMPAIGN OUTPUT
java -cp /app unitlib.Main parse-units CAMPAIGN OUTPUT
java -cp /app unitlib.Main build-graph CAMPAIGN OUTPUT
java -cp /app unitlib.Main convert CAMPAIGN OUTPUT
java -cp /app unitlib.Main merge CAMPAIGN OUTPUT
java -cp /app unitlib.Main validate CAMPAIGN OUTPUT
java -cp /app unitlib.Main export CAMPAIGN OUTPUT
java -cp /app unitlib.Main run CAMPAIGN OUTPUT
```

`ingest` reads all campaign definitions and dataset shards. Later commands read
definitions plus only their declared artifacts in `output-schema.json`; they
must not enumerate or read `CAMPAIGN/datasets`. `run` executes the same public
stage functions in order in a temporary output directory, then atomically
replaces all nine products. Commands return zero on success and nonzero after
printing one concise error to stderr on failure.

## Public Java API

`unitlib.Pipeline` exposes static methods:

```java
void ingest(String campaign, String output);
void parseUnits(String campaign, String output);
void buildGraph(String campaign, String output);
void convert(String campaign, String output);
void merge(String campaign, String output);
void validate(String campaign, String output);
void exportStage(String campaign, String output);
void run(String campaign, String output);
```

`unitlib.Exact.roundHalfAway(long numerator, long denominator)` accepts a
positive integer denominator and returns the nearest integer with ties rounded
away from zero.

## Campaign files

`campaign.toml` contains `schema_version`, `si_system`, and `canonical_units`
mapping each nonempty convention group to a canonical `unit_id`.

CSV schemas are exact:

* `registry.csv`: `unit_id,symbol,dimension,si_factor,si_offset,convention_group`
* `conservation.csv`: `constraint_id,quantity,window_start,window_end,expected_sum_si,tolerance_si`
* each `datasets/*.csv`: `obs_id,source_id,timestamp,quantity,magnitude,unit_symbol`

Identifiers are nonempty printable ASCII without leading or trailing whitespace.
Rationals are canonical reduced `n/d` strings or base-10 integers. Empty
`convention_group` means the unit is not part of an alias family. Every
observation unit symbol must appear in the registry. Conservation windows are
inclusive on both bounds.

## Canonical products

JSON is UTF-8, sort-key ordered, indented by two spaces, and LF terminated.
JSONL is compact sort-key ordered JSON, one object per LF-terminated line.
Array ordering and JSONL ordering are semantic and are specified by the output
schema. No product contains absolute paths, wall-clock times, shard names, row
numbers, random values, or platform-dependent data.

Merged SI sums use exact rational arithmetic through conversion and merge.
Conservation validation fails the stage when any constraint is outside its
tolerance. An empty `rejections.jsonl` file is valid when no observation is
excluded.
