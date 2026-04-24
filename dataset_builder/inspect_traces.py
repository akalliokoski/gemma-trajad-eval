"""EDA utilities for Hermes agent traces.

Usage:
    python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl
    python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --sample 5
    python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --schema-report
    python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --tool-stats
    python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --eligibility-report
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


def get_trajectory_field_name(record: dict) -> str | None:
    for candidate in ("conversations", "trajectory", "messages"):
        if candidate in record:
            return candidate
    return None


def has_trajectory_field(record: dict) -> bool:
    return get_trajectory_field_name(record) is not None


def get_role(msg: dict) -> str:
    return msg.get("role", msg.get("from", "?"))


def get_content(msg: dict) -> str:
    return msg.get("content", msg.get("value", "")) or ""


def get_message_shape(msg: dict) -> str:
    if "role" in msg or "content" in msg:
        return "role/content"
    if "from" in msg or "value" in msg:
        return "from/value"
    return "other"


def count_roles(trajectory: list[dict]) -> Counter:
    return Counter(get_role(msg) for msg in trajectory)


def has_tool_call(content: str) -> bool:
    return "<tool_call>" in content


def has_tool_response(content: str) -> bool:
    return "<tool_response>" in content


def has_think(content: str) -> bool:
    return "<think>" in content


def count_tool_calls_in_trajectory(trajectory: list[dict]) -> int:
    return sum(1 for msg in trajectory if has_tool_call(get_content(msg)))


def count_tool_responses_in_trajectory(trajectory: list[dict]) -> int:
    return sum(1 for msg in trajectory if has_tool_response(get_content(msg)))


def count_assistant_tool_pairs(trajectory: list[dict]) -> int:
    assistant_roles = {"assistant", "gpt"}
    pair_count = 0
    for first, second in zip(trajectory, trajectory[1:]):
        if get_role(first) in assistant_roles and has_tool_call(get_content(first)) and get_role(second) == "tool":
            pair_count += 1
    return pair_count


def has_tool_arguments(trajectory: list[dict]) -> bool:
    for msg in trajectory:
        content = get_content(msg)
        if not has_tool_call(content):
            continue
        try:
            tool_json = content.split("<tool_call>", 1)[1].split("</tool_call>", 1)[0]
            parsed = json.loads(tool_json)
        except (IndexError, json.JSONDecodeError):
            continue
        args = parsed.get("arguments", parsed.get("parameters", {}))
        if isinstance(args, dict) and args:
            return True
    return False


def has_nearby_tool_candidate(trajectory: list[dict]) -> bool:
    for msg in trajectory:
        content = get_content(msg)
        if not has_tool_call(content):
            continue
        try:
            tool_json = content.split("<tool_call>", 1)[1].split("</tool_call>", 1)[0]
            parsed = json.loads(tool_json)
        except (IndexError, json.JSONDecodeError):
            continue
        if parsed.get("name"):
            return True
    return False


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

    role_counter: Counter = Counter()
    tool_call_count = 0
    think_count = 0
    traces_with_tool_call = 0
    traces_with_two_pairs = 0
    for r in records:
        traj = get_trajectory(r)
        role_counter.update(count_roles(traj))
        trace_tool_calls = count_tool_calls_in_trajectory(traj)
        tool_call_count += trace_tool_calls
        if trace_tool_calls > 0:
            traces_with_tool_call += 1
        if count_assistant_tool_pairs(traj) >= 2:
            traces_with_two_pairs += 1
        think_count += sum(1 for msg in traj if has_think(get_content(msg)))

    print("\nRole distribution across all messages:")
    for role, count in role_counter.most_common():
        print(f"  {role:15s}: {count:,}")

    print(f"\nMessages with <tool_call>: {tool_call_count:,}")
    print(f"Messages with <think>:     {think_count:,}")
    print(f"Traces with >=1 tool call: {traces_with_tool_call / n:.1%}")
    print(f"Traces with >=2 assistant/tool-call pairs: {traces_with_two_pairs / n:.1%}")

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


def print_schema_report(records: list[dict]) -> None:
    n = len(records)
    print("Schema report:")
    if not records:
        print("  No records loaded.")
        return

    trajectory_fields = Counter()
    message_shapes = Counter()
    records_with_tools_field = 0
    records_with_embedded_tool_call = 0

    for record in records:
        field_name = get_trajectory_field_name(record) or "missing"
        trajectory_fields[field_name] += 1
        trajectory = get_trajectory(record)
        if trajectory:
            message_shapes[get_message_shape(trajectory[0])] += 1
        if "tools" in record:
            records_with_tools_field += 1
        if any(has_tool_call(get_content(msg)) for msg in trajectory):
            records_with_embedded_tool_call += 1

    print("  Trajectory fields:")
    for name, count in trajectory_fields.items():
        print(f"    {name}: {count}")

    print("  Message shapes:")
    for name, count in message_shapes.items():
        print(f"    {name}: {count}")

    print(f"  Records with tools field: {records_with_tools_field / n:.1%}")
    print(f"  Records with embedded <tool_call>: {records_with_embedded_tool_call / n:.1%}")


def print_tool_stats(records: list[dict]) -> None:
    n = len(records)
    print("Tool stats:")
    if not records:
        print("  No records loaded.")
        return

    total_tool_calls = 0
    total_tool_responses = 0
    traces_with_tool_call = 0
    traces_with_two_pairs = 0

    for record in records:
        trajectory = get_trajectory(record)
        tool_calls = count_tool_calls_in_trajectory(trajectory)
        tool_responses = count_tool_responses_in_trajectory(trajectory)
        total_tool_calls += tool_calls
        total_tool_responses += tool_responses
        if tool_calls > 0:
            traces_with_tool_call += 1
        if count_assistant_tool_pairs(trajectory) >= 2:
            traces_with_two_pairs += 1

    print(f"  Average <tool_call> blocks per trace: {total_tool_calls / n:.1f}")
    print(f"  Average <tool_response> blocks per trace: {total_tool_responses / n:.1f}")
    print(f"  Traces with >=1 tool call: {traces_with_tool_call / n:.1%}")
    print(f"  Traces with >=2 assistant/tool-call pairs: {traces_with_two_pairs / n:.1%}")


def print_eligibility_report(records: list[dict]) -> None:
    n = len(records)
    print("Eligibility report:")
    if not records:
        print("  No records loaded.")
        return

    p1 = 0
    p2 = 0
    p345 = 0
    p8 = 0

    for record in records:
        trajectory = get_trajectory(record)
        pair_count = count_assistant_tool_pairs(trajectory)
        if has_nearby_tool_candidate(trajectory):
            p1 += 1
        if has_tool_arguments(trajectory):
            p2 += 1
        if pair_count >= 1:
            p345 += 1
        if pair_count >= 2:
            p8 += 1

    print(f"  P1 wrong_tool_choice: {p1}/{n} ({p1 / n:.1%})")
    print(f"  P2 bad_tool_arguments: {p2}/{n} ({p2 / n:.1%})")
    print(f"  P3/P4/P5 tool-interaction rules: {p345}/{n} ({p345 / n:.1%})")
    print(f"  P8 multi-tool-step rules: {p8}/{n} ({p8 / n:.1%})")


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
    parser.add_argument("--schema-report", action="store_true", help="Print schema and message-shape summary")
    parser.add_argument("--tool-stats", action="store_true", help="Print tool-call and tool-response statistics")
    parser.add_argument("--eligibility-report", action="store_true", help="Estimate rule eligibility from trajectory structure")
    args = parser.parse_args()

    records = load_jsonl(args.path)
    print_summary(records)
    if args.schema_report:
        print()
        print_schema_report(records)
    if args.tool_stats:
        print()
        print_tool_stats(records)
    if args.eligibility_report:
        print()
        print_eligibility_report(records)
    if args.sample > 0:
        print_sample(records, args.sample)


if __name__ == "__main__":
    main()
