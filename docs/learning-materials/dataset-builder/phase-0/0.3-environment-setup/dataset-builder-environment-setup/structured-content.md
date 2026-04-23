# Dataset builder environment setup

## Overview
This infographic explains the minimal environment needed to run the dataset-builder pipeline. It shows the generic repo contract, the VPS-specific `uv` adaptation, the verification checks that matter, and the three data directories that structure the pipeline.

## Learning Objectives
The viewer will understand:
1. the setup contract of the repo
2. when to use `venv + pip` and when `uv` is the safer host-specific choice
3. why imports and directory checks are the real proof of readiness
4. why HF authentication is optional for public download but useful later

---

## Section 1: Start with the repo contract

**Key Concept**: The setup target is a reproducible local environment, not a clever platform stack.

**Content**:
- Python 3.11+
- repo-local `.venv`
- install project dependencies
- keep the environment boring and local

**Visual Element**:
- Type: opening checklist
- Subject: four setup requirements
- Treatment: simple checklist card

**Text Labels**:
- Headline: "Repo contract"
- Subhead: "Small, reproducible, local"
- Labels: "Python 3.11+", ".venv", "deps", "boring is good"

---

## Section 2: Generic learning-plan path

**Key Concept**: The canonical repo-level setup is standard virtualenv plus editable install.

**Content**:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -e ".[dev]"`
- import smoke test

**Visual Element**:
- Type: step ladder
- Subject: four canonical setup steps
- Treatment: numbered sequence with shell chips

**Text Labels**:
- Headline: "Canonical path"
- Subhead: "Portable and easy to understand"
- Labels: "venv", "activate", "editable install", "import check"

---

## Section 3: VPS-specific adaptation

**Key Concept**: When system packaging is awkward, switch tools without changing the environment contract.

**Content**:
- system `python3` existed
- system `pip` under `/usr/bin/python3` was unavailable
- `uv` was available
- walkthrough used `uv venv .venv`
- walkthrough used `uv pip install ...`

**Visual Element**:
- Type: decision branch
- Subject: standard path vs `uv` fallback
- Treatment: fork diagram with `uv` highlighted for VPS

**Text Labels**:
- Headline: "Host-specific branch"
- Subhead: "Same contract, different tool"
- Labels: "venv + pip", "uv", "VPS path"

---

## Section 4: Verify readiness, not just command success

**Key Concept**: The environment is ready only when imports work.

**Content**:
- `import datasets, tqdm, pydantic`
- stronger practical checks can include `huggingface_hub`, `numpy`, `sklearn`
- successful imports matter more than nostalgic attachment to one installer

**Visual Element**:
- Type: verification panel
- Subject: pass/fail import checks
- Treatment: terminal card with green check badges

**Text Labels**:
- Headline: "Real verification"
- Subhead: "Imports beat assumptions"
- Labels: "datasets", "tqdm", "pydantic", "ready"

---

## Section 5: Hugging Face auth is later-facing setup

**Key Concept**: Login is useful, but not required to read the public filtered dataset.

**Content**:
- `pip install huggingface-hub`
- `huggingface-cli login`
- `huggingface-cli whoami`
- public dataset read path does not require auth
- upload/publication later does

**Visual Element**:
- Type: timing panel
- Subject: now vs later distinction for auth
- Treatment: split card showing optional-now and needed-later

**Text Labels**:
- Headline: "HF auth timing"
- Subhead: "Optional now, useful later"
- Labels: "public read", "publish later", "whoami"

---

## Section 6: Directory layout is part of the contract

**Key Concept**: The data pipeline expects three storage layers.

**Content**:
- `data/raw/`
- `data/interim/`
- `data/processed/`
- raw snapshot -> normalized records -> final split outputs

**Visual Element**:
- Type: directory tree panel
- Subject: three-layer data layout
- Treatment: folder tree with arrows between stages

**Text Labels**:
- Headline: "Pipeline storage layout"
- Subhead: "Raw -> interim -> processed"
- Labels: "raw", "interim", "processed"

---

## Data Points (Verbatim)

### Key Terms
- "requires-python = >=3.11"
- ".venv"
- `.[dev]`
- `uv`
- `huggingface-cli login`
- `data/raw/`
- `data/interim/`
- `data/processed/`

---

## Design Instructions

### Style Preferences
- simple and calming
- shell commands shown as short chips only
- low-density text inside the image

### Layout Preferences
- stepwise flow with one branch
- explicit folder-tree module
- strong visual distinction between generic path and VPS-specific path

### Other Requirements
- emphasize practical elegance over tooling ideology
- make the environment feel approachable
