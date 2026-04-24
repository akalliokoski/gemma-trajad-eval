from dataset_builder.inspect_traces import (
    count_roles,
    print_eligibility_report,
    print_sample,
    print_schema_report,
    print_summary,
    print_tool_stats,
)


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


def test_print_schema_report_describes_detected_message_shapes(capsys) -> None:
    records = [
        {"id": "raw-1", "conversations": RAW_TRAJECTORY, "tools": "[]"},
        {"id": "norm-1", "trajectory": NORMALIZED_TRAJECTORY},
    ]

    print_schema_report(records)
    output = capsys.readouterr().out

    assert "Schema report:" in output
    assert "conversations: 1" in output
    assert "trajectory: 1" in output
    assert "from/value: 1" in output
    assert "role/content: 1" in output
    assert "Records with tools field: 50.0%" in output
    assert "Records with embedded <tool_call>: 50.0%" in output


def test_print_tool_stats_reports_average_call_and_pair_rates(capsys) -> None:
    records = [
        {"id": "raw-1", "conversations": RAW_TRAJECTORY},
        {
            "id": "norm-1",
            "trajectory": [
                {"role": "system", "content": "sys"},
                {"role": "user", "content": "hi"},
                {"role": "assistant", "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'},
                {"role": "tool", "content": "<tool_response>ok</tool_response>"},
                {"role": "assistant", "content": '<tool_call>{"name": "read_file", "arguments": {"path": "x"}}</tool_call>'},
                {"role": "tool", "content": "<tool_response>contents</tool_response>"},
            ],
        },
    ]

    print_tool_stats(records)
    output = capsys.readouterr().out

    assert "Tool stats:" in output
    assert "Average <tool_call> blocks per trace: 1.5" in output
    assert "Average <tool_response> blocks per trace: 1.5" in output
    assert "Traces with >=1 tool call: 100.0%" in output
    assert "Traces with >=2 assistant/tool-call pairs: 50.0%" in output


def test_print_eligibility_report_estimates_rule_coverage(capsys) -> None:
    records = [
        {"id": "no-tool", "trajectory": NORMALIZED_TRAJECTORY},
        {"id": "raw-1", "conversations": RAW_TRAJECTORY},
        {
            "id": "multi-pair",
            "trajectory": [
                {"role": "system", "content": "sys"},
                {"role": "user", "content": "hi"},
                {"role": "assistant", "content": '<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>'},
                {"role": "tool", "content": "<tool_response>ok</tool_response>"},
                {"role": "assistant", "content": '<tool_call>{"name": "read_file", "arguments": {"path": "x"}}</tool_call>'},
                {"role": "tool", "content": "<tool_response>contents</tool_response>"},
            ],
        },
    ]

    print_eligibility_report(records)
    output = capsys.readouterr().out

    assert "Eligibility report:" in output
    assert "P1 wrong_tool_choice: 2/3 (66.7%)" in output
    assert "P2 bad_tool_arguments: 2/3 (66.7%)" in output
    assert "P3/P4/P5 tool-interaction rules: 2/3 (66.7%)" in output
    assert "P8 multi-tool-step rules: 1/3 (33.3%)" in output
