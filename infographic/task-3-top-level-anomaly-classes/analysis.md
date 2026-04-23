---
title: "Task 3 — Top-Level Anomaly Classes"
topic: "technical"
data_type: "overview"
complexity: "moderate"
point_count: 4
source_language: "en"
user_language: "en"
---

## Main Topic
This infographic explains how Task 3 added explicit top-level anomaly classes to the dataset pipeline so records encode both detailed anomaly types and higher-level taxonomy labels.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. Why top-level anomaly classes improve dataset clarity.
2. How anomaly_class is populated and validated.
3. Which taxonomy decisions were encoded and how the implementation was verified.

## Target Audience
- **Knowledge Level**: Intermediate
- **Context**: Repo contributor or learner studying dataset labeling and perturbation outputs.
- **Expectations**: Understand the taxonomy change, the label flow, and the verification evidence.

## Content Type Analysis
- **Data Structure**: motivation → mapping table → validation/build behavior → verification
- **Key Relationships**: perturbations assign anomaly_class, build preserves normal defaults, validator enforces correctness.
- **Visual Opportunities**: show type-to-class mapping, normal vs anomalous record labeling, and verification metrics.

## Key Data Points (Verbatim)
- "6 passed"
- "Wrote 36,712 records"
- "All records valid"
- "wrong_tool_choice → process_inefficiency"
- "skipped_required_step → task_failure"

## Layout × Style Signals
- Content type: implementation summary with taxonomy mapping → suggests bento-grid
- Tone: engineering + labeling rules → suggests technical-schematic
- Audience: repo contributors and learners → suggests technical-schematic
- Complexity: moderate → suggests clear multi-panel layout

## Design Instructions (from user input)
Create an infographic for the Task 3 implementation.

## Recommended Combinations
1. **bento-grid + technical-schematic** (Recommended): Fits taxonomy, validation, build behavior, and verification into one engineering summary.
2. **comparison-matrix + technical-schematic**: Good for emphasizing anomaly_type to anomaly_class mapping.
3. **dashboard + corporate-memphis**: Good if emphasizing verification metrics over logic flow.
