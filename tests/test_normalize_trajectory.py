from dataset_builder.normalize_trajectory import derive_trace_metadata, normalize_record


RAW_RECORD = {
    "id": "source-1",
    "category": "research",
    "metadata": {"source": "hermes", "custom_flag": True},
    "conversations": [
        {"from": "system", "value": "sys"},
        {"from": "human", "value": "hello"},
        {
            "from": "gpt",
            "value": (
                '<think>need tool</think>'
                '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'
            ),
        },
        {"from": "tool", "value": "<tool_response>ok</tool_response>"},
        {
            "from": "gpt",
            "value": '<tool_call>{"name": "read_file", "arguments": {"path": "notes.txt"}}</tool_call>',
        },
        {"from": "tool", "value": "<tool_response>done</tool_response>"},
    ],
}


def test_derive_trace_metadata_counts_structural_markers() -> None:
    trajectory = [
        {"role": "assistant", "content": "<think>plan</think><tool_call>{}</tool_call>"},
        {"role": "tool", "content": "<tool_response>ok</tool_response>"},
        {"role": "assistant", "content": "plain answer <tool_call>{}</tool_call>"},
    ]

    metadata = derive_trace_metadata(trajectory)

    assert metadata == {
        "trajectory_length": 3,
        "tool_call_count": 2,
        "tool_response_count": 1,
        "has_think": True,
    }


def test_normalize_record_merges_derived_metadata_without_changing_trajectory_shape() -> None:
    normalized = normalize_record(RAW_RECORD, index=7)

    assert normalized["trajectory"] == [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "hello"},
        {
            "role": "assistant",
            "content": (
                '<think>need tool</think>'
                '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'
            ),
        },
        {"role": "tool", "content": "<tool_response>ok</tool_response>"},
        {
            "role": "assistant",
            "content": '<tool_call>{"name": "read_file", "arguments": {"path": "notes.txt"}}</tool_call>',
        },
        {"role": "tool", "content": "<tool_response>done</tool_response>"},
    ]

    assert normalized["metadata"] == {
        "category": "research",
        "source": "hermes",
        "custom_flag": True,
        "trajectory_length": 6,
        "tool_call_count": 2,
        "tool_response_count": 2,
        "has_think": True,
    }
