# Structured content — P5 append_continuation walkthrough infographic

## Title
P5 append_continuation

## Subtitle
continued_after_sufficient_evidence

## Panel 1 — Why the old version felt wrong
- Answer was already complete
- P5 still appended more work
- Extra tool was always `search_web`
- Real corpus did not use `search_web` here

## Panel 2 — New rule behavior
- Find existing assistant/tool pairs
- Prefer lightweight verification tools
- Copy exact pair from the trajectory
- Add short wrap-up assistant step
- Mark `bad_step` at first appended step

## Panel 3 — Preferred tools
- `terminal`
- `read_file`
- `browser_snapshot`
- `search_files`
- also browser/session-search variants when present

## Panel 4 — Corpus evidence
- eligible records: `3182`
- preferred choice used: `3150`
- preferred choice rate: `98.99%`
- fallback cases: `32`
- minimum valid source length: `5`

## Panel 5 — Top appended tools after fix
- `terminal` `2146`
- `read_file` `546`
- `browser_snapshot` `314`
- `search_files` `113`

## Panel 6 — Verification
- focused regression tests passed
- `tests/test_perturbations.py`: `17 passed`
- label validation check passed

## Footer takeaway
Structural correctness is not enough. P5 got better when the continuation stayed inside the trace's own tool ecosystem.
