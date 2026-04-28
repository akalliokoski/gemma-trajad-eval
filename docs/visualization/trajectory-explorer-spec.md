# Trajectory Explorer Spec

Reference visualization:
- GitHub: https://github.com/ArkAung/interactive-turboquant
- Live demo: https://arkaung.github.io/interactive-turboquant/

## Goal

Ship a static, desktop-first visualization slice that makes the gemma-trajad-eval project legible to a newcomer and useful in a presentation.

## Audience

1. Newcomer
   - Needs to understand what a trajectory is and why anomaly labels exist.
2. Researcher/operator
   - Needs to inspect one normal trace, one anomalous trace, and the surrounding dataset context.
3. Project owner
   - Needs a visually strong artifact that explains the repo's data, training, and evaluation direction.

## First-slice scope

The first slice must include:
- one static HTML entrypoint at `apps/trajectory_explorer/index.html`
- generated payload assets under `apps/trajectory_explorer/assets/`
- one normal trajectory sample and one anomalous trajectory sample
- a visible `bad_step` highlight
- a dataset summary panel
- a fine-tuning lifecycle panel
- an evaluation/rule-coverage panel

## Constraints

- No frontend build step.
- Plain HTML/CSS/JS only.
- Theme should reuse the repo's tactical HUD visual language.
- The browser should consume compact exported payloads, not raw JSONL corpora.
- The exported asset bundle should support local static viewing without a live backend.

## Acceptance criteria

- A reader can explain the difference between a normal and anomalous trajectory after using the page.
- The page explains `bad_step` visually and textually.
- The dataset panel shows repo-truth counts from generated payloads.
- The training panel explains the path from processed JSONL to adapters and evaluation reports.
- The evaluation panel clearly distinguishes current dataset/rule coverage from future model-run metrics.
