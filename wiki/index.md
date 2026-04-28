# Wiki Index

> Content catalog for the project wiki.
> Last updated: 2026-04-27 | Total pages: 28

## Entities
- [[gemma]] - Model family anchoring the project's local-first fine-tuning direction.
- [[hermes-agent]] - Primary agentic execution system that now drives project work.
- [[modal]] - Planned future heavy-compute tier for truly GPU-intensive work.
- [[syncthing]] - Intended file-synchronization layer between the VPS and the Mac.
- [[tailscale]] - Secure connectivity layer for cross-machine coordination.
- [[unsloth]] - Preferred fine-tuning workflow for Gemma experiments where feasible.

## Concepts
- [[execution-topology]] - Rules for deciding whether work runs on the VPS, the Mac, or later Modal.
- [[hermes-first-development]] - Operating model where Hermes performs the work and generates study material in parallel.
- [[home-ai-lab-principles]] - Practical operating philosophy for this repo as the first project in the user's home AI lab.

## Comparisons

## Queries
- [[binary-sft-handoff-2026-04-17]] - Durable answer describing the binary SFT data handoff on the VPS.
- [[hermes-filtered-traces-dataset-structure-2026-04-22]] - Durable answer describing the Hermes filtered traces dataset structure, tool density, and ShareGPT-style storage.
- [[dataset-builder-phase-0-improvements-2026-04-22]] - Durable answer describing how to improve dataset_builder after Phase 0 without over-engineering it.
- [[dataset-builder-phase-1-readiness-2026-04-24]] - Durable answer describing the uv-first, inspection, audit, and P9 readiness pass before Phase 1 hands-on work.
- [[codebase-baseline-2026-04-17]] - Durable answer describing the repo's current state and why the dataset pipeline is the next slice.
- [[training-smoke-test-audit-2026-04-17]] - Durable answer describing the first training preflight audit and bounded smoke-test recommendation.
- [[tiny-dataset-pipeline-vps-2026-04-17]] - Durable answer describing the first successful end-to-end VPS dataset pipeline slice.
- [[task-4-lightweight-coherence-screen-2026-04-23]] - Durable answer describing the lightweight post-perturbation coherence screen, its determinism fix, and why repeated_step remains in scope.
- [[task-5-p5-p6-realism-2026-04-23]] - Durable answer describing how P5 and P6 were made less synthetic while preserving deterministic dataset builds.
- [[task-6-rule-aware-bad-step-validation-2026-04-23]] - Durable answer describing how the validator now checks rule-aware bad_step localization for P4, P5, and P7.
- [[task-7-build-manifest-and-diagnostics-2026-04-23]] - Durable answer describing how each dataset build now writes build_manifest.json with reproducibility and diagnostics data.
- [[phase-1-scope-boundary-2026-04-26]] - Durable answer describing why SFT and RL remain future goals while the active learning path stops at dataset-builder Phase 1.
- [[dataset-builder-phase-1-understanding-2026-04-26]] - Durable answer describing what Phase 1 established about the real Hermes trace corpus and why normalization is the next honest learning step.
- [[dataset-builder-phase-2-normalization-2026-04-26]] - Durable answer describing how normalization preserves rows, stabilizes trace identity, and turns raw traces into the internal trajectory contract.
- [[dataset-builder-phase-3-perturbation-context-2026-04-27]] - Durable answer describing why anomaly taxonomy and generation strategy must be judged together before the rule-by-rule Phase 3 walkthrough.
- [[dataset-builder-p1-replace-tool-choice-2026-04-27]] - Durable answer describing why believable replacements and bounded mutation scope both matter for the first wrong-tool-choice perturbation rule.
- [[dataset-builder-p1-realism-coverage-2026-04-27]] - Durable answer describing why P1 now prefers curated realism over synthetic `_v2` yield and how the corpus-wide before/after comparison justifies that trade-off.
- [[dataset-builder-perturbation-diagnostics-script-2026-04-27]] - Durable answer describing how the new rule-by-rule diagnostics script established P1 as the clear remaining coverage bottleneck in the normalized corpus.
- [[interactive-trajectory-explorer-first-slice-2026-04-27]] - Durable answer describing the first static visualization slice, its payload exporter, and how it connects trajectories to later training and evaluation work.
