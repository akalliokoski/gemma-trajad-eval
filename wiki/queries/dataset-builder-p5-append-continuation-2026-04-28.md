---
title: Dataset-builder P5 append_continuation walkthrough
created: 2026-04-28
updated: 2026-04-28
type: query
tags: [dataset, workflow, documentation, python, course-material]
sources: [docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md, dataset_builder/perturbations.py, tests/test_perturbations.py, tests/test_validate_labels.py, raw/transcripts/p5-append-continuation-walkthrough-2026-04-28.md]
---

# Dataset-builder P5 append_continuation walkthrough

## Durable answer
The important P5 insight was that a perturbation can be structurally valid and still be distributionally unrealistic.

The earlier Task 5 fix had already made `append_continuation` produce a complete assistant -> tool -> assistant tail instead of a dangling tool call. But the rule still hard-coded a `search_web` continuation that did not fit the real Hermes trace corpus. On the current normalized snapshot, P5 applied to `3182` eligible records, and all `3182` lacked prior `search_web` usage.

The right bounded fix was to keep P5 deterministic while making the continuation come from the trajectory itself. P5 now gathers existing assistant/tool pairs from the source trace, prefers lightweight verification-style tools such as `terminal`, `read_file`, `browser_snapshot`, and `search_files`, and copies that pair exactly before appending the wrap-up assistant step.

That change matters because the failure now looks like one more unnecessary verification pass rather than an obviously synthetic tool suddenly appearing after the answer is already complete.

## Evidence
- eligible records: `3182`
- minimum valid source trajectory length: `5`
- preferred lightweight choice used: `3150` (`98.99%`)
- fallback cases: `32` (`1.01%`)
- most common appended tools after the fix:
  - `terminal` `2146`
  - `read_file` `546`
  - `browser_snapshot` `314`
  - `search_files` `113`

## Verification
- focused P5 regression tests passed
- `tests/test_perturbations.py` passed with `17 passed`
- the P5 label-validation check passed

## Related pages
- [[task-5-p5-p6-realism-2026-04-23]]
- [[task-6-rule-aware-bad-step-validation-2026-04-23]]
- [[dataset-builder-p4-duplicate-tool-step-2026-04-28]]
