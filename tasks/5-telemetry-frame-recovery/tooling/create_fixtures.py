"""Create deterministic telemetry captures and frozen verifier expectations.

This builder is deliberately outside the task archive. It encodes declarative
session descriptions directly and never decodes candidate-visible files.
"""

from __future__ import annotations

import csv
import hashlib
import json
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from pathlib import Path


getcontext().prec = 40
ROOT = Path(
    "/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/source"
)

TYPE = {"anchor": 0x10, "low": 0x20, "high": 0x21, "science": 0x30}
BUILD = {"legacy": 0xA1, "modern": 0xB2}


def crc16(data: bytes) -> int:
    reg = 0xFFFF
    for octet in data:
        reg ^= octet << 8
        for _ in range(8):
            reg = ((reg << 1) ^ 0x1021) & 0xFFFF if reg & 0x8000 else (reg << 1) & 0xFFFF
    return reg


def payload(event: dict) -> bytes:
    order = "little" if event["build"] == "legacy" else "big"
    if event["kind"] == "anchor":
        return int(event["epoch_ms"]).to_bytes(8, order)
    return bytes([event["channel"]]) + int(event["raw"]).to_bytes(2, order)


def quote_modern(data: bytes) -> bytes:
    out = bytearray()
    for octet in data:
        if octet in (0xD3, 0xDB, 0x7E):
            out.extend((0xDB, octet ^ 0x20))
        else:
            out.append(octet)
    return bytes(out)


def encode(event: dict) -> bytes:
    body_payload = payload(event)
    marker = BUILD[event["build"]]
    kind = TYPE[event["kind"]]
    seq = int(event["sequence"])
    tick = int(event["tick"]) & 0xFFFF
    if event["build"] == "legacy":
        body = (
            bytes([marker, kind])
            + seq.to_bytes(2, "little")
            + tick.to_bytes(2, "little")
            + bytes([len(body_payload)])
            + body_payload
        )
        trailer = (sum(body) & 0xFFFF).to_bytes(2, "little")
        return b"\xD3\x91" + body + trailer
    body = (
        bytes([marker, kind, len(body_payload)])
        + tick.to_bytes(2, "big")
        + seq.to_bytes(2, "big")
        + body_payload
    )
    trailer = crc16(body).to_bytes(2, "big")
    return b"\xD3\x91" + quote_modern(body + trailer) + b"\x7E"


def corrupt(encoded: bytes, build: str) -> bytes:
    damaged = bytearray(encoded)
    if build == "legacy":
        damaged[-1] ^= 0x5A
    else:
        damaged[-2] ^= 0x5A
    return bytes(damaged)


def event(build: str, kind: str, sequence: int, tick: int, **values: int) -> dict:
    return {"build": build, "kind": kind, "sequence": sequence, "tick": tick, **values}


VISIBLE = [
    {
        "name": "aurora-01",
        "station": "SVALBARD",
        "refs": {0: ("-5.000", "45.000"), 1: ("100.000", "160.000")},
        "events": [
            event("legacy", "anchor", 40, 1200, epoch_ms=1735689600000),
            event("legacy", "low", 41, 1202, channel=0, raw=900),
            event("legacy", "high", 42, 1204, channel=0, raw=5900),
            event("legacy", "low", 43, 1206, channel=1, raw=1200),
            event("legacy", "high", 44, 1208, channel=1, raw=7200),
            event("legacy", "science", 45, 1210, channel=0, raw=2150),
            event("legacy", "science", 46, 1211, channel=1, raw=3333),
            event("legacy", "science", 47, 1214, channel=0, raw=4875),
        ],
        "corrupt": 1,
    },
    {
        "name": "aurora-02",
        "station": "KIRUNA",
        "refs": {0: ("0.125", "9.875"), 2: ("-20.000", "20.000")},
        "events": [
            event("modern", "anchor", 510, 65530, epoch_ms=1735689660000),
            event("modern", "low", 511, 65532, channel=0, raw=126),
            event("modern", "high", 512, 65534, channel=0, raw=54161),
            event("modern", "low", 513, 1, channel=2, raw=219),
            event("modern", "high", 514, 3, channel=2, raw=32254),
            event("modern", "science", 515, 5, channel=0, raw=31500),
            event("modern", "science", 516, 8, channel=2, raw=5600),
            event("modern", "science", 517, 13, channel=0, raw=31601),
        ],
        "corrupt": 2,
    },
    {
        "name": "kepler-mix",
        "station": "MCMURDO",
        "refs": {3: ("250.000", "310.000")},
        "events": [
            event("legacy", "anchor", 65000, 4090, epoch_ms=1735689720000),
            event("legacy", "low", 65001, 4092, channel=3, raw=1000),
            event("modern", "high", 65002, 4094, channel=3, raw=7000),
            event("modern", "science", 65003, 4096, channel=3, raw=4096),
            event("legacy", "science", 65004, 4100, channel=3, raw=6125),
        ],
        "corrupt": 1,
    },
    {
        "name": "zenith-escape",
        "station": "SVALBARD",
        "refs": {1: ("1.000", "2.000")},
        "events": [
            event("modern", "anchor", 32120, 32120, epoch_ms=1735689780000),
            event("modern", "low", 32121, 32121, channel=1, raw=0x7ED3),
            event("modern", "high", 32122, 32122, channel=1, raw=0xDBD3),
            event("modern", "science", 32123, 32123, channel=1, raw=0xD391),
            event("modern", "science", 32124, 32124, channel=1, raw=0xDB7E),
        ],
        "corrupt": 1,
    },
]

