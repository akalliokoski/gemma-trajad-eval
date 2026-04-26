# Hermes normalization deep dive

Source topic: Phase 2 → Normalization Deep Dive → 2.1 Run normalization and verify output + 2.2 Edge cases in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## What this artifact covers

This package combines the normalization run, side-by-side raw-versus-normalized inspection, source-trace stability reasoning, and edge-case checks into one coherent learning slice.

## Questions and answers

### 1) Did normalization run successfully on the real raw corpus?
Yes. Running:

```bash
uv run python dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized_phase2.jsonl
```

produced:

- `3,679` normalized records
- output file: `data/interim/hermes_normalized_phase2.jsonl`
- `0` errors

So the first Phase 2 verification result is strong: row count was preserved and the script did not have to skip bad records.

### 2) What changes between the raw record and the normalized record?
The side-by-side sample in `raw-vs-normalized-sample.json` shows the core transformation clearly.

Raw record shape:
- top-level fields include `id`, `conversations`, `tools`, `category`, `subcategory`, and `task`
- messages are stored as `{from, value}`
- raw roles use `system`, `human`, `gpt`, and `tool`

Normalized record shape:
- `id` becomes a builder-side variant id such as `trace_000000_var_00`
- `source_trace_id` preserves the original trace identity
- `trajectory` becomes a list of `{role, content}` objects
- raw roles become normalized roles:
  - `human` -> `user`
  - `gpt` -> `assistant`
  - `system` -> `system`
  - `tool` -> `tool`
- label fields are initialized as clean defaults:
  - `is_anomalous=false`
  - `anomaly_type=null`
  - `bad_step=null`
  - `generation_rule=null`

This is the key conceptual move in the pipeline: raw agent traces stop being a dataset-card-shaped artifact and become a builder-shaped artifact.

### 3) What metadata gets attached during normalization?
The sample normalized record shows `metadata` containing both source metadata and derived structural metadata.

Observed keys include:
- `category`
- `subcategory`
- `trajectory_length`
- `tool_call_count`
- `tool_response_count`
- `has_think`

That is an elegant design choice because the trajectory object stays simple while cheap structural signals move into metadata where later diagnostics and filtering can use them.

### 4) Does normalization preserve row count and basic trajectory statistics?
Yes.

The normalized corpus still has `3,679` records, and the derived `trajectory_length` statistics line up with the raw inspection pass:
- min `5`
- max `54`
- average `32.09`

So normalization is not silently dropping or reshaping records in a way that changes the dataset scale.

### 5) Why is `source_trace_id` so important?
`source_trace_id` is the stable identity of the underlying clean trace family.

In the current code:
- if the raw record already has `id` or `source_id`, that value becomes `source_trace_id`
- otherwise the code falls back to a deterministic SHA-256 hash of the raw trajectory content

That matters because later split assignment is done by trace family, not by individual variant row. If `source_trace_id` changed between runs, the same logical trace could land in a different split on a rebuild, which would make train/dev/test membership unstable and could create leakage across clean and anomalous variants.

### 6) Did the stability check actually hold in practice?
Yes.

The stability check in `normalization-stability-and-edge-cases.json` recomputed `source_trace_id` for multiple records and confirmed:
- `stable_on_repeat: true`

The checked records kept the same IDs across repeated normalization of the same raw inputs.

That means the normalization logic is behaving deterministically on the real corpus, not just in theory.

### 7) Were there any non-standard role names or role fallthroughs?
No.

The raw role inventory observed in the corpus is exactly:
- `gpt`
- `human`
- `system`
- `tool`

The normalized role inventory is exactly:
- `assistant`
- `user`
- `system`
- `tool`

So for the current raw file, `normalize_role()` covers the observed role space cleanly and does not appear to hit an unknown-role fallback path.

### 8) Did metadata extraction encounter missing-category edge cases?
Not in this corpus snapshot.

The edge-case scan found:
- `missing_category_count: 0`
- `missing_subcategory_count: 0`
- `empty_metadata_count: 0`

So the current filtered Hermes dataset is cleaner than the plan’s hypothetical edge case suggested.

That does not make the edge-case question pointless, though. It tells us something useful: the code’s graceful extraction path exists, but this particular corpus does not currently stress it very hard.

### 9) What is the most important practical takeaway from Phase 2?
Normalization is the schema bridge that makes the rest of the project possible.

The most important lessons are:
1. the builder keeps the trajectory representation intentionally simple
2. role names become consistent and model-friendly
3. source identity stays stable for leakage-safe splitting
4. useful structural signals are added without redesigning the message schema

That means normalization is not just "format cleanup." It is the point where the project turns messy serialized raw traces into a trustworthy substrate for perturbation, validation, and later learning.

## Suggested next study step
When the learning path resumes, the right next move is Phase 3 perturbation-engine study: read the anomaly rules one by one now that the normalized trajectory contract is clear.
