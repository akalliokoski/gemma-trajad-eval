# P1 replace_tool_choice walkthrough

## Overview
This infographic explains what the first perturbation rule does on real normalized traces. It contrasts a believable nearby-tool replacement against unrealistic `_v2` fallbacks, then shows the implementation bug that was discovered and fixed during the walkthrough.

## Learning Objectives
The viewer will understand:
1. that P1 changes a tool name while keeping the call structurally valid
2. that nearby mapped replacements are more believable than `_v2` fallbacks
3. that a small regex fix made the mutation more bounded and trustworthy

---

## Section 1: What P1 does

**Key Concept**: P1 creates a wrong-tool-choice anomaly without breaking JSON structure.

**Content**:
- anomaly type: `wrong_tool_choice`
- selects an assistant step with `<tool_call>`
- swaps the tool name
- keeps call structure valid

**Visual Element**:
- Type: rule summary card
- Subject: compact rule pipeline
- Treatment: four chips with one arrowed flow

**Text Labels**:
- Headline: "What P1 does"
- Labels: "wrong_tool_choice", "assistant step", "swap tool name", "structure stays valid"

---

## Section 2: Mapped replacement example

**Key Concept**: A nearby mapped replacement can look like a believable mistake.

**Content**:
- real sample: `read_file -> list_directory`
- same path argument preserved
- structurally valid, procedurally wrong

**Visual Element**:
- Type: before/after comparison
- Subject: one tool-call card turning into another
- Treatment: left-right example with preserved argument chip

**Text Labels**:
- Headline: "Nearby mapped example"
- Labels: "read_file", "list_directory", "same arguments", "better realism"

---

## Section 3: Fallback weakness

**Key Concept**: `_v2` fallback names are the main realism weakness in the current rule.

**Content**:
- `search_files -> search_files_v2`
- `terminal -> terminal_v2`
- passes validation
- still looks synthetic

**Visual Element**:
- Type: warning comparison card
- Subject: two fallback examples with a warning badge
- Treatment: pink caution highlight around `_v2`

**Text Labels**:
- Headline: "Fallback weakness"
- Labels: "search_files_v2", "terminal_v2", "passes validation", "looks synthetic"

---

## Section 4: Bug discovered

**Key Concept**: Multi-tool assistant messages were being over-mutated.

**Content**:
- some assistant messages contain multiple `<tool_call>` blocks
- old helper replaced every match
- unrelated tool calls were overwritten too

**Visual Element**:
- Type: bug panel
- Subject: one assistant message with three tool-call boxes
- Treatment: highlight all boxes in red for the buggy behavior

**Text Labels**:
- Headline: "Bug discovered"
- Labels: "multi-tool assistant message", "all matches replaced", "over-mutation"

---

## Section 5: Fix and verification

**Key Concept**: The helper now replaces only the first match, and tests pass.

**Content**:
- fix: `count=1`
- `replace_tool_call()` limited to first match
- `replace_tool_call_raw()` limited to first match
- verification result: `7 passed`

**Visual Element**:
- Type: fix panel
- Subject: first tool-call box changed, later boxes preserved
- Treatment: green check, one changed box, two untouched boxes

**Text Labels**:
- Headline: "Fix and verification"
- Labels: "count=1", "only first match", "7 passed"

---

## Section 6: Main takeaway

**Key Concept**: Realistic anomalies require both believable replacements and bounded mutations.

**Content**:
- realism depends on `NEARBY_TOOLS`
- realism also depends on mutating only what you intended
- next improvement: expand nearby mappings or skip unmapped tools

**Visual Element**:
- Type: takeaway card
- Subject: two conditions feeding into one quality badge
- Treatment: simple summary with one next-step arrow

**Text Labels**:
- Headline: "What P1 taught us"
- Labels: "believable replacement", "bounded mutation", "next: improve mappings"

---

## Data Points (Verbatim)

### Key Terms
- "wrong_tool_choice"
- "read_file -> list_directory"
- "search_files -> search_files_v2"
- "terminal -> terminal_v2"
- "count=1"
- "7 passed"

---

## Design Instructions

### Style Preferences
- Technical and implementation-grounded
- Prefer larger labels and fewer words than the earlier dense context visual
- Use warnings only for the fallback weakness and the pre-fix over-mutation bug

### Layout Preferences
- Use a simple modular layout with clear before/after cards
- Keep the mapped example and the bug/fix contrast visually central

### Other Requirements
- `infographic.png` must be the generated canonical artifact
- Avoid text-heavy panels that are likely to garble in image generation
