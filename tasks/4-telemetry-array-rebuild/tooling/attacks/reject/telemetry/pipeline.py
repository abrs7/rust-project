from pathlib import Path


def _reject(*_args: Path | str) -> None:
    raise RuntimeError("reject-everything attack")


ingest = assemble = decode = fit_clock = calibrate = reconcile = export = run = _reject
