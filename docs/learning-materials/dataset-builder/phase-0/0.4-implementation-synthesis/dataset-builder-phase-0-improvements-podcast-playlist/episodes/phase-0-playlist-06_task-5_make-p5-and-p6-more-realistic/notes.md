# Episode notes

Task: 5 — Make P5 and P6 more realistic

Status: Done (2026-04-23)

Objective:
- Improve the most obviously synthetic perturbations without adding model-generated continuation.

Why it matters:
- Phase 0 made it clear that unrealistic anomalies hurt dataset quality. Right now: - `P5` creates a dangling continuation pattern - `P6` uses an explicit contradiction marker that is too artificial

Verification recorded in plan:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_perturbations.py -v`, `python3 dataset_builder/build_trajad_dataset.py --seed 42`, and `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`

Downstream effect:
- Improving P5 and P6 raises realism where the synthetic feel was most visible, so later models learn from more plausible failures.
- Better realism raises the value of deeper validation because the pipeline is now checking stronger examples rather than obviously fake ones.
