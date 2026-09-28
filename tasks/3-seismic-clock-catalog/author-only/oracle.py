#!/usr/bin/env python3
"""Private entry point for running the reference implementation directly."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TASK / "source" / "solution"))

from clockrecover.pipeline import run  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("campaign", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.campaign, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
