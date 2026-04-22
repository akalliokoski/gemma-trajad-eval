---
title: "Trajectory anomaly detection for LLM agents"
topic: "educational-technical"
data_type: "comparison + process overview"
complexity: "moderate"
point_count: 7
source_language: "en"
user_language: "en"
---

## Main Topic
This topic explains trajectory anomaly detection in the LLM-agent setting, contrasts it with GPS trajectory anomaly detection, and shows why first-error localization plus perturb-and-complete matter for runtime auditing and dataset design.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. what an agent trajectory is and what counts as a trajectory anomaly in TrajAD
2. the key differences between GPS trajectory anomaly detection and agent trajectory anomaly detection
3. why first-error-step localization and perturb-and-complete matter for rollback, retry, and realistic dataset construction

## Target Audience
- **Knowledge Level**: Beginner-to-intermediate technical learner
- **Context**: Working through the dataset-builder learning plan for the first time
- **Expectations**: A clear conceptual map, one strong comparison, and a direct connection to this repo's dataset builder

## Content Type Analysis
- **Data Structure**: Mixed structure: definition, side-by-side comparison, then a 3-step construction process plus project implications
- **Key Relationships**: Agent trajectories are execution traces; anomalies are procedural failures; first-error localization enables rollback-and-retry; perturb-and-complete produces realistic post-error continuations; this repo currently uses direct perturbation only
- **Visual Opportunities**: A definition module, a side-by-side comparison table, a 3-step process strip for TrajBench construction, a rollback/localization callout, and a repo-specific implications module

## Key Data Points (Verbatim)
- "Trajectory anomaly detection means auditing that execution process to answer two questions:"
- "1. Is this trajectory anomalous or normal?"
- "2. If it is anomalous, where is the first erroneous step?"
- "wrong reasoning that leads to a bad action"
- "wrong tool choice or wrong tool arguments"
- "loops, detours, and redundant actions"
- "continuing to act when the task is already complete or should stop"
- "Object being modeled | Movement in physical space | Multi-step task execution"
- "Typical sequence elements | GPS points, staypoints, durations, activities | Reasoning, actions, tool calls, observations"
- "What counts as an anomaly | Unusual route or movement pattern | Wrong reasoning, bad tool use, inefficient process, unwarranted continuation"
- "Main supervision target | Trajectory-level or point-level anomaly scoring | Binary detection plus first-error-step localization"
- "Why it matters | Detect abnormal mobility behavior | Enable runtime monitoring, rollback, and retry for LLM agents"
- "1. Start from a clean, successful trajectory."
- "2. Inject an anomaly at a chosen step."
- "3. Continue the trajectory from that corrupted state so the downstream steps reflect the consequences of the mistake."
- "This repo currently uses direct perturbation only: it edits one step and leaves later steps unchanged."
- "The verifier is not just checking whether the final answer looks okay; it is checking whether the execution process stays coherent, efficient, and properly bounded."

## Layout × Style Signals
- Content type: comparison + process overview + repo implications → suggests `dense-modules`
- Tone: technical, educational, analysis-oriented → suggests `pop-laboratory`
- Audience: technically curious learner → suggests a precise but legible technical style
- Complexity: moderate with several distinct concept blocks → suggests a modular layout with 6-7 sections

## Design Instructions (from user input)
- Educational, technical framing for a technically curious learner
- Prefer a layout/style combination that fits an educational concept comparison/process overview
- The earlier Matplotlib infographic workflow should no longer be treated as the source of truth

## Recommended Combinations
1. **dense-modules + pop-laboratory** (Recommended): Best fit for a compact educational technical guide that combines definition, comparison table, process strip, and repo-specific takeaways in one dense artifact.
2. **bento-grid + hand-drawn-edu**: Strong for approachable educational summaries, but less precise for the comparison table and process-auditing framing.
3. **comparison-matrix + technical-schematic**: Strong for the GPS-vs-agent contrast, but too narrow for the perturb-and-complete process and repo implications.
