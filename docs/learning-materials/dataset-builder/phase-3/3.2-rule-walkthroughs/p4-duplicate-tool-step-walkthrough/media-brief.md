# Media brief — P4 duplicate_tool_step walkthrough

Audience: the repo owner learning how the dataset-builder perturbation rules behave on real Hermes traces.

Learning goal:
- Understand exactly what P4 duplicates.
- Understand why `bad_step` points to the duplicate assistant step.
- See the minimum valid case and a multi-pair case from the real corpus.
- Learn the implementation lesson: message-level repeated-step generation should prefer the narrowest plausible unit.

Core facts to preserve:
- P4 duplicates an `(assistant tool_call, tool response)` pair.
- The duplicate is inserted immediately after the original pair.
- `bad_step` points to the duplicate assistant step.
- The duplicate is exact byte-for-byte content, not a paraphrase.
- Real corpus stats from `data/interim/hermes_normalized_phase2.jsonl`:
  - eligible records: 3679
  - minimum valid source trajectory length: 5
  - eligible assistant/tool pairs: 53191
  - simple pairs: 43912
  - compound pairs: 9279
  - compound-pair share: 17.4%
  - records only simple: 1753
  - records only compound: 76
  - records mixed simple+compound: 1850
- Implementation improvement:
  - prefer simple one-call/one-response pairs when available
  - fall back to any pair when no simple pair exists

Repo-specific framing:
- This is Phase 3.2 of the dataset-builder learning plan.
- The artifact should emphasize dataset realism and first-error localization, not generic anomaly-generation theory.
- Highlight that the fix is intentionally bounded and deterministic.

Tone:
- Practical
- Elegant
- Best-practice oriented
- Honest about remaining rough edges

Media outputs in this package:
- PNG infographic summarizing the anomaly shape, real-corpus evidence, and the implementation refinement
- Two-host podcast transcript focusing on the realism lesson from compound vs simple pairs

Sources:
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
- `tests/test_coherence.py`
- `tests/test_validate_labels.py`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `p4-sample-comparisons.json`
