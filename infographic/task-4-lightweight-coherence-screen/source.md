Objective: Filter out obviously implausible anomalous trajectories after perturbation without adding a full perturb-and-complete system.

Implementation facts:
- Added dataset_builder/coherence.py with is_plausible_trajectory(record) -> tuple[bool, str | None].
- The screen stays intentionally small and deterministic.
- It rejects dangling assistant tool calls with no immediate tool response.
- It rejects orphan tool responses with no matching preceding assistant tool call.
- It rejects exact adjacent duplicate fragments of the same message type.
- build_trajad_dataset.py now screens each perturbed record immediately after apply_perturbation(...).
- Implausible anomalies are dropped and counted by rejection reason.
- build_trajad_dataset.py now uses unique_source_ids_in_order(records) so split assignment stays reproducible for a fixed seed.
- The coherence screen was narrowed so repeated_step anomalies from P4 remain plausible instead of being eliminated.

Verification:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_coherence.py tests/test_perturbations.py tests/test_validate_labels.py tests/test_build_trajad_dataset.py -q
- 13 passed
- python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42
- Generated 29,354 anomalous records
- Coherence screen: kept=29,354 rejected=0
- Split sizes: train=27,536  dev=3,671  test=5,505
- repeated_step train count: 5,518
- repeated_step test count: 1,104
- python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
- All records valid
- diff -u /tmp/task4_build1.log /tmp/task4_build2.log
- no diff output for two same-seed builds

Files involved:
- dataset_builder/coherence.py
- dataset_builder/build_trajad_dataset.py
- tests/test_coherence.py
- tests/test_build_trajad_dataset.py
- tests/test_perturbations.py
- tests/test_validate_labels.py
