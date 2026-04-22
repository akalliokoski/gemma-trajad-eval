---
title: Dataset-builder improvements after Phase 0
created: 2026-04-22
updated: 2026-04-22
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

## Related pages
- [[hermes-filtered-traces-dataset-structure-2026-04-22]]
- [[codebase-baseline-2026-04-17]]
