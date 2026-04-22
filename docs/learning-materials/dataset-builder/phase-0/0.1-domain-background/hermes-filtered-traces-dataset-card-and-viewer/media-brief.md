# Media brief: Hermes filtered traces dataset card and viewer

Use this brief to generate an infographic and podcast for the third Phase 0.1 domain-background topic in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`.

## Audience
A technically curious learner working through the dataset-builder plan for the first time.

## Target understanding
By the end, the learner should understand:
1. that typical trajectories in the filtered Hermes dataset are about 32 messages long, not tiny chat snippets
2. that the raw roles are `system`, `human`, `gpt`, and `tool`
3. that tool calls are extremely common and effectively universal in this filtered corpus
4. that the `conversations` field is ShareGPT-like outer structure with serialized tool-calling markup inside message text
5. why this storage format matters for normalization, perturbation, and validation in `dataset_builder/`

## Core facts to preserve
- The dataset has 3,679 rows in one train split.
- The dataset card reports an average of 32.1 messages per conversation.
- A raw scan of `train.jsonl` gives about 32.09 messages on average, median 31, min 5, max 54.
- The raw roles are `system`, `human`, `gpt`, and `tool`.
- The dataset card reports 18.5 tool calls per conversation on average.
- A raw scan counting `<tool_call>` blocks finds about 20.47 tool calls per trace on average.
- The `conversations` field is a list of `{from, value}` objects rather than native OpenAI `role/content/tool_calls` objects.
- Tool behavior is serialized inside text with `<tool_call>` and `<tool_response>` wrappers.

## Repo-specific framing
Explain why this matters to `dataset_builder/`:
- long trajectories make first-error localization a whole-trace problem
- the role mapping explains what normalization must do
- dense tool use explains why perturbation rules often target tool-call pairs
- serialized tool protocol means downstream code must parse structure out of text

## Suggested tone
- clear and concrete
- technically grounded
- no hype
- emphasize structure, not just surface statistics

## Source files
- `answers.md`
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `podcast-transcript.json`
- `podcast-transcript.txt`
- `infographic.png` is the current prompt-driven image-generation artifact

## Sources
- Dataset page: https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered
- Dataset card / README: https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered/blob/main/README.md
- Dataset server first rows: https://datasets-server.huggingface.co/first-rows?dataset=DJLougen%2Fhermes-agent-traces-filtered&config=default&split=train
- Raw JSONL analyzed: https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered/resolve/main/data/train.jsonl
