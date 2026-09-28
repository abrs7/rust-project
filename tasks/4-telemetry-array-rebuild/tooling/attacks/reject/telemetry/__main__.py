"""Attack CLI."""

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
