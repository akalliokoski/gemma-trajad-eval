Create a professional infographic following these specifications:

## Image Specifications
- Type: Infographic
- Layout: bento-grid
- Style: technical-schematic
- Aspect Ratio: 16:9
- Language: en

## Core Principles
- Clean engineering blueprint look
- Strong panel-based hierarchy
- Emphasize bad_step localization semantics, not generic schema validation
- Keep text concise and readable
- Preserve the exact verification numbers below
- Final artifact must be PNG

## Content
Title: Task 6 — Deepen Validation for First-Error Localization
Panels:
1. Why Task 6 exists: bad_step is a supervision target, so range-only validation is too weak; the goal is to check where the anomaly starts for the current perturbation rules.
2. Validator helpers: show _content, _has_tool_call, and _validate_rule_aware_bad_step as a small helper layer feeding validate_record.
3. Rule-aware checks: P4 repeated_step must point to the duplicated assistant step; P5 continued_after_sufficient_evidence must point to the first unnecessary extra step in an assistant -> tool -> assistant continuation; P7 premature_final_answer must point to the inserted premature final answer at the cut point after earlier tool evidence.
4. Tests: updated tests/test_validate_labels.py with focused negative tests for mislocalized P4, P5, and P7 records plus an allowed skipped-step end-position edge case.
5. Verification: 8 passed; Validated 64,082 records from data/processed/all.jsonl; All records valid.
6. Result chips: P4, P5, P7, bad_step, generation_rule.

Text labels (in en):
- From Range Checks to Semantics
- Small Helper Layer
- Three Rules, Three Localization Checks
- Tests Encode the Semantics
- Verified Against Real Data
- bad_step in range
- first bad action
- label trustworthiness
- _content
- _has_tool_call
- _validate_rule_aware_bad_step
- validate_record
- P4 duplicate start
- P5 first extra step
- P7 premature final answer
- mislocalized P4
- mislocalized P5
- mislocalized P7
- end-position skip allowed
- 8 passed
- 64,082 validated
- strict mode
- all records valid
- bad_step
- generation_rule
