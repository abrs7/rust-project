# Project Thanos preflight: telemetry-frame-recovery

## Verdict

**READY TO UPLOAD for Stage 1.**

The rebuilt TB3 package passes the current Harbor 0.23.0 contract, three final Oracle runs at reward 1.0, a final NOP run at reward 0.0, fifteen conjunctive verifier tests, and six adversarial runs at reward 0.0. The final ZIP contains one task root and no build logs, jobs, caches, preflight scripts, or legacy Django files.

**Stage 2 remains high risk.** Local checks cannot prove the platform predicates of at most two successful frontier-model rollouts and a median above 80 assistant turns. The task now requires multi-stage binary reconstruction, but a strong model may still implement it in fewer than 80 turns.

## Summary

| Phase | Check | Result | Evidence |
|---|---|---:|---|
| 0 | Accepted proposal | PASS | User confirmed the clean-room telemetry proposal was accepted |
| 0 | Docker | PASS | Docker 28.5.0 |
| 0 | Harbor | PASS | Upgraded from 0.2.0 to 0.23.0 |
| 1 | Single root and slug | PASS | One `telemetry-frame-recovery/` root; three lowercase kebab tokens |
| 1 | TB3 layout | PASS | `task.toml`, `instruction.md`, environment, solution, and separate tests image present |
| 1 | Archive safety | PASS | 45 entries; 46,301 bytes uncompressed; 64.8% compression |
| 1 | Stray files | PASS | No `.git`, jobs, logs, caches, venv, secrets, or legacy task files |
| 2 | Schema | PASS | Harbor schema 1.4 parses and executes |
| 2 | Required metadata | PASS | All eight required metadata fields are populated |
| 2 | Canary | PASS | Present in every required core file |
| 2 | Closing line | PASS | Exact required line, preceded by a blank line |
| 2 | Timeouts | PASS | Live TB4 contract: agent 28,800s; verifier 1,800s |
| 2 | Separate verifier | PASS | `environment_mode = "separate"` |
| 2 | Artifacts | PASS | `/app/telemetry` and `/app/output` declared and successfully transferred |
| 3 | Base images | PASS | Both use digest-pinned Python image `sha256:9d2e...00285` |
| 3 | Dependencies | PASS | Standard library only; no apt, pip, uv, or grade-time downloads |
| 3 | Network | PASS | Live profile requires `public` for agent and separate-verifier baselines/phases |
| 3 | Agent isolation | PASS | Agent image does not copy tests or solution |
| 3 | Artifact parents | PASS | Verifier image pre-creates `/app/telemetry`, `/app/output`, and reward parent |
| 3 | LF scripts | PASS | No CRLF in working tree or extracted ZIP |
| 3 | Image size | PASS | Built verifier image is 126 MB |
| 4 | Final Oracle run 1 | PASS | Reward 1.0; 15 tests passed |
| 4 | Final Oracle run 2 | PASS | Reward 1.0 |
| 4 | Final Oracle run 3 | PASS | Reward 1.0 |
| 4 | Determinism | PASS | Repeated hidden execution is byte-identical; every Oracle matches frozen truth |
| 4 | Final NOP | PASS | Reward 0.0 |
| 5 | Empty workspace | PASS | NOP reward 0.0; required candidate and outputs are mandatory |
| 5 | Naive parser | PASS | Reward 0.0 |
| 5 | Laziest shaped output | PASS | Reward 0.0 |
| 5 | Visible-constant copy | PASS | Reward 0.0 on varied hidden sessions |
| 5 | Reward/test read attack | PASS | Reward 0.0; candidate UID cannot read `/tests` or write verifier reward |
| 5 | `os._exit(0)` attack | PASS | Reward 0.0 |
| 5 | Agent-visible fixture tamper | PASS | Reward 0.0 against frozen pristine truth |
| 7 | Instruction length/style | PASS | 298 words; plain prose; absolute paths and complete output schema |
| 8 | Final ZIP | PASS | Hash and path recorded below |

## Oracle, NOP, and determinism

- Final Oracle rewards: **1.0, 1.0, 1.0**
- Final Oracle Harbor runtimes: **58s, 39s, 41s**
- Final NOP reward: **0.0**
- Final NOP Harbor runtime: **40s**
- Verifier tests: **15/15 passed**
- Agent/verifier image class: **126 MB**
- Output determinism: **PASS**, including a byte-for-byte second hidden run

Logs:

- `/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/runs/tb4-oracle-1.log`
- `/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/runs/tb4-oracle-2.log`
- `/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/runs/tb4-oracle-3.log`
- `/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/runs/tb4-nop.log`

