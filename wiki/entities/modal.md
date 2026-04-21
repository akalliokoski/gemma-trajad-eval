---
title: Modal
created: 2026-04-17
updated: 2026-04-17
type: entity
tags: [cloud, training, fine-tuning, evaluation, workflow]
sources: [raw/transcripts/execution-topology-update-2026-04-17.md]
---

# Modal

## Overview
Modal is the planned heavy-compute tier for this project.

## Why it matters here
The MacBook Pro should handle only small and medium heavy-lifting, especially because it is also the user's daily workstation. Truly heavy training or GPU-intensive workloads should move to Modal once setup is intentionally done.

## Practical implications
- Do not treat Modal as active infrastructure yet.
- Delay account setup until the project reaches a stage where cloud GPU work is justified.
- When the first heavy GPU task appears, Hermes should document the decision and setup path carefully.

## Related pages
- [[execution-topology]]
- [[gemma]]
- [[unsloth]]
