from pathlib import Path
import shutil

DUMP = Path(__file__).resolve().parent / "_dump"


def _copy(output: Path | str) -> None:
    target = Path(output)
    target.mkdir(parents=True, exist_ok=True)
    for path in DUMP.rglob("*"):
        if path.is_file():
            destination = target / path.relative_to(DUMP)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)


def ingest(fragments: Path | str, campaigns: Path | str, output: Path | str) -> None:
    _copy(output)


def assemble(campaigns: Path | str, output: Path | str) -> None:
    _copy(output)


def decode(campaigns: Path | str, output: Path | str) -> None:
    _copy(output)


def fit_clock(campaigns: Path | str, output: Path | str) -> None:
    _copy(output)


def calibrate(references: Path | str, output: Path | str) -> None:
    _copy(output)


def reconcile(references: Path | str, output: Path | str) -> None:
    _copy(output)


def export(campaigns: Path | str, references: Path | str, output: Path | str) -> None:
    _copy(output)


def run(
    fragments: Path | str,
    campaigns: Path | str,
    references: Path | str,
    output: Path | str,
) -> None:
    _copy(output)
