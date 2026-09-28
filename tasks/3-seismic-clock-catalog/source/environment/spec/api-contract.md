# Clockrecover API contract

Python 3.11+ and the standard library are the only runtime requirements.

## Command line

Each command takes `CAMPAIGN OUTPUT`:

```text
python -m clockrecover ingest CAMPAIGN OUTPUT
python -m clockrecover diagnose CAMPAIGN OUTPUT
python -m clockrecover catalogue CAMPAIGN OUTPUT
python -m clockrecover residuals CAMPAIGN OUTPUT
python -m clockrecover fit-clock CAMPAIGN OUTPUT
python -m clockrecover reconcile CAMPAIGN OUTPUT
python -m clockrecover export CAMPAIGN OUTPUT
python -m clockrecover run CAMPAIGN OUTPUT
```

`ingest` reads all campaign definitions and pick shards. Later commands read
definitions plus only their declared artifacts in `output-schema.json`; they
must not enumerate or read `CAMPAIGN/picks`. `run` executes the same public
stage functions in order in a temporary output directory, then atomically
replaces all nine products. Commands return zero on success and nonzero after
printing one concise error to stderr on failure.

## Public Python API

`clockrecover.pipeline` exports:

```python
ingest(campaign: Path | str, output: Path | str) -> None
diagnose(campaign: Path | str, output: Path | str) -> None
catalogue(campaign: Path | str, output: Path | str) -> None
residuals(campaign: Path | str, output: Path | str) -> None
fit_clock(campaign: Path | str, output: Path | str) -> None
reconcile(campaign: Path | str, output: Path | str) -> None
export(campaign: Path | str, output: Path | str) -> None
run(campaign: Path | str, output: Path | str) -> None
```

`clockrecover.exact.round_half_away(numerator, denominator) -> int` accepts an
integer numerator and positive integer denominator.

## Campaign files

`campaign.toml` contains `schema_version`, signed campaign bounds,
`min_stable_stations`, residual bounds, `allowed_rates` strings (`p/q` in
reduced positive form), and `candidate_boundaries_us`.

CSV schemas are exact:

* `stations.csv`: `station_id,name`
* `sources.csv`: `source_id,x_m,y_m,depth_m`
* `travel_times.csv`: `station_id,source_id,travel_us`
* `known_events.csv`: `event_id,source_id,origin_us`
* each `picks/*.csv`: `pick_id,station_id,recorded_us`

Identifiers are nonempty printable ASCII without leading/trailing whitespace.
All integers are canonical base-10 signed int64 values. Every station/source
pair must have one positive travel time. Known event IDs and
`(source_id,origin_us)` pairs are unique and inside campaign bounds.

## Canonical products

JSON is UTF-8, sort-key ordered, indented by two spaces, and LF terminated.
JSONL is compact sort-key ordered JSON, one object per LF-terminated line.
Array ordering and JSONL ordering are semantic and are specified by the
output schema. No product contains absolute paths, wall-clock times, shard
names, row numbers, random values, or platform-dependent data.

The stable catalogue assigns canonical IDs `EV000001`, ... in
`(origin_us,source_id)` order. Surveyed IDs are retained in `surveyed_ids`.
Every normalized pick ID occurs exactly once in either
`corrected-assignments.jsonl` or `rejections.jsonl`.
