# Episode notes

Task: 6 — Deepen validation for first-error localization

Status: Done (2026-04-23)

Objective:
- Make label validation care more about the intended first-bad-step semantics, not just type/range checks.

Why it matters:
- Phase 0 emphasized first-error localization as a core supervision target. Current validation mostly checks that `bad_step` exists and is in range. That is necessary, but not enough.

Verification recorded in plan:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py -v` and `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`

Downstream effect:
- Rule-aware localization validation makes bad_step supervision closer to the first-error signal that later evaluation actually depends on.
- Once labels are semantically sharper, saved build manifests become much more informative for comparing dataset versions.
