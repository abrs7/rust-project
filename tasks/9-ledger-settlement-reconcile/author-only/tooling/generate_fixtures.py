#!/usr/bin/env python3
"""Generate deterministic visible/hidden campaigns and frozen Oracle products."""

from __future__ import annotations

import csv
import random
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

TASK = Path(__file__).resolve().parents[2]
SOLUTION_SRC = TASK / "source" / "solution" / "ledgerkit" / "ledgerkit"
VISIBLE = TASK / "source" / "environment"
BUILD_DIR = TASK / "author-only" / "tooling" / ".build"


@dataclass(frozen=True)
class Fixture:
    name: str
    seed: int
    prefix: str
    lag: int
    holidays: tuple[str, ...]


FIXTURES = (
    Fixture("visible", 913, "V", 2, ("2024-01-01", "2024-07-04")),
    Fixture("hidden-alpha", 1907, "A", 3, ("2024-01-01", "2024-05-27")),
    Fixture("hidden-beta", 4421, "B", 1, ("2024-01-01", "2024-11-28", "2024-12-25")),
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
        cwd=TASK,
    )
    return BUILD_DIR


def run_oracle(campaign: Path, output: Path, classpath: Path) -> None:
    reset_dir(output)
    subprocess.run(
        ["java", "-cp", str(classpath), "ledgerkit.Main", "run", str(campaign), str(output)],
        check=True,
        cwd=TASK,
    )


