---
title: "Task 4 — Lightweight Coherence Screen"
topic: "technical"
data_type: "process"
complexity: "moderate"
point_count: 5
source_language: "en"
user_language: "en"
---

## Main Topic
This infographic explains how Task 4 added a tiny deterministic coherence screen after perturbation so obviously broken anomalous traces are filtered without introducing a heavy perturb-and-complete system.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. Why a post-perturbation coherence screen improves dataset quality.
2. Which structural failures the screen rejects and where it runs in the pipeline.
3. How the implementation preserved repeated_step coverage and reproducible same-seed builds.

## Target Audience
- **Knowledge Level**: Intermediate
- **Context**: Repo contributor or learner studying trajectory perturbations and dataset quality controls.
- **Expectations**: Understand what the coherence screen checks, how it integrates into the builder, and what evidence shows it is safe.

## Content Type Analysis
- **Data Structure**: motivation → rejection rules → pipeline integration → reproducibility safeguard → verification evidence
- **Key Relationships**: perturbations generate anomalies, coherence.py screens structure, build_trajad_dataset.py counts rejections and preserves deterministic split assignment.
- **Visual Opportunities**: show before/after pipeline, three rejection rule cards, and a verification dashboard with counts.

## Key Data Points (Verbatim)
- "13 passed"
- "Generated 29,354 anomalous records"
- "Coherence screen: kept=29,354 rejected=0"
- "repeated_step train count: 5,518"
- "repeated_step test count: 1,104"
- "All records valid"
- "no diff output for two same-seed builds"

## Layout × Style Signals
- Content type: implementation pipeline plus checks → suggests bento-grid
- Tone: engineering quality gate → suggests technical-schematic
- Audience: repo contributors and learners → suggests technical-schematic
- Complexity: moderate → suggests multi-panel layout with one evidence panel

## Design Instructions (from user input)
Create an infographic for the Task 4 implementation.

## Recommended Combinations
1. **bento-grid + technical-schematic** (Recommended): Fits motivation, rejection logic, pipeline placement, determinism, and verification into a single engineering summary.
2. **structural-breakdown + technical-schematic**: Good for emphasizing the builder/coherence module interaction.
3. **dashboard + pop-laboratory**: Good if the focus is mostly on metrics and verification output.
