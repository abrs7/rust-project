# Stage 0 proposal: Rebuild the WAL segment compactor

Proposed slug: `wal-segment-compactor`

Category: Software

Subcategory: Databases  

Estimated expert time: 11 hours

Append-only WAL segments with checksum frames must be compacted by dropping superseded records and tombstones while preserving commit order. The compactor reads sharded segment files and writes compacted segments plus a manifest of dropped ranges.

Failed runs exit nonzero without altering a previous successful output set. The verifier independently replays and compacts, checks CRC validation, sequence monotonicity, and byte-identical compactions on reshuffled inputs. Hidden segments include torn frames and duplicate LSNs.

WAL compaction mirrors real database maintenance; long horizon comes from staged correctness, not huge files.
