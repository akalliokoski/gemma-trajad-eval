# Deferred Training and RL Roadmap

Date: 2026-04-26
Status: deferred by design
Current execution tier: VPS for documentation and inspection only

## Why this document exists

The project still intends to teach:
- supervised fine-tuning (SFT)
- practical Gemma training workflow decisions
- later reward-driven post-training such as GRPO/RL

But those topics are **not** the active scope of the current Phase 1 learning-path pass.

Right now, the narrow goal is to finish the dataset-builder learning path through empirical Phase 1 understanding:
- get the raw data onto disk
- inspect the real trace structure
- understand tool-call embedding and perturbation eligibility
- keep the current learning materials focused and finishable

This document captures the later training path so the work is not lost, while protecting the current scope from expanding too early.

## What is intentionally deferred

The following are out of scope for the current learning-path pass:
- actual Gemma training runs on the Mac
- Mac-side high-RAM smoke tests
- Modal GPU setup for training
- full SFT evaluation workflow
- GRPO / RL reward implementation
- experiment tracking and scaling decisions
- model-quality claims beyond data-format and preflight readiness

## Why the deferral is correct

Three repo facts argue for delaying training execution:

1. **The current learning path is about dataset understanding first.**
   The active materials already center on Phase 0 and Phase 1 dataset-builder work.

2. **The existing binary SFT path is real, but not yet a clean first training lesson.**
   `docs/binary-sft-handoff.md` and `docs/training-smoke-test-audit.md` show that the data can be formatted for SFT, but also that many examples are extremely long and that real training requires additional environment and scope decisions.

3. **RL is most useful after a narrow SFT baseline exists.**
   The project should first prove a tiny supervised path, then a structured-output path, and only then introduce reward design.

## Current stop line

For the current pass, stop after the dataset-builder learning path has produced:
- Phase 0 orientation understanding
- Phase 1 raw-data and exploration understanding
- concise documentation of what was learned

Do **not** expand the active learning path into model-training execution yet.

## Later roadmap

When the project is ready to resume training work, use this order.

### Stage 1 — Binary SFT smoke test

Goal:
- prove the training path can start and finish a tiny bounded run

Starting points already in repo:
- `docs/binary-sft-handoff.md`
- `docs/training-smoke-test-audit.md`
- `training/prepare_sft_data.py`
- `training/train_e2b.py`

Constraints:
- ask for explicit approval before dispatching Mac training work
- treat the first run as infrastructure validation, not model-quality validation
- prefer a tiny capped subset and a conservative sequence length

Expected learning:
- Hugging Face auth and gated-model access
- Apple Silicon training environment setup
- smallest useful LoRA/SFT workflow
- adapter artifact layout and smoke-test verification

### Stage 2 — Shorten the training task before scaling it

Goal:
- make the first real SFT lesson easier to understand and less distorted by sequence-length pressure

Likely work:
- define a shorter rendered-input format for training
- or create a bounded subset focused on shorter traces
- document exactly what fidelity is lost and what practicality is gained

Why this comes before broader SFT evaluation:
- current binary SFT examples are large enough that naive first-run results would be dominated by truncation rather than training insight

### Stage 3 — Real binary SFT baseline

Goal:
- produce a small but honest supervised baseline for anomaly / non-anomaly judgment

Target output:
```json
{"anomalous": true}
```
or
```json
{"anomalous": false}
```

What to learn:
- baseline prompting vs SFT
- train/dev/test discipline
- simple evaluation before over-complicating the task
- where Apple Silicon is sufficient and where Modal becomes justified

### Stage 4 — Structured SFT for richer supervision

Goal:
- move from binary labels to a structured anomaly-judging output that is more useful for later RL

Suggested progression:
1. binary label only
2. binary label + anomaly type
3. binary label + anomaly type + bad-step index

Why this is the right bridge:
- it teaches output-schema discipline
- it creates more meaningful evaluation signals
- it sets up later reward shaping naturally

### Stage 5 — GRPO / RL pilot

Goal:
- learn reward-driven post-training on a task with verifiable structure

Recommended first reward components:
- valid JSON reward
- correct binary label reward
- correct anomaly type reward
- exact or near-exact `bad_step` reward

Non-goals for the first RL pass:
- do not begin with open-ended explanation quality rewards
- do not start with large-scale cloud runs
- do not skip the structured SFT baseline

Why this is a better RL fit than earlier alternatives:
- the task has objective, inspectable signals
- partial credit is straightforward
- regressions are easier to detect than with purely stylistic rewards

### Stage 6 — Scale only after the small loop works

Only after Stages 1–5 are stable should the project decide whether to add:
- Modal GPU training runs
- experiment tracking beyond lightweight local records
- broader hyperparameter sweeps
- larger model variants

## Minimal prerequisite checklist before resuming this roadmap

Before reactivating training work, confirm:
- the current dataset-builder learning path pass is complete enough to pause cleanly
- the binary SFT handoff docs still match the data artifacts on disk
- the training smoke-test audit is still accurate for the current scripts
- Hugging Face auth and Gemma access are available on the intended training host
- explicit user approval exists before meaningful Mac RAM pressure is created

## Recommended next action for now

For the active project phase, continue improving and packaging the **dataset-builder Phase 1 learning path** only.

Use this roadmap later when the project intentionally switches from:
- understanding and curating the data

to:
- training and evaluating models on that data.