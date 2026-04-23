# Task 1 — Raw Trace Inspection Repair

## Overview
This infographic shows how the raw trace inspection path was repaired to support real ShareGPT-style Hermes data and how the fix was verified on both tests and the raw dataset.

## Learning Objectives
The viewer will understand:
1. What broke in the original inspection path.
2. Which code changes restored compatibility.
3. What verification evidence confirms the fix.

---

## Section 1: Problem

**Key Concept**: The raw dataset used a different message schema than the inspection script expected.

**Content**:
- Objective: Make the inspection path trustworthy on the real raw dataset before deeper changes.
- dataset_builder/inspect_traces.py supports both role/content and from/value message schemas.
- The original failure mode was a broken assumption around role/content on raw data.

**Visual Element**: Broken schema mismatch diagram.
- Type: diagram
- Subject: two message schema boxes converging into one inspection tool
- Treatment: red warning on mismatch, green arrow on compatibility layer

**Text Labels**:
- Headline: "Broken Assumption"
- Labels: "role/content", "from/value", "inspect_traces.py"

---

## Section 2: Implementation

**Key Concept**: Small compatibility helpers fixed the traversal path without redesigning the script.

**Content**:
- Added helpers get_role(msg) and get_content(msg).
- count_roles(), print_summary(), and print_sample() use the helpers.
- Summary now reports traces with >=1 tool call and traces with >=2 assistant/tool-call pairs.

**Visual Element**: Function patch map.
- Type: diagram
- Subject: helper functions feeding three inspection functions
- Treatment: blueprint-style callout boxes

**Text Labels**:
- Headline: "Minimal Fix"
- Labels: "get_role", "get_content", "count_roles", "print_summary", "print_sample"

---

## Section 3: Verification

**Key Concept**: The implementation was checked with targeted tests and the real raw JSONL file.

**Content**:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_inspect_traces.py -v
- python3 dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl
- Tests passed: 5
- Total records: 3,679
- Traces with >=1 tool call: 100.0%
- Traces with >=2 assistant/tool-call pairs: 99.4%

**Visual Element**: Verification board.
- Type: dashboard
- Subject: command snippets and numeric result tiles
- Treatment: blueprint boxes with large metrics

**Text Labels**:
- Headline: "Verified on Real Data"
- Labels: "5 passed", "3,679 records", "100.0%", "99.4%"

---

## Data Points (Verbatim)
- "Tests passed: 5"
- "Total records: 3,679"
- "Traces with >=1 tool call: 100.0%"
- "Traces with >=2 assistant/tool-call pairs: 99.4%"

---

## Design Instructions
- Use technical-schematic visual language.
- Use a clean engineering summary layout.
- Emphasize implementation and verification equally.
