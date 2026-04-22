# Dataset construction and anomaly taxonomy in TrajAD

## Overview
This infographic explains how TrajAD organizes anomalous trajectories, how TrajBench generates anomalous samples, and why this matters for the `dataset_builder/` work in this repo. It combines taxonomy, generation-method comparison, and quality-bar evidence in one technical learning asset.

## Learning Objectives
The viewer will understand:
1. the three top-level anomaly classes in TrajAD and the six perturbation families that map onto them
2. how TrajBench's perturb-and-complete pipeline differs from this repo's current 8 perturbation rules and direct perturbation strategy
3. why coherent downstream behavior and high human agreement matter for later `dataset_builder/` manual review and first-error localization work

---

## Section 1: Top-level anomaly taxonomy

**Key Concept**: TrajAD organizes anomalous trajectories into three top-level classes.

**Content**:
- 1. Task Failure
- 2. Process Inefficiency
- 3. Unwarranted Continuation
- These classes are meant to cover not only obvious failed runs, but also trajectories that still finish the task while using a wasteful or unsafe process, and trajectories that should have stopped but keep going.
- Task Failure = the agent does not successfully complete the task because its reasoning or execution goes wrong.
- Process Inefficiency = the agent reaches the goal, but the path is unnecessarily long or redundant.
- Unwarranted Continuation = the agent should stop, refuse, or declare completion, but instead keeps acting.

**Visual Element**:
- Type: diagram
- Subject: three labeled taxonomy branches with one-line definitions under each class
- Treatment: coordinate-labeled technical module with one parent label feeding three class blocks

**Text Labels**:
- Headline: "Three anomaly classes"
- Subhead: "TrajAD top-level taxonomy"
- Labels: "Task Failure", "Process Inefficiency", "Unwarranted Continuation"

---

## Section 2: Six perturbation families

**Key Concept**: TrajBench uses six perturbation families aligned to the three anomaly classes.

**Content**:
- TrajBench uses six perturbation families to synthesize anomalous trajectories. They align with the paper's anomaly taxonomy:
- Task Failure:
- reasoning-error injection
- execution-error injection
- Process Inefficiency:
- loop insertion
- detour or redundant-subsequence insertion
- Unwarranted Continuation:
- failure-to-refuse setup
- redundant-continuation setup

**Visual Element**:
- Type: diagram
- Subject: class-to-family mapping table or stacked module with two families under each class
- Treatment: six compact cells grouped by class color accents

**Text Labels**:
- Headline: "Six perturbation families"
- Subhead: "TrajBench synthesis rules"
- Labels: "reasoning-error injection", "execution-error injection", "loop insertion", "detour or redundant-subsequence insertion", "failure-to-refuse setup", "redundant-continuation setup"

---

## Section 3: TrajBench vs this repo

**Key Concept**: The difference is not only 6 versus 8; the generation strategy is richer in TrajBench because it models downstream consequences after the injected mistake.

**Content**:
| Aspect | TrajBench | This repo |
|--------|-----------|-----------|
| Rule count framing | TrajBench uses six perturbation families to synthesize anomalous trajectories. | Compared with this repo's current 8 perturbation rules, this project has a slightly broader rule count at the implementation level, but it uses a simpler generation strategy. |
| Generation method | TrajBench starts from a successful trajectory, injects an anomaly at a chosen step, and then continues the rest of the trajectory from that corrupted state. | This repo's current dataset builder uses direct perturbation: it edits a step and leaves later steps unchanged. |
| Consequence | That continuation matters because later reasoning, actions, and observations now reflect the consequences of the mistake. | That is simpler and cheaper, but it can create internally inconsistent samples. |

**Visual Element**:
- Type: split comparison
- Subject: side-by-side pipeline cards for TrajBench and this repo
- Treatment: left-right comparison with arrows showing "inject" then either "continue from corrupted state" or "leave later steps unchanged"

**Text Labels**:
- Headline: "6 rules vs 8 rules is not the real difference"
- Subhead: "Generation method matters more"
- Labels: "TrajBench", "This repo", "perturb-and-complete", "direct perturbation"

---

## Section 4: What perturb-and-complete adds

**Key Concept**: Perturb-and-complete creates coherent bad trajectories whose later steps evolve naturally from the first error.

