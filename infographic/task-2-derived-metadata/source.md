Objective: Preserve more useful signal about tool-heavy trajectories without redesigning the schema.

Implementation facts:
- Added derive_trace_metadata(trajectory) in dataset_builder/normalize_trajectory.py.
- Derived metadata includes trajectory_length, tool_call_count, tool_response_count, has_think.
- normalize_record() merges derived metadata into existing metadata.
- Core trajectory item shape remains {"role": ..., "content": ...}.

Verification:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_normalize_trajectory.py -v
- python3 dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized.jsonl
- Tests passed: 2
- Smoke test wrote 3,679 normalized records with 0 errors.
- Example metadata: {'category': 'Agent Tools', 'subcategory': 'Memory & Context', 'trajectory_length': 13, 'tool_call_count': 11, 'tool_response_count': 10, 'has_think': True}

Files involved:
- dataset_builder/normalize_trajectory.py
- tests/test_normalize_trajectory.py
