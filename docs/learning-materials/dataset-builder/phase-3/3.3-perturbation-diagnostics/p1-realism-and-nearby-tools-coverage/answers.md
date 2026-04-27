# P1 realism and NEARBY_TOOLS coverage improvement

Source topic: Phase 3 -> Perturbation diagnostics -> improve `NEARBY_TOOLS` coverage after the P1 walkthrough findings.

## What changed?

P1 no longer fabricates fallback tool names like `search_files_v2` or `patch_v2`.

Instead:
- if a tool has a curated nearby replacement, P1 uses it
- if the replacement needs a different argument shape, P1 adapts the arguments
- if the tool has no believable replacement yet, P1 returns `None` and the record is skipped for P1

This is a deliberate precision-over-recall decision.

## Why remove the generic `_v2` fallback?

The earlier walkthrough showed that `_v2` names solved a bookkeeping problem but created a realism problem.

They were:
- structurally valid JSON
- easy to generate
- but visibly synthetic to a human reviewer

That is exactly the kind of anomaly quality debt the project is trying to reduce.

## What curated replacements were added?

New corpus-facing coverage added in `dataset_builder/perturbations.py`:
- `search_files -> terminal`
- `terminal -> execute_code`
- `browser_snapshot -> browser_console | browser_get_images`
- `browser_console -> browser_snapshot | browser_get_images`
- `browser_get_images -> browser_snapshot | browser_console`
- `browser_scroll -> browser_snapshot | browser_console`

Two of those replacements also adapt arguments:

1. `search_files -> terminal`
   - old search-style arguments are converted into a shell command
   - example: `{"target": "files", "pattern": "*.py"}` becomes `{"command": "find . -name '*.py' 2>/dev/null | head -50"}`

2. `terminal -> execute_code`
   - the shell command is wrapped into a small Python snippet
   - example: `{"command": "pwd"}` becomes `{"code": "import subprocess\nsubprocess.run(\"pwd\", shell=True, check=False)"}`

## What did the corpus-level comparison show?

The comparison artifact was generated on all 3,679 records in `data/interim/hermes_normalized_phase2.jsonl`.

Before this change:
- P1 succeeded on 3,679 / 3,679 records
- but 509 successful mutations were fake `_v2` names

After this change:
- P1 succeeded on 3,170 / 3,679 records
- fake `_v2` names dropped to 0

Key observation:
- the drop in success count is exactly 509
- that means the change removed synthetic fallback cases without harming already-curated cases

In other words, this was not a broad regression in curated coverage. It was a controlled removal of low-quality examples.

## Which high-volume tools now behave better?

The two most important improvements are:

1. `terminal`
   - before: already mapped to `execute_code`, but the arguments stayed shell-shaped
   - after: the replacement now carries `execute_code`-style `code` arguments
   - impact: 1,869 corpus records keep P1 coverage with a more believable wrong-tool shape

2. `search_files`
   - before: name changed to `terminal`, but the arguments stayed search-shaped
   - after: the replacement now carries a derived shell command
   - impact: 314 corpus records keep P1 coverage with a more plausible wrong-tool call

## Which tools are intentionally skipped now?

The top explicit gaps exposed by the new policy are:
- `browser_navigate` (126)
- `patch` (114)
- `browser_click` (70)
- `process` (32)
- `browser_vision` (29)
- `execute_code` (24)

These used to be hidden behind obviously synthetic names like `browser_navigate_v2` and `patch_v2`.

That is actually useful. It tells us exactly where future curated mapping work should go.

## Why is skipping better than forcing 100% yield?

Because the project goal is not just to create lots of anomalous rows. It is to create anomalies that teach a model a believable failure boundary.

Fake tool names are cheap, but they teach the wrong lesson:
- the model may learn to spot impossible API names
- instead of learning realistic procedural confusion between nearby tools

Skipping unmapped tools keeps the dataset cleaner and makes future coverage work more targeted.

## What verification was run?

RED/GREEN tests for the behavior change:
- `uv run pytest tests/test_perturbations.py::test_p1_returns_none_for_unmapped_tool_instead_of_fabricating_v2_name tests/test_perturbations.py::test_p1_uses_curated_realistic_replacement_for_terminal tests/test_perturbations.py::test_p1_uses_curated_realistic_replacement_for_search_files -v`
- first run failed before the implementation change
- second run passed after the implementation change

Regression check:
- `uv run pytest tests/test_perturbations.py -v`
- result: `10 passed`

Corpus comparison:
- generated `p1-realism-coverage-comparison.json` from the normalized phase-2 corpus

## Main judgment

This is the right trade-off for the project right now.

- Better realism
- Cleaner anomaly semantics
- Lower P1 yield, but only by eliminating the most visibly fake examples
- Clearer roadmap for the next coverage expansions

## Sources
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `p1-realism-coverage-comparison.json`
