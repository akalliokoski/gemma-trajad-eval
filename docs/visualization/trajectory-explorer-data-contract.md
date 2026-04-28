# Trajectory Explorer Data Contract

## Export entrypoint

Command:

```bash
uv run python scripts/export_trajectory_explorer_payload.py
```

Default output directory:
- `apps/trajectory_explorer/assets/`

## Output files

### `overview_payload.json`

Purpose:
- hero stats, taxonomy summary, execution topology, and reference links

Key fields:
- `generated_at`
- `project.name`
- `project.reference_visualization`
- `counts.raw_traces`
- `counts.processed_examples`
- `counts.train|dev|test`
- `anomaly_class_distribution[]`
- `taxonomy[]`
- `execution_topology[]`

### `sample_trajectories.json`

Purpose:
- compact browser-safe samples for the trajectory explorer

Key fields:
- `selected_ids.normal`
- `selected_ids.anomalous`
- `samples[]`
  - `sample_kind`
  - `id`
  - `source_trace_id`
  - `anomaly_type`
  - `anomaly_class`
  - `bad_step`
  - `window.start|end`
  - `messages[]`
    - `absolute_index`
    - `role`
    - `tool_name`
    - `has_tool_call`
    - `has_tool_response`
    - `content_excerpt`
  - `diff_hints.focus_indexes[]`
  - `source_pair.messages[]` when available

Caps:
- max 12 messages per exported sample window
- max 280 chars per message excerpt

### `training_payload.json`

Purpose:
- make the later fine-tuning path visible even before committed model-run reports exist

Key fields:
- `training_stages[]`
- `task_modes[]`
- `run_notes[]`

### `evaluation_payload.json`

Purpose:
- visualize current dataset/evaluation context

Key fields:
- `split_counts`
- `anomaly_type_distribution[]`
- `perturbation_rules[]`
- `reported_runs[]`
- `notes[]`

### `payload_bundle.js`

Purpose:
- local static viewing convenience

Contract:
- writes `window.__TRAJAD_EXPLORER_DATA__ = { overview, samples, training, evaluation }`
- allows `index.html` to work without fetching JSON over HTTP
