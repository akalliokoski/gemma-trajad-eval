Objective: Make dataset builds reproducible and inspectable by saving a build manifest and printing a compact diagnostics summary.

Implementation facts:
- Updated dataset_builder/build_trajad_dataset.py.
- Added build_manifest(...), write_manifest(...), and format_manifest_summary(...).
- The builder now records source_input_paths, rules_used, split counts, anomaly-type counts, anomaly-class counts, perturbation failures by rule, and coherence rejections.
- The builder now writes data/processed/build_manifest.json after the JSONL outputs.
- The builder now prints a compact Build manifest summary to stdout for interactive inspection.
- Added tests/test_build_manifest.py with focused checks for manifest contents and summary formatting.

Verification:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_build_manifest.py -v
- 2 passed
- python3 dataset_builder/build_trajad_dataset.py --seed 42
- Generated 56,724 anomalous records
- Coherence screen: kept=56,724 rejected=0
- Split sizes: train=47,973  dev=6,413  test=9,696
- Wrote build manifest -> /home/hermes/gemma-trajad-eval/data/processed/build_manifest.json
- Build manifest summary: seed 42, rules used 8, totals normal=7,358 anomalous=56,724 all=64,082
- python3 -m json.tool data/processed/build_manifest.json > /tmp/build_manifest.pretty.json
- python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
- Validated 64,082 records from data/processed/all.jsonl
- All records valid.

Files involved:
- dataset_builder/build_trajad_dataset.py
- tests/test_build_manifest.py
- data/processed/build_manifest.json
