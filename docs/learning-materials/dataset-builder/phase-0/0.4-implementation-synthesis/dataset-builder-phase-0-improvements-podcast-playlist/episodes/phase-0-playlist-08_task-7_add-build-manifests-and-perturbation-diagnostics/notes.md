# Episode notes

Task: 7 — Add build manifests and perturbation diagnostics

Status: Done (2026-04-23)

Objective:
- Make every dataset build reproducible and inspectable.

Why it matters:
- A home lab benefits more from repeatability than from platform complexity. Right now the builder prints useful counts but does not save them.

Verification recorded in plan:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_build_manifest.py -v`, `python3 dataset_builder/build_trajad_dataset.py --seed 42`, `python3 -m json.tool data/processed/build_manifest.json > /tmp/build_manifest.pretty.json`, and `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`

Downstream effect:
- Build manifests and perturbation diagnostics turn one-off dataset runs into inspectable, comparable artifacts.
- That reproducibility is what makes the next phase—training, evaluation, ablations, and maybe GPU-backed continuation—feel scientific instead of anecdotal.
