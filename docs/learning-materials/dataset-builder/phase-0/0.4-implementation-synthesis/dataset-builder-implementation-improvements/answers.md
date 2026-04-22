# Dataset-builder implementation improvements after Phase 0

Source topic: synthesis based on the existing Phase 0 learning materials in `docs/learning-materials/dataset-builder/phase-0/` plus the current `dataset_builder/` implementation.

## Questions and answers

### 1) What should stay the same in `dataset_builder/`?
A lot should stay the same.

The current implementation already has the right overall shape for a home AI lab:
- plain Python scripts
- JSONL in and JSONL out
- a clear normalization step
- perturbation-based synthetic anomaly generation
- split assignment by `source_trace_id`
- a lightweight validation pass

That means the right move is not a rewrite. The right move is to strengthen the weak points that Phase 0 made visible.

### 2) What did Phase 0 reveal as the most important implementation gap?
The biggest gap is dataset quality discipline, not missing infrastructure.

Phase 0 made three points especially clear:
1. the raw Hermes traces are long, tool-centric execution traces
2. the raw storage format is ShareGPT-like `{from, value}` with serialized tool protocol in text
3. good trajectory anomaly datasets need coherent bad trajectories, not just arbitrary corruption

The current builder is good at simple direct perturbation, but it does not yet do enough to guard against unrealistic or internally inconsistent anomalies.

### 3) What is the single highest-priority improvement?
Fix raw-data inspection first.

`dataset_builder/inspect_traces.py` currently crashes on the real raw Hermes dataset because it assumes `role/content` rather than `from/value`. That is a concrete bug, and it blocks trustworthy inspection.

This matters because Phase 0 showed that raw-format awareness is not a side detail. It is central to the entire pipeline. If the inspection tool is wrong, later decisions about normalization and perturbation become less grounded.

### 4) Why add a coherence screen instead of full perturb-and-complete right away?
Because it is the best practical compromise.

TrajAD's strongest methodological idea is perturb-and-complete: inject a mistake, then continue the trajectory from that corrupted state. That produces more realistic downstream behavior.

This repo currently uses direct perturbation only. Building a full model-assisted continuation system now would add a lot of complexity.

A lightweight coherence screen is the practical middle path:
- keep the pipeline simple and deterministic
- reject obviously implausible perturbed outputs
- improve training-data quality immediately

That fits the project's style much better than jumping straight to a heavier generation system.

### 5) Why add `anomaly_class` if `anomaly_type` already exists?
Because Phase 0 gave the project a clearer conceptual taxonomy.

The TrajAD framing distinguishes three top-level classes:
- task failure
- process inefficiency
- unwarranted continuation

The current code stores only leaf labels like `wrong_tool_choice` or `repeated_step`. Those are useful, but they do not make the big-picture supervision target explicit.

Adding `anomaly_class` keeps the current detail while making the dataset easier to analyze, balance, explain, and evaluate.

### 6) Why keep normalization simple instead of redesigning the trajectory schema?
Because simple is still the right default here.

Phase 0 confirmed that the traces are tool-heavy and that structure is serialized inside text. That could tempt a full schema redesign.

But the practical move is smaller:
- keep the current normalized message shape
- add cheap derived metadata like tool-call counts, tool-response counts, `has_think`, and trajectory length

That gives better observability without forcing every downstream component to change.

### 7) Which current perturbation rules most need improvement?
P5 and P6.

They target meaningful anomaly ideas, but their current implementation looks overly synthetic:
- P5 creates a continuation pattern that can look structurally incomplete
- P6 uses an explicit contradiction marker, which is too artificial

These should become more natural-language-plausible while still staying deterministic.

### 8) Why strengthen `validate_labels.py` beyond range checks?
Because first-error localization is one of the main supervision targets.

Phase 0 repeatedly emphasized that the dataset is not only about classifying a trajectory as good or bad. It is also about localizing the first erroneous step.

The current validator mostly checks:
- field presence
- basic types
- whether `bad_step` is in range

That is helpful, but it is weaker than the real task. Rule-aware checks make the labels more trustworthy without making validation complicated.

### 9) Why add a build manifest?
Because a home lab needs reproducibility more than platform ceremony.

Right now the builder prints useful counts, but they disappear after the run. A small JSON manifest gives lasting answers to questions like:
- which seed produced this build?
- which rules were active?
- how many anomalies were rejected?
- what was the class balance?

That is high-value, low-ops engineering.

### 10) What should be the compute default going forward?
For GPU-backed work, Modal serverless GPU should be the default option.

That includes future tasks like:
- model-assisted perturb-and-complete
- semantic filtering or scoring
- sample auditing with stronger models

Apple Silicon is still useful, but it should be treated as the secondary path for bounded fallback experiments rather than the default GPU tier.

For the specific improvements in this plan, the VPS is enough because the work is mostly Python and JSONL data engineering.

## Key takeaway for this project
The best improvement path is not to make `dataset_builder/` bigger. It is to make it more disciplined.

The winning combination is:
- keep the current script-first architecture
- fix raw-schema awareness
- add cheap structural metadata
- make anomaly taxonomy explicit
- screen obviously implausible perturbations
- improve the weakest synthetic rules
- save reproducible manifests

That is how the project can stay elegant and simple while still getting meaningfully better.
