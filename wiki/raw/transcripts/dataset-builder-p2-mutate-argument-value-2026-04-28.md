# Raw transcript notes — dataset-builder P2 mutate_argument_value walkthrough

Date: 2026-04-28
Source type: rule walkthrough / implementation debrief

## What was done
- read the P2 walkthrough task from the dataset-builder learning plan
- inspected `dataset_builder/perturbations.py`
- applied P2 to real normalized records from `data/interim/hermes_normalized_phase2.jsonl`
- collected real before/after examples in `p2-sample-comparisons.json`
- confirmed that `_CORRUPTED` string suffixes were too explicit and replaced them with more plausible typo/path-like mutations
- discovered a type-ordering bug where boolean arguments were being treated as integers because `bool` was checked after `int`
- added focused regression tests to `tests/test_perturbations.py`
- fixed P2 so booleans flip logically and string mutations become more believable
- verified with:
  - `uv run pytest tests/test_perturbations.py::test_p2_mutates_path_like_strings_without_corrupted_suffix tests/test_perturbations.py::test_p2_toggles_boolean_arguments_instead_of_treating_them_as_ints -v`
  - `uv run pytest tests/test_perturbations.py -v`
- generated the learning package infographic and podcast
- updated the learning plan to mark the P2 walkthrough complete

## Main findings
- real string sample: `terminal.command` changed from `ls -la` to `sl -la`, which is much subtler than a literal corruption marker
- real integer sample: `read_file.offset` changed from `501` to `-498`, preserving numeric type while making the access pattern wrong
- real boolean sample after the fix: `background=true` changed to `background=false`
- before the fix, that same boolean field could become numeric junk like `-998`, which was a realism bug caused by Python type hierarchy
- the current P2 rule is more believable because corruption now respects value type more closely
- focused and full perturbation-file tests passed after the fix (`12 passed`)

## Important interpretation
P2 realism depends on mutating values in the way the field itself can fail. If booleans, strings, and paths are all corrupted with the same blunt strategy, the model may learn the generator's signature instead of the anomaly class.

## Artifact package
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p2-mutate-argument-value-walkthrough/README.md`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p2-mutate-argument-value-walkthrough/answers.md`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p2-mutate-argument-value-walkthrough/p2-sample-comparisons.json`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p2-mutate-argument-value-walkthrough/infographic.png`
- `/data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-3-perturbation-engine/3.2-rule-walkthroughs/p2-mutate-argument-value-walkthrough/phase-3_3.2-02_p2-mutate-argument-value-walkthrough.mp3`
