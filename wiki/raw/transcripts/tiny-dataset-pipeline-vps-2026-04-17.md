# Tiny dataset pipeline run on VPS

Date: 2026-04-17
Source type: internal project execution notes

Summary:
- Created a repo-local virtualenv with `uv` because system `pip` was unavailable.
- Downloaded the filtered Hermes traces dataset to `data/raw/hermes_filtered.jsonl`.
- Normalized the raw ShareGPT-style traces to `data/interim/hermes_filtered.normalized.jsonl`.
- Built an MVP processed dataset with train/dev/test/all splits under `data/processed/`.
- Found and fixed a regex replacement bug in `dataset_builder/perturbations.py`.
- Found and fixed a validator mismatch for `skipped_required_step` semantics in `dataset_builder/validate_labels.py`.
- Added regression tests covering both fixes.
