---
title: Task 6 rule-aware bad-step validation
created: 2026-04-23
updated: 2026-04-23
type: query
tags: [dataset, workflow, documentation, python, course-material]
sources: [docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md, dataset_builder/validate_labels.py, tests/test_validate_labels.py, raw/transcripts/task-6-rule-aware-bad-step-validation-2026-04-23.md]
---

# Task 6 rule-aware bad-step validation

Task 6 made first-error localization validation stricter by checking that `bad_step` points to the right semantic position for the highest-value perturbation rules already implemented in the repo.

## Durable answer

The right upgrade was to keep schema validation simple, then add a narrow rule-aware layer for the rules where mislocalized labels would most directly damage supervision quality.

### What changed
- added `_content(step)` and `_has_tool_call(step)` as tiny helpers
- added `_validate_rule_aware_bad_step(record)` and called it from `validate_record(...)`
- added semantic checks for `P4`, `P5`, and `P7`
- left the rest of the validator generic rather than overfitting to hypothetical future rules

### What each rule now enforces
- `P4` repeated_step: `bad_step` must point to the duplicated assistant step and matching assistant/tool pair
- `P5` continued_after_sufficient_evidence: `bad_step` must point to the first unnecessary extra step in the appended continuation
- `P7` premature_final_answer: `bad_step` must point to the inserted premature final answer at the cut point, after earlier tool evidence exists

### Why this shape fits the repo
- strengthens the first-error supervision target without redesigning the dataset format
- keeps the validator deterministic and readable
- focuses effort on real rules already emitted by the perturbation pipeline
- improves trustworthiness without over-engineering the home-lab workflow

## Verification evidence
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py -v`
- `8 passed`
- `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
- `Validated 64,082 records from data/processed/all.jsonl`
- `All records valid.`

## Related pages
- [[dataset-builder-phase-0-improvements-2026-04-22]]
- [[task-5-p5-p6-realism-2026-04-23]]
- [[hermes-filtered-traces-dataset-structure-2026-04-22]]
