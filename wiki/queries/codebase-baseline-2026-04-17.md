---
title: Codebase Baseline - 2026-04-17
created: 2026-04-17
updated: 2026-04-17
type: query
tags: [documentation, roadmap, workflow, decision, dataset]
sources: [docs/codebase-baseline.md]
---

# Codebase Baseline - 2026-04-17

## Core answer
The repository contains a credible skeleton for dataset building, training, evaluation, and demo integrations, but it is not yet runnable end-to-end.

## Most important conclusion
The next implementation slice should stay on the VPS and make the tiny dataset pipeline runnable.

## Why
- dataset generation is the nearest path to first real artifacts
- training depends on processed dataset outputs that do not exist yet
- integrations depend on model/runtime artifacts that do not exist yet
- this slice is lightweight enough for the VPS and does not justify Mac disruption or Modal setup

## Key findings
- `dataset_builder/` is the strongest and most actionable area
- `training/` is a useful skeleton but blocked by missing processed data and missing runtime dependencies
- `integrations/` contains promising demos but is too early for the first implementation slice
- docs and code have a few mismatches that should be cleaned up after the first pipeline artifact exists

## Recommended next step
1. install the minimum VPS dependencies for dataset work
2. download filtered Hermes traces
3. inspect and normalize them
4. build an MVP processed dataset
5. validate it strictly
6. document the walkthrough

## Related pages
- [[hermes-first-development]]
- [[execution-topology]]
- [[gemma]]
