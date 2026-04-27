# Raw transcript — dataset-builder perturbation diagnostics script (2026-04-27)

## Context
Next undone Phase 3.3 slice after the P1 realism cleanup.

## Implemented artifact
- Added `dataset_builder/perturbation_diagnostics.py`
- Added `tests/test_perturbation_diagnostics.py`
- Generated `data/processed/perturbation_diagnostics.json`

## Verification
- `uv run pytest tests/test_perturbation_diagnostics.py -v`
- `uv run pytest tests/test_perturbation_diagnostics.py tests/test_perturbations.py -v`
- `uv run python dataset_builder/perturbation_diagnostics.py --input data/interim/hermes_normalized_phase2.jsonl --output data/processed/perturbation_diagnostics.json`

## First corpus results
- total records: `3679`
- `p1_replace_tool_choice`: eligible `3679`, succeeded `3170`, failed `509`, success rate `86.2%`
- `p2_mutate_argument_value`: eligible `3678`, succeeded `3646`, failed `32`, success rate `99.1%`
- `p3`/`p4`/`p5`/`p6`/`p7`/`p8`/`p9`: `100%` on eligible records

## Interpretation
- P1 is the only rule with significant remaining failure volume.
- P1 failures are now explicit coverage gaps after removing the synthetic `_v2` fallback.
- The script creates a reusable rule-by-rule coverage meter for future realism passes.

## Learning-material package
- `docs/learning-materials/dataset-builder/phase-3/3.3-perturbation-diagnostics/rule-diagnostics-script/`
