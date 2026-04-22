# Media brief: Trajectory anomaly detection for LLM agents

Use this brief to generate a podcast and video explainer for the first topic in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`.

## Audience
A technically curious learner working through the dataset-builder plan for the first time.

## Target understanding
By the end, the learner should understand:
1. what an agent trajectory is
2. why agent trajectory anomaly detection is different from GPS trajectory anomaly detection
3. why first-error localization matters for rollback-and-retry
4. what perturb-and-complete adds over direct perturbation
5. why this matters for this repo's dataset builder design

## Core facts to preserve
- In TrajAD, a trajectory is an instruction plus interleaved reasoning, action, and observation steps.
- Trajectory anomaly detection means both detecting whether a trajectory is anomalous and localizing the first erroneous step.
- GPS trajectory anomaly detection is about physical movement patterns; agent trajectory anomaly detection is about procedural failures in task execution.
- TrajBench is built with perturb-and-complete: inject an error, then continue the trajectory from that corrupted state so the downstream behavior stays realistic.
- This repo currently uses direct perturbation, which is simpler but can leave later steps internally inconsistent.

## Repo-specific framing
Explain why this matters to `dataset_builder/`:
- anomaly taxonomy quality matters
- realistic bad trajectories matter
- step-level labels matter
- leakage-safe grouping by source trace matters because the goal is reliable supervision, not superficial pattern matching

## Suggested tone
- clear and concrete
- no hype
- explain with contrasts and small mental models
- prefer one running comparison between GPS trajectories and agent trajectories

## Source files
- `answers.md`
- `infographic.svg`

## Sources
- TrajAD paper: https://arxiv.org/abs/2602.06443
- LM-TAD paper: https://arxiv.org/abs/2409.15366
