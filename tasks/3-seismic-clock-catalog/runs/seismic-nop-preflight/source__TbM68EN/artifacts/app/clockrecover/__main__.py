"""CLI skeleton for candidates."""

import argparse

from . import pipeline


def main() -> int:
    parser = argparse.ArgumentParser(prog="clockrecover")
    parser.add_argument(
        "command",
        choices=("ingest", "diagnose", "catalogue", "residuals", "fit-clock", "reconcile", "export", "run"),
    )
    parser.add_argument("campaign")
    parser.add_argument("output")
    args = parser.parse_args()
    function = getattr(pipeline, args.command.replace("-", "_"))
    function(args.campaign, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
