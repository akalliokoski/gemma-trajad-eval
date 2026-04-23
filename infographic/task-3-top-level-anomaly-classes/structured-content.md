# Task 3 — Top-Level Anomaly Classes

## Overview
This infographic shows how the dataset builder now adds explicit top-level anomaly classes, preserves null classes for normal records, and validates the taxonomy end-to-end.

## Learning Objectives
The viewer will understand:
1. Why top-level anomaly classes were added.
2. How perturbation, build, and validation stages coordinate the new field.
3. What evidence shows the implementation works.

---

## Section 1: Motivation

**Key Concept**: Leaf anomaly labels alone were not enough to express the higher-level supervision target.

**Content**:
- Added top-level anomaly_class labels.
- Anomalous records now carry both anomaly_type and anomaly_class.
- Normal records keep anomaly_class=None.

**Visual Element**: Before/after labeling schema.
- Type: diagram
- Subject: leaf label only vs leaf label plus top-level class
- Treatment: blueprint cards with highlighted taxonomy arrows

**Text Labels**:
- Headline: "Make Taxonomy Explicit"
- Labels: "anomaly_type", "anomaly_class", "normal = None"

---

## Section 2: Mapping Logic

**Key Concept**: A single mapping table now converts anomaly_type into anomaly_class consistently.

**Content**:
- wrong_tool_choice → process_inefficiency
- bad_tool_arguments → task_failure
- repeated_step → process_inefficiency
- continued_after_sufficient_evidence → unwarranted_continuation
- skipped_required_step → task_failure

**Visual Element**: Mapping table schematic.
- Type: diagram
- Subject: anomaly subtype cards feeding top-level class buckets
- Treatment: engineering table with arrows and grouped destinations

**Text Labels**:
- Headline: "One Mapping Table"
- Labels: "task_failure", "process_inefficiency", "unwarranted_continuation"

---

## Section 3: Pipeline Behavior

**Key Concept**: Perturbation, build, and validation stages now agree on how the new field behaves.

**Content**:
- perturbations.py assigns anomaly_class to anomalous outputs.
- build_trajad_dataset.py ensures normal records keep anomaly_class=None.
- validate_labels.py enforces anomaly_class presence and validity for anomalous records and null for normal records.

**Visual Element**: Pipeline flow.
- Type: process diagram
- Subject: perturbations → build → validator
- Treatment: blueprint arrows with green validation checkpoint

**Text Labels**:
- Headline: "Three Stages Agree"
- Labels: "perturb", "build", "validate"

---

## Section 4: Verification

**Key Concept**: Tests, rebuild, and strict validation confirm the taxonomy change works at dataset scale.

**Content**:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py tests/test_perturbations.py -q
- 6 passed
- python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42
- Wrote 36,712 records
- python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
- All records valid

**Visual Element**: Verification board.
- Type: dashboard
- Subject: command snippets and result tiles
- Treatment: blueprint panels with prominent metrics

**Text Labels**:
- Headline: "Verified End-to-End"
- Labels: "6 passed", "36,712 records", "All valid"

---

## Data Points (Verbatim)
- "6 passed"
- "Wrote 36,712 records"
- "All records valid"
- "wrong_tool_choice → process_inefficiency"
- "skipped_required_step → task_failure"

---

## Design Instructions
- Use technical-schematic visual language.
- Use a clean engineering summary layout.
- Emphasize taxonomy mapping and validation evidence equally.
