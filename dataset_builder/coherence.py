"""Tiny rule-based coherence screen for perturbed trajectories."""

from __future__ import annotations

from typing import Any


DANGLING_TOOL_CALL = "dangling_tool_call"
ORPHAN_TOOL_RESPONSE = "orphan_tool_response"
DUPLICATE_ADJACENT_FRAGMENT = "duplicate_adjacent_fragment"


def _content(step: dict[str, Any]) -> str:
    value = step.get("content")
    return value if isinstance(value, str) else ""


def _is_assistant_tool_call(step: dict[str, Any]) -> bool:
    return step.get("role") == "assistant" and "<tool_call>" in _content(step)


def _is_tool_response(step: dict[str, Any]) -> bool:
    return step.get("role") == "tool"


def is_plausible_trajectory(record: dict[str, Any]) -> tuple[bool, str | None]:
    """Reject only obviously broken structural artifacts.

    This intentionally stays small and deterministic. It screens for:
    - assistant tool calls left hanging without an immediate tool response
    - tool responses that no longer have a matching assistant tool-call step
    - exact adjacent duplicate fragments of the same message type
    """

    trajectory = record.get("trajectory")
    if not isinstance(trajectory, list) or not trajectory:
        return False, "invalid_trajectory"

    for idx in range(len(trajectory) - 1):
        current = trajectory[idx]
        following = trajectory[idx + 1]
        if _is_assistant_tool_call(current) and current == following:
            return False, DUPLICATE_ADJACENT_FRAGMENT
        if _is_tool_response(current) and current == following:
            return False, DUPLICATE_ADJACENT_FRAGMENT

    for idx, step in enumerate(trajectory):
        if _is_assistant_tool_call(step):
            if idx + 1 >= len(trajectory) or not _is_tool_response(trajectory[idx + 1]):
                return False, DANGLING_TOOL_CALL

        if _is_tool_response(step):
            if idx == 0 or not _is_assistant_tool_call(trajectory[idx - 1]):
                return False, ORPHAN_TOOL_RESPONSE

    return True, None
