# Episode notes

Task: 2 — Add derived structural metadata during normalization

Status: Done (2026-04-23)

Objective:
- Preserve more useful signal about tool-heavy trajectories without redesigning the schema.

Why it matters:
- Phase 0 established that the corpus is tool-dense and structure-heavy. The current normalized format is appropriately simple, but it throws away cheap-to-compute metadata that would help diagnostics and filtering.

Verification recorded in plan:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_normalize_trajectory.py -v` and `python3 dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized.jsonl`

Downstream effect:
- This metadata becomes the cheap signal that later filtering, diagnostics, and evaluation slices can depend on.
- With richer metadata in place, anomaly taxonomy and perturbation analysis stop being blind to trajectory structure.
