#!/usr/bin/env python3
"""Generate deterministic visible/hidden campaigns and frozen Oracle products."""

from __future__ import annotations

import csv
import random
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

TASK = Path(__file__).resolve().parents[2]
SOLUTION_SRC = TASK / "source" / "solution" / "unitlib" / "unitlib"
VISIBLE = TASK / "source" / "environment"
BUILD_DIR = TASK / "author-only" / "tooling" / ".build"


@dataclass(frozen=True)
class Fixture:
    name: str
    seed: int
    prefix: str
    force_a: str
    force_b: str
    energy_a: str
    energy_b: str


FIXTURES = (
    Fixture("visible", 811, "V", "lbf", "lb_f", "cal", "calorie"),
    Fixture("hidden-alpha", 1907, "A", "lb_f", "lbf", "calorie", "cal"),
    Fixture("hidden-beta", 4421, "B", "lbf", "lb_f", "cal", "calorie"),
)


def reset_dir(path: Path) -> None:
    resolved = path.resolve()
    if TASK not in resolved.parents and resolved != TASK:
        raise RuntimeError(f"refusing to replace path outside task: {path}")
    shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def compile_oracle() -> Path:
    reset_dir(BUILD_DIR)
    for src in sorted(SOLUTION_SRC.glob("*.java")):
        shutil.copy2(src, BUILD_DIR / src.name)
    subprocess.run(
        ["javac", "-d", str(BUILD_DIR), *[str(BUILD_DIR / p.name) for p in BUILD_DIR.glob("*.java")]],
        check=True,
    )
    return BUILD_DIR


def run_oracle(campaign: Path, output: Path, classpath: Path) -> None:
    reset_dir(output)
    subprocess.run(
        ["java", "-cp", str(classpath), "unitlib.Main", "run", str(campaign), str(output)],
        check=True,
    )


