from dataset_builder.build_trajad_dataset import build_all_records_with_split, unique_source_ids_in_order


def test_unique_source_ids_in_order_preserves_first_seen_order() -> None:
    records = [
        {"source_trace_id": "trace-b"},
        {"source_trace_id": "trace-a"},
        {"source_trace_id": "trace-b"},
        {"source_trace_id": "trace-c"},
        {"source_trace_id": "trace-a"},
    ]

    assert unique_source_ids_in_order(records) == ["trace-b", "trace-a", "trace-c"]


def test_build_all_records_with_split_preserves_split_labels() -> None:
    split_records = {
        "train": [{"id": "train-1", "split": "train"}],
        "dev": [{"id": "dev-1", "split": "dev"}],
        "test": [{"id": "test-1", "split": "test"}],
    }

    combined = build_all_records_with_split(split_records)

    assert [record["id"] for record in combined] == ["train-1", "dev-1", "test-1"]
    assert [record["split"] for record in combined] == ["train", "dev", "test"]
