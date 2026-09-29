# Stage 0 proposal: Rebuild the log rotation tool

Proposed slug: `log-rotation-rebuild`

Category: Software

Subcategory: Systems

Estimated expert time: 10 hours

---

## Submission text

Operations lost a log-rotation utility after a migration, and the solver rebuilds the Python (stdlib-only) package that applies retention policies to synthetic log trees described entirely in the campaign. Each tree lists log files with path, byte content (UTF-8 or raw bytes flagged as binary), a boolean writer_open flag, and a synthetic mtime as Unix seconds UTC. Policies name a tree root prefix, max_size_bytes, max_age_seconds, keep_count (at least one), and compress_after (rotate generation at or above this number is gzip-compressed). Shard order and file names carry no meaning; duplicate paths after normalization are invalid.

Rotation is a fixed policy, not an optimization. For each policy-matched file in lexicographic path order, if writer_open is true the file is never truncated or deleted; only archived copies rotate. Otherwise, if size exceeds max_size_bytes or age exceeds max_age_seconds, the tool rotates at the last complete line boundary (last byte of content must be newline for text files; binary files rotate only at exact size boundary when over limit). Partial final lines without trailing newline defer rotation and record reason deferred_partial_line. A rotation renames existing archives log.ext.N to log.ext.N+1 (highest dropped when keep_count exceeded), then moves the active log to .1, optionally gzip-compressing when 1 >= compress_after. Archive names are {path}.{N} or {path}.{N}.gz with no gaps. The run writes report.json (per-file action: none, rotated, deferred, or skipped_writer with reason), inventory.jsonl (one object per surviving file: path, size, generation, compressed bool, sha256 hex), and manifest.json (SHA-256 of every input shard and output file). All use canonical JSON: UTF-8, keys sorted, separators , and : with no spaces, integers and booleans only where typed, one trailing newline; inventory.jsonl uses the same object serialization per line.

Any invalid campaign exits 2, writes a canonical JSON diagnostic to the separate report path on the command line, and leaves any previous output directory byte-identical. Invalid means duplicate normalized paths, keep_count zero, negative limits, compress_after zero, unknown tree root, a symlink entry in the tree manifest, or a policy whose root is not a prefix of any file. Verification recomputes rotations with an independent reference implementation, compares exact bytes on visible and hidden campaigns with mixed CRLF/LF, deferred partial lines, writer_open files, overlapping size and age triggers, and keep_count one edge cases. It requires identical output after shard reshuffle and checks atomic replacement by invalid runs after success. The ten-hour estimate reflects interacting line-boundary rules, generation chains, conditional gzip, and writer protection; one misapplied rule changes inventory hashes downstream.
