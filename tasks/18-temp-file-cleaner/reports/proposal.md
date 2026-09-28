# Stage 0 proposal: Restore the temp file cleaner

Proposed slug: `temp-file-cleaner`

Category: Software

Subcategory: Systems  

Estimated expert time: 4 hours

A maintenance daemon should delete expired temp files by inode metadata and path rules, but the current script removes active files. Campaigns include synthetic directory trees, retention policies, and protected path lists. The corrected tool emits a deletion log, retained inventory, and checksum manifest.

Failed runs exit nonzero without altering a previous successful output set. The verifier checks that protected and in-use files survive, expired files are removed exactly once, and failed runs leave prior logs untouched. Hidden trees vary mount boundaries, symlink traps, and clock skew encoded in metadata.

This is a short systems hygiene task with enough edge cases to fail naive implementations while remaining solvable in half a day.
