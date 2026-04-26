# Raw transcript notes — dataset-builder Phase 2 normalization deep dive

Date: 2026-04-26
Source type: implementation / learning-path debrief

## What was done
- read the Phase 2 normalization tasks from the dataset-builder learning plan
- inspected `dataset_builder/normalize_trajectory.py`
- ran:
  - `uv run python dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized_phase2.jsonl`
- verified result:
  - `3,679` normalized records
  - `0` errors
- ran:
  - `uv run pytest tests/test_normalize_trajectory.py -v`
- verified result:
  - `2 passed`
- created compact learning artifacts:
  - `raw-vs-normalized-sample.json`
  - `normalization-stability-and-edge-cases.json`
- created a combined Phase 2.1–2.2 learning package with answers, infographic, and podcast
- updated the learning plan to mark the normalization and edge-case tasks complete

## Main findings
- normalization preserves row count on the real corpus
- raw message shape is `{from, value}` and normalized message shape is `{role, content}`
- raw roles observed: `gpt`, `human`, `system`, `tool`
- normalized roles observed: `assistant`, `user`, `system`, `tool`
- normalized clean records carry:
  - `is_anomalous=false`
  - `anomaly_type=null`
  - `bad_step=null`
  - `generation_rule=null`
- normalized metadata includes:
  - `category`
  - `subcategory`
  - `trajectory_length`
  - `tool_call_count`
  - `tool_response_count`
  - `has_think`
- `source_trace_id` remained stable on repeated checks
- this matters because later split assignment depends on stable trace-family identity
- the current filtered corpus did not show stressful missing-role or missing-metadata cases:
  - `missing_category_count: 0`
  - `missing_subcategory_count: 0`
  - `empty_metadata_count: 0`

## Important interpretation
Normalization is not mere format cleanup. It is the schema bridge and identity-preservation step that makes later perturbation, validation, and leakage-safe splitting trustworthy.

## Artifact package
- `docs/learning-materials/dataset-builder/phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/README.md`
- `docs/learning-materials/dataset-builder/phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/answers.md`
- `docs/learning-materials/dataset-builder/phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/infographic.png`
- `docs/learning-materials/dataset-builder/phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/raw-vs-normalized-sample.json`
- `docs/learning-materials/dataset-builder/phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/normalization-stability-and-edge-cases.json`
- `/data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-2-understanding/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/phase-2_2.1-2.2-01_hermes-normalization-deep-dive.mp3`
