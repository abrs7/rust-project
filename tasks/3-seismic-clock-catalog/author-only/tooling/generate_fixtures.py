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


@dataclass(frozen=True)
class Fixture:
    name: str
    seed: int
    epoch: int
    station_count: int
    faulty_index: int
    event_count: int
    id_prefix: str


FIXTURES = (
    Fixture("visible", 731, -6_000_000, 5, 4, 9, "V"),
    Fixture("hidden-alpha", 1907, 0, 5, 1, 9, "A"),
    Fixture("hidden-beta", 4421, 12_000_000, 6, 3, 10, "B"),
)


def round_half_away(numerator: int, denominator: int) -> int:
    sign = -1 if numerator < 0 else 1
    quotient, remainder = divmod(abs(numerator), denominator)
    return sign * (quotient + (2 * remainder >= denominator))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def reset_dir(path: Path) -> None:
    resolved = path.resolve()
    if TASK not in resolved.parents:
        raise RuntimeError(f"refusing to replace path outside task: {path}")
    shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True)


def make_campaign(config: Fixture, root: Path) -> None:
    reset_dir(root)
    rng = random.Random(config.seed)
    start = config.epoch
    end = start + 10_000_000
    boundaries = [start + 4_000_000, start + 5_000_000, start + 7_000_000]
    rates = [(1, 1), (999_999, 1_000_000), (1_000_001, 1_000_000)]
    root.joinpath("campaign.toml").write_text(
        "\n".join(
            [
                'schema_version = "1.0"',
                f"campaign_start_us = {start}",
                f"campaign_end_us = {end}",
                f"min_stable_stations = {config.station_count - 2}",
                "residual_min_us = -500000",
                "residual_max_us = 500000",
                'allowed_rates = ["1/1", "999999/1000000", "1000001/1000000"]',
                "candidate_boundaries_us = [" + ", ".join(map(str, boundaries)) + "]",
                "",
            ]
        ),
        encoding="utf-8",
    )

    stations = [
        {"station_id": f"{config.id_prefix}Q{17 + 13 * i:03d}", "name": f"Recorder {chr(75 + i)}"}
        for i in range(config.station_count)
    ]
    sources = [
        {
            "source_id": f"{config.id_prefix}X{index * 19 + 11:03d}",
            "x_m": -4200 + index * 5100,
            "y_m": 3300 - index * 2700,
            "depth_m": 1800 + index * 900,
        }
        for index in range(3)
    ]
    write_csv(root / "stations.csv", ["station_id", "name"], stations)
    write_csv(root / "sources.csv", ["source_id", "x_m", "y_m", "depth_m"], sources)

    travel: dict[tuple[str, str], int] = {}
    travel_rows = []
    for station_index, station in enumerate(stations):
        for source_index, source in enumerate(sources):
            value = 50_000 + station_index * 17_000 + source_index * 23_000 + station_index * source_index * 3_000
            travel[(station["station_id"], source["source_id"])] = value
            travel_rows.append(
                {"station_id": station["station_id"], "source_id": source["source_id"], "travel_us": value}
            )
    rng.shuffle(travel_rows)
    write_csv(root / "travel_times.csv", ["station_id", "source_id", "travel_us"], travel_rows)

    relative_true = [1_500_000, 2_250_000, 3_300_000, 4_500_000, 5_350_000, 6_300_000, 7_500_000, 8_350_000, 9_300_000, 9_720_000]
    faulty = stations[config.faulty_index]["station_id"]
    events = []
    for index in range(config.event_count):
        source = sources[(index * 2 + 1) % len(sources)]["source_id"]
        true_faulty = start + relative_true[index]
        origin = true_faulty - travel[(faulty, source)]
        events.append({"index": index, "source_id": source, "origin_us": origin, "true_faulty": true_faulty})
    known_rows = [
        {
            "event_id": f"SHOT-{config.id_prefix}-{event['index'] + 1:02d}",
            "source_id": event["source_id"],
            "origin_us": event["origin_us"],
        }
        for event in events
        if event["index"] in {0, 3, config.event_count - 1}
    ]
    rng.shuffle(known_rows)
    write_csv(root / "known_events.csv", ["event_id", "source_id", "origin_us"], known_rows)

    picks: list[dict[str, object]] = []
    serial = 0

    def add(station_id: str, recorded: int) -> dict[str, object]:
        nonlocal serial
        serial += 1
        token = (serial * 7919 + config.seed * 17) % 99991
        row = {"pick_id": f"{config.id_prefix}P{token:05d}", "station_id": station_id, "recorded_us": recorded}
        picks.append(row)
        return row

    stable = [row["station_id"] for row in stations if row["station_id"] != faulty]
    duplicated: dict[str, object] | None = None
    for event in events:
        missing = stable[(event["index"] + config.seed) % len(stable)] if event["index"] % 3 == 1 else None
        for station in stable:
            if station == missing:
                continue
            true = event["origin_us"] + travel[(station, event["source_id"])]
            row = add(station, true)
            if duplicated is None and event["index"] == 0:
                duplicated = dict(row)

    segment_models = (
        (start, 999_999, 1_000_000, -120_000),
        (start + 4_000_000, 1_000_001, 1_000_000, 220_000),
        (start + 7_000_000, 1, 1, -330_000),
    )
    omitted_faulty_event = 7 if config.event_count == 9 else 8
    for event in events:
        if event["index"] == omitted_faulty_event:
            continue
        true = event["true_faulty"]
        segment = max((item for item in segment_models if item[0] <= true), key=lambda x: x[0])
        seg_start, p, q, offset = segment
        recorded = true + offset + round_half_away((p - q) * (true - seg_start), q)
        add(faulty, recorded)

    # Plausible residual-lattice decoys and unrelated stable noise.
    for event_index in (2, 4, 6):
        if event_index < len(events):
            event = events[event_index]
            add(faulty, event["true_faulty"] + (310_000 if event_index % 4 else -260_000))
    for station_index, station in enumerate(stable[:3]):
        add(station, start + 800_000 + station_index * 1_337_111 + config.seed % 997)

    rng.shuffle(picks)
    shards = [[], [], []]
    for index, row in enumerate(picks):
        shards[index % len(shards)].append(row)
    if duplicated is not None:
        shards[2].append(duplicated)
    shard_names = [f"packet-{rng.randrange(1000, 9999)}.csv" for _ in shards]
    for name, rows in zip(shard_names, shards):
        rng.shuffle(rows)
        write_csv(root / "picks" / name, ["pick_id", "station_id", "recorded_us"], rows)


