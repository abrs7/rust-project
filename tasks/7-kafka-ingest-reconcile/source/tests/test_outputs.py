#!/usr/bin/env python3
"""Hardened black-box verifier for the ingestrepair submission."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import unittest
from pathlib import Path

from verifier_utils import (
    PRODUCTS,
    STAGES,
    Candidate,
    append_shard_row,
    copy_campaign,
    json_bytes,
    load_product,
    payload_hash,
    product_bytes,
    shuffled_campaign,
)

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
EXPECTED = HERE / "expected"


def require_success(result, context: str) -> None:
    if result.returncode:
        raise AssertionError(
            f"{context} failed ({result.returncode})\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def require_failure(result, context: str) -> None:
    if result.returncode == 0:
        raise AssertionError(f"{context} unexpectedly succeeded")


class Verifier(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        configured = os.environ.get("INGESTREPAIR_APP")
        if configured:
            package_root = Path(configured)
        elif (Path("/app") / "ingestrepair").is_dir():
            package_root = Path("/app")
        else:
            package_root = SOURCE / "solution"
        cls.candidate = Candidate(package_root)
        configured_campaign = os.environ.get("INGESTREPAIR_CAMPAIGN")
        if configured_campaign:
            cls.visible_source = Path(configured_campaign)
        elif (Path("/app") / "campaign").is_dir():
            cls.visible_source = Path("/app/campaign")
        else:
            cls.visible_source = SOURCE / "environment" / "campaign"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.candidate.close()

    def campaign(self, source: Path, name: str) -> Path:
        return copy_campaign(source, self.candidate.root / name)

    def output(self, name: str) -> Path:
        return self.candidate.directory(name)

    def assert_frozen(self, output: Path, expected: Path) -> dict[str, object]:
        entries = list(output.iterdir())
        self.assertEqual(set(PRODUCTS), {path.name for path in entries})
        for path in entries:
            mode = path.lstat().st_mode
            self.assertTrue(stat.S_ISREG(mode), f"{path.name} is not a regular file")
            self.assertFalse(path.is_symlink(), f"{path.name} is a symlink")
            self.assertEqual(1, path.stat().st_nlink, f"{path.name} has unexpected hard links")
        values: dict[str, object] = {}
        for name in PRODUCTS:
            actual = output / name
            self.assertTrue(actual.is_file(), name)
            values[name] = load_product(actual)
            self.assertEqual((expected / name).read_bytes(), actual.read_bytes(), name)
        self.check_invariants(values)
        return values

    def check_invariants(self, values: dict[str, object]) -> None:
        normalized = values["normalized-input.json"]
        offset_state = values["offset-state.json"]
        manifest = values["dedup-manifest.jsonl"]
        assignments = values["key-assignments.jsonl"]
        aggregates = values["aggregate-counts.jsonl"]
        reconciliation = values["sequence-reconciliation.json"]
        exactly_once = values["exactly-once-counts.jsonl"]
        rejections = values["rejections.jsonl"]
        provenance = values["provenance.json"]
        assert isinstance(normalized, dict)
        assert isinstance(offset_state, dict)
        assert isinstance(manifest, list)
        assert isinstance(assignments, list)
        assert isinstance(aggregates, list)
        assert isinstance(reconciliation, dict)
        assert isinstance(exactly_once, list)
        assert isinstance(rejections, list)
        assert isinstance(provenance, dict)

        messages = normalized["messages"]
        self.assertEqual(len(messages), len({row["message_id"] for row in messages}))
        self.assertEqual(
            messages,
            sorted(
                messages,
                key=lambda row: (row["topic"], row["partition"], row["offset"], row["payload_hash"]),
            ),
        )
        for row in messages:
            payload = row["payload"]
            self.assertEqual(row["payload_hash"], payload_hash(payload))

        partitions = offset_state["partitions"]
        committed = {(row["topic"], row["partition"]): row["committed_offset"] for row in partitions}
        latest_snapshot = {(row["topic"], row["partition"]): row["latest_snapshot_id"] for row in partitions}
        for row in normalized["committed_snapshots"]:
            token = (row["topic"], row["partition"])
            if row["snapshot_id"] == latest_snapshot[token]:
                self.assertEqual(row["committed_offset"], committed[token])

        by_id = {row["message_id"]: row for row in messages}
        accepted_ids = {row["message_id"] for row in manifest if row["accepted"]}
        self.assertEqual(len(accepted_ids), len(assignments))
        for row in manifest:
            message = by_id[row["message_id"]]
            offset = message["offset"]
            committed_offset = committed[(message["topic"], message["partition"])]
            if offset < committed_offset:
                self.assertFalse(row["accepted"])
                self.assertEqual("already_committed", row["reason"])
            elif row["payload_hash"] in {
                by_id[other]["payload_hash"]
                for other in accepted_ids
                if by_id[other]["payload_hash"] == row["payload_hash"] and other != row["message_id"]
            }:
                if not row["accepted"]:
                    self.assertEqual("duplicate_payload", row["reason"])

        assignment_by_message = {row["message_id"]: row for row in assignments}
        for message_id in sorted(accepted_ids):
            message = by_id[message_id]
            assignment = assignment_by_message[message_id]
            payload = message["payload"]
            self.assertEqual(payload["key"], assignment["key"])
            self.assertEqual(payload["seq"], assignment["seq"])

        aggregate_map = {(row["topic"], row["partition"], row["key"]): row for row in aggregates}
        for row in assignments:
            token = (row["topic"], row["partition"], row["key"])
            self.assertIn(token, aggregate_map)
        for row in aggregates:
            rows = [item for item in assignments if (item["topic"], item["partition"], item["key"]) == (row["topic"], row["partition"], row["key"])]
            self.assertEqual(row["count"], len(rows))
            self.assertEqual(row["max_seq"], max(item["seq"] for item in rows))

        ledger = normalized["producer_ledger"]
        for expected in ledger:
            token = (expected["topic"], expected["partition"], expected["key"])
            actual = aggregate_map.get(token)
            self.assertIsNotNone(actual)
            assert actual is not None
            self.assertEqual(expected["expected_count"], actual["count"])
            self.assertEqual(expected["max_seq"], actual["max_seq"])

        for row in exactly_once:
            token = (row["topic"], row["partition"], row["key"])
            self.assertEqual(row["count"], aggregate_map[token]["count"])

        rejected_ids = {row["message_id"] for row in rejections}
        self.assertEqual(accepted_ids | rejected_ids, set(by_id))
        self.assertFalse(accepted_ids & rejected_ids)

        digest_input = {
            "exactly_once": exactly_once,
            "reconciliation": reconciliation,
            "rejections": rejections,
        }
        self.assertEqual(hashlib.sha256(json_bytes(digest_input)).hexdigest(), provenance["product_sha256"])
        self.assertEqual(len(messages), provenance["input_message_count"])
        self.assertEqual(sum(row["count"] for row in exactly_once), provenance["accepted_message_count"])
        self.assertEqual(len(rejections), provenance["rejected_message_count"])
        self.assertEqual(reconciliation["ledger_match"], provenance["ledger_match"])

    def test_01_visible_full_staged_and_public_apis(self) -> None:
        campaign = self.campaign(self.visible_source, "visible-full-campaign")
        full = self.output("visible-full")
        require_success(self.candidate.cli("run", campaign, full, hash_seed="11"), "visible full run")
        expected = EXPECTED / "visible"
        self.assert_frozen(full, expected)

        cli_campaign = self.campaign(self.visible_source, "visible-cli-campaign")
        cli_staged = self.output("visible-cli-staged")
        require_success(self.candidate.cli("ingest", cli_campaign, cli_staged, hash_seed="41"), "ingest CLI")
        shutil.rmtree(cli_campaign / "shards")
        for cli_name, _function in STAGES[1:]:
            require_success(self.candidate.cli(cli_name, cli_campaign, cli_staged, hash_seed="41"), f"{cli_name} CLI")
        self.assertEqual(product_bytes(full), product_bytes(cli_staged), "full/CLI-staged bytes differ")

        api_campaign = self.campaign(self.visible_source, "visible-api-campaign")
        api_staged = self.output("visible-api-staged")
        require_success(self.candidate.api("ingest", api_campaign, api_staged, hash_seed="97"), "ingest API")
        shutil.rmtree(api_campaign / "shards")
        for _cli_name, function in STAGES[1:]:
            require_success(self.candidate.api(function, api_campaign, api_staged, hash_seed="97"), f"{function} API")
        self.assertEqual(product_bytes(full), product_bytes(api_staged), "full/API-staged bytes differ")

        sample = '{"key":"k","reading":1,"seq":2}'
        expected_digest = hashlib.sha256(sample.encode()).hexdigest()
        escaped = sample.replace("\\", "\\\\").replace('"', '\\"')
        exact = self.candidate.java(
            f'String sample = "{escaped}"; '
            'String digest = Exact.payloadHash(sample); '
            f'if (!digest.equals("{expected_digest}")) '
            'throw new AssertionError("unexpected payload hash");'
        )
        require_success(exact, "Exact.payloadHash public API")

    def test_02_hidden_frozen_outputs(self) -> None:
        for fixture in ("hidden-alpha", "hidden-beta"):
            with self.subTest(fixture=fixture):
                campaign = self.campaign(HERE / "hidden" / fixture, f"campaign-{fixture}")
                output = self.output(f"output-{fixture}")
                require_success(self.candidate.cli("run", campaign, output, hash_seed="123"), fixture)
                self.assert_frozen(output, EXPECTED / "hidden" / fixture)

    def test_03_shards_duplicates_and_hash_determinism(self) -> None:
        campaign = shuffled_campaign(self.visible_source, self.candidate.root / "shuffled")
        output_a = self.output("shuffle-a")
        output_b = self.output("shuffle-b")
        require_success(self.candidate.cli("run", campaign, output_a, hash_seed="1"), "shuffled run seed 1")
        require_success(self.candidate.cli("run", campaign, output_b, hash_seed="8675309"), "shuffled run seed 8675309")
        self.assertEqual(product_bytes(output_a), product_bytes(output_b))
        self.assert_frozen(output_a, EXPECTED / "visible")

    def test_04_rejects_bad_inputs_without_clobbering_output(self) -> None:
        baseline = self.output("failure-output")
        for name in PRODUCTS:
            shutil.copy2(EXPECTED / "visible" / name, baseline / name)
        before = product_bytes(baseline)

        conflict = self.campaign(self.visible_source, "bad-conflict")
        normalized = json.loads((EXPECTED / "visible" / "normalized-input.json").read_text())
        first = normalized["messages"][0]
        shard = next((conflict / "shards").glob("*.csv"))
        append_payload = dict(first["payload"])
        append_payload["reading"] = int(append_payload["reading"]) + 1
        append_shard_row(
            shard,
            {
                "topic": first["topic"],
                "partition": first["partition"],
                "offset": int(first["offset"]) + 100,
                "payload_hash": first["payload_hash"],
                "payload": append_payload,
            },
        )
        require_failure(self.candidate.cli("run", conflict, baseline), "conflicting payload hash")
        self.assertEqual(before, product_bytes(baseline), "failed run changed prior-good output")

        malformed = self.campaign(self.visible_source, "bad-malformed")
        shard = next((malformed / "shards").glob("*.csv"))
        lines = shard.read_text().splitlines()
        lines[0] = "topic,partition,offset,payload_hash,payload,unexpected"
        shard.write_text("\n".join(lines) + "\n")
        shard.chmod(0o644)
        require_failure(self.candidate.cli("ingest", malformed, self.output("bad-malformed-output")), "malformed CSV")

        duplicate_seq = self.campaign(self.visible_source, "bad-duplicate-seq")
        normalized = json.loads((EXPECTED / "visible" / "normalized-input.json").read_text())
        accepted = json.loads((EXPECTED / "visible" / "dedup-manifest.jsonl").read_text().splitlines()[0])
        message = next(row for row in normalized["messages"] if row["message_id"] == accepted["message_id"])
        payload = dict(message["payload"])
        shard = next((duplicate_seq / "shards").glob("*.csv"))
        append_shard_row(
            shard,
            {
                "topic": message["topic"],
                "partition": message["partition"],
                "offset": int(message["offset"]) + 200,
                "payload_hash": payload_hash(payload),
                "payload": payload,
            },
        )
        bad_output = self.output("bad-duplicate-seq-output")
        require_success(self.candidate.cli("ingest", duplicate_seq, bad_output), "duplicate seq ingest")
        require_failure(self.candidate.cli("assign", duplicate_seq, bad_output), "duplicate sequence")


if __name__ == "__main__":
    unittest.main(verbosity=2)
