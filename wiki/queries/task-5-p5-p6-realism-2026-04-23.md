---
title: Task 5 P5/P6 realism upgrade
created: 2026-04-23
updated: 2026-04-23
type: query
tags: [dataset, workflow, documentation, python, course-material]
sources: [docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md, dataset_builder/perturbations.py, tests/test_perturbations.py, raw/transcripts/task-5-p5-p6-realism-2026-04-23.md]
---

# Task 5 P5/P6 realism upgrade

Task 5 improved the two most obviously synthetic perturbation rules so the dataset builder now produces more plausible anomalous trajectories without adding a larger generation subsystem.

## Durable answer

The right fix was to make the perturbations look like believable bad agent behavior while keeping them deterministic and narrow in scope.

### P5 now does
- stop appending a dangling extra tool call
- append a structurally complete but unnecessary continuation: assistant tool call, tool response, assistant wrap-up
- point `bad_step` at the first unnecessary extra step

### P6 now does
- stop using a literal `[CONTRADICTION]` marker
- replace the final assistant answer with a subtle but wrong natural-language conclusion
- infer the contradiction direction from the last tool response using `extract_tool_response_text(...)` and `tool_response_looks_empty(...)`

### Why this shape fits the repo
- better realism without adding model-generated continuation
- better training examples for unwarranted continuation and contradicted tool-result failures
- still simple enough to inspect, test, and explain in a home-lab workflow

## Verification evidence
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_perturbations.py -v`
- `4 passed`
- `python3 dataset_builder/build_trajad_dataset.py --seed 42`
- `Generated 56,724 anomalous records`
- `Coherence screen: kept=56,724 rejected=0`
- `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
- `Validated 64,082 records from data/processed/all.jsonl`
- `All records valid.`

## Related pages
- [[dataset-builder-phase-0-improvements-2026-04-22]]
- [[task-4-lightweight-coherence-screen-2026-04-23]]
- [[hermes-filtered-traces-dataset-structure-2026-04-22]]
