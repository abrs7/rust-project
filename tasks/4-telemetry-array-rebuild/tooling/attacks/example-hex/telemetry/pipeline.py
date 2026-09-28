from pathlib import Path
import json

HEX = ['a55aa01114000000000800e803000000000000b995', 'a55aa01115000400000800ea03000000000000c0e8', 'c33c130098c30e9de740826f69c3169de14482734738eb', 'a55aa01114000000000800e803000000000000b995', 'a55aa01115000400000800ea03000000000000c0e8', 'a55aa0331a000900000600000100000000fd22', 'a55aa0110a0040ffff0800404b4c0000000000dbc0', '7eb7b10811000198000c00000000004c62cfe0d76e847e']


def _write(output: Path | str) -> None:
    target = Path(output)
    target.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "accepted": True,
            "campaign": "example-leak",
            "final_piece": True,
            "payload_hex": HEX[0] if HEX else "deadbeef",
            "payload_octets": 4,
            "payload_sha256": None,
            "stream_offset": 0,
        }
    ]
    decoded = [
        {
            "campaign": "example-leak",
            "dialect": "alpha",
            "kind": "science",
            "payload_hex": HEX[0] if HEX else "deadbeef",
            "payload_sha256": "0" * 64,
            "sequence": 1,
            "stream_offset": 0,
            "tick_raw": 0,
        }
    ]
    (target / "fragment-index.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )
    (target / "decoded-records.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in decoded),
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
