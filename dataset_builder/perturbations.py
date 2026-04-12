"""Eight perturbation rules for generating synthetic anomalous trajectories.

Each rule takes a normalized trajectory record (is_anomalous=False) and
returns a perturbed copy with is_anomalous=True, bad_step set, and
anomaly_type set.

Rules:
    P1 - replace_tool_choice       → wrong_tool_choice
    P2 - mutate_argument_value     → bad_tool_arguments
    P3 - remove_step_pair          → skipped_required_step
    P4 - duplicate_tool_step       → repeated_step
    P5 - append_continuation       → continued_after_sufficient_evidence
    P6 - contradict_final_answer   → contradicted_tool_result
    P7 - truncate_before_decision  → premature_final_answer
    P8 - swap_dependent_steps      → skipped_required_step
"""

import copy
import json
import random
import re
from typing import Any

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

TOOL_CALL_RE = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)
TOOL_RESP_RE = re.compile(r"<tool_response>(.*?)</tool_response>", re.DOTALL)

NEARBY_TOOLS: dict[str, list[str]] = {
    "search_web": ["search_wikipedia", "search_news", "search_arxiv"],
    "search_wikipedia": ["search_web", "search_news"],
    "read_file": ["list_directory", "read_csv", "read_json"],
    "write_file": ["append_file", "create_file"],
    "run_bash": ["run_python", "run_command"],
    "run_python": ["run_bash", "execute_code"],
    "list_directory": ["read_file", "find_files"],
    "http_get": ["http_post", "fetch_url"],
    "sql_query": ["nosql_query", "read_csv"],
}


def find_assistant_steps(trajectory: list[dict]) -> list[int]:
    """Return indices of assistant steps that contain a tool call."""
    return [
        i
        for i, msg in enumerate(trajectory)
        if msg["role"] == "assistant" and "<tool_call>" in (msg.get("content") or "")
    ]


def parse_tool_call(content: str) -> dict | None:
    m = TOOL_CALL_RE.search(content)
    if m is None:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def replace_tool_call(content: str, new_call: dict) -> str:
    return TOOL_CALL_RE.sub(f"<tool_call>{json.dumps(new_call)}</tool_call>", content)


# ---------------------------------------------------------------------------
# Perturbation rules
# ---------------------------------------------------------------------------


def p1_replace_tool_choice(record: dict, rng: random.Random) -> dict | None:
    """P1: Replace a tool call with a semantically nearby wrong tool."""
    traj = record["trajectory"]
    candidates = find_assistant_steps(traj)
    if not candidates:
        return None

    step_idx = rng.choice(candidates)
    msg = traj[step_idx]
    call = parse_tool_call(msg["content"])
    if call is None:
        return None

    tool_name = call.get("name", "")
    replacements = NEARBY_TOOLS.get(tool_name)
    if not replacements:
        # Generic fallback: append "_v2" suffix
        replacements = [tool_name + "_v2"]

    new_call = dict(call)
    new_call["name"] = rng.choice(replacements)

    out = copy.deepcopy(record)
    out["trajectory"][step_idx]["content"] = replace_tool_call(msg["content"], new_call)
    out["is_anomalous"] = True
    out["anomaly_type"] = "wrong_tool_choice"
    out["bad_step"] = step_idx
    out["generation_rule"] = "P1"
    return out


