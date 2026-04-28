---
source_url: local-session://2026-04-28-p4-duplicate-tool-step-walkthrough
ingested: 2026-04-28
sha256: pending-local-summary
---

# P4 duplicate_tool_step walkthrough — 2026-04-28

Summary of the repo work completed for the Phase 3.2 P4 walkthrough.

## What was analyzed
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
- `tests/test_coherence.py`
- `tests/test_validate_labels.py`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `data/interim/hermes_normalized_phase2.jsonl`

## Real corpus findings captured
- P4 was eligible on `3679` normalized records.
- Minimum valid source trajectory length was `5`.
- Across all eligible records there were `53191` assistant/tool pairs.
- `43912` of those pairs were simple one-call/one-response pairs.
- `9279` pairs were compound multi-call or multi-response bundles.
- `1850` records mixed simple and compound pairs, so the old random pair selection could choose a broader bundle even when a narrower repeated step existed.
- `76` records contained only compound pairs, so any realism improvement had to preserve fallback applicability.

## Implementation change
P4 now prefers duplicating a simple one-call/one-response pair when available, while preserving exact byte-for-byte duplication and falling back to any eligible pair when no simple pair exists.

## Verification run
- `uv run --with pytest --no-project pytest tests/test_perturbations.py::test_p4_duplicates_pair_with_exact_content_and_marks_duplicate_step tests/test_perturbations.py::test_p4_prefers_single_call_pair_when_mixed_with_compound_pairs -v`
- `uv run --with pytest --no-project pytest tests/test_perturbations.py -v`
- `uv run --with pytest --no-project pytest tests/test_coherence.py::test_accepts_repeated_step_perturbation_as_plausible tests/test_validate_labels.py::test_validate_record_rejects_repeated_step_when_bad_step_is_not_duplicate_start -v`

## Learning artifacts created
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p4-duplicate-tool-step-walkthrough/README.md`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p4-duplicate-tool-step-walkthrough/answers.md`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p4-duplicate-tool-step-walkthrough/p4-sample-comparisons.json`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p4-duplicate-tool-step-walkthrough/infographic.png`
- `docs/learning-materials/dataset-builder/phase-3/3.2-rule-walkthroughs/p4-duplicate-tool-step-walkthrough/podcast-transcript.json`
- Podcast MP3 published under the Audiobookshelf profile-aware path for the new topic
