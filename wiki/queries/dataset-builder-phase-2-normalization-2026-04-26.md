---
title: Dataset-builder Phase-2 normalization deep dive
created: 2026-04-26
updated: 2026-04-26
type: query
tags: [dataset, workflow, documentation, course-material, python]
sources: [raw/transcripts/dataset-builder-phase-2-normalization-2026-04-26.md]
---

# Dataset-builder Phase-2 normalization deep dive

## Durable answer
The most important thing Phase 2 establishes is that normalization is the schema bridge that turns raw Hermes traces into a stable internal dataset contract without losing rows or destabilizing trace identity.

## What changed in understanding
- raw traces are no longer just observed as agentic and tool-centric; they are now understood as inputs to a concrete transformation contract
- the normalized representation explicitly standardizes roles into `system`, `user`, `assistant`, and `tool`
- clean-label defaults and structural metadata are attached at normalization time
- `source_trace_id` is now clearly understood as a leakage-prevention prerequisite for later split assignment

## Why this matters
Three guarantees make the rest of the project more trustworthy:

1. **Row preservation** — the real corpus normalized to `3,679` records with `0` errors.
2. **Deterministic identity** — `source_trace_id` stayed stable on repeated checks.
3. **Bounded schema simplification** — the trajectory stays simple while metadata carries extra structure.

## Edge-case lesson
The plan raised good questions about unknown roles and missing metadata, but the current filtered Hermes corpus is cleaner than that hypothetical:
- no non-standard roles were observed
- no missing `category` / `subcategory` cases were observed
- metadata was never empty in the audited snapshot

## Practical takeaway
Normalization is not the boring prelude to the project. It is the step that makes perturbation, validation, and later learning mean the same thing across runs.

## Related pages
- [[dataset-builder-phase-1-understanding-2026-04-26]]
- [[dataset-builder-phase-1-readiness-2026-04-24]]
- [[tiny-dataset-pipeline-vps-2026-04-17]]
- [[task-7-build-manifest-and-diagnostics-2026-04-23]]
