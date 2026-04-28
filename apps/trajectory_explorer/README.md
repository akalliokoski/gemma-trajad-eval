# Trajectory Explorer

First static visualization slice for `gemma-trajad-eval`.

Reference inspiration:
- GitHub: https://github.com/ArkAung/interactive-turboquant
- Live demo: https://arkaung.github.io/interactive-turboquant/

## Regenerate payloads

```bash
uv run python scripts/export_trajectory_explorer_payload.py
```

This writes:
- `assets/overview_payload.json`
- `assets/sample_trajectories.json`
- `assets/training_payload.json`
- `assets/evaluation_payload.json`
- `assets/payload_bundle.js`

## Open locally

Because the first slice emits `payload_bundle.js`, the page can be opened directly as a static file:

- `apps/trajectory_explorer/index.html`

A tiny local server is still fine if preferred:

```bash
cd apps/trajectory_explorer
uv run python -m http.server 8000
```

Then open `http://127.0.0.1:8000/`.

## What this slice includes

- hero and project pipeline framing
- one normal sample and one anomalous sample
- timeline canvas with `bad_step` highlight
- dataset summary and perturbation coverage
- fine-tuning lifecycle panel
- evaluation status panel
