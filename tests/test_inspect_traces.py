from dataset_builder.inspect_traces import count_roles, print_sample, print_summary


RAW_TRAJECTORY = [
    {"from": "system", "value": "sys"},
    {"from": "human", "value": "hi"},
    {
        "from": "gpt",
        "value": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>',
    },
    {"from": "tool", "value": "<tool_response>ok</tool_response>"},
]


NORMALIZED_TRAJECTORY = [
    {"role": "system", "content": "sys"},
    {"role": "user", "content": "hi"},
    {"role": "assistant", "content": "plain answer"},
]


def test_count_roles_supports_sharegpt_style_messages() -> None:
    counts = count_roles(RAW_TRAJECTORY)

    assert counts == {"system": 1, "human": 1, "gpt": 1, "tool": 1}


def test_print_summary_supports_normalized_and_raw_messages(capsys) -> None:
    records = [
        {"id": "raw-1", "conversations": RAW_TRAJECTORY},
        {"id": "norm-1", "trajectory": NORMALIZED_TRAJECTORY},
    ]

    print_summary(records)
    output = capsys.readouterr().out

    assert "Total records: 2" in output
    assert "system" in output
    assert "human" in output
    assert "assistant" in output
    assert "Messages with <tool_call>: 1" in output
    assert "Traces with >=1 tool call: 50.0%" in output
    assert "Traces with >=2 assistant/tool-call pairs: 0.0%" in output


def test_print_summary_handles_empty_records(capsys) -> None:
    print_summary([])
    output = capsys.readouterr().out

    assert "Total records: 0" in output
    assert "Trajectory length" not in output
    assert "WARNING" not in output


def test_print_summary_warns_only_when_trajectory_field_is_missing(capsys) -> None:
    print_summary([{"id": "missing-traj"}])
    missing_output = capsys.readouterr().out

    assert "WARNING: could not detect trajectory field." in missing_output
    assert "id" in missing_output

    print_summary([{"id": "empty-traj", "trajectory": []}])
    empty_output = capsys.readouterr().out

    assert "WARNING" not in empty_output
    assert "Trajectory length — min: 0, max: 0, avg: 0.0" in empty_output


def test_print_sample_supports_mixed_tool_and_non_tool_messages(capsys) -> None:
    records = [
        {
            "id": "raw-1",
            "conversations": [
                {"from": "human", "value": "hello"},
                {
                    "from": "gpt",
                    "value": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>',
                },
                {"from": "tool", "value": "<tool_response>ok</tool_response>"},
                {"from": "gpt", "value": "done"},
            ],
        }
    ]

    print_sample(records, n=1)
    output = capsys.readouterr().out

    assert "[0] human: 'hello'" in output
    assert "[1] gpt: '<tool_call>" in output
    assert "[2] tool: '<tool_response>ok</tool_response>'" in output
    assert "[3] gpt: 'done'" in output
