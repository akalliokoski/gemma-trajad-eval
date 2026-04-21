# Codebase Baseline

Date: 2026-04-17

This document captures the current baseline of the repository after the Hermes-first pivot and before the first substantial implementation slice.

## Executive summary

The repo already contains a coherent skeleton for:
- dataset building from Hermes traces
- SFT data preparation
- local-first Gemma fine-tuning
- later Unsloth/GPU fine-tuning
- inference and evaluation
- demo integrations with observability/agent frameworks

The codebase is not yet runnable end-to-end.

The most important near-term fact is this:
- the data pipeline is the real starting point
- training and integrations mostly depend on artifacts that the data pipeline does not yet produce in this checkout
- the next implementation slice should stay on the VPS and make the tiny dataset pipeline runnable on a small sample

Likely execution tier for the next slice: VPS.

Why:
- this is primarily dependency wiring, small data processing, and verification work
- it does not yet justify a disruptive Mac workload
- it definitely does not require Modal yet

## Current top-level assessment

### What looks structurally strong
- clear directory separation: `dataset_builder/`, `training/`, `integrations/`, `prompts/`, `docs/`
- practical script-oriented workflow instead of overengineered framework code
- useful prompt templates already exist
- anomaly taxonomy and evaluation intent are documented
- training stack already reflects local-first + later-cloud split

### What blocks end-to-end execution today
- no `data/processed/*.jsonl` artifacts exist yet
- repo environment on this VPS is missing key runtime packages for some paths
- some docs and code contracts are out of sync
- integrations are mostly demos, not yet validated reusable workflows
- there are no tests for the major pipeline pieces

## Baseline by area

## 1. Dataset builder

Files inspected:
- `dataset_builder/download_hermes.py`
- `dataset_builder/inspect_traces.py`
- `dataset_builder/normalize_trajectory.py`
- `dataset_builder/perturbations.py`
- `dataset_builder/build_trajad_dataset.py`
- `dataset_builder/validate_labels.py`

### What exists
The dataset builder is the most concrete end-to-end path in the repo.

It already covers:
- Hugging Face trace download into JSONL
- raw-trace inspection/EDA
- normalization into an internal trajectory format
- synthetic perturbation-based anomaly generation
- train/dev/test splitting by `source_trace_id`
- label/schema validation

The perturbation module already implements 8 rules and `build_trajad_dataset.py` can assemble processed train/dev/test/all JSONL outputs.

### What appears runnable
Runnable now on the VPS:
- CLI help for the dataset-builder scripts
- syntax validation for all files
- `build_trajad_dataset.py --mvp` reaches its guard rails correctly

Blocked but close:
- `download_hermes.py` currently fails because the active VPS environment does not have the `datasets` package installed
- `build_trajad_dataset.py` cannot proceed because `data/interim/*.jsonl` does not exist yet

### Gaps
- no `data/` artifacts in the repo checkout yet
- no tests for dataset generation or validation
- `validate_labels.py` allows anomaly types that `perturbations.py` does not yet generate:
  - `hallucinated_tool`
  - `invalid_tool_json`
  - `unnecessary_replanning`
- no per-rule perturbation diagnostics or success-rate reporting
- no dedicated manual-review helper for generated anomalies

### Assessment
The dataset builder is the strongest place to start. It is closest to producing real artifacts and unblocks everything else.

## 2. Training

Files inspected:
- `training/prepare_sft_data.py`
- `training/train_e2b.py`
- `training/train_e4b.py`
- `training/inference.py`
- `training/evaluate.py`

### What exists
The training directory has a clear intended ladder:
- convert processed dataset records into chat-style SFT files
- run local Apple-Silicon-oriented training for Gemma E2B
- run later Unsloth/NVIDIA-oriented training for Gemma E4B
- run inference over single or batch trajectories
- compute evaluation metrics over predictions vs ground truth

### What appears runnable
Runnable now on the VPS:
- `prepare_sft_data.py` runs, but only as a no-op because `data/processed/*.jsonl` is missing
- `inference.py --help` works

Not runnable in current VPS environment:
- `train_e2b.py` requires `mlx_tune`
- `train_e4b.py` requires `unsloth`
- `evaluate.py` requires `scikit-learn`

### Gaps
- no processed dataset means the full training handoff is blocked
- `train_e2b.py` and `train_e4b.py` import heavy backend dependencies at module import time, so even `--help` breaks when those deps are missing
- `inference.py` single-run mode hardcodes a joint-task prompt path that does not match the training formatting as cleanly as it should
- `docs/evaluation-plan.md` appears out of sync with the actual `evaluate.py` CLI
- `pyproject.toml` likely does not yet fully describe all practical training dependencies for the intended workflows

### Assessment
The training code is a useful skeleton, but it is downstream of the dataset pipeline. The right near-term move is not “run training”; it is “make binary-task smoke testing possible once processed data exists.”

## 3. Integrations

Files inspected:
- `integrations/langfuse_demo.py`
- `integrations/smolagents_demo.py`
- `integrations/phoenix_openinference_demo.py`

### What exists
The integrations directory contains demo-style scripts for:
- Langfuse trace scoring and writeback
- smolagents run-to-trajectory conversion and local scoring
- Phoenix/OpenInference-style trace annotation

These scripts show the intended downstream value of the project: trajectory scoring that plugs into real agent tooling.

### What appears runnable
Structurally:
- scripts compile
- CLI help works

Operationally on the VPS right now:
- none are runnable end-to-end because required packages and/or backends are missing
- default adapter paths under `outputs/adapters/...` do not exist yet
- live external services are not configured for these demos

### Gaps
- shared scoring logic is duplicated across demo scripts
- no offline fixtures or conversion tests exist
- no dry-run mode for validating conversion/annotation payloads without model execution
- dependency declarations look incomplete for at least some integration imports
- integrations are demos rather than a reusable internal integration layer

### Assessment
These should not be the first implementation slice. The right move is to revisit them after the data and local evaluation path are more grounded.

## Environment findings from this VPS

Observed directly or via script execution:
- `tailscale` is installed on the VPS and running
- the Mac is visible on the tailnet
- `syncthing` CLI was not found in the VPS shell PATH
- missing Python/runtime pieces in the current VPS environment include at least:
  - `datasets`
  - `mlx_tune`
  - `unsloth`
  - `scikit-learn`
  - several integration-related packages depending on which demo is used

This reinforces the current workload-placement rule:
- keep the next slice on the VPS
- do not push compute-heavy work to the Mac yet
- do not start Modal setup yet

## Best next implementation slice

### Recommended slice
Make the tiny end-to-end data pipeline runnable on the VPS.

### Concrete objective
Produce and validate a small processed dataset sample that can later feed the binary SFT path.

### Suggested sequence
1. ensure the repo environment has the minimum dataset-builder dependencies needed on the VPS
2. run `dataset_builder/download_hermes.py` for the filtered dataset
3. inspect downloaded traces with `dataset_builder/inspect_traces.py`
4. normalize them with `dataset_builder/normalize_trajectory.py`
5. run `dataset_builder/build_trajad_dataset.py --mvp`
6. validate the output with `dataset_builder/validate_labels.py --strict`
7. document commands, artifacts, and checks in a walkthrough

### Why this slice
- it creates the first real project artifact
- it unblocks `training/prepare_sft_data.py`
- it stays within the VPS control-plane tier
- it avoids unnecessary Mac disruption
- it produces excellent learn-by-doing material

## Near-term backlog after that

1. Add perturbation diagnostics/reporting to dataset generation.
2. Reconcile training/eval docs with the actual scripts.
3. Make heavy-import training scripts friendlier by deferring backend imports.
4. Align single-example inference formatting with training prompts.
5. Add dry-run and fixture-based validation to integrations.
6. Only after the pipeline is grounded, consider a bounded Mac-side local experiment.

## Workload placement recommendation

### VPS now
Use the VPS for the next slice:
- dependency fixes
- tiny data pipeline run
- baseline docs and wiki updates
- lightweight validation

### Mac later, with care
Use the Mac for:
- bounded Apple-Silicon validation
- local Gemma experiments
- moderate compute once the pipeline is already producing training-ready artifacts

Approval gate:
- ask the user before any high-RAM Mac task

### Modal later
Use Modal only when:
- a real heavy GPU need exists
- the project has already proven the local-first path enough to justify cloud setup
