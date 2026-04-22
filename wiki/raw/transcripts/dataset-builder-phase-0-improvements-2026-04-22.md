# Raw snapshot: dataset-builder improvements after Phase 0

Date: 2026-04-22

Sources reviewed:
- docs/learning-materials/dataset-builder/phase-0/0.1-domain-background/trajectory-anomaly-detection/answers.md
- docs/learning-materials/dataset-builder/phase-0/0.1-domain-background/dataset-construction-and-anomaly-taxonomy/answers.md
- docs/learning-materials/dataset-builder/phase-0/0.1-domain-background/hermes-filtered-traces-dataset-card-and-viewer/answers.md
- dataset_builder/inspect_traces.py
- dataset_builder/normalize_trajectory.py
- dataset_builder/perturbations.py
- dataset_builder/build_trajad_dataset.py
- dataset_builder/validate_labels.py
- docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md

Key raw findings:
- The current dataset builder already has a good simple backbone: normalization, perturbation, source-trace-safe splitting, and lightweight validation.
- The raw Hermes data is ShareGPT-like (`from`, `value`) with serialized `<tool_call>` and `<tool_response>` markup inside text.
- Phase 0 showed typical trajectories are about 32 messages long and tool use is effectively universal in the filtered corpus.
- The current builder still uses direct perturbation only, which can create internally inconsistent anomalous trajectories.
- The highest-value improvements are quality-oriented rather than infrastructure-oriented.
- Modal serverless GPU is now the default future GPU path for this project; Apple Silicon is secondary.

Recommended implementation priorities:
1. Repair raw-schema-safe inspection.
2. Add derived structural metadata during normalization.
3. Add explicit top-level anomaly classes.
4. Add a lightweight coherence screen after perturbation.
5. Improve realism of P5 and P6.
6. Add rule-aware first-error localization validation.
7. Save build manifests and perturbation diagnostics.
