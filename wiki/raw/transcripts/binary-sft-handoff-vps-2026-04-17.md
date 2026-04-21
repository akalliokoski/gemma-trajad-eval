# Binary SFT handoff on VPS

Date: 2026-04-17
Source type: internal project execution notes

Summary:
- Used `training/prepare_sft_data.py --task binary` on the processed dataset.
- Generated train/dev/test binary SFT JSONL files under `data/processed/`.
- Verified that SFT output counts matched the processed split counts exactly.
- Confirmed sample records use the expected `system` / `user` / `assistant` chat-message structure.
- Noted that full trajectories create large user-message payloads, which matters for later training smoke tests.
