# Task 2 — Derived Structural Metadata

## Overview
This infographic shows how the normalization stage now derives structural metadata from tool-heavy trajectories while preserving the simple normalized message schema.

## Learning Objectives
The viewer will understand:
1. Why cheap structural metadata is useful.
2. Which fields were added and where.
3. How the change was verified.

---

## Section 1: Motivation

**Key Concept**: The pipeline needed to keep more signal about tool-heavy trajectories without redesigning the schema.

**Content**:
- Objective: Preserve more useful signal about tool-heavy trajectories without redesigning the schema.
- Core trajectory item shape remains {"role": ..., "content": ...}.
- Derived metadata includes trajectory_length, tool_call_count, tool_response_count, has_think.

**Visual Element**: Before/after schema card.
- Type: diagram
- Subject: unchanged trajectory list beside enriched metadata map
- Treatment: blueprint cards with highlighted metadata box

**Text Labels**:
- Headline: "Keep Schema Simple"
- Labels: "trajectory", "metadata", "role/content"

---

## Section 2: Implementation

**Key Concept**: A small helper computes the metadata and normalize_record merges it into existing metadata.

**Content**:
- Added derive_trace_metadata(trajectory) in dataset_builder/normalize_trajectory.py.
- normalize_record() merges derived metadata into existing metadata.
- Existing source metadata is preserved.

**Visual Element**: Function flow map.
- Type: diagram
- Subject: trajectory input → derive_trace_metadata → metadata update → normalized record
- Treatment: technical schematic with arrows and callouts

**Text Labels**:
- Headline: "Cheap Derived Signals"
- Labels: "trajectory_length", "tool_call_count", "tool_response_count", "has_think"

---

## Section 3: Verification

**Key Concept**: Tests and a normalization smoke test confirm the new metadata is emitted correctly.

**Content**:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_normalize_trajectory.py -v
- python3 dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized.jsonl
- Tests passed: 2
- Normalized 3,679 records → data/interim/hermes_normalized.jsonl (0 errors)
- Example metadata: trajectory_length 13; tool_call_count 11; tool_response_count 10; has_think True

**Visual Element**: Verification board.
- Type: dashboard
- Subject: command snippets and metadata example tiles
- Treatment: blueprint boxes with highlighted numbers

**Text Labels**:
- Headline: "Verified on Smoke Run"
- Labels: "2 passed", "3,679 records", "0 errors", "13 / 11 / 10 / True"

---

## Data Points (Verbatim)
- "Tests passed: 2"
- "Normalized 3,679 records → data/interim/hermes_normalized.jsonl (0 errors)"
- "trajectory_length"
- "tool_call_count"
- "tool_response_count"
- "has_think"

---

## Design Instructions
- Use technical-schematic visual language.
- Use a clean engineering summary layout.
- Emphasize schema preservation and metadata enrichment.
