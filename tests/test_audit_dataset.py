from pathlib import Path

from dataset_builder.audit_dataset import bucket_bad_step_position, summarize_file, summarize_records


RECORDS = [
    {
        "id": "clean-train",
        "source_trace_id": "s1",
        "split": "train",
        "trajectory": [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "done"},
        ],
        "is_anomalous": False,
        "anomaly_type": None,
        "anomaly_class": None,
        "bad_step": None,
        "metadata": {"tool_call_count": 0},
    },
    {
        "id": "anomaly-dev",
        "source_trace_id": "s2",
        "split": "dev",
        "trajectory": [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'},
            {"role": "tool", "content": "<tool_response>ok</tool_response>"},
            {"role": "assistant", "content": "done"},
        ],
        "is_anomalous": True,
        "anomaly_type": "invalid_tool_json",
        "anomaly_class": "task_failure",
        "bad_step": 2,
        "metadata": {"tool_call_count": 1},
    },
    {
        "id": "anomaly-test",
        "source_trace_id": "s3",
        "split": "test",
        "trajectory": [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'},
            {"role": "tool", "content": "<tool_response>ok</tool_response>"},
            {"role": "assistant", "content": '<tool_call>{"name": "read_file", "arguments": {"path": "x"}}</tool_call>'},
            {"role": "tool", "content": "<tool_response>contents</tool_response>"},
        ],
        "is_anomalous": True,
        "anomaly_type": "repeated_step",
        "anomaly_class": "process_inefficiency",
        "bad_step": 4,
        "metadata": {"tool_call_count": 2},
    },
]


def test_bucket_bad_step_position_uses_early_middle_late_ranges() -> None:
    assert bucket_bad_step_position(bad_step=0, trajectory_length=6) == "early"
    assert bucket_bad_step_position(bad_step=2, trajectory_length=6) == "middle"
    assert bucket_bad_step_position(bad_step=5, trajectory_length=6) == "late"


def test_summarize_records_reports_counts_and_averages() -> None:
    summary = summarize_records(RECORDS)

    assert summary["total_records"] == 3
    assert summary["split_counts"] == {"dev": 1, "test": 1, "train": 1}
    assert summary["anomaly_type_counts"] == {"invalid_tool_json": 1, "repeated_step": 1}
    assert summary["anomaly_class_counts"] == {"process_inefficiency": 1, "task_failure": 1}
    assert summary["average_trajectory_length_by_split"] == {"dev": 5.0, "test": 6.0, "train": 3.0}
    assert summary["average_tool_call_count_by_split"] == {"dev": 1.0, "test": 2.0, "train": 0.0}
    assert summary["bad_step_position_buckets"] == {"late": 1, "middle": 1}


def test_summarize_file_streams_jsonl_without_loading_everything_first(tmp_path: Path) -> None:
    path = tmp_path / "sample.jsonl"
    path.write_text("\n".join(__import__("json").dumps(record) for record in RECORDS) + "\n")

    summary = summarize_file(path)

    assert summary["total_records"] == 3
    assert summary["split_counts"] == {"dev": 1, "test": 1, "train": 1}
