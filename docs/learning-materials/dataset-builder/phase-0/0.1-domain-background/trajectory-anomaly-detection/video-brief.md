# Overview

This explainer teaches the first undone Phase 0.1 topic from the dataset-builder learning plan: trajectory anomaly detection for LLM agents. It should make one core contrast memorable: an agent trajectory is a task-execution trace, not a GPS route.

# Audience

A technically literate learner studying `dataset_builder/` and trying to understand why anomaly taxonomy, step labels, and realistic perturbations matter.

# Core Takeaway

TrajAD reframes anomaly detection as runtime process supervision for LLM agents. The goal is not only to detect that something went wrong, but to localize the first bad step so the system can roll back and retry. TrajBench supports this by using perturb-and-complete rather than plain one-step corruption.

# Source Notes

- In TrajAD, a trajectory consists of an instruction plus interleaved reasoning, action, and observation steps.
- Agent trajectory anomaly detection asks whether the execution process is anomalous and where the first erroneous step occurs.
- GPS trajectory anomaly detection models movement through physical space; agent trajectory anomaly detection models movement through task execution.
- TrajBench is built by starting from successful trajectories, injecting an anomaly, then continuing from that corrupted state so later behavior remains coherent.
- This repo's current dataset builder uses direct perturbation, which is simpler but can produce later-step contradictions.
- Sources: https://arxiv.org/abs/2602.06443 and https://arxiv.org/abs/2409.15366

# Narrative Arc

Start by dissolving the common misconception that "trajectory" means location history. Then show what an agent trajectory actually contains. Next, explain why first-error localization turns anomaly detection into a runtime control tool. Finally, show how perturb-and-complete raises the realism bar compared with this repo's simpler direct-perturbation approach.

# Scene Plan

## Scene `scene_01_misconception`
- Goal: Break the reflex that trajectory means a path on a map.
- On-screen visuals:
  - Split screen: map route on the left, task trace on the right
  - Label: GPS trajectory versus agent trajectory
  - Visual punchline: same word, different object
- Narration:
  - Many readers hear trajectory and imagine a GPS route.
  - TrajAD uses the same word for something else: the full execution trace of an LLM agent doing a task.

## Scene `scene_02_agent_trace`
- Goal: Define the agent trajectory clearly.
- On-screen visuals:
  - Flow: instruction → reason → act → observe
  - Compact callouts for reasoning, tool call, tool response, next step
  - Badge: execution process over time
- Narration:
  - In this setting, the trajectory is the instruction plus the sequence of reasoning, actions, and observations.
  - The verifier is auditing the process, not just the final answer.

## Scene `scene_03_anomalies`
- Goal: Show what counts as an anomaly in the agent setting.
- On-screen visuals:
  - Four cards: wrong reasoning, wrong tool use, loops, unwarranted continuation
  - Accent strip: procedural failures
  - Small note: plausible final answer can still hide a bad process
- Narration:
  - Agent anomalies are procedural failures such as bad reasoning, bad tool arguments, loops, or continuing when the task should already stop.
  - That is very different from looking for unusual movement through physical space.

## Scene `scene_04_localization`
- Goal: Explain why first-error localization matters.
- On-screen visuals:
  - Timeline with steps one through four
  - Step three highlighted red as first bad step
  - Arrow back from step three to step two with rollback and retry label
- Narration:
  - TrajAD does not stop at anomaly detection.
  - It wants the first erroneous step so the system can halt, roll back to the previous safe point, and retry efficiently.

## Scene `scene_05_perturb_complete`
- Goal: Explain perturb-and-complete.
- On-screen visuals:
  - Three-stage pipeline: clean trajectory → inject anomaly → continue from corrupted state
  - Compare against a small side note: direct perturbation leaves future steps untouched
  - Highlight: realistic downstream consequences
- Narration:
  - TrajBench is built with perturb-and-complete.
  - Instead of editing one step and freezing the rest, it lets the bad state propagate into later steps so the flawed trajectory stays coherent.

## Scene `scene_06_repo_implication`
- Goal: Connect the paper back to this repo.
- On-screen visuals:
  - Repo card: current builder uses direct perturbation
  - Tradeoff table: simpler and cheaper versus less realistic downstream behavior
  - Final takeaway banner: better supervision needs better bad trajectories
- Narration:
  - That comparison matters for this repo's dataset builder.
  - Direct perturbation is useful and practical, but TrajAD shows why realistic post-error continuation is the stronger target if you want high-quality anomaly supervision.

# Visual Language

Dark background, bright cyan and teal accents, clear card-based layout, monospace micro-labels for process steps, and minimal text per slide. Prefer left-to-right flow, simple timelines, and contrast cards over dense paragraphs.

# Optional Narration Draft

Use the scene narrations as the backbone. Keep the pace deliberate, with a short pause after the misconception reveal, after the rollback timeline, and after the perturb-and-complete comparison.

# Build Notes

Use the generated scene manifest as the source of truth. Each scene should read like an infographic card, not a lecture slide. Keep labels short, make the comparison between GPS and agent trajectories visually obvious, and let the final scene explicitly mention the repo's direct-perturbation tradeoff.
