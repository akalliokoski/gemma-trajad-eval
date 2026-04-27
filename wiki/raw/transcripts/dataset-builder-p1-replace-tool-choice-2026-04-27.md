# Raw transcript notes — dataset-builder P1 replace_tool_choice walkthrough

Date: 2026-04-27
Source type: rule walkthrough / implementation debrief

## What was done
- read the P1 walkthrough task from the dataset-builder learning plan
- inspected `dataset_builder/perturbations.py`
- applied P1 to real normalized records from `data/interim/hermes_normalized_phase2.jsonl`
- collected three real before/after examples in `p1-sample-comparisons.json`
- discovered a helper bug where multi-tool assistant messages were over-mutated
- added a regression test to `tests/test_perturbations.py`
- fixed `replace_tool_call()` and `replace_tool_call_raw()` to replace only the first match via `count=1`
- verified with:
  - `uv run pytest tests/test_perturbations.py::test_replace_tool_call_only_replaces_first_tool_call_in_message -v`
  - `uv run pytest tests/test_perturbations.py -v`
- generated the learning package infographic and podcast
- updated the learning plan to mark the P1 walkthrough complete

## Main findings
- mapped replacement example: `read_file -> list_directory` preserved arguments and produced the clearest believable wrong-tool-choice anomaly
- fallback examples like `search_files -> search_files_v2` and `terminal -> terminal_v2` remained structurally valid but still looked synthetic
- the main implementation bug was mutation scope, not schema validity
- before the fix, one selected tool-call rewrite could overwrite every `<tool_call>` block in the same assistant message
- after the fix, the helper mutates only the first intended match
- focused and full perturbation-file tests passed after the fix (`7 passed`)
- a full dataset rebuild + strict validation attempt was launched, but the background process exited `137` before completion, so the strongest completed verification evidence remains the targeted regression tests and the real-sample artifact inspection

## Important interpretation
P1 realism depends on two independent things: believable replacement candidates and bounded mutation scope. A nearby tool map helps, but it is still easy to create synthetic anomalies if the implementation rewrites more of the message than intended.

## Artifact package
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/README.md`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/answers.md`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/p1-sample-comparisons.json`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/infographic.png`
- `/data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-3-perturbation-engine/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/phase-3_3.2-01_p1-replace-tool-choice-walkthrough.mp3`
