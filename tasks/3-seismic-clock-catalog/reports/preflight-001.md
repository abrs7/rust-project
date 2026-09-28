# Seismic clock catalogue — iteration 001 preflight

Verdict: **ready for Stage 1 and a Stage 2 pilot**.

## Package

- Task: `rustlabs/seismic-clock-catalog`
- Schema: Harbor 1.4
- Candidate artifacts: `/app/clockrecover`, `/app/campaign`, `/app/output`
- Runtime: Python standard library only
- Network mode: public
- Canary: present in all six core task files

## Contract and fixtures

- Seven isolated stages plus complete `run` and public Python APIs.
- Exact signed integer/rational arithmetic with half-away-from-zero rounding.
- One visible and two hidden deterministic campaigns.
- Nine canonical intermediate/final products per campaign.
- Visible/hidden products, staged/full parity, every-pick disposition, negative
  residuals, clock jumps, missing observations, exact duplicates, and decoys
  were checked.

## Verifier controls

- Candidate code executes only in child processes and is privilege-dropped.
- Hidden products are inaccessible to the candidate process.
- Canonical bytes, exact file set, regular-file/link constraints, scientific
  invariants, stage/API isolation, shard permutations, hash-seed determinism,
  malformed inputs, non-unique diagnosis, and failure atomicity are checked.
- Author-only NOP and constant-output probes are rejected.

## Results

- Direct verifier against reference: 4/4 tests passed in 6.862 seconds.
- Harbor dry-run: passed.
- Harbor Oracle: reward 1.0, no exceptions.
- Harbor NOP: reward 0.0, no exceptions.
- Workspace validation and lints: passed.

Two early local Harbor runs exposed and led to fixes for the environment build
context and the separate-verifier campaign artifact boundary. They are not
submission candidates; the final successful evidence is in
`runs/seismic-oracle-preflight-3` and `runs/seismic-nop-preflight`.

Stage 2 long-horizon behavior remains an empirical platform property and must
be assessed from the submitted iteration's rollout trajectories.
