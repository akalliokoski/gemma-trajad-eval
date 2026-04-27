"""Perturbation diagnostics for normalized Hermes trajectories.

Usage:
    python dataset_builder/perturbation_diagnostics.py
    python dataset_builder/perturbation_diagnostics.py --input data/interim/hermes_normalized_phase2.jsonl
    python dataset_builder/perturbation_diagnostics.py --output data/processed/perturbation_diagnostics.json
"""

import argparse
import json
import random
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

try:
    from dataset_builder.build_trajad_dataset import load_jsonl
    from dataset_builder.perturbations import (
        ALL_RULES,
        find_assistant_steps,
        parse_tool_call,
        p1_replace_tool_choice,
        p2_mutate_argument_value,
        p3_remove_step_pair,
        p4_duplicate_tool_step,
        p5_append_continuation,
        p6_contradict_final_answer,
        p7_truncate_before_decision,
        p8_swap_dependent_steps,
        p9_invalid_tool_json,
    )
except ModuleNotFoundError:
    from build_trajad_dataset import load_jsonl
    from perturbations import (
        ALL_RULES,
        find_assistant_steps,
        parse_tool_call,
        p1_replace_tool_choice,
        p2_mutate_argument_value,
        p3_remove_step_pair,
        p4_duplicate_tool_step,
        p5_append_continuation,
        p6_contradict_final_answer,
        p7_truncate_before_decision,
        p8_swap_dependent_steps,
        p9_invalid_tool_json,
    )

ROOT = Path(__file__).parent.parent
DEFAULT_INPUT = ROOT / "data" / "interim" / "hermes_normalized_phase2.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "perturbation_diagnostics.json"

RuleFn = Callable[[dict, random.Random], dict | None]


def _assistant_tool_pair_indices(trajectory: list[dict]) -> list[int]:
    pairs = []
    for i in range(len(trajectory) - 1):
        if (
            trajectory[i].get("role") == "assistant"
            and "<tool_call>" in (trajectory[i].get("content") or "")
            and trajectory[i + 1].get("role") == "tool"
        ):
            pairs.append(i)
    return pairs


def _has_parsed_tool_call(record: dict) -> bool:
    for step_idx in find_assistant_steps(record["trajectory"]):
        if parse_tool_call(record["trajectory"][step_idx].get("content") or "") is not None:
            return True
    return False


def _has_tool_arguments(record: dict) -> bool:
    for step_idx in find_assistant_steps(record["trajectory"]):
        call = parse_tool_call(record["trajectory"][step_idx].get("content") or "")
        if call is None:
            continue
        args = call.get("arguments", call.get("parameters", {}))
        if isinstance(args, dict) and args:
            return True
    return False


def _has_final_assistant_after_tool(record: dict) -> bool:
    traj = record["trajectory"]
    last_tool_idx = None
    for i in range(len(traj) - 1, -1, -1):
        if traj[i].get("role") == "tool":
            last_tool_idx = i
            break
    if last_tool_idx is None:
        return False
    return any(step.get("role") == "assistant" for step in traj[last_tool_idx + 1 :])


def is_record_eligible_for_rule(record: dict, rule_fn: RuleFn) -> bool:
    traj = record["trajectory"]
    pairs = _assistant_tool_pair_indices(traj)

    if rule_fn is p1_replace_tool_choice:
        return _has_parsed_tool_call(record)
    if rule_fn is p2_mutate_argument_value:
        return _has_tool_arguments(record)
    if rule_fn in {p3_remove_step_pair, p4_duplicate_tool_step, p9_invalid_tool_json}:
        return bool(pairs)
    if rule_fn is p5_append_continuation:
        return bool(traj) and traj[-1].get("role") == "assistant"
    if rule_fn is p6_contradict_final_answer:
        return _has_final_assistant_after_tool(record)
    if rule_fn is p7_truncate_before_decision:
        return len(pairs) >= 2
    if rule_fn is p8_swap_dependent_steps:
        return len(pairs) >= 2
    return False


def _failure_example(record: dict) -> dict[str, Any]:
    tool_name = None
    for step_idx in find_assistant_steps(record["trajectory"]):
        call = parse_tool_call(record["trajectory"][step_idx].get("content") or "")
        if call is not None:
            tool_name = call.get("name")
            break
    return {
        "source_trace_id": record.get("source_trace_id"),
        "id": record.get("id"),
        "tool_name": tool_name,
    }


def compute_rule_diagnostics(records: list[dict], rules: list[RuleFn], seed: int = 0) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "seed": seed,
        "total_records": len(records),
        "rules": [],
    }

    for rule_idx, rule_fn in enumerate(rules):
        eligible = 0
        succeeded = 0
        failed = 0
        ineligible = 0
        failure_examples: list[dict[str, Any]] = []

        for record_idx, record in enumerate(records):
            if not is_record_eligible_for_rule(record, rule_fn):
                ineligible += 1
                continue

            eligible += 1
            rng = random.Random(seed + rule_idx * 100_000 + record_idx)
            result = rule_fn(record, rng)
            if result is None:
                failed += 1
                if len(failure_examples) < 5:
                    failure_examples.append(_failure_example(record))
            else:
                succeeded += 1

        success_rate = (succeeded / eligible) if eligible else 0.0
        diagnostics["rules"].append(
            {
                "rule_name": rule_fn.__name__,
                "eligible": eligible,
                "succeeded": succeeded,
                "failed": failed,
                "ineligible": ineligible,
                "success_rate": round(success_rate, 4),
                "failure_examples": failure_examples,
            }
        )

    return diagnostics


def format_diagnostics_table(diagnostics: dict[str, Any]) -> str:
    lines = [
        "Rule | Eligible | Succeeded | Failed | Success Rate",
        "--- | ---: | ---: | ---: | ---:",
    ]
    for row in diagnostics["rules"]:
        lines.append(
            f"{row['rule_name']} | {row['eligible']} | {row['succeeded']} | {row['failed']} | {row['success_rate'] * 100:.1f}%"
        )
    return "\n".join(lines)


def write_diagnostics(diagnostics: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(diagnostics, f, indent=2, sort_keys=True)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Normalized JSONL input file")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output JSON path")
    parser.add_argument("--seed", type=int, default=0, help="Deterministic seed for per-record rule application")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    diagnostics = compute_rule_diagnostics(records, ALL_RULES, seed=args.seed)
    write_diagnostics(diagnostics, args.output)

    print(f"Loaded {len(records):,} normalized records from {args.input}")
    print(format_diagnostics_table(diagnostics))
    print(f"Wrote perturbation diagnostics -> {args.output}")


if __name__ == "__main__":
    main()
