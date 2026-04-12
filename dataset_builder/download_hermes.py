"""Download and cache Hermes agent trace datasets from Hugging Face."""

import argparse
import json
from pathlib import Path

from datasets import load_dataset
from tqdm import tqdm

# Primary filtered dataset — ~3,679 rows, ShareGPT-compatible JSONL
# https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered
PRIMARY_DATASET = "DJLougen/hermes-agent-traces-filtered"

# Optional noisier original source
# https://huggingface.co/datasets/lambda/hermes-agent-reasoning-traces
ORIGINAL_DATASET = "lambda/hermes-agent-reasoning-traces"

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"


def download(dataset_id: str, output_path: Path, split: str = "train") -> int:
    """Download a HuggingFace dataset to JSONL.

    Returns the number of rows written.
    """
    print(f"Downloading {dataset_id} ...")
    ds = load_dataset(dataset_id, split=split)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        for row in tqdm(ds, desc="Writing rows"):
            f.write(json.dumps(row) + "\n")
    print(f"Saved {len(ds):,} rows → {output_path}")
    return len(ds)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        choices=["filtered", "original", "both"],
        default="filtered",
        help="Which dataset to download (default: filtered)",
    )
    args = parser.parse_args()

    if args.dataset in ("filtered", "both"):
        download(PRIMARY_DATASET, RAW_DIR / "hermes_filtered.jsonl")

    if args.dataset in ("original", "both"):
        download(ORIGINAL_DATASET, RAW_DIR / "hermes_original.jsonl")


if __name__ == "__main__":
    main()
