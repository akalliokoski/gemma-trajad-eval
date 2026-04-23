"""Convert ShareGPT-style Hermes traces to the internal trajectory format.

Hermes traces use ShareGPT message format with roles: system, human, gpt, tool.
This module normalizes them to: system, user, assistant, tool.

Internal format (one record):
{
    "id": str,
    "source_trace_id": str,
    "trajectory": [{"role": str, "content": str}, ...],
    "metadata": dict
}
"""

import hashlib
import json
from pathlib import Path
from typing import Any

ROLE_MAP = {
    "system": "system",
    "human": "user",
    "gpt": "assistant",
    "tool": "tool",
    # already-normalized roles pass through
    "user": "user",
    "assistant": "assistant",
}


def normalize_role(role: str) -> str:
    normalized = ROLE_MAP.get(role.lower())
    if normalized is None:
        raise ValueError(f"Unknown role: {role!r}")
    return normalized


def extract_metadata(record: dict) -> dict:
    """Pull any metadata fields that are present in the source record."""
    meta: dict[str, Any] = {}
    for key in ("category", "subcategory", "source", "task_type", "difficulty"):
        if key in record:
            meta[key] = record[key]
    if "metadata" in record and isinstance(record["metadata"], dict):
        meta.update(record["metadata"])
    return meta


def derive_trace_metadata(trajectory: list[dict[str, str]]) -> dict[str, Any]:
    """Compute cheap structural metadata from a normalized trajectory."""
    tool_call_count = 0
    tool_response_count = 0
    has_think = False

    for message in trajectory:
        content = message.get("content", "") or ""
        tool_call_count += content.count("<tool_call>")
        tool_response_count += content.count("<tool_response>")
        has_think = has_think or "<think>" in content

    return {
        "trajectory_length": len(trajectory),
        "tool_call_count": tool_call_count,
        "tool_response_count": tool_response_count,
        "has_think": has_think,
    }


def normalize_record(record: dict, index: int) -> dict:
    """Normalize one raw Hermes record to internal format."""
    # Detect trajectory field
    traj_field = None
    for candidate in ("conversations", "trajectory", "messages"):
        if candidate in record and isinstance(record[candidate], list):
            traj_field = candidate
            break
    if traj_field is None:
        raise ValueError(f"No trajectory field found in record. Keys: {list(record.keys())}")

    raw_traj = record[traj_field]
    trajectory = []
    for msg in raw_traj:
        role = normalize_role(msg.get("role", msg.get("from", "")))
        content = msg.get("content", msg.get("value", "")) or ""
        trajectory.append({"role": role, "content": content})

    # Generate a stable source_trace_id from record content
    source_id = record.get("id") or record.get("source_id")
    if source_id is None:
        h = hashlib.sha256(json.dumps(raw_traj, sort_keys=True).encode()).hexdigest()[:16]
        source_id = f"hermes_{h}"

    metadata = extract_metadata(record)
    metadata.update(derive_trace_metadata(trajectory))

    return {
        "id": f"trace_{index:06d}_var_00",
        "source_trace_id": str(source_id),
        "trajectory": trajectory,
        "is_anomalous": False,
        "anomaly_type": None,
        "bad_step": None,
        "generation_rule": None,
        "metadata": metadata,
    }


def normalize_file(input_path: Path, output_path: Path) -> int:
    """Normalize all records in a JSONL file.

    Returns number of records written.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    errors = 0

    with input_path.open() as fin, output_path.open("w") as fout:
        for i, line in enumerate(fin):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                normalized = normalize_record(record, i)
                fout.write(json.dumps(normalized) + "\n")
                written += 1
            except Exception as exc:
                errors += 1
                if errors <= 5:
                    print(f"  WARN: skipping record {i}: {exc}")

    print(f"Normalized {written:,} records → {output_path} ({errors} errors)")
    return written


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Raw JSONL file")
    parser.add_argument("output", type=Path, help="Normalized output JSONL file")
    args = parser.parse_args()

    normalize_file(args.input, args.output)
