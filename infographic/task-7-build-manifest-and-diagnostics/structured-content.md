# Task 7 — Build Manifest and Diagnostics

## Overview
This infographic shows how the dataset builder now writes a durable build manifest and prints a concise diagnostics summary so each build is reproducible and easy to inspect.

## Learning Objectives
The viewer will understand:
1. Why build counts should be saved, not only printed.
2. What information the new manifest records.
3. What verification evidence shows the new reproducibility layer works on the real dataset.

---

## Section 1: Why Task 7 Exists

**Key Concept**: printed counts are useful during a run, but a saved artifact is what makes a build reproducible later.

**Content**:
- The builder already printed useful counts.
- It did not save them.
- Task 7 adds a durable manifest without changing the script-first architecture.

**Visual Element**: before/after panel.
- Type: comparison
- Subject: console-only output vs saved manifest artifact
- Treatment: left ephemeral terminal card, right persistent JSON artifact card

**Text Labels**:
- Headline: "From Ephemeral Counts to Durable Build State"
- Labels: "stdout only", "build_manifest.json", "reproducible"

---

## Section 2: What the Manifest Records

**Key Concept**: the manifest captures the build inputs, outputs, and diagnostics that matter for later inspection.

**Content**:
- seed
- rules_used
- source_input_paths
- split_counts
- anomaly_type_counts
- anomaly_class_counts
- perturbation_failures_by_rule
- coherence_rejections_by_rule
- coherence_rejection_reasons

**Visual Element**: artifact schema card.
- Type: modules
- Subject: one JSON manifest card with nested sections
- Treatment: blueprint file card with grouped field chips

**Text Labels**:
- Headline: "Manifest Contents"
- Labels: "seed", "rules_used", "split_counts", "anomaly counts", "failures", "rejections"

---

## Section 3: Runtime Diagnostics

**Key Concept**: the command stays pleasant to use because the builder still prints a compact summary after writing files.

**Content**:
- Added format_manifest_summary(...).
- Summary prints seed, rules used, split counts, totals, anomaly counts, failures, and rejection reasons.
- Manifest path: data/processed/build_manifest.json.

**Visual Element**: dashboard panel.
- Type: dashboard
- Subject: summary panel with key chips and manifest path callout
- Treatment: engineering monitor with bold metric chips

**Text Labels**:
- Headline: "Human-Friendly Diagnostics"
- Labels: "seed 42", "rules used 8", "47,973 / 6,413 / 9,696", "build_manifest.json"

---

## Section 4: Tests and Files

**Key Concept**: the reproducibility layer is protected with focused tests and a narrow code footprint.

**Content**:
- Added tests/test_build_manifest.py.
- Tests cover manifest contents and summary formatting.
- Updated dataset_builder/build_trajad_dataset.py.

**Visual Element**: file/test panel.
- Type: modules
- Subject: code file, test file, manifest artifact
- Treatment: blueprint module cards with check badges

**Text Labels**:
- Headline: "Small Change Surface"
- Labels: "build_trajad_dataset.py", "test_build_manifest.py", "build_manifest.json"

---

## Section 5: Verification

**Key Concept**: the manifest workflow passes targeted tests, writes the real artifact, and still produces a strictly valid dataset.

**Content**:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_build_manifest.py -v
- 2 passed
- python3 dataset_builder/build_trajad_dataset.py --seed 42
- Generated 56,724 anomalous records
- Coherence screen: kept=56,724 rejected=0
- Split sizes: train=47,973  dev=6,413  test=9,696
- normal=7,358 anomalous=56,724 all=64,082
- python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
- Validated 64,082 records from data/processed/all.jsonl
- All records valid.

**Visual Element**: verification dashboard.
- Type: dashboard
- Subject: pass chips and dataset metrics
- Treatment: clean engineering summary with bold exact numbers

**Text Labels**:
- Headline: "Verified End-to-End"
- Labels: "2 passed", "56,724 anomalies", "0 rejected", "64,082 valid"

---

## Data Points (Verbatim)
- "2 passed"
- "Generated 56,724 anomalous records"
- "Coherence screen: kept=56,724 rejected=0"
- "Split sizes: train=47,973  dev=6,413  test=9,696"
- "normal=7,358 anomalous=56,724 all=64,082"
- "Validated 64,082 records from data/processed/all.jsonl"
- "All records valid."
- "build_manifest.json"

---

## Design Instructions
- Use technical-schematic visual language.
- Make the manifest artifact and saved-path concept visually obvious.
- Preserve the exact verification numbers.
- Final artifact must be PNG.
