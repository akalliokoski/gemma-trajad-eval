---
title: Dataset-builder improvements after Phase 0
created: 2026-04-22
updated: 2026-04-23
type: query
tags: [dataset, workflow, decision, documentation, python, course-material]
sources: [raw/transcripts/dataset-builder-phase-0-improvements-2026-04-22.md]
---

# Dataset-builder improvements after Phase 0

Based on the Phase 0 learning materials and the current `dataset_builder/` implementation, the project should not rewrite the dataset pipeline. The current script-first architecture is already a good fit for a home AI lab.

## Durable answer

The best next step is to improve data-quality discipline rather than add new infrastructure.

### Keep
- normalization
- perturbation-based synthetic generation
- split assignment by `source_trace_id`
- lightweight schema validation
- plain Python + JSONL workflow

### Improve first
1. Make raw-data inspection schema-aware so it works on Hermes ShareGPT-style traces.
2. Add small derived metadata during normalization instead of redesigning the schema.
3. Add `anomaly_class` alongside `anomaly_type` to align the dataset with the TrajAD taxonomy.
4. Add a lightweight coherence screen to reject obviously implausible perturbed outputs.
5. Improve realism of the most synthetic perturbation rules.
6. Strengthen first-error localization checks in validation.
7. Save build manifests and diagnostics for reproducibility.

## Why this is the right shape

Phase 0 clarified that the dataset is long-trace, tool-heavy, and stored in ShareGPT-like outer structure with embedded tool protocol markup. That means the key challenge is trustworthy structure recovery and realistic anomaly construction, not platform complexity.

A small, deterministic, quality-focused roadmap is the best fit for the repo's current scale.

## Compute policy

For future GPU-backed extensions, Modal serverless GPU is now the default path. Apple Silicon remains useful as a secondary local option, but it is no longer the default GPU tier.

## Implementation progress

As of 2026-04-23, the first five improvement tasks from the plan have been completed and committed:
- Task 1: raw-schema-safe inspection for ShareGPT-style Hermes traces
- Task 2: derived structural metadata during normalization
- Task 3: explicit top-level anomaly classes
- Task 4: lightweight perturbation coherence screening
- Task 5: more realistic P5/P6 continuation and contradiction rules

These changes reinforce the core conclusion of this page: the right path is small, high-leverage quality improvements on top of the existing script-first pipeline, not a rewrite.

As of later on 2026-04-23, Task 6 is also complete:
- Task 6: rule-aware bad-step validation for first-error localization semantics

## Home-lab fit

This repository is now explicitly the first project in the user's home AI lab. That raises the bar for craft, but not for complexity: best practices should be applied in a practical, elegant, community-friendly way, with over-engineering treated as a failure mode rather than a mark of seriousness.

## Related pages
- [[hermes-filtered-traces-dataset-structure-2026-04-22]]
- [[codebase-baseline-2026-04-17]]
- [[task-4-lightweight-coherence-screen-2026-04-23]]
- [[task-5-p5-p6-realism-2026-04-23]]
- [[task-6-rule-aware-bad-step-validation-2026-04-23]]
- [[home-ai-lab-principles]]
