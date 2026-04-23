# Task 6 — Deepen Validation for First-Error Localization

## Overview
This infographic shows how the dataset builder made bad_step validation care about rule semantics for the current perturbations instead of only checking presence and numeric range.

## Learning Objectives
The viewer will understand:
1. Why first-error supervision needs more than schema checks.
2. How P4, P5, and P7 now receive targeted bad_step validation.
3. What verification evidence shows the stricter validator still accepts the full dataset.

---

## Section 1: Why Task 6 Exists

**Key Concept**: first-error localization is a supervision target, so the validator must check where the anomaly starts, not just whether bad_step is an integer.

**Content**:
- Current validation mostly checked that bad_step existed and was in range.
- Phase 0 emphasized first-bad-step semantics as a core supervision target.
- Task 6 adds rule-aware checks only for the currently implemented high-value rules.

**Visual Element**: problem statement panel.
- Type: diagram
- Subject: generic range check vs semantic bad-step check
- Treatment: engineering comparison card with a weak validator on the left and a rule-aware validator on the right

**Text Labels**:
- Headline: "From Range Checks to Semantics"
- Labels: "bad_step in range", "first bad action", "label trustworthiness"

---

## Section 2: Validator Helpers

**Key Concept**: a small helper layer keeps the rule-aware logic narrow and readable.

**Content**:
- Added _content(step).
- Added _has_tool_call(step).
- Added _validate_rule_aware_bad_step(record).
- Generic schema checks still run first.

**Visual Element**: helper stack panel.
- Type: modules
- Subject: three helper blocks feeding into validate_record
- Treatment: blueprint modules with arrows into the main validator

**Text Labels**:
- Headline: "Small Helper Layer"
- Labels: "_content", "_has_tool_call", "_validate_rule_aware_bad_step", "validate_record"

---

## Section 3: Rule-Aware Checks

**Key Concept**: Task 6 adds high-value semantics for the rules where bad_step meaning is easiest to drift.

**Content**:
- P4 repeated_step: bad_step must point to the duplicated assistant step and match the previous assistant/tool pair.
- P5 continued_after_sufficient_evidence: bad_step must point to the first unnecessary extra step in the assistant -> tool -> assistant continuation.
- P7 premature_final_answer: bad_step must point to the inserted premature final answer at the cut point, after earlier tool evidence.

**Visual Element**: three rule cards.
- Type: comparison
- Subject: P4, P5, and P7 cards with the correct bad_step location highlighted
- Treatment: schematic trace snippets with one glowing index per rule

**Text Labels**:
- Headline: "Three Rules, Three Localization Checks"
- Labels: "P4 duplicate start", "P5 first extra step", "P7 premature final answer"

---

## Section 4: Tests

**Key Concept**: focused negative tests now catch mislocalized labels instead of only malformed fields.

**Content**:
- Added focused tests for mislocalized P4, P5, and P7 records.
- Added a skipped-step edge case that allows the missing position at the end.
- Updated tests/test_validate_labels.py.

**Visual Element**: test panel.
- Type: dashboard
- Subject: failing-example cards turning into passing assertions
- Treatment: clean terminal-style cards with red-to-green transitions

**Text Labels**:
- Headline: "Tests Encode the Semantics"
- Labels: "mislocalized P4", "mislocalized P5", "mislocalized P7", "end-position skip allowed"

---

## Section 5: Verification

**Key Concept**: the stricter validator improves label discipline without breaking the existing processed dataset.

**Content**:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py -v
- 8 passed
- python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
- Validated 64,082 records from data/processed/all.jsonl
- All records valid.

**Visual Element**: verification dashboard.
- Type: dashboard
- Subject: command snippets and result chips
- Treatment: engineering monitor with bold pass counters and validation badges

**Text Labels**:
- Headline: "Verified Against Real Data"
- Labels: "8 passed", "64,082 validated", "strict mode", "all records valid"

---

## Data Points (Verbatim)
- "8 passed"
- "Validated 64,082 records from data/processed/all.jsonl"
- "All records valid."
- "P4"
- "P5"
- "P7"
- "bad_step"
- "generation_rule"

---

## Design Instructions
- Use technical-schematic visual language.
- Make the correct bad_step location visually obvious for each covered rule.
- Keep the helper layer small and readable.
- Preserve the exact verification numbers.
- Final artifact must be PNG.