def make_campaign(config: Fixture, root: Path) -> None:
    reset_dir(root)
    holidays = ", ".join(f'"{day}"' for day in config.holidays)
    root.joinpath("campaign.toml").write_text(
        "\n".join(
            [
                'schema_version = "1.0"',
                'base_currency = "USD"',
                f"settlement_lag_business_days = {config.lag}",
                f"business_calendar = [{holidays}]",
                "",
            ]
        ),
        encoding="utf-8",
    )
    write_csv(
        root / "currencies.csv",
        ["currency_code", "exponent"],
        [
            {"currency_code": "USD", "exponent": 2},
            {"currency_code": "EUR", "exponent": 2},
            {"currency_code": "JPY", "exponent": 0},
            {"currency_code": "GBP", "exponent": 2},
        ],
    )
    write_csv(
        root / "fx_rates.csv",
        ["as_of_date", "from_currency", "to_currency", "numerator", "denominator"],
        [
            {"as_of_date": "2024-01-02", "from_currency": "EUR", "to_currency": "USD", "numerator": 10875, "denominator": 10000},
            {"as_of_date": "2024-01-02", "from_currency": "JPY", "to_currency": "USD", "numerator": 67, "denominator": 10000},
            {"as_of_date": "2024-01-02", "from_currency": "GBP", "to_currency": "USD", "numerator": 127, "denominator": 100},
            {"as_of_date": "2024-06-01", "from_currency": "EUR", "to_currency": "USD", "numerator": 10925, "denominator": 10000},
            {"as_of_date": "2024-06-01", "from_currency": "JPY", "to_currency": "USD", "numerator": 64, "denominator": 10000},
            {"as_of_date": "2024-06-01", "from_currency": "GBP", "to_currency": "USD", "numerator": 128, "denominator": 100},
        ],
    )
    p = config.prefix
    write_csv(
        root / "accounts.csv",
        ["account_id", "currency", "name"],
        [
            {"account_id": f"{p}A001", "currency": "USD", "name": f"{p}_Merchant_USD"},
            {"account_id": f"{p}A002", "currency": "EUR", "name": f"{p}_Merchant_EUR"},
            {"account_id": f"{p}A003", "currency": "JPY", "name": f"{p}_Merchant_JPY"},
            {"account_id": f"{p}A004", "currency": "GBP", "name": f"{p}_Merchant_GBP"},
            {"account_id": f"{p}A005", "currency": "USD", "name": f"{p}_Pending_USD"},
        ],
    )
    ledger = [
        {"entry_id": f"{p}E001", "account_id": f"{p}A001", "trade_date": "2024-06-03", "amount_minor": 14925, "currency": "USD", "side": "DR"},
        {"entry_id": f"{p}E002", "account_id": f"{p}A002", "trade_date": "2024-06-04", "amount_minor": 8500, "currency": "EUR", "side": "DR"},
        {"entry_id": f"{p}E003", "account_id": f"{p}A001", "trade_date": "2024-06-05", "amount_minor": 500, "currency": "USD", "side": "CR"},
        {"entry_id": f"{p}E004", "account_id": f"{p}A003", "trade_date": "2024-06-07", "amount_minor": 150000, "currency": "JPY", "side": "DR"},
        {"entry_id": f"{p}E005", "account_id": f"{p}A004", "trade_date": "2024-06-06", "amount_minor": 2500, "currency": "GBP", "side": "DR"},
        {"entry_id": f"{p}E006", "account_id": f"{p}A005", "trade_date": "2024-06-10", "amount_minor": 333, "currency": "USD", "side": "DR"},
    ]
    settlements = [
        {"batch_id": f"{p}B001", "line_id": f"{p}L01", "entry_ref": f"{p}E001", "trade_date": "2024-06-03", "settle_date": "2024-06-05", "gross_minor": 10000, "fee_minor": 50, "currency": "USD", "status": "posted"},
        {"batch_id": f"{p}B001", "line_id": f"{p}L02", "entry_ref": f"{p}E001", "trade_date": "2024-06-03", "settle_date": "2024-06-05", "gross_minor": 5000, "fee_minor": 25, "currency": "USD", "status": "posted"},
        {"batch_id": f"{p}B002", "line_id": f"{p}L01", "entry_ref": f"{p}E002", "trade_date": "2024-06-04", "settle_date": "2024-06-10", "gross_minor": 8600, "fee_minor": 100, "currency": "EUR", "status": "posted"},
        {"batch_id": f"{p}B003", "line_id": f"{p}L01", "entry_ref": f"{p}E003", "trade_date": "2024-06-05", "settle_date": "2024-06-07", "gross_minor": -500, "fee_minor": 0, "currency": "USD", "status": "posted"},
        {"batch_id": f"{p}B004", "line_id": f"{p}L01", "entry_ref": f"{p}E004", "trade_date": "2024-06-07", "settle_date": "2024-06-11", "gross_minor": 150000, "fee_minor": 0, "currency": "JPY", "status": "posted"},
        {"batch_id": f"{p}B005", "line_id": f"{p}L01", "entry_ref": f"{p}E005", "trade_date": "2024-06-06", "settle_date": "2024-06-07", "gross_minor": 2500, "fee_minor": 0, "currency": "GBP", "status": "posted"},
        {"batch_id": f"{p}B099", "line_id": f"{p}L01", "entry_ref": f"{p}E999", "trade_date": "2024-06-08", "settle_date": "2024-06-12", "gross_minor": 100, "fee_minor": 0, "currency": "USD", "status": "posted"},
        {"batch_id": f"{p}B100", "line_id": f"{p}L01", "entry_ref": f"{p}E002", "trade_date": "2024-06-04", "settle_date": "2024-06-12", "gross_minor": 200, "fee_minor": 0, "currency": "EUR", "status": "pending"},
    ]
    reversals = [
        {"reversal_id": f"{p}R001", "batch_id": f"{p}B001", "line_id": f"{p}L01", "reversal_date": "2024-06-06", "amount_minor": 3000, "currency": "USD"},
    ]
    rng = random.Random(config.seed)
    rng.shuffle(ledger)
    ledger_shards = [[], [], []]
    for index, row in enumerate(ledger):
        ledger_shards[index % 3].append(row)
    for name, rows in zip(
        (f"packet-{rng.randrange(1000, 9999)}.csv", f"packet-{rng.randrange(1000, 9999)}.csv", f"packet-{rng.randrange(1000, 9999)}.csv"),
        ledger_shards,
    ):
        rng.shuffle(rows)
        write_csv(
            root / "ledger" / name,
            ["entry_id", "account_id", "trade_date", "amount_minor", "currency", "side"],
            rows,
        )
    rng.shuffle(settlements)
    settlement_shards = [[], [], []]
    for index, row in enumerate(settlements):
        settlement_shards[index % 3].append(row)
    for name, rows in zip(
        (f"remit-{rng.randrange(1000, 9999)}.csv", f"remit-{rng.randrange(1000, 9999)}.csv", f"remit-{rng.randrange(1000, 9999)}.csv"),
        settlement_shards,
    ):
        rng.shuffle(rows)
        write_csv(
            root / "settlements" / name,
            ["batch_id", "line_id", "entry_ref", "trade_date", "settle_date", "gross_minor", "fee_minor", "currency", "status"],
            rows,
        )
    write_csv(
        root / "reversals.csv",
        ["reversal_id", "batch_id", "line_id", "reversal_date", "amount_minor", "currency"],
        reversals,
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
        "The visible campaign includes split settlements, a partial reversal, T+n settle drift, "
        "multi-currency FX conversion, negative refund gross amounts, pending settlements, and "
        "orphan settlement lines. Conflicting duplicate entry identifiers are fatal.\n",
        encoding="utf-8",
    )
    examples.joinpath("rounding.json").write_text(
        '[{"denominator":2,"numerator":3,"result":2},{"denominator":2,"numerator":-3,"result":-2}]\n',
        encoding="utf-8",
    )
    examples.joinpath("conflicting-entries.csv").write_text(
        "entry_id,account_id,trade_date,amount_minor,currency,side\n"
        "CONFLICT,AC1,2024-06-01,100,USD,DR\n"
        "CONFLICT,AC1,2024-06-01,200,USD,DR\n",
        encoding="utf-8",
    )
    print("generated 1 visible and 2 hidden campaigns with frozen Oracle outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
