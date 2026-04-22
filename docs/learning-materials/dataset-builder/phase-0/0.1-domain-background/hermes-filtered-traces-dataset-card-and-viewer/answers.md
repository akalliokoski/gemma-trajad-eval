# Hermes filtered traces dataset card and viewer

Source topic: Phase 0 → Orientation → 0.1 Domain background → third topic in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## Questions and answers

### 1) How long are typical trajectories in the Hermes filtered traces dataset?
Typical trajectories are long multi-step agent traces, not short chat snippets.

The Hugging Face dataset card reports an average of 32.1 messages per conversation. A full raw-data scan of `train.jsonl` lines up with that: the average is about 32.09 messages, the median is 31, the minimum is 5, and the maximum is 54.

That means a "typical" trace in this dataset is roughly a 30-message execution, which is long enough to contain planning, repeated tool use, tool responses, and a final synthesis step. This matters because later anomaly-detection work has to reason over whole execution traces, not just isolated turns.

### 2) What roles appear in the `conversations` field?
The `conversations` field uses four raw role labels:

1. `system`
2. `human`
3. `gpt`
4. `tool`

In other words, the dataset stores the full agent loop: system setup, user request, assistant/tool-calling behavior, and tool outputs.

A practical implication for this repo is that `normalize_trajectory.py` has to map these raw labels into the normalized format used downstream. In particular, `human` corresponds to the user role and `gpt` corresponds to the assistant role.

### 3) How common are tool calls?
Tool use is extremely common in this filtered dataset. In practice, it is effectively universal.

The dataset card says there are 18.5 tool calls per conversation on average. A raw scan that counts `<tool_call>` blocks inside assistant messages finds about 20.47 tool calls per trace on average, with a median of 18. The same scan finds about 19.47 `<tool_response>` blocks per trace.

So the important takeaway is not the exact decimal place. The real takeaway is that this dataset is densely tool-driven. Tool use is not an occasional side feature here; it is the dominant structural pattern of the trajectories.

### 4) What does the `conversations` field structure look like? Is it ShareGPT format or OpenAI chat format?
It is much closer to ShareGPT-style storage than to native OpenAI chat format.

Each record contains a `conversations` array, and each item is a simple object with fields like:
- `from`
- `value`

That is the core ShareGPT-style pattern: the message role is stored as a simple label, and the content is stored as one big text field.

But this dataset also embeds a tool protocol inside those text fields:
- assistant (`gpt`) turns often contain `<tool_call> ... </tool_call>` blocks
- tool turns contain `<tool_response> ... </tool_response>` blocks
- the top-level `tools` field stores tool definitions as a JSON string

So it is not native OpenAI chat format, because native OpenAI tool-calling would normally use structured fields like `role`, `content`, `tool_calls`, and separate tool messages with explicit `tool_call_id` wiring.

The right mental model is: this dataset is ShareGPT-like outer structure plus serialized tool-calling markup inside message text.

### 5) Why does this matter for `dataset_builder/`?
It matters for three reasons.

1. The traces are long enough that anomaly detection has to model full execution flow, not only the final answer.
2. The role set and tool-heavy structure explain why many perturbation rules in this repo focus on assistant/tool-call pairs rather than plain chat-only mistakes.
3. Because tool calls are serialized inside text rather than stored in fully structured OpenAI objects, downstream code has to parse or normalize the trajectory carefully before applying perturbations or validation.

## Key takeaway for this project
The Hermes filtered traces dataset is a strongly tool-centric corpus of long agent trajectories. The `conversations` field is best understood as ShareGPT-style `{from, value}` storage wrapped around serialized tool-calling markup. That makes it a good fit for trajectory anomaly work, but it also means the repo's normalization and perturbation logic must treat message structure carefully.

## Sources
- Dataset page: https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered
- Dataset card / README: https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered/blob/main/README.md
- Hugging Face dataset API: https://huggingface.co/api/datasets/DJLougen/hermes-agent-traces-filtered
- Dataset server first rows: https://datasets-server.huggingface.co/first-rows?dataset=DJLougen%2Fhermes-agent-traces-filtered&config=default&split=train
- Raw JSONL analyzed: https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered/resolve/main/data/train.jsonl
