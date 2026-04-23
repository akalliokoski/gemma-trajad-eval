# Task 5 — Make P5 and P6 More Realistic

## Overview
This infographic shows how the dataset builder replaced two obviously synthetic perturbations with more realistic bad-agent behavior while keeping the implementation deterministic, testable, and build-safe.

## Learning Objectives
The viewer will understand:
1. Why P5 and P6 needed realism upgrades.
2. How P5 now adds a complete unnecessary continuation and P6 now uses subtle natural-language contradiction.
3. What verification evidence shows the dataset still builds and validates cleanly.

---

## Section 1: Why Task 5 Exists

**Key Concept**: The two weakest perturbations were synthetic for different reasons and needed to look more like plausible bad agent behavior.

**Content**:
- `P5` creates a dangling continuation pattern.
- `P6` uses an explicit contradiction marker that is too artificial.
- Improve the most obviously synthetic perturbations without adding model-generated continuation.

**Visual Element**: Problem panel.
- Type: diagram
- Subject: two warning cards labeled P5 and P6 with synthetic-pattern callouts
- Treatment: engineering schematic cards with red issue badges

**Text Labels**:
- Headline: "Fix the Most Synthetic Rules"
- Labels: "dangling continuation", "explicit contradiction marker", "keep it deterministic"

---

## Section 2: P5 Redesign

**Key Concept**: P5 now creates an unnecessary extra continuation that is structurally complete instead of dangling.

**Content**:
- P5 no longer appends a dangling assistant tool call.
- P5 now appends a structurally complete unnecessary continuation: assistant tool call -> tool response -> assistant wrap-up.
- P5 marks bad_step at the first unnecessary extra step, not at the final appended message.

**Visual Element**: Before/after comparison.
- Type: comparison
- Subject: old dangling extra tool call vs new assistant -> tool -> assistant sequence
- Treatment: left red broken trace, right green complete but unnecessary continuation

**Text Labels**:
- Headline: "P5: Complete the Extra Continuation"
- Labels: "old: dangling", "new: assistant", "new: tool", "new: wrap-up"

---

## Section 3: P6 Redesign

**Key Concept**: P6 now contradicts the last tool result with a subtle natural-language answer instead of a bracketed marker.

**Content**:
- P6 no longer prepends an explicit bracketed marker like `[CONTRADICTION]`.
- P6 now replaces the final assistant answer with a subtle but wrong natural-language conclusion.
- Added extract_tool_response_text(content).
- Added tool_response_looks_empty(content).
- P6 now contradicts whether the last tool response contained a concrete result.

**Visual Element**: Logic panel.
- Type: diagram
- Subject: last tool response -> helper checks -> wrong natural-language conclusion
- Treatment: schematic flow with helper-function labels and a crossed-out marker tag

**Text Labels**:
- Headline: "P6: Contradict More Naturally"
- Labels: "extract_tool_response_text", "tool_response_looks_empty", "no [CONTRADICTION]"

---

## Section 4: Tests and Files

**Key Concept**: The realism upgrade is locked in with focused tests and a narrow code footprint.

**Content**:
- Updated dataset_builder/perturbations.py.
- Updated tests/test_perturbations.py.
- Added focused tests for P5 structural completeness.
- Added focused tests for P6 natural-language contradiction behavior.

**Visual Element**: File card cluster.
- Type: modules
- Subject: code file and test file with check badges
- Treatment: blueprint module cards with small assertion icons

**Text Labels**:
- Headline: "Small Change Surface"
- Labels: "perturbations.py", "test_perturbations.py", "P5 structure", "P6 language"

---

## Section 5: Verification

**Key Concept**: Tests, rebuild, and strict validation confirm the more realistic perturbations still fit the pipeline.

**Content**:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_perturbations.py -v
- 4 passed
- python3 dataset_builder/build_trajad_dataset.py --seed 42
- Generated 56,724 anomalous records
- Coherence screen: kept=56,724 rejected=0
- Validated 64,082 records from data/processed/all.jsonl
- All records valid.

**Visual Element**: Verification dashboard.
- Type: dashboard
- Subject: command snippets and result tiles
- Treatment: clean engineering monitor with bold pass/fact chips

**Text Labels**:
- Headline: "Verified End-to-End"
- Labels: "4 passed", "56,724 anomalies", "0 rejected", "64,082 valid"

---

## Data Points (Verbatim)
- "4 passed"
- "Generated 56,724 anomalous records"
- "Coherence screen: kept=56,724 rejected=0"
- "Validated 64,082 records from data/processed/all.jsonl"
- "All records valid."
- "continued_after_sufficient_evidence"
- "contradicted_tool_result"

---

## Design Instructions
- Use technical-schematic visual language.
- Emphasize the old-vs-new realism improvement for P5 and P6.
- Make the structural completeness of P5 visually obvious.
- Make the removal of the explicit contradiction marker visually obvious.
- Keep verification numbers exact and readable.
