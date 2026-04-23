# Episode notes

Task: 1 — Repair raw-data inspection for ShareGPT-style Hermes traces

Status: Done (2026-04-23)

Objective:
- Make the inspection path trustworthy on the real raw dataset before deeper changes.

Why it matters:
- Phase 0 showed that raw Hermes records use `from/value`, but `inspect_traces.py` currently assumes `role/content` and fails on the real file. A broken inspection script undermines every later decision.

Verification recorded in plan:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_inspect_traces.py -v` and `python3 dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl`

Downstream effect:
- This repair makes every later inspection, debugging, and schema decision start from the real Hermes raw format instead of a broken mental model.
- Once inspection is trustworthy, it becomes safe to derive metadata and compare raw versus normalized structure without guessing.
