# Training smoke-test audit source snapshot

Date: 2026-04-17

Summary:
- Audited `training/train_e2b.py` against the generated binary SFT artifacts.
- Confirmed the binary SFT file structure matches the script's expected `messages` shape.
- Confirmed the VPS is not a training host for this stage: no `mlx_tune`, no `torch`, no `unsloth`, and Hugging Face auth is not logged in.
- Measured that the binary SFT files are extremely large, with train user messages averaging ~82.8k characters and peaking above 514k characters.
- Patched `train_e2b.py` so backend import is lazy and added smoke-test subset flags.
- Added tests in `tests/test_train_e2b.py` and verified the test suite passes.
- Recommended first real training run: bounded binary smoke test on the Mac only after explicit approval.
