"""EDA utilities for Hermes agent traces.

Usage:
    python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl
    python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --sample 5
"""

import argparse
import json
from collections import Counter
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def count_roles(trajectory: list[dict]) -> Counter:
    return Counter(msg["role"] for msg in trajectory)


def has_tool_call(content: str) -> bool:
    return "<tool_call>" in content


def has_think(content: str) -> bool:
    return "<think>" in content


def print_summary(records: list[dict]) -> None:
    n = len(records)
    print(f"\nTotal records: {n:,}")

    # Determine trajectory field name
    traj_field = None
    for candidate in ("conversations", "trajectory", "messages"):
        if candidate in records[0]:
            traj_field = candidate
            break

    if traj_field is None:
        print("WARNING: could not detect trajectory field. Keys:", list(records[0].keys()))
        return

    lengths = [len(r[traj_field]) for r in records]
    print(f"Trajectory length — min: {min(lengths)}, max: {max(lengths)}, avg: {sum(lengths)/n:.1f}")

    # Role distribution
    role_counter: Counter = Counter()
    tool_call_count = 0
    think_count = 0
    for r in records:
        traj = r[traj_field]
        role_counter.update(count_roles(traj))
        for msg in traj:
            content = msg.get("content", "") or ""
            if has_tool_call(content):
                tool_call_count += 1
            if has_think(content):
                think_count += 1

    print("\nRole distribution across all messages:")
    for role, count in role_counter.most_common():
        print(f"  {role:15s}: {count:,}")

    print(f"\nMessages with <tool_call>: {tool_call_count:,}")
    print(f"Messages with <think>:     {think_count:,}")

    # Category distribution (if present)
    if "category" in records[0].get("metadata", {}):
        cats: Counter = Counter(r["metadata"]["category"] for r in records)
        print("\nTop categories:")
        for cat, cnt in cats.most_common(10):
            print(f"  {cat:40s}: {cnt:,}")
    elif "category" in records[0]:
        cats = Counter(r["category"] for r in records)
        print("\nTop categories:")
        for cat, cnt in cats.most_common(10):
            print(f"  {cat:40s}: {cnt:,}")


def print_sample(records: list[dict], n: int = 3) -> None:
    traj_field = None
    for candidate in ("conversations", "trajectory", "messages"):
        if candidate in records[0]:
            traj_field = candidate
            break

    for i, record in enumerate(records[:n]):
        print(f"\n{'='*60}")
        print(f"Record {i}  id={record.get('id', record.get('source_id', '?'))}")
        print(f"{'='*60}")
        traj = record.get(traj_field, []) if traj_field else []
        for j, msg in enumerate(traj):
            role = msg.get("role", "?")
            content = (msg.get("content", "") or "")[:300]
            print(f"  [{j}] {role}: {content!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to JSONL file")
    parser.add_argument("--sample", type=int, default=0, help="Print N sample records")
    args = parser.parse_args()

    records = load_jsonl(args.path)
    print_summary(records)
    if args.sample > 0:
        print_sample(records, args.sample)


if __name__ == "__main__":
    main()
