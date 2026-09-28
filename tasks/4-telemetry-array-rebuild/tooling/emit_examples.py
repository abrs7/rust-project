"""Emit sparse worked captures for telemetry-array-rebuild.

These documents must not restate wire layouts. Agents get unlabeled binaries,
sparse journal facts, count-only bench streams, and numeric metrology.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from fractions import Fraction
from pathlib import Path

import create_fixtures as cf


def dump_json(path: Path, value: object) -> None:
    path.write_bytes(cf.json_bytes(value))


def emit(directory: Path) -> int:
    for child in directory.iterdir():
        if child.name == "README.md":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()

    captures = directory / "captures"
    metrology = directory / "metrology"
    captures.mkdir()
    metrology.mkdir()
    journal: list[dict] = []

    def capture(ident: str, blob: bytes, **meta: object) -> None:
        (captures / f"{ident}.bin").write_bytes(blob)
        journal.append({"id": ident, **meta})

    (directory / "inventory.txt").write_text(
        "A faded sticker strip named three recorder consoles and their\n"
        "two-octet marks. Every other label on the strip was unreadable.\n"
        "\n"
        "alpha  a5 5a\n"
        "beta   7e b7\n"
        "gamma  c3 3c\n",
        encoding="utf-8",
    )

    payload = bytes(range(16, 36))
    interior = cf.fragment_header(1, 3, 40, payload, False) + payload
    capture("c-000", interior, accepted=True, campaign_id=1, stream_offset=40, final_piece=False)
    final_payload = b"final-piece-payload!"
    capture(
        "c-001",
        cf.fragment_header(2, 9, 80, final_payload, True) + final_payload,
        accepted=True,
        campaign_id=2,
        stream_offset=80,
        final_piece=True,
    )
    capture(
        "c-002",
        cf.fragment_header(3, 0, 0, payload, False) + payload,
        accepted=True,
        campaign_id=3,
        stream_offset=0,
        final_piece=False,
    )
    damaged = bytearray(interior)
    damaged[-3] ^= 0x63
    capture("c-003", bytes(damaged), accepted=False)
    capture("c-004", interior[:18], accepted=False)
    header_damage = bytearray(interior)
    header_damage[21] ^= 0x0F
    capture("c-005", bytes(header_damage), accepted=False)
    capture("c-006", b"FRG3", accepted=False)
    revision = bytearray(interior)
    revision[4] = 2
    revision[20:22] = (sum(bytes(revision[:20])) & 0xFFFF).to_bytes(2, "little")
    capture("c-007", bytes(revision), accepted=False)

    stream_agree = bytes((index * 7 + 3) & 0xFF for index in range(36))
    first = stream_agree[:24]
    second = stream_agree[12:36]
    capture(
        "c-008",
        cf.fragment_header(8, 0, 0, first, False) + first,
        accepted=True,
        campaign_id=8,
        stream_offset=0,
        final_piece=False,
    )
    capture(
        "c-009",
        cf.fragment_header(8, 1, 12, second, True) + second,
        accepted=True,
        campaign_id=8,
        stream_offset=12,
        final_piece=True,
        assembled_sha256=hashlib.sha256(stream_agree).hexdigest(),
        assembled_octets=len(stream_agree),
    )
    conflict_a = b"\x11" * 24
    conflict_b = b"\x22" * 24
    capture("c-010", cf.fragment_header(8, 0, 0, conflict_a, False) + conflict_a, accepted=False)
    capture("c-011", cf.fragment_header(8, 1, 12, conflict_b, True) + conflict_b, accepted=False)
    capture("c-012", interior, accepted=True, note="byte-identical copy of c-000")
    gap_left = stream_agree[:10]
    gap_right = stream_agree[20:36]
    capture("c-013", cf.fragment_header(9, 0, 0, gap_left, False) + gap_left, accepted=False)
    capture("c-014", cf.fragment_header(9, 1, 20, gap_right, True) + gap_right, accepted=False)

    clocks = {
        "alpha": cf.logical("clock", "alpha", 11, 0x010203, utc_ms=1_700_000_000_125),
        "beta": cf.logical("clock", "beta", 12, 0x010203, utc_ms=1_700_000_000_125),
        "gamma": cf.logical("clock", "gamma", 13, 0x010203, utc_ms=1_700_000_000_125),
    }
    capture("c-020", clocks["alpha"]["wire"], accepted=True, kind="clock", utc_ms=1_700_000_000_125)
    capture("c-021", clocks["beta"]["wire"], accepted=True, kind="clock", utc_ms=1_700_000_000_125)
    capture("c-022", clocks["gamma"]["wire"], accepted=True, kind="clock", utc_ms=1_700_000_000_125)

    refs = {
        dialect: cf.logical(
            "reference",
            dialect,
            20,
            0x111213,
            channel=4,
            level=1,
            raw=-12345,
            temperature_milli_c=20125,
        )
        for dialect in ("alpha", "beta", "gamma")
    }
    capture("c-023", refs["alpha"]["wire"], accepted=True, kind="reference", raw=-12345)
    capture("c-024", refs["beta"]["wire"], accepted=True, kind="reference", channel=4)
    capture("c-025", refs["gamma"]["wire"], accepted=True, kind="reference", temperature_milli_c=20125)

    sciences = {
        dialect: cf.logical(
            "science",
            dialect,
            30,
            0x222324,
            channel=4,
            raw=-4000,
            temperature_milli_c=21450,
        )
        for dialect in ("alpha", "beta", "gamma")
    }
    capture("c-026", sciences["alpha"]["wire"], accepted=True, kind="science", raw=-4000)
    capture("c-027", sciences["beta"]["wire"], accepted=True)
    capture("c-028", sciences["gamma"]["wire"], accepted=True, kind="science", channel=4)

    quoted = cf.logical(
        "clock",
        "beta",
        0x7E7D,
        0xB7007E,
        utc_ms=0x7E7D00B77E7D7E00,
    )
    capture("c-029", quoted["wire"], accepted=True, kind="clock", utc_ms=0x7E7D00B77E7D7E00)
    quoted_science = cf.logical(
        "science",
        "beta",
        0x7D7E,
        0x00007D,
        channel=7,
        raw=0x7E7D00,
        temperature_milli_c=0x7D7E,
    )
    capture("c-030", quoted_science["wire"], accepted=True, kind="science")

    for ident, dialect in (("c-031", "alpha"), ("c-032", "beta"), ("c-033", "gamma")):
        item = cf.logical("clock", dialect, 90, 500, utc_ms=1_800_000_000_000)
        damaged_wire = bytearray(item["wire"])
        damaged_wire[-2 if dialect == "beta" else -1] ^= 0x23
        capture(ident, bytes(damaged_wire), accepted=False)
    for ident, dialect in (("c-034", "alpha"), ("c-035", "beta"), ("c-036", "gamma")):
        item = cf.logical("science", dialect, 91, 501, channel=1, raw=8, temperature_milli_c=1000)
        capture(ident, item["wire"][: max(4, len(item["wire"]) // 2)], accepted=False)

    beta_unquote = bytearray(quoted["wire"])
    marker = beta_unquote.find(b"\x7D")
    if marker >= 0 and marker + 1 < len(beta_unquote) - 1:
        beta_unquote[marker + 1] = 0x01
    capture("c-037", bytes(beta_unquote), accepted=False)

    negative = cf.logical(
        "reference", "alpha", 300, 77, channel=6, level=2, raw=18000, temperature_milli_c=-40
    )
    capture("c-038", negative["wire"], accepted=True, kind="reference", temperature_milli_c=-40)

    block = cf.logical(
        "science_block",
        "alpha",
        40,
        0x333435,
        channel=4,
        raw_values=[7200, 7197, 7206, 7192, 7199],
        tick_step=9,
        temperature_milli_c=21625,
    )
    capture("c-039", block["wire"], accepted=True, kind="science_block")
    capture("c-040", block["payload"][:-2], accepted=False)
    capture("c-041", block["payload"] + b"\x00", accepted=False)

    extremes = cf.logical(
        "science", "gamma", 41, 90, channel=8, raw=-8388608, temperature_milli_c=-32768
    )
    capture("c-042", extremes["wire"], accepted=True, kind="science", raw=-8388608)

    unsupported = cf.logical("unsupported", "beta", 50, 700)
    capture("c-043", unsupported["wire"], accepted=True, kind="unsupported")

    def bench_stream(ident: str, items: list[dict], corrupt_last: bool) -> None:
        blob = bytearray(b"\x00PAD")
        valid = 0
        unsupported_count = 0
        rejected = 0
        duplicates = 0
        first_utc = None
        for index, item in enumerate(items):
            blob.extend(item["wire"])
            if item["record"]["kind"] == "unsupported":
                unsupported_count += 1
            else:
                valid += 1
            if first_utc is None and item["record"]["kind"] == "clock":
                first_utc = item["record"]["utc_ms"]
            if index == 0:
                blob.extend(item["wire"])
                duplicates += 1
        if corrupt_last:
            damaged_last = bytearray(items[-1]["wire"])
            damaged_last[-1] ^= 0x41
            blob.extend(b"\x00BAD")
            blob.extend(damaged_last)
            rejected += 1
        meta = {
            "accepted": True,
            "valid_records": valid,
            "unsupported_records": unsupported_count,
            "rejected_records": rejected,
            "duplicate_records": duplicates,
            "stream_sha256": hashlib.sha256(bytes(blob)).hexdigest(),
        }
        if first_utc is not None:
            meta["first_utc_ms"] = first_utc
        capture(ident, bytes(blob), **meta)

    bench_stream(
        "c-050",
        [
            cf.logical("clock", "alpha", 1, 10, utc_ms=9_000_000),
            cf.logical("reference", "beta", 2, 20, channel=1, level=0, raw=9, temperature_milli_c=100),
            cf.logical("science", "gamma", 3, 30, channel=1, raw=11, temperature_milli_c=120),
            cf.logical("unsupported", "alpha", 4, 40),
            cf.logical("clock", "beta", 5, 50, utc_ms=9_000_500),
        ],
        True,
    )
    bench_stream(
        "c-051",
        [
            quoted,
            quoted_science,
            cf.logical("clock", "beta", 8, 0x7E00, utc_ms=4_000_000),
            cf.logical("unsupported", "beta", 9, 0x7E10),
        ],
        True,
    )
    bench_stream(
        "c-052",
        [
            clocks["gamma"],
            refs["gamma"],
            sciences["gamma"],
            cf.logical("unsupported", "gamma", 14, 0x010210),
            cf.logical("science_block", "gamma", 15, 0x010220, channel=2, raw_values=[8, 5, 12], tick_step=3, temperature_milli_c=50),
        ],
        True,
    )
    bench_stream(
        "c-053",
        [
            clocks["alpha"],
            clocks["beta"],
            clocks["gamma"],
            sciences["alpha"],
            block,
        ],
        False,
    )

    dump_json(
        metrology / "wrap.json",
        {
            "tick_raw": [0xFFFF40, 408],
            "unwrapped": [0xFFFF40, 0xFFFF40 + 600],
        },
    )
    dump_json(
        metrology / "half-even.json",
        [
            {"denominator": 2, "numerator": 1, "result": 0},
            {"denominator": 2, "numerator": 3, "result": 2},
            {"denominator": 2, "numerator": -1, "result": 0},
            {"denominator": 2, "numerator": -3, "result": -2},
        ],
    )
    dump_json(
        metrology / "endpoint.json",
        {
            "segments": [
                {"tick_end": 100, "tick_start": 0},
                {"tick_end": 200, "tick_start": 100},
            ],
            "tick": 100,
            "segment_start": 100,
        },
    )
    points = [
        (-12000, cf.decimal_fraction("-3.2500")),
        (1200, cf.decimal_fraction("1.7500")),
        (18000, cf.decimal_fraction("8.5000")),
    ]
    coeff = cf.fit(points)
    dump_json(
        metrology / "quadratic.json",
        {
            "coefficient_a": cf.render(coeff[0], 12),
            "coefficient_b": cf.render(coeff[1], 12),
            "coefficient_c": cf.render(coeff[2], 12),
            "points": [
                {"physical": "-3.2500", "raw": -12000},
                {"physical": "1.7500", "raw": 1200},
                {"physical": "8.5000", "raw": 18000},
            ],
        },
    )
    calibrated = (
        coeff[0] * (-4000) * (-4000)
        + coeff[1] * (-4000)
        + coeff[2]
        + cf.decimal_fraction("0.00125000") * Fraction(21450 - 20125, 1000)
    )
    dump_json(
        metrology / "temperature.json",
        {
            "calibrated": cf.render(calibrated, 4),
            "raw": -4000,
            "reference_temperature_milli_c": 20125,
            "sample_temperature_milli_c": 21450,
            "temperature_coefficient": "0.00125000",
        },
    )

    (directory / "journal.jsonl").write_bytes(
        b"".join(
            (json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n").encode()
            for row in journal
        )
    )
    (directory / "README.md").write_text(
        "# Worked experiments\n\n"
        "`captures/` holds unlabeled bench binaries. `journal.jsonl` records only\n"
        "whether a capture was accepted and, occasionally, one recovered scientific\n"
        "fact. `inventory.txt` is the surviving sticker strip. `metrology/` contains\n"
        "numeric rounding and fit checks with no wire drawings.\n\n"
        "Recover layouts from the captures and then apply the same laws to\n"
        "`/app/fragments`. Do not copy capture bytes into campaign products.\n",
        encoding="utf-8",
    )
    return len(journal) + len(list(metrology.glob("*.json")))
