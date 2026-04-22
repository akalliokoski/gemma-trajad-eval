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


def get_trajectory(record: dict) -> list[dict]:
    for candidate in ("conversations", "trajectory", "messages"):
        if candidate in record:
            return record[candidate]
    return []


def has_trajectory_field(record: dict) -> bool:
    return any(candidate in record for candidate in ("conversations", "trajectory", "messages"))


def get_role(msg: dict) -> str:
    return msg.get("role", msg.get("from", "?"))


def get_content(msg: dict) -> str:
    return msg.get("content", msg.get("value", "")) or ""


def count_roles(trajectory: list[dict]) -> Counter:
    return Counter(get_role(msg) for msg in trajectory)


def has_tool_call(content: str) -> bool:
    return "<tool_call>" in content


def has_think(content: str) -> bool:
    return "<think>" in content


def count_assistant_tool_pairs(trajectory: list[dict]) -> int:
    assistant_roles = {"assistant", "gpt"}
    pair_count = 0
    for first, second in zip(trajectory, trajectory[1:]):
        if get_role(first) in assistant_roles and has_tool_call(get_content(first)) and get_role(second) == "tool":
            pair_count += 1
    return pair_count


def print_summary(records: list[dict]) -> None:
    n = len(records)
    print(f"\nTotal records: {n:,}")

    if not records:
        return

    if not has_trajectory_field(records[0]):
        print("WARNING: could not detect trajectory field. Keys:", list(records[0].keys()))
        return

    lengths = [len(get_trajectory(r)) for r in records]
    print(f"Trajectory length — min: {min(lengths)}, max: {max(lengths)}, avg: {sum(lengths)/n:.1f}")

    # Role distribution
    role_counter: Counter = Counter()
    tool_call_count = 0
    think_count = 0
    traces_with_tool_call = 0
    traces_with_two_pairs = 0
    for r in records:
        traj = get_trajectory(r)
        role_counter.update(count_roles(traj))
        trace_has_tool_call = False
        for msg in traj:
            content = get_content(msg)
            if has_tool_call(content):
                tool_call_count += 1
                trace_has_tool_call = True
            if has_think(content):
                think_count += 1
        if trace_has_tool_call:
            traces_with_tool_call += 1
        if count_assistant_tool_pairs(traj) >= 2:
            traces_with_two_pairs += 1

    print("\nRole distribution across all messages:")
    for role, count in role_counter.most_common():
        print(f"  {role:15s}: {count:,}")

    print(f"\nMessages with <tool_call>: {tool_call_count:,}")
    print(f"Messages with <think>:     {think_count:,}")
    print(f"Traces with >=1 tool call: {traces_with_tool_call / n:.1%}")
    print(f"Traces with >=2 assistant/tool-call pairs: {traces_with_two_pairs / n:.1%}")

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
    for i, record in enumerate(records[:n]):
        print(f"\n{'='*60}")
        print(f"Record {i}  id={record.get('id', record.get('source_id', '?'))}")
        print(f"{'='*60}")
        traj = get_trajectory(record)
        for j, msg in enumerate(traj):
            role = get_role(msg)
            content = get_content(msg)[:300]
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
