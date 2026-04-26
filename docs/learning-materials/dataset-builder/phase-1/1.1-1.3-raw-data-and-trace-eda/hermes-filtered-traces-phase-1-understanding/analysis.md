---
title: "Hermes filtered traces Phase 1 understanding"
topic: "educational/technical"
data_type: "dataset structure + empirical EDA + workflow implications"
complexity: "moderate"
point_count: 8
source_language: "en"
user_language: "en"
---

## Main Topic
This topic captures what Phase 1 actually established after downloading and inspecting the filtered Hermes traces locally. It explains the raw schema, the degree of tool density, the kinds of tasks present in the corpus, and why those facts strongly constrain the design of `dataset_builder/`.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. that the filtered Hermes corpus is a long-form, tool-centric agent-trace dataset rather than a simple chat dataset
2. that the raw storage format is ShareGPT-style `{from, value}` plus serialized tool markup, which makes normalization essential
3. that the correct stop line after Phase 1 is better data understanding and Phase 2 normalization study, not a premature jump into training

## Target Audience
- **Knowledge Level**: Beginner-to-intermediate technical learner
- **Context**: Completing the active Phase 1 stop-line of the dataset-builder learning path
- **Expectations**: Understand the dataset reality well enough to read normalization and perturbation code with concrete mental models

## Content Type Analysis
- **Data Structure**: one raw-data verification block, one schema block, one EDA metrics block, one sample-task block, one tool-serialization block, one perturbation-eligibility block, and one repo-implication block
- **Key Relationships**: long traces + tool density explain why trajectory anomaly detection is whole-trace work; ShareGPT-style storage explains normalization needs; eligibility patterns explain why perturbation realism matters more than perturbation existence
- **Visual Opportunities**: large metric tiles for 3,679 / 32.1 / 100.0%, a raw-schema panel, a sample-task strip, embedded tool-call example boxes, and a final “why this matters” module

## Key Data Points (Verbatim)
- "3,679"
- "about 368 MB"
- "id"
- "conversations"
- "tools"
- "category"
- "subcategory"
- "task"
- "{from, value}"
- "system"
- "human"
- "gpt"
- "tool"
- "32.1"
- "5"
- "54"
- "100.0%"
- "99.4%"
- "Repository Tasks"
- "Agent Tools"
- "Terminal & Coding"
- "<tool_call>"
- "<tool_response>"
- "{"name": "session_search", "arguments": {"query": "staging deployment config"}}"

## Layout × Style Signals
- Content type: multi-block technical summary with metrics and structural examples → suggests `dense-modules`
- Tone: technical, educational, grounded → suggests `pop-laboratory`
- Audience: technically curious learner → suggests precise modular design instead of decorative style
- Complexity: moderate with several evidence blocks → suggests a compact portrait layout with strong sectioning

## Design Instructions (from user input)
- Keep the content technically meaningful instead of boilerplate or repetitive
- Hammer home the most important topics rather than mirroring the same structure mechanically
- Treat `infographic.png` as the canonical image-generated artifact
- Make the asset feel like a debrief from real inspection work, not a generic lesson card

## Recommended Combinations
1. **dense-modules + pop-laboratory** (Recommended): Best fit for technical metrics, schema panels, raw examples, and repo implications in one compact learning asset.
2. **bento-grid + technical-schematic**: Good for modular structure, but slightly weaker than `dense-modules` for the density of evidence here.
3. **dashboard + pop-laboratory**: Good for metrics, but weaker for the raw-schema and serialized-tool-call explanation.
