# Hermes normalization deep dive

## Overview
This infographic explains how `normalize_trajectory.py` turns raw Hermes traces into the repo’s internal trajectory format. It combines successful run verification, raw-vs-normalized comparison, role mapping, metadata enrichment, source-ID stability, edge-case findings, and the main project-level takeaway.

## Learning Objectives
The viewer will understand:
1. that normalization is the schema bridge from raw traces to the internal dataset contract
2. that `source_trace_id` stability is critical for leakage-safe splitting later
3. that the current corpus is clean enough that several hypothetical edge cases do not actually fire in practice

---

## Section 1: Run result

**Key Concept**: Normalization succeeded cleanly on the full real corpus.

**Content**:
- `uv run python dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized_phase2.jsonl`
- `3,679` records written
- `0` errors
- output file: `data/interim/hermes_normalized_phase2.jsonl`

**Visual Element**:
- Type: number highlight
- Subject: command plus success summary panel
- Treatment: command chip, output-path chip, and large success metrics

**Text Labels**:
- Headline: "Normalization succeeded"
- Subhead: "Full-corpus run on real raw data"
- Labels: "3,679 records", "0 errors", "hermes_normalized_phase2.jsonl"

---

## Section 2: Raw vs normalized shape

**Key Concept**: The script converts ShareGPT-style raw traces into a cleaner internal trajectory contract.

**Content**:
- raw message shape: `{from, value}`
- normalized message shape: `{role, content}`
- raw top-level context includes `id`, `conversations`, `tools`, `category`, `subcategory`, `task`
- normalized record adds `source_trace_id`, `trajectory`, clean-label fields, and `metadata`

**Visual Element**:
- Type: split comparison
- Subject: raw record card beside normalized record card
- Treatment: left-right structural comparison with key field highlights

**Text Labels**:
- Headline: "Raw vs normalized"
- Subhead: "What changes in the record contract"
- Labels: "{from, value}", "{role, content}", "source_trace_id", "metadata"

---

## Section 3: Role mapping

**Key Concept**: Role normalization is a central part of the transformation, not a cosmetic rename.

**Content**:
- `system` -> `system`
- `human` -> `user`
- `gpt` -> `assistant`
- `tool` -> `tool`
- raw roles observed: `gpt`, `human`, `system`, `tool`
- normalized roles observed: `assistant`, `user`, `system`, `tool`

**Visual Element**:
- Type: mapping diagram
- Subject: raw-role chips pointing to normalized-role chips
- Treatment: arrow-based schema mapping panel

**Text Labels**:
- Headline: "Role mapping"
- Subhead: "The assistant/user schema becomes explicit"
- Labels: "human -> user", "gpt -> assistant", "system", "tool"

---

## Section 4: Clean defaults and metadata

**Key Concept**: Normalization initializes clean labels and enriches metadata without complicating the trajectory object.

**Content**:
- clean defaults:
  - `is_anomalous=false`
  - `anomaly_type=null`
  - `bad_step=null`
  - `generation_rule=null`
- metadata keys include:
  - `category`
  - `subcategory`
  - `trajectory_length`
  - `tool_call_count`
  - `tool_response_count`
  - `has_think`

**Visual Element**:
- Type: checklist / chips panel
- Subject: clean-default flags beside metadata chips
- Treatment: compact boolean and field chips

**Text Labels**:
- Headline: "Simple trajectory, richer metadata"
- Subhead: "Labels start clean; structure gets summarized"
- Labels: "is_anomalous=false", "anomaly_type=null", "trajectory_length", "tool_call_count", "has_think"

---

## Section 5: Why source_trace_id matters

**Key Concept**: Stable source IDs are the hidden prerequisite for trustworthy split assignment later.

**Content**:
- `source_trace_id` preserves the underlying clean trace family
- if `id` or `source_id` exists, it is reused
- otherwise a deterministic content hash is used
- stability check result: `stable_on_repeat: true`

**Visual Element**:
- Type: concept panel
- Subject: stable trace-family identity flowing into later split assignment
- Treatment: identity badge plus arrow toward train/dev/test discipline

**Text Labels**:
- Headline: "Stable trace identity"
- Subhead: "Why split discipline depends on normalization"
- Labels: "source_trace_id", "stable_on_repeat: true", "trace family", "leakage-safe splitting"

---

## Section 6: Edge-case audit

**Key Concept**: The current corpus is cleaner than the hypothetical edge cases suggested in the plan.

**Content**:
- `missing_category_count: 0`
- `missing_subcategory_count: 0`
- `empty_metadata_count: 0`
- no non-standard raw roles were observed in this corpus snapshot

**Visual Element**:
- Type: audit panel
- Subject: edge-case counts and verdict badges
- Treatment: zero-count badges with a short note that the graceful path still matters

**Text Labels**:
- Headline: "Edge-case audit"
- Subhead: "This corpus does not stress missing metadata much"
- Labels: "0 missing category", "0 missing subcategory", "0 empty metadata", "no unknown roles"

---

## Section 7: Main takeaway

**Key Concept**: Normalization is the schema bridge that makes perturbation, validation, and later learning trustworthy.

**Content**:
- the trajectory object stays intentionally simple
- the role contract becomes consistent
- stable source IDs protect later splitting
- structural signals are preserved in metadata
- next step: Phase 3 perturbation engine

**Visual Element**:
- Type: takeaway module
- Subject: four guarantees plus one next-step arrow
- Treatment: bold summary card with a single forward pointer

**Text Labels**:
- Headline: "Why this script matters"
- Subhead: "Normalization carries real data-quality guarantees"
- Labels: "schema bridge", "simple trajectory", "stable source IDs", "next: perturbation engine"

---

## Data Points (Verbatim)

### Statistics
- "3,679"
- "0"
- "stable_on_repeat: true"
- "missing_category_count: 0"
- "missing_subcategory_count: 0"
- "empty_metadata_count: 0"

### Key Terms
- "{from, value}"
- "{role, content}"
- "source_trace_id"
- "trajectory_length"
- "tool_call_count"
- "tool_response_count"
- "has_think"

---

## Design Instructions

### Style Preferences
- Technical and implementation-grounded
- Emphasize guarantees and implications more than low-level busy detail
- Prefer readable headings and chips over prose-heavy panels

### Layout Preferences
- Use a dense modular layout that can hold comparison, mapping, guarantees, and audit findings together
- Keep the side-by-side raw-vs-normalized comparison visually central

### Other Requirements
- `infographic.png` must be the generated canonical artifact
- Make the asset feel like a debrief of what normalization guarantees in practice
