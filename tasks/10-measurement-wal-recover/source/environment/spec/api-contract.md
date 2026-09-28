# WAL recovery API contract

Go 1.22 and the standard library are the only runtime requirements.

## Command line

Each command takes `CAMPAIGN OUTPUT`:

```text
walrecover ingest CAMPAIGN OUTPUT
walrecover scan CAMPAIGN OUTPUT
walrecover dedup CAMPAIGN OUTPUT
walrecover merge CAMPAIGN OUTPUT
walrecover validate CAMPAIGN OUTPUT
walrecover gap CAMPAIGN OUTPUT
walrecover export CAMPAIGN OUTPUT
walrecover run CAMPAIGN OUTPUT
```

`ingest` reads recorder metadata and all shard payloads into
`normalized-input.json`. Later commands read recorder metadata plus only their
declared artifacts in `output-schema.json`; they must not enumerate or read
`CAMPAIGN/shards`. `run` executes the public stage methods in order in a
temporary output directory, then atomically replaces all seven products.

## Public Go API

`walrecover` exposes:

```go
func Ingest(campaign, output string) error
func Scan(campaign, output string) error
func Dedupe(campaign, output string) error
func Merge(campaign, output string) error
func Validate(campaign, output string) error
func Gap(campaign, output string) error
func Export(campaign, output string) error
func Run(campaign, output string) error
```

`walrecover.FrameCRC(header []byte) uint32` returns CRC32-IEEE over the 24-byte
frame prefix (magic, sequence, timestamp, value).

## Campaign files

`recorder.toml` contains `schema_version`, `checksum`, `frame_magic`,
`max_gap_ns`, and `dedup_key`.

`shards.csv` columns: `shard_id,path`

Each WAL shard stores 28-byte frames:

* bytes 0-3: magic `MWAL`
* bytes 4-7: sequence (`uint32` big-endian)
* bytes 8-15: timestamp_ns (`uint64` big-endian)
* bytes 16-23: value (`int64` big-endian)
* bytes 24-27: CRC32-IEEE of bytes 0-23

## Canonical products

JSON is UTF-8, sort-key ordered, indented by two spaces, and LF terminated.
JSONL is compact sort-key ordered JSON, one object per LF-terminated line.
No product contains absolute paths, wall-clock times, random values, or
platform-dependent data.
