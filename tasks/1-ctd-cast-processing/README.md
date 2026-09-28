# 1) ctd-cast-processing

Status: **iteration 006-pending ready for Stage 1 re-upload** (005 failed G05: test_21 spec path missing in verifier container)

**Upload this file:** `iterations/006-pending/1-ctd-cast-processing.zip`

Do **not** upload `ctd-cast-processing.zip` (sha256 `ca4439189…`) — that is the pre-TB4 001 package without README or `terminal-bench/` namespace.

- Editable Harbor task: `source/`
- Accepted design: `reports/proposal.md`
- Author-only generators, Oracle runs, and attacks: `author-only/`
- Immutable submission iterations: `iterations/`
- Local Harbor evidence: `runs/`
- Platform trajectories: `trajectories/`

No ZIP should be created until the Oracle, NOP, isolation, attack, and
determinism checks pass. Package iteration 001 with the workspace packaging
script; never place development tooling inside `source/`.
