---
title: "Dataset builder environment setup"
topic: "practical repo setup"
data_type: "portable setup contract + VPS-specific adaptation"
complexity: "medium"
point_count: 6
source_language: "en"
user_language: "en"
---

## Main Topic
This topic explains how to set up a minimal, reproducible environment for the `dataset_builder/` project. It contrasts the generic learning-plan recipe with the documented VPS-specific `uv` workflow and emphasizes verification, Hugging Face readiness, and the expected `data/` directory layout.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. the baseline environment contract of the repo
2. when to use standard `venv + pip` versus `uv`
3. why import checks and directory checks matter
4. why Hugging Face auth is preparation for publishing rather than a blocker for public download

## Target Audience
- **Knowledge Level**: beginner technical learner
- **Context**: preparing to run the dataset pipeline for the first time
- **Expectations**: wants practical setup instructions, not DevOps theater

## Content Type Analysis
- **Data Structure**: setup checklist + decision branch + verification layer + directory map
- **Key Relationships**: repo contract -> machine-specific tool choice -> verification -> ready state
- **Visual Opportunities**: decision fork, checklist, directory tree, and do-now vs later-auth panel

## Key Data Points (Verbatim)
- "requires-python = >=3.11"
- ".venv"
- `.[dev]`
- `uv`
- `huggingface-cli login`
- `data/raw/`
- `data/interim/`
- `data/processed/`

## Layout × Style Signals
- Content type: setup guide + decision branch -> suggests `linear-progression`
- Tone: calm, practical, confidence-building -> suggests `ikea-manual`
- Audience: first-run learner -> needs clear sequence and low visual noise
- Complexity: medium -> best served by a readable step ladder with one small branch

## Design Instructions (from user input)
- Create learning-path material for Phase 0.3 environment setup
- Match the earlier learning-materials structure
- Keep the explanation practical and repo-grounded
- Generate PNG infographic artifact via image workflow

## Recommended Combinations
1. **linear-progression + ikea-manual** (Recommended): best for a clear step-by-step setup path with one practical decision branch.
2. **bridge + hand-drawn-edu**: good for generic-vs-VPS comparison, but weaker for the step sequence.
3. **bento-grid + corporate-memphis**: good overview, but less intuitive for setup order.
