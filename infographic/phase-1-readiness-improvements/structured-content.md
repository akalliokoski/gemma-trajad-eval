# Structured content

## Title
Dataset-builder Phase-1 Readiness Improvements

## Learning objectives
- See what changed in the codebase before Phase 1 hands-on work.
- Understand the new default `uv` workflow.
- Understand the new inspection, perturbation, audit, and data-contract improvements.

## Section 1 — Workflow
- Label: `uv` standard
- Points:
  - `.python-version: 3.12`
  - `uv.lock added`
  - `uv sync --extra dev`
  - `setuptools.build_meta`
  - `dataset_builder/__init__.py`

## Section 2 — Bootstrap
- Label: one-command setup
- Points:
  - `scripts/bootstrap_dataset_builder.sh`
  - sync deps
  - create `data/raw data/interim data/processed`
  - smoke import check

## Section 3 — Inspection
- Label: stronger microscope
- Points:
  - `--schema-report`
  - `--tool-stats`
  - `--eligibility-report`
  - raw traces use `conversations` + `from/value`

## Section 4 — Perturbations
- Label: taxonomy gap closed
- Points:
  - new rule: `P9 invalid_tool_json`
  - class: `task_failure`
  - validation checks malformed assistant tool-call JSON
  - added to `ALL_RULES`, not `MVP_RULES`

## Section 5 — Audit
- Label: post-build audit
- Points:
  - `dataset_builder/audit_dataset.py`
  - streams JSONL instead of loading everything first
  - reports split counts
  - reports anomaly counts and bad-step buckets

## Section 6 — Data contract
- Label: keep stages simple
- Points:
  - `data/raw`
  - `data/interim`
  - `data/processed`
  - bronze/silver/gold is doc-only

## Verification strip
- `bootstrap script: OK`
- `test suite: 32 passed`
- `strict validation: All records valid`
- `audit command: OK`

## Metrics strip
- `raw records: 3,679`
- `avg raw trajectory length: 32.1`
- `tool-call traces: 100.0%`
- `>=2 tool-call pairs: 99.4%`
- `processed all.jsonl: 71,429`
- `splits: train 53,557 / dev 7,154 / test 10,718`

## Decision strip
- Keep implementation names: `raw -> interim -> processed`
- Avoid renaming code/docs to bronze/silver/gold
- Use the mapping only as a mental model
