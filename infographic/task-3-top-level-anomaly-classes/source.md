Objective: Align the dataset output with the Phase-0 anomaly taxonomy while keeping the current rule-level labels.

Implementation facts:
- Added top-level anomaly_class labels.
- Anomalous records now carry both anomaly_type and anomaly_class.
- Normal records keep anomaly_class=None.
- validate_labels.py enforces anomaly_class presence and validity for anomalous records and null for normal records.
- build_trajad_dataset.py ensures rebuilt normal records keep anomaly_class=None.
- The taxonomy was aligned with repo docs so wrong_tool_choice maps to process_inefficiency.
- skipped_required_step remains task_failure with inline rationale.

Verification:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py tests/test_perturbations.py -q
- 6 passed
- python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42
- Wrote 36,712 records total
- python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
- All records valid

Files involved:
- dataset_builder/perturbations.py
- dataset_builder/validate_labels.py
- dataset_builder/build_trajad_dataset.py
- tests/test_validate_labels.py
- tests/test_perturbations.py
