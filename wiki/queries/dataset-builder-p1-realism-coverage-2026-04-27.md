# Dataset-builder P1 realism and NEARBY_TOOLS coverage

Question: How should the project address the finding that P1's `_v2` fallback names are synthetic even though they preserve perturbation yield?

Answer:
The project should optimize P1 for realism, not for maximum perturbation count.

## Decision
- Remove the generic `_v2` fallback entirely.
- Keep P1 only for curated, believable replacement pairs.
- Adapt arguments when the replacement tool has a different interface but the confusion is still realistic.
- Skip unmapped tools instead of inventing fake tool names.

## Why this is the right trade-off
The old fallback guaranteed 100 percent P1 yield on the normalized corpus, but it also created 509 visibly synthetic examples such as `patch_v2` and `browser_navigate_v2`.

After the change:
- P1 success fell from `3679` to `3170`
- fake `_v2` outputs fell from `509` to `0`

That means the lower success rate is not accidental damage. It is the deliberate removal of the weakest examples.

## Concrete improvements implemented
- `terminal -> execute_code` now adapts `command` into `code`
- `search_files -> terminal` now adapts search arguments into a shell command
- browser snapshot / console / images / scroll now have curated nearby confusion sets

## What the change teaches
This slice reinforces a central Phase 0 lesson: structural validity and semantic realism are different quality axes.

A dataset can still be formally valid while teaching the wrong boundary if its anomalies are obviously synthetic. Removing fake fallback names is therefore a quality-discipline upgrade, not just a style preference.

## Remaining roadmap
Future curated mappings should focus on the newly visible gaps:
- `browser_navigate`
- `patch`
- `browser_click`
- `process`
- `browser_vision`
- `execute_code`

## Related pages
- [[dataset-builder-phase-3-perturbation-context-2026-04-27]]
- [[dataset-builder-p1-replace-tool-choice-2026-04-27]]
