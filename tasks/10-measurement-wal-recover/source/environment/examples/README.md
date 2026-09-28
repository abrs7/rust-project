# Worked WAL examples

This directory holds tiny illustrations only. It is not a complete solution.

## CRC failure

A frame with a valid header but an incorrect CRC32 must appear in
`frame-index.jsonl` with `"crc_ok": false` and in `dedup-manifest.jsonl` with
`"status": "rejected_crc"`.

## Duplicate sequence

Two CRC-valid frames with the same sequence number must leave exactly one
accepted frame: the one with the lexicographically smallest
`(shard_id, byte_offset)`.
