# Iteration 002 verifier plan

Grade the staged `telemetry` package, not `rebuild.py`. Freeze all nine
products plus `streams/{campaign}.bin` for visible and hidden collections.

Do not import the Oracle. Do not put fragment magic, sync words, whitening,
Fletcher/CRC/BLAKE, quoting, or payload layouts in `tests/`.

## Artifact set

Named files: `fragment-index.jsonl`, `assembly.json`, `decoded-records.jsonl`,
`clock-models.json`, `calibration.json`, `records.jsonl`, `observations.jsonl`,
`manifest.json`, `provenance.json`.

Stream binaries: `streams/{campaign}.bin` for every recovered campaign.
Successful `run` leaves exactly those nine names plus `streams/`. Unlisted
paths such as `stale.txt` must remain.

JSON is indent-2, sort-key ordered, LF. JSONL is compact sort-key ordered.

## Isolation

`ingest` is the only command that may read fragments. After ingest, delete or
replace the fragment directory, then run assemble through export. Byte-compare
staged CLI, staged API, and `run`. Decoy fragments after ingest must not
change later products.

## Independent invariants

Rebuild streams from `fragment-index.jsonl` payload hex only. Unwrap ticks
from `decoded-records.jsonl` in stream order. Fit quadratics from ledger
references and product raw points with `fractions.Fraction`. Evaluate
observations from unrounded coefficients. Recompute provenance SHA-256 from
the declared product object.

## Negative contracts

Missing/malformed ledgers, empty fragments, missing stage requirements,
poisoned index/clock/duplicates, and unwritable output must exit nonzero and
leave a previous successful set, including stream binaries, unchanged.

## Attacks

NOP, reject-everything, visible-constant dump, five-file 001 dump, example-hex
copy, and post-ingest fragment reread must score 0.
