# Task 4 — Lightweight Coherence Screen

## Overview
This infographic shows how the dataset builder now rejects obviously broken perturbed trajectories with a tiny deterministic screen while preserving intended anomaly coverage and same-seed reproducibility.

## Learning Objectives
The viewer will understand:
1. Why a coherence screen was added after perturbation.
2. Which structural pathologies it rejects.
3. How the builder preserves repeated_step coverage and reproducible split assignment.

---

## Section 1: Motivation

**Key Concept**: Direct perturbation is simple and useful, but it can create structurally broken traces that should not become training data.

**Content**:
- Add a lightweight post-perturbation quality gate.
- Keep the system deterministic and small.
- Avoid a full perturb-and-complete subsystem.

**Visual Element**: Problem/solution panel.
- Type: diagram
- Subject: direct perturbation alone vs direct perturbation plus coherence screen
- Treatment: engineering blueprint with red broken trace icon and green quality-gate icon

**Text Labels**:
- Headline: "Catch Broken Traces Early"
- Labels: "perturb", "screen", "keep it simple"

---

## Section 2: What the Screen Rejects

**Key Concept**: The screen only targets obvious structural failures.

**Content**:
- Reject dangling assistant tool calls with no immediate tool response.
- Reject orphan tool responses with no matching preceding assistant tool call.
- Reject exact adjacent duplicate fragments of the same message type.

**Visual Element**: Three rule cards.
- Type: diagram
- Subject: dangling call, orphan response, duplicate fragment
- Treatment: blueprint cards with red warning badges and compact message examples

**Text Labels**:
- Headline: "Three Deterministic Checks"
- Labels: "dangling_tool_call", "orphan_tool_response", "duplicate_adjacent_fragment"

---

## Section 3: Pipeline Integration

**Key Concept**: build_trajad_dataset.py screens every perturbed record immediately after apply_perturbation(...).

**Content**:
- apply_perturbation(...) creates a candidate anomaly.
- coherence.py returns (plausible, reason).
- Plausible anomalies are kept.
- Implausible anomalies are dropped and counted by rejection reason.

**Visual Element**: Pipeline flow.
- Type: process diagram
- Subject: perturbation → coherence.py → keep/drop counters → processed dataset
- Treatment: left-to-right engineering flow with a fork into green keep and red reject paths

**Text Labels**:
- Headline: "Screen Right After Perturbation"
- Labels: "apply_perturbation", "is_plausible_trajectory", "kept", "rejected"

---

## Section 4: Reproducibility and Coverage

**Key Concept**: The implementation also preserved repeated_step anomalies and fixed same-seed split determinism.

**Content**:
- build_trajad_dataset.py now uses unique_source_ids_in_order(records).
- Same-seed builds had no diff output.
- The coherence rule was narrowed so repeated_step anomalies from P4 remain plausible.
- repeated_step train count: 5,518.
- repeated_step test count: 1,104.

**Visual Element**: Dual evidence panel.
- Type: dashboard
- Subject: deterministic split assignment plus repeated_step coverage tiles
- Treatment: blueprint board with file-order icon, seed icon, and anomaly-count tiles

**Text Labels**:
- Headline: "Deterministic and Non-Destructive"
- Labels: "unique_source_ids_in_order", "no diff output", "5,518", "1,104"

---

## Section 5: Verification

**Key Concept**: Tests, rebuild, and strict validation confirm the Task 4 change is safe.

**Content**:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_coherence.py tests/test_perturbations.py tests/test_validate_labels.py tests/test_build_trajad_dataset.py -q
- 13 passed
- Generated 29,354 anomalous records
- Coherence screen: kept=29,354 rejected=0
- All records valid

**Visual Element**: Verification dashboard.
- Type: dashboard
- Subject: command snippets and result tiles
- Treatment: clean engineering monitor with bold pass/fact chips

**Text Labels**:
- Headline: "Verified End-to-End"
- Labels: "13 passed", "29,354 kept", "0 rejected", "All valid"

---

## Data Points (Verbatim)
- "13 passed"
- "Generated 29,354 anomalous records"
- "Coherence screen: kept=29,354 rejected=0"
- "repeated_step train count: 5,518"
- "repeated_step test count: 1,104"
- "All records valid"
- "no diff output for two same-seed builds"

---

## Design Instructions
- Use technical-schematic visual language.
- Keep the screen intentionally small and deterministic.
- Balance implementation logic with verification evidence.
- Make the keep/drop gate visually obvious.
