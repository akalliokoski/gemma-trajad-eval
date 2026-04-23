from dataset_builder.build_trajad_dataset import unique_source_ids_in_order


def test_unique_source_ids_in_order_preserves_first_seen_order() -> None:
    records = [
        {"source_trace_id": "trace-b"},
        {"source_trace_id": "trace-a"},
        {"source_trace_id": "trace-b"},
        {"source_trace_id": "trace-c"},
        {"source_trace_id": "trace-a"},
    ]

    assert unique_source_ids_in_order(records) == ["trace-b", "trace-a", "trace-c"]