## Verifier and attack results

The verifier runs candidate code as UID/GID 65534 with cleared supplementary groups, a restricted environment, resource limits, `/tests` mode 0700, and `/logs/verifier` mode 0700. A privilege probe confirms that the candidate cannot read frozen truth or write the reward file.

The verifier checks exact visible and hidden event streams, calibration values, manifests, file sets, varied firmware sessions, noise/corruption accounting, repeat determinism, malformed-ledger rejection, missing-input rejection, unusable calibration rejection, and output-write failure.

| Attack | Reward | Result |
|---|---:|---:|
| Empty/NOP | 0.0 | PASS |
| Well-shaped empty output | 0.0 | PASS |
| Legacy-only naive parser | 0.0 | PASS |
| Visible constants copied into every run | 0.0 | PASS |
| Read tests/write reward | 0.0 | PASS |
| Candidate `os._exit(0)` | 0.0 | PASS |
| Modified agent-visible capture | 0.0 | PASS |

Attack logs are under `/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/runs/attacks/` and are not included in the task ZIP.

## Ground-truth independence

The capture builder is outside the task root. It encodes declarative session descriptions directly and freezes expected values before packaging. The submitted verifier does not import, execute, or reproduce the Oracle decoder. Candidate-visible files contain no expected output, hidden hashes, answer mappings, or verifier code.

Hidden sessions vary firmware representation, mixed-build records, byte quoting, counter rollover position, calibration coefficients, channel identifiers, corruption count, noise placement, and escaped values.

## Stage 2 assessment

The solve path requires:

1. Inventorying captures, evidence, and output contracts.
2. Reconstructing the legacy wire frame.
3. Combining damaged notes, startup diagnostics, and loopback probes to recover modern framing.
4. Implementing two byte orders, quoting, two trailer algorithms, noisy-stream resynchronization, and corrupt/incomplete handling.
5. Reconstructing device time across a 16-bit counter.
6. Deriving per-session/channel affine calibration with exact decimal formatting.
7. Producing three ordered, mutually consistent artifact families.
8. Debugging visible mixed-build and escaped-byte sessions before hidden verification.

Compounding seams include firmware-dependent field order, firmware-dependent numeric order, quoting, CRC versus additive trailers, rollover, complete-candidate rejection accounting, mixed firmware, decimal half-even rounding, and deterministic ordering.

`LONG_HORIZON_RISK`: **HIGH / UNVERIFIED**. A strict static review estimated that a strong model might still solve the task in roughly 25–50 turns because the evidence is intentionally sufficient. Only actual Stage 2 rollouts can establish the required median above 80.

## Quality-check infrastructure note

`harbor check` was attempted twice. Both attempts failed during checker-agent setup after 360 seconds with `AgentSetupTimeoutError`, before producing a content judgment. Per the guidebook, the identical second infrastructure failure was not treated as a task defect and was not retried again.

A separate strict read-only rubric review found four actionable verifier/spec issues. They were fixed before the final Oracle/NOP/attack runs:

- removed unstated JSON object key-order grading;
- pre-created verifier artifact parents;
- added missing negative-contract tests;
- made previously vacuous tests depend on successful candidate behavior.

## Changes from the rejected legacy package

- Preserved the old Django task under `tasks/django-cors-broken/source/`.
- Removed the legacy task from the submission root.
- Replaced it with a clean-room scientific telemetry concept matching the accepted proposal.
- Upgraded the package from legacy `task.yaml` format to Harbor/TB3 schema 1.4.
- Added pinned offline agent and verifier images.
- Added deterministic synthetic visible and hidden captures.
- Added a thin Oracle launcher and full reference implementation.
- Added an independent, isolated, all-or-nothing verifier with fifteen tests.
- Removed old task logs, agent logs, build jobs, caches, and validation artifacts from the archive.

## Unverifiable platform-only items

- The live Stage 1 taxonomy requires category `Science`; confirm only the open `scientific-data-processing` subcategory if the platform later raises an advisory.
- Confirm that `abrahamasrat791@gmail.com` is the required project author address.
- Contamination screening is platform-only. The packet format, captures, expected values, and implementation were generated clean-room for this task.
- Stage 2 solve count and assistant-turn median cannot be reproduced locally.

## Final ZIP

- Path: `/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/iterations/003-failed/submission.zip`
- SHA-256: `7308592159bc12c7c88e73e53cfc1b721d4fc6d051bbd960250423b22a84d57e`
- Size: **26,759 bytes**

This iteration is retained as failed history and must not be uploaded again.
