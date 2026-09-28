# Preflight 006: 1-ctd-cast-processing

## Verdict

READY TO UPLOAD

## Platform failure addressed (iteration 005)

**G05 ORACLE.REWARD_BELOW_FULL** — oracle scored 0 because `test_21` crashed in the verifier container:

```text
FileNotFoundError: /environment/spec
```

The verifier Docker image only copies `/tests/`; `environment/spec` is not mounted there. Local runs passed because `SOURCE/environment/spec` exists on the host.

## Fix

- Mirror `environment/spec/` → `tests/spec/` (included in verifier image)
- `Candidate` now copies `tests/spec` into the workspace as `/app/spec`
- `test_21` asserts the spec mirror exists instead of copying from missing paths

## Upload artifact

```text
tasks/1-ctd-cast-processing/iterations/006-pending/1-ctd-cast-processing.zip
```

## Local checks

- Harbor oracle: reward **1.0**
- Harbor NOP: reward **0.0**
- G06 IT02: addressed in iteration 005