def p2_mutate_argument_value(record: dict, rng: random.Random) -> dict | None:
    """P2: Corrupt one argument value in a tool call."""
    traj = record["trajectory"]
    candidates = find_assistant_steps(traj)
    if not candidates:
        return None

    step_idx = rng.choice(candidates)
    msg = traj[step_idx]
    call = parse_tool_call(msg["content"])
    if call is None:
        return None

    args = call.get("arguments", call.get("parameters", {}))
    if not isinstance(args, dict) or not args:
        return None

    key = rng.choice(list(args.keys()))
    original = args[key]

    if isinstance(original, str):
        mutated: Any = original + "_CORRUPTED"
    elif isinstance(original, int):
        mutated = original + rng.choice([-999, 999, -1, 1])
    elif isinstance(original, float):
        mutated = original * -1.0
    elif isinstance(original, bool):
        mutated = not original
    elif isinstance(original, list):
        mutated = []
    else:
        mutated = None

    new_args = dict(args)
    new_args[key] = mutated
    new_call = dict(call)
    if "arguments" in call:
        new_call["arguments"] = new_args
    else:
        new_call["parameters"] = new_args

    out = copy.deepcopy(record)
    out["trajectory"][step_idx]["content"] = replace_tool_call(msg["content"], new_call)
    out["is_anomalous"] = True
    out["anomaly_type"] = "bad_tool_arguments"
    out["bad_step"] = step_idx
    out["generation_rule"] = "P2"
    return out


def p3_remove_step_pair(record: dict, rng: random.Random) -> dict | None:
    """P3: Remove one assistant+tool step pair."""
    traj = record["trajectory"]
    # Find consecutive (assistant[tool_call], tool) pairs
    pairs = []
    for i in range(len(traj) - 1):
        if (
            traj[i]["role"] == "assistant"
            and "<tool_call>" in (traj[i].get("content") or "")
            and traj[i + 1]["role"] == "tool"
        ):
            pairs.append(i)

    if not pairs:
        return None

    step_idx = rng.choice(pairs)
    out = copy.deepcopy(record)
    del out["trajectory"][step_idx : step_idx + 2]

    # bad_step = where the removed step was
    out["is_anomalous"] = True
    out["anomaly_type"] = "skipped_required_step"
    out["bad_step"] = step_idx
    out["generation_rule"] = "P3"
    return out


def p4_duplicate_tool_step(record: dict, rng: random.Random) -> dict | None:
    """P4: Duplicate a (assistant[tool_call], tool) pair."""
    traj = record["trajectory"]
    pairs = []
    for i in range(len(traj) - 1):
        if (
            traj[i]["role"] == "assistant"
            and "<tool_call>" in (traj[i].get("content") or "")
            and traj[i + 1]["role"] == "tool"
        ):
            pairs.append(i)

    if not pairs:
        return None

    step_idx = rng.choice(pairs)
    dup_assistant = copy.deepcopy(traj[step_idx])
    dup_tool = copy.deepcopy(traj[step_idx + 1])

    out = copy.deepcopy(record)
    insert_at = step_idx + 2
    out["trajectory"].insert(insert_at, dup_tool)
    out["trajectory"].insert(insert_at, dup_assistant)

    out["is_anomalous"] = True
    out["anomaly_type"] = "repeated_step"
    out["bad_step"] = insert_at  # the duplicate begins here
    out["generation_rule"] = "P4"
    return out


def p5_append_continuation(record: dict, rng: random.Random) -> dict | None:
    """P5: Append an unnecessary follow-up step after the final answer."""
    traj = record["trajectory"]
    if not traj or traj[-1]["role"] != "assistant":
        return None

    # Append a fake extra tool call at the end
    fake_step = {
        "role": "assistant",
        "content": (
            "<think>Let me double-check this with one more search.</think>"
            '<tool_call>{"name": "search_web", "arguments": {"query": "verify previous result"}}</tool_call>'
        ),
    }
    out = copy.deepcopy(record)
    out["trajectory"].append(fake_step)

    out["is_anomalous"] = True
    out["anomaly_type"] = "continued_after_sufficient_evidence"
    out["bad_step"] = len(out["trajectory"]) - 1
    out["generation_rule"] = "P5"
    return out


