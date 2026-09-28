from pathlib import Path
import hashlib
import json

MARKER = ".telemetry-fragments-path"


def ingest(fragments, campaigns, output):
    target = Path(output)
    target.mkdir(parents=True, exist_ok=True)
    source = Path(fragments).resolve()
    (target / MARKER).write_text(str(source), encoding="utf-8")
    digest = hashlib.sha256()
    for path in sorted(source.glob("*.frag")):
        digest.update(path.read_bytes())
    (target / "fragment-index.jsonl").write_text(
        json.dumps({"reread": digest.hexdigest()}, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def assemble(campaigns, output):
    target = Path(output)
    saved = Path((target / MARKER).read_text(encoding="utf-8").strip())
    digest = hashlib.sha256()
    for path in sorted(saved.glob("*.frag")):
        digest.update(path.read_bytes())
    payload = {
        "campaigns": [],
        "reread_sha256": digest.hexdigest(),
        "schema_version": 1,
    }
    (target / "assembly.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def decode(campaigns, output):
    assemble(campaigns, output)


def fit_clock(campaigns, output):
    assemble(campaigns, output)


def calibrate(references, output):
    assemble("-", output)


def reconcile(references, output):
    assemble("-", output)


def export(campaigns, references, output):
    assemble(campaigns, output)


def run(fragments, campaigns, references, output):
    ingest(fragments, campaigns, output)
    assemble(campaigns, output)
