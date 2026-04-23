import random

from dataset_builder.perturbations import apply_perturbation, p1_replace_tool_choice
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
