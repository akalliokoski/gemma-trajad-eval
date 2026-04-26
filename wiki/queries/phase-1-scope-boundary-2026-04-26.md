---
title: Phase-1 scope boundary for deferred training work
created: 2026-04-26
updated: 2026-04-26
type: query
tags: [workflow, roadmap, documentation, fine-tuning, course-material]
sources: [raw/transcripts/phase-1-scope-boundary-2026-04-26.md]
---

# Phase-1 scope boundary for deferred training work

## Durable answer

The project should keep fine-tuning and RL as real future goals, but the **current** learning-path pass should stop at dataset-builder Phase 0 and Phase 1 understanding work.

## What changed

- a dedicated later-path document now exists at `docs/deferred-training-roadmap.md`
- the dataset-builder learning plan explicitly says the active pass is narrowed to Phase 0 + Phase 1
- the broader Hermes-first roadmap now marks the local training task as intentionally deferred for the current pass

## Why this is the right scope cut

- it keeps the current learning materials finishable
- it preserves the future SFT / RL path instead of dropping it
- it respects the existing repo evidence that training is possible later but not the right next teaching slice

## Practical resume point later

When training work becomes active again, resume with this sequence:
1. `docs/deferred-training-roadmap.md`
2. `docs/binary-sft-handoff.md`
3. `docs/training-smoke-test-audit.md`

## Related pages
- [[dataset-builder-phase-1-readiness-2026-04-24]]
- [[binary-sft-handoff-2026-04-17]]
- [[training-smoke-test-audit-2026-04-17]]
- [[home-ai-lab-principles]]