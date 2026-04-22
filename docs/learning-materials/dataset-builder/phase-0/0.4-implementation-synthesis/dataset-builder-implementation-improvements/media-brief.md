# Media brief: dataset-builder implementation improvements after Phase 0

Use this brief to generate an infographic and podcast for the Phase 0 synthesis topic on how `dataset_builder/` should improve after the existing learning materials.

## Audience
A technically curious learner building a first home AI lab project and wanting practical, elegant engineering guidance rather than platform sprawl.

## Target understanding
By the end, the learner should understand:
1. that the current dataset-builder architecture is fundamentally good and should be improved, not replaced
2. that the highest-value changes are about data quality discipline rather than infrastructure
3. that raw ShareGPT-style schema awareness, perturbation coherence, anomaly taxonomy, and stronger validation are the real implementation leverage points
4. that Modal serverless GPU is now the default future GPU option, with Apple Silicon as a secondary path
5. that the plan intentionally follows best practices like YAGNI, DRY, determinism, and reproducibility

## Core facts to preserve
- The current pipeline already has a good simple backbone: normalization, perturbation, source-trace-safe splits, and lightweight validation.
- Raw Hermes traces use ShareGPT-like `{from, value}` storage with serialized `<tool_call>` and `<tool_response>` markup.
- Typical trajectories are about 32 messages long and tool use is effectively universal in the filtered dataset.
- The current builder uses direct perturbation only, so some anomalies can become internally inconsistent.
- The highest-priority improvements are: raw-schema-safe inspection, lightweight coherence screening, explicit anomaly classes, better P5/P6 realism, stronger localization validation, and build manifests.
- Modal serverless GPU should be treated as the default future GPU tier; Apple Silicon is secondary.

## Repo-specific framing
Frame this as a home-lab engineering decision:
- keep the current script-first pipeline
- improve trustworthiness before adding new infrastructure
- use Phase 0 findings to shape code changes directly
- prefer practical elegance over architecture cosplay

## Suggested tone
- confident but grounded
- technically specific
- practical and anti-hype
- explicitly explain tradeoffs and why simpler choices win here

## Source files
- `answers.md`
- `README.md`
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `podcast-transcript.json`
- `podcast-transcript.txt`
- `../../../../plans/2026-04-22-dataset-builder-phase-0-improvements.md`

## Sources
- `docs/learning-materials/dataset-builder/phase-0/0.1-domain-background/trajectory-anomaly-detection/answers.md`
- `docs/learning-materials/dataset-builder/phase-0/0.1-domain-background/dataset-construction-and-anomaly-taxonomy/answers.md`
- `docs/learning-materials/dataset-builder/phase-0/0.1-domain-background/hermes-filtered-traces-dataset-card-and-viewer/answers.md`
- `docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md`
- `dataset_builder/inspect_traces.py`
- `dataset_builder/normalize_trajectory.py`
- `dataset_builder/perturbations.py`
- `dataset_builder/build_trajad_dataset.py`
- `dataset_builder/validate_labels.py`
