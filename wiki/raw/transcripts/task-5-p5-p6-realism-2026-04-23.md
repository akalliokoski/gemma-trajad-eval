# Task 5 P5/P6 realism implementation note

Date: 2026-04-23
Source: verified local implementation in the active Hermes session

Task 5 from `docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md` focused on making perturbation rules P5 and P6 less synthetic without adding model-generated continuation or a larger perturb-and-complete system.

Key implementation facts:
- `P5` no longer appends a dangling assistant tool call.
- `P5` now appends a structurally complete but unnecessary continuation: assistant tool call, tool response, assistant wrap-up.
- `P5` marks `bad_step` at the first unnecessary extra step.
- `P6` no longer uses a literal `[CONTRADICTION]` marker.
- `P6` now produces a subtle but wrong natural-language final answer that contradicts whether the last tool response contained a concrete result.
- `dataset_builder/perturbations.py` gained helper functions `extract_tool_response_text(...)` and `tool_response_looks_empty(...)` to support the P6 logic.
- `tests/test_perturbations.py` now contains focused tests for the new P5 and P6 expectations.

Verification facts:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_perturbations.py -v`
- `4 passed`
- `python3 dataset_builder/build_trajad_dataset.py --seed 42`
- `Generated 56,724 anomalous records`
- `Coherence screen: kept=56,724 rejected=0`
- `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
- `Validated 64,082 records from data/processed/all.jsonl`
- `All records valid.`
