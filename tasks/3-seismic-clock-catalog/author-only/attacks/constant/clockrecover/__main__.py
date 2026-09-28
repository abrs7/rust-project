from pathlib import Path

PRODUCTS = (
    "normalized-input.json",
    "network-diagnosis.json",
    "stable-catalogue.jsonl",
    "residual-alternatives.jsonl",
    "clock-model.json",
    "corrected-assignments.jsonl",
    "rejections.jsonl",
    "final-catalogue.jsonl",
    "provenance.json",
)


def main():
    output = Path(__import__("sys").argv[3])
    output.mkdir(parents=True, exist_ok=True)
    for name in PRODUCTS:
        (output / name).write_text("{}\n" if name.endswith(".json") else "")
    return 0
