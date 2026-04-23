# Task 7 build manifest and diagnostics implementation note

Date: 2026-04-23
Source: verified local implementation in the active Hermes session

Task 7 from `docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md` made dataset builds reproducible and inspectable by adding a saved manifest and compact diagnostics output.

Key implementation facts:
- Added `build_manifest(...)`, `write_manifest(...)`, and `format_manifest_summary(...)` to `dataset_builder/build_trajad_dataset.py`.
- The builder now tracks `source_input_paths`, `rules_used`, split counts, anomaly-type counts, anomaly-class counts, perturbation failures by rule, and coherence rejections.
- The builder now writes `data/processed/build_manifest.json` after the dataset JSONL files.
- The builder now prints a compact `Build manifest summary` block after writing the manifest.
- Added `tests/test_build_manifest.py` with focused tests for manifest contents and summary formatting.

Verification facts:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_build_manifest.py -v`
- `2 passed`
- `python3 dataset_builder/build_trajad_dataset.py --seed 42`
- `Generated 56,724 anomalous records`
- `Coherence screen: kept=56,724 rejected=0`
- `Split sizes: train=47,973  dev=6,413  test=9,696`
- `normal=7,358 anomalous=56,724 all=64,082`
- `python3 -m json.tool data/processed/build_manifest.json > /tmp/build_manifest.pretty.json`
- `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
- `Validated 64,082 records from data/processed/all.jsonl`
- `All records valid.`
