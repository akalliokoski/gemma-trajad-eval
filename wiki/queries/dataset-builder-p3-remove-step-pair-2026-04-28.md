---
title: Why P3 remove_step_pair now prefers non-terminal pair removal
created: 2026-04-28
updated: 2026-04-28
type: query
tags: [trajectory-analysis, dataset, experiment, documentation, course-material]
sources: [raw/transcripts/dataset-builder-p3-remove-step-pair-2026-04-28.md]
---

# Why P3 remove_step_pair now prefers non-terminal pair removal

## Short answer
Because the best `skipped_required_step` anomaly is a missing workflow dependency, not an obviously truncated conversation ending.

## Durable answer
During the P3 walkthrough, corpus inspection on `data/interim/hermes_normalized_phase2.jsonl` showed that the rule could already apply broadly: 3679 records were eligible, and the minimum valid source trajectory length was 5.

The real issue was not applicability. It was realism.

The old P3 implementation chose uniformly from all eligible `(assistant tool_call, tool response)` pairs. In longer traces, that allowed the rule to remove a terminal pair even when an earlier interior pair existed. When that happened, the anomalous trajectory could end on a raw tool response, which made the sample feel more like a generic truncation artifact than a focused skipped-step failure.

The fix was intentionally small:
- prefer removing a non-terminal assistant+tool pair when one exists
- fall back to the only available pair when the trace has just one pair

This preserves the important short-case behavior while producing cleaner multi-step anomalies.

## Why this matters for later training and evaluation
- It keeps the anomaly localized to a missing dependency inside the workflow.
- It reduces the chance that a model learns to detect a crude end-of-trace artifact instead of a skipped required step.
- It keeps `bad_step` semantically meaningful as the missing location where the removed assistant step used to begin.

## Verification
- Added regression tests in `tests/test_perturbations.py` for:
  - non-terminal preference when multiple pairs exist
  - shortest valid fallback when only one pair exists
- Verified with `uv run pytest tests/test_perturbations.py -v` -> `14 passed`

## Related
- [[dataset-builder-phase-3-perturbation-context-2026-04-27]]
- [[dataset-builder-p2-mutate-argument-value-2026-04-28]]
