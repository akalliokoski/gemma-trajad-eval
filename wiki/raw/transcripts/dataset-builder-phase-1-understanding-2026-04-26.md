# Raw transcript notes — dataset-builder Phase 1 understanding

Date: 2026-04-26
Source type: implementation / learning-path debrief

## What was done
- committed and pushed the Phase-1 scope-boundary docs that intentionally keep the active learning path narrowed to Phase 0 + Phase 1 understanding work
- re-ran the actual dataset download command:
  - `uv run python dataset_builder/download_hermes.py --dataset filtered`
- verified the raw filtered Hermes dataset exists locally at:
  - `data/raw/hermes_filtered.jsonl`
- inspected one real raw record and saved a compact pretty-printed preview to:
  - `docs/learning-materials/dataset-builder/phase-1/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/sample-record.json`
- ran empirical inspection commands over the real raw corpus, including:
  - `uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --schema-report --tool-stats --eligibility-report`
  - `uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --sample 5`
- created a combined Phase 1.1–1.3 learning-artifact package instead of three repetitive mini-packages
- generated a PNG infographic and a new podcast episode
- updated the learning plan to mark Phase 1.1–1.3 complete with links and concrete findings

## Main empirical findings
- raw file size is about 368 MB
- row count is 3,679
- stable top-level fields are:
  - `id`
  - `conversations`
  - `tools`
  - `category`
  - `subcategory`
  - `task`
- raw message shape is consistently ShareGPT-style `{from, value}`
- raw roles are:
  - `system`
  - `human`
  - `gpt`
  - `tool`
- average trajectory length is about 32.1 messages, with min 5 and max 54
- `100.0%` of traces have at least one tool call
- `99.4%` have at least two assistant/tool-call pairs
- top categories are repository tasks, agent tools, terminal and coding, browser automation, and multi-tool work
- tool calls are serialized inside assistant message text with `<tool_call>...</tool_call>`
- tool outputs are serialized inside tool message text with `<tool_response>...</tool_response>`
- perturbation eligibility is broad; the harder quality problem is realism, not lack of eligible tool structure

## Important interpretation
The most important Phase 1 conclusion is that the filtered Hermes corpus is already a strongly agentic, tool-centric execution-trace dataset, but its structure is serialized rather than natively exposed. That means Phase 2 normalization study is the honest next step, not premature training work.

## Artifact package
- `docs/learning-materials/dataset-builder/phase-1/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/README.md`
- `docs/learning-materials/dataset-builder/phase-1/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/answers.md`
- `docs/learning-materials/dataset-builder/phase-1/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/infographic.png`
- `docs/learning-materials/dataset-builder/phase-1/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/podcast-transcript.json`
- `/data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-1-understanding/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/phase-1_1.1-1.3-01_hermes-filtered-traces-phase-1-understanding.mp3`
