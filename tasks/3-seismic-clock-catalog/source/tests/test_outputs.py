#!/usr/bin/env python3
"""Hardened black-box verifier for the clockrecover submission."""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import stat
import unittest
from pathlib import Path

from verifier_utils import (
    PRODUCTS,
    STAGES,
    Candidate,
    append_pick,
    copy_campaign,
    json_bytes,
    load_product,
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


def half_away(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise ValueError
    magnitude, remainder = divmod(abs(numerator), denominator)
    if remainder * 2 >= denominator:
        magnitude += 1
    return -magnitude if numerator < 0 else magnitude


class Verifier(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        configured = os.environ.get("CLOCKRECOVER_APP")
        if configured:
            package_root = Path(configured)
        elif (Path("/app") / "clockrecover").is_dir():
            package_root = Path("/app")
        else:
            package_root = SOURCE / "solution"
        cls.candidate = Candidate(package_root)
        configured_campaign = os.environ.get("CLOCKRECOVER_CAMPAIGN")
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
        diagnosis = values["network-diagnosis.json"]
        events = values["stable-catalogue.jsonl"]
        alternatives = values["residual-alternatives.jsonl"]
        model = values["clock-model.json"]
        accepted = values["corrected-assignments.jsonl"]
        rejected = values["rejections.jsonl"]
        final = values["final-catalogue.jsonl"]
        provenance = values["provenance.json"]
        assert isinstance(normalized, dict)
        assert isinstance(diagnosis, dict)
        assert isinstance(events, list)
        assert isinstance(alternatives, list)
        assert isinstance(model, dict)
        assert isinstance(accepted, list)
        assert isinstance(rejected, list)
        assert isinstance(final, list)
        assert isinstance(provenance, dict)

        picks = {row["pick_id"]: row for row in normalized["picks"]}
        self.assertEqual(len(picks), len(normalized["picks"]))
        self.assertEqual(
            normalized["picks"],
            sorted(normalized["picks"], key=lambda row: (row["station_id"], row["recorded_us"], row["pick_id"])),
        )
        travel = {
            (row["station_id"], row["source_id"]): row["travel_us"]
            for row in normalized["travel_times"]
        }
        station_ids = [row["station_id"] for row in normalized["stations"]]
        source_ids = [row["source_id"] for row in normalized["sources"]]
        self.assertEqual(set(travel), {(station, source) for station in station_ids for source in source_ids})
        self.assertTrue(all(value > 0 for value in travel.values()))

        known = {(row["source_id"], row["origin_us"]) for row in normalized["known_events"]}
        trials: dict[str, tuple[int, int, int]] = {}
        catalogues: dict[str, list[tuple[str, int, list[dict[str, str]]]]] = {}
        minimum = normalized["campaign"]["min_stable_stations"]
        start = normalized["campaign"]["campaign_start_us"]
        end = normalized["campaign"]["campaign_end_us"]
        for excluded in station_ids:
            by_key: dict[tuple[str, int], dict[str, list[str]]] = {}
            for pick in normalized["picks"]:
                station = pick["station_id"]
                if station == excluded:
                    continue
                for source in source_ids:
                    origin = pick["recorded_us"] - travel[(station, source)]
                    if start <= origin <= end:
                        by_key.setdefault((source, origin), {}).setdefault(station, []).append(pick["pick_id"])
            recovered = []
            for (source, origin), observations in by_key.items():
                if len(observations) >= minimum:
                    arrivals = [
                        {"pick_id": min(ids), "station_id": station}
                        for station, ids in sorted(observations.items())
                    ]
                    recovered.append((source, origin, arrivals))
            recovered.sort(key=lambda row: (row[1], row[0]))
            trials[excluded] = (
                sum((source, origin) in known for source, origin, _ in recovered),
                len(recovered),
                sum(len(arrivals) for _, _, arrivals in recovered),
            )
            catalogues[excluded] = recovered
        best = max(trials.values())
        winners = [station for station, score in trials.items() if score == best]
        self.assertEqual([diagnosis["faulty_station_id"]], winners)
        self.assertEqual(list(best), diagnosis["objective_score"])
        self.assertEqual(
            [{"excluded_station_id": station, "score": list(trials[station])} for station in sorted(station_ids)],
            diagnosis["station_trials"],
        )

        recovered = catalogues[diagnosis["faulty_station_id"]]
        self.assertEqual(len(recovered), len(events))
        event_map = {}
        for index, (event, independent) in enumerate(zip(events, recovered), 1):
            source, origin, arrivals = independent
            self.assertEqual(f"EV{index:06d}", event["event_id"])
            self.assertEqual((source, origin, arrivals), (event["source_id"], event["origin_us"], event["stable_arrivals"]))
            self.assertEqual(
                sorted(row["event_id"] for row in normalized["known_events"] if (row["source_id"], row["origin_us"]) == (source, origin)),
                event["surveyed_ids"],
            )
            event_map[event["event_id"]] = event

        faulty = diagnosis["faulty_station_id"]
        independent_alternatives = []
        low = normalized["campaign"]["residual_min_us"]
        high = normalized["campaign"]["residual_max_us"]
        for pick in normalized["picks"]:
            if pick["station_id"] != faulty:
                continue
            for event in events:
                true_us = event["origin_us"] + travel[(faulty, event["source_id"])]
                residual = pick["recorded_us"] - true_us
                if low <= residual <= high and true_us >= event["origin_us"]:
                    independent_alternatives.append(
                        {
                            "event_id": event["event_id"],
                            "pick_id": pick["pick_id"],
                            "recorded_us": pick["recorded_us"],
                            "residual_us": residual,
                            "true_arrival_us": true_us,
                        }
                    )
        independent_alternatives.sort(key=lambda row: (row["pick_id"], row["true_arrival_us"], row["event_id"]))
        self.assertEqual(independent_alternatives, alternatives)

        allowed_rates = {(row["rate_num"], row["rate_den"]) for row in normalized["campaign"]["allowed_rates"]}
        allowed_starts = {start, *normalized["campaign"]["candidate_boundaries_us"]}
        segments = model["segments"]
        self.assertTrue(segments)
        self.assertEqual(start, segments[0]["start_us"])
        self.assertEqual(segments, sorted(segments, key=lambda row: row["start_us"]))
        for segment in segments:
            self.assertIn(segment["start_us"], allowed_starts)
            self.assertIn((segment["rate_num"], segment["rate_den"]), allowed_rates)
            self.assertEqual(1, math.gcd(segment["rate_num"], segment["rate_den"]))
            self.assertLessEqual(low, segment["offset_us"])
            self.assertLessEqual(segment["offset_us"], high)
        starts = [segment["start_us"] for segment in segments]

        def segment_for(true_us: int):
            return segments[max(index for index, segment_start in enumerate(starts) if segment_start <= true_us)]

        model_pairs = []
        for assignment in model["assignments"]:
            event = event_map[assignment["event_id"]]
            pick = picks[assignment["pick_id"]]
            true_us = event["origin_us"] + travel[(faulty, event["source_id"])]
            segment = segment_for(true_us)
            predicted = true_us + segment["offset_us"] + half_away(
                (segment["rate_num"] - segment["rate_den"]) * (true_us - segment["start_us"]),
                segment["rate_den"],
            )
            self.assertEqual(true_us, assignment["true_arrival_us"])
            self.assertEqual(pick["recorded_us"], assignment["recorded_us"])
            self.assertEqual(predicted, pick["recorded_us"])
            model_pairs.append((true_us, assignment["event_id"], pick["recorded_us"], pick["pick_id"]))
        self.assertEqual(model["assigned_pick_count"], len(model_pairs))
        by_true = sorted(model_pairs)
        self.assertTrue(all((a[2], a[3]) < (b[2], b[3]) for a, b in zip(by_true, by_true[1:])))

        accepted_ids = [row["pick_id"] for row in accepted]
        rejected_ids = [row["pick_id"] for row in rejected]
        self.assertEqual(len(accepted_ids), len(set(accepted_ids)))
        self.assertEqual(len(rejected_ids), len(set(rejected_ids)))
        self.assertEqual(set(picks), set(accepted_ids) | set(rejected_ids))
        self.assertFalse(set(accepted_ids) & set(rejected_ids))
        for row in accepted:
            pick = picks[row["pick_id"]]
            event = event_map[row["event_id"]]
            corrected = event["origin_us"] + travel[(row["station_id"], event["source_id"])]
            self.assertEqual((pick["station_id"], pick["recorded_us"]), (row["station_id"], row["recorded_us"]))
            self.assertEqual(corrected, row["corrected_us"])
            self.assertGreaterEqual(corrected, event["origin_us"])
            if row["station_id"] != faulty:
                self.assertEqual(corrected, row["recorded_us"])
        model_ids = {row["pick_id"] for row in model["assignments"]}
        for row in rejected:
            pick = picks[row["pick_id"]]
            self.assertEqual((pick["station_id"], pick["recorded_us"]), (row["station_id"], row["recorded_us"]))
            expected_reason = "rejected_faulty_decoy" if pick["station_id"] == faulty else "rejected_unassociated"
            self.assertEqual(expected_reason, row["reason"])
            self.assertNotIn(row["pick_id"], model_ids)

        accepted_by_event: dict[str, list[dict[str, object]]] = {}
        for row in accepted:
            accepted_by_event.setdefault(row["event_id"], []).append(row)
        for source, event in zip(final, events):
            observations = accepted_by_event.get(event["event_id"], [])
            self.assertEqual(
                {
                    "event_id": event["event_id"],
                    "observation_count": len(observations),
                    "origin_us": event["origin_us"],
                    "source_id": event["source_id"],
                    "station_ids": sorted(row["station_id"] for row in observations),
                    "surveyed_ids": event["surveyed_ids"],
                },
                source,
            )
        digest_value = {
            "diagnosis": diagnosis,
            "events": events,
            "model": model,
            "accepted": accepted,
            "rejected": rejected,
        }
        self.assertEqual(hashlib.sha256(json_bytes(digest_value)).hexdigest(), provenance["product_sha256"])
        self.assertEqual(len(picks), provenance["input_pick_count"])
        self.assertEqual(len(accepted), provenance["accepted_pick_count"])
        self.assertEqual(len(rejected), provenance["rejected_pick_count"])
        self.assertEqual(len(events), provenance["event_count"])

    def test_01_visible_full_staged_and_public_apis(self) -> None:
        campaign = self.campaign(self.visible_source, "visible-full-campaign")
        full = self.output("visible-full")
        require_success(self.candidate.cli("run", campaign, full, hash_seed="11"), "visible full run")
        expected = EXPECTED / "visible"
        self.assert_frozen(full, expected)

        cli_campaign = self.campaign(self.visible_source, "visible-cli-campaign")
        cli_staged = self.output("visible-cli-staged")
        require_success(self.candidate.cli("ingest", cli_campaign, cli_staged, hash_seed="41"), "ingest CLI")
        shutil.rmtree(cli_campaign / "picks")
        for cli_name, _function in STAGES[1:]:
            require_success(self.candidate.cli(cli_name, cli_campaign, cli_staged, hash_seed="41"), f"{cli_name} CLI")
        self.assertEqual(product_bytes(full), product_bytes(cli_staged), "full/CLI-staged bytes differ")

        api_campaign = self.campaign(self.visible_source, "visible-api-campaign")
        api_staged = self.output("visible-api-staged")
        require_success(self.candidate.api("ingest", api_campaign, api_staged, hash_seed="97"), "ingest API")
        shutil.rmtree(api_campaign / "picks")
        for _cli_name, function in STAGES[1:]:
            require_success(self.candidate.api(function, api_campaign, api_staged, hash_seed="97"), f"{function} API")
        self.assertEqual(product_bytes(full), product_bytes(api_staged), "full/API-staged bytes differ")

        exact = self.candidate.python(
            "from clockrecover.exact import round_half_away as r; "
            "assert [r(n,d) for n,d in [(1,2),(-1,2),(3,2),(-3,2),(4,3),(-4,3),(0,7)]] "
            "== [1,-1,2,-2,1,-1,0]; "
            "\ntry: r(1,0)\nexcept ValueError: pass\nelse: raise AssertionError('zero denominator accepted')"
        )
        require_success(exact, "exact arithmetic public API")

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
        first = normalized["picks"][0]
        shard = next((conflict / "picks").glob("*.csv"))
        append_pick(
            shard,
            {
                "pick_id": first["pick_id"],
                "station_id": first["station_id"],
                "recorded_us": first["recorded_us"] + 1,
            },
        )
        require_failure(self.candidate.cli("run", conflict, baseline), "conflicting pick identifier")
        self.assertEqual(before, product_bytes(baseline), "failed run changed prior-good output")

        missing_travel = self.campaign(self.visible_source, "bad-travel")
        travel_path = missing_travel / "travel_times.csv"
        lines = travel_path.read_text().splitlines()
        travel_path.write_text("\n".join(lines[:-1]) + "\n")
        travel_path.chmod(0o644)
        require_failure(self.candidate.cli("run", missing_travel, self.output("bad-travel-output")), "missing travel coverage")

        malformed = self.campaign(self.visible_source, "bad-malformed")
        shard = next((malformed / "picks").glob("*.csv"))
        lines = shard.read_text().splitlines()
        lines[0] = "pick_id,station_id,recorded_us,unexpected"
        shard.write_text("\n".join(lines) + "\n")
        shard.chmod(0o644)
        require_failure(self.candidate.cli("ingest", malformed, self.output("bad-malformed-output")), "malformed CSV")

        nonunique = self.campaign(self.visible_source, "bad-nonunique")
        for shard in (nonunique / "picks").glob("*.csv"):
            shard.write_text("pick_id,station_id,recorded_us\n")
            shard.chmod(0o644)
        nonunique_output = self.output("bad-nonunique-output")
        require_success(self.candidate.cli("ingest", nonunique, nonunique_output), "empty ingestion")
        require_failure(self.candidate.cli("diagnose", nonunique, nonunique_output), "nonunique diagnosis")


if __name__ == "__main__":
    unittest.main(verbosity=2)
