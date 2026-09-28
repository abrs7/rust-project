# Telemetry array rebuild — iteration 002 preflight

Verdict: **ready for Stage 1 and a new Stage 2 pilot**.

Iteration 001 failed `long_horizon` at 44.5 median turns while difficulty
passed (0/8 full credit). This iteration removes the four protocol manuals and
requires staged, example-driven reconstruction.

## Package

- Slug: `rustlabs/telemetry-array-rebuild`
- Schema: Harbor 1.4
- Artifacts: `/app/telemetry`, `/app/fragments`, `/app/evidence`, `/app/output`
- Instruction: 320 words, required closing line
- Canary: present in core files

## Horizon change

- 84 worked hex↔JSON examples replace field-order logs.
- Seven isolated stage commands; after `ingest`, fragments are not reread.
- Nine products plus `streams/{campaign}.bin`.
- Hidden campaigns and exact arithmetic are unchanged.

## Results

- Direct verifier: 15/15 in 6.5 seconds.
- Harbor Oracle: reward 1.0.
- Harbor NOP: reward 0.0.

Stage 2 long horizon remains an empirical platform property.
