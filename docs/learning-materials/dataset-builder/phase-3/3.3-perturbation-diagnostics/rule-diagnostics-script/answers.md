# Perturbation diagnostics script

Source topic: Phase 3 -> 3.3 Perturbation diagnostics -> write a perturbation diagnostics script.

## What was implemented?

A new script was added at `dataset_builder/perturbation_diagnostics.py`.

It does exactly what the plan asked for:
- reads normalized records from `data/interim/hermes_normalized_phase2.jsonl`
- applies each perturbation rule across the corpus in a deterministic way
- counts eligible, succeeded, failed, and ineligible records per rule
- prints a compact markdown-style table to stdout
- writes structured JSON to `data/processed/perturbation_diagnostics.json`

The JSON artifact was also copied into this learning package as `perturbation-diagnostics-snapshot.json`.

## How does the script define "eligible"?

The key design choice was separating structural eligibility from actual rule success.

That matters because a rule can fail for two very different reasons:
1. the record is not structurally suitable for the rule at all
2. the record looks structurally suitable, but the rule still cannot produce a perturbation

For example, after the P1 realism cleanup:
- a record with no parsed tool call is not eligible for P1
- a record with a parsed tool call but an unmapped tool is eligible, yet still fails

This is the right distinction because it keeps the diagnostics honest.

## What rules were used?

The script runs all current rules in `ALL_RULES`:
- `p1_replace_tool_choice`: eligible 3679, succeeded 3170, failed 509, success rate 86.2%
- `p2_mutate_argument_value`: eligible 3678, succeeded 3646, failed 32, success rate 99.1%
- `p3_remove_step_pair`: eligible 3679, succeeded 3679, failed 0, success rate 100.0%
- `p4_duplicate_tool_step`: eligible 3679, succeeded 3679, failed 0, success rate 100.0%
- `p5_append_continuation`: eligible 3182, succeeded 3182, failed 0, success rate 100.0%
- `p6_contradict_final_answer`: eligible 3182, succeeded 3182, failed 0, success rate 100.0%
- `p7_truncate_before_decision`: eligible 3658, succeeded 3658, failed 0, success rate 100.0%
- `p8_swap_dependent_steps`: eligible 3658, succeeded 3658, failed 0, success rate 100.0%
- `p9_invalid_tool_json`: eligible 3679, succeeded 3679, failed 0, success rate 100.0%

## What did the first real run show?

The generated diagnostics on all 3,679 normalized records produced the following headline result:
- P1 is now the only rule with meaningful failures
- every other rule is either perfect or near-perfect on the current normalized corpus

Most important rows:
- `p1_replace_tool_choice`: eligible `3679`, succeeded `3170`, failed `509`, success rate `86.2%`
- `p2_mutate_argument_value`: eligible `3678`, succeeded `3646`, failed `32`, success rate `99.1%`
- `p3_remove_step_pair`: `100.0%`
- `p4_duplicate_tool_step`: `100.0%`
- `p5_append_continuation`: eligible `3182`, `100.0%`
- `p6_contradict_final_answer`: eligible `3182`, `100.0%`
- `p7_truncate_before_decision`: eligible `3658`, `100.0%`
- `p8_swap_dependent_steps`: eligible `3658`, `100.0%`
- `p9_invalid_tool_json`: eligible `3679`, `100.0%`

## Why is the P1 result so important?

Because it confirms the realism story quantitatively.

Earlier, P1 hit 100 percent success only by inventing fake fallback names like `patch_v2` and `browser_navigate_v2`.
After the realism cleanup, the script shows that:
- P1 still succeeds on most records
- but it now fails on 509 eligible records instead of generating synthetic fake-name anomalies

That failure count is not a bug. It is the cost of a cleaner anomaly boundary.

## What do the P1 failure examples look like?

The diagnostics script stores a few example failures for inspection. The first run captured:
  - 930977e3-cb4e-4bcd-8218-c717389c4c14 (clarify)
  - e0faf24b-e135-412f-b89d-c90b263e677b (session_search)
  - 66890ddc-faa5-4ca2-9f80-f751e2f8eed3 (terminal)
  - 19be0b4f-b8d3-48f9-af88-6d22eda39812 (skills_list)
  - 268a8715-aca4-4edd-908c-60feff040be7 (execute_code)

Those examples are useful because they expose the next mapping targets directly instead of hiding them behind fake fallback names.

## What else did the diagnostics teach?

Three smaller but useful lessons showed up:

1. P2 is almost universal but not fully universal
- one record out of 3,679 was not eligible
- 32 eligible records still failed
- that means argument mutation remains strong, but not literally guaranteed

2. P5 and P6 depend on conversation endings
- only 3,182 records were eligible
- that tells us not every normalized record ends in the final assistant shape these rules expect

3. P7 and P8 depend on multi-step tool structure
- 3,658 records were eligible
- so the corpus is very rich in multi-step tool use, but not perfectly uniform

## Why is this script a good next slice?

Because it turns vague intuition into measured rule behavior.

Before this script, we had point observations from walkthroughs.
After this script, we have a repeatable corpus-wide measurement artifact that can answer questions like:
- which rules are actually coverage bottlenecks?
- did a realism improvement help or hurt?
- which rule needs the next cleanup pass?

That makes Phase 3 less anecdotal and more engineering-driven.

## What verification was run?

Test-first verification:
- `uv run pytest tests/test_perturbation_diagnostics.py -v`
- first run failed before the module existed
- second run passed after implementation

Focused regression + neighboring rule check:
- `uv run pytest tests/test_perturbation_diagnostics.py tests/test_perturbations.py -v`
- result: `12 passed`

Artifact generation:
- `uv run python dataset_builder/perturbation_diagnostics.py --input data/interim/hermes_normalized_phase2.jsonl --output data/processed/perturbation_diagnostics.json`

## Main judgment

This was the right next slice.

It adds a reusable measurement tool, creates a durable processed-data artifact, and gives the project a quantitative basis for deciding which perturbation rules need work next.

## Sources
- `dataset_builder/perturbation_diagnostics.py`
- `tests/test_perturbation_diagnostics.py`
- `data/processed/perturbation_diagnostics.json`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
