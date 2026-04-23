"""End-to-end pipeline: Hermes traces → TrajAD-style supervised dataset.

Steps:
    1. Load normalized normal trajectories from data/interim/
    2. Apply perturbation rules to generate anomalous variants
    3. Combine normal + anomalous examples
    4. Split into train / dev / test
    5. Write JSONL files to data/processed/

Usage:
    python dataset_builder/build_trajad_dataset.py
    python dataset_builder/build_trajad_dataset.py --mvp      # P1-P4 only
    python dataset_builder/build_trajad_dataset.py --seed 99
"""

import argparse
import json
import random
from collections import Counter
from pathlib import Path

from perturbations import ALL_RULES, MVP_RULES, apply_perturbation

INTERIM_DIR = Path(__file__).parent.parent / "data" / "interim"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"

TRAIN_FRAC = 0.75
DEV_FRAC = 0.10
TEST_FRAC = 0.15  # remainder


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"  Wrote {len(records):,} records → {path}")


def ensure_label_fields(record: dict) -> dict:
    out = dict(record)
    out.setdefault("bad_step", None)
    out.setdefault("anomaly_type", None)
    out.setdefault("anomaly_class", None)
    return out


def build(rules: list, seed: int) -> None:
    rng = random.Random(seed)

    # Load normalized normal records
    normal_files = list(INTERIM_DIR.glob("*.jsonl"))
    if not normal_files:
        print(f"ERROR: No JSONL files found in {INTERIM_DIR}")
        print("Run normalize_trajectory.py first.")
        return

    normals: list[dict] = []
    for f in normal_files:
        normals.extend(ensure_label_fields(record) for record in load_jsonl(f))
    print(f"Loaded {len(normals):,} normal records from {INTERIM_DIR}")

    # Generate anomalous variants
    anomalous: list[dict] = []
    for record in normals:
        for v_idx, rule_fn in enumerate(rules):
            result = apply_perturbation(record, rule_fn, v_idx + 1, rng)
            if result is not None:
                anomalous.append(result)

    print(f"Generated {len(anomalous):,} anomalous records")

    # Combine and shuffle
    all_records = normals + anomalous
    rng.shuffle(all_records)

    # Assign split by source_trace_id to avoid leakage
    unique_ids = list({r["source_trace_id"] for r in all_records})
    rng.shuffle(unique_ids)
    n = len(unique_ids)
    train_ids = set(unique_ids[: int(n * TRAIN_FRAC)])
    dev_ids = set(unique_ids[int(n * TRAIN_FRAC) : int(n * (TRAIN_FRAC + DEV_FRAC))])

    train, dev, test = [], [], []
    for r in all_records:
        sid = r["source_trace_id"]
        r_out = dict(r)
        if sid in train_ids:
            r_out["split"] = "train"
            train.append(r_out)
        elif sid in dev_ids:
            r_out["split"] = "dev"
            dev.append(r_out)
        else:
            r_out["split"] = "test"
            test.append(r_out)

    print(f"\nSplit sizes: train={len(train):,}  dev={len(dev):,}  test={len(test):,}")

    # Print class balance
    for split_name, split_data in [("train", train), ("test", test)]:
        types = Counter(r["anomaly_type"] or "normal" for r in split_data)
        print(f"\n{split_name} class distribution:")
        for k, v in types.most_common():
            print(f"  {k:45s}: {v:,}")

    # Write outputs
    write_jsonl(train, PROCESSED_DIR / "train.jsonl")
    write_jsonl(dev, PROCESSED_DIR / "dev.jsonl")
    write_jsonl(test, PROCESSED_DIR / "test.jsonl")

    # Write combined for easy inspection
    write_jsonl(all_records, PROCESSED_DIR / "all.jsonl")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mvp", action="store_true", help="Use MVP rules only (P1-P4)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    rules = MVP_RULES if args.mvp else ALL_RULES
    rule_names = [f.__name__ for f in rules]
    print(f"Using {len(rules)} rules: {rule_names}")
    build(rules, args.seed)


if __name__ == "__main__":
    main()
