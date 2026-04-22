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

## Text Requirements

- All text must be in English
- Main title should be prominent and readable
- Key concepts and phrases should be visually emphasized
- Labels should stay exact to the source wording where provided

## Layout Guidelines

Use a high-density modular infographic with 7 distinct information modules packed with concrete implementation guidance.

- Every module should contain specific phrases, file names, or labeled relationships.
- Use a coordinate-labeled variant with section markers such as SEC-A, SEC-B, MOD-1.
- Main title at the top with a concise subtitle.
- Include a simple-backbone module, a main-gap module, a Phase-0-findings module, a priority-roadmap module, a concrete-file-map module, a best-practices module, and a compute-policy module.
- Minimal whitespace; dense but organized.
- Add module boundary markers, small technical metadata, arrows, and compact callouts.

## Style Guidelines

Apply the pop-laboratory style consistently:

- Background: professional grayish-white with faint blueprint grid texture
- Primary blocks: muted teal/sage green
- High-alert accent: fluorescent pink only for warnings, critical data, or standout contrasts
- Marker highlights: vivid lemon yellow highlighter effect for keywords and important phrases
- Line art: ultra-fine charcoal brown for technical grids, coordinates, rulers, and hairlines
- Add coordinate-style labels on every module
- Use technical diagrams, rulers, cross-hair targets, and compact annotations
- Keep a strong contrast between bold headers and small precise labels
- Avoid cute/cartoonish doodles, soft pastels, rainbow palettes, and decorative empty space

---

Generate the infographic based on the content below:

# Dataset-builder implementation improvements after Phase 0

## Overview
This infographic explains how the current dataset-builder should improve after Phase 0. Keep the architecture simple, fix the real data-quality gaps, and make future GPU-backed extensions Modal-first.

## Module plan

### MOD-1 — Keep the simple backbone
- Headline: "Keep the simple backbone"
- Subhead: "Do not rewrite what already works"
- Show exactly:
  - "normalize"
  - "perturb"
  - "split safely"
  - "validate"
- Add note: "keep the current script-first pipeline"

### MOD-2 — Main gap
- Headline: "Main gap"
- Subhead: "Quality, not platform sprawl"
- Show exactly:
  - "data quality discipline"
  - "direct perturbation only"
  - "coherence risk"
  - "trustworthy labels"

### MOD-3 — Phase 0 findings
- Headline: "Phase 0 findings"
- Subhead: "The code should follow the data"
- Show exactly:
  - "{from, value}"
  - "<tool_call>"
  - "~32 messages"
  - "tool-heavy corpus"

### MOD-4 — Priority roadmap
- Headline: "Priority roadmap"
- Subhead: "Small changes, big quality gain"
- Show exactly:
  - "raw-schema-safe inspection"
  - "lightweight coherence screening"
  - "explicit anomaly classes"
  - "improve P5 and P6 realism"
  - "rule-aware localization validation"
  - "build manifests and perturbation diagnostics"

### MOD-5 — Concrete file map
- Headline: "Where the changes go"
- Subhead: "Specific files, not vague architecture talk"
- Show exactly:
  - "dataset_builder/inspect_traces.py"
  - "dataset_builder/normalize_trajectory.py"
  - "dataset_builder/perturbations.py"
  - "dataset_builder/build_trajad_dataset.py"
  - "dataset_builder/validate_labels.py"
  - "tests/"

### MOD-6 — Best-practice guardrails
- Headline: "Best-practice guardrails"
- Subhead: "Simple on purpose"
- Show exactly:
  - "YAGNI"
  - "DRY"
  - "deterministic"
  - "reproducible"
  - "explainable"
  - "practical, elegant, and understandable"

### MOD-7 — Compute policy
- Headline: "Compute policy"
- Subhead: "Modal first for GPU work"
- Show exactly:
  - "Modal serverless GPU is now the default future GPU tier"
  - "Apple Silicon is secondary"
  - "VPS for current tasks"
- Add note: "Use Modal first if future model-assisted continuation or GPU-backed filtering is added."

## Additional composition instructions
- Use technical callouts, arrows, and coordinate markers to connect modules.
- Visually emphasize the phrases "data quality discipline", "raw-schema-safe inspection", and "Modal serverless GPU".
- Keep the infographic readable, but information-dense.
- Use exactly one visible module label for each module: MOD-1, MOD-2, MOD-3, MOD-4, MOD-5, MOD-6, MOD-7. Do not duplicate or skip module numbers.
- Prefer larger primary text and fewer tiny side annotations; readability matters more than decorative clutter.
