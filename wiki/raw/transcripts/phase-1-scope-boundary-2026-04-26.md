# Phase-1 scope boundary for training work — 2026-04-26

Summary:
- created `docs/deferred-training-roadmap.md`
- narrowed the active dataset-builder learning-path scope to Phase 0 + Phase 1 understanding work
- kept SFT, fine-tuning, and RL in the project, but moved them out of the current active pass
- updated the long-form learning plan to make the stop line explicit
- updated the Hermes-first roadmap to mark local training as deferred for now

Why:
- the user wants to learn fine-tuning and RL later, but the current work should stay focused on generating the Phase 1 learning path
- the repo already has binary SFT and training-preflight docs, so the right move is not to forget training, but to sequence it later

Primary docs:
- `docs/deferred-training-roadmap.md`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `docs/plans/2026-04-17-hermes-first-roadmap.md`

Decision:
- current active learning-path work stops after dataset-builder Phase 1 understanding
- later training work should resume from the deferred roadmap, then the binary SFT handoff and training smoke-test audit