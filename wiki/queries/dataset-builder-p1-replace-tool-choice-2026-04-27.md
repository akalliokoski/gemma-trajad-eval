---
title: Dataset-builder P1 replace_tool_choice walkthrough
created: 2026-04-27
updated: 2026-04-27
type: query
tags: [dataset, workflow, documentation, course-material, python]
sources: [raw/transcripts/dataset-builder-p1-replace-tool-choice-2026-04-27.md]
---

# Dataset-builder P1 replace_tool_choice walkthrough

## Durable answer
The first perturbation-rule walkthrough established that P1 is only convincing when it makes a believable nearby-tool substitution and mutates exactly one intended tool-call block.

## What changed in understanding
- mapped replacements such as `read_file -> list_directory` can create useful wrong-tool-choice anomalies while preserving structural validity
- `_v2` fallback names such as `search_files_v2` and `terminal_v2` remain the main realism weakness in P1
- the walkthrough exposed a real implementation bug: helper-based substitution was mutating every `<tool_call>` block in a multi-tool assistant message
- the rule is now more trustworthy because replacement scope was reduced to the first intended match via `count=1`

## Why this matters
Three concrete lessons came out of the first rule walkthrough:

1. **Replacement quality matters** — nearby-tool maps produce better anomalies than fabricated suffix-based fallbacks.
2. **Mutation granularity matters** — over-mutation can silently turn a bounded perturbation into a much more synthetic rewrite.
3. **Walkthroughs can improve implementation directly** — this learning slice produced a real regression test and a real bug fix, not just documentation.

## Practical takeaway
The next future improvement for P1 is not another large refactor. It is likely either expanding `NEARBY_TOOLS` from the real corpus or skipping unmapped tools instead of inventing `_v2` names.

## Related pages
- [[dataset-builder-phase-3-perturbation-context-2026-04-27]]
- [[task-5-p5-p6-realism-2026-04-23]]
- [[task-6-rule-aware-bad-step-validation-2026-04-23]]
- [[dataset-builder-phase-2-normalization-2026-04-26]]
