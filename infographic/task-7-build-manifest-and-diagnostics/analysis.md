---
title: "Task 7 — Build Manifest and Diagnostics"
topic: "technical"
data_type: "process"
complexity: "moderate"
point_count: 5
source_language: "en"
user_language: "en"
---

## Main Topic
This infographic explains how Task 7 made dataset builds reproducible by writing a manifest JSON and printing a concise diagnostics summary.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. Why interactive console counts are not enough for reproducibility.
2. What the new build manifest stores.
3. What verification evidence shows the manifest workflow works on the real dataset.

## Target Audience
- **Knowledge Level**: Intermediate
- **Context**: Repo contributor or learner studying build reproducibility and dataset diagnostics.
- **Expectations**: Understand the new manifest fields, the saved artifact path, and the real build numbers.

## Content Type Analysis
- **Data Structure**: motivation -> manifest contents -> stdout diagnostics -> tests -> verification
- **Key Relationships**: build_trajad_dataset.py builds data and now saves metadata, build_manifest.json becomes the durable artifact, tests/test_build_manifest.py protects schema and summary behavior.
- **Visual Opportunities**: manifest file card, summary dashboard, counts chips, and a path artifact callout.

## Key Data Points (Verbatim)
- "2 passed"
- "Generated 56,724 anomalous records"
- "Coherence screen: kept=56,724 rejected=0"
- "Split sizes: train=47,973  dev=6,413  test=9,696"
- "normal=7,358 anomalous=56,724 all=64,082"
- "Validated 64,082 records from data/processed/all.jsonl"
- "All records valid."
- "build_manifest.json"

## Layout × Style Signals
- Content type: artifact + metrics + reproducibility -> suggests dashboard
- Tone: reproducible engineering workflow -> suggests technical-schematic
- Audience: repo contributors and learners -> suggests technical-schematic
- Complexity: moderate -> suggests panel layout with one artifact panel and one metrics panel

## Design Instructions (from user input)
Create an infographic for the Task 7 implementation and keep it in PNG format.

## Recommended Combinations
1. **dashboard + technical-schematic** (Recommended): Fits manifest artifact, summary metrics, per-rule diagnostics, and verification evidence.
2. **bento-grid + technical-schematic**: Good for mixing code, artifact, and metrics panels.
3. **flowchart + technical-schematic**: Good for showing build -> manifest -> validation flow, but weaker for numbers.
