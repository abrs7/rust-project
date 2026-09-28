# Ingestrepair API contract

Java 21 and the JDK standard library are the only runtime requirements.

## Command line

Each command takes `CAMPAIGN OUTPUT`:

```text
java -cp /app/ingestrepair ingestrepair.Main ingest CAMPAIGN OUTPUT
java -cp /app/ingestrepair ingestrepair.Main offsets CAMPAIGN OUTPUT
java -cp /app/ingestrepair ingestrepair.Main dedup CAMPAIGN OUTPUT
java -cp /app/ingestrepair ingestrepair.Main assign CAMPAIGN OUTPUT
java -cp /app/ingestrepair ingestrepair.Main aggregate CAMPAIGN OUTPUT
java -cp /app/ingestrepair ingestrepair.Main reconcile CAMPAIGN OUTPUT
java -cp /app/ingestrepair ingestrepair.Main export CAMPAIGN OUTPUT
java -cp /app/ingestrepair ingestrepair.Main run CAMPAIGN OUTPUT
```

`ingest` reads all campaign definitions and message shards. Later commands read
definitions plus only their declared artifacts in `output-schema.json`; they
must not enumerate or read `CAMPAIGN/shards`. `run` executes the same public
stage methods in order in a temporary output directory, then atomically
replaces all nine products. Commands return zero on success and nonzero after
printing one concise error to stderr on failure.

## Public Java API

`ingestrepair.Pipeline` exposes:

```java
void ingest(String campaign, String output);
void offsets(String campaign, String output);
void dedup(String campaign, String output);
void assign(String campaign, String output);
void aggregate(String campaign, String output);
void reconcile(String campaign, String output);
void export(String campaign, String output);
void run(String campaign, String output);
```

`ingestrepair.Exact.payloadHash(String compactPayload)` returns the lowercase
hex SHA-256 digest of the UTF-8 compact payload text.

## Campaign files

`consumer.toml` contains `schema_version`, `offset_semantics`, and
`dedup_identity`.

CSV schemas are exact:

* `topics.csv`: `topic,partition_count`
* each `shards/*.csv`: `topic,partition,offset,payload_hash,payload`

Each `committed/*.jsonl` line is a JSON object with `snapshot_id`, `topic`,
`partition`, `committed_offset`, and `captured_at_ms`.

`producer-ledger.jsonl` rows contain `topic`, `partition`, `key`, `max_seq`,
and `expected_count`. `broken-aggregates.jsonl` rows contain `topic`,
`partition`, `key`, and `count`.

Payload JSON objects contain `key` (identifier), `seq` (positive int64), and
`reading` (number). `payload_hash` must equal
`Exact.payloadHash(compact(payload))` using compact JSON with sorted keys and
no spaces. Identifiers are nonempty printable ASCII without leading or
trailing whitespace. All integers are canonical base-10 signed int64 values.

## Canonical products

JSON is UTF-8, sort-key ordered, indented by two spaces, and LF terminated.
JSONL is compact sort-key ordered JSON, one object per LF-terminated line.
Array ordering and JSONL ordering are semantic and are specified by the
output schema. No product contains absolute paths, wall-clock times, shard
names, row numbers, random values, or platform-dependent data.

Accepted messages receive canonical IDs `M000001`, ... in
`(topic,partition,offset,payload_hash)` order. Every input message ID occurs
exactly once in either accepted assignments or `rejections.jsonl`.
