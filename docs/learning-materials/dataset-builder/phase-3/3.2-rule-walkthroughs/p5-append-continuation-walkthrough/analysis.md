# Infographic analysis — P5 append_continuation walkthrough

## Goal
Summarize why the P5 continuation rule needed a realism refinement and what the new heuristic actually does.

## Audience takeaway
The learner should leave with one main idea: a structurally complete continuation can still be unrealistic if it invents a tool that the trace never used. P5 got better by staying inside the source trajectory's established tool set and by preferring lightweight verification-style pairs.

## Best layout
A wide landscape bento layout with five panels:
1. title + anomaly type
2. old P5 problem
3. new P5 selection heuristic
4. corpus evidence
5. regression-test verification

## Panel guidance
### Panel 1 — title
- "P5 append_continuation"
- subtitle: "continued_after_sufficient_evidence"

### Panel 2 — old problem
Short labels only:
- answer already finished
- hard-coded `search_web`
- out-of-distribution tool insertion
- structurally valid but distributionally wrong

### Panel 3 — new heuristic
Show the policy as a compact ladder:
- collect assistant/tool pairs
- prefer lightweight verification pair
- copy exact assistant + tool content
- append short wrap-up
- `bad_step = first appended step`

### Panel 4 — corpus evidence
Use exact numbers:
- eligible: `3182`
- preferred choice: `3150 (98.99%)`
- fallback: `32 (1.01%)`
- top appended tools: `terminal 2146`, `read_file 546`, `browser_snapshot 314`, `search_files 113`

### Panel 5 — verification
- focused P5 tests passed
- full perturbations file: `17 passed`
- label validation check passed

## Style
- dark technical dashboard
- crisp cards and arrows
- large typography
- very little prose
- avoid code blocks and long filenames inside the image

## What not to include
- no dense paragraph text
- no giant raw JSON snippets
- no tiny file paths
- no full pytest commands; summarize them as focused tests + full module + label validation
