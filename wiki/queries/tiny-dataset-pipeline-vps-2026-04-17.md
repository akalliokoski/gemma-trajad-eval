---
title: Tiny Dataset Pipeline on VPS - 2026-04-17
created: 2026-04-17
updated: 2026-04-17
type: query
tags: [dataset, workflow, documentation, decision, roadmap]
sources: [docs/data-pipeline-walkthrough.md]
---

# Tiny Dataset Pipeline on VPS - 2026-04-17

## Core answer
The first end-to-end dataset pipeline slice now works on the VPS.

## What succeeded
- filtered Hermes traces were downloaded
- raw traces were normalized successfully
- MVP perturbation-based processed splits were generated
- strict validation passed for train/dev/test
- regression tests were added for the two bugs fixed during the run

## Bugs fixed during execution
1. `dataset_builder/perturbations.py`
   - regex replacement broke when JSON contained unicode escape sequences
2. `dataset_builder/validate_labels.py`
   - validator was too strict for `skipped_required_step` when the missing step should occur at the end of the trajectory

## Important remaining gap
- `dataset_builder/inspect_traces.py` still assumes raw messages already use `role/content` instead of ShareGPT-style `from/value`

## Recommended next step
- run `training/prepare_sft_data.py` on the processed dataset, starting with the binary task

## Related pages
- [[codebase-baseline-2026-04-17]]
- [[execution-topology]]
- [[hermes-first-development]]
