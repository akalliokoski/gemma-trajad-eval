"""Schema and consistency checks for the TrajAD dataset.

Usage:
    python dataset_builder/validate_labels.py data/processed/train.jsonl
    python dataset_builder/validate_labels.py data/processed/all.jsonl --strict
"""

import argparse
import json
from pathlib import Path

VALID_ANOMALY_TYPES = {
    "wrong_tool_choice",
    "bad_tool_arguments",
    "skipped_required_step",
    "repeated_step",
    "premature_final_answer",
    "continued_after_sufficient_evidence",
    "contradicted_tool_result",
    "hallucinated_tool",
    "invalid_tool_json",
    "unnecessary_replanning",
}

VALID_SPLITS = {"train", "dev", "test"}
VALID_ROLES = {"system", "user", "assistant", "tool"}


def validate_record(record: dict, idx: int) -> list[str]:
    errors: list[str] = []

    def err(msg: str) -> None:
        errors.append(f"[{idx}] {record.get('id', '?')}: {msg}")

    # Required fields
    for field in ("id", "source_trace_id", "trajectory", "is_anomalous"):
        if field not in record:
            err(f"missing required field: {field!r}")

    if errors:
        return errors  # bail early if basic structure is missing

    # Trajectory
    traj = record["trajectory"]
    if not isinstance(traj, list) or len(traj) == 0:
        err("trajectory must be a non-empty list")
    else:
        for step_idx, msg in enumerate(traj):
            if not isinstance(msg, dict):
                err(f"trajectory[{step_idx}] is not a dict")
                continue
            role = msg.get("role")
            if role not in VALID_ROLES:
                err(f"trajectory[{step_idx}] has invalid role: {role!r}")
            if "content" not in msg:
                err(f"trajectory[{step_idx}] missing 'content'")

    # is_anomalous
    is_anomalous = record["is_anomalous"]
    if not isinstance(is_anomalous, bool):
        err(f"is_anomalous must be bool, got {type(is_anomalous).__name__}")

    # Consistency: normal records
    if not is_anomalous:
        if record.get("bad_step") is not None:
            err("normal record has non-null bad_step")
        if record.get("anomaly_type") is not None:
            err("normal record has non-null anomaly_type")

    # Consistency: anomalous records
    if is_anomalous:
        bad_step = record.get("bad_step")
        if bad_step is None:
            err("anomalous record has null bad_step")
        elif not isinstance(bad_step, int):
            err(f"bad_step must be int, got {type(bad_step).__name__}")
        anomaly_type = record.get("anomaly_type")
        if anomaly_type is None:
            err("anomalous record has null anomaly_type")
        elif anomaly_type not in VALID_ANOMALY_TYPES:
            err(f"unknown anomaly_type: {anomaly_type!r}")

        if isinstance(bad_step, int) and isinstance(traj, list):
            max_allowed = len(traj)
            if anomaly_type == "skipped_required_step":
                if not (0 <= bad_step <= max_allowed):
                    err(f"bad_step={bad_step} out of range [0, {max_allowed}] for skipped_required_step")
            elif not (0 <= bad_step < len(traj)):
                err(f"bad_step={bad_step} out of range [0, {len(traj)})")

    # Optional split field
    split = record.get("split")
    if split is not None and split not in VALID_SPLITS:
        err(f"invalid split: {split!r}")

    return errors


def validate_file(path: Path, strict: bool = False) -> bool:
    errors: list[str] = []
    total = 0
    with path.open() as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"[{i}] JSON parse error: {exc}")
                continue
            errors.extend(validate_record(record, i))
            total += 1

    print(f"Validated {total:,} records from {path}")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors[:50]:
            print(f"  {e}")
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more")
        if strict:
            return False
    else:
        print("All records valid.")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSONL file to validate")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 on any error")
    args = parser.parse_args()

    ok = validate_file(args.path, strict=args.strict)
    if args.strict and not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
