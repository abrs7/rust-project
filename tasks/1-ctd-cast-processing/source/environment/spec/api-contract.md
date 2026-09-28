# Ctdproc API contract

Python 3.11+ and the standard library are the only runtime requirements.

## Command line

Each command takes `CAMPAIGN OUTPUT`:

```text
python -m ctdproc ingest CAMPAIGN OUTPUT
python -m ctdproc split CAMPAIGN OUTPUT
python -m ctdproc depth CAMPAIGN OUTPUT
python -m ctdproc derive CAMPAIGN OUTPUT
python -m ctdproc bin CAMPAIGN OUTPUT
python -m ctdproc qc CAMPAIGN OUTPUT
python -m ctdproc export CAMPAIGN OUTPUT
python -m ctdproc run CAMPAIGN OUTPUT
```

`ingest` reads `cast.toml` and all profile shards under `profiles/`. Later
commands read `cast.toml` plus only their declared artifacts in
`output-schema.json`; they must not enumerate or read `CAMPAIGN/profiles`.
`run` executes the same public stage functions in order in a temporary output
directory, then atomically replaces all nine products. Commands return zero on
success and nonzero after printing one concise error to stderr on failure.

## Public Python API

`ctdproc.pipeline` exports:

```python
ingest(campaign: Path | str, output: Path | str) -> None
split(campaign: Path | str, output: Path | str) -> None
depth(campaign: Path | str, output: Path | str) -> None
derive(campaign: Path | str, output: Path | str) -> None
bin(campaign: Path | str, output: Path | str) -> None
qc(campaign: Path | str, output: Path | str) -> None
export(campaign: Path | str, output: Path | str) -> None
run(campaign: Path | str, output: Path | str) -> None
```

`ctdproc.exact.round_half_away(numerator, denominator) -> int` accepts an
integer numerator and positive integer denominator.

`ctdproc.exact.parse_rational(text) -> tuple[int, int]` parses reduced positive
`num/den` strings.

`ctdproc.exact.gravity_micro_ms2(lat_num, lat_den) -> tuple[int, int]` returns
`(g_num, g_den)` for the contract gravity formula in micro-metres per second
squared.

## Campaign files

`cast.toml` contains `schema_version`, `cast_id`, `latitude_deg` and
`bin_size_m` as reduced positive rational strings, and
`candidate_latitudes_deg` as a list of reduced positive rational strings.

Each `profiles/*.csv` row contains `time_s`, `pressure_dbar`, `temperature_c`,
and `conductivity_mS`. Values are canonical base-10 signed int64 scaled
integers; scales are fixed in `/app/spec/contract.json`.

Identifiers are nonempty printable ASCII without leading/trailing whitespace.
Every normalized sample receives a canonical `sample_id` of the form
`S000001`, ... in `(time_s, pressure_dbar, temperature_c, conductivity_mS)`
order.

## Canonical products

JSON is UTF-8, sort-key ordered, indented by two spaces, and LF terminated.
JSONL is compact sort-key ordered JSON, one object per LF-terminated line.
Array ordering and JSONL ordering are semantic and are specified by the
output schema. No product contains absolute paths, wall-clock times, shard
names, row numbers, random values, or platform-dependent data.

The inferred working latitude is recorded in `latitude-diagnosis.json`.
Every downcast `sample_id` appears exactly once across `depth-profile.jsonl`,
`derived-profile.jsonl`, and the discard counts in `provenance.json`.
