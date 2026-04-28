from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PROCESSED = REPO_ROOT / "data" / "processed"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "apps" / "trajectory_explorer" / "assets"

_TOOL_CALL_NAME_RE = re.compile(r'<tool_call>\s*(?:\{)?[^\n]*?"name"\s*:\s*"([^"]+)"', re.DOTALL)


PLANNED_TAXONOMY = [
    {"id": "wrong_tool_choice", "label": "Wrong Tool Choice", "anomaly_class": "process_inefficiency"},
    {"id": "bad_tool_arguments", "label": "Bad Tool Arguments", "anomaly_class": "task_failure"},
    {"id": "skipped_required_step", "label": "Skipped Required Step", "anomaly_class": "task_failure"},
    {"id": "repeated_step", "label": "Repeated Step", "anomaly_class": "process_inefficiency"},
    {"id": "premature_final_answer", "label": "Premature Final Answer", "anomaly_class": "task_failure"},
    {"id": "continued_after_sufficient_evidence", "label": "Continued After Sufficient Evidence", "anomaly_class": "unwarranted_continuation"},
    {"id": "contradicted_tool_result", "label": "Contradicted Tool Result", "anomaly_class": "task_failure"},
    {"id": "hallucinated_tool", "label": "Hallucinated Tool", "anomaly_class": "task_failure"},
    {"id": "invalid_tool_json", "label": "Invalid Tool JSON", "anomaly_class": "task_failure"},
    {"id": "unnecessary_replanning", "label": "Unnecessary Replanning", "anomaly_class": "process_inefficiency"},
]


def summarize_processed_distribution(processed_path: Path) -> dict[str, Any]:
    anomaly_type_counts: Counter[str] = Counter()
    anomaly_class_counts: Counter[str] = Counter()
    normal_examples = 0
    anomalous_examples = 0

    for record in iter_jsonl(processed_path):
        if record.get("is_anomalous"):
            anomalous_examples += 1
            anomaly_type_counts[record.get("anomaly_type") or "unknown"] += 1
            anomaly_class_counts[record.get("anomaly_class") or "unknown"] += 1
        else:
            normal_examples += 1

    taxonomy = []
    for entry in PLANNED_TAXONOMY:
        taxonomy.append(
            {
                **entry,
                "count": anomaly_type_counts.get(entry["id"], 0),
            }
        )

    return {
        "normal_examples": normal_examples,
        "anomalous_examples": anomalous_examples,
        "taxonomy": taxonomy,
        "anomaly_class_distribution": [
            {"id": key, "count": value}
            for key, value in sorted(anomaly_class_counts.items())
        ],
    }


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open() as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def count_jsonl_rows(path: Path) -> int:
    result = subprocess.run(["wc", "-l", str(path)], check=True, capture_output=True, text=True)
    return int(result.stdout.strip().split()[0])

