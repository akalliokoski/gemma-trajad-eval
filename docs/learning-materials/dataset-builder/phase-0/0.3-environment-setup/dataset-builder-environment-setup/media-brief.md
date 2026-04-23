# Media brief: dataset builder environment setup

Use this brief to generate an infographic and podcast for Phase 0.3 environment setup of the `dataset_builder/` learning path.

## Audience
A learner who wants a clean mental model for setting up the repo without over-engineering the environment.

## Target understanding
By the end, the learner should understand:
1. the portable setup contract for this repo
2. the difference between the generic learning-plan path and the VPS-specific `uv` path
3. why import verification matters more than command nostalgia
4. why Hugging Face auth is optional for early public-dataset work
5. why the `data/raw`, `data/interim`, and `data/processed` directories exist

## Core facts to preserve
- `pyproject.toml` requires Python 3.11 or newer.
- The canonical plan suggests `.venv` creation with `python3 -m venv`, activation, editable install with `.[dev]`, and a small import test.
- The documented VPS walkthrough used `uv` because system `pip` under `/usr/bin/python3` was not available.
- The Hermes filtered dataset is public, so auth is mainly needed later for upload/publication work.
- The repo expects `data/raw/`, `data/interim/`, and `data/processed/` as the storage layers of the pipeline.

## Repo-specific framing
Frame this as practical environment design for a home-lab data pipeline:
- boring and reproducible beats clever
- adapt commands to the machine only when needed
- keep the repo contract stable

## Suggested tone
- calm
- pragmatic
- confidence-building
- specific about the difference between generic and machine-specific setup

## Source files
- `answers.md`
- `README.md`
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `podcast-transcript.json`
- `podcast-transcript.txt`

## Sources
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `pyproject.toml`
- `docs/data-pipeline-walkthrough.md`
- `docs/codebase-baseline.md`
