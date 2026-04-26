# Media brief: Hermes filtered traces Phase 1 understanding

Use this brief to generate an infographic and podcast for the combined Phase 1.1–1.3 stop-line topic in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`.

## Audience
A technically curious learner who wants to understand what the dataset-builder project is actually operating on before moving deeper into normalization, perturbations, or training.

## Target understanding
By the end, the learner should understand:
1. that the filtered Hermes dataset is real local evidence, not just a paper or dataset-card abstraction
2. that typical records are long, tool-rich agent trajectories rather than simple chat pairs
3. that raw messages use ShareGPT-style `{from, value}` storage with serialized `<tool_call>` / `<tool_response>` markup
4. that this raw structure directly explains why `normalize_trajectory.py`, tool-pair perturbations, and schema-aware validation exist
5. that Phase 1 should end with stronger dataset understanding, not an early jump into training

## Core facts to preserve
- The download command wrote `data/raw/hermes_filtered.jsonl` with `3,679` rows.
- The raw file is about `368 MB`.
- Stable top-level fields are `id`, `conversations`, `tools`, `category`, `subcategory`, and `task`.
- Raw messages are stored as `{from, value}` objects.
- Raw roles are `system`, `human`, `gpt`, and `tool`.
- Average trajectory length is about `32.1` messages, with min `5` and max `54`.
- `100.0%` of traces have at least one tool call.
- `99.4%` of traces have at least two assistant/tool-call pairs.
- The corpus is dominated by practical agent-work categories such as `Repository Tasks`, `Agent Tools`, and `Terminal & Coding`.
- Tool calls and tool responses are serialized inside message text rather than stored as native structured OpenAI objects.

## Repo-specific framing
Hammer home these three ideas:
- **agentic corpus**: the traces are already long, real execution loops
- **tool-centric corpus**: perturbation rules target the real action because tool use is nearly universal
- **serialized structure**: normalization is essential because structure must be recovered from strings before downstream logic can trust it

## Suggested podcast angle
Avoid boilerplate walk-through energy. Make the episode feel like a debrief after doing the work:
- what changed after looking at the real data instead of assumptions
- which facts most strongly constrain later pipeline design
- why the project should stop after Phase 1 understanding rather than pretending to be ready for training just because the data exists

## Suggested tone
- concrete and grounded
- more “what we learned by actually opening the file” than “chapter recap”
- emphasize the few important ideas repeatedly, but from different angles
- no hype and no repetitive filler

## Source files
- `answers.md`
- `sample-record.json`
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `podcast-transcript.json`
- `podcast-transcript.txt`
- `infographic.png`

## Verification facts to mention accurately
- download command succeeded locally on the VPS
- inspection command succeeded against the real raw file
- the next suggested learning step is Phase 2 normalization, not training
