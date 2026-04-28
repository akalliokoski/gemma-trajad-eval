---
title: Dataset-builder P4 duplicate_tool_step walkthrough
created: 2026-04-28
updated: 2026-04-28
type: query
tags: [dataset, workflow, documentation, python, course-material]
sources: [raw/transcripts/p4-duplicate-tool-step-walkthrough-2026-04-28.md, dataset_builder/perturbations.py, tests/test_perturbations.py, docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md]
---

# Dataset-builder P4 duplicate_tool_step walkthrough

The P4 walkthrough showed that repeated-step realism depends on the granularity of the pair chosen for duplication, not just on whether the pair is duplicated correctly.

## Durable answer

The right bounded improvement was to keep P4 deterministic and byte-exact, but prefer duplicating a simple one-call/one-response assistant/tool pair when the trace offers one.

### What changed
- `dataset_builder/perturbations.py` still duplicates an adjacent assistant/tool pair and still sets `bad_step` to the duplicate assistant step
- P4 now counts `<tool_call>` blocks in the assistant message and `<tool_response>` blocks in the tool message
- when a record mixes simple and compound candidate pairs, P4 now prefers the simple pair
- fallback behavior is unchanged for records that only contain compound pairs

### Why this was necessary
- P4 was eligible on `3679` records in the normalized corpus snapshot
- across those records there were `53191` eligible assistant/tool pairs
- `9279` pairs, or `17.4%`, were compound bundles with multiple calls or responses in one pair
- `1850` records mixed simple and compound pairs, so the old random policy could pick a broader multi-call bundle even though a narrower repeated step existed in the same trace
- only `76` records were all-compound, so a preference rule was enough; no redesign was needed

### What stayed the same
- `bad_step` still points to the duplicate assistant step, not the original occurrence
- the duplicate remains an exact byte-for-byte copy of the original assistant and tool messages
- the anomaly remains `repeated_step`, not a new subtype
- the coherence screen still accepts the resulting repeated-step trajectories as plausible

### Verification evidence
- focused P4 regression tests passed for exact duplication and simple-pair preference
- the full perturbations suite passed with `16 passed`
- the related coherence and validator checks passed with `2 passed`

## Related pages
- [[dataset-builder-phase-3-perturbation-context-2026-04-27]]
- [[dataset-builder-p3-remove-step-pair-2026-04-28]]
- [[task-6-rule-aware-bad-step-validation-2026-04-23]]
