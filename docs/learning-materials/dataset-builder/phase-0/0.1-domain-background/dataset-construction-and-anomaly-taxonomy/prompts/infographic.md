Create a professional infographic following these specifications:

## Image Specifications

- **Type**: Infographic
- **Layout**: dense-modules
- **Style**: pop-laboratory
- **Aspect Ratio**: landscape (16:9)
- **Language**: en

## Core Principles

- Follow the layout structure precisely for information architecture
- Apply style aesthetics consistently throughout
- Keep information concise, highlight keywords and core concepts
- Maintain clear visual hierarchy while preserving high information density
- Treat this as an educational technical infographic for a technically curious learner
- Make `infographic.png` the primary rendered artifact from this prompt-driven workflow
- Do not imitate earlier Matplotlib styling; use the selected layout and style as the source of truth

## Text Requirements

- All text must be in English
- Main title should be prominent and readable
- Key concepts and percentages should be visually emphasized
- Labels should stay exact to the source wording where provided

## Layout Guidelines

Use a high-density modular infographic with 6 distinct information modules packed with concrete data.

- Every module should contain specific terms, numbers, or labeled relationships.
- Use a coordinate-labeled variant with section markers such as SEC-A, SEC-B, MOD-1.
- Main title at the top with a concise subtitle.
- Include a taxonomy module, a class-to-family mapping module, a side-by-side method comparison module, a downstream-consequences module, a human-agreement metrics module, and a quick-reference takeaway module.
- Minimal whitespace; dense but organized.
- Add module boundary markers, small technical metadata, arrows, and compact data callouts.

## Style Guidelines

Apply the pop-laboratory style consistently:

- Background: professional grayish-white with faint blueprint grid texture
- Primary blocks: muted teal/sage green
- High-alert accent: fluorescent pink only for warnings, critical data, or winner highlights
- Marker highlights: vivid lemon yellow highlighter effect for keywords and important numbers
- Line art: ultra-fine charcoal brown for technical grids, coordinates, rulers, and hairlines
- Add coordinate-style labels on every module
- Use technical diagrams, rulers, cross-hair targets, mathematical symbols, and small technical annotations
- Keep a strong contrast between bold headers and small precise labels
- Avoid cute/cartoonish doodles, soft pastels, rainbow palettes, and decorative empty space

---

Generate the infographic based on the content below:

# Dataset construction and anomaly taxonomy in TrajAD

## Overview
This infographic explains how TrajAD organizes anomalous trajectories, how TrajBench generates anomalous samples, and why this matters for the `dataset_builder/` work in this repo.

## Module plan

### MOD-1 — Three anomaly classes
- Headline: "Three anomaly classes"
- Subhead: "TrajAD top-level taxonomy"
- Show three branches labeled exactly:
  - "Task Failure"
  - "Process Inefficiency"
  - "Unwarranted Continuation"
- Add one-line definitions:
  - "the agent does not successfully complete the task because its reasoning or execution goes wrong"
  - "the agent reaches the goal, but the path is unnecessarily long or redundant"
  - "the agent should stop, refuse, or declare completion, but instead keeps acting"

### MOD-2 — Six perturbation families
- Headline: "Six perturbation families"
- Subhead: "TrajBench synthesis rules"
- Group these exactly under the three classes:
  - Task Failure → "reasoning-error injection", "execution-error injection"
  - Process Inefficiency → "loop insertion", "detour or redundant-subsequence insertion"
  - Unwarranted Continuation → "failure-to-refuse setup", "redundant-continuation setup"

### MOD-3 — Why 6 vs 8 is not the real difference
- Headline: "6 rules vs 8 rules is not the real difference"
- Subhead: "Generation method matters more"
- Left card: "TrajBench"
  - "TrajBench uses six perturbation families to synthesize anomalous trajectories."
  - "injects an anomaly at a chosen step, and then continues the rest of the trajectory from that corrupted state"
- Right card: "This repo"
  - "8 perturbation rules"
  - "it edits a step and leaves later steps unchanged"
  - "simpler generation strategy"

### MOD-4 — Perturb-and-complete adds downstream coherence
- Headline: "Perturb-and-complete adds downstream coherence"
- Subhead: "Why later steps should reflect the first error"
- Show a sequence: successful trajectory → chosen step → corrupted state → later reasoning / later actions / later observations
- Add a contrast note: "direct perturbation" can leave later steps "internally inconsistent samples"

### MOD-5 — Human agreement is the quality bar
- Headline: "Human agreement is the quality bar"
- Subhead: "Reliable labels depend on clear anomaly construction"
- Highlight these exactly:
  - "96.2% agreement for anomaly classification"
  - "94.5% agreement for first-error localization"
- Add note: "These numbers matter because they set a quality bar for this repo's later manual-review work."

### MOD-6 — Dataset-builder takeaway
- Headline: "Dataset-builder takeaway"
- Subhead: "Taxonomy + generation method both matter"
- Show this checklist exactly:
  - "a clear anomaly taxonomy"
  - "perturbations that map cleanly to that taxonomy"
  - "coherent downstream behavior after the first error"
  - "labels that humans can agree on reliably"
- Footer note: "later phases in this repo depend on realistic perturbation rules, stable step labels, and high-confidence manual review"

## Additional composition instructions
- Use technical callouts, arrows, and coordinate markers to connect modules
- Make the comparison and taxonomy equally prominent
- Keep every module text-dense but readable
- Use fluorescent pink only for warnings/critical emphasis and lemon yellow only for highlighted keywords or numeric callouts
- Include tiny technical metadata in corners for visual flavor, but do not add new factual claims

Text labels (in en):
- "Dataset construction and anomaly taxonomy in TrajAD"
- "Three anomaly classes"
- "TrajAD top-level taxonomy"
- "Task Failure"
- "Process Inefficiency"
- "Unwarranted Continuation"
- "Six perturbation families"
- "TrajBench synthesis rules"
- "6 rules vs 8 rules is not the real difference"
- "Generation method matters more"
- "TrajBench"
- "This repo"
- "perturb-and-complete"
- "direct perturbation"
- "Perturb-and-complete adds downstream coherence"
- "Why later steps should reflect the first error"
- "Human agreement is the quality bar"
- "Reliable labels depend on clear anomaly construction"
- "96.2% agreement for anomaly classification"
- "94.5% agreement for first-error localization"
- "Dataset-builder takeaway"
- "Taxonomy + generation method both matter"