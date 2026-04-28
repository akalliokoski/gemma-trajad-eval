# Media brief — P2 mutate_argument_value walkthrough

Audience: a learner studying the dataset-builder perturbation engine after already seeing Phase 1 normalization and the P1 walkthrough.

Goal: make the listener understand why P2 is a narrower, argument-level anomaly rule and why type-aware corruption matters for realism.

Core facts to preserve exactly:
- P2 keeps the tool name but mutates one argument value.
- Real string sample: `command="ls -la" -> "sl -la"`.
- Real integer sample: `offset=501 -> -498`.
- Real boolean bug found: `background=true` was previously becoming `-998` because `bool` was checked after `int`.
- Fix: handle `bool` before `int`, and replace `_CORRUPTED` string suffixes with typo/path-like mutations.
- Verification: focused P2 tests passed, and `uv run pytest tests/test_perturbations.py -v` passed with `12 passed`.

Tone:
- practical and debrief-oriented
- emphasize the most important design lesson instead of reciting every code branch
- make clear that the walkthrough improved the implementation, not just the docs

Repo framing:
- this is part of `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- the artifact package lives beside the P1 walkthrough under `phase-3/3.2-rule-walkthroughs/`
- no video explainer for this topic

Sources:
- `answers.md`
- `p2-sample-comparisons.json`
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
