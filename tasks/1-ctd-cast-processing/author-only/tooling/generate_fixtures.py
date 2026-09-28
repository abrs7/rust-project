#!/usr/bin/env python3
"""Generate deterministic visible/hidden campaigns and frozen Oracle products."""

from __future__ import annotations

import csv
import importlib
import json
import random
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

TASK = Path(__file__).resolve().parents[2]
SOLUTION = TASK / "source" / "solution"
VISIBLE = TASK / "source" / "environment"
DEPTH_SCALE = 1_000_000


@dataclass(frozen=True)
class Fixture:
    name: str
    seed: int
    cast_id: str
    true_lat: tuple[int, int]
    header_lat: tuple[int, int]
    candidates: tuple[tuple[int, int], ...]
    bin_size: tuple[int, int]
    depth_levels_m: tuple[int, ...]


FIXTURES = (
    Fixture(
        "visible",
        731,
        "V-CAST-001",
        (45, 1),
        (45, 1),
        ((43, 1), (45, 1), (47, 1)),
        (5, 2),
        tuple(range(0, 101, 5)),
    ),
    Fixture(
        "hidden-alpha",
        1907,
        "A-CAST-017",
        (52, 1),
        (52, 1),
        ((51, 1), (52, 1), (53, 1)),
        (2, 1),
        tuple(range(0, 81, 5)),
    ),
    Fixture(
        "hidden-beta",
        4421,
        "B-CAST-009",
        (47, 1),
        (43, 1),
        ((43, 1), (45, 1), (47, 1)),
        (5, 2),
        tuple(range(0, 121, 5)),
    ),
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


def rational_string(num: int, den: int) -> str:
    return f"{num}/{den}"


def load_solution():
    if str(SOLUTION) not in sys.path:
        sys.path.insert(0, str(SOLUTION))
    exact = importlib.import_module("ctdproc.exact")
    return exact


def make_campaign(config: Fixture, root: Path) -> None:
    reset_dir(root)
    exact = load_solution()
    candidates = [rational_string(n, d) for n, d in config.candidates]
    root.joinpath("cast.toml").write_text(
        "\n".join(
            [
                'schema_version = "1.0"',
                f'cast_id = "{config.cast_id}"',
                f'latitude_deg = "{rational_string(*config.header_lat)}"',
                f'bin_size_m = "{rational_string(*config.bin_size)}"',
                "candidate_latitudes_deg = ["
                + ", ".join(f'"{item}"' for item in candidates)
                + "]",
                "",
            ]
        ),
        encoding="utf-8",
    )

    rows: list[dict[str, int]] = []
    time_ms = 0
    for depth_m in config.depth_levels_m:
        depth_micro = depth_m * DEPTH_SCALE
        temperature_mdc = 15000 - depth_m * 50
        salinity_milli = 35000 + depth_m * 12
        conductivity_us = exact.round_half_away(salinity_milli + 25 * temperature_mdc, 700)
        pressure_mdb = exact.pressure_mdb_from_depth(depth_micro, *config.true_lat)
        rows.append(
            {
                "time_s": time_ms,
                "pressure_dbar": pressure_mdb,
                "temperature_c": temperature_mdc,
                "conductivity_mS": conductivity_us,
            }
        )
        time_ms += 1500 + (depth_m % 7) * 11

    upcast = list(reversed(rows[:-1]))
    for index, row in enumerate(upcast):
        row = dict(row)
        row["time_s"] = time_ms + index * 1200
        row["pressure_dbar"] = max(0, row["pressure_dbar"] - 3000 - index * 500)
        row["temperature_c"] = row["temperature_c"] + 100
        rows.append(row)

    rng = random.Random(config.seed)
    duplicated = dict(rows[3])
    rng.shuffle(rows)
    rows.append(duplicated)

    shards = [[], [], []]
    for index, row in enumerate(rows):
        shards[index % len(shards)].append(row)
    shard_names = [f"trace-{rng.randrange(1000, 9999)}.csv" for _ in shards]
    for name, shard_rows in zip(shard_names, shards):
        rng.shuffle(shard_rows)
        write_csv(
            root / "profiles" / name,
            ["time_s", "pressure_dbar", "temperature_c", "conductivity_mS"],
            shard_rows,
        )


def run_oracle(campaign: Path, output: Path) -> None:
    if str(SOLUTION) not in sys.path:
        sys.path.insert(0, str(SOLUTION))
    for name in list(sys.modules):
        if name == "ctdproc" or name.startswith("ctdproc."):
            del sys.modules[name]
    module = importlib.import_module("ctdproc.pipeline")
    module.run(campaign, output)


def freeze(config: Fixture, campaign: Path) -> None:
    expected = (
        TASK / "source" / "tests" / "expected" / "visible"
        if config.name == "visible"
        else TASK / "source" / "tests" / "expected" / "hidden" / config.name
    )
    reset_dir(expected)
    run_oracle(campaign, expected)


def write_examples() -> None:
    exact = load_solution()
    examples = VISIBLE / "examples"
    reset_dir(examples)
    examples.joinpath("README.md").write_text(
        "# Worked edge cases\n\n"
        "`depth-formula.json` shows latitude-dependent depth conversion at a survey "
        "latitude. `density-inversion.json` explains the signal when the header "
        "latitude is wrong. `survey-tie-points.csv` lists reference densities at "
        "known depths for each candidate latitude; tie RMS breaks latitude ties.\n",
        encoding="utf-8",
    )
    lat = (45, 1)
    depth_micro = 50 * DEPTH_SCALE
    pressure = exact.pressure_mdb_from_depth(depth_micro, *lat)
    recovered = exact.depth_micro_m(pressure, *lat)
    examples.joinpath("depth-formula.json").write_text(
        json.dumps(
            {
                "depth_micro_m": depth_micro,
                "latitude_deg": rational_string(*lat),
                "pressure_dbar": pressure,
                "recovered_depth_micro_m": recovered,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    examples.joinpath("density-inversion.json").write_text(
        json.dumps(
            {
                "explanation": "Using header latitude 43/1 on a cast taken at 47/1 produces density decreasing with depth.",
                "header_latitude_deg": "43/1",
                "true_latitude_deg": "47/1",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    tie_rows = []
    tie_latitudes = ((43, 1), (45, 1), (47, 1), (50, 1), (51, 1), (52, 1), (53, 1), (54, 1))
    tie_depths = tuple(range(0, 121, 5))
    for lat in tie_latitudes:
        for depth_m in tie_depths:
            depth_micro = depth_m * DEPTH_SCALE
            temperature_mdc = 15000 - depth_m * 50
            salinity_milli = 35000 + depth_m * 12
            conductivity_us = exact.round_half_away(salinity_milli + 25 * temperature_mdc, 700)
            pressure_mdb = exact.pressure_mdb_from_depth(depth_micro, *lat)
            recovered_depth = exact.depth_micro_m(pressure_mdb, *lat)
            density = exact.density_micro(salinity_milli, temperature_mdc, recovered_depth)
            tie_rows.append(
                {
                    "latitude_deg": rational_string(*lat),
                    "depth_m": depth_m,
                    "density_micro_kg_m3": density,
                }
            )
    write_csv(
        examples / "survey-tie-points.csv",
        ["latitude_deg", "depth_m", "density_micro_kg_m3"],
        tie_rows,
    )


def mirror_examples_to_tests() -> None:
    source = VISIBLE / "examples"
    target = TASK / "source" / "tests" / "examples"
    reset_dir(target)
    shutil.copytree(source, target, dirs_exist_ok=True)


def main() -> int:
    write_examples()
    mirror_examples_to_tests()
    for config in FIXTURES:
        campaign = (
            VISIBLE / "campaign"
            if config.name == "visible"
            else TASK / "source" / "tests" / "hidden" / config.name
        )
        make_campaign(config, campaign)
        freeze(config, campaign)
    print("generated 1 visible and 2 hidden campaigns with frozen Oracle outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
