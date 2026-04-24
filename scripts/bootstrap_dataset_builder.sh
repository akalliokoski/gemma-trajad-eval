#!/usr/bin/env bash
set -euo pipefail

command -v uv >/dev/null 2>&1 || {
  echo "uv is required"
  exit 1
}

uv sync --extra dev
mkdir -p data/raw data/interim data/processed
uv run python - <<'PY'
import datasets, tqdm, pydantic, huggingface_hub, numpy, sklearn
print('dataset-builder bootstrap ok')
PY

echo "Ready: data/raw data/interim data/processed"
