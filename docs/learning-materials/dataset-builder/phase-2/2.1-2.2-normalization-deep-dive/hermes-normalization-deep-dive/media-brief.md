# Media brief: Hermes normalization deep dive

Use this brief to generate an infographic and podcast for the combined Phase 2.1–2.2 normalization slice in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`.

## Audience
A technically curious learner who now understands the raw corpus and needs to understand exactly how the repo converts it into a stable internal dataset contract.

## Target understanding
By the end, the learner should understand:
1. that normalization preserves row count and converts the raw corpus into a cleaner internal trajectory schema
2. that role mapping from `human/gpt` to `user/assistant` is a central part of the transformation
3. that `source_trace_id` stability is essential for later split assignment and leakage prevention
4. that metadata enrichment is intentionally lightweight and useful
5. that the current corpus does not actually stress missing-role or missing-category edge cases very hard

## Core facts to preserve
- normalization wrote `3,679` records with `0` errors
- output file: `data/interim/hermes_normalized_phase2.jsonl`
- raw message shape is `{from, value}`
- normalized message shape is `{role, content}`
- raw roles are `system`, `human`, `gpt`, `tool`
- normalized roles are `system`, `user`, `assistant`, `tool`
- normalized clean-label defaults are `is_anomalous=false`, `anomaly_type=null`, `bad_step=null`, `generation_rule=null`
- metadata keys include `category`, `subcategory`, `trajectory_length`, `tool_call_count`, `tool_response_count`, `has_think`
- `source_trace_id` was stable on repeat checks
- `missing_category_count`, `missing_subcategory_count`, and `empty_metadata_count` were all `0`

## Repo-specific framing
Hammer home these ideas:
- normalization is the schema bridge for the whole project
- simple trajectory objects plus enriched metadata is a deliberate design choice
- stable `source_trace_id` is the hidden prerequisite for trustworthy splitting
- the current dataset is clean enough that some hypothetical edge cases are absent, which is itself a useful finding

## Suggested podcast angle
Make the episode feel like a code-level debrief:
- what changed when the trace crossed from raw format into internal format
- why `source_trace_id` matters more than it looks at first glance
- why a “boring” normalization script actually carries major data-quality guarantees

## Suggested tone
- technically grounded
- emphasize the hidden guarantees, not just the mechanical field mapping
- avoid boilerplate and repeat the key normalization lessons from different angles

## Source files
- `answers.md`
- `raw-vs-normalized-sample.json`
- `normalization-stability-and-edge-cases.json`
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `podcast-transcript.json`
- `podcast-transcript.txt`
- `infographic.png`