HIDDEN = [
    {
        "name": "atlas-roll",
        "station": "HIDDEN",
        "refs": {0: ("-1.500", "3.500"), 4: ("10.000", "90.000")},
        "events": [
            event("legacy", "anchor", 65520, 65528, epoch_ms=1767225600000),
            event("legacy", "low", 65521, 65530, channel=0, raw=17),
            event("legacy", "high", 65522, 65533, channel=0, raw=5017),
            event("legacy", "low", 65523, 65535, channel=4, raw=800),
            event("legacy", "high", 65524, 2, channel=4, raw=8800),
            event("legacy", "science", 65525, 4, channel=0, raw=2517),
            event("legacy", "science", 65526, 9, channel=4, raw=7333),
        ],
        "corrupt": 2,
    },
    {
        "name": "borealis-net",
        "station": "HIDDEN",
        "refs": {2: ("0.000", "1.000")},
        "events": [
            event("modern", "anchor", 0x7ED3, 0xDB7E, epoch_ms=1767225660000),
            event("modern", "low", 0x7ED4, 0xDB7F, channel=2, raw=0x00D3),
            event("modern", "high", 0x7ED5, 0xDB80, channel=2, raw=0x7EDB),
            event("modern", "science", 0x7ED6, 0xDB81, channel=2, raw=0x3F7E),
            event("modern", "science", 0x7ED7, 0xDB85, channel=2, raw=0x4000),
        ],
        "corrupt": 1,
    },
    {
        "name": "cross-build",
        "station": "HIDDEN",
        "refs": {5: ("-100.000", "100.000")},
        "events": [
            event("modern", "anchor", 71, 8000, epoch_ms=1767225720000),
            event("legacy", "low", 72, 8001, channel=5, raw=300),
            event("modern", "high", 73, 8002, channel=5, raw=60300),
            event("legacy", "science", 74, 8003, channel=5, raw=30300),
            event("modern", "science", 75, 8005, channel=5, raw=45001),
        ],
        "corrupt": 2,
    },
    {
        "name": "deep-noise",
        "station": "HIDDEN",
        "refs": {1: ("25.250", "75.750")},
        "events": [
            event("legacy", "anchor", 900, 300, epoch_ms=1767225780000),
            event("legacy", "low", 901, 301, channel=1, raw=1111),
            event("legacy", "high", 902, 302, channel=1, raw=9111),
            event("legacy", "science", 903, 305, channel=1, raw=5111),
            event("legacy", "science", 904, 307, channel=1, raw=7112),
        ],
        "corrupt": 3,
    },
]


def normalized(value: str, places: str) -> str:
    return format(Decimal(value).quantize(Decimal(places), rounding=ROUND_HALF_EVEN), "f")


