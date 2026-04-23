# Dataset builder codebase orientation

## Overview
This infographic explains how the `dataset_builder/` files fit together. It shows the flow from remote traces to local JSONL to normalized trajectories to anomalous variants to final splits, while highlighting the design contracts that keep the pipeline reproducible and leakage-safe.

## Learning Objectives
The viewer will understand:
1. which script owns which step
2. how data changes shape across the pipeline
3. why stable source IDs and variant suffixes matter
4. which parts of the taxonomy are still ahead of implementation

---

## Section 1: The six-file backbone

**Key Concept**: The codebase is intentionally split into small scripts with narrow jobs.

**Content**:
- `download_hermes.py`
- `inspect_traces.py`
- `normalize_trajectory.py`
- `perturbations.py`
- `build_trajad_dataset.py`
- `validate_labels.py`

**Visual Element**:
- Type: file-map panel
- Subject: six core scripts as connected modules
- Treatment: simple repository cards with arrows

**Text Labels**:
- Headline: "Six-file backbone"
- Subhead: "Small scripts, clear jobs"
- Labels: "download", "inspect", "normalize", "perturb", "build", "validate"

---

## Section 2: Raw data enters as JSONL

**Key Concept**: Downloading is only about freezing the source dataset locally.

**Content**:
- remote HF dataset
- `data/raw/hermes_filtered.jsonl`
- one JSON object per line
- no labels or schema rewriting yet

**Visual Element**:
- Type: ingress panel
- Subject: remote-to-local arrow ending at JSONL
- Treatment: download pipe into a raw-data box

**Text Labels**:
- Headline: "Raw ingestion"
- Subhead: "Freeze the source first"
- Labels: "HF dataset", "JSONL", "data/raw/"

---

## Section 3: Inspection is the microscope

**Key Concept**: `inspect_traces.py` reads plain Python dict/list objects and summarizes trajectory structure.

**Content**:
- `load_jsonl()` returns `list[dict]`
- detects `conversations`, `trajectory`, or `messages`
- detects `role/content` or `from/value`
- reports lengths, roles, tool calls, `<think>` usage

**Visual Element**:
- Type: analysis panel
- Subject: magnifying glass over trajectory records
- Treatment: summary counters and field-name chips

**Text Labels**:
- Headline: "Inspection layer"
- Subhead: "The codebase microscope"
- Labels: "list[dict]", "conversations", "trajectory", "messages"

---

## Section 4: Normalization creates the internal contract

**Key Concept**: Raw ShareGPT-like traces are converted into one consistent internal schema.

**Content**:
- `human -> user`
- `gpt -> assistant`
- `{from, value} -> {role, content}`
- metadata extraction
- derived fields: `trajectory_length`, `tool_call_count`, `tool_response_count`, `has_think`

**Visual Element**:
- Type: transformation panel
- Subject: before/after schema mapping
- Treatment: two-column raw-vs-normalized card

**Text Labels**:
- Headline: "Normalization contract"
- Subhead: "Translate once, rely on it everywhere"
- Labels: "role map", "metadata", "derived counts"

---

## Section 5: Identity and variants protect reproducibility

**Key Concept**: `source_trace_id` and variant suffixes keep trace families stable across builds.

**Content**:
- `source_trace_id`
- hash fallback when source ID is missing
- `var_00` = clean baseline
- `var_01+` = anomalous variants
- split by source trace, not by individual record

**Visual Element**:
- Type: guardrail module
- Subject: one source trace branching into variant family, then staying in one split bucket
- Treatment: family tree feeding one split bin

**Text Labels**:
- Headline: "Identity guardrail"
- Subhead: "Prevent leakage"
- Labels: "source_trace_id", "var_00", "var_01+", "same-family split"

---

## Section 6: Perturbation and build layer

**Key Concept**: The builder creates synthetic anomalies by applying rule functions, then assembles final splits and a manifest.

**Content**:
- `MVP_RULES`
- `ALL_RULES`
- surgical edits inside `<tool_call>` JSON
- coherence screening
- write `train.jsonl`, `dev.jsonl`, `test.jsonl`, `all.jsonl`
- write `build_manifest.json`

**Visual Element**:
- Type: process panel
- Subject: clean record -> rule application -> screened variants -> split outputs
- Treatment: left-to-right mini pipeline with outputs stack

**Text Labels**:
- Headline: "Build layer"
- Subhead: "Generate, screen, split, record"
- Labels: "MVP_RULES", "ALL_RULES", "manifest"

---

## Section 7: Validation checks structure, not realism

**Key Concept**: `validate_labels.py` enforces schema and some rule-aware bad-step semantics, but it is not a semantic judge.

**Content**:
- checks required fields and valid roles
- checks normal vs anomalous label consistency
- checks some rule-aware bad-step behavior
- does not guarantee human-like realism
- valid but unimplemented types: `hallucinated_tool`, `invalid_tool_json`, `unnecessary_replanning`

**Visual Element**:
- Type: boundary panel
- Subject: checkbox list plus "not covered" callout
- Treatment: green checks on one side, red exclusion bubble on the other

**Text Labels**:
- Headline: "Validator boundary"
- Subhead: "Structure yes, realism no"
- Labels: "schema", "bad_step", "not realism", "future anomaly types"

---

## Data Points (Verbatim)

### Key Terms
- "data/raw/"
- "source_trace_id"
- "var_00"
- "MVP_RULES"
- "ALL_RULES"
- "build_manifest.json"
- "hallucinated_tool"
- "invalid_tool_json"
- "unnecessary_replanning"

---

## Design Instructions

### Style Preferences
- highly legible technical infographic
- short labels, not dense prose
- code-oriented but approachable

### Layout Preferences
- dense modular layout
- arrows for data flow
- explicit before/after schema block

### Other Requirements
- preserve exact filenames and field names
- emphasize split safety and reproducibility
