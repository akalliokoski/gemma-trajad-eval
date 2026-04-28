import json
import random

from dataset_builder.coherence import is_plausible_trajectory
from dataset_builder.perturbations import (
    ALL_RULES,
    ANOMALY_TYPE_TO_CLASS,
    NEARBY_TOOLS,
    p1_replace_tool_choice,
    p2_mutate_argument_value,
    p3_remove_step_pair,
    p4_duplicate_tool_step,
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


def test_p1_returns_none_for_unmapped_tool_instead_of_fabricating_v2_name() -> None:
    record = {
        **BASE_RECORD,
        "trajectory": [
            BASE_RECORD["trajectory"][0],
            BASE_RECORD["trajectory"][1],
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "totally_custom_tool", "arguments": {"query": "x"}}</tool_call>',
            },
            BASE_RECORD["trajectory"][3],
            BASE_RECORD["trajectory"][4],
        ],
    }

    perturbed = p1_replace_tool_choice(record, random.Random(0))

    assert perturbed is None


def test_p1_uses_curated_realistic_replacement_for_terminal() -> None:
    record = {
        **BASE_RECORD,
        "trajectory": [
            BASE_RECORD["trajectory"][0],
            BASE_RECORD["trajectory"][1],
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "terminal", "arguments": {"command": "pwd"}}</tool_call>',
            },
            BASE_RECORD["trajectory"][3],
            BASE_RECORD["trajectory"][4],
        ],
    }

    perturbed = p1_replace_tool_choice(record, random.Random(0))

    assert perturbed is not None
    mutated = parse_tool_call(perturbed["trajectory"][2]["content"])
    assert mutated is not None
    assert mutated["name"] in NEARBY_TOOLS["terminal"]
    assert mutated["arguments"] == {"code": 'import subprocess\nsubprocess.run("pwd", shell=True, check=False)'}
    assert not mutated["name"].endswith("_v2")


def test_p1_uses_curated_realistic_replacement_for_search_files() -> None:
    record = {
        **BASE_RECORD,
        "trajectory": [
            BASE_RECORD["trajectory"][0],
            BASE_RECORD["trajectory"][1],
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "search_files", "arguments": {"target": "files", "pattern": "*.py"}}</tool_call>',
            },
            BASE_RECORD["trajectory"][3],
            BASE_RECORD["trajectory"][4],
        ],
    }

    perturbed = p1_replace_tool_choice(record, random.Random(0))

    assert perturbed is not None
    mutated = parse_tool_call(perturbed["trajectory"][2]["content"])
    assert mutated is not None
    assert mutated["name"] in NEARBY_TOOLS["search_files"]
    assert mutated["arguments"] == {"command": "find . -name '*.py' 2>/dev/null | head -50"}
    assert not mutated["name"].endswith("_v2")


def test_p2_mutates_path_like_strings_without_corrupted_suffix() -> None:
    record = {
        **BASE_RECORD,
        "trajectory": [
            BASE_RECORD["trajectory"][0],
            BASE_RECORD["trajectory"][1],
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "read_file", "arguments": {"path": "config/settings.py"}}</tool_call>',
            },
            BASE_RECORD["trajectory"][3],
            BASE_RECORD["trajectory"][4],
        ],
    }

    perturbed = p2_mutate_argument_value(record, random.Random(0))

    assert perturbed is not None
    mutated = parse_tool_call(perturbed["trajectory"][2]["content"])
    assert mutated is not None
    assert mutated["arguments"]["path"] == "config/settings-old.py"
    assert "_CORRUPTED" not in perturbed["trajectory"][2]["content"]


def test_p2_toggles_boolean_arguments_instead_of_treating_them_as_ints() -> None:
    record = {
        **BASE_RECORD,
        "trajectory": [
            BASE_RECORD["trajectory"][0],
            BASE_RECORD["trajectory"][1],
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "terminal", "arguments": {"background": true}}</tool_call>',
            },
            BASE_RECORD["trajectory"][3],
            BASE_RECORD["trajectory"][4],
        ],
    }

    perturbed = p2_mutate_argument_value(record, random.Random(0))

    assert perturbed is not None
    mutated = parse_tool_call(perturbed["trajectory"][2]["content"])
    assert mutated is not None
    assert mutated["arguments"]["background"] is False


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


def test_p3_prefers_removing_non_terminal_pair_when_available() -> None:
    record = {
        **BASE_RECORD,
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
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "read_file", "arguments": {"path": "report.md"}}</tool_call>',
            },
            {
                "role": "tool",
                "content": '<tool_response>{"content": "report details"}</tool_response>',
            },
            {"role": "assistant", "content": "Final answer based on both checks."},
        ],
    }

    perturbed = p3_remove_step_pair(record, random.Random(0))

    assert perturbed is not None
    assert perturbed["bad_step"] == 2
    assert perturbed["trajectory"][-1]["role"] == "assistant"
    assert '<tool_call>{"name": "read_file"' in perturbed["trajectory"][2]["content"]


