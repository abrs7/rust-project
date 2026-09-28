# Preflight 003: 1-ctd-cast-processing

## Verdict

READY TO UPLOAD

## What went wrong on platform (iteration 002 attempt)

The platform received the **old** pre-TB4 ZIP:

- Uploaded: `ctd-cast-processing.zip`
- SHA-256: `ca4439189f404d72317636c4c122dbb0b9bc23671ec046d91cad20133da7f03e`
- Missing: `source/README.md`, `[task] name = "terminal-bench/…"`

That hash is iteration **001** (rejected). Do not re-upload it.

## Correct upload artifact

```text
tasks/1-ctd-cast-processing/iterations/003-pending/1-ctd-cast-processing.zip
```

Upload the file named **`1-ctd-cast-processing.zip`** (matches numbered folder). The ZIP interior root stays `ctd-cast-processing/`.

## TB4 fixes included

- `[task] name = "terminal-bench/ctd-cast-processing"`
- `README.md` with four `##` explanation sections
- Canaries on all `ctdproc/*.py` modules
