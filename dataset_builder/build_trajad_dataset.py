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
from datetime import UTC, datetime
from pathlib import Path

try:
    from dataset_builder.coherence import is_plausible_trajectory
    from dataset_builder.perturbations import ALL_RULES, MVP_RULES, apply_perturbation
except ModuleNotFoundError:
    from coherence import is_plausible_trajectory
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


def unique_source_ids_in_order(records: list[dict]) -> list[str]:
    seen: set[str] = set()
    ordered_ids: list[str] = []
    for record in records:
        source_id = record["source_trace_id"]
        if source_id not in seen:
            seen.add(source_id)
            ordered_ids.append(source_id)
    return ordered_ids


def build_all_records_with_split(split_records: dict[str, list[dict]]) -> list[dict]:
    ordered: list[dict] = []
    for split_name in ("train", "dev", "test"):
        ordered.extend(split_records.get(split_name, []))
    return ordered


def _sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def build_manifest(
    *,
    seed: int,
    rule_names: list[str],
    source_input_paths: list[str],
    split_records: dict[str, list[dict]],
    perturbation_failures: Counter[str],
    coherence_rejections: Counter[str],
    coherence_rejection_reasons: Counter[str],
) -> dict:
    all_records = [record for records in split_records.values() for record in records]
    anomaly_type_counts = Counter(
        record["anomaly_type"] for record in all_records if record.get("anomaly_type") is not None
    )
    anomaly_class_counts = Counter(
        record["anomaly_class"] for record in all_records if record.get("anomaly_class") is not None
    )
    normal_total = sum(1 for record in all_records if not record.get("is_anomalous", record.get("anomaly_type") is not None))
    anomalous_total = sum(1 for record in all_records if record.get("is_anomalous", record.get("anomaly_type") is not None))

    return {
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "seed": seed,
        "rules_used": list(rule_names),
        "source_input_paths": list(source_input_paths),
        "totals": {
            "normal": normal_total,
            "anomalous": anomalous_total,
            "all_records": len(all_records),
        },
        "split_counts": {split: len(records) for split, records in split_records.items()},
        "anomaly_type_counts": _sorted_counter(anomaly_type_counts),
        "anomaly_class_counts": _sorted_counter(anomaly_class_counts),
        "perturbation_failures_by_rule": _sorted_counter(perturbation_failures),
        "coherence_rejections_by_rule": _sorted_counter(coherence_rejections),
        "coherence_rejection_reasons": _sorted_counter(coherence_rejection_reasons),
    }


def write_manifest(manifest: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"  Wrote build manifest → {path}")


def format_manifest_summary(manifest: dict) -> str:
    split_counts = manifest["split_counts"]
    totals = manifest["totals"]
    lines = [
        "Build manifest summary:",
        f"  seed: {manifest['seed']}",
        f"  rules used: {len(manifest['rules_used'])}",
        (
            "  split counts: "
            f"train={split_counts.get('train', 0):,} "
            f"dev={split_counts.get('dev', 0):,} "
            f"test={split_counts.get('test', 0):,}"
        ),
        (
            "  totals: "
            f"normal={totals['normal']:,} "
            f"anomalous={totals['anomalous']:,} "
            f"all={totals['all_records']:,}"
        ),
    ]

    if manifest["anomaly_type_counts"]:
        lines.append("  anomaly types:")
        for name, count in manifest["anomaly_type_counts"].items():
            lines.append(f"    {name}: {count:,}")

    if manifest["anomaly_class_counts"]:
        lines.append("  anomaly classes:")
        for name, count in manifest["anomaly_class_counts"].items():
            lines.append(f"    {name}: {count:,}")

    if manifest["perturbation_failures_by_rule"]:
        lines.append("  perturbation failures by rule:")
        for name, count in manifest["perturbation_failures_by_rule"].items():
            lines.append(f"    {name}: {count:,}")

    if manifest["coherence_rejections_by_rule"]:
        lines.append("  coherence rejections by rule:")
        for name, count in manifest["coherence_rejections_by_rule"].items():
            lines.append(f"    {name}: {count:,}")

    if manifest["coherence_rejection_reasons"]:
        lines.append("  coherence rejection reasons:")
        for name, count in manifest["coherence_rejection_reasons"].items():
            lines.append(f"    {name}: {count:,}")

    return "\n".join(lines)


def build(rules: list, seed: int) -> dict | None:
    rng = random.Random(seed)
    rejection_reasons: Counter[str] = Counter()
    perturbation_failures: Counter[str] = Counter()
    coherence_rejections_by_rule: Counter[str] = Counter()

    # Load normalized normal records
    normal_files = list(INTERIM_DIR.glob("*.jsonl"))
    if not normal_files:
        print(f"ERROR: No JSONL files found in {INTERIM_DIR}")
        print("Run normalize_trajectory.py first.")
        return None

    source_input_paths = [str(path.relative_to(Path(__file__).parent.parent)) for path in sorted(normal_files)]

    normals: list[dict] = []
    for f in normal_files:
        normals.extend(ensure_label_fields(record) for record in load_jsonl(f))
    print(f"Loaded {len(normals):,} normal records from {INTERIM_DIR}")

    # Generate anomalous variants
    anomalous: list[dict] = []
    for record in normals:
        for v_idx, rule_fn in enumerate(rules):
            rule_name = rule_fn.__name__
            result = apply_perturbation(record, rule_fn, v_idx + 1, rng)
            if result is None:
                perturbation_failures[rule_name] += 1
                continue

            plausible, reason = is_plausible_trajectory(result)
            if plausible:
                anomalous.append(result)
            else:
                rejection_reasons[reason or "unknown"] += 1
                coherence_rejections_by_rule[rule_name] += 1

    rejected_total = sum(rejection_reasons.values())
    print(f"Generated {len(anomalous):,} anomalous records")
    print(f"Coherence screen: kept={len(anomalous):,} rejected={rejected_total:,}")
    if rejection_reasons:
        print("Rejected by reason:")
        for reason, count in rejection_reasons.most_common():
            print(f"  {reason:30s}: {count:,}")

    # Combine and shuffle
    all_records = normals + anomalous
    rng.shuffle(all_records)

    # Assign split by source_trace_id to avoid leakage
    unique_ids = unique_source_ids_in_order(all_records)
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
    split_records = {"train": train, "dev": dev, "test": test}
    write_jsonl(build_all_records_with_split(split_records), PROCESSED_DIR / "all.jsonl")

    manifest = build_manifest(
        seed=seed,
        rule_names=[rule.__name__ for rule in rules],
        source_input_paths=source_input_paths,
        split_records=split_records,
        perturbation_failures=perturbation_failures,
        coherence_rejections=coherence_rejections_by_rule,
        coherence_rejection_reasons=rejection_reasons,
    )
    write_manifest(manifest, PROCESSED_DIR / "build_manifest.json")
    print()
    print(format_manifest_summary(manifest))
    return manifest


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
