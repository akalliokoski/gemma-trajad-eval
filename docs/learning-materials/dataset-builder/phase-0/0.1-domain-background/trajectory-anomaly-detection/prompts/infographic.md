Create a professional infographic following these specifications:

## Image Specifications

- **Type**: Infographic
- **Layout**: dense-modules
- **Style**: pop-laboratory
- **Aspect Ratio**: portrait (9:16)
- **Language**: en

## Core Principles

- Follow the layout structure precisely for information architecture
- Apply style aesthetics consistently throughout
- Use the prompt-driven infographic workflow as the source of truth; do not reproduce the old Matplotlib look
- Keep information concise, highlight keywords and core concepts
- Maintain clear visual hierarchy while preserving high information density
- Preserve source facts faithfully and keep the GPS-vs-agent comparison explicit

## Text Requirements

- All text must be in English
- Main titles should be prominent and readable
- Key concepts should be visually emphasized
- Labels should be clear and appropriately sized
- Keep wording faithful to the structured content and source facts

## Layout Guidelines

High-density modular layout with 6-7 typed information modules packed with concrete data.

- 6-7 distinct modules per image, each serving a specific information function
- Minimal whitespace—compact spacing prioritized over breathing room
- Smaller text acceptable to maximize information density
- Each module identified by coordinate label or section marker (e.g., MOD-1, SEC-A)
- Use a coordinate-labeled or grid-cell dense-modules variant so definition, comparison, process, rollback logic, and repo implications each live in distinct modules
- Include one side-by-side comparison module and one numbered process module
- Include one warning/pitfall zone that contrasts direct perturbation only with perturb-and-complete

## Style Guidelines

Lab manual precision meets pop art color impact—coordinate systems, technical diagrams, and fluorescent accents on blueprint grid.

- Background: professional grayish-white with faint blueprint grid texture
- Primary blocks in muted teal/sage green
- High-alert accent: vibrant fluorescent pink strictly for warnings, critical data, or winner highlights
- Marker highlights: vivid lemon yellow for key phrases and numbers
- Line art: ultra-fine charcoal brown for technical grids, coordinates, and hairlines
- Coordinate-style labels on every module
- Technical diagrams, rulers, cross-hair targets, mathematical symbols, and corner metadata throughout
- High contrast between bold headers and tiny technical annotations
- Avoid cute/cartoonish doodles, soft pastels, generic stock icons, or large empty white space

---

Generate the infographic based on the content below:

# Trajectory anomaly detection for LLM agents

## Overview
This infographic explains what trajectory anomaly detection means in the agent setting, why it differs from GPS trajectory anomaly detection, how TrajBench uses perturb-and-complete, and why those ideas matter for this repo's dataset builder.

## Learning Objectives
The viewer will understand:
1. what an agent trajectory is and what counts as an anomaly in TrajAD
2. the key differences between GPS trajectory anomaly detection and agent trajectory anomaly detection
3. why first-error-step localization and perturb-and-complete matter for rollback, retry, and realistic dataset construction

## Sections to render
1. Agent trajectory = execution trace, not GPS route
2. Common anomaly types: wrong reasoning, bad tool use, loops/detours, unwarranted continuation
3. GPS path vs agent process comparison table
4. Why first-error localization matters for rollback-and-retry
5. Perturb-and-complete 3-step pipeline
6. Repo design implication: direct perturbation only vs realistic bad-trajectory continuation

## Verbatim content to preserve
- "In TrajAD, a trajectory is not a GPS route. It is the agent's full execution trace for one task: the instruction plus the sequence of reasoning, actions, and observations across time."
- "Trajectory anomaly detection means auditing that execution process to answer two questions:"
- "1. Is this trajectory anomalous or normal?"
- "2. If it is anomalous, where is the first erroneous step?"
- "wrong reasoning that leads to a bad action"
- "wrong tool choice or wrong tool arguments"
- "loops, detours, and redundant actions"
- "continuing to act when the task is already complete or should stop"
- Comparison rows:
  - "Object being modeled | Movement in physical space | Multi-step task execution"
  - "Typical sequence elements | GPS points, staypoints, durations, activities | Reasoning, actions, tool calls, observations"
  - "What counts as an anomaly | Unusual route or movement pattern | Wrong reasoning, bad tool use, inefficient process, unwarranted continuation"
  - "Main supervision target | Trajectory-level or point-level anomaly scoring | Binary detection plus first-error-step localization"
  - "Why it matters | Detect abnormal mobility behavior | Enable runtime monitoring, rollback, and retry for LLM agents"
- "If the verifier can localize the first bad step, the system can roll back to the previous good state and retry instead of restarting the whole task."
- "1. Start from a clean, successful trajectory."
- "2. Inject an anomaly at a chosen step."
- "3. Continue the trajectory from that corrupted state so the downstream steps reflect the consequences of the mistake."
- "This repo currently uses direct perturbation only: it edits one step and leaves later steps unchanged."
- "That is simpler and cheaper, but it can create internal contradictions that would not appear in a naturally unfolding bad trajectory."
- "The verifier is not just checking whether the final answer looks okay; it is checking whether the execution process stays coherent, efficient, and properly bounded."
- "That is exactly why this dataset-builder project cares about anomaly taxonomy, step labels, and leakage-safe splits."

Text labels (in en):
- Main title: "Trajectory anomaly detection for LLM agents"
- Subtitle: "Definition, comparison, runtime auditing, and dataset design implications"
- Module labels: "execution trace", "anomaly types", "GPS vs agent", "first bad step", "perturb-and-complete", "repo implication"
- Highlight labels: "rollback", "retry", "direct perturbation only", "realistic downstream consequences", "process supervision", "leakage-safe splits"
