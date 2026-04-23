# Task 6 rule-aware bad-step validation implementation note

Date: 2026-04-23
Source: verified local implementation in the active Hermes session

Task 6 from `docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md` strengthened first-error localization validation in `dataset_builder/validate_labels.py`.

Key implementation facts:
- Added helper functions `_content(step)`, `_has_tool_call(step)`, and `_validate_rule_aware_bad_step(record)`.
- Kept the existing generic schema checks, then layered on narrow rule-aware checks.
- Added semantic validation for generation rules `P4`, `P5`, and `P7`.
- `P4` now requires `bad_step` to point to the duplicated assistant step and matching assistant/tool pair.
- `P5` now requires `bad_step` to point to the first unnecessary extra step in the appended assistant -> tool -> assistant continuation.
- `P7` now requires `bad_step` to point to the inserted premature final answer at the cut point, after earlier tool evidence exists.
- `tests/test_validate_labels.py` now includes focused negative tests for mislocalized `P4`, `P5`, and `P7` records plus a skipped-step end-position edge case.

Verification facts:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py -v`
- `8 passed`
- `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
- `Validated 64,082 records from data/processed/all.jsonl`
- `All records valid.`