def p6_contradict_final_answer(record: dict, rng: random.Random) -> dict | None:
    """P6: Alter the final assistant answer so it contradicts the last tool result."""
    traj = record["trajectory"]
    # Find last tool response
    last_tool_idx = None
    for i in range(len(traj) - 1, -1, -1):
        if traj[i]["role"] == "tool":
            last_tool_idx = i
            break

    if last_tool_idx is None:
        return None

    # Find the final assistant message after the last tool
    final_assistant_idx = None
    for i in range(last_tool_idx + 1, len(traj)):
        if traj[i]["role"] == "assistant":
            final_assistant_idx = i

    if final_assistant_idx is None:
        return None

    out = copy.deepcopy(record)
    original = out["trajectory"][final_assistant_idx]["content"] or ""
    # Prepend a contradicting statement
    out["trajectory"][final_assistant_idx]["content"] = (
        "[CONTRADICTION] Based on my analysis, the result is the opposite of what was returned. "
        + original
    )
    out["is_anomalous"] = True
    out["anomaly_type"] = "contradicted_tool_result"
    out["bad_step"] = final_assistant_idx
    out["generation_rule"] = "P6"
    return out


def p7_truncate_before_decision(record: dict, rng: random.Random) -> dict | None:
    """P7: Truncate trajectory before the crucial decision step."""
    traj = record["trajectory"]
    pairs = []
    for i in range(len(traj) - 1):
        if (
            traj[i]["role"] == "assistant"
            and "<tool_call>" in (traj[i].get("content") or "")
            and traj[i + 1]["role"] == "tool"
        ):
            pairs.append(i)

    # Need at least two tool calls to truncate before the last one
    if len(pairs) < 2:
        return None

    # Truncate before the last tool call, then add a fake final answer
    cut_point = pairs[-1]
    fake_answer = {
        "role": "assistant",
        "content": "Based on my analysis so far, I have reached a conclusion without the final check.",
    }
    out = copy.deepcopy(record)
    out["trajectory"] = out["trajectory"][:cut_point] + [fake_answer]

    out["is_anomalous"] = True
    out["anomaly_type"] = "premature_final_answer"
    out["bad_step"] = cut_point
    out["generation_rule"] = "P7"
    return out


def p8_swap_dependent_steps(record: dict, rng: random.Random) -> dict | None:
    """P8: Swap the order of two consecutive tool-call steps."""
    traj = record["trajectory"]
    pairs = []
    for i in range(len(traj) - 3):
        if (
            traj[i]["role"] == "assistant"
            and "<tool_call>" in (traj[i].get("content") or "")
            and traj[i + 1]["role"] == "tool"
            and traj[i + 2]["role"] == "assistant"
            and "<tool_call>" in (traj[i + 2].get("content") or "")
            and traj[i + 3]["role"] == "tool"
        ):
            pairs.append(i)

    if not pairs:
        return None

    step_idx = rng.choice(pairs)
    out = copy.deepcopy(record)
    t = out["trajectory"]
    # Swap pair 1 (i, i+1) with pair 2 (i+2, i+3)
    t[step_idx], t[step_idx + 2] = t[step_idx + 2], t[step_idx]
    t[step_idx + 1], t[step_idx + 3] = t[step_idx + 3], t[step_idx + 1]

    out["is_anomalous"] = True
    out["anomaly_type"] = "skipped_required_step"
    out["bad_step"] = step_idx
    out["generation_rule"] = "P8"
    return out


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

ALL_RULES = [
    p1_replace_tool_choice,
    p2_mutate_argument_value,
    p3_remove_step_pair,
    p4_duplicate_tool_step,
    p5_append_continuation,
    p6_contradict_final_answer,
    p7_truncate_before_decision,
    p8_swap_dependent_steps,
]

MVP_RULES = ALL_RULES[:4]  # P1–P4 for the MVP


def apply_perturbation(
    record: dict,
    rule_fn: Any,
    variant_index: int,
    rng: random.Random,
) -> dict | None:
    """Apply one perturbation rule and update the record id/variant fields."""
    result = rule_fn(record, rng)
    if result is None:
        return None
    source_id = record["source_trace_id"]
    rule_name = rule_fn.__name__
    result["id"] = f"{source_id}_var_{variant_index:02d}"
    result["source_trace_id"] = source_id
    return result
