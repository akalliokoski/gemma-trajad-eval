# Trajectory anomaly detection for LLM agents

## Overview
This infographic explains what trajectory anomaly detection means in the agent setting, why it differs from GPS trajectory anomaly detection, how TrajBench uses perturb-and-complete, and why those ideas matter for this repo's dataset builder.

## Learning Objectives
The viewer will understand:
1. what an agent trajectory is and what counts as an anomaly in TrajAD
2. the key differences between GPS trajectory anomaly detection and agent trajectory anomaly detection
3. why first-error-step localization and perturb-and-complete matter for rollback, retry, and realistic dataset construction

---

## Section 1: What is a trajectory here?

**Key Concept**: In TrajAD, a trajectory is an execution trace, not a path through physical space.

**Content**:
- In TrajAD, a trajectory is not a GPS route. It is the agent's full execution trace for one task: the instruction plus the sequence of reasoning, actions, and observations across time.
- Trajectory anomaly detection means auditing that execution process to answer two questions:
- 1. Is this trajectory anomalous or normal?
- 2. If it is anomalous, where is the first erroneous step?

**Visual Element**:
- Type: diagram
- Subject: a task instruction flowing into interleaved reasoning, action, and observation steps
- Treatment: technical flow strip with one highlighted first-error marker on a later step

**Text Labels**:
- Headline: "Agent trajectory = execution trace"
- Subhead: "Instruction + reasoning + actions + observations across time"
- Labels: "normal or anomalous?", "first erroneous step", "runtime auditing"

---

## Section 2: What counts as an anomaly?

**Key Concept**: Agent-trajectory anomalies are procedural failures in task execution.

**Content**:
- wrong reasoning that leads to a bad action
- wrong tool choice or wrong tool arguments
- loops, detours, and redundant actions
- continuing to act when the task is already complete or should stop

**Visual Element**:
- Type: illustration
- Subject: four anomaly cards with warning markers
- Treatment: compact warning zone with one icon per failure mode

**Text Labels**:
- Headline: "Common anomaly types"
- Labels: "wrong reasoning", "bad tool use", "loops/detours", "won't stop"

---

## Section 3: GPS vs agent trajectories

**Key Concept**: The core difference is what the word trajectory means.

**Content**:
| Dimension | GPS trajectory anomaly detection | Agent trajectory anomaly detection |
|---|---|---|
| Object being modeled | Movement in physical space | Multi-step task execution |
| Typical sequence elements | GPS points, staypoints, durations, activities | Reasoning, actions, tool calls, observations |
| What counts as an anomaly | Unusual route or movement pattern | Wrong reasoning, bad tool use, inefficient process, unwarranted continuation |
| Main supervision target | Trajectory-level or point-level anomaly scoring | Binary detection plus first-error-step localization |
| Why it matters | Detect abnormal mobility behavior | Enable runtime monitoring, rollback, and retry for LLM agents |

**Visual Element**:
- Type: split comparison
- Subject: map-like spatial path on the left and execution-trace audit path on the right
- Treatment: side-by-side matrix with row labels and contrasting icons

**Text Labels**:
- Headline: "GPS path vs agent process"
- Left label: "physical movement"
- Right label: "task execution"
- Labels: "object", "sequence elements", "anomaly", "supervision target", "why it matters"

---

## Section 4: Why first-error localization matters

**Key Concept**: Localization enables rollback-and-retry instead of restarting the entire task.

**Content**:
- That second part matters because the paper is explicitly about runtime auditing.
- If the verifier can localize the first bad step, the system can roll back to the previous good state and retry instead of restarting the whole task.

**Visual Element**:
- Type: diagram
- Subject: execution steps with a highlighted first bad step, rollback arrow, and retry branch
- Treatment: coordinate-labeled callout with a bright rollback arrow

**Text Labels**:
- Headline: "Find the first bad step"
- Labels: "localize", "roll back", "retry", "don't restart everything"

---

## Section 5: How TrajBench is constructed

**Key Concept**: TrajBench uses perturb-and-complete, not just a one-step edit.

**Content**:
- TrajBench is built from successful agent trajectories using a perturb-and-complete pipeline.
- 1. Start from a clean, successful trajectory.
- 2. Inject an anomaly at a chosen step.
- 3. Continue the trajectory from that corrupted state so the downstream steps reflect the consequences of the mistake.
- If you only perturb one step and leave the rest untouched, the result can look artificial because later steps may no longer make sense.
- Perturb-and-complete produces a more realistic post-error continuation, so the anomaly is embedded in a coherent but flawed trajectory rather than being an isolated broken token or one-step glitch.

**Visual Element**:
- Type: numbered step icon
- Subject: three-step pipeline with a clean trace, injected error, and flawed continuation
- Treatment: horizontal micro-process embedded inside a dense module

**Text Labels**:
- Headline: "Perturb-and-complete"
- Action: "start clean → inject error → continue from corrupted state"
- Labels: "clean trajectory", "chosen step", "realistic downstream consequences"

---

## Section 6: Why this matters for this repo

**Key Concept**: The repo's current direct perturbation approach is simpler but can create unrealistic downstream states.

**Content**:
- For this repo, that matters because the current dataset builder uses direct perturbation only: it edits one step and leaves later steps unchanged.
- That is simpler and cheaper, but it can create internal contradictions that would not appear in a naturally unfolding bad trajectory.
- TrajAD frames the problem as process supervision for LLM agents.
- The verifier is not just checking whether the final answer looks okay; it is checking whether the execution process stays coherent, efficient, and properly bounded.
- That is exactly why this dataset-builder project cares about anomaly taxonomy, step labels, and leakage-safe splits.

**Visual Element**:
- Type: comparison
- Subject: direct perturbation versus perturb-and-complete, ending in repo design implications
- Treatment: warning/pitfall zone next to a best-practice reference box

**Text Labels**:
- Headline: "Repo design implication"
- Labels: "direct perturbation only", "simpler and cheaper", "internal contradictions", "process supervision", "leakage-safe splits"

---

## Data Points (Verbatim)

All statistics, numbers, and quotes exactly as they appear in source:

### Statistics
- "1. Is this trajectory anomalous or normal?"
- "2. If it is anomalous, where is the first erroneous step?"
- "1. Start from a clean, successful trajectory."
- "2. Inject an anomaly at a chosen step."
- "3. Continue the trajectory from that corrupted state so the downstream steps reflect the consequences of the mistake."

### Quotes
- "In TrajAD, a trajectory is not a GPS route. It is the agent's full execution trace for one task: the instruction plus the sequence of reasoning, actions, and observations across time."
- "The verifier is not just checking whether the final answer looks okay; it is checking whether the execution process stays coherent, efficient, and properly bounded."

### Key Terms
- **trajectory anomaly detection**: "auditing that execution process"
- **agent trajectory anomaly detection**: "a path through task execution"
- **GPS trajectory anomaly detection**: "a path through physical space"
- **perturb-and-complete**: "inject an error, then continue the trajectory from that corrupted state so the downstream behavior stays realistic"

---

## Design Instructions

Extracted from user's steering prompt:

### Style Preferences
- educational
- technical
- for a technically curious learner
- use a style/layout that fits concept comparison and process overview

### Layout Preferences
- support both side-by-side comparison and a small process pipeline
- treat the prompt-driven infographic workflow as the source of truth, not the old Matplotlib artifacts

### Other Requirements
- create `analysis.md`, `structured-content.md`, `prompts/infographic.md`
- regenerate `infographic.png` if image-generation tooling is available
- do not edit `answers.md`
