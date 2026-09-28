#!/usr/bin/env python3
"""Materialize author-only attack packages. Never copy these into source/."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parents[1]
VISIBLE = TASK / "source" / "tests" / "expected" / "visible"
EXAMPLES = TASK / "source" / "environment" / "examples"
FIVE = (
    "calibration.json",
    "clock-models.json",
    "manifest.json",
    "observations.jsonl",
    "records.jsonl",
)

MAIN = '''"""Attack CLI."""

from __future__ import annotations

import argparse
import sys

from . import pipeline

ARITY = {
    "ingest": 3,
    "assemble": 2,
    "decode": 2,
    "fit-clock": 2,
    "calibrate": 2,
    "reconcile": 2,
    "export": 3,
    "run": 4,
}


def main() -> int:
    parser = argparse.ArgumentParser(prog="telemetry")
    parser.add_argument("command", choices=tuple(ARITY))
    parser.add_argument("args", nargs="*")
    parsed = parser.parse_args()
    expected = ARITY[parsed.command]
    if len(parsed.args) != expected:
        print(f"telemetry: {parsed.command} expects {expected} arguments", file=sys.stderr)
        return 2
    try:
        getattr(pipeline, parsed.command.replace("-", "_"))(*parsed.args)
    except Exception as exc:
        print(f"telemetry: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

INIT = '"""Attack package."""\n'
EXACT = '''def round_half_even(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    sign = -1 if numerator < 0 else 1
    magnitude = abs(numerator)
    quotient, remainder = divmod(magnitude, denominator)
    doubled = remainder * 2
    if doubled > denominator or (doubled == denominator and quotient & 1):
        quotient += 1
    return sign * quotient
'''

NOP = '''from pathlib import Path


def _missing(*_args: Path | str) -> None:
    raise NotImplementedError("nop attack")


ingest = assemble = decode = fit_clock = calibrate = reconcile = export = run = _missing
'''

REJECT = '''from pathlib import Path


def _reject(*_args: Path | str) -> None:
    raise RuntimeError("reject-everything attack")


ingest = assemble = decode = fit_clock = calibrate = reconcile = export = run = _reject
'''

DUMP = '''from pathlib import Path
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
'''

EXAMPLE_HEX = '''from pathlib import Path
import json

HEX = {hexes}


def _write(output: Path | str) -> None:
    target = Path(output)
    target.mkdir(parents=True, exist_ok=True)
    rows = [
        {{
            "accepted": True,
            "campaign": "example-leak",
            "final_piece": True,
            "payload_hex": HEX[0] if HEX else "deadbeef",
            "payload_octets": 4,
            "payload_sha256": None,
            "stream_offset": 0,
        }}
    ]
    decoded = [
        {{
            "campaign": "example-leak",
            "dialect": "alpha",
            "kind": "science",
            "payload_hex": HEX[0] if HEX else "deadbeef",
            "payload_sha256": "0" * 64,
            "sequence": 1,
            "stream_offset": 0,
            "tick_raw": 0,
        }}
    ]
    (target / "fragment-index.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\\n" for row in rows),
        encoding="utf-8",
    )
    (target / "decoded-records.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\\n" for row in decoded),
        encoding="utf-8",
    )


def ingest(fragments, campaigns, output):
    _write(output)


def assemble(campaigns, output):
    _write(output)


def decode(campaigns, output):
    _write(output)


def fit_clock(campaigns, output):
    _write(output)


def calibrate(references, output):
    _write(output)


def reconcile(references, output):
    _write(output)


def export(campaigns, references, output):
    _write(output)


def run(fragments, campaigns, references, output):
    _write(output)
'''

REREAD = '''from pathlib import Path
import hashlib
import json

MARKER = ".telemetry-fragments-path"


def ingest(fragments, campaigns, output):
    target = Path(output)
    target.mkdir(parents=True, exist_ok=True)
    source = Path(fragments).resolve()
    (target / MARKER).write_text(str(source), encoding="utf-8")
    digest = hashlib.sha256()
    for path in sorted(source.glob("*.frag")):
        digest.update(path.read_bytes())
    (target / "fragment-index.jsonl").write_text(
        json.dumps({"reread": digest.hexdigest()}, sort_keys=True) + "\\n",
        encoding="utf-8",
    )


def assemble(campaigns, output):
    target = Path(output)
    saved = Path((target / MARKER).read_text(encoding="utf-8").strip())
    digest = hashlib.sha256()
    for path in sorted(saved.glob("*.frag")):
        digest.update(path.read_bytes())
    payload = {
        "campaigns": [],
        "reread_sha256": digest.hexdigest(),
        "schema_version": 1,
    }
    (target / "assembly.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\\n", encoding="utf-8"
    )


def decode(campaigns, output):
    assemble(campaigns, output)


def fit_clock(campaigns, output):
    assemble(campaigns, output)


def calibrate(references, output):
    assemble("-", output)


def reconcile(references, output):
    assemble("-", output)


def export(campaigns, references, output):
    assemble(campaigns, output)


def run(fragments, campaigns, references, output):
    ingest(fragments, campaigns, output)
    assemble(campaigns, output)
'''


def write_package(name: str, pipeline: str) -> Path:
    package = ROOT / name / "telemetry"
    if package.exists():
        shutil.rmtree(package.parent)
    package.mkdir(parents=True)
    (package / "__init__.py").write_text(INIT, encoding="utf-8")
    (package / "__main__.py").write_text(MAIN, encoding="utf-8")
    (package / "exact.py").write_text(EXACT, encoding="utf-8")
    (package / "pipeline.py").write_text(pipeline, encoding="utf-8")
    return package


def copy_dump(package: Path, names: tuple[str, ...] | None = None) -> None:
    dump = package / "_dump"
    dump.mkdir()
    selected = names or tuple(path.name for path in VISIBLE.iterdir() if path.is_file())
    for name in selected:
        shutil.copy2(VISIBLE / name, dump / name)
    if names is None:
        shutil.copytree(VISIBLE / "streams", dump / "streams")


def example_hex_list() -> list[str]:
    found: list[str] = []
    for path in EXAMPLES.rglob("*.json"):
        text = path.read_text(encoding="utf-8")
        if '"hex"' not in text:
            continue
        import json

        def walk(value: object) -> None:
            if isinstance(value, dict):
                hex_value = value.get("hex")
                if isinstance(hex_value, str) and hex_value:
                    found.append(hex_value.lower())
                for item in value.values():
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(json.loads(text))
    return found


def main() -> None:
    write_package("nop", NOP)
    write_package("reject", REJECT)
    visible = write_package("visible-constant", DUMP)
    copy_dump(visible)
    five = write_package("five-file", DUMP)
    copy_dump(five, FIVE)
    hexes = example_hex_list()
    frozen_hex = set()
    for name in ("fragment-index.jsonl", "decoded-records.jsonl"):
        for line in (VISIBLE / name).read_text(encoding="utf-8").splitlines():
            payload = __import__("json").loads(line).get("payload_hex")
            if payload:
                frozen_hex.add(payload.lower())
    distinctive = [value for value in hexes if value not in frozen_hex][:8] or ["c0ffee"]
    write_package("example-hex", EXAMPLE_HEX.format(hexes=repr(distinctive)))
    write_package("reread", REREAD)
    print("wrote attack packages under", ROOT)


if __name__ == "__main__":
    main()
