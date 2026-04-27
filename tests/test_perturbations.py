import json
import random

from dataset_builder.coherence import is_plausible_trajectory
from dataset_builder.perturbations import (
    ALL_RULES,
    ANOMALY_TYPE_TO_CLASS,
    p5_append_continuation,
    p6_contradict_final_answer,
    p9_invalid_tool_json,
    parse_tool_call,
    replace_tool_call,
)
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


def test_replace_tool_call_only_replaces_first_tool_call_in_message() -> None:
    first_call = {"name": "read_file", "arguments": {"path": "a.txt"}}
    second_call = {"name": "write_file", "arguments": {"path": "b.txt", "content": "x"}}
    content = (
        f'<tool_call>{json.dumps(first_call)}</tool_call>'
        f'\n<tool_call>{json.dumps(second_call)}</tool_call>'
    )

    new_call = {"name": "list_directory", "arguments": {"path": "a.txt"}}

    replaced = replace_tool_call(content, new_call)

    assert replaced.count("<tool_call>") == 2
    assert parse_tool_call(replaced) == new_call
    assert '"name": "write_file"' in replaced
    assert '"name": "list_directory"' in replaced


BASE_RECORD = {
    "id": "trace-1",
    "source_trace_id": "trace-1",
    "trajectory": [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "find x"},
        {
            "role": "assistant",
            "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>',
        },
        {
            "role": "tool",
            "content": '<tool_response>{"results": [{"title": "X found"}], "count": 1}</tool_response>',
        },
        {"role": "assistant", "content": "I found one matching result for x."},
    ],
    "is_anomalous": False,
    "anomaly_type": None,
    "anomaly_class": None,
    "bad_step": None,
}


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
        "anomaly_class": "task_failure",
        "bad_step": 3,
        "generation_rule": "P3",
    }

    assert validate_record(record, 0) == []


def test_p5_appends_structurally_complete_extra_continuation() -> None:
    perturbed = p5_append_continuation(BASE_RECORD, random.Random(0))

    assert perturbed is not None
    assert len(perturbed["trajectory"]) == len(BASE_RECORD["trajectory"]) + 3
    assert perturbed["bad_step"] == len(BASE_RECORD["trajectory"])
    extra_steps = perturbed["trajectory"][-3:]
    assert [step["role"] for step in extra_steps] == ["assistant", "tool", "assistant"]
    assert "<tool_call>" in extra_steps[0]["content"]
    assert "<tool_response>" in extra_steps[1]["content"]
    assert "<tool_call>" not in extra_steps[2]["content"]
    perturbed["anomaly_class"] = ANOMALY_TYPE_TO_CLASS[perturbed["anomaly_type"]]
    assert validate_record(perturbed, 0) == []
    assert is_plausible_trajectory(perturbed) == (True, None)


def test_p6_contradicts_tool_result_without_bracketed_marker() -> None:
    perturbed = p6_contradict_final_answer(BASE_RECORD, random.Random(0))

    assert perturbed is not None
    final_message = perturbed["trajectory"][-1]["content"]

    assert perturbed["bad_step"] == len(BASE_RECORD["trajectory"]) - 1
    assert "[CONTRADICTION]" not in final_message
    assert "did not show a concrete result" in final_message
    assert "one matching result" not in final_message
    perturbed["anomaly_class"] = ANOMALY_TYPE_TO_CLASS[perturbed["anomaly_type"]]
    assert validate_record(perturbed, 0) == []


def test_p9_invalid_tool_json_marks_bad_assistant_step() -> None:
    perturbed = p9_invalid_tool_json(BASE_RECORD, random.Random(0))

    assert perturbed is not None
    assert perturbed["anomaly_type"] == "invalid_tool_json"
    assert perturbed["bad_step"] == 2
    assert perturbed["generation_rule"] == "P9"
    assert perturbed["trajectory"][2]["role"] == "assistant"
    assert "<tool_call>" in perturbed["trajectory"][2]["content"]
    assert parse_tool_call(perturbed["trajectory"][2]["content"]) is None
    perturbed["anomaly_class"] = ANOMALY_TYPE_TO_CLASS[perturbed["anomaly_type"]]
    assert validate_record(perturbed, 0) == []


def test_all_rules_includes_invalid_tool_json_rule() -> None:
    assert p9_invalid_tool_json in ALL_RULES
