# Interactive trajectory explorer first slice

Question: What did the first implemented slice of the trajectory visualization add to the repository?

Answer:
The first slice added a static, TurboQuant-inspired trajectory explorer under `apps/trajectory_explorer/` plus the export path and docs needed to keep it grounded in repo data.

## What shipped
- `apps/trajectory_explorer/index.html` provides the static visualization shell
- `apps/trajectory_explorer/app.js` renders the hero, pipeline, trajectory explorer, dataset summary, training lifecycle, and evaluation summary
- `scripts/export_trajectory_explorer_payload.py` regenerates browser payloads
- `dataset_builder/trajectory_explorer_payload.py` builds compact exported payloads and a `payload_bundle.js` file for static local viewing
- `docs/visualization/trajectory-explorer-spec.md`, `trajectory-explorer-storyboard.md`, and `trajectory-explorer-data-contract.md` define the first-slice product shape

## Why it matters
This turns the visualization plan into a runnable artifact instead of a design note. The repo now has a concrete browser-facing surface that explains:
- what a trajectory looks like
- where `bad_step` lives
- how dataset counts and perturbation coverage fit around the example
- how later fine-tuning and evaluation stages connect to the current dataset work

## Design decision
The first slice keeps the frontend buildless.

Instead of requiring a framework or dev server, the exporter writes compact JSON plus `payload_bundle.js`, which lets `index.html` open as a static artifact while still keeping the data export step explicit.

## Validation
- `uv run pytest -q`
- `uv run python scripts/export_trajectory_explorer_payload.py`
- `node --check apps/trajectory_explorer/app.js`

## Related pages
- [[hermes-first-development]]
- [[execution-topology]]
