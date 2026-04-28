import json
from pathlib import Path

from dataset_builder.trajectory_explorer_payload import export_payload_bundle


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_export_payload_bundle_writes_expected_files(tmp_path: Path) -> None:
    result = export_payload_bundle(repo_root=REPO_ROOT, output_dir=tmp_path)

    expected_names = {
        "overview": "overview_payload.json",
        "samples": "sample_trajectories.json",
        "training": "training_payload.json",
        "evaluation": "evaluation_payload.json",
        "bundle": "payload_bundle.js",
    }
    assert set(result) == set(expected_names)

    for key, filename in expected_names.items():
        assert result[key].name == filename
        assert result[key].exists()

    overview = json.loads(result["overview"].read_text())
    assert overview["project"]["name"] == "gemma-trajad-eval"
    assert overview["counts"]["raw_traces"] > 0
    assert overview["counts"]["processed_examples"] > 0
    assert overview["taxonomy"]

    samples = json.loads(result["samples"].read_text())
    assert {sample["sample_kind"] for sample in samples["samples"]} == {"normal", "anomalous"}
    anomalous = next(sample for sample in samples["samples"] if sample["sample_kind"] == "anomalous")
    assert anomalous["anomaly_type"] is not None
    assert anomalous["bad_step"] is not None
    assert anomalous["messages"]
    assert anomalous["diff_hints"]["focus_indexes"]

    training = json.loads(result["training"].read_text())
    stage_ids = {stage["stage_id"] for stage in training["training_stages"]}
    assert "prepare-binary-sft" in stage_ids
    assert "train-e2b-binary" in stage_ids
    assert training["task_modes"]

    evaluation = json.loads(result["evaluation"].read_text())
    assert evaluation["split_counts"]["train"] > 0
    assert evaluation["perturbation_rules"]
    assert evaluation["anomaly_type_distribution"]

    bundle_text = result["bundle"].read_text()
    assert "window.__TRAJAD_EXPLORER_DATA__" in bundle_text
    assert '"overview"' in bundle_text


def test_export_payload_bundle_keeps_samples_compact(tmp_path: Path) -> None:
    result = export_payload_bundle(repo_root=REPO_ROOT, output_dir=tmp_path)
    samples = json.loads(result["samples"].read_text())

    for sample in samples["samples"]:
        assert len(sample["messages"]) <= 12
        for message in sample["messages"]:
            assert set(message) >= {"role", "content_excerpt"}
            assert len(message["content_excerpt"]) <= 280


def test_export_payload_bundle_exports_anomalous_source_pair_and_real_tool_calls(tmp_path: Path) -> None:
    result = export_payload_bundle(repo_root=REPO_ROOT, output_dir=tmp_path)
    samples = json.loads(result["samples"].read_text())

    anomalous = next(sample for sample in samples["samples"] if sample["sample_kind"] == "anomalous")
    assert anomalous["source_pair"]
    assert anomalous["source_pair"]["messages"]

    non_tool_messages = [
        message
        for sample in samples["samples"]
        for message in sample["messages"]
        if not message["has_tool_call"]
    ]
    assert non_tool_messages
    assert all(message["tool_name"] is None for message in non_tool_messages)


def test_export_payload_bundle_exports_measured_taxonomy_counts(tmp_path: Path) -> None:
    result = export_payload_bundle(repo_root=REPO_ROOT, output_dir=tmp_path)

    overview = json.loads(result["overview"].read_text())
    evaluation = json.loads(result["evaluation"].read_text())

    assert overview["taxonomy_mode"] == "observed-from-processed-all-jsonl"
    assert evaluation["anomaly_type_distribution_mode"] == "observed-from-processed-all-jsonl"
    assert overview["counts"]["normal_examples"] > 0
    assert overview["counts"]["anomalous_examples"] > 0

    measured_total = sum(entry["count"] for entry in evaluation["anomaly_type_distribution"])
    assert measured_total == evaluation["anomalous_examples"]
    assert any(entry["count"] > 0 for entry in evaluation["anomaly_type_distribution"])
    assert any(entry["count"] == 0 for entry in evaluation["anomaly_type_distribution"])


def test_static_trajectory_explorer_shell_exists() -> None:
    html_path = REPO_ROOT / "apps" / "trajectory_explorer" / "index.html"
    readme_path = REPO_ROOT / "apps" / "trajectory_explorer" / "README.md"

    assert html_path.exists()
    assert readme_path.exists()

    html = html_path.read_text()
    assert "Trajectory Explorer" in html
    assert 'id="trajectory-explorer"' in html
    assert 'id="dataset-summary"' in html
    assert 'id="training-lifecycle"' in html
    assert 'id="evaluation-summary"' in html
    assert 'id="source-pair-grid"' in html
    assert 'id="taxonomy-grid"' in html
    assert 'id="taxonomy-status"' in html
    assert 'id="localization-strip"' in html
    assert 'id="localization-summary"' in html
    assert "payload_bundle.js" in html
