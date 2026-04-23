import random

from dataset_builder.coherence import is_plausible_trajectory
from dataset_builder.perturbations import p4_duplicate_tool_step


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
    "is_anomalous": True,
    "anomaly_type": "wrong_tool_choice",
    "anomaly_class": "process_inefficiency",
    "bad_step": 2,
}


def make_record(trajectory: list[dict]) -> dict:
    record = dict(BASE_RECORD)
    record["trajectory"] = trajectory
    return record


def test_accepts_structurally_complete_tool_interaction() -> None:
    ok, reason = is_plausible_trajectory(BASE_RECORD)

    assert ok is True
    assert reason is None


def test_rejects_dangling_assistant_tool_call_without_tool_response() -> None:
    record = make_record(
        [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "find x"},
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>',
            },
            {"role": "assistant", "content": "done"},
        ]
    )

    ok, reason = is_plausible_trajectory(record)

    assert ok is False
    assert reason == "dangling_tool_call"


def test_rejects_tool_response_without_matching_assistant_call() -> None:
    record = make_record(
        [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "find x"},
            {"role": "assistant", "content": "done"},
            {"role": "tool", "content": "<tool_response>ok</tool_response>"},
        ]
    )

    ok, reason = is_plausible_trajectory(record)

    assert ok is False
    assert reason == "orphan_tool_response"


def test_rejects_exact_adjacent_duplicate_tool_response_fragment() -> None:
    record = make_record(
        [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "find x"},
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>',
            },
            {"role": "tool", "content": "<tool_response>ok</tool_response>"},
            {"role": "tool", "content": "<tool_response>ok</tool_response>"},
            {"role": "assistant", "content": "done"},
        ]
    )

    ok, reason = is_plausible_trajectory(record)

    assert ok is False
    assert reason == "duplicate_adjacent_fragment"


def test_rejects_misaligned_swap_that_leaves_tool_before_its_call() -> None:
    record = make_record(
        [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "find x"},
            {"role": "tool", "content": "<tool_response>ok</tool_response>"},
            {
                "role": "assistant",
                "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>',
            },
            {"role": "assistant", "content": "done"},
        ]
    )

    ok, reason = is_plausible_trajectory(record)

    assert ok is False
    assert reason == "orphan_tool_response"


def test_accepts_repeated_step_perturbation_as_plausible() -> None:
    perturbed = p4_duplicate_tool_step(make_record(BASE_RECORD["trajectory"]), random.Random(0))

    assert perturbed is not None
    ok, reason = is_plausible_trajectory(perturbed)

    assert ok is True
    assert reason is None
