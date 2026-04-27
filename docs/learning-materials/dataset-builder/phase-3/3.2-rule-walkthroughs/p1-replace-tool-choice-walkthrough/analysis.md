---
title: "P1 replace_tool_choice walkthrough"
topic: "educational/technical"
data_type: "rule walkthrough + sample comparison + bugfix debrief"
complexity: "moderate"
point_count: 6
source_language: "en"
user_language: "en"
---

## Main Topic
This topic explains what the first perturbation rule actually does on real normalized traces, why mapped replacements are better than `_v2` fallback names, and how the walkthrough exposed and fixed an over-mutation bug in multi-tool assistant messages.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. that P1 changes tool choice while preserving structural validity
2. that realism depends heavily on whether the replacement tool comes from a believable nearby map or a synthetic `_v2` fallback
3. that the walkthrough directly improved the implementation by limiting replacement to the first tool-call block in a multi-tool assistant message

## Target Audience
- **Knowledge Level**: Beginner-to-intermediate technical learner
- **Context**: First rule-level deep dive after the Phase 3 domain-context overview
- **Expectations**: Understand both the behavior and the realism limits of P1

## Content Type Analysis
- **Data Structure**: one rule-definition module, one mapped-example module, one fallback-example module, one bug-discovery module, one fix-and-verification module, and one takeaway module
- **Key Relationships**: mapped replacement affects realism; fallback strategy affects realism more negatively; mutation granularity affects whether the output is a single bounded anomaly or a broader synthetic rewrite
- **Visual Opportunities**: side-by-side before/after tool-call cards, nearby-vs-fallback contrast, bug/fix panel, and verification badges

## Key Data Points (Verbatim)
- "wrong_tool_choice"
- "read_file -> list_directory"
- "search_files -> search_files_v2"
- "terminal -> terminal_v2"
- "count=1"
- "7 passed"
- "multi-tool assistant message"
- "only the first match"

## Layout × Style Signals
- Content type: comparison plus implementation bugfix debrief -> suggests `bento-grid`
- Tone: technical and code-adjacent -> suggests `technical-schematic`
- Audience: learner moving from concept to code behavior -> suggests readable modular diagrams with larger labels
- Complexity: moderate -> suggests a simpler, lower-text layout than the earlier dense context poster

## Design Instructions (from user input)
- Keep the artifact meaningful and emphasize the most important ideas over boilerplate
- Treat `infographic.png` as the canonical generated output
- Keep text load low enough that the model has a realistic chance of rendering it legibly

## Recommended Combinations
1. **bento-grid + technical-schematic** (Recommended): Best fit for clear rule debrief, before/after cards, and a bugfix panel with fewer text blocks.
2. **binary-comparison + technical-schematic**: Strong for nearby-vs-fallback contrast, but weaker for showing the implementation fix and verification status together.
3. **bento-grid + pop-laboratory**: Good fallback if the typography is legible enough, but less clean than `technical-schematic` for this smaller rule walkthrough.
