"""Lightweight post-build audit for processed dataset JSONL files."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def bucket_bad_step_position(*, bad_step: int, trajectory_length: int) -> str:
    if trajectory_length <= 0:
        return "unknown"
    ratio = bad_step / trajectory_length
    if ratio < 1 / 3:
        return "early"
    if ratio < 2 / 3:
        return "middle"
    return "late"


def _average_by_split(values_by_split: dict[str, list[float]]) -> dict[str, float]:
    return {
        split: round(sum(values) / len(values), 1)
        for split, values in sorted(values_by_split.items())
        if values
    }


def _empty_accumulator() -> dict:
    return {
        "total_records": 0,
        "split_counts": Counter(),
        "anomaly_type_counts": Counter(),
        "anomaly_class_counts": Counter(),
        "bad_step_position_buckets": Counter(),
        "trajectory_lengths_by_split": defaultdict(list),
        "tool_calls_by_split": defaultdict(list),
    }


def _accumulate_record(acc: dict, record: dict) -> None:
    acc["total_records"] += 1
    split = record.get("split") or "unspecified"
    acc["split_counts"][split] += 1

    trajectory = record.get("trajectory") or []
    acc["trajectory_lengths_by_split"][split].append(float(len(trajectory)))

    metadata = record.get("metadata") or {}
    acc["tool_calls_by_split"][split].append(float(metadata.get("tool_call_count", 0)))

    anomaly_type = record.get("anomaly_type")
    anomaly_class = record.get("anomaly_class")
    if anomaly_type is not None:
        acc["anomaly_type_counts"][anomaly_type] += 1
    if anomaly_class is not None:
        acc["anomaly_class_counts"][anomaly_class] += 1

    bad_step = record.get("bad_step")
    if isinstance(bad_step, int) and trajectory:
        bucket = bucket_bad_step_position(bad_step=bad_step, trajectory_length=len(trajectory))
        acc["bad_step_position_buckets"][bucket] += 1


def _finalize_summary(acc: dict) -> dict:
    return {
        "total_records": acc["total_records"],
        "split_counts": dict(sorted(acc["split_counts"].items())),
        "anomaly_type_counts": dict(sorted(acc["anomaly_type_counts"].items())),
        "anomaly_class_counts": dict(sorted(acc["anomaly_class_counts"].items())),
        "average_trajectory_length_by_split": _average_by_split(acc["trajectory_lengths_by_split"]),
        "average_tool_call_count_by_split": _average_by_split(acc["tool_calls_by_split"]),
        "bad_step_position_buckets": dict(sorted(acc["bad_step_position_buckets"].items())),
    }


def summarize_records(records: list[dict]) -> dict:
    acc = _empty_accumulator()
    for record in records:
        _accumulate_record(acc, record)
    return _finalize_summary(acc)


def summarize_file(path: Path) -> dict:
    acc = _empty_accumulator()
    with path.open() as f:
        for line in f:
            if not line.strip():
                continue
            _accumulate_record(acc, json.loads(line))
    return _finalize_summary(acc)


def format_summary(summary: dict, *, markdown: bool = False) -> str:
    if markdown:
        lines = ["# Dataset audit report", ""]
        lines.append(f"- Total records: {summary['total_records']}")
        lines.append(f"- Split counts: {summary['split_counts']}")
        lines.append(f"- Anomaly types: {summary['anomaly_type_counts']}")
        lines.append(f"- Anomaly classes: {summary['anomaly_class_counts']}")
        lines.append(f"- Avg trajectory length by split: {summary['average_trajectory_length_by_split']}")
        lines.append(f"- Avg tool-call count by split: {summary['average_tool_call_count_by_split']}")
        lines.append(f"- Bad-step buckets: {summary['bad_step_position_buckets']}")
        return "\n".join(lines)

    lines = [
        "Dataset audit report:",
        f"  Total records: {summary['total_records']}",
        f"  Split counts: {summary['split_counts']}",
        f"  Anomaly types: {summary['anomaly_type_counts']}",
        f"  Anomaly classes: {summary['anomaly_class_counts']}",
        f"  Avg trajectory length by split: {summary['average_trajectory_length_by_split']}",
        f"  Avg tool-call count by split: {summary['average_tool_call_count_by_split']}",
        f"  Bad-step buckets: {summary['bad_step_position_buckets']}",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Processed JSONL file to audit")
    parser.add_argument("--markdown", action="store_true", help="Emit markdown instead of plain text")
    args = parser.parse_args()

    summary = summarize_file(args.path)
    print(format_summary(summary, markdown=args.markdown))


if __name__ == "__main__":
    main()