def make_campaign(config: Fixture, root: Path) -> None:
    reset_dir(root)
    root.joinpath("campaign.toml").write_text(
        "\n".join(
            [
                'schema_version = "1.0"',
                'si_system = "SI"',
                'canonical_units = { FORCE_POUND = "U001", CAL_THERMO = "U004" }',
                "",
            ]
        ),
        encoding="utf-8",
    )
    registry = [
        {
            "unit_id": "U001",
            "symbol": "lbf",
            "dimension": "force",
            "si_factor": "444822160/100000000",
            "si_offset": "0/1",
            "convention_group": "FORCE_POUND",
        },
        {
            "unit_id": "U002",
            "symbol": "lb_f",
            "dimension": "force",
            "si_factor": "444822160/100000000",
            "si_offset": "0/1",
            "convention_group": "FORCE_POUND",
        },
        {"unit_id": "U003", "symbol": "N", "dimension": "force", "si_factor": "1/1", "si_offset": "0/1", "convention_group": ""},
        {
            "unit_id": "U004",
            "symbol": "cal",
            "dimension": "energy",
            "si_factor": "4184/1",
            "si_offset": "0/1",
            "convention_group": "CAL_THERMO",
        },
        {
            "unit_id": "U005",
            "symbol": "calorie",
            "dimension": "energy",
            "si_factor": "4184/1",
            "si_offset": "0/1",
            "convention_group": "CAL_THERMO",
        },
        {"unit_id": "U006", "symbol": "J", "dimension": "energy", "si_factor": "1/1", "si_offset": "0/1", "convention_group": ""},
    ]
    write_csv(
        root / "registry.csv",
        ["unit_id", "symbol", "dimension", "si_factor", "si_offset", "convention_group"],
        registry,
    )
    conservation = [
        {
            "constraint_id": f"{config.prefix}C01",
            "quantity": "net_force",
            "window_start": 1000,
            "window_end": 1000,
            "expected_sum_si": "0/1",
            "tolerance_si": "1/1000",
        },
        {
            "constraint_id": f"{config.prefix}C02",
            "quantity": "heat_in",
            "window_start": 2000,
            "window_end": 2000,
            "expected_sum_si": "8368/1",
            "tolerance_si": "1/1",
        },
        {
            "constraint_id": f"{config.prefix}C03",
            "quantity": "stored_energy",
            "window_start": 3000,
            "window_end": 3000,
            "expected_sum_si": "12552/1",
            "tolerance_si": "2/1",
        },
    ]
    write_csv(
        root / "conservation.csv",
        ["constraint_id", "quantity", "window_start", "window_end", "expected_sum_si", "tolerance_si"],
        conservation,
    )

    observations = [
        {
            "obs_id": f"{config.prefix}O001",
            "source_id": f"{config.prefix}SRC-A",
            "timestamp": 1000,
            "quantity": "net_force",
            "magnitude": "10/1",
            "unit_symbol": config.force_a,
        },
        {
            "obs_id": f"{config.prefix}O002",
            "source_id": f"{config.prefix}SRC-A",
            "timestamp": 1000,
            "quantity": "net_force",
            "magnitude": "-10/1",
            "unit_symbol": config.force_a,
        },
        {
            "obs_id": f"{config.prefix}O003",
            "source_id": f"{config.prefix}SRC-A",
            "timestamp": 2000,
            "quantity": "heat_in",
            "magnitude": "1/1",
            "unit_symbol": config.energy_a,
        },
        {
            "obs_id": f"{config.prefix}O004",
            "source_id": f"{config.prefix}SRC-B",
            "timestamp": 1000,
            "quantity": "net_force",
            "magnitude": "5/1",
            "unit_symbol": config.force_b,
        },
        {
            "obs_id": f"{config.prefix}O005",
            "source_id": f"{config.prefix}SRC-B",
            "timestamp": 1000,
            "quantity": "net_force",
            "magnitude": "-5/1",
            "unit_symbol": config.force_b,
        },
        {
            "obs_id": f"{config.prefix}O006",
            "source_id": f"{config.prefix}SRC-B",
            "timestamp": 2000,
            "quantity": "heat_in",
            "magnitude": "1/1",
            "unit_symbol": config.energy_b,
        },
        {
            "obs_id": f"{config.prefix}O007",
            "source_id": f"{config.prefix}SRC-C",
            "timestamp": 3000,
            "quantity": "stored_energy",
            "magnitude": "2/1",
            "unit_symbol": config.energy_a,
        },
        {
            "obs_id": f"{config.prefix}O008",
            "source_id": f"{config.prefix}SRC-C",
            "timestamp": 3000,
            "quantity": "stored_energy",
            "magnitude": "1/1",
            "unit_symbol": config.energy_b,
        },
    ]
    rng = random.Random(config.seed)
    duplicate = dict(observations[0])
    rng.shuffle(observations)
    shards = [[], [], []]
    for index, row in enumerate(observations):
        shards[index % 3].append(row)
    shards[rng.randrange(3)].append(duplicate)
    shard_names = [f"packet-{rng.randrange(1000, 9999)}.csv" for _ in shards]
    for name, rows in zip(shard_names, shards):
        rng.shuffle(rows)
        write_csv(
            root / "datasets" / name,
            ["obs_id", "source_id", "timestamp", "quantity", "magnitude", "unit_symbol"],
            rows,
        )


def freeze(config: Fixture, campaign: Path, classpath: Path) -> None:
    expected = (
        TASK / "source" / "tests" / "expected" / "visible"
        if config.name == "visible"
        else TASK / "source" / "tests" / "expected" / "hidden" / config.name
    )
    run_oracle(campaign, expected, classpath)


def main() -> int:
    classpath = compile_oracle()
    for config in FIXTURES:
        campaign = (
            VISIBLE / "campaign"
            if config.name == "visible"
            else TASK / "source" / "tests" / "hidden" / config.name
        )
        make_campaign(config, campaign)
        freeze(config, campaign, classpath)
    examples = VISIBLE / "examples"
    reset_dir(examples)
    examples.joinpath("README.md").write_text(
        "# Worked edge cases\n\n"
        "`rounding.json` demonstrates positive and negative half ties for `roundHalfAway`. "
        "The visible campaign uses `lbf` versus `lb_f` and `cal` versus `calorie` across "
        "different sources. Conflicting duplicate observation identifiers are fatal.\n",
        encoding="utf-8",
    )
    examples.joinpath("rounding.json").write_text(
        '[{"denominator":2,"numerator":3,"result":2},{"denominator":2,"numerator":-3,"result":-2}]\n',
        encoding="utf-8",
    )
    examples.joinpath("conflicting-observations.csv").write_text(
        "obs_id,source_id,timestamp,quantity,magnitude,unit_symbol\n"
        "CONFLICT,SRC-X,1000,net_force,1/1,lbf\n"
        "CONFLICT,SRC-X,1000,net_force,2/1,lbf\n",
        encoding="utf-8",
    )
    spec_mirror = TASK / "source" / "environment" / "spec"
    print("generated 1 visible and 2 hidden campaigns with frozen Oracle outputs")
    print(f"spec at {spec_mirror}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
