Create a professional infographic following these specifications:

## Image Specifications

- **Type**: Infographic
- **Layout**: dense-modules
- **Style**: pop-laboratory
- **Aspect Ratio**: 9:16
- **Language**: en

## Core Principles

- Follow the layout structure precisely for information architecture
- Apply style aesthetics consistently throughout
- Keep information concise, diagrammatic, and highly legible
- Use ample whitespace and strong section boundaries
- Maintain clear visual hierarchy
- No garbled text, no misspellings, no tiny dense paragraphs
- Prefer large readable headings, metric chips, and short labels over long body copy

## Layout Guidelines

Use a dense-modules layout for a technical learning debrief. Organize the canvas into eight compact but clearly separated modules: local download evidence, raw schema, long-trace metrics, tool-density metrics, top task categories, serialized tool-call examples, perturbation eligibility snapshot, and the final stop-line / next-step takeaway. Keep each module visually self-contained with clear titles, short supporting text, and technical callout chips.

## Style Guidelines

Use pop-laboratory style: blueprint-grid energy, precise labels, educational lab aesthetic, bright but controlled accent colors, modular cards, technical diagram cues, and clean scientific-poster readability. Avoid clutter, visual noise, and decorative flourishes that reduce legibility.

---

Generate the infographic based on the content below:

Title: Hermes filtered traces Phase 1 understanding

Main message:
Phase 1 proves that the filtered Hermes dataset is a real local, long-form, tool-centric execution-trace corpus. The most important lesson is that the structure is serialized inside text, which is why normalization is essential and why the correct next step is Phase 2 normalization study rather than premature training.

Module 1 — Local evidence
- 3,679 rows
- about 368 MB
- data/raw/hermes_filtered.jsonl
- Download succeeded on the VPS

Module 2 — Raw schema
- top-level fields: id, conversations, tools, category, subcategory, task
- raw message shape: {from, value}
- raw roles: system, human, gpt, tool

Module 3 — Long execution traces
- average trajectory length about 32.1
- min 5
- max 54
- gpt: 56,376
- tool: 53,191
- human: 4,797
- system: 3,679

Module 4 — Tool use dominates
- 100.0% with at least one tool call
- 99.4% with at least two assistant/tool-call pairs
- 56,870 tool-call markers
- 56,378 think markers

Module 5 — The tasks are operational
- top categories: Repository Tasks, Agent Tools, Terminal & Coding, Browser Automation, Multi-Tool
- representative task types: recover configs, create endpoints, continue project work, start services, work through todo-driven implementation

Module 6 — Serialized tool protocol
- assistant messages contain <tool_call> ... </tool_call>
- tool messages contain <tool_response> ... </tool_response>
- example tool call: {"name": "session_search", "arguments": {"query": "staging deployment config"}}
- key lesson: semantics are stored inside strings, not native tool objects

Module 7 — Perturbation eligibility
- P1: 3679/3679
- P2: 3678/3679
- P3/P4/P5: 3679/3679
- P8: 3658/3679
- insight: eligibility is broad; realism is the real challenge

Module 8 — Stop line and next step
- three core lessons: agentic corpus, tool-centric corpus, serialized structure
- next step: Phase 2 normalization deep dive
- not yet: training

Text labels (in en):
Hermes filtered traces Phase 1 understanding
real local file
raw schema
{from, value}
system
human
gpt
tool
32.1 avg messages
100.0% with tool calls
99.4% with 2+ tool pairs
serialized tool protocol
<tool_call>
<tool_response>
eligibility is not the bottleneck
realism is the harder problem
next: Phase 2 normalization
not yet training
