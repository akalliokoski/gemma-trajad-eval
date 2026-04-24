# Dataset-builder Phase-1 Readiness Improvements

Scope completed:
- standardize local workflow on `uv`
- add `scripts/bootstrap_dataset_builder.sh`
- expand `inspect_traces.py` with `--schema-report`, `--tool-stats`, and `--eligibility-report`
- add `invalid_tool_json` as `P9`
- add `dataset_builder/audit_dataset.py`
- document `data/raw -> data/interim -> data/processed`

Key implementation points:
- added `.python-version` with `3.12`
- added `uv.lock`
- fixed packaging for `uv sync` by switching to `setuptools.build_meta`
- limited setuptools discovery to `dataset_builder*`
- added `dataset_builder/__init__.py`
- added `docs/dataset-builder-data-contract.md`
- kept bronze/silver/gold as a doc-only mental model

Verification:
- `uv sync --extra dev`
- `./scripts/bootstrap_dataset_builder.sh`
- `uv run pytest tests/test_inspect_traces.py tests/test_perturbations.py tests/test_validate_labels.py tests/test_build_manifest.py tests/test_build_trajad_dataset.py tests/test_audit_dataset.py tests/test_normalize_trajectory.py -q`
- result: `32 passed`
- `uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --schema-report --tool-stats --eligibility-report`
- `uv run python dataset_builder/build_trajad_dataset.py --seed 42`
- `uv run python dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
- `uv run python dataset_builder/audit_dataset.py data/processed/all.jsonl`

Real dataset observations:
- records: 3,679 raw traces
- avg raw trajectory length: 32.1
- traces with embedded `<tool_call>`: 100.0%
- traces with >=2 assistant/tool-call pairs: 99.4%
- processed all.jsonl size after rebuild: 71,429 records
- split counts: train 53,557 / dev 7,154 / test 10,718
- anomaly classes: task_failure 42,991 / process_inefficiency 14,716 / unwarranted_continuation 6,364

Design decision:
- keep `raw`, `interim`, and `processed` in implementation
- optional conceptual mapping only: raw ≈ bronze, interim ≈ silver, processed ≈ gold
