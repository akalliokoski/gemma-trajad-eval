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
- Key concepts and numbers should be visually emphasized
- Labels should stay exact to the source wording where provided

## Layout Guidelines

Use a high-density modular infographic with 6 distinct information modules packed with concrete data.

- Every module should contain specific terms, numbers, or labeled relationships.
- Use a coordinate-labeled variant with section markers such as SEC-A, SEC-B, MOD-1.
- Main title at the top with a concise subtitle.
- Include a dataset-snapshot module, a role-inventory module, a tool-density module, a structure-breakdown module, a ShareGPT-vs-OpenAI comparison module, and a repo takeaway module.
- Minimal whitespace; dense but organized.
- Add module boundary markers, small technical metadata, arrows, and compact data callouts.

## Style Guidelines

Apply the pop-laboratory style consistently:

- Background: professional grayish-white with faint blueprint grid texture
- Primary blocks: muted teal/sage green
- High-alert accent: fluorescent pink only for warnings, critical data, or standout contrasts
- Marker highlights: vivid lemon yellow highlighter effect for keywords and important numbers
- Line art: ultra-fine charcoal brown for technical grids, coordinates, rulers, and hairlines
- Add coordinate-style labels on every module
- Use technical diagrams, rulers, cross-hair targets, and compact annotations
- Keep a strong contrast between bold headers and small precise labels
- Avoid cute/cartoonish doodles, soft pastels, rainbow palettes, and decorative empty space

---

Generate the infographic based on the content below:

# Hermes filtered traces dataset card and viewer

## Overview
This infographic explains what the Hermes filtered traces dataset looks like when you inspect the Hugging Face dataset card and viewer. It combines dataset scale, trajectory length, role structure, tool-call density, format comparison, and repo-specific implications in one technical learning asset.

## Module plan

### MOD-1 — Dataset snapshot
- Headline: "Dataset snapshot"
- Subhead: "Scale and typical trajectory length"
- Highlight exactly:
  - "3,679 rows"
  - "32.1 messages per conversation"
  - "median 31"
  - "min 5"
  - "max 54"
- Add note: "Typical traces are roughly 30-message agent executions, not short chat snippets."

### MOD-2 — Raw role inventory
- Headline: "Four raw roles"
- Subhead: "What appears in conversations"
- Show exactly:
  - "system"
  - "human"
  - "gpt"
  - "tool"
- Add note: "The dataset stores system setup, user request, assistant behavior, and tool outputs."

### MOD-3 — Tool calls dominate
- Headline: "Tool calls dominate"
- Subhead: "This is a tool-centric trajectory dataset"
- Highlight exactly:
  - "18.5 tool calls per conversation"
  - "about 20.47 `<tool_call>` blocks per trace"
  - "about 19.47 `<tool_response>` blocks per trace"
- Show assistant-to-tool flow arrows.

### MOD-4 — ShareGPT-style outer format
- Headline: "ShareGPT-style outer format"
- Subhead: "Tool protocol is embedded inside text"
- Show these labels exactly:
  - "{from, value}"
  - "<tool_call>"
  - "<tool_response>"
  - "tools JSON string"
- Include a visual of one record with embedded markup highlighted.

### MOD-5 — Not native OpenAI chat format
- Headline: "Not native OpenAI chat format"
- Subhead: "Think ShareGPT-style storage plus embedded tool markup"
- Compare:
  - "Outer message structure: {from, value} vs role/content"
  - "Tool calls: serialized inside text vs structured tool_calls objects"
  - "Tool responses: serialized inside text vs separate structured tool messages"
  - "Practical implication: parser must recover structure from strings"

### MOD-6 — Dataset-builder takeaway
- Headline: "Dataset-builder takeaway"
- Subhead: "Structure drives the pipeline design"
- Show this checklist exactly:
  - "whole-trace reasoning"
  - "role mapping"
  - "tool-call perturbations"
  - "parse structure from text"
- Footer note: "Long, tool-rich trajectories are why normalization and perturbation code matter so much in this repo."

## Additional composition instructions
- Use technical callouts, arrows, and coordinate markers to connect modules.
- Visually emphasize the numbers `3,679`, `32.1`, and `18.5`.
- Keep the infographic readable, but information-dense.
