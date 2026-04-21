---
title: Gemma
created: 2026-04-17
updated: 2026-04-17
type: entity
tags: [model, fine-tuning, evaluation, local-first, apple-silicon]
sources: [raw/articles/original-project-spec-2026-04-17.md]
---

# Gemma

## Overview
Gemma is the model family anchoring this project's local-first LLM engineering work. The original specification focused on Gemma 4 E2B first, with E4B as an optional comparison target.

## Why it matters here
Keeping Gemma as the main model family preserves continuity with the original project while fitting the new Hermes-first scope. It lets the repo stay focused instead of diffusing across too many unrelated model stacks.

## Practical implications
- Local experimentation should prefer Gemma-sized workflows that fit the Apple Silicon environment.
- Training and evaluation docs should remain centered on Gemma-specific choices.
- Comparisons against larger alternatives should be documented explicitly rather than introduced casually.

## Related pages
- [[unsloth]]
- [[hermes-first-development]]
- [[hermes-agent]]
