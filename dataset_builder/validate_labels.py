"""Schema and consistency checks for the TrajAD dataset.

Usage:
    python dataset_builder/validate_labels.py data/processed/train.jsonl
    python dataset_builder/validate_labels.py data/processed/all.jsonl --strict
"""

import argparse
import json
from pathlib import Path

try:
    from dataset_builder.perturbations import VALID_ANOMALY_CLASSES, has_malformed_tool_call_json
except ModuleNotFoundError:
    from perturbations import VALID_ANOMALY_CLASSES, has_malformed_tool_call_json

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


def _content(step: dict) -> str:
    return step.get("content") or ""


def _has_tool_call(step: dict) -> bool:
    return step.get("role") == "assistant" and "<tool_call>" in _content(step)


def _validate_rule_aware_bad_step(record: dict) -> list[str]:
    errors: list[str] = []
    traj = record.get("trajectory")
    bad_step = record.get("bad_step")
    generation_rule = record.get("generation_rule")

    if not isinstance(traj, list) or not isinstance(bad_step, int):
        return errors

    if generation_rule == "P4":
        if bad_step + 1 >= len(traj):
            errors.append("P4 repeated_step bad_step must leave room for the duplicated assistant/tool pair")
            return errors
        duplicate_assistant = traj[bad_step]
        duplicate_tool = traj[bad_step + 1]
        if not _has_tool_call(duplicate_assistant) or duplicate_tool.get("role") != "tool":
            errors.append("P4 repeated_step bad_step must point to the duplicated assistant step")
            return errors
        if bad_step < 2:
            errors.append("P4 repeated_step bad_step must point to a duplicated pair that follows an original pair")
            return errors
        original_assistant = traj[bad_step - 2]
        original_tool = traj[bad_step - 1]
        if (
            original_assistant.get("role") != duplicate_assistant.get("role")
            or _content(original_assistant) != _content(duplicate_assistant)
            or original_tool.get("role") != duplicate_tool.get("role")
            or _content(original_tool) != _content(duplicate_tool)
        ):
            errors.append("P4 repeated_step bad_step must point to the duplicated assistant step")

    elif generation_rule == "P5":
        if bad_step < 1 or bad_step + 2 >= len(traj):
            errors.append("P5 continuation bad_step must point to the first unnecessary extra step")
            return errors
        prior_step = traj[bad_step - 1]
        first_extra = traj[bad_step]
        middle_extra = traj[bad_step + 1]
        last_extra = traj[bad_step + 2]
        if _has_tool_call(prior_step):
            errors.append("P5 continuation bad_step must point to the first unnecessary extra step")
        elif not _has_tool_call(first_extra):
            errors.append("P5 continuation bad_step must point to the first unnecessary extra step")
        elif middle_extra.get("role") != "tool" or last_extra.get("role") != "assistant":
            errors.append("P5 continuation bad_step must point to the first unnecessary extra step")

    elif generation_rule == "P7":
        if bad_step != len(traj) - 1:
            errors.append("P7 premature_final_answer bad_step must point to the inserted premature final answer")
            return errors
        premature_answer = traj[bad_step]
        if premature_answer.get("role") != "assistant" or _has_tool_call(premature_answer):
            errors.append("P7 premature_final_answer bad_step must point to the inserted premature final answer")
        elif not any(step.get("role") == "tool" for step in traj[:bad_step]):
            errors.append("P7 premature_final_answer requires earlier tool evidence before the inserted premature final answer")

    elif generation_rule == "P9":
        if bad_step < 0 or bad_step >= len(traj):
            errors.append("P9 invalid_tool_json bad_step must point to an assistant tool-call step with malformed JSON")
            return errors
        bad_step_message = traj[bad_step]
        if bad_step_message.get("role") != "assistant" or "<tool_call>" not in _content(bad_step_message):
            errors.append("P9 invalid_tool_json bad_step must point to an assistant tool-call step with malformed JSON")
        elif not has_malformed_tool_call_json(_content(bad_step_message)):
            errors.append("P9 invalid_tool_json bad_step must point to an assistant tool-call step with malformed JSON")

    return errors


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
        if record.get("anomaly_class") is not None:
            err("normal record has non-null anomaly_class")

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

        anomaly_class = record.get("anomaly_class")
        if anomaly_class is None:
            err("anomalous record has null anomaly_class")
        elif anomaly_class not in VALID_ANOMALY_CLASSES:
            err(f"unknown anomaly_class: {anomaly_class!r}")

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

    for rule_error in _validate_rule_aware_bad_step(record):
        err(rule_error)

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
