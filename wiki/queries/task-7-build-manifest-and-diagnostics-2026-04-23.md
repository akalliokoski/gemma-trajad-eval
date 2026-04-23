---
title: Task 7 build manifest and diagnostics
created: 2026-04-23
updated: 2026-04-23
type: query
tags: [dataset, workflow, documentation, python, course-material]
sources: [docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md, dataset_builder/build_trajad_dataset.py, tests/test_build_manifest.py, raw/transcripts/task-7-build-manifest-and-diagnostics-2026-04-23.md]
---

# Task 7 build manifest and diagnostics

Task 7 made each dataset build reproducible by saving the key inputs, outputs, and diagnostics to `data/processed/build_manifest.json` instead of leaving that information only in transient console output.

## Durable answer

The right implementation was to keep the script-first builder, then add one durable manifest layer plus a compact human-readable summary.

### What changed
- added `build_manifest(...)` to assemble a structured summary of the build
- added `write_manifest(...)` to persist `data/processed/build_manifest.json`
- added `format_manifest_summary(...)` so the command still feels pleasant interactively
- tracked source input paths, rules used, split counts, anomaly-type counts, anomaly-class counts, perturbation failures by rule, and coherence rejections
- added `tests/test_build_manifest.py` to lock in both manifest contents and summary formatting

### Why this shape fits the repo
- improves reproducibility without adding platform complexity
- keeps the builder script deterministic and inspectable
- captures the exact diagnostics needed for later review in a home-lab workflow
- preserves the repo's plain Python + JSONL design

## Verification evidence
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_build_manifest.py -v`
- `2 passed`
- `python3 dataset_builder/build_trajad_dataset.py --seed 42`
- `Generated 56,724 anomalous records`
- `Coherence screen: kept=56,724 rejected=0`
- `Split sizes: train=47,973  dev=6,413  test=9,696`
- `normal=7,358 anomalous=56,724 all=64,082`
- `python3 -m json.tool data/processed/build_manifest.json > /tmp/build_manifest.pretty.json`
- `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
- `Validated 64,082 records from data/processed/all.jsonl`
- `All records valid.`

## Related pages
- [[dataset-builder-phase-0-improvements-2026-04-22]]
- [[task-6-rule-aware-bad-step-validation-2026-04-23]]
- [[task-4-lightweight-coherence-screen-2026-04-23]]
