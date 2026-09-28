# Telemetry reconstruction API contract

Python 3.11+ and the standard library are the only runtime requirements.

## Command line

```text
python -m telemetry ingest FRAGMENTS CAMPAIGNS OUTPUT
python -m telemetry assemble CAMPAIGNS OUTPUT
python -m telemetry decode CAMPAIGNS OUTPUT
python -m telemetry fit-clock CAMPAIGNS OUTPUT
python -m telemetry calibrate REFERENCES OUTPUT
python -m telemetry reconcile REFERENCES OUTPUT
python -m telemetry export CAMPAIGNS REFERENCES OUTPUT
python -m telemetry run FRAGMENTS CAMPAIGNS REFERENCES OUTPUT
```

`ingest` is the only command that may enumerate or read `FRAGMENTS`. Later
commands read campaign/reference ledgers plus only their declared artifacts in
`output-schema.json`. `run` executes the same public stage functions in order in
a temporary directory, then atomically replaces the complete listed set.
Commands return zero on success and nonzero after printing one concise error to
stderr on failure.

## Public Python API

`telemetry.pipeline` exports:

```python
ingest(fragments: Path | str, campaigns: Path | str, output: Path | str) -> None
assemble(campaigns: Path | str, output: Path | str) -> None
decode(campaigns: Path | str, output: Path | str) -> None
fit_clock(campaigns: Path | str, output: Path | str) -> None
calibrate(references: Path | str, output: Path | str) -> None
reconcile(references: Path | str, output: Path | str) -> None
export(campaigns: Path | str, references: Path | str, output: Path | str) -> None
run(fragments: Path | str, campaigns: Path | str, references: Path | str, output: Path | str) -> None
```

`telemetry.exact.round_half_even(numerator, denominator) -> int` accepts an
integer numerator and positive integer denominator, including negative ties.

## Ledgers

`campaigns.csv` columns: `campaign_id,campaign`.
`references.csv` columns: `campaign,channel,reference_low,reference_mid,reference_high,reference_temperature_milli_c,temperature_coefficient`.

Identifiers are nonempty printable ASCII without leading or trailing
whitespace. Integers are canonical base-10 signed values in the int64 range.
Ledger decimals are canonical base-10 strings.

## Canonical products

JSON is UTF-8, sort-key ordered, indented by two spaces, and LF terminated.
JSONL is compact sort-key ordered JSON, one object per LF-terminated line.
Binary stream files are raw octets with no added header. No product contains
absolute paths, wall-clock times, fragment filenames, row numbers, random
values, or platform-dependent data.

Dialect names are recovered from the wire, not from the ledgers. Campaign names
come from `campaigns.csv` via the container campaign number.
