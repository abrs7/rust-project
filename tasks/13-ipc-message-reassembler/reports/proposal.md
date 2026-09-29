# Stage 0 proposal: Restore the IPC message reassembler

Proposed slug: `ipc-message-reassembler`

Category: Software

Subcategory: Systems

Estimated expert time: 11 hours

---

## Submission text

A broker upgrade left fragmented binary messages in sharded capture files, and the solver rebuilds the Python (stdlib-only) package that reassembles them into ordered streams. Each capture shard holds zero or more frames: magic bytes IPC1, session_id as 16 raw bytes, sequence u64 big-endian, fragment_index u16 BE, fragment_count u16 BE, payload_length u32 BE, CRC-32/IEEE over bytes from session_id through payload, then payload. Frame order within a shard and shard file names are meaningless. Duplicate frames share the same session_id, sequence, and fragment_index; the survivor is the one from the lexicographically smaller shard path, then the smaller byte offset within that shard.

Reassembly is a fixed policy, not heuristics. For each (session_id, sequence), if all fragment_index values 0 through fragment_count-1 are present after duplicate resolution, payloads concatenate in index order into one message. CRC failures exclude the frame and list session_id hex, sequence, and fragment_index in rejections.jsonl. Incomplete groups after scanning all shards produce no message; missing indices appear as gap records in gaps.jsonl with session_id hex, sequence, first_missing_index, last_missing_index inclusive. Complete messages sort by session_id hex ascending, then sequence ascending. messages.jsonl holds one canonical JSON object per message: session_id hex, sequence, payload_base64 (standard alphabet, no padding), payload_sha256 hex. gaps.jsonl and rejections.jsonl use the same canonical JSON line format. manifest.json records SHA-256 of every input shard and output file with the global canonical JSON rules: UTF-8, sorted keys, separators , and : without spaces, one trailing newline on JSON files.

Any invalid campaign exits 2, writes a canonical JSON diagnostic to the separate report path, and leaves any previous output directory byte-identical. Invalid means bad magic, fragment_index >= fragment_count, fragment_count zero, payload_length exceeding the campaign max_bytes, or a shard unreadable as frames. Empty capture (no frames) is valid and yields empty messages.jsonl. Verification recomputes assembly with an independent reference parser, compares exact bytes on visible and hidden campaigns with torn counts, overlapping duplicates from different shards, CRC errors mixed with valid frames, and multi-session interleaving. It requires identical output after shard reshuffle and checks atomic replacement after a successful run. The eleven-hour estimate reflects binary parsing, duplicate tie-breaking, gap detection, and base64-canonical output interacting; a single wrong survivor choice changes message order and breaks byte comparison.