def run_oracle(campaign: Path, output: Path) -> None:
    if str(SOLUTION) not in sys.path:
        sys.path.insert(0, str(SOLUTION))
    module = importlib.import_module("clockrecover.pipeline")
    module.run(campaign, output)


def freeze(config: Fixture, campaign: Path) -> None:
    expected = (
        TASK / "source" / "tests" / "expected" / "visible"
        if config.name == "visible"
        else TASK / "source" / "tests" / "expected" / "hidden" / config.name
    )
    reset_dir(expected)
    run_oracle(campaign, expected)


def main() -> int:
    for config in FIXTURES:
        campaign = (
            VISIBLE / "campaign"
            if config.name == "visible"
            else TASK / "source" / "tests" / "hidden" / config.name
        )
        make_campaign(config, campaign)
        freeze(config, campaign)
    examples = VISIBLE / "examples"
    reset_dir(examples)
    examples.joinpath("README.md").write_text(
        "# Worked edge cases\n\n"
        "`rounding.json` demonstrates exact positive and negative half ties. The visible campaign also contains "
        "an exact duplicate pick, missing stable observations, unrelated and plausible faulty-station decoys, "
        "negative offsets, two jumps, and an unused candidate boundary. Conflicting identifiers are fatal rather "
        "than part of a solvable campaign.\n",
        encoding="utf-8",
    )
    examples.joinpath("rounding.json").write_text(
        json.dumps(
            [
                {"denominator": 2, "numerator": 3, "result": 2},
                {"denominator": 2, "numerator": -3, "result": -2},
                {"denominator": 4, "numerator": 5, "result": 1},
                {"denominator": 4, "numerator": -5, "result": -1},
            ],
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    examples.joinpath("conflicting-picks.csv").write_text(
        "pick_id,station_id,recorded_us\nCONFLICT,Q1,-7\nCONFLICT,Q1,-6\n",
        encoding="utf-8",
    )
    examples.joinpath("boundary-evaluation.json").write_text(
        json.dumps(
            {
                "explanation": "A true tick equal to 4000000 uses the segment starting at 4000000.",
                "segment_start_us": 4_000_000,
                "true_us": 4_000_000,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print("generated 1 visible and 2 hidden campaigns with frozen Oracle outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
