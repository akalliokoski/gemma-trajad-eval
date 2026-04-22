---
title: Hermes filtered traces dataset structure
created: 2026-04-22
updated: 2026-04-22
type: query
tags: [dataset, data, trajectory-analysis, documentation]
sources: [raw/transcripts/phase-0-domain-background-hermes-filtered-traces-2026-04-22.md]
---

# Hermes filtered traces dataset structure

This note records the durable answer from the Phase 0.1 domain-background task about the Hugging Face dataset `DJLougen/hermes-agent-traces-filtered`.

## Short answer
The dataset is a tool-centric corpus of long [[hermes-agent]] trajectories. Typical examples are about 32 messages long, use the raw roles `system`, `human`, `gpt`, and `tool`, and store tool protocol inside text rather than as fully structured OpenAI tool-call objects. That makes it directly relevant to [[hermes-first-development]] and later `dataset_builder/` normalization work.

## Durable observations
- Scale: 3,679 rows in one train split.
- Typical trajectory length: the card reports 32.1 messages per conversation; a raw scan comes out to about 32.09 average, median 31, min 5, max 54.
- Raw roles: `system`, `human`, `gpt`, `tool`.
- Tool density: the card reports 18.5 tool calls per conversation; a raw scan finds about 20.47 `<tool_call>` blocks and 19.47 `<tool_response>` blocks per trace.
- Format: `conversations` is a ShareGPT-style list of `{from, value}` objects, with serialized `<tool_call>` and `<tool_response>` markup inside message text.

## Why it matters in this repo
- Long trajectories make anomaly detection a whole-trace problem instead of a final-answer-only problem.
- The raw roles explain what `normalize_trajectory.py` has to map into the repo's normalized schema.
- Dense tool use explains why many perturbation rules target assistant/tool-call pairs rather than plain chat-only failures.
- Serialized tool structure means downstream code must parse message text carefully before validation, perturbation, and labeling.

## Practical takeaway
When working on `dataset_builder/`, think of this dataset as:
1. long execution traces
2. dense tool usage
3. ShareGPT-style outer storage
4. OpenAI-like tool semantics serialized inside strings

That combination is exactly why normalization logic is not optional plumbing; it is what turns raw trajectory text into something the rest of the pipeline can reason over reliably.
