# Dataset-builder implementation improvements after Phase 0

## Overview
This infographic explains how the current `dataset_builder/` should improve after Phase 0. It keeps the existing simple architecture, highlights the biggest quality gaps, maps the best next changes to concrete files, and shows the compute policy shift toward Modal serverless GPU as the default future GPU path.

## Learning Objectives
The viewer will understand:
1. that the current script-first builder should be improved rather than rewritten
2. that the biggest problem is data-quality discipline, not missing infrastructure
3. which concrete improvements should come first and why
4. that Modal serverless GPU is the default future GPU option and Apple Silicon is the secondary path

---

## Section 1: Keep the simple backbone

**Key Concept**: The existing architecture is fundamentally sound for a home AI lab.

**Content**:
- keep the current script-first pipeline
- normalization
- perturbation
- split assignment by source trace
- lightweight validation
- Improve the weak points instead of replacing the whole system.

**Visual Element**:
- Type: architecture panel
- Subject: preserved core pipeline blocks
- Treatment: four stable modules with a green "keep" banner

**Text Labels**:
- Headline: "Keep the simple backbone"
- Subhead: "Do not rewrite what already works"
- Labels: "normalize", "perturb", "split safely", "validate"

---

## Section 2: The real gap is data quality discipline

**Key Concept**: The main implementation problem is not missing infrastructure. It is trustworthiness of synthetic trajectories.

**Content**:
- data quality discipline
- direct perturbation only
- some anomalies can become internally inconsistent
- realistic bad trajectories matter more than extra architecture

**Visual Element**:
- Type: tension panel
- Subject: simple pipeline vs unrealistic anomalies
- Treatment: contrast card showing why quality beats extra infrastructure

**Text Labels**:
- Headline: "Main gap"
- Subhead: "Quality, not platform sprawl"
- Labels: "direct perturbation only", "coherence risk", "trustworthy labels"

---

## Section 3: Phase 0 findings that drive the roadmap

**Key Concept**: The learning materials already revealed the implementation constraints.

**Content**:
- raw ShareGPT-like `{from, value}` format
- serialized `<tool_call>` and `<tool_response>` markup
- typical traces are about 32 messages long
- tool use is effectively universal

**Visual Element**:
- Type: evidence block
- Subject: four grounded findings from Phase 0
- Treatment: compact cards with one finding per card

**Text Labels**:
- Headline: "Phase 0 findings"
- Subhead: "The code should follow the data"
- Labels: "{from, value}", "<tool_call>", "~32 messages", "tool-heavy corpus"

---

## Section 4: Highest-priority implementation upgrades

**Key Concept**: The best next improvements are small, practical, and code-adjacent.

**Content**:
- raw-schema-safe inspection
- lightweight coherence screening
- explicit anomaly classes
- improve P5 and P6 realism
- rule-aware localization validation
- build manifests and perturbation diagnostics

**Visual Element**:
- Type: ranked roadmap
- Subject: six priority upgrades in descending order
- Treatment: numbered ladder or stacked modules with code-file callouts

**Text Labels**:
- Headline: "Priority roadmap"
- Subhead: "Small changes, big quality gain"
- Labels: "inspection", "coherence", "taxonomy", "realism", "bad-step checks", "manifests"

---

## Section 5: Concrete file map

**Key Concept**: The roadmap is implementable because each improvement maps to a small number of files.

**Content**:
- `dataset_builder/inspect_traces.py`
- `dataset_builder/normalize_trajectory.py`
- `dataset_builder/perturbations.py`
- `dataset_builder/build_trajad_dataset.py`
- `dataset_builder/validate_labels.py`
- `tests/`

**Visual Element**:
- Type: code map
- Subject: file list tied to the improvements
- Treatment: compact repository diagram with arrows from improvement names to files

**Text Labels**:
- Headline: "Where the changes go"
- Subhead: "Specific files, not vague architecture talk"
- Labels: "inspect", "normalize", "perturb", "build", "validate", "tests"

---

## Section 6: Best-practice guardrails

**Key Concept**: The plan follows practical engineering principles instead of future-proofing theater.

**Content**:
- YAGNI
- DRY
- determinism
- reproducibility
- explainability
- practical, elegant, and understandable

**Visual Element**:
- Type: principles strip
- Subject: six engineering guardrails
- Treatment: badge row or mini cards with concise one-line meanings

**Text Labels**:
- Headline: "Best-practice guardrails"
- Subhead: "Simple on purpose"
- Labels: "YAGNI", "DRY", "deterministic", "reproducible", "explainable"

---

## Section 7: Compute policy update

**Key Concept**: Future GPU-backed extensions should default to Modal, not local Apple Silicon.

**Content**:
- Modal serverless GPU is now the default future GPU tier
- Apple Silicon is secondary
- Tasks in this plan are still VPS CPU-friendly
- If future model-assisted continuation is added, start with Modal first

**Visual Element**:
- Type: decision module
- Subject: compute-tier policy
- Treatment: highlighted default path with a clear primary/secondary split

**Text Labels**:
- Headline: "Compute policy"
- Subhead: "Modal first for GPU work"
- Labels: "Modal default", "Apple Silicon secondary", "VPS for current tasks"

---

## Data Points (Verbatim)

All statistics, phrases, and quotes exactly as they appear in source:

### Key Phrases
- "keep the current script-first pipeline"
- "data quality discipline"
- "raw-schema-safe inspection"
- "lightweight coherence screening"
- "explicit anomaly classes"
- "rule-aware localization validation"
- "build manifests and perturbation diagnostics"
- "Modal serverless GPU is now the default future GPU tier"
- "Apple Silicon is secondary"
- "practical, elegant, and understandable"

---

## Design Instructions

Extracted from user's steering prompt:

### Style Preferences
- Detailed but practical
- Technical and educational
- Anti-overengineering
- Emphasize why each change is chosen

### Layout Preferences
- Use a dense modular layout that can show priorities, principles, file map, and compute policy in one view
- Make the roadmap easy to scan

### Other Requirements
- Base the media on the plan and analysis
- Reflect the Modal-first GPU default explicitly
- Keep the output simple, elegant, and grounded in current repo reality
