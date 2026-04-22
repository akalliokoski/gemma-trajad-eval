# Media brief: TrajAD dataset construction and anomaly taxonomy

Use this brief to generate an infographic and podcast for the second Phase 0.1 domain-background topic in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`.

## Audience
A technically curious learner working through the dataset-builder plan for the first time.

## Target understanding
By the end, the learner should understand:
1. the three top-level anomaly classes in TrajAD
2. that TrajBench uses six perturbation families
3. how that compares with this repo's current 8 perturbation rules
4. what perturb-and-complete adds over direct perturbation
5. why the paper's human agreement rates set a quality bar for later manual review

## Core facts to preserve
- The three top-level anomaly classes are Task Failure, Process Inefficiency, and Unwarranted Continuation.
- TrajBench uses six perturbation families spanning those classes.
- This repo currently has 8 perturbation rules, but its generation strategy is simpler than TrajBench's.
- Perturb-and-complete means injecting an anomaly and then continuing the trajectory from the corrupted state so later behavior reflects the mistake.
- This repo currently uses direct perturbation, which is simpler but can leave later steps internally inconsistent.
- The paper reports 96.2% human agreement on anomaly classification and 94.5% on first-error localization.

## Repo-specific framing
Explain why this matters to `dataset_builder/`:
- anomaly taxonomy quality matters
- realistic bad trajectories matter
- first-error localization depends on coherent downstream behavior
- high human agreement is the standard to aim for in later manual review phases

## Suggested tone
- clear and concrete
- no hype
- emphasize taxonomy plus generation method
- compare TrajBench's richer data construction to this repo's simpler direct perturbation

## Source files
- `answers.md`
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `infographic.png` is the current prompt-driven image-generation artifact

## Sources
- TrajAD paper: https://arxiv.org/abs/2602.06443
- TrajAD HTML source used for extraction: https://arxiv.org/html/2602.06443
