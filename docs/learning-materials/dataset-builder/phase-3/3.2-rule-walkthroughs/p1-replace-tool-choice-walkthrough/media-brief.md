# Media brief: P1 replace_tool_choice walkthrough

Use this brief to generate an infographic and podcast for the Phase 3.2 P1 walkthrough in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`.

## Audience
A technically curious learner who already understands normalization and Phase 3 context, and now wants to see what one perturbation rule actually does on real traces.

## Target understanding
By the end, the learner should understand:
1. that P1 changes the tool name while keeping the call structurally valid
2. that mapped replacements like `read_file -> list_directory` are much more believable than `_v2` fallback names
3. that the walkthrough discovered and fixed a real implementation bug in multi-tool assistant messages
4. that P1 is now more bounded technically, but still has realism debt in the fallback path

## Core facts to preserve
- P1 anomaly type is `wrong_tool_choice`
- mapped sample: `read_file -> list_directory`
- fallback samples: `search_files -> search_files_v2`, `terminal -> terminal_v2`
- multi-tool assistant messages can contain multiple `<tool_call>` blocks
- bug fix: `replace_tool_call()` and `replace_tool_call_raw()` now replace only the first match via `count=1`
- verification commands:
  - `uv run pytest tests/test_perturbations.py::test_replace_tool_call_only_replaces_first_tool_call_in_message -v`
  - `uv run pytest tests/test_perturbations.py -v`
- result: `7 passed`

## Repo-specific framing
Hammer home these ideas:
- the first rule walkthrough already improved the implementation, not just the documentation
- realism depends on both the replacement map and the mutation granularity
- `_v2` fallback names are the main remaining weakness in P1

## Suggested podcast angle
Make the episode feel like a debugging-and-understanding debrief:
- what P1 is trying to simulate
- what real traces revealed that the code review alone did not
- why the regex helper bug mattered for realism
- why the next future improvement is probably expanding `NEARBY_TOOLS` or skipping unmapped tools

## Suggested tone
- technically grounded
- implementation-first
- emphasize the most important insight repeatedly: realistic anomalies require bounded mutations

## Source files
- `answers.md`
- `p1-sample-comparisons.json`
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `podcast-transcript.json`
- `podcast-transcript.txt`
- `infographic.png`
