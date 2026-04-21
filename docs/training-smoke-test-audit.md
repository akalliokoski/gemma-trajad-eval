# Training Smoke-Test Audit

Date: 2026-04-17
Primary execution tier: VPS for inspection and preflight only

## Goal

Audit `training/train_e2b.py` against the generated binary SFT artifacts and decide the smallest realistic first training smoke test.

## What was checked

Code inspected:
- `training/train_e2b.py`
- `training/train_e4b.py`
- `training/prepare_sft_data.py`
- `training/inference.py`
- `pyproject.toml`

Environment checks performed on the VPS:
- `python training/train_e2b.py --help`
- module availability for `mlx_tune`, `mlx`, `mlx_lm`, `transformers`, `trl`, `unsloth`, `torch`
- `hf auth whoami`

Data checks performed on the generated binary SFT files:
- sample structure inspection
- file sizes
- character-length distribution of the user message field
- trajectory step-count distribution

## Findings

### 1. The script contract matches the binary SFT file shape

`training/train_e2b.py` expects:
- `data/processed/{split}_sft_{task}.jsonl`
- each row loaded as JSON with a top-level `messages` field

The generated binary data matches that contract structurally:
- keys: `id`, `messages`
- roles: `system`, `user`, `assistant`
- assistant target is strict JSON such as `{"anomalous": true}`

### 2. The original `train_e2b.py` had a real ergonomics blocker

Before patching, `train_e2b.py` imported `mlx_tune` at module import time. That meant even:
- `python training/train_e2b.py --help`

failed on the VPS with:
- `ModuleNotFoundError: No module named 'mlx_tune'`

This prevented basic inspection and made remote preflight harder than necessary.

### 3. `train_e2b.py` now has better smoke-test ergonomics

Patched behavior:
- backend import is now lazy, so `--help` works without `mlx_tune`
- `load_sft_data()` now supports an example cap
- new CLI flags:
  - `--max-seq-length`
  - `--max-train-examples`
  - `--max-eval-examples`

This does not make the VPS capable of Apple-Silicon training. It does make the script inspectable and makes a bounded Mac smoke test easier to launch later.

### 4. The VPS is not a viable E2B training host

Current VPS preflight results:
- `mlx_tune`: missing
- `mlx`: missing
- `mlx_lm`: missing
- `unsloth`: missing
- `torch`: missing
- `hf auth whoami`: `Error: Not logged in`

This means the VPS cannot currently do any of the following:
- local Apple Silicon `mlx-tune` training
- CUDA/Unsloth training
- gated Gemma model download

So the VPS remains the correct control-plane and inspection tier, not the actual E2B training tier.

### 5. The SFT examples are very large relative to the current 4096-token default

Observed binary SFT file sizes:
- `train_sft_binary.jsonl`: 1,232,789,553 bytes
- `dev_sft_binary.jsonl`: 163,115,205 bytes
- `test_sft_binary.jsonl`: 246,288,394 bytes

Observed user-message character lengths:
- train mean: 82,765.8 chars
- train p50: 63,189 chars
- train p95: 198,424 chars
- train p99: 303,017 chars
- train max: 514,624 chars

Observed trajectory structure in the processed train split:
- mean steps: 32.4
- p50 steps: 31
- p95 steps: 54
- max steps: 56

Important implication:
- the current default `MAX_SEQ_LENGTH = 4096` in `training/train_e2b.py` is almost certainly much smaller than the full effective tokenized context for a large fraction of examples
- without authenticated Gemma tokenizer access on the VPS, this is a strong preflight warning rather than a measured Gemma-token count
- in practice, the initial smoke test should assume heavy truncation unless the data format is shortened first

### 6. Model access is also blocked by Hugging Face auth

Attempting tokenizer access against a Gemma repo on the VPS failed with a gated-repo 401.

That confirms a second non-code blocker:
- even after moving to the Mac, Hugging Face authentication with access to the Gemma model repo must be in place before training starts

## Tests added

Added:
- `tests/test_train_e2b.py`

Verified:
- `PYTHONPATH=. pytest tests/test_train_e2b.py -q` → pass
- `PYTHONPATH=. pytest tests -q` → pass (`4 passed`)

The new tests cover:
- importing `train_e2b.py` without `mlx_tune`
- limiting loaded SFT examples for smoke-test subsets

## Smallest realistic smoke-test path

Recommended first real training run:
1. run on the Mac, not the VPS
2. authenticate to Hugging Face first
3. install the Apple Silicon training stack there (`mlx-tune`/related deps)
4. start with a deliberately bounded run such as:
   - task: `binary`
   - `--max-train-examples 32`
   - `--max-eval-examples 16`
   - `--max-seq-length 4096`
5. treat the result as infrastructure validation only:
   - model download works
   - adapter output directory is created
   - trainer starts and can complete a tiny run

Suggested first command on the Mac once approved and prepared:

```bash
python training/train_e2b.py \
  --task binary \
  --run-name e2b-binary-smoke-32x16 \
  --max-seq-length 4096 \
  --max-train-examples 32 \
  --max-eval-examples 16
```

## Decision

Do not dispatch the actual smoke-test run to the Mac yet without explicit approval, because it is the first real model-training step and may create meaningful local RAM pressure.

## Follow-up options

Best immediate follow-ups, still safe to do on the VPS:
1. add a preflight utility that reports SFT length statistics before training
2. create an intentionally short training subset for smoke tests
3. inspect/fix `training/inference.py` and `training/evaluate.py` before the first Mac run
4. prepare exact Mac-side setup instructions once user approves the first training attempt
