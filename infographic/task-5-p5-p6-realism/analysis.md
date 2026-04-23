---
title: "Task 5 — Make P5 and P6 More Realistic"
topic: "technical"
data_type: "process"
complexity: "moderate"
point_count: 5
source_language: "en"
user_language: "en"
---

## Main Topic
This infographic explains how Task 5 made the two most synthetic perturbation rules more realistic by replacing a dangling continuation and an explicit contradiction marker with behavior that still looks like plausible bad agent output.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. Why P5 and P6 were considered the most obviously synthetic perturbations.
2. How the implementation made P5 structurally complete and P6 subtly contradictory.
3. What verification evidence shows the change preserved build health and label validity.

## Target Audience
- **Knowledge Level**: Intermediate
- **Context**: Repo contributor or learner studying how to build realistic trajectory anomalies.
- **Expectations**: Understand the old failure modes, the new rule behavior, and the validation evidence.

## Content Type Analysis
- **Data Structure**: problem diagnosis → P5 redesign → P6 redesign → code/test artifacts → verification evidence
- **Key Relationships**: perturbations.py defines anomaly behavior, tests/test_perturbations.py encodes the new expectations, build_trajad_dataset.py and validate_labels.py confirm the dataset still builds cleanly.
- **Visual Opportunities**: before/after cards for P5 and P6, a small code-logic panel for helper functions, and a verification dashboard with result counts.

## Key Data Points (Verbatim)
- "4 passed"
- "Generated 56,724 anomalous records"
- "Coherence screen: kept=56,724 rejected=0"
- "Validated 64,082 records from data/processed/all.jsonl"
- "All records valid."
- "continued_after_sufficient_evidence"
- "contradicted_tool_result"

## Layout × Style Signals
- Content type: implementation change with before/after comparisons → suggests bento-grid
- Tone: engineering cleanup and realism upgrade → suggests technical-schematic
- Audience: repo contributors and learners → suggests technical-schematic
- Complexity: moderate → suggests multi-panel layout with a verification summary panel

## Design Instructions (from user input)
Create an infographic for the Task 5 implementation and keep it in PNG format.

## Recommended Combinations
1. **bento-grid + technical-schematic** (Recommended): Fits two before/after perturbation redesigns, helper logic, files touched, and verification evidence in one engineering summary.
2. **binary-comparison + technical-schematic**: Good for emphasizing old vs new behavior for P5 and P6, but weaker for showing verification evidence.
3. **dashboard + pop-laboratory**: Good if the focus is mostly on implementation metrics and result counts.
