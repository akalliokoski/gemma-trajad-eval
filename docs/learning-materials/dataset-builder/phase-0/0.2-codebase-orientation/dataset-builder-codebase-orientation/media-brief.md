# Media brief: dataset builder codebase orientation

Use this brief to generate an infographic and podcast for Phase 0.2 codebase orientation of the `dataset_builder/` pipeline.

## Audience
A technically curious learner who wants to understand this repo by reading code, not just by running commands.

## Target understanding
By the end, the learner should understand:
1. how the dataset-builder files divide responsibilities
2. how raw data moves from Hugging Face download to normalized records to labeled dataset splits
3. why `source_trace_id`, split grouping, and rule-aware validation matter
4. where the current code is intentionally small versus where it is still incomplete

## Core facts to preserve
- `download_hermes.py` downloads remote HF data into local JSONL under `data/raw/`.
- `inspect_traces.py` is the microscope: it analyzes raw or normalized trajectories using plain Python dict/list objects.
- `normalize_trajectory.py` is the schema bridge from ShareGPT-like `{from, value}` messages to `{role, content}` trajectories.
- `source_trace_id` is a stable identity used for leakage-safe split assignment.
- `perturbations.py` applies surgical mutations inside serialized `<tool_call>` blocks and maps anomaly types to anomaly classes.
- `build_trajad_dataset.py` orchestrates perturbation, coherence screening, split assignment, and build-manifest generation.
- `validate_labels.py` checks structural correctness and some rule-aware localization semantics, but not full semantic realism.
- Valid-but-unimplemented anomaly types currently include `hallucinated_tool`, `invalid_tool_json`, and `unnecessary_replanning`.

## Repo-specific framing
Frame this as a code-reading map for a script-first home-lab repository:
- keep the files small
- understand the contracts between files
- focus on data movement and labeling semantics, not abstract architecture patterns

## Suggested tone
- precise
- educational
- practical
- anti-hype

## Source files
- `answers.md`
- `README.md`
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `podcast-transcript.json`
- `podcast-transcript.txt`

## Sources
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `dataset_builder/download_hermes.py`
- `dataset_builder/inspect_traces.py`
- `dataset_builder/normalize_trajectory.py`
- `dataset_builder/perturbations.py`
- `dataset_builder/build_trajad_dataset.py`
- `dataset_builder/validate_labels.py`
- `docs/codebase-baseline.md`
- `docs/data-pipeline-walkthrough.md`
