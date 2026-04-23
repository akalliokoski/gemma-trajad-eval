---
title: "Task 2 — Derived Structural Metadata"
topic: "technical"
data_type: "overview"
complexity: "moderate"
point_count: 4
source_language: "en"
user_language: "en"
---

## Main Topic
This infographic explains how Task 2 enriched normalized trajectories with derived structural metadata while preserving the simple role/content trajectory schema.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. Why structural metadata matters for tool-heavy Hermes traces.
2. Which metadata fields were added and where they live.
3. How the change was validated with tests and a normalization smoke run.

## Target Audience
- **Knowledge Level**: Intermediate
- **Context**: Repo contributor or learner studying the normalization stage.
- **Expectations**: Understand the metadata design and how it was validated.

## Content Type Analysis
- **Data Structure**: motivation → helper function → metadata fields → verification
- **Key Relationships**: derive_trace_metadata computes cheap signals; normalize_record merges them into metadata without altering trajectory items.
- **Visual Opportunities**: show unchanged trajectory shape next to enriched metadata box and highlight numeric smoke-test output.

## Key Data Points (Verbatim)
- "Tests passed: 2"
- "Normalized 3,679 records → data/interim/hermes_normalized.jsonl (0 errors)"
- "trajectory_length"
- "tool_call_count"
- "tool_response_count"
- "has_think"

## Layout × Style Signals
- Content type: overview + implementation summary → suggests bento-grid
- Tone: engineering metadata change → suggests technical-schematic
- Audience: repo contributors and learners → suggests technical-schematic
- Complexity: moderate → suggests clear multi-panel layout

## Design Instructions (from user input)
Create an infographic of the implementation.

## Recommended Combinations
1. **bento-grid + technical-schematic** (Recommended): Fits schema, helper logic, metadata, and verification into one engineering summary.
2. **structural-breakdown + technical-schematic**: Good if emphasizing data shape transformation.
3. **dashboard + corporate-memphis**: Good if emphasizing counts and smoke-test metrics.
