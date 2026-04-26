---
title: Dataset-builder Phase-1 understanding stop line
created: 2026-04-26
updated: 2026-04-26
type: query
tags: [dataset, workflow, documentation, course-material]
sources: [raw/transcripts/dataset-builder-phase-1-understanding-2026-04-26.md]
---

# Dataset-builder Phase-1 understanding stop line

## Durable answer
Phase 1 should stop after raw-data download, empirical trace inspection, and tool-call-structure understanding, because the most important missing knowledge was not whether data exists but what shape that data really has.

## What Phase 1 established
- the raw filtered Hermes dataset is locally reproducible on disk (`3,679` rows, about `368 MB`)
- the corpus is made of long execution traces rather than short prompt/response pairs
- tool use is effectively universal in the filtered corpus
- raw messages are ShareGPT-style `{from, value}` objects with serialized `<tool_call>` / `<tool_response>` markup inside text
- most perturbation families are broadly eligible on the corpus

## Why this matters
These findings explain three major design choices in `dataset_builder/`:

1. `normalize_trajectory.py` is essential, not cosmetic, because it must recover explicit structure from serialized raw text.
2. Tool-pair perturbations are targeting the real center of gravity of the corpus, not a fringe slice.
3. The honest next learning step is Phase 2 normalization study; training should remain deferred until the learner understands how raw traces become normalized trajectories.

## Practical lesson
The bottleneck after Phase 1 is not access to data. It is schema understanding and trust in the transformation path.

## Related pages
- [[dataset-builder-phase-1-readiness-2026-04-24]]
- [[hermes-filtered-traces-dataset-structure-2026-04-22]]
- [[phase-1-scope-boundary-2026-04-26]]
- [[tiny-dataset-pipeline-vps-2026-04-17]]
