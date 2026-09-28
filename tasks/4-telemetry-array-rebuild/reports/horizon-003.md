# Horizon tightening after 44.5 turns

Iteration 001 failed at 44.5 median turns because four logs specified every
layout. Iteration 002 still paired hex with recovered dialect, sequence,
tick, and payload fields, so a strong agent could transcribe a decoder.

This revision keeps the same encodings and hidden campaigns. It removes those
field maps.

Candidate-visible evidence is now:

- `inventory.txt` — three console names and sync marks only
- `captures/*.bin` — unlabeled binaries
- `journal.jsonl` — accepted/rejected plus at most one scientific fact or
  bench count (`valid_records`, `stream_sha256`)
- `metrology/` — numeric wrap, half-even, quadratic, and temperature checks

There is no recovered `dialect`, `sequence`, `tick_raw`, or `payload_hex` in
the examples. Framing has to be recovered by matching bench stream counts and
by inspecting `/app/fragments`. Difficulty should still hold; 90–100 median
turns is the intended path, not a guarantee.
