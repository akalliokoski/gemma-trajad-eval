# Dataset-builder data contract

Keep the on-disk pipeline simple:

- `data/raw` — downloaded source snapshots; treat as immutable inputs
- `data/interim` — normalized records and other pre-split artifacts
- `data/processed` — split-ready outputs, manifests, and audits

## Why these names stay

The repo already uses `raw -> interim -> processed` consistently in code, tests, docs, and learning materials. They are clear enough and do not need a rename.

## Optional mental model

If you like warehouse language, the rough mapping is:

- raw ≈ bronze
- interim ≈ silver
- processed ≈ gold

That mapping is explanatory only. The implementation should keep `raw`, `interim`, and `processed`.
