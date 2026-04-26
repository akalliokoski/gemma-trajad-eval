---
title: "Hermes normalization deep dive"
topic: "educational/technical"
data_type: "schema transformation + stability guarantees + edge-case audit"
complexity: "moderate"
point_count: 7
source_language: "en"
user_language: "en"
---

## Main Topic
This topic explains what normalization actually does inside `dataset_builder/`: how it converts raw `{from, value}` traces into internal `{role, content}` trajectories, how it preserves trace identity with `source_trace_id`, and what the real corpus does or does not reveal about edge cases.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. that normalization is the schema bridge from raw Hermes traces to the repo’s internal trajectory contract
2. that `source_trace_id` stability is essential for leakage-safe split assignment later
3. that the current corpus is clean enough that role and metadata edge cases are mostly absent, which sharpens trust in the transformation step

## Target Audience
- **Knowledge Level**: Beginner-to-intermediate technical learner
- **Context**: Continuing from Phase 1 into the first code-level transformation stage
- **Expectations**: Understand what the normalization script guarantees before studying perturbation logic

## Content Type Analysis
- **Data Structure**: one run-verification module, one raw-vs-normalized comparison module, one role-mapping module, one metadata module, one stability module, one edge-case module, and one project-implication module
- **Key Relationships**: schema mapping enables consistent trajectories; stable source IDs enable split discipline; metadata enrichment adds signal without complicating the core trajectory object
- **Visual Opportunities**: side-by-side raw versus normalized cards, role-mapping arrows, defaults/metadata chips, stability badge, and an edge-case audit panel

## Key Data Points (Verbatim)
- "3,679"
- "0"
- "data/interim/hermes_normalized_phase2.jsonl"
- "{from, value}"
- "{role, content}"
- "system"
- "human"
- "gpt"
- "tool"
- "user"
- "assistant"
- "is_anomalous=false"
- "anomaly_type=null"
- "bad_step=null"
- "generation_rule=null"
- "trajectory_length"
- "tool_call_count"
- "tool_response_count"
- "has_think"
- "stable_on_repeat: true"
- "missing_category_count: 0"
- "missing_subcategory_count: 0"
- "empty_metadata_count: 0"

## Layout × Style Signals
- Content type: technical transformation plus guarantees → suggests `dense-modules`
- Tone: precise and code-adjacent → suggests `pop-laboratory`
- Audience: learner crossing from concept to implementation → suggests readable modular diagrams rather than decorative visuals
- Complexity: moderate with multiple guarantees → suggests a portrait modular layout

## Design Instructions (from user input)
- Keep the artifact meaningful and emphasize the most important topics
- Treat `infographic.png` as the canonical generated output
- Make the infographic feel like a debrief of what normalization guarantees, not a generic textbook slide

## Recommended Combinations
1. **dense-modules + pop-laboratory** (Recommended): Best fit for side-by-side schema comparison, guarantee badges, and code-adjacent takeaways.
2. **structural-breakdown + technical-schematic**: Good for transformation anatomy, but less flexible for the stability and edge-case audit modules.
3. **bento-grid + pop-laboratory**: Usable fallback, but less strong than `dense-modules` for a coherent technical flow.
