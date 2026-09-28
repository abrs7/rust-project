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

SLOPE_NUM = 251
SLOPE_DEN = 1
INTERCEPT_NUM = 9850
INTERCEPT_DEN = 1


@dataclass(frozen=True)
class Fixture:
    name: str
    seed: int
    saturated_index: int
    tau_us: int
    event_count: int
    span_us: int
    id_prefix: str


FIXTURES = (
    Fixture("visible", 831, 2, 75_000, 420, 50_000_000, "V"),
    Fixture("hidden-alpha", 2103, 1, 92_000, 510, 62_000_000, "A"),
    Fixture("hidden-beta", 5507, 3, 68_000, 380, 44_000_000, "B"),
)

LINE_ENERGIES = (300_000, 477_100, 661_657, 843_200, 900_000)


def round_half_away(numerator: int, denominator: int) -> int:
    sign = -1 if numerator < 0 else 1
    quotient, remainder = divmod(abs(numerator), denominator)
    return sign * (quotient + (2 * remainder >= denominator))


def energy_to_channel(energy_mkeV: int) -> int:
    return round_half_away(energy_mkeV * SLOPE_DEN * INTERCEPT_DEN - INTERCEPT_NUM * SLOPE_DEN, SLOPE_NUM * INTERCEPT_DEN)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def reset_dir(path: Path) -> None:
    resolved = path.resolve()
    if TASK not in resolved.parents and resolved != TASK:
        raise RuntimeError(f"refusing to replace path outside task: {path}")
    shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True)


def add_peak(histogram: dict[int, int], center: int, height: int, saturated: bool) -> None:
    if saturated:
        half = height // 2
        for offset in range(-14, 15):
            channel = center + offset
            if offset == 0:
                count = height
            elif abs(offset) <= 4:
                count = height - 1
            elif abs(offset) <= 8:
                count = half + 800
            else:
                distance = abs(offset) - 8
                count = max(half - distance * 120, 20)
            histogram[channel] = histogram.get(channel, 0) + count
    else:
        for offset in range(-5, 6):
            channel = center + offset
            count = max(height - abs(offset) * (height // 8), height // 5)
            histogram[channel] = histogram.get(channel, 0) + count


def make_campaign(config: Fixture, root: Path) -> None:
    reset_dir(root)
    rng = random.Random(config.seed)
    root.joinpath("campaign.toml").write_text(
        "\n".join(
            [
                'schema_version = "1.0"',
                "channel_min = 0",
                "channel_max = 4095",
                "peak_min_counts = 800",
                "peak_min_separation = 12",
                "saturation_fwhm_min = 12",
                "saturation_plateau_delta = 2",
                "saturation_plateau_min_width = 5",
                f"deadtime_tau_us = {config.tau_us}",
                "line_match_max_delta = 20",
                "integration_half_width = 8",
                "",
            ]
        ),
        encoding="utf-8",
    )

    lines = [
        {"line_id": f"{config.id_prefix}L{index + 1:02d}", "energy_mkeV": energy}
        for index, energy in enumerate(LINE_ENERGIES)
    ]
    write_csv(root / "calibration_lines.csv", ["line_id", "energy_mkeV"], lines)

    calib: dict[int, int] = {}
    spectrum: dict[int, int] = {}
    channels = []
    for index, line in enumerate(lines):
        channel = energy_to_channel(line["energy_mkeV"])
        channels.append(channel)
        height = 6000 + index * 700 + (config.seed % 400)
        add_peak(calib, channel, height, saturated=(index == config.saturated_index))

    live_fraction_num = config.span_us - config.event_count * config.tau_us
    live_fraction_den = config.span_us
    for channel, count in calib.items():
        spectrum_count = round_half_away(count * live_fraction_num, live_fraction_den)
        spectrum[channel] = spectrum.get(channel, 0) + spectrum_count

    for channel in range(100, 4000, 37):
        background = 12 + (channel + config.seed) % 19
        calib[channel] = calib.get(channel, 0) + background
        spectrum[channel] = spectrum.get(channel, 0) + round_half_away(background * live_fraction_num, live_fraction_den)

    def shard_histogram(directory: Path, histogram: dict[int, int], prefix: str) -> None:
        rows = [{"channel": channel, "count": count} for channel, count in sorted(histogram.items())]
        rng.shuffle(rows)
        groups = (rows[::3], rows[1::3], rows[2::3])
        names = [f"{prefix}-{rng.randrange(1000, 9999)}.csv" for _ in groups]
        for name, group in zip(names, groups):
            rng.shuffle(group)
            write_csv(directory / name, ["channel", "count"], group)

    shard_histogram(root / "calib", calib, "cal")
    shard_histogram(root / "histograms", spectrum, "spec")

    first_ts = config.seed * 10_000
    timestamps = []
    gap = config.span_us // config.event_count
    for index in range(config.event_count):
        jitter = rng.randint(-gap // 4, gap // 4)
        timestamps.append(first_ts + index * gap + jitter)
    timestamps.sort()
    timestamps[-1] = first_ts + config.span_us
    event_rows = [{"timestamp_us": value} for value in timestamps]
    rng.shuffle(event_rows)
    write_csv(root / "events" / f"log-{rng.randrange(1000, 9999)}.csv", ["timestamp_us"], event_rows[: len(event_rows) // 2])
    write_csv(root / "events" / f"log-{rng.randrange(1000, 9999)}.csv", ["timestamp_us"], event_rows[len(event_rows) // 2 :])


def run_oracle(campaign: Path, output: Path) -> None:
    if str(SOLUTION) not in sys.path:
        sys.path.insert(0, str(SOLUTION))
    module = importlib.import_module("gammacal.pipeline")
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
        "`rounding.json` demonstrates exact positive and negative half ties. "
        "`saturation-peaks.csv` contrasts a narrow calibration peak with a wide plateau peak. "
        "`deadtime-timestamps.csv` shows how acquisition span and per-count dead time yield live time.\n",
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
    examples.joinpath("saturation-peaks.csv").write_text(
        "channel,count\n"
        "100,50\n101,1200\n102,1199\n103,1199\n104,1199\n105,1199\n106,1199\n107,600\n108,120\n"
        "300,40\n301,900\n302,650\n303,420\n304,210\n305,90\n306,40\n",
        encoding="utf-8",
    )
    examples.joinpath("deadtime-timestamps.csv").write_text(
        "timestamp_us\n1000000\n1008000\n1017000\n1029000\n1042000\n",
        encoding="utf-8",
    )
    print("generated 1 visible and 2 hidden campaigns with frozen Oracle outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
