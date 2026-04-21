# Binary SFT Handoff

Date: 2026-04-17
Execution tier: VPS
Why this tier: this step reformats existing processed JSONL into chat-style SFT examples and verifies the output. It is lightweight and does not require Apple Silicon execution or Modal.

## Goal

Convert the processed trajectory dataset into binary-task SFT files suitable for the first training path.

## Inputs

Used processed dataset files:
- `data/processed/train.jsonl`
- `data/processed/dev.jsonl`
- `data/processed/test.jsonl`

Prompt used:
- `prompts/anomaly_binary.txt`

Formatter used:
- `training/prepare_sft_data.py`

## Command used

```bash
. .venv/bin/activate
python training/prepare_sft_data.py --task binary
```

## Result

Generated:
- `data/processed/train_sft_binary.jsonl`
- `data/processed/dev_sft_binary.jsonl`
- `data/processed/test_sft_binary.jsonl`

Verified line counts:
- train: 13,767
- dev: 1,833
- test: 2,755
- total: 18,355

These counts match the underlying processed split counts exactly.

## Output format

Each SFT record has:
- `id`
- `messages`
  - system: anomaly detector instruction from `prompts/anomaly_binary.txt`
  - user: full trajectory rendered as numbered `[Step N] [ROLE]` blocks plus `Task: binary`
  - assistant: strict JSON target like `{"anomalous": true}` or `{"anomalous": false}`

## Verification performed

1. Ran the formatter successfully.
2. Verified output line counts with `wc -l`.
3. Inspected sample records to confirm:
   - system/user/assistant message structure exists
   - task is binary
   - targets are binary JSON labels

## Important observations

- The user message includes the full trajectory text, including the original system/tool context from the source trace.
- This is useful for fidelity to the original trajectory, but it also means examples can become very large.
- The generated SFT files are appropriate for formatting and smoke-test work, but sequence-length pressure should be considered before actual local training runs.

## What this unblocks

This handoff unblocks the next layer of work:
- inspect whether the local training script contract matches these SFT files
- improve training-script ergonomics if needed
- decide the first bounded local training smoke test plan

## Recommended next slice

1. inspect `training/train_e2b.py` against the generated binary SFT format
2. identify the smallest realistic smoke-test path
3. keep the investigation on the VPS first
4. only ask for Mac approval when a run is likely to create meaningful RAM pressure