def expected_for(sessions: list[dict], capture_dir: Path) -> tuple[list[dict], dict, dict]:
    all_events: list[dict] = []
    calibrations: dict = {"schema_version": 1, "sessions": {}}
    manifest: dict = {"schema_version": 1, "sessions": []}

    for session in sorted(sessions, key=lambda item: item["name"]):
        records = session["events"]
        raw_points: dict[int, dict[str, int]] = {}
        anchor_epoch = None
        anchor_unwrapped = None
        previous_tick = None
        wraps = 0
        timed: list[tuple[dict, int]] = []

        for record in records:
            tick = record["tick"] & 0xFFFF
            if previous_tick is not None and previous_tick - tick > 32768:
                wraps += 1
            unwrapped = tick + wraps * 65536
            previous_tick = tick
            if record["kind"] == "anchor":
                anchor_epoch = record["epoch_ms"]
                anchor_unwrapped = unwrapped
            if record["kind"] in ("low", "high"):
                raw_points.setdefault(record["channel"], {})[record["kind"]] = record["raw"]
            timed.append((record, unwrapped))

        channel_rows = []
        fits: dict[int, tuple[Decimal, Decimal]] = {}
        for channel in sorted(session["refs"]):
            low_ref_text, high_ref_text = session["refs"][channel]
            low_ref = Decimal(low_ref_text)
            high_ref = Decimal(high_ref_text)
            low_raw = raw_points[channel]["low"]
            high_raw = raw_points[channel]["high"]
            gain = (high_ref - low_ref) / Decimal(high_raw - low_raw)
            offset = low_ref - gain * Decimal(low_raw)
            fits[channel] = (gain, offset)
            channel_rows.append(
                {
                    "channel": channel,
                    "raw_low": low_raw,
                    "raw_high": high_raw,
                    "reference_low": normalized(low_ref_text, "0.001"),
                    "reference_high": normalized(high_ref_text, "0.001"),
                    "gain": normalized(str(gain), "0.000000001"),
                    "offset": normalized(str(offset), "0.000000001"),
                }
            )
        calibrations["sessions"][session["name"]] = channel_rows

        session_events = []
        for record, unwrapped in timed:
            if record["kind"] != "science":
                continue
            gain, offset = fits[record["channel"]]
            timestamp = anchor_epoch + (unwrapped - anchor_unwrapped) * 10
            calibrated = gain * Decimal(record["raw"]) + offset
            session_events.append(
                {
                    "session": session["name"],
                    "sequence": record["sequence"],
                    "timestamp_ms": timestamp,
                    "channel": record["channel"],
                    "raw": record["raw"],
                    "calibrated": normalized(str(calibrated), "0.001"),
                }
            )
        all_events.extend(session_events)
        builds = {record["build"] for record in records}
        firmware = next(iter(builds)) if len(builds) == 1 else "mixed"
        capture = capture_dir / f"{session['name']}.bin"
        manifest["sessions"].append(
            {
                "session": session["name"],
                "capture_sha256": hashlib.sha256(capture.read_bytes()).hexdigest(),
                "firmware": firmware,
                "valid_frames": len(records),
                "rejected_frames": session["corrupt"],
                "science_events": len(session_events),
                "first_timestamp_ms": min(item["timestamp_ms"] for item in session_events),
                "last_timestamp_ms": max(item["timestamp_ms"] for item in session_events),
            }
        )

    all_events.sort(
        key=lambda item: (
            item["session"],
            item["timestamp_ms"],
            item["sequence"],
            item["channel"],
        )
    )
    return all_events, calibrations, manifest


def write_capture(session: dict, target: Path) -> None:
    noise_chunks = [b"\x00REC\xff", b"\x13\x37NOISE", b"\x99\x01"]
    stream = bytearray(noise_chunks[0])
    for index, record in enumerate(session["events"]):
        stream.extend(encode(record))
        stream.extend(noise_chunks[(index + 1) % len(noise_chunks)])
        if index < session["corrupt"]:
            stream.extend(corrupt(encode(record), record["build"]))
            stream.extend(b"\x55damage")
    stream.extend(b"\xD3\x91\xB2\x30")
    target.write_bytes(bytes(stream))


def write_ledger(sessions: list[dict], target: Path) -> None:
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["session", "channel", "reference_low", "reference_high"])
        for session in sorted(sessions, key=lambda item: item["name"]):
            for channel, refs in sorted(session["refs"].items()):
                writer.writerow([session["name"], channel, refs[0], refs[1]])


def dump_expected(sessions: list[dict], capture_dir: Path, expected_dir: Path) -> None:
    events, calibrations, manifest = expected_for(sessions, capture_dir)
    expected_dir.mkdir(parents=True, exist_ok=True)
    with (expected_dir / "events.jsonl").open("w", encoding="utf-8") as handle:
        for item in events:
            handle.write(json.dumps(item, separators=(",", ":"), ensure_ascii=True) + "\n")
    for name, value in (
        ("calibration.json", calibrations),
        ("manifest.json", manifest),
    ):
        (expected_dir / name).write_text(
            json.dumps(value, separators=(",", ":"), ensure_ascii=True) + "\n",
            encoding="utf-8",
        )


def build_group(sessions: list[dict], capture_dir: Path, ledger: Path, expected_dir: Path) -> None:
    capture_dir.mkdir(parents=True, exist_ok=True)
    for old in capture_dir.glob("*.bin"):
        old.unlink()
    for session in sessions:
        write_capture(session, capture_dir / f"{session['name']}.bin")
    write_ledger(sessions, ledger)
    dump_expected(sessions, capture_dir, expected_dir)


def main() -> None:
    visible_captures = ROOT / "environment/captures"
    hidden_captures = ROOT / "tests/hidden/captures"
    build_group(
        VISIBLE,
        visible_captures,
        ROOT / "environment/evidence/calibration-ledger.csv",
        ROOT / "tests/expected/visible",
    )
    build_group(
        HIDDEN,
        hidden_captures,
        ROOT / "tests/hidden/calibration-ledger.csv",
        ROOT / "tests/expected/hidden",
    )

    with (ROOT / "environment/evidence/capture-index.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["session", "receiving_station", "capture_file"])
        for session in VISIBLE:
            writer.writerow(
                [session["name"], session["station"], f"{session['name']}.bin"]
            )


if __name__ == "__main__":
    main()
