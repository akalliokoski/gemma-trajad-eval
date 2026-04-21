import json

from dataset_builder.perturbations import parse_tool_call, replace_tool_call
from dataset_builder.validate_labels import validate_record


def test_replace_tool_call_handles_unicode_escapes_in_json() -> None:
    original_call = {
        "name": "read_file",
        "arguments": {"path": "C:/tmp/naïve-✓.txt", "note": "\u2713"},
    }
    content = f"prefix <tool_call>{json.dumps(original_call)}</tool_call> suffix"

    new_call = {
        "name": "read_file_v2",
        "arguments": {"path": "C:/tmp/naïve-✓.txt", "note": "\u2713"},
    }

    replaced = replace_tool_call(content, new_call)

    assert replaced.startswith("prefix ")
    assert replaced.endswith(" suffix")
    assert parse_tool_call(replaced) == new_call


def test_validate_record_allows_missing_step_index_at_trajectory_end() -> None:
    record = {
        "id": "example_var_03",
        "source_trace_id": "example",
        "trajectory": [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "user"},
            {"role": "assistant", "content": "final answer without required call"},
        ],
        "is_anomalous": True,
        "anomaly_type": "skipped_required_step",
        "bad_step": 3,
        "generation_rule": "P3",
    }

    assert validate_record(record, 0) == []
