---
title: Dataset-builder Phase-3 perturbation context
created: 2026-04-27
updated: 2026-04-27
type: query
tags: [dataset, workflow, documentation, course-material, python]
sources: [raw/transcripts/dataset-builder-phase-3-perturbation-context-2026-04-27.md]
---

# Dataset-builder Phase-3 perturbation context

## Durable answer
The most important thing Phase 3.1 establishes is that anomaly taxonomy and anomaly generation strategy cannot be evaluated separately: the label may be correct while the trajectory is still unrealistically edited.

## What changed in understanding
- TrajAD's `perturb-and-complete` strategy is now the reference point for realism because downstream behavior is regenerated after the first error
- this repo's direct perturbation path is still valuable for deterministic, inspectable dataset building, but it is weaker on downstream coherence
- Phase 3 should therefore judge each rule twice: once for taxonomy fit and once for trajectory realism
- the repo's current anomaly inventory is now understood as `10` subtypes mapped into the three TrajAD top-level classes with `9` implemented rules and `2` remaining stubs

## Why this matters
Three concrete consequences follow from this comparison:

1. **Realism is the main quality risk** — especially for locally edited rules like P6 and P7 where later steps are not regenerated.
2. **Coverage is uneven** — Task Failure dominates the implemented inventory, while `hallucinated_tool` and `unnecessary_replanning` remain missing.
3. **Phase 3.2 has a sharper purpose** — it is not just a code tour, but a realism audit of each perturbation rule.

## Practical takeaway
The next good question is no longer "what does this rule edit?" It is "does this rule create a believable procedural failure that matches the class we assigned to it?"

## Related pages
- [[dataset-builder-phase-2-normalization-2026-04-26]]
- [[dataset-builder-phase-1-understanding-2026-04-26]]
- [[task-5-p5-p6-realism-2026-04-23]]
- [[task-6-rule-aware-bad-step-validation-2026-04-23]]