def summarize_text(text: str, limit: int = 280) -> str:
    compact = " ".join((text or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def extract_tool_name(content: str) -> str | None:
    match = _TOOL_CALL_NAME_RE.search(content or "")
    return match.group(1) if match else None


def summarize_message(message: dict[str, Any], absolute_index: int) -> dict[str, Any]:
    content = message.get("content") or ""
    return {
        "absolute_index": absolute_index,
        "role": message.get("role"),
        "tool_name": extract_tool_name(content),
        "has_tool_call": "<tool_call>" in content,
        "has_tool_response": "<tool_response>" in content,
        "content_excerpt": summarize_text(content),
    }


def choose_window(trajectory: list[dict[str, Any]], focus_index: int | None, window_size: int = 12) -> tuple[int, int]:
    if len(trajectory) <= window_size:
        return 0, len(trajectory)

    if focus_index is None:
        return 0, window_size

    half = window_size // 2
    start = max(0, focus_index - half)
    end = start + window_size
    if end > len(trajectory):
        end = len(trajectory)
        start = end - window_size
    return start, end


def diff_indexes(source_messages: list[dict[str, Any]], variant_messages: list[dict[str, Any]]) -> list[int]:
    changed: list[int] = []
    max_len = max(len(source_messages), len(variant_messages))
    for index in range(max_len):
        left = source_messages[index] if index < len(source_messages) else None
        right = variant_messages[index] if index < len(variant_messages) else None
        if left != right:
            changed.append(index)
    return changed


def build_sample(
    record: dict[str, Any],
    sample_kind: str,
    *,
    source_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    focus_index = record.get("bad_step") if sample_kind == "anomalous" else None
    start, end = choose_window(record["trajectory"], focus_index)
    messages = [
        summarize_message(message, absolute_index=index)
        for index, message in enumerate(record["trajectory"][start:end], start=start)
    ]

    changed_indexes = diff_indexes(source_record["trajectory"], record["trajectory"]) if source_record else []
    focus_indexes = sorted(
        {
            *(index for index in changed_indexes if start <= index < end),
            *([focus_index] if focus_index is not None and start <= focus_index < end else []),
        }
    )
    if not focus_indexes and messages:
        focus_indexes = [messages[min(len(messages) - 1, max(0, len(messages) // 2))]["absolute_index"]]

    payload = {
        "id": record["id"],
        "sample_kind": sample_kind,
        "source_trace_id": record.get("source_trace_id"),
        "split": record.get("split"),
        "is_anomalous": record.get("is_anomalous"),
        "anomaly_type": record.get("anomaly_type"),
        "anomaly_class": record.get("anomaly_class"),
        "bad_step": record.get("bad_step"),
        "generation_rule": record.get("generation_rule"),
        "message_count": len(record["trajectory"]),
        "window": {"start": start, "end": end},
        "messages": messages,
        "diff_hints": {
            "focus_indexes": focus_indexes,
            "changed_message_indexes": changed_indexes,
        },
    }
    if source_record:
        payload["source_pair"] = {
            "id": source_record["id"],
            "message_count": len(source_record["trajectory"]),
            "messages": [
                summarize_message(message, absolute_index=index)
                for index, message in enumerate(source_record["trajectory"][start:end], start=start)
            ],
        }
    return payload


def select_samples_from_processed(processed_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
    normal_by_source: dict[str, dict[str, Any]] = {}
    first_normal: dict[str, Any] | None = None
    first_anomalous: dict[str, Any] | None = None
    source_pair: dict[str, Any] | None = None
    needed_source_trace_id: str | None = None

    for record in iter_jsonl(processed_path):
        source_trace_id = record.get("source_trace_id")
        if not record.get("is_anomalous"):
            normal_by_source.setdefault(source_trace_id, record)
            if first_normal is None:
                first_normal = record
            if needed_source_trace_id is not None and source_trace_id == needed_source_trace_id and source_pair is None:
                source_pair = record

        if (
            first_anomalous is None
            and record.get("is_anomalous")
            and record.get("bad_step") is not None
            and record.get("anomaly_type")
        ):
            first_anomalous = record
            needed_source_trace_id = source_trace_id
            source_pair = normal_by_source.get(source_trace_id)

        if first_normal is not None and first_anomalous is not None and source_pair is not None:
            break

    if first_normal is None or first_anomalous is None:
        raise ValueError("Could not find both normal and anomalous samples in processed data.")

    return first_normal, first_anomalous, source_pair


def build_overview_payload(
    split_counts: dict[str, int],
    diagnostics: dict[str, Any],
    processed_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "generated_at": diagnostics.get("timestamp"),
        "project": {
            "name": "gemma-trajad-eval",
            "tagline": "Hermes-first trajectory anomaly engineering lab",
            "reference_visualization": {
                "github": "https://github.com/ArkAung/interactive-turboquant",
                "live_demo": "https://arkaung.github.io/interactive-turboquant/",
            },
        },
        "counts": {
            "raw_traces": diagnostics.get("total_records"),
            "processed_examples": sum(split_counts.values()),
            "normal_examples": processed_summary["normal_examples"],
            "anomalous_examples": processed_summary["anomalous_examples"],
            **split_counts,
        },
        "anomaly_class_distribution": processed_summary["anomaly_class_distribution"],
        "taxonomy": processed_summary["taxonomy"],
        "taxonomy_mode": "observed-from-processed-all-jsonl",
        "execution_topology": [
            {
                "node": "vps",
                "role": "control-plane",
                "summary": "Hermes planning, docs, orchestration, and lightweight automation",
            },
            {
                "node": "apple-silicon-mac",
                "role": "bounded-compute-worker",
                "summary": "Preferred small/medium fine-tuning and local validation tier",
            },
            {
                "node": "modal",
                "role": "future-heavy-gpu-tier",
                "summary": "Deferred destination for truly heavy training or inference jobs",
            },
        ],
    }


def build_samples_payload(normal: dict[str, Any], anomalous: dict[str, Any], source_pair: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "selected_ids": {"normal": normal["id"], "anomalous": anomalous["id"]},
        "samples": [
            build_sample(normal, "normal"),
            build_sample(anomalous, "anomalous", source_record=source_pair),
        ],
    }


def build_training_payload(repo_root: Path) -> dict[str, Any]:
    processed_dir = repo_root / "data" / "processed"
    task_modes = []
    for task in ("binary", "localize", "joint"):
        train_path = processed_dir / f"train_sft_{task}.jsonl"
        dev_path = processed_dir / f"dev_sft_{task}.jsonl"
        test_path = processed_dir / f"test_sft_{task}.jsonl"
        task_modes.append(
            {
                "task": task,
                "train_rows": count_jsonl_rows(train_path) if train_path.exists() else 0,
                "dev_rows": count_jsonl_rows(dev_path) if dev_path.exists() else 0,
                "test_rows": count_jsonl_rows(test_path) if test_path.exists() else 0,
                "prompt_file": f"prompts/anomaly_{task}.txt",
            }
        )

    return {
        "training_stages": [
            {
                "stage_id": "prepare-binary-sft",
                "label": "Prepare binary SFT data",
                "script": "training/prepare_sft_data.py --task binary",
                "input_artifact": "data/processed/train.jsonl",
                "output_artifact": "data/processed/train_sft_binary.jsonl",
            },
            {
                "stage_id": "train-e2b-binary",
                "label": "Train Gemma 4 E2B binary adapter",
                "script": "training/train_e2b.py --task binary",
                "input_artifact": "data/processed/train_sft_binary.jsonl",
                "output_artifact": "outputs/adapters/e2b-sft-binary-run1/final",
            },
            {
                "stage_id": "evaluate-run",
                "label": "Evaluate predictions against held-out data",
                "script": "training/evaluate.py --predictions <file> --ground-truth data/processed/test.jsonl",
                "input_artifact": "outputs/reports/predictions.jsonl",
                "output_artifact": "outputs/reports/eval_results.json",
            },
        ],
        "task_modes": task_modes,
        "run_notes": [
            "E2B is the primary local-first fine-tuning target.",
            "E4B remains an optional comparison path for later runs.",
            "RL/GRPO belongs to a later phase after SFT and evaluation are stable.",
        ],
    }


def build_evaluation_payload(
    split_counts: dict[str, int],
    diagnostics: dict[str, Any],
    processed_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "split_counts": split_counts,
        "normal_examples": processed_summary["normal_examples"],
        "anomalous_examples": processed_summary["anomalous_examples"],
        "anomaly_type_distribution": processed_summary["taxonomy"],
        "anomaly_type_distribution_mode": "observed-from-processed-all-jsonl",
        "perturbation_rules": diagnostics.get("rules", []),
        "reported_runs": [],
        "notes": [
            "Anomaly-type counts are measured from data/processed/all.jsonl and cover the full currently exported taxonomy.",
            "No evaluation report JSON artifacts are committed yet, so this panel emphasizes measured dataset distributions and rule coverage rather than model metrics.",
        ],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_bundle(path: Path, payloads: dict[str, dict[str, Any]]) -> None:
    bundle = "window.__TRAJAD_EXPLORER_DATA__ = " + json.dumps(payloads, indent=2) + ";\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(bundle)


def export_payload_bundle(repo_root: Path = REPO_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Path]:
    processed_dir = repo_root / "data" / "processed"
    diagnostics = read_json(processed_dir / "perturbation_diagnostics.json")
    split_counts = {
        split: count_jsonl_rows(processed_dir / f"{split}.jsonl")
        for split in ("train", "dev", "test")
    }
    processed_summary = summarize_processed_distribution(processed_dir / "all.jsonl")
    normal, anomalous, source_pair = select_samples_from_processed(processed_dir / "all.jsonl")

    overview = build_overview_payload(split_counts, diagnostics, processed_summary)
    samples = build_samples_payload(normal, anomalous, source_pair)
    training = build_training_payload(repo_root)
    evaluation = build_evaluation_payload(split_counts, diagnostics, processed_summary)

    overview_path = output_dir / "overview_payload.json"
    samples_path = output_dir / "sample_trajectories.json"
    training_path = output_dir / "training_payload.json"
    evaluation_path = output_dir / "evaluation_payload.json"
    bundle_path = output_dir / "payload_bundle.js"

    write_json(overview_path, overview)
    write_json(samples_path, samples)
    write_json(training_path, training)
    write_json(evaluation_path, evaluation)
    write_bundle(
        bundle_path,
        {
            "overview": overview,
            "samples": samples,
            "training": training,
            "evaluation": evaluation,
        },
    )

    return {
        "overview": overview_path,
        "samples": samples_path,
        "training": training_path,
        "evaluation": evaluation_path,
        "bundle": bundle_path,
    }
