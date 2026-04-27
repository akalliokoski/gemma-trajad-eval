from pathlib import Path

from dataset_builder.perturbation_diagnostics import (
    compute_rule_diagnostics,
    format_diagnostics_table,
    write_diagnostics,
)
from dataset_builder.perturbations import p1_replace_tool_choice


MAPPED_RECORD = {
    "id": "trace-mapped",
    "source_trace_id": "trace-mapped",
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
}

UNMAPPED_RECORD = {
    "id": "trace-unmapped",
    "source_trace_id": "trace-unmapped",
    "trajectory": [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "apply edit"},
        {
            "role": "assistant",
            "content": '<tool_call>{"name": "patch", "arguments": {"path": "a.txt", "old_string": "a", "new_string": "b"}}</tool_call>',
        },
        {"role": "tool", "content": '<tool_response>{"ok": true}</tool_response>'},
        {"role": "assistant", "content": "Patch applied."},
    ],
}

NO_TOOL_RECORD = {
    "id": "trace-no-tool",
    "source_trace_id": "trace-no-tool",
    "trajectory": [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "say hi"},
        {"role": "assistant", "content": "hello"},
    ],
}


def test_compute_rule_diagnostics_distinguishes_ineligible_and_failed_records() -> None:
    diagnostics = compute_rule_diagnostics(
        [MAPPED_RECORD, UNMAPPED_RECORD, NO_TOOL_RECORD],
        [p1_replace_tool_choice],
        seed=7,
    )

    assert diagnostics["total_records"] == 3
    rule = diagnostics["rules"][0]
    assert rule["rule_name"] == "p1_replace_tool_choice"
    assert rule["eligible"] == 2
    assert rule["succeeded"] == 1
    assert rule["failed"] == 1
    assert rule["ineligible"] == 1
    assert rule["success_rate"] == 0.5
    assert rule["failure_examples"][0]["source_trace_id"] == "trace-unmapped"
    assert rule["failure_examples"][0]["tool_name"] == "patch"


def test_write_diagnostics_and_table(tmp_path: Path) -> None:
    diagnostics = compute_rule_diagnostics([MAPPED_RECORD, UNMAPPED_RECORD], [p1_replace_tool_choice], seed=11)
    out_path = tmp_path / "perturbation_diagnostics.json"

    write_diagnostics(diagnostics, out_path)
    table = format_diagnostics_table(diagnostics)

    assert out_path.exists()
    assert "Rule | Eligible | Succeeded | Failed | Success Rate" in table
    assert "p1_replace_tool_choice" in table
    assert "50.0%" in table
