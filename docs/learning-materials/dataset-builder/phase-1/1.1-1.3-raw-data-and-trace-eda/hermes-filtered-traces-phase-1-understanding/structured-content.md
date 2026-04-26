# Hermes filtered traces Phase 1 understanding

## Overview
This infographic explains what was learned by actually downloading and inspecting the filtered Hermes traces locally during Phase 1. It combines raw-data verification, schema shape, EDA metrics, sample task patterns, serialized tool-call structure, perturbation eligibility, and the most important repo-level implications.

## Learning Objectives
The viewer will understand:
1. that the dataset is a long-form, tool-centric execution-trace corpus
2. that the raw structure is ShareGPT-style `{from, value}` plus serialized tool-call markup
3. that these facts justify stopping after Phase 1 understanding and studying normalization next instead of jumping to training

---

## Section 1: Local evidence, not theory

**Key Concept**: Phase 1 established a real local artifact and concrete evidence base.

**Content**:
- `uv run python dataset_builder/download_hermes.py --dataset filtered`
- `data/raw/hermes_filtered.jsonl`
- `3,679`
- about `368 MB`
- Phase 1 starts from local raw data, not just a dataset card.

**Visual Element**:
- Type: number highlight
- Subject: local download and file artifact panel
- Treatment: large metric card plus command chip and file path chip

**Text Labels**:
- Headline: "Phase 1 starts with a real local file"
- Subhead: "Download succeeded on the VPS"
- Labels: "3,679 rows", "about 368 MB", "data/raw/hermes_filtered.jsonl"

---

## Section 2: Raw schema shape

**Key Concept**: A raw record contains more than just chat messages and uses ShareGPT-style message objects.

**Content**:
- `id`
- `conversations`
- `tools`
- `category`
- `subcategory`
- `task`
- `{from, value}`

**Visual Element**:
- Type: structural breakdown
- Subject: compact record anatomy panel
- Treatment: boxed top-level fields with a highlighted message-shape chip

**Text Labels**:
- Headline: "Raw record anatomy"
- Subhead: "Top-level fields and message shape"
- Labels: "id", "conversations", "tools", "category", "subcategory", "task", "{from, value}"

---

## Section 3: This is a long execution-trace corpus

**Key Concept**: Typical records are full multi-step traces, not tiny Q/A pairs.

**Content**:
- average trajectory length about `32.1`
- min `5`
- max `54`
- role counts across all messages:
  - `gpt`: `56,376`
  - `tool`: `53,191`
  - `human`: `4,797`
  - `system`: `3,679`

**Visual Element**:
- Type: metrics panel
- Subject: trajectory-length and role-density summary
- Treatment: large average metric with supporting role bars or chips

**Text Labels**:
- Headline: "Not a simple chat dataset"
- Subhead: "Typical traces are about 32 messages long"
- Labels: "32.1 avg", "min 5", "max 54", "gpt", "tool", "human", "system"

---

## Section 4: Tool use is basically universal

**Key Concept**: Tool interaction is the center of gravity of the corpus.

**Content**:
- traces with `>=1` tool call: `100.0%`
- traces with `>=2` assistant/tool-call pairs: `99.4%`
- messages with `<tool_call>`: `56,870`
- messages with `<think>`: `56,378`

**Visual Element**:
- Type: number highlight
- Subject: tool-density and reasoning-density panel
- Treatment: bold percentage cards with callout counts underneath

**Text Labels**:
- Headline: "Tool-centric by construction"
- Subhead: "Tool use is not an edge case here"
- Labels: "100.0% with tool calls", "99.4% with 2+ tool pairs", "56,870 tool-call markers", "56,378 think markers"

---

## Section 5: What the traces are actually about

**Key Concept**: The corpus clusters around practical agent work rather than generic chatting.

**Content**:
- `Repository Tasks`
- `Agent Tools`
- `Terminal & Coding`
- `Browser Automation`
- `Multi-Tool`
- representative tasks include recovering configs, creating endpoints, continuing project work, starting services, and tracking todo-driven implementation work

**Visual Element**:
- Type: categorized modules
- Subject: top categories plus a short sample-task strip
- Treatment: category cards and compact example prompts

**Text Labels**:
- Headline: "The tasks are operational and agentic"
- Subhead: "This is practical work, not small-talk data"
- Labels: "Repository Tasks", "Agent Tools", "Terminal & Coding", "Browser Automation", "Multi-Tool"

---

## Section 6: Tool calls are serialized inside text

**Key Concept**: The tool protocol exists, but it is embedded inside strings rather than stored as native structured tool-call objects.

**Content**:
- `<tool_call>`
- `<tool_response>`
- `{"name": "session_search", "arguments": {"query": "staging deployment config"}}`
- `{"tool_call_id": "functions.session_search:0", "name": "session_search", "content": {"success": false, "error": "Session database not available."}}`

**Visual Element**:
- Type: comparison / code example panel
- Subject: assistant-side tool call and tool-side response example boxes
- Treatment: two stacked code-like cards with highlighted wrapper tags

**Text Labels**:
- Headline: "The structure is serialized, not native"
- Subhead: "Meaning matters are packed into strings"
- Labels: "<tool_call>", "<tool_response>", "assistant message text", "tool message text"

---

## Section 7: Why perturbation rules are broadly applicable

**Key Concept**: Most of the perturbation families are eligible on almost the whole corpus.

**Content**:
- `P1 wrong_tool_choice`: `3679/3679` in the inspector report
- `P2 bad_tool_arguments`: `3678/3679`
- `P3/P4/P5`: `3679/3679`
- `P8`: `3658/3679`
- The real bottleneck is anomaly realism, not lack of tool structure.

**Visual Element**:
- Type: table / metric strip
- Subject: eligibility snapshot by rule family
- Treatment: four compact rule cards with a final insight callout

**Text Labels**:
- Headline: "Eligibility is not the bottleneck"
- Subhead: "Realism is the harder problem"
- Labels: "P1", "P2", "P3/P4/P5", "P8"

---

## Section 8: Stop line and next step

**Key Concept**: The right next move is Phase 2 normalization study, not premature training work.

**Content**:
- the corpus is already agentic
- the corpus is structurally tool-heavy
- the structure is serialized, not native
- next study step: compare raw `{from, value}` traces to normalized `{role, content}` trajectories and study `source_trace_id`

**Visual Element**:
- Type: takeaway module
- Subject: three core lessons plus one next-step arrow
- Treatment: bold conclusion card with a single forward pointer

**Text Labels**:
- Headline: "What Phase 1 really taught"
- Subhead: "Understand the data, then study normalization"
- Labels: "agentic corpus", "tool-centric corpus", "serialized structure", "next: Phase 2 normalization"

---

## Data Points (Verbatim)

### Statistics
- "3,679"
- "about 368 MB"
- "32.1"
- "5"
- "54"
- "100.0%"
- "99.4%"
- "56,870"
- "56,378"
- "3679/3679"
- "3678/3679"
- "3658/3679"

### Key Terms
- **message shape**: "{from, value}"
- **roles**: "system", "human", "gpt", "tool"
- **markup**: "<tool_call>", "<tool_response>"

---

## Design Instructions

### Style Preferences
- Technical and educational
- High-signal, not generic or fluffy
- Make the asset feel like a debrief from real inspection work

### Layout Preferences
- Use a dense modular layout that can fit metrics, schema, examples, and takeaways together
- Prioritize readability of headings and key labels over dense paragraph text

### Other Requirements
- `infographic.png` must be the image-generated canonical artifact
- Emphasize the few most important lessons instead of repeating a boilerplate learning-plan structure
