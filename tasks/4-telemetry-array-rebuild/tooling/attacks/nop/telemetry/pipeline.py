from pathlib import Path


def _missing(*_args: Path | str) -> None:
    raise NotImplementedError("nop attack")


ingest = assemble = decode = fit_clock = calibrate = reconcile = export = run = _missing
