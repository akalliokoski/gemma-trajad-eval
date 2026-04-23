import copy
import random

from dataset_builder.perturbations import (
    apply_perturbation,
    p1_replace_tool_choice,
)
from dataset_builder.validate_labels import validate_record


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
        {"role": "tool", "content": "<tool_response>ok</tool_response>"},
        {"role": "assistant", "content": "done"},
    ],
}


def test_validate_record_requires_anomaly_class_for_anomalous_records() -> None:
    record = {
        **BASE_RECORD,
        "is_anomalous": True,
        "anomaly_type": "wrong_tool_choice",
        "anomaly_class": None,
        "bad_step": 2,
    }

    errors = validate_record(record, 0)

    assert any("anomalous record has null anomaly_class" in error for error in errors)


def test_validate_record_rejects_unknown_anomaly_class() -> None:
    record = {
        **BASE_RECORD,
        "is_anomalous": True,
        "anomaly_type": "wrong_tool_choice",
        "anomaly_class": "made_up_class",
        "bad_step": 2,
    }

    errors = validate_record(record, 0)

    assert any("unknown anomaly_class" in error for error in errors)


def test_validate_record_requires_normals_to_keep_anomaly_class_null() -> None:
    record = {
        **BASE_RECORD,
        "is_anomalous": False,
        "anomaly_type": None,
        "anomaly_class": "task_failure",
        "bad_step": None,
    }

    errors = validate_record(record, 0)

    assert any("normal record has non-null anomaly_class" in error for error in errors)


def test_apply_perturbation_sets_top_level_anomaly_class() -> None:
    result = apply_perturbation(
        {
            **BASE_RECORD,
            "is_anomalous": False,
            "anomaly_type": None,
            "anomaly_class": None,
            "bad_step": None,
        },
        p1_replace_tool_choice,
        variant_index=1,
        rng=random.Random(0),
    )

    assert result is not None
    assert result["anomaly_type"] == "wrong_tool_choice"
    assert result["anomaly_class"] == "process_inefficiency"


def make_anomalous_record(*, generation_rule: str, bad_step: int, trajectory: list[dict], anomaly_type: str) -> dict:
    return {
        "id": f"trace-{generation_rule.lower()}",
        "source_trace_id": "trace-1",
        "trajectory": copy.deepcopy(trajectory),
        "is_anomalous": True,
        "anomaly_type": anomaly_type,
        "anomaly_class": "task_failure" if anomaly_type != "repeated_step" and anomaly_type != "continued_after_sufficient_evidence" else ("process_inefficiency" if anomaly_type == "repeated_step" else "unwarranted_continuation"),
        "bad_step": bad_step,
        "generation_rule": generation_rule,
    }


def test_validate_record_rejects_repeated_step_when_bad_step_is_not_duplicate_start() -> None:
    duplicated_pair_trajectory = [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "find x"},
        {"role": "assistant", "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'},
        {"role": "tool", "content": "<tool_response>first</tool_response>"},
        {"role": "assistant", "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'},
        {"role": "tool", "content": "<tool_response>first</tool_response>"},
        {"role": "assistant", "content": "done"},
    ]
    record = make_anomalous_record(
        generation_rule="P4",
        bad_step=5,
        trajectory=duplicated_pair_trajectory,
        anomaly_type="repeated_step",
    )

    errors = validate_record(record, 0)

    assert any("P4 repeated_step bad_step must point to the duplicated assistant step" in error for error in errors)


def test_validate_record_rejects_continuation_when_bad_step_skips_first_extra_step() -> None:
    continued_trajectory = [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "find x"},
        {"role": "assistant", "content": "done"},
        {"role": "assistant", "content": '<tool_call>{"name": "search_web", "arguments": {"query": "extra"}}</tool_call>'},
        {"role": "tool", "content": "<tool_response>redundant</tool_response>"},
        {"role": "assistant", "content": "still done"},
    ]
    record = make_anomalous_record(
        generation_rule="P5",
        bad_step=4,
        trajectory=continued_trajectory,
        anomaly_type="continued_after_sufficient_evidence",
    )
    record["anomaly_class"] = "unwarranted_continuation"

    errors = validate_record(record, 0)

    assert any("P5 continuation bad_step must point to the first unnecessary extra step" in error for error in errors)


def test_validate_record_rejects_premature_final_answer_when_bad_step_is_not_cut_point() -> None:
    truncated_trajectory = [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "find x"},
        {"role": "assistant", "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'},
        {"role": "tool", "content": "<tool_response>first</tool_response>"},
        {"role": "assistant", "content": "Based on my analysis so far, I have reached a conclusion without the final check."},
    ]
    record = make_anomalous_record(
        generation_rule="P7",
        bad_step=3,
        trajectory=truncated_trajectory,
        anomaly_type="premature_final_answer",
    )

    errors = validate_record(record, 0)

    assert any("P7 premature_final_answer bad_step must point to the inserted premature final answer" in error for error in errors)


def test_validate_record_accepts_skipped_required_step_missing_position_at_end() -> None:
    skipped_trajectory = [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "find x"},
        {"role": "assistant", "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'},
        {"role": "tool", "content": "<tool_response>first</tool_response>"},
    ]
    record = make_anomalous_record(
        generation_rule="P3",
        bad_step=len(skipped_trajectory),
        trajectory=skipped_trajectory,
        anomaly_type="skipped_required_step",
    )

    errors = validate_record(record, 0)

    assert not any("out of range" in error for error in errors)
