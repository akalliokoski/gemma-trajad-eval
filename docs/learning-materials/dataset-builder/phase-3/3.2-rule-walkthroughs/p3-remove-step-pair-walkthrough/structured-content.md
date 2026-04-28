# Structured content — P3 remove_step_pair walkthrough

## Title
P3 remove_step_pair

## Subtitle
How skipped_required_step works, why bad_step points to a missing location, and why interior pair removal is more believable than terminal truncation

## Learning objectives
- Understand what P3 deletes from a trajectory
- See the smallest real trajectory where P3 can work
- Understand the realism improvement made to pair selection
- Remember the exact verification evidence

## Section 1 — Rule contract
### Heading
What P3 removes
### Core content
- Delete one consecutive `(assistant tool_call, tool response)` pair
- Keep the remaining trajectory intact
- Label as `skipped_required_step`
- Set `generation_rule` to `P3`
### Visual
A simple two-row before/after role diagram with the middle pair highlighted and removed
### Labels
- Before
- Removed pair
- After jump
- bad_step marks missing location

## Section 2 — Real corpus evidence
### Heading
What the corpus showed
### Core content
- Source snapshot: `data/interim/hermes_normalized_phase2.jsonl`
- Applicable records: `3679`
- Minimum valid source length: `5`
- Shortest successful pattern: `system -> user -> assistant tool_call -> tool -> assistant`
### Visual
Metric cards plus a short role-sequence strip
### Labels
- 3679 applicable
- min length 5
- shortest valid shape

## Section 3 — Realism fix
### Heading
Why pair selection matters
### Core content
- Old behavior could remove a terminal pair even when earlier pairs existed
- That sometimes left a trajectory ending on a raw tool response
- New behavior prefers non-terminal pair removal when available
- Fallback still allows the single-pair case
### Visual
Binary comparison: terminal removal vs non-terminal removal
### Labels
- too truncation-like
- better skipped-step failure
- preserve assistant ending when possible

## Section 4 — bad_step semantics
### Heading
What bad_step means here
### Core content
- `bad_step` does not point to a surviving bad message
- It points to where the removed assistant step used to start
- This is valid because the anomaly is a missing step, not a mutated step
### Visual
Index marker on a missing gap in the sequence
### Labels
- missing boundary
- removed assistant index

## Section 5 — Verification
### Heading
How the change was verified
### Core content
- Focused tests:
  - `test_p3_prefers_removing_non_terminal_pair_when_available`
  - `test_p3_returns_shortest_valid_skip_when_only_one_pair_exists`
- Full file check: `uv run pytest tests/test_perturbations.py -v`
- Result: `14 passed`
### Visual
Checklist cards
### Labels
- targeted regression
- corpus evidence snapshot
- 14 passed

## Final takeaway
The best P3 anomaly is not just “a pair was deleted.” It is “a dependency step inside the workflow disappeared,” which is why non-terminal removal is the better default.