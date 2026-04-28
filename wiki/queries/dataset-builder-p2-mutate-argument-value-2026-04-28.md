---
title: Dataset-builder P2 mutate_argument_value walkthrough
created: 2026-04-28
updated: 2026-04-28
type: query
tags: [dataset, workflow, documentation, course-material, python]
sources: [raw/transcripts/dataset-builder-p2-mutate-argument-value-2026-04-28.md]
---

# Dataset-builder P2 mutate_argument_value walkthrough

## Durable answer
The second perturbation-rule walkthrough established that P2 becomes much more trustworthy when argument corruption is type-aware rather than using blunt explicit markers.

## What changed in understanding
- the previous `_CORRUPTED` string suffix was too obvious for realistic `bad_tool_arguments` anomalies
- typo-style command corruption like `ls -la -> sl -la` is still wrong, but much more believable
- integer corruption such as `offset=501 -> -498` preserves schema while breaking behavior cleanly
- the walkthrough exposed a real implementation bug: Python `bool` values were being treated as integers because branch order checked `int` before `bool`
- the rule is now more trustworthy because booleans flip logically and string values mutate in a more field-appropriate way

## Why this matters
Three concrete lessons came out of the second rule walkthrough:

1. **Type-aware realism matters** — bad arguments should fail in the way that particular field fails, not with one generic corruption style.
2. **Language-level quirks matter** — Python's `bool` subclassing `int` created a silent realism bug that only showed up when reading real outputs.
3. **Walkthroughs can improve implementation directly** — this learning slice produced real regression tests and a real bug fix, not just explanation text.

## Practical takeaway
The next future improvement for P2 is not a wholesale rewrite. It is likely gradual specialization by argument role: path strings, shell commands, search queries, numeric offsets, and structured payloads.

## Related pages
- [[dataset-builder-phase-3-perturbation-context-2026-04-27]]
- [[dataset-builder-p1-replace-tool-choice-2026-04-27]]
- [[dataset-builder-perturbation-diagnostics-script-2026-04-27]]
- [[dataset-builder-phase-2-normalization-2026-04-26]]
