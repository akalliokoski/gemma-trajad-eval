# P5 append_continuation walkthrough raw transcript

Date: 2026-04-28
Project: `gemma-trajad-eval`
Topic: Phase 3.2 perturbation rule walkthrough for `P5 append_continuation`

## Summary
This walkthrough revisited `P5` after the earlier structural realism fix from Task 5 and focused on a remaining distributional realism problem in the current Hermes trajectory corpus.

The key observation was that the older P5 implementation still appended a hard-coded `search_web` continuation after the final answer. On the current normalized corpus snapshot (`data/interim/hermes_normalized_phase2.jsonl`), P5 was eligible on `3182` records, and every one of those eligible traces lacked prior `search_web` usage. So the rule had the right assistant -> tool -> assistant structure but still produced an out-of-distribution tool insertion.

## What changed
- Added/updated focused P5 regression tests in `tests/test_perturbations.py`.
- Verified the new tests fail against the old implementation.
- Updated `dataset_builder/perturbations.py` so P5 now:
  - gathers existing assistant/tool pairs from the source trajectory
  - prefers lightweight verification-style pairs (`terminal`, `read_file`, `browser_snapshot`, `search_files`, related browser/session-search tools)
  - falls back only when no preferred pair exists
  - copies the chosen assistant and tool steps exactly, then appends the short wrap-up assistant reply

## Corpus findings captured in the walkthrough
- eligible records: `3182`
- minimum valid source trajectory length: `5`
- preferred lightweight choice used: `3150` (`98.99%`)
- fallback cases: `32` (`1.01%`)
- top appended tools after the fix:
  - `terminal` `2146`
  - `read_file` `546`
  - `browser_snapshot` `314`
  - `search_files` `113`

## Verification performed
- `uv run --with pytest --no-project pytest tests/test_perturbations.py::test_p5_appends_existing_final_tool_pair_as_unnecessary_continuation tests/test_perturbations.py::test_p5_prefers_established_lightweight_verification_pair_when_mixed -v`
- `uv run --with pytest --no-project pytest tests/test_perturbations.py -v`
- `uv run --with pytest --no-project pytest tests/test_validate_labels.py::test_validate_record_rejects_continuation_when_bad_step_skips_first_extra_step -v`

All verification passed after the implementation change.

## Learning-material artifacts created
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p5-append-continuation-walkthrough/README.md`
- `.../answers.md`
- `.../media-brief.md`
- `.../analysis.md`
- `.../structured-content.md`
- `.../prompts/infographic.md`
- `.../podcast-transcript.json`
- `.../podcast-transcript.txt`
- `.../p5-sample-comparisons.json`
- `.../infographic.png`

## Key conclusion
For P5, structural correctness was not enough. The anomaly became materially better when the continuation stayed inside the trace's established tool ecosystem and preferentially looked like one more gratuitous verification pass instead of a synthetic new action.
