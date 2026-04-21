---
title: Training Smoke-Test Audit - 2026-04-17
created: 2026-04-17
updated: 2026-04-17
type: query
tags: [training, workflow, documentation, decision, apple-silicon]
sources: [docs/training-smoke-test-audit.md]
---

# Query: What is the smallest realistic first training smoke test after the binary SFT handoff?

Date answered: 2026-04-17

## Short answer

Keep the analysis on the VPS, but do the first real training run on the Mac after explicit approval.

## Why

The VPS audit showed three hard blockers for actual training there:
- no `mlx_tune` / `mlx`
- no `torch` / `unsloth`
- Hugging Face auth is not logged in for gated Gemma access

The audit also showed that the generated binary SFT examples are large enough that the current 4096-token default should be treated as a truncation-heavy smoke-test setting, not a full-fidelity training configuration.

## Recommended first run

A bounded infrastructure-validation run on the Mac:
- task: `binary`
- max train examples: 32
- max eval examples: 16
- max sequence length: 4096

Example command:

```bash
python training/train_e2b.py \
  --task binary \
  --run-name e2b-binary-smoke-32x16 \
  --max-seq-length 4096 \
  --max-train-examples 32 \
  --max-eval-examples 16
```

## Key supporting evidence

- `train_sft_binary.jsonl` is ~1.23 GB
- train user-message mean length is ~82.8k characters
- train user-message p95 length is ~198.4k characters
- train user-message max length is ~514.6k characters
- `train_e2b.py` was patched to support lazy backend import and bounded sample caps for smoke tests

## Source docs

- `docs/binary-sft-handoff.md`
- `docs/training-smoke-test-audit.md`
