---
title: "Task 6 — Deepen Validation for First-Error Localization"
topic: "technical"
data_type: "process"
complexity: "moderate"
point_count: 5
source_language: "en"
user_language: "en"
---

## Main Topic
This infographic explains how Task 6 upgraded label validation from generic schema checks to rule-aware bad-step checks for the current synthetic perturbation rules.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. Why first-error localization needs semantic checks beyond integer range validation.
2. Which generation rules received targeted validation logic and what each check enforces.
3. What verification evidence shows the stricter validator still accepts the real dataset.

## Target Audience
- **Knowledge Level**: Intermediate
- **Context**: Repo contributor or learner studying trajectory-label trustworthiness.
- **Expectations**: Understand the bad_step semantics, the rules covered, and the pass evidence.

## Content Type Analysis
- **Data Structure**: motivation -> validator helpers -> rule-specific checks -> tests -> verification evidence
- **Key Relationships**: validate_labels.py enforces semantics, tests/test_validate_labels.py encodes counterexamples, all.jsonl strict validation proves compatibility with the built dataset.
- **Visual Opportunities**: a bad_step semantics ladder, three rule cards, and a pass dashboard.

## Key Data Points (Verbatim)
- "8 passed"
- "Validated 64,082 records from data/processed/all.jsonl"
- "All records valid."
- "P4"
- "P5"
- "P7"
- "bad_step"
- "generation_rule"

## Layout × Style Signals
- Content type: implementation with rule comparisons -> suggests bento-grid
- Tone: validation discipline and localization semantics -> suggests technical-schematic
- Audience: repo contributors and learners -> suggests technical-schematic
- Complexity: moderate -> suggests multi-panel explanation with one verification panel

## Design Instructions (from user input)
Create an infographic for the Task 6 implementation and keep it in PNG format.

## Recommended Combinations
1. **bento-grid + technical-schematic** (Recommended): Fits motivation, helper logic, three rule cards, tests, and verification evidence.
2. **timeline + technical-schematic**: Good for showing first-error position semantics across a trace, but weaker for code/test coverage.
3. **dashboard + technical-schematic**: Good for metrics-first presentation, but weaker for teaching the per-rule logic.
