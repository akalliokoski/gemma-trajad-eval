---
title: "Hermes filtered traces dataset card and viewer"
topic: "educational/technical"
data_type: "dataset structure + metrics + format comparison"
complexity: "moderate"
point_count: 7
source_language: "en"
user_language: "en"
---

## Main Topic
This topic explains what the Hermes filtered traces dataset actually looks like when you inspect the Hugging Face dataset card and viewer, with special attention to trajectory length, role labels, tool-call density, and message format. It also connects those observations to why `dataset_builder/` has to normalize and perturb traces carefully.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. that typical trajectories in this dataset are roughly 32-message agent traces with many tool interactions
2. which raw roles appear and how strongly tool-centric the corpus is
3. why the `conversations` field is closer to ShareGPT-style `{from, value}` storage than native OpenAI chat format, and why that matters for this repo

## Target Audience
- **Knowledge Level**: Beginner-to-intermediate technical learner
- **Context**: Working through the dataset-builder learning plan for the first time
- **Expectations**: Understand the dataset's practical structure before reading normalization and perturbation code

## Content Type Analysis
- **Data Structure**: One dataset snapshot, one role inventory, one tool-use density block, one format-comparison block, and one repo-implications block
- **Key Relationships**: Trajectory length and tool density explain why the corpus is suitable for trajectory anomaly work; role labels feed normalization; ShareGPT-style storage plus embedded tool markup drives parser complexity
- **Visual Opportunities**: large metric callouts for 3,679 / 32.1 / 18.5, a role panel, a tool-density module, a ShareGPT-vs-OpenAI comparison module, and a repo takeaway module

## Key Data Points (Verbatim)
- "3,679 rows"
- "32.1 messages per conversation"
- "18.5 tool calls per conversation"
- "system"
- "human"
- "gpt"
- "tool"
- "about 32.09 messages"
- "median 31"
- "min 5"
- "max 54"
- "about 20.47 `<tool_call>` blocks per trace"
- "The `conversations` field is a list of `{from, value}` objects"
- "assistant (`gpt`) turns often contain `<tool_call> ... </tool_call>` blocks"
- "tool turns contain `<tool_response> ... </tool_response>` blocks"
- "This dataset is ShareGPT-like outer structure plus serialized tool-calling markup inside message text."

## Layout × Style Signals
- Content type: dataset structure + metrics + format comparison → suggests `dense-modules`
- Tone: technical, educational, no hype → suggests `pop-laboratory` or `technical-schematic`
- Audience: technically curious learner → suggests a precise but readable technical style
- Complexity: moderate with multiple evidence blocks → suggests a compact modular layout instead of a single chart

## Design Instructions (from user input)
- Educational and technical for a technically curious learner
- Use the established learning-materials folder structure
- `infographic.png` should be the canonical infographic artifact
- The infographic should be generated from the Q&A-derived structured content

## Recommended Combinations
1. **dense-modules + pop-laboratory** (Recommended): Best fit for showing metrics, roles, format comparison, and repo implications in one technical but readable infographic.
2. **dashboard + technical-schematic**: Strong for metrics, but weaker for the ShareGPT-versus-OpenAI structural comparison.
3. **comparison-matrix + pop-laboratory**: Strong for format comparison, but weaker for presenting the dataset snapshot and role/tool-density blocks cleanly.
