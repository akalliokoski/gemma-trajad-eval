# Episode notes

Task: 4 — Add a lightweight coherence screen after perturbation

Status: Done (2026-04-23)

Objective:
- Filter out obviously implausible anomalous records without adding a full perturb-and-complete system.

Why it matters:
- This is the highest-value quality improvement from Phase 0. The current system directly perturbs one step and leaves the rest unchanged. That simplicity is good, but it can create broken-looking trajectories. A small coherence filter gives most of the benefit without requiring LLM-generated continuation.

Verification recorded in plan:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_coherence.py tests/test_perturbations.py tests/test_validate_labels.py tests/test_build_trajad_dataset.py -q`, `python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42`, `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`, and `diff -u /tmp/task4_build1.log /tmp/task4_build2.log`

Downstream effect:
- Coherence screening is the gate that prevents obviously broken anomalies from poisoning future training and evaluation.
- After that gate exists, realism work on individual perturbation rules compounds instead of leaking garbage through the pipeline.
