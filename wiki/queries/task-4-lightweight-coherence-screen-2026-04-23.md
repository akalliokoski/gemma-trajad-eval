---
title: Task 4 lightweight coherence screen
created: 2026-04-23
updated: 2026-04-23
type: query
tags: [dataset, workflow, documentation, python, course-material]
sources: [docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md, dataset_builder/coherence.py, dataset_builder/build_trajad_dataset.py, tests/test_coherence.py, tests/test_build_trajad_dataset.py]
---

# Task 4 lightweight coherence screen

Task 4 added a tiny deterministic coherence layer after perturbation so the dataset builder can reject obviously broken anomalous traces without introducing a heavy perturb-and-complete workflow.

## Durable answer

The right shape for this repo is a narrow structural screen, not a semantic judge.

### The screen now checks
- dangling assistant tool calls with no immediate tool response
- orphan tool responses with no matching preceding assistant tool call
- exact adjacent duplicate fragments of the same message type

### Where it runs
- `build_trajad_dataset.py` now calls `is_plausible_trajectory(...)` immediately after `apply_perturbation(...)`
- plausible anomalies are kept
- implausible anomalies are dropped and counted by rejection reason

### Important implementation nuance
The first draft accidentally made `repeated_step` a dead anomaly family because it rejected all adjacent duplicate assistant/tool pairs. The final implementation narrowed the duplicate rule so `P4` remains plausible while still catching obviously broken duplicate fragments.

### Reproducibility fix bundled with Task 4
`build_trajad_dataset.py` now uses `unique_source_ids_in_order(records)` before shuffling source IDs. This preserves reproducible same-seed split assignment instead of depending on nondeterministic set ordering.

## Verification evidence
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_coherence.py tests/test_perturbations.py tests/test_validate_labels.py tests/test_build_trajad_dataset.py -q`
- `13 passed`
- `python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42`
- `Generated 29,354 anomalous records`
- `Coherence screen: kept=29,354 rejected=0`
- `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
- `All records valid`
- `diff -u /tmp/task4_build1.log /tmp/task4_build2.log` produced no diff output for same-seed builds

## Related pages
- [[dataset-builder-phase-0-improvements-2026-04-22]]
- [[hermes-filtered-traces-dataset-structure-2026-04-22]]
