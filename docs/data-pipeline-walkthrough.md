# Data Pipeline Walkthrough

Date: 2026-04-17
Execution tier: VPS
Why this tier: the work was lightweight setup, download, normalization, perturbation, validation, and debugging. It did not justify Mac resource usage and did not require Modal.

## Goal

Make the first end-to-end dataset pipeline runnable and verified on the VPS.

## Starting state

Before this run:
- the repo had dataset-builder scripts but no `data/` artifacts
- the VPS environment did not have the required dataset dependencies available in a project virtualenv
- the codebase baseline suggested the dataset pipeline was the best next slice

## Context note

We did not need to compress context first in a special way before starting this slice.

Reason:
- the important project context had already been externalized into repo docs and wiki pages
- `AGENTS.md`, `README.md`, `docs/execution-topology.md`, `docs/codebase-baseline.md`, and the repo-local wiki were already serving as working memory

## Environment setup

### Findings
- system `python3` existed on the VPS
- system `pip` module was not available under `/usr/bin/python3`
- `uv` was available at `/home/hermes/.local/bin/uv`

### Decision
Use `uv` to create a repo-local virtualenv instead of trying to repair the system Python.

### Commands used

```bash
uv venv .venv
. .venv/bin/activate
uv pip install setuptools wheel datasets huggingface_hub jsonlines tqdm pydantic transformers tokenizers scikit-learn numpy pytest
```

## Pipeline commands used

### 1. Download filtered Hermes traces

```bash
. .venv/bin/activate
python dataset_builder/download_hermes.py --dataset filtered
```

Result:
- downloaded `DJLougen/hermes-agent-traces-filtered`
- wrote `data/raw/hermes_filtered.jsonl`
- saved 3,679 rows

### 2. Inspect raw traces

First attempt:

```bash
. .venv/bin/activate
python dataset_builder/inspect_traces.py --input data/raw/hermes_filtered.jsonl --sample 2
```

Result:
- failed because the script expects a positional `path` argument, not `--input`

Correct command:

```bash
. .venv/bin/activate
python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --sample 2
```

Observed result:
- script began summarizing records
- then failed with `KeyError: 'role'`

Root cause:
- the raw dataset uses ShareGPT-style message fields like `from` and `value`
- `inspect_traces.py` assumes each message already has `role` and `content`

Practical outcome for this slice:
- inspection is currently not robust against raw ShareGPT-style input
- we moved forward with normalization, because normalization is explicitly designed for this schema

### 3. Normalize raw traces

```bash
mkdir -p data/interim data/processed
. .venv/bin/activate
python dataset_builder/normalize_trajectory.py \
  data/raw/hermes_filtered.jsonl \
  data/interim/hermes_filtered.normalized.jsonl
```

Result:
- normalized 3,679 records
- wrote `data/interim/hermes_filtered.normalized.jsonl`
- reported 0 errors

### 4. Build MVP processed dataset

Initial command:

```bash
. .venv/bin/activate
python dataset_builder/build_trajad_dataset.py --mvp
```

Initial result:
- failed during perturbation generation with:
  - `re.error: bad escape \u`

Root cause:
- `dataset_builder/perturbations.py` used `re.sub(replacement_string, ...)`
- the replacement string contained JSON escapes such as `\u2713`
- Python regex replacement strings interpret backslash escapes, so JSON-escaped Unicode triggered the failure

Fix applied:
- changed `replace_tool_call()` to use a lambda replacement instead of passing JSON text directly as the regex replacement string

Regression test added:
- `tests/test_perturbations.py`
- verifies `replace_tool_call()` works when JSON contains unicode escapes

Re-run:

```bash
. .venv/bin/activate
python dataset_builder/build_trajad_dataset.py --mvp
```

Successful result:
- loaded 3,679 normal records
- generated 14,676 anomalous records
- wrote:
  - `data/processed/train.jsonl` with 13,767 records
  - `data/processed/dev.jsonl` with 1,833 records
  - `data/processed/test.jsonl` with 2,755 records
  - `data/processed/all.jsonl` with 18,355 records

## Validation

Initial strict validation:

```bash
. .venv/bin/activate
python dataset_builder/validate_labels.py data/processed/train.jsonl --strict
```

Initial result:
- failed with multiple `bad_step out of range` errors
- all observed failures were `*_var_03` records, i.e. P3 / `skipped_required_step`

Root cause:
- repo labeling guidance says `skipped_required_step` should use:
  - the step immediately after the last valid step
- for trajectories where the missing step would have been at the end, `bad_step == len(trajectory)` is valid by project semantics
- `validate_labels.py` incorrectly required `bad_step < len(traj)` for every anomaly type

Fix applied:
- updated `validate_labels.py` so `skipped_required_step` accepts `0 <= bad_step <= len(traj)`
- kept stricter in-range validation for other anomaly types

Regression test added:
- `tests/test_perturbations.py` now also checks that validator behavior allows the end-of-trajectory missing-step index

Test command:

```bash
. .venv/bin/activate
PYTHONPATH=. pytest tests/test_perturbations.py -q
```

Result:
- `2 passed`

Final validation commands:

```bash
. .venv/bin/activate
python dataset_builder/validate_labels.py data/processed/train.jsonl --strict
python dataset_builder/validate_labels.py data/processed/dev.jsonl --strict
python dataset_builder/validate_labels.py data/processed/test.jsonl --strict
```

Final result:
- all three splits validated successfully

## Files created

Artifacts:
- `data/raw/hermes_filtered.jsonl`
- `data/interim/hermes_filtered.normalized.jsonl`
- `data/processed/train.jsonl`
- `data/processed/dev.jsonl`
- `data/processed/test.jsonl`
- `data/processed/all.jsonl`

Docs/tests:
- `docs/data-pipeline-walkthrough.md`
- `tests/test_perturbations.py`

## Files modified

- `dataset_builder/perturbations.py`
- `dataset_builder/validate_labels.py`

## What was verified

Verified directly by commands and test runs:
- filtered Hermes traces can be downloaded from Hugging Face on the VPS
- raw traces can be normalized successfully
- MVP perturbation build completes successfully after the regex replacement fix
- processed outputs are produced for train/dev/test/all
- strict label validation passes after aligning validator logic with project labeling semantics
- regression tests pass for both fixes

## Important follow-up work

1. Fix `dataset_builder/inspect_traces.py` so it can handle raw ShareGPT-style `from/value` message schema.
2. Add per-rule perturbation diagnostics and success-rate reporting.
3. Run `training/prepare_sft_data.py` next on the processed dataset, likely still on the VPS.
4. Only consider Mac-side local experiments after the data handoff to training is clean.

## Recommendation for the next slice

Next best move:
- prepare binary-task SFT data from the processed dataset
- document that handoff
- then inspect what remains before the first bounded local training smoke test
