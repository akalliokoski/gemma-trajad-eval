---
title: Dataset-builder Phase-1 readiness improvements
created: 2026-04-24
updated: 2026-04-24
type: query
tags: [dataset, workflow, documentation, python, course-material]
sources: [raw/transcripts/dataset-builder-phase-1-readiness-2026-04-24.md]
---

# Dataset-builder Phase-1 readiness improvements

## Durable answer

The right next implementation slice after Phase 0 was not a pipeline rewrite. It was a readiness pass that made the existing script-first pipeline easier to run, inspect, and trust.

## What changed

- the repo now has a clear `uv`-first workflow
- setup is one command via `scripts/bootstrap_dataset_builder.sh`
- `inspect_traces.py` can now report schema shape, tool density, and perturbation eligibility signals
- the taxonomy gap for `invalid_tool_json` is now covered by `P9`
- post-build auditing exists in `dataset_builder/audit_dataset.py`
- the storage contract is now documented explicitly as `raw -> interim -> processed`

## Why this matters

This keeps the home-lab version of the project elegant:
- no orchestration framework
- no database
- no rename churn
- better operational confidence
- better observability before more complexity

## Verification snapshot

- bootstrap script: OK
- targeted test suite: `32 passed`
- strict validation on `data/processed/all.jsonl`: OK
- audit report now runs on the full dataset and reports split-aware counts

## Storage-stage decision

Keep these as the real implementation stages:
- `data/raw`
- `data/interim`
- `data/processed`

The bronze/silver/gold language is useful only as a conceptual mapping, not as a rename target.

## Related pages
- [[dataset-builder-phase-0-improvements-2026-04-22]]
- [[hermes-filtered-traces-dataset-structure-2026-04-22]]
- [[home-ai-lab-principles]]
