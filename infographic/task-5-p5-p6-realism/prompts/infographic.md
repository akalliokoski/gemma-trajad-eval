Create a professional infographic following these specifications:

## Image Specifications
- **Type**: Infographic
- **Layout**: bento-grid
- **Style**: technical-schematic
- **Aspect Ratio**: 16:9
- **Language**: en

## Core Principles
- Clean engineering blueprint look
- Strong panel-based hierarchy
- Emphasize the old-vs-new redesign for P5 and P6
- Keep text concise and readable
- Preserve the exact verification numbers below
- No SVG output; final artifact must be a PNG infographic

## Content
Title: Task 5 — Make P5 and P6 More Realistic
Panels:
1. Why Task 5 exists: P5 created a dangling continuation pattern; P6 used an explicit contradiction marker that felt artificial; the goal was to make the two weakest perturbations look more like plausible bad agent behavior without adding model-generated continuation.
2. P5 redesign: old behavior = one dangling extra tool call; new behavior = a complete but unnecessary continuation with three steps: assistant tool call, tool response, assistant wrap-up; bad_step points to the first unnecessary extra step.
3. P6 redesign: old behavior = a loud marker that literally said contradiction; new behavior = a subtle but wrong natural-language conclusion based on the last tool response; helper functions extract_tool_response_text and tool_response_looks_empty support this logic.
4. Files and tests: updated dataset_builder/perturbations.py and tests/test_perturbations.py; added focused tests for P5 structural completeness and P6 natural-language contradiction behavior.
5. Verification: 4 passed; Generated 56,724 anomalous records; Coherence screen kept 56,724 and rejected 0; Validated 64,082 records from data/processed/all.jsonl; All records valid.
6. Result labels: continued_after_sufficient_evidence and contradicted_tool_result shown as simple anomaly chips, not dense prose paragraphs.

Text labels (in en):
- Fix the Most Synthetic Rules
- P5: Complete the Extra Continuation
- P6: Contradict More Naturally
- Small Change Surface
- Verified End-to-End
- old: dangling
- new: assistant
- new: tool
- new: wrap-up
- old: explicit marker
- new: subtle wrong conclusion
- extract_tool_response_text
- tool_response_looks_empty
- no explicit contradiction tag
- perturbations.py
- test_perturbations.py
- 4 passed
- 56,724 anomalies
- 0 rejected
- 64,082 valid
- continued_after_sufficient_evidence
- contradicted_tool_result
