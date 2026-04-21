---
title: Unsloth
created: 2026-04-17
updated: 2026-04-17
type: entity
tags: [training, fine-tuning, python, open-source, local-first]
sources: [raw/articles/original-project-spec-2026-04-17.md]
---

# Unsloth

## Overview
Unsloth is the preferred fine-tuning workflow for this project where feasible. It remains part of the technical backbone after the Hermes-first pivot.

## Why it matters here
The repo wants to preserve the original stack wherever practical. That means training plans, data prep, and experiments should continue to consider Unsloth as the default path before introducing alternatives.

## Practical implications
- Fine-tuning plans should explain whether a task runs directly with Unsloth or with an Apple-Silicon-compatible fallback.
- Workflow notes should capture any gaps between local Mac constraints and cloud GPU execution.
- Reusable training procedures should be documented as project skills if they become stable.

## Related pages
- [[gemma]]
- [[hermes-first-development]]
- [[hermes-agent]]
