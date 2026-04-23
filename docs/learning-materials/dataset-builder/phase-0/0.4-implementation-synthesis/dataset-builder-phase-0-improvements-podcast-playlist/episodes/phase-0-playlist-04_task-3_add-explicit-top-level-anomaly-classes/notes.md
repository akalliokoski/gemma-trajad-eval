# Episode notes

Task: 3 — Add explicit top-level anomaly classes

Status: Done (2026-04-23)

Objective:
- Align the dataset output with the Phase-0 anomaly taxonomy while keeping the current rule-level labels.

Why it matters:
- Phase 0 framed the problem in top-level classes: - task failure - process inefficiency - unwarranted continuation

Verification recorded in plan:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py tests/test_perturbations.py -q`, `python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42`, and `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`

Downstream effect:
- Explicit anomaly classes make later reporting, stratified evaluation, and curriculum choices far easier.
- Once class labels exist, coherence screening and rule tuning can be analyzed at both rule-level and class-level granularity.
