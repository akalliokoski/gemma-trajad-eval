# Hermes filtered traces Phase 1 understanding

Source topic: Phase 1 → Data Acquisition & Exploration → 1.1 Download, 1.2 EDA with `inspect_traces.py`, and 1.3 Understand tool call structure in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## What this artifact covers

This package documents the actual stop-line work for the current pass:
1. verify the raw filtered Hermes dataset is on disk
2. inspect one real raw record
3. run empirical EDA over the full corpus
4. manually inspect representative traces
5. understand how tool calls are serialized and which perturbation rules are broadly eligible

## Questions and answers

### 1) Did the download step succeed, and what landed on disk?
Yes. Running `uv run python dataset_builder/download_hermes.py --dataset filtered` wrote:

- `data/raw/hermes_filtered.jsonl`
- row count: `3,679`
- file size: about `368 MB`

So the Phase 1 starting point is real local data, not just the dataset card.

### 2) What fields are present in a real raw record?
A pretty-printed raw record shows these stable top-level fields:

- `id`
- `conversations`
- `tools`
- `category`
- `subcategory`
- `task`

This matters because the current dataset is richer than a bare chat log. It stores both the message trace and extra task metadata, while tool definitions live in a top-level `tools` field as a serialized JSON string.

A compact preview of one record was saved to `sample-record.json`.

### 3) What does the raw message structure actually look like?
The raw messages are consistently ShareGPT-style `{from, value}` objects rather than normalized `{role, content}` objects.

The exact role names seen in the corpus are:

- `system`
- `human`
- `gpt`
- `tool`

That means `normalize_trajectory.py` is not optional cleanup. It is the schema bridge that maps real dataset roles into the internal trajectory format used later by perturbation and validation code.

### 4) What did the full EDA run show?
Using `uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --schema-report --tool-stats --eligibility-report` and the plain summary run produced the core facts:

- total records: `3,679`
- trajectory length: min `5`, max `54`, average about `32.1`
- role counts across all messages:
  - `gpt`: `56,376`
  - `tool`: `53,191`
  - `human`: `4,797`
  - `system`: `3,679`
- traces with `>=1` tool call: `100.0%`
- traces with `>=2` assistant/tool-call pairs: `99.4%`
- messages with `<tool_call>`: `56,870`
- messages with `<think>`: `56,378`

The practical conclusion is that this is not a mostly-chat corpus with occasional tool use. It is a deeply tool-centric execution-trace corpus.

### 5) What are the most common categories in the raw data?
The top categories from the inspection run were:

1. `Repository Tasks` — `1,024`
2. `Agent Tools` — `730`
3. `Terminal & Coding` — `636`
4. `Browser Automation` — `532`
5. `Multi-Tool` — `391`
6. `File Operations` — `209`
7. `Scheduling` — `116`
8. `Planning & Organization` — `39`

So even before labeling anomalies, the source corpus already clusters around practical agent work: repository operations, coding, terminals, browsers, files, and orchestration.

### 6) What do the first five complete traces look like at a human level?
A manual scan of five full traces shows the same pattern repeatedly: the user asks for multi-step agent work, the assistant plans internally with `<think>`, then executes a chain of tools before finishing.

Representative examples:

1. recover a staging deployment config from past sessions
2. save an API convention to memory and create a new GraphQL-style endpoint
3. inspect a todo list, infer project context, and continue an in-progress data-pipeline project
4. start background services and monitor them
5. track a three-item API documentation task list and work through it

What stands out is not just tool use, but *compound* tool use. The assistant often chains search, read, write, terminal, todo, and session tools inside one trace.

### 7) How are tool calls embedded inside assistant messages?
The raw dataset does **not** store native structured tool-call objects.

Instead, assistant turns contain serialized markup like:

```json
{"name": "session_search", "arguments": {"query": "staging deployment config"}}
```

inside `<tool_call> ... </tool_call>` wrappers.

Tool turns then contain serialized results like:

```json
{"tool_call_id": "functions.session_search:0", "name": "session_search", "content": {"success": false, "error": "Session database not available."}}
```

inside `<tool_response> ... </tool_response>` wrappers.

That is the most important structural observation in Phase 1. The semantics are there, but they are packed into strings. Downstream code has to recover structure by parsing text.

### 8) What does this imply for perturbation eligibility?
The empirical eligibility picture is strong:

- `P1 wrong_tool_choice`: `3679/3679` according to the inspector report, with a stricter direct parse finding `2825` traces whose observed tool names already fall into known `NEARBY_TOOLS` mappings
- `P2 bad_tool_arguments`: `3678/3679` (essentially universal)
- `P3/P4/P5` tool-interaction rules: `3679/3679`
- `P8` multi-tool-step rules: `3658/3679` from the inspector report

The main lesson is that most of the current perturbation space is well-supported by the raw data shape. The dataset is rich enough that the bottleneck is not whether tool interaction exists; it is whether the synthetic anomaly remains realistic.

### 9) What is the most important Phase 1 takeaway for the repo?
Three points matter more than everything else:

1. **The corpus is already agentic.** These are long execution traces, not toy prompt/response pairs.
2. **The corpus is structurally tool-heavy.** Tool interaction is basically universal, so tool-pair perturbations are targeting the real center of gravity.
3. **The structure is serialized, not native.** That is why normalization and validation are critical. The pipeline must recover explicit structure before it can perturb or judge trajectories reliably.

## Suggested next study step
When the learning path resumes, the right next move is Phase 2 normalization deep dive: compare raw `{from, value}` traces against normalized `{role, content}` trajectories and study how `source_trace_id` preserves split stability.
