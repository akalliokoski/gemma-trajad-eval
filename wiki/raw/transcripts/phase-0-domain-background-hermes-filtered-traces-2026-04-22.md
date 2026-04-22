# Phase 0.1 domain background — Hermes filtered traces dataset card and viewer

Captured: 2026-04-22
Type: raw research snapshot

## Prompt focus
Browse the Hermes filtered traces Hugging Face dataset card and viewer to answer:
- how long typical trajectories are
- what roles appear
- how common tool calls are
- whether the format is closer to ShareGPT or native OpenAI chat format

## Findings
- Dataset size: 3,679 rows in one train split.
- Dataset card claim: 32.1 messages per conversation.
- Raw scan summary: about 32.09 messages average, median 31, min 5, max 54.
- Raw roles: `system`, `human`, `gpt`, `tool`.
- Dataset card claim: 18.5 tool calls per conversation.
- Raw scan summary: about 20.47 `<tool_call>` blocks and 19.47 `<tool_response>` blocks per trace.
- Format conclusion: `conversations` is closer to ShareGPT-style `{from, value}` storage, with serialized `<tool_call>` and `<tool_response>` markup embedded in text rather than native OpenAI `role/content/tool_calls` objects.

## External sources
- https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered
- https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered/blob/main/README.md
- https://huggingface.co/api/datasets/DJLougen/hermes-agent-traces-filtered
- https://datasets-server.huggingface.co/first-rows?dataset=DJLougen%2Fhermes-agent-traces-filtered&config=default&split=train
- https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered/resolve/main/data/train.jsonl
