# Dataset-builder Phase-1 readiness improvements — 2026-04-24

Summary:
- standardized the repo workflow on `uv`
- added `.python-version`, `uv.lock`, and a working editable-package setup for `uv sync`
- added `scripts/bootstrap_dataset_builder.sh`
- expanded `inspect_traces.py` with schema, tool, and eligibility reports
- added `P9 invalid_tool_json`
- added `dataset_builder/audit_dataset.py`
- documented the storage contract in `docs/dataset-builder-data-contract.md`

Verification:
- `./scripts/bootstrap_dataset_builder.sh`
- `uv run pytest tests/test_inspect_traces.py tests/test_perturbations.py tests/test_validate_labels.py tests/test_build_manifest.py tests/test_build_trajad_dataset.py tests/test_audit_dataset.py tests/test_normalize_trajectory.py -q`
- result: `32 passed`
- `uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --schema-report --tool-stats --eligibility-report`
- `uv run python dataset_builder/build_trajad_dataset.py --seed 42`
- `uv run python dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
- `uv run python dataset_builder/audit_dataset.py data/processed/all.jsonl`

Key numbers:
- raw records: 3,679
- avg raw trajectory length: 32.1
- traces with embedded `<tool_call>`: 100.0%
- traces with >=2 assistant/tool-call pairs: 99.4%
- processed all.jsonl: 71,429 records
- split counts: train 53,557 / dev 7,154 / test 10,718

Decision:
- keep `data/raw`, `data/interim`, and `data/processed` in implementation
- treat bronze/silver/gold as a doc-only mental model
