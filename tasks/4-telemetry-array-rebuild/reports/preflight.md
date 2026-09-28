# Telemetry Array Rebuild Preflight

Verdict: **READY FOR STAGE 1 AND A NEW STAGE 2 PILOT**. Mechanical, Oracle,
isolation, deterministic-output, and adversarial checks pass. The redesigned
horizon is materially larger, but the median-turn predicate cannot be proven
locally because `harbor check` could not authenticate its Claude agent.

## Package

- Slug: `telemetry-array-rebuild`
- Source: `/home/abraham/workspace/rustlabs/tasks/telemetry-array-rebuild/source`
- Upload ZIP: `/home/abraham/workspace/rustlabs/tasks/telemetry-array-rebuild/iterations/001-pending/submission.zip`
- ZIP SHA-256: `35a4ca5ea52df935f43d4cf28788e076968f088e0140f83332fdf41a41b22e0b`
- Archive: one task root, 99 entries, 140,904 uncompressed bytes, 68% overall compression
- Local Harbor: `0.23.0`
- Verifier image: 126 MB

## Structural tightening

The failed task exposed almost the entire protocol and collapsed into one
decoder over four captures totaling 694 bytes. This successor uses a new slug
and six dependent reconstruction stages:

1. Validate and account for fragment containers.
2. Collapse duplicates and reconcile overlapping fragments into streams.
3. Recover alpha, beta, and gamma transport dialects with different framing,
   transforms, integrity algorithms, field order, and byte order.
4. Decode individual and compressed sample payloads, reject corruption, and
   arbitrate logical duplicates.
5. Unwrap 24-bit clocks and construct piecewise drift models from anchors.
6. Fit exact quadratic channel calibration, apply temperature compensation,
   and emit five mutually dependent products.

The candidate-visible collection contains six campaigns and 35 fragment files.
Hidden verification uses four different campaigns and 23 fragment files. The
Oracle implementation is 821 lines and the output contract covers records,
clock models, calibration models, observations, and campaign accounting.

## Mechanical and static checks

- Required Harbor/TB4 metadata: pass.
- TB4 `Science` category, public network profile, and 28,800-second agent timeout: pass.
- Canary in every core file: pass.
- Required closing line and blank-line placement: pass.
- Instruction length: 374 words.
- Pinned base images: pass.
- No apt, pip, uv, network fetch, test dependency, or agent-image answer leakage: pass.
- Verifier uses a separate image and unprivileged candidate subprocess: pass.
- CRLF and cache checks: pass.
- Frozen truth and hidden inputs exist only under `tests/`: pass.
- Fixture generator remains outside the task archive: pass.
- Final ZIP excludes Harbor job logs and caches: pass.

## Oracle and verifier

- Harbor Oracle run 1: reward 1.0, 39 seconds.
- Harbor Oracle run 2: reward 1.0, 36 seconds.
- Harbor Oracle run 3: reward 1.0, 35 seconds.
- Final-ZIP Oracle reproduction: reward 1.0, 38 seconds.
- Harbor NOP: reward 0.0.
- Exact verifier: all 23 tests pass.
- Visible and hidden outputs match independently generated frozen truth.
- Repeated output is byte-identical.
- Missing inputs, malformed catalogs, incomplete references, empty fragment
  collections, and blocked output paths return nonzero.
- Failed input validation preserves a previous successful output set.

## Adversarial checks

- Empty/NOP candidate: reward 0.
- Reject-everything candidate: reward 0.
- Visible constant-output candidate: reward 0.
- Reward-file tampering candidate: reward 0 and cannot cross the privilege boundary.
- Candidate cannot read hidden truth or write the verifier reward.

## Remaining uncertainty

`harbor check` reached its model trial but failed with
`AgentAuthenticationError: Not logged in`; this is local authentication, not a
task execution failure. No honest local check can guarantee the platform's
median assistant-turn result. The new package removes the observed short path,
but it should be submitted as a new task and its first Stage 2 trajectories
reviewed before spending later versions.
