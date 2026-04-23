Objective: Deepen dataset label validation so first-error localization is checked semantically for the current perturbation rules, not just by type and range.

Implementation facts:
- Updated dataset_builder/validate_labels.py.
- Added helper functions _content(step), _has_tool_call(step), and _validate_rule_aware_bad_step(record).
- Validation now performs targeted generation_rule checks for P4 repeated_step, P5 continued_after_sufficient_evidence, and P7 premature_final_answer.
- P4 validation now checks that bad_step points to the duplicated assistant step and that the following tool step matches the preceding original pair.
- P5 validation now checks that bad_step points to the first unnecessary extra step in the appended assistant -> tool -> assistant continuation.
- P7 validation now checks that bad_step points to the inserted premature final answer at the cut point and that earlier tool evidence exists.
- Updated tests/test_validate_labels.py with focused negative tests for mislocalized P4, P5, and P7 labels, plus a skipped-step edge case that allows a missing position at the end.

Verification:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py -v
- 8 passed
- python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
- Validated 64,082 records from data/processed/all.jsonl
- All records valid.

Files involved:
- dataset_builder/validate_labels.py
- tests/test_validate_labels.py
