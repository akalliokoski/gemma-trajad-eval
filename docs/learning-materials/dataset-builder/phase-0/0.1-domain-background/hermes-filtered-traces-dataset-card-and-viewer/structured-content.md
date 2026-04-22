# Hermes filtered traces dataset card and viewer

## Overview
This infographic explains what the Hermes filtered traces dataset looks like when you inspect the Hugging Face dataset card and viewer. It combines dataset scale, trajectory length, role structure, tool-call density, format comparison, and repo-specific implications in one technical learning asset.

## Learning Objectives
The viewer will understand:
1. that typical trajectories in the filtered Hermes dataset are roughly 32-message agent traces with dense tool use
2. that the raw roles are `system`, `human`, `gpt`, and `tool`
3. that the `conversations` field is ShareGPT-like `{from, value}` storage with serialized tool-calling markup, which matters directly to `dataset_builder/`

---

## Section 1: Dataset snapshot

**Key Concept**: The filtered Hermes dataset is a moderate-size corpus of long, tool-rich agent trajectories.

**Content**:
- 3,679 rows
- 32.1 messages per conversation
- about 32.09 messages
- median 31
- min 5
- max 54
- That means a typical trace is roughly a 30-message execution rather than a short chat snippet.

**Visual Element**:
- Type: number highlight
- Subject: dataset size and trajectory-length summary panel
- Treatment: large metric cards with compact distribution callouts

**Text Labels**:
- Headline: "Dataset snapshot"
- Subhead: "Scale and typical trajectory length"
- Labels: "3,679 rows", "32.1 messages per conversation", "median 31", "min 5", "max 54"

---

## Section 2: Raw role inventory

**Key Concept**: The `conversations` field captures the full agent loop with four raw roles.

**Content**:
- system
- human
- gpt
- tool
- In other words, the dataset stores system setup, user request, assistant/tool-calling behavior, and tool outputs.

**Visual Element**:
- Type: diagram
- Subject: four-role loop or stacked role inventory
- Treatment: compact role chips connected in a cyclic flow

**Text Labels**:
- Headline: "Four raw roles"
- Subhead: "What appears in `conversations`"
- Labels: "system", "human", "gpt", "tool"

---

## Section 3: Tool calls are the dominant pattern

**Key Concept**: Tool use is not occasional in this corpus; it is the main structural pattern.

**Content**:
- 18.5 tool calls per conversation
- about 20.47 `<tool_call>` blocks per trace
- about 19.47 `<tool_response>` blocks per trace
- Tool use is extremely common and effectively universal in this filtered corpus.

**Visual Element**:
- Type: metrics panel
- Subject: tool-call and tool-response density card
- Treatment: highlighted counts with arrows between assistant and tool turns

**Text Labels**:
- Headline: "Tool calls dominate"
- Subhead: "This is a tool-centric trajectory dataset"
- Labels: "18.5 avg tool calls", "20.47 `<tool_call>`", "19.47 `<tool_response>`"

---

## Section 4: What the `conversations` field looks like

**Key Concept**: The outer storage format is ShareGPT-like `{from, value}` rather than native OpenAI tool-call objects.

**Content**:
- The `conversations` field is a list of `{from, value}` objects.
- assistant (`gpt`) turns often contain `<tool_call> ... </tool_call>` blocks.
- tool turns contain `<tool_response> ... </tool_response>` blocks.
- the top-level `tools` field stores tool definitions as a JSON string.

**Visual Element**:
- Type: structural breakdown
- Subject: one sample record broken into outer fields and embedded tool markup
- Treatment: boxed JSON-like frame with highlighted embedded tags

**Text Labels**:
- Headline: "ShareGPT-style outer format"
- Subhead: "Tool protocol is embedded inside text"
- Labels: "{from, value}", "<tool_call>", "<tool_response>", "tools JSON string"

---

## Section 5: ShareGPT-style vs OpenAI-style

**Key Concept**: The dataset is easier to think of as ShareGPT-style storage with serialized tool markup than as native OpenAI chat format.

**Content**:
| Aspect | This dataset | Native OpenAI chat |
|--------|--------------|--------------------|
| Outer message structure | `{from, value}` | `role`, `content` |
| Tool calls | serialized inside text | structured `tool_calls` objects |
| Tool responses | serialized inside text | separate structured tool messages |
| Practical implication | parser/normalizer must recover structure from strings | structure already explicit |

**Visual Element**:
- Type: split comparison
- Subject: side-by-side format comparison cards
- Treatment: left-right comparison with highlighted structural differences

**Text Labels**:
- Headline: "Not native OpenAI chat format"
- Subhead: "Think ShareGPT-style storage plus embedded tool markup"
- Labels: "This dataset", "Native OpenAI chat", "serialized inside text", "structured objects"

---

## Section 6: Why this matters to `dataset_builder/`

**Key Concept**: Dataset structure directly shapes the repo's normalization, perturbation, and validation logic.

**Content**:
- long trajectories make anomaly detection a whole-trace problem
- the role set explains what normalization must map
- dense tool use explains why many perturbation rules target assistant/tool-call pairs
- serialized tool protocol means downstream code must parse structure out of text

**Visual Element**:
- Type: quick reference
- Subject: repo takeaway checklist tied to normalization and perturbation
- Treatment: boxed takeaway module with four action-oriented implications

**Text Labels**:
- Headline: "Dataset-builder takeaway"
- Subhead: "Structure drives the pipeline design"
- Labels: "whole-trace reasoning", "role mapping", "tool-call perturbations", "parse structure from text"

---

## Data Points (Verbatim)

All statistics, numbers, and quotes exactly as they appear in source:

### Statistics
- "3,679 rows"
- "32.1 messages per conversation"
- "18.5 tool calls per conversation"
- "about 32.09 messages"
- "median 31"
- "min 5"
- "max 54"
- "about 20.47 `<tool_call>` blocks per trace"
- "about 19.47 `<tool_response>` blocks per trace"

### Key Terms
- **system**: "system"
- **human**: "human"
- **gpt**: "gpt"
- **tool**: "tool"
- **conversations**: "The `conversations` field is a list of `{from, value}` objects."

---

## Design Instructions

Extracted from user's steering prompt:

### Style Preferences
- Educational, technical, and clear
- Fit dataset metrics plus format-comparison content
- Treat `infographic.png` as the primary infographic artifact

### Layout Preferences
- Use a layout that can hold metrics, role structure, and format comparison in one view
- Prefer a technical modular structure over a single chart

### Other Requirements
- Do not edit the learning plan document
- Save the generation prompt at `prompts/infographic.md`