**Content**:
- Perturb-and-complete adds realistic downstream consequences.
- TrajBench starts from a successful trajectory, injects an anomaly at a chosen step, and then continues the rest of the trajectory from that corrupted state. That continuation matters because later reasoning, actions, and observations now reflect the consequences of the mistake.
- This repo's current dataset builder uses direct perturbation: it edits a step and leaves later steps unchanged. That is simpler and cheaper, but it can create internally inconsistent samples.
- So the real advantage of perturb-and-complete is not only realism in a vague sense. It creates coherent bad trajectories whose later steps evolve naturally from the first error. That gives better supervision for both anomaly classification and first-error localization.

**Visual Element**:
- Type: process comparison
- Subject: before/after trajectory strip showing one injected error and downstream consequences
- Treatment: technical sequence with highlighted corrupted state and later-step propagation

**Text Labels**:
- Headline: "Perturb-and-complete adds downstream coherence"
- Subhead: "Why later steps should reflect the first error"
- Labels: "chosen step", "corrupted state", "later reasoning", "later actions", "later observations"

---

## Section 5: Human agreement rates

**Key Concept**: Strong human agreement shows that the anomaly definitions and localization targets are clear enough to support reliable supervision.

**Content**:
- The paper reports strong human agreement:
- 96.2% agreement for anomaly classification
- 94.5% agreement for first-error localization
- These numbers matter because they set a quality bar for this repo's later manual-review work.
- If this project's synthetic anomalies are confusing, unrealistic, or hard to localize consistently, then downstream supervision quality will suffer.

**Visual Element**:
- Type: number highlight
- Subject: two large percentage callouts with a quality-bar annotation
- Treatment: fluorescent numeric emphasis with compact explanatory notes

**Text Labels**:
- Headline: "Human agreement is the quality bar"
- Subhead: "Reliable labels depend on clear anomaly construction"
- Labels: "96.2% anomaly classification", "94.5% first-error localization"

---

## Section 6: Why this matters to `dataset_builder/`

**Key Concept**: A useful dataset is not just corrupted traces; it needs taxonomy alignment, coherent downstream behavior, and labels humans can agree on.

**Content**:
- The main lesson from TrajAD section 3 is that anomaly quality depends on both taxonomy and generation method.
- A useful dataset is not just a pile of corrupted traces. It needs:
- a clear anomaly taxonomy
- perturbations that map cleanly to that taxonomy
- coherent downstream behavior after the first error
- labels that humans can agree on reliably
- That is directly relevant to `dataset_builder/`, because later phases in this repo depend on realistic perturbation rules, stable step labels, and high-confidence manual review.

**Visual Element**:
- Type: quick reference
- Subject: compact checklist or design principles panel tied to `dataset_builder/`
- Treatment: boxed takeaway module with four checklist items and repo-specific footer note

**Text Labels**:
- Headline: "Dataset-builder takeaway"
- Subhead: "Taxonomy + generation method both matter"
- Labels: "clear anomaly taxonomy", "map perturbations cleanly", "coherent downstream behavior", "high-confidence manual review"

---

## Data Points (Verbatim)

All statistics, numbers, and quotes exactly as they appear in source:

### Statistics
- "six perturbation families"
- "8 perturbation rules"
- "96.2% agreement for anomaly classification"
- "94.5% agreement for first-error localization"

### Key Terms
- **Task Failure**: "the agent does not successfully complete the task because its reasoning or execution goes wrong."
- **Process Inefficiency**: "the agent reaches the goal, but the path is unnecessarily long or redundant."
- **Unwarranted Continuation**: "the agent should stop, refuse, or declare completion, but instead keeps acting."
- **perturb-and-complete**: "injects an anomaly at a chosen step, and then continues the rest of the trajectory from that corrupted state"
- **direct perturbation**: "it edits a step and leaves later steps unchanged"

---

## Design Instructions

Extracted from user's steering prompt:

### Style Preferences
- Educational, technical, and clear
- Fit taxonomy + generation-method comparison
- Treat `infographic.png` as the primary infographic artifact

### Layout Preferences
- Use a layout that can hold taxonomy, rule-family mapping, method comparison, and metrics in one view
- Prefer a technical modular structure over a single-figure tree or single comparison chart

### Other Requirements
- Do not edit `answers.md`
- The earlier Matplotlib infographic workflow should no longer be the source of truth
- Save the generation prompt at `prompts/infographic.md`