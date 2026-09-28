"""Canonical numbered task folders under tasks/."""

from __future__ import annotations

# Harbor slug -> workspace folder number (stable; do not renumber after upload).
TASK_NUMBERS: dict[str, int] = {
    "ctd-cast-processing": 1,
    "gamma-spectrum-calibration": 2,
    "seismic-clock-catalog": 3,
    "telemetry-array-rebuild": 4,
    "telemetry-frame-recovery": 5,
    "django-cors-broken": 6,
    "kafka-ingest-reconcile": 7,
    "units-library-reconcile": 8,
    "ledger-settlement-reconcile": 9,
    "measurement-wal-recover": 10,
}

NUMBER_TO_SLUG: dict[int, str] = {v: k for k, v in TASK_NUMBERS.items()}
