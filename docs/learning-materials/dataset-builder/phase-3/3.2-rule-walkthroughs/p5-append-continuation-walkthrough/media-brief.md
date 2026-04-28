# Media brief — P5 append_continuation walkthrough

## Audience
- Primary: the repo owner learning how the perturbation engine really behaves on the Hermes trajectory corpus
- Secondary: future contributors trying to understand why P5 was tightened without redesigning the whole generator

## Learning objective
Help the learner understand that P5 realism is not just about having a complete assistant -> tool -> assistant tail. It is about making that extra continuation stay inside the trace's established tool ecosystem so the failure looks like one more unnecessary verification pass rather than a synthetic tool insertion.

## Core story
1. P5 appends extra work after the answer is already complete.
2. The older version had the right structure but the wrong content: it always injected `search_web`.
3. Real-corpus analysis showed that none of the `3182` eligible traces used `search_web`.
4. The improved rule now copies an existing assistant/tool pair and prefers lightweight verification-style tools in `98.99%` of eligible cases.
5. The anomaly still stays deterministic, bounded, and easy to validate.

## Facts to preserve exactly
- Eligible records on `data/interim/hermes_normalized_phase2.jsonl`: `3182`
- Minimum valid source trajectory length: `5`
- Preferred lightweight choice used: `3150` (`98.99%`)
- Fallback cases: `32` (`1.01%`)
- Top appended tools after the fix: `terminal` `2146`, `read_file` `546`, `browser_snapshot` `314`, `search_files` `113`
- Verification result: `17 passed` in `tests/test_perturbations.py`

## Tone
- Practical
- technical
- focused on what the corpus inspection changed in understanding
- slightly emphatic about the distinction between structural validity and distributional realism

## Suggested visual angle
Use a before/after workflow card layout:
- before: hard-coded `search_web` continuation after answer
- after: copied established verification pair from the same trajectory
- bottom row: corpus stats and regression tests

## Sources
- `answers.md`
- `p5-sample-comparisons.json`
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
- `tests/test_validate_labels.py`
