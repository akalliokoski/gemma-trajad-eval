# Raw transcript — dataset-builder P1 realism and NEARBY_TOOLS coverage (2026-04-27)

## Context
Follow-up to the Phase 3.2 P1 walkthrough after identifying `_v2` fallback naming as the main realism weakness.

## Implemented code changes
- `dataset_builder/perturbations.py`
  - removed the generic `_v2` fallback from `p1_replace_tool_choice`
  - added curated Hermes-corpus mappings for:
    - `search_files`
    - `terminal`
    - `browser_snapshot`
    - `browser_console`
    - `browser_get_images`
    - `browser_scroll`
  - added argument adaptation helpers for:
    - `search_files -> terminal`
    - `terminal -> execute_code`
- `tests/test_perturbations.py`
  - added RED/GREEN regression coverage for:
    - unmapped tools now return `None`
    - `terminal` uses curated replacement plus adapted `code` arguments
    - `search_files` uses curated replacement plus adapted `command` arguments

## Verification
- Focused RED/GREEN check failed before implementation and passed after:
  - `uv run pytest tests/test_perturbations.py::test_p1_returns_none_for_unmapped_tool_instead_of_fabricating_v2_name tests/test_perturbations.py::test_p1_uses_curated_realistic_replacement_for_terminal tests/test_perturbations.py::test_p1_uses_curated_realistic_replacement_for_search_files -v`
- Regression suite:
  - `uv run pytest tests/test_perturbations.py -v`
  - result: `10 passed`

## Corpus comparison results
Source file: `data/interim/hermes_normalized_phase2.jsonl`
Total records: `3679`

Before change:
- P1 success: `3679`
- fake `_v2` outputs: `509`

After change:
- P1 success: `3170`
- fake `_v2` outputs: `0`

Interpretation:
- success dropped by exactly `509`
- all removed cases were the previously synthetic `_v2` fallback cases
- curated cases were preserved

## Exposed remaining gaps
Top skipped source tools after removing fallback:
- `browser_navigate` 126
- `patch` 114
- `browser_click` 70
- `process` 32
- `browser_vision` 29
- `execute_code` 24

## Learning artifact package
- `docs/learning-materials/dataset-builder/phase-3/3.3-perturbation-diagnostics/p1-realism-and-nearby-tools-coverage/`
