Create a clean, highly legible setup-guide infographic PNG in English.

Layout: linear-progression
Style: ikea-manual
Aspect ratio: 16:9 landscape

Topic: Dataset builder environment setup

Goal:
Teach a learner the minimal reproducible setup for this repo, including the generic venv path, the VPS-specific uv path, the import verification step, Hugging Face auth timing, and the three data directories.

Hard constraints:
- very high text legibility
- large typography only
- no paragraphs
- no tiny terminal screenshots
- no garbled filler text
- perfect spelling
- use short shell-command chips only
- clean minimal instruction-manual aesthetic

Required content blocks:
1. Title block: "Dataset Builder Environment Setup"
2. Repo contract checklist with exact terms:
   Python 3.11+, .venv, install deps, boring and local
3. Canonical path ladder with these exact command chips:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   python -c "import datasets, tqdm, pydantic; print('ok')"
4. VPS-specific branch with exact terms:
   system python3 exists, system pip unavailable, uv available, uv venv .venv, uv pip install
5. Verification panel with exact labels:
   datasets, tqdm, pydantic, huggingface_hub, numpy, sklearn
6. HF auth timing panel with exact command chips:
   pip install huggingface-hub
   huggingface-cli login
   huggingface-cli whoami
   public read now, publish later
7. Directory tree panel with exact folders:
   data/raw/
   data/interim/
   data/processed/

Visual guidance:
- show a single left-to-right or top-to-bottom sequence with one decision fork for uv
- use folder icons and terminal chips
- make the message feel calm and approachable
- visually distinguish generic repo contract from host-specific adaptation
- overall feel: elegant practical setup card, not corporate poster
