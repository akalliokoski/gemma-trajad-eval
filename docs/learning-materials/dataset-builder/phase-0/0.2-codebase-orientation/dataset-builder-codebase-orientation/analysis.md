---
title: "Dataset builder codebase orientation"
topic: "technical codebase walkthrough"
data_type: "module map + dataflow + design contracts"
complexity: "high"
point_count: 7
source_language: "en"
user_language: "en"
---

## Main Topic
This topic explains how the `dataset_builder/` codebase is organized, how data moves through it, and why the repo’s most important design choices are stable source IDs, leakage-safe splits, schema translation, and modular script responsibilities.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. which file owns which job in the dataset-builder pipeline
2. how raw HF traces become normalized records and then labeled train/dev/test outputs
3. why `source_trace_id`, `var_00`, and anomaly variants exist
4. where current code is robust versus still incomplete

## Target Audience
- **Knowledge Level**: beginner-to-intermediate technical learner
- **Context**: reading a script-first ML data pipeline for the first time
- **Expectations**: wants a concrete file-by-file map with real contracts

## Content Type Analysis
- **Data Structure**: repository map + left-to-right dataflow + contract callouts + known gaps
- **Key Relationships**: raw dataset -> inspection -> normalization -> perturbation -> build -> validation
- **Visual Opportunities**: pipeline ribbon, file cards, identity/split guardrail module, anomaly-rule module, and open-gaps module

## Key Data Points (Verbatim)
- "data/raw/"
- "source_trace_id"
- "var_00"
- "MVP_RULES"
- "ALL_RULES"
- "build_manifest.json"
- "hallucinated_tool"
- "invalid_tool_json"
- "unnecessary_replanning"

## Layout × Style Signals
- Content type: technical guide + file map + dataflow -> suggests `dense-modules`
- Tone: practical code-reading aid -> suggests `technical-schematic`
- Audience: learner reading source files -> needs legibility and explicit arrows
- Complexity: high but modular -> favors separate panels over a single long roadmap

## Design Instructions (from user input)
- Create learning-path material for Phase 0.2 codebase orientation
- Match the established learning-materials structure used in earlier materials
- Prefer practical explanations of why the code is shaped this way
- Generate a PNG infographic and podcast, not a manual SVG fallback

## Recommended Combinations
1. **dense-modules + technical-schematic** (Recommended): best for file responsibilities, data movement, and design-contract callouts.
2. **bento-grid + pop-laboratory**: good for overview, but slightly weaker for code-structure legibility.
3. **dashboard + ui-wireframe**: good for status-style summaries, but weaker for showing transformation flow.
