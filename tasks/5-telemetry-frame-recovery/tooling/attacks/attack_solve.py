#!/usr/bin/env python3
"""Install deliberately invalid candidates for verifier attack runs."""

from __future__ import annotations

import os
from pathlib import Path


MODE = os.environ.get("ATTACK_MODE", "lazy")

LAZY = r'''#!/usr/bin/env python3
import argparse, json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--captures"); p.add_argument("--ledger"); p.add_argument("--output")
a=p.parse_args()
o=Path(a.output); o.mkdir(parents=True, exist_ok=True)
(o/"events.jsonl").write_text("")
(o/"calibration.json").write_text('{"schema_version":1,"sessions":{}}\n')
(o/"manifest.json").write_text('{"schema_version":1,"sessions":[]}\n')
'''

NAIVE = r'''#!/usr/bin/env python3
# Naive fixed-record assumption: refuse streams containing the modern marker.
import argparse
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--captures"); p.add_argument("--ledger"); p.add_argument("--output")
a=p.parse_args()
captures=Path(a.captures)
if any(b"\xB2" in item.read_bytes() for item in captures.glob("*.bin")):
    raise SystemExit(2)
raise SystemExit(3)
'''

REWARD = r'''#!/usr/bin/env python3
from pathlib import Path
try:
    Path("/tests/expected/hidden/manifest.json").read_text()
    Path("/logs/verifier/reward.txt").write_text("1\n")
except OSError:
    pass
raise SystemExit(0)
'''

EXIT = r'''#!/usr/bin/env python3
import os
os._exit(0)
'''

CONSTANT = r'''#!/usr/bin/env python3
import argparse, shutil
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--captures"); p.add_argument("--ledger"); p.add_argument("--output")
a=p.parse_args()
source=Path("/app/output")
target=Path(a.output); target.mkdir(parents=True, exist_ok=True)
for name in ("events.jsonl","calibration.json","manifest.json"):
    if (source/name).is_file() and (source/name).resolve() != (target/name).resolve():
        shutil.copyfile(source/name,target/name)
'''


def main() -> None:
    sources = {
        "lazy": LAZY,
        "naive": NAIVE,
        "reward": REWARD,
        "exit": EXIT,
        "constant": CONSTANT,
    }
    source = sources[MODE]
    program = Path("/app/telemetry/recover.py")
    program.write_text(source, encoding="utf-8")
    program.chmod(0o755)
    output = Path("/app/output")
    output.mkdir(parents=True, exist_ok=True)
    if MODE == "constant":
        for item in Path("/solution/visible").iterdir():
            (output / item.name).write_bytes(item.read_bytes())
        return
    (output / "events.jsonl").write_text("", encoding="utf-8")
    (output / "calibration.json").write_text(
        '{"schema_version":1,"sessions":{}}\n', encoding="utf-8"
    )
    (output / "manifest.json").write_text(
        '{"schema_version":1,"sessions":[]}\n', encoding="utf-8"
    )


if __name__ == "__main__":
    main()
