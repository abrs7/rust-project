# Stage 0 proposal: Rebuild the log rotation tool

Proposed slug: `log-rotation-rebuild`

Category: Software

Subcategory: Systems  

Estimated expert time: 5 hours

Operations needs a small utility that rotates application logs under size and age policies without dropping partial lines or breaking active writers. The starter tree contains sample log trees, policy tables, and a stub binary that truncates files incorrectly. The finished tool must produce a rotation report, retained file inventory, and checksum manifest for every run.

The verifier checks line-boundary preservation, gzip naming conventions, idempotent reruns, and failure behavior when a destination is not writable. Hidden fixtures vary timezone stamps, mixed line endings, and concurrent-size edge cases. Outputs must match frozen references byte for byte.

This is a familiar systems task for anyone who has maintained production logs; difficulty comes from getting edge cases and deterministic reporting right, because exact contract semantics and deterministic output make naive shortcuts fail grading.
