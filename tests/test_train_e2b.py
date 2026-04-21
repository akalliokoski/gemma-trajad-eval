from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAIN_E2B_PATH = ROOT / "training" / "train_e2b.py"


def load_train_e2b_module():
    spec = importlib.util.spec_from_file_location("train_e2b_under_test", TRAIN_E2B_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_train_e2b_import_does_not_require_mlx_tune():
    module = load_train_e2b_module()
    assert module.MODEL_ID == "google/gemma-4-E2B-it"


def test_load_sft_data_can_limit_examples(tmp_path):
    module = load_train_e2b_module()
    module.PROCESSED_DIR = tmp_path

    path = tmp_path / "train_sft_binary.jsonl"
    path.write_text(
        "\n".join(
            [
                '{"id": "a", "messages": [{"role": "system", "content": "s"}, {"role": "user", "content": "u1"}, {"role": "assistant", "content": "{\\"anomalous\\": false}"}]}',
                '{"id": "b", "messages": [{"role": "system", "content": "s"}, {"role": "user", "content": "u2"}, {"role": "assistant", "content": "{\\"anomalous\\": true}"}]}',
                '{"id": "c", "messages": [{"role": "system", "content": "s"}, {"role": "user", "content": "u3"}, {"role": "assistant", "content": "{\\"anomalous\\": false}"}]}',
            ]
        )
        + "\n"
    )

    rows = module.load_sft_data("train", "binary", max_examples=2)

    assert [row["id"] for row in rows] == ["a", "b"]
