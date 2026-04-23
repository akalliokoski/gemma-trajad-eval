from collections import Counter
from pathlib import Path

from dataset_builder.build_trajad_dataset import (
    build_manifest,
    format_manifest_summary,
    write_manifest,
)


def test_build_manifest_captures_counts_and_diagnostics(tmp_path: Path) -> None:
    manifest = build_manifest(
        seed=42,
        rule_names=["p1_replace_tool_choice", "p4_duplicate_tool_step"],
        source_input_paths=["data/interim/sample.jsonl"],
        split_records={
            "train": [
                {"anomaly_type": None, "anomaly_class": None},
                {"anomaly_type": "wrong_tool_choice", "anomaly_class": "process_inefficiency"},
            ],
            "dev": [
                {"anomaly_type": "repeated_step", "anomaly_class": "process_inefficiency"},
            ],
            "test": [
                {"anomaly_type": "bad_tool_arguments", "anomaly_class": "task_failure"},
            ],
        },
        perturbation_failures=Counter({"p1_replace_tool_choice": 2}),
        coherence_rejections=Counter({"p4_duplicate_tool_step": 3}),
        coherence_rejection_reasons=Counter({"duplicate_adjacent_fragment": 3}),
    )

    assert manifest["seed"] == 42
    assert manifest["rules_used"] == ["p1_replace_tool_choice", "p4_duplicate_tool_step"]
    assert manifest["source_input_paths"] == ["data/interim/sample.jsonl"]
    assert manifest["totals"]["normal"] == 1
    assert manifest["totals"]["anomalous"] == 3
    assert manifest["totals"]["all_records"] == 4
    assert manifest["split_counts"] == {"train": 2, "dev": 1, "test": 1}
    assert manifest["anomaly_type_counts"] == {
        "bad_tool_arguments": 1,
        "repeated_step": 1,
        "wrong_tool_choice": 1,
    }
    assert manifest["anomaly_class_counts"] == {
        "process_inefficiency": 2,
        "task_failure": 1,
    }
    assert manifest["perturbation_failures_by_rule"] == {"p1_replace_tool_choice": 2}
    assert manifest["coherence_rejections_by_rule"] == {"p4_duplicate_tool_step": 3}
    assert manifest["coherence_rejection_reasons"] == {"duplicate_adjacent_fragment": 3}


def test_write_manifest_and_summary(tmp_path: Path) -> None:
    manifest = build_manifest(
        seed=7,
        rule_names=["p1_replace_tool_choice"],
        source_input_paths=["data/interim/sample.jsonl"],
        split_records={"train": [], "dev": [], "test": []},
        perturbation_failures=Counter(),
        coherence_rejections=Counter(),
        coherence_rejection_reasons=Counter(),
    )
    out_path = tmp_path / "build_manifest.json"

    write_manifest(manifest, out_path)
    summary = format_manifest_summary(manifest)

    assert out_path.exists()
    assert 'seed: 7' in summary
    assert 'rules used: 1' in summary
    assert 'split counts: train=0 dev=0 test=0' in summary