def test_p3_returns_shortest_valid_skip_when_only_one_pair_exists() -> None:
    perturbed = p3_remove_step_pair(BASE_RECORD, random.Random(0))

    assert perturbed is not None
    assert len(BASE_RECORD["trajectory"]) == 5
    assert len(perturbed["trajectory"]) == 3
    assert perturbed["bad_step"] == 2
    assert [step["role"] for step in perturbed["trajectory"]] == ["system", "user", "assistant"]
    assert perturbed["trajectory"][-1]["content"] == "I found one matching result for x."


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


def test_p4_duplicates_pair_with_exact_content_and_marks_duplicate_step() -> None:
    perturbed = p4_duplicate_tool_step(BASE_RECORD, random.Random(0))

    assert perturbed is not None
    assert len(perturbed["trajectory"]) == len(BASE_RECORD["trajectory"]) + 2
    assert perturbed["bad_step"] == 4
    assert perturbed["trajectory"][perturbed["bad_step"]]["content"] == BASE_RECORD["trajectory"][2]["content"]
    assert perturbed["trajectory"][perturbed["bad_step"] + 1]["content"] == BASE_RECORD["trajectory"][3]["content"]
    assert perturbed["trajectory"][2]["content"] == BASE_RECORD["trajectory"][2]["content"]
    assert perturbed["trajectory"][3]["content"] == BASE_RECORD["trajectory"][3]["content"]
    perturbed["anomaly_class"] = ANOMALY_TYPE_TO_CLASS[perturbed["anomaly_type"]]
    assert validate_record(perturbed, 0) == []
    assert is_plausible_trajectory(perturbed) == (True, None)


def test_p4_prefers_single_call_pair_when_mixed_with_compound_pairs() -> None:
    record = {
        **BASE_RECORD,
        "trajectory": [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "find x"},
            {
                "role": "assistant",
                "content": (
                    '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'
                    '\n<tool_call>{"name": "read_file", "arguments": {"path": "report.md"}}</tool_call>'
                ),
            },
            {
                "role": "tool",
                "content": (
                    '<tool_response>{"results": [{"title": "X found"}], "count": 1}</tool_response>'
                    '\n<tool_response>{"content": "report details"}</tool_response>'
                ),
            },
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "terminal", "arguments": {"command": "pwd"}}</tool_call>',
            },
            {
                "role": "tool",
                "content": '<tool_response>{"output": "/tmp"}</tool_response>',
            },
            {"role": "assistant", "content": "Final answer based on both checks."},
        ],
    }

    perturbed = p4_duplicate_tool_step(record, random.Random(0))

    assert perturbed is not None
    assert perturbed["bad_step"] == 6
    assert perturbed["trajectory"][6]["content"] == record["trajectory"][4]["content"]
    assert perturbed["trajectory"][7]["content"] == record["trajectory"][5]["content"]
    assert perturbed["trajectory"][2]["content"] == record["trajectory"][2]["content"]
    assert perturbed["trajectory"][3]["content"] == record["trajectory"][3]["content"]


def test_p5_appends_existing_final_tool_pair_as_unnecessary_continuation() -> None:
    perturbed = p5_append_continuation(BASE_RECORD, random.Random(0))

    assert perturbed is not None
    assert len(perturbed["trajectory"]) == len(BASE_RECORD["trajectory"]) + 3
    assert perturbed["bad_step"] == len(BASE_RECORD["trajectory"])
    extra_steps = perturbed["trajectory"][-3:]
    assert [step["role"] for step in extra_steps] == ["assistant", "tool", "assistant"]
    assert extra_steps[0]["content"] == BASE_RECORD["trajectory"][2]["content"]
    assert extra_steps[1]["content"] == BASE_RECORD["trajectory"][3]["content"]
    assert "previous answer stands" in extra_steps[2]["content"].lower()
    perturbed["anomaly_class"] = ANOMALY_TYPE_TO_CLASS[perturbed["anomaly_type"]]
    assert validate_record(perturbed, 0) == []
    assert is_plausible_trajectory(perturbed) == (True, None)


def test_p5_prefers_established_lightweight_verification_pair_when_mixed() -> None:
    record = {
        **BASE_RECORD,
        "trajectory": [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "inspect repo"},
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "terminal", "arguments": {"command": "git status --short"}}</tool_call>',
            },
            {
                "role": "tool",
                "content": '<tool_response>{"output": ""}</tool_response>',
            },
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "write_file", "arguments": {"path": "notes.md", "content": "saved"}}</tool_call>',
            },
            {
                "role": "tool",
                "content": '<tool_response>{"bytes_written": 5}</tool_response>',
            },
            {"role": "assistant", "content": "Everything needed for the answer is already clear."},
        ],
    }

    perturbed = p5_append_continuation(record, random.Random(0))

    assert perturbed is not None
    extra_steps = perturbed["trajectory"][-3:]
    assert extra_steps[0]["content"] == record["trajectory"][2]["content"]
    assert extra_steps[1]["content"] == record["trajectory"][3]["content"]
    assert '"name": "write_file"' not in extra_steps[0]["content"]
    assert '"name": "search_web"' not in extra_steps[0]["content"]


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
