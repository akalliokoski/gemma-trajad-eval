# Dataset Builder Phase-1 Readiness Improvements Implementation Plan

> For Hermes: use subagent-driven-development when executing this plan task-by-task.

**Goal:** Turn the Phase 0 findings into a small set of practical implementation upgrades that make `dataset_builder/` easier to run, easier to trust, and better prepared for Phase 1 hands-on pipeline work without rewriting the project.

**Architecture:** Keep the current script-first `raw -> interim -> processed` pipeline and improve the weak seams around environment reproducibility, inspection ergonomics, perturbation coverage, and post-build quality visibility. Prefer `uv` as the package and environment workflow. Keep `raw/interim/processed` as the canonical storage contract; do not rename the pipeline to bronze/silver/gold in code.

**Tech Stack:** Python 3.11+, `uv`, pytest, JSONL, Hugging Face datasets, markdown docs, Hermes Agent.

---

## Naming decision

This plan is named **Phase-1 Readiness Improvements**, not `phase-0-improvements-part-2`.

Reasoning:
1. The motivation does come from Phase 0 learning materials, especially 0.2 codebase orientation and 0.3 environment setup.
2. But the code changes themselves are mainly about making the implementation safer and smoother for the next stage of actual pipeline work.
3. So the most honest framing is: these are implementation improvements derived from Phase 0, in service of entering Phase 1 cleanly.

If a future plan is still purely retrospective and taxonomy-driven, `phase-0-improvements-part-2` would be reasonable. For this one, `phase-1 readiness` is the better fit.

## Staging terminology decision

Keep these as the canonical dataset-builder storage stages:
- `data/raw`
- `data/interim`
- `data/processed`

Do **not** rename directories, CLI help, manifests, or code paths to bronze/silver/gold right now.

Why:
- the current names are already clear and widely understood in Python/data-pipeline repos
- they appear throughout the codebase and docs already
- renaming them would create churn without improving data quality
- this project benefits more from trustworthy outputs than from warehouse-style terminology

However, it is reasonable to mention this conceptual mapping in one architecture doc:
- raw ≈ bronze
- interim ≈ silver
- processed ≈ gold

That gives the user the mental model without polluting the implementation.

---

## Why this plan exists

Phase 0.2 and 0.3 suggest four practical conclusions:

1. The current modular script layout is good and should be preserved.
2. `uv` should be the default environment workflow for this repo.
3. Inspection and diagnostics should be strengthened before adding more complexity.
4. The next missing value is not infrastructure sprawl; it is better operational ergonomics and better data-quality confidence.

The project is the first one in the user's home AI lab, so the right bar is:
- best practice
- practical elegance
- simple defaults
- no platform theater

---

## Target improvements

This plan focuses on six concrete improvements:

1. Make `uv` the first-class environment and command workflow.
2. Add a small dataset-builder bootstrap entrypoint with repeatable checks.
3. Expand `inspect_traces.py` into a more useful planning/debugging tool for Phase 1 work.
4. Fill the most obvious perturbation-coverage gap with `invalid_tool_json`.
5. Add a lightweight post-build audit report that summarizes dataset quality signals.
6. Document the storage contract and explicitly keep bronze/silver/gold as a doc-only mental model.

---

## Scope constraints

### Explicitly in scope
- `uv`-first local workflow
- repo-local scripts and docs
- additional tests for new behavior
- lightweight reports written to disk
- one new perturbation rule if it cleanly fits the current architecture

### Explicitly out of scope
- no workflow orchestrator
- no database
- no notebook-first redesign
- no web UI
- no LLM continuation generation
- no directory rename from `raw/interim/processed` to bronze/silver/gold
- no heavy cross-machine work

---

## Task 1: Make `uv` the canonical local workflow

**Status:** Done (2026-04-24)
**Verification:** `uv lock`, `uv sync --extra dev`, `uv run python - <<'PY' ... print('ok') ... PY`
**Implementation infographic:** `infographic/phase-1-readiness-improvements/infographic.png`

**Objective:** Replace mixed setup guidance with a single repo-standard `uv` workflow.

**Files:**
- Create: `.python-version`
- Create: `uv.lock`
- Modify: `README.md`
- Modify: `docs/data-pipeline-walkthrough.md`
- Modify: `docs/learning-materials/dataset-builder/phase-0/0.3-environment-setup/dataset-builder-environment-setup/README.md`
- Modify: `docs/learning-materials/dataset-builder/phase-0/0.3-environment-setup/dataset-builder-environment-setup/answers.md`

**Step 1: Confirm current Python target**

Use the already-declared project requirement:
```toml
requires-python = ">=3.11"
```
Choose one concrete local default for the repo, preferably `3.11` unless the current environment strongly requires a newer patch line.

**Step 2: Add `.python-version`**

Write a single line such as:
```text
3.11
```

**Step 3: Generate and commit `uv.lock`**

Run:
```bash
uv lock
```
Expected: a new `uv.lock` file is created and can be committed.

**Step 4: Update setup docs to prefer `uv`**

Standardize examples around:
```bash
uv sync --extra dev
uv run pytest -q
uv run python dataset_builder/inspect_traces.py --help
```

**Step 5: Keep one compatibility note only**

Do not keep dual-path documentation everywhere. Mention once that `venv/pip` is conceptually equivalent, but the repo standard is now `uv`.

**Step 6: Verify**

Run:
```bash
uv sync --extra dev
uv run python -c "import datasets, tqdm, pydantic, huggingface_hub, numpy, sklearn; print('ok')"
```
Expected: prints `ok`.

**Step 7: Commit**

```bash
git add .python-version uv.lock README.md docs/data-pipeline-walkthrough.md docs/learning-materials/dataset-builder/phase-0/0.3-environment-setup/dataset-builder-environment-setup/README.md docs/learning-materials/dataset-builder/phase-0/0.3-environment-setup/dataset-builder-environment-setup/answers.md
git commit -m "build: standardize repo workflow on uv"
```

---

## Task 2: Add a single dataset-builder bootstrap command

**Status:** Done (2026-04-24)
**Verification:** `./scripts/bootstrap_dataset_builder.sh`
**Implementation infographic:** `infographic/phase-1-readiness-improvements/infographic.png`

**Objective:** Make repo setup and data-directory preparation boring and repeatable.

**Files:**
- Create: `scripts/bootstrap_dataset_builder.sh`
- Modify: `README.md`
- Modify: `docs/data-pipeline-walkthrough.md`

**Step 1: Write the bootstrap script**

Create a small shell script that:
1. checks `uv` exists
2. runs `uv sync --extra dev`
3. creates `data/raw`, `data/interim`, and `data/processed`
4. runs a dependency smoke test
5. prints a short success summary

Suggested script shape:
```bash
#!/usr/bin/env bash
set -euo pipefail

command -v uv >/dev/null 2>&1 || { echo "uv is required"; exit 1; }

uv sync --extra dev
mkdir -p data/raw data/interim data/processed
uv run python -c "import datasets, tqdm, pydantic, huggingface_hub, numpy, sklearn; print('dataset-builder bootstrap ok')"

echo "Ready: data/raw data/interim data/processed"
```

**Step 2: Make the script executable**

Run:
```bash
chmod +x scripts/bootstrap_dataset_builder.sh
```

**Step 3: Document the one-command setup**

Add a short section to `README.md`:
```bash
./scripts/bootstrap_dataset_builder.sh
```

**Step 4: Verify**

Run:
```bash
./scripts/bootstrap_dataset_builder.sh
```
Expected:
- `uv sync --extra dev` completes
- data directories exist
- smoke test prints success

**Step 5: Commit**

```bash
git add scripts/bootstrap_dataset_builder.sh README.md docs/data-pipeline-walkthrough.md
git commit -m "feat: add dataset-builder bootstrap script"
```

---

## Task 3: Expand `inspect_traces.py` for Phase 1 planning work

**Status:** Done (2026-04-24)
**Verification:** `uv run pytest tests/test_inspect_traces.py -v`, `uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --schema-report --tool-stats --eligibility-report`
**Implementation infographic:** `infographic/phase-1-readiness-improvements/infographic.png`

**Objective:** Turn the inspection script into the main operational microscope for upcoming hands-on tasks.

**Files:**
- Modify: `dataset_builder/inspect_traces.py`
- Test: `tests/test_inspect_traces.py`
- Modify: `docs/learning-materials/dataset-builder/phase-0/0.2-codebase-orientation/dataset-builder-codebase-orientation/answers.md`
- Optionally modify: `docs/data-pipeline-walkthrough.md`

**Step 1: Add failing tests for new CLI/report modes**

Add tests for helper behavior behind the following capabilities:
- `--schema-report`
- `--tool-stats`
- `--eligibility-report`

At minimum, test pure helper functions even if full CLI snapshot tests are too brittle.

**Step 2: Add a schema report**

Implement a mode that reports:
- detected trajectory field name(s)
- detected role key style(s): `role/content` vs `from/value`
- proportion of records with `tools`
- proportion of records with embedded `<tool_call>` markup

**Step 3: Add a tool stats report**

Implement a mode that reports:
- average tool-call count per trace
- average tool-response count per trace
- percent of traces with at least one tool call
- percent with at least two assistant tool-call turns

**Step 4: Add an eligibility report**

Implement a mode that estimates how many records are eligible for:
- P1-style wrong tool choice
- P2-style tool argument mutation
- P3/P4/P5 class rules that need tool interaction
- P8-style multi-step patterns that need multiple tool-call pairs

Keep this rule-of-thumb simple and derived from observable trajectory structure.

**Step 5: Keep the implementation small**

Do not introduce pandas, notebooks, or a reporting framework. Keep it as additional CLI flags and helper functions inside `inspect_traces.py`.

**Step 6: Verify**

Run:
```bash
uv run pytest tests/test_inspect_traces.py -v
uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --schema-report
uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --tool-stats
uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --eligibility-report
```
Expected: tests pass and each command prints a stable readable report.

**Step 7: Commit**

```bash
git add dataset_builder/inspect_traces.py tests/test_inspect_traces.py docs/learning-materials/dataset-builder/phase-0/0.2-codebase-orientation/dataset-builder-codebase-orientation/answers.md docs/data-pipeline-walkthrough.md
git commit -m "feat: expand trace inspection for phase 1 planning"
```

---

## Task 4: Implement `invalid_tool_json` as the next perturbation rule

**Status:** Done (2026-04-24)
**Verification:** `uv run pytest tests/test_perturbations.py tests/test_validate_labels.py -v`, `uv run python dataset_builder/build_trajad_dataset.py --seed 42`, `uv run python dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
**Implementation infographic:** `infographic/phase-1-readiness-improvements/infographic.png`

**Objective:** Fill the most obvious Phase 0 taxonomy gap with one practical new anomaly rule.

**Files:**
- Modify: `dataset_builder/perturbations.py`
- Modify: `dataset_builder/validate_labels.py`
- Test: `tests/test_perturbations.py`
- Test: `tests/test_validate_labels.py`
- Optionally modify: `dataset_builder/build_trajad_dataset.py`

**Step 1: Write failing tests for the new rule**

Add tests that cover:
- eligible records return an anomalous variant
- ineligible records return `None`
- the produced anomaly uses `anomaly_type == "invalid_tool_json"`
- `anomaly_class` is set consistently
- `bad_step` points at the assistant turn containing the corrupted tool call

**Step 2: Define the rule minimally**

Implement a rule that corrupts serialized tool-call JSON in one assistant message while preserving the rest of the trajectory.

Good corruption patterns:
- missing closing brace
- trailing comma
- mismatched quote around a key or string value

Bad patterns to avoid:
- replacing the whole message with gibberish
- deleting the entire step
- modifying downstream turns to simulate continuation

**Step 3: Decide anomaly class deliberately**

Map `invalid_tool_json` to `task_failure`.
Document the reasoning inline.

**Step 4: Keep validation rule-aware but simple**

In `validate_labels.py`, add just enough checks to ensure:
- the labeled bad step exists
- the bad-step message is an assistant turn
- the assistant turn contains tool-call markup that is malformed in the intended way

Do not attempt a full parser framework.

**Step 5: Decide whether to add it to `ALL_RULES` only or also `MVP_RULES`**

Default recommendation:
- add to `ALL_RULES`
- do not add to `MVP_RULES` yet

Reason: this is useful coverage, but it is still a new realism surface and should earn its way into the default safer subset.

**Step 6: Verify**

Run:
```bash
uv run pytest tests/test_perturbations.py tests/test_validate_labels.py -v
uv run python dataset_builder/build_trajad_dataset.py --seed 42
uv run python dataset_builder/validate_labels.py data/processed/all.jsonl --strict
```
Expected:
- tests pass
- build completes
- strict validation passes
- manifest includes the new anomaly type if the rule fires

**Step 7: Commit**

```bash
git add dataset_builder/perturbations.py dataset_builder/validate_labels.py tests/test_perturbations.py tests/test_validate_labels.py dataset_builder/build_trajad_dataset.py
git commit -m "feat: add invalid tool json perturbation rule"
```

---

## Task 5: Add a lightweight post-build audit report

**Status:** Done (2026-04-24)
**Verification:** `uv run pytest tests/test_audit_dataset.py -v`, `uv run python dataset_builder/audit_dataset.py data/processed/all.jsonl`
**Implementation infographic:** `infographic/phase-1-readiness-improvements/infographic.png`

**Objective:** Make each dataset build easier to assess without reading JSONL manually.

**Files:**
- Create: `dataset_builder/audit_dataset.py`
- Test: `tests/test_build_manifest.py` or create `tests/test_audit_dataset.py`
- Modify: `README.md`
- Optionally modify: `dataset_builder/build_trajad_dataset.py`

**Step 1: Create a tiny audit script**

The script should read `data/processed/all.jsonl` and print a concise report with:
- total records
- split counts
- anomaly type counts
- anomaly class counts
- average trajectory length by split
- average tool-call count by split when present in metadata
- bad-step position histogram buckets, e.g. early / middle / late

**Step 2: Support a file argument**

CLI shape:
```bash
uv run python dataset_builder/audit_dataset.py data/processed/all.jsonl
```

**Step 3: Optionally emit markdown**

If simple, support:
```bash
uv run python dataset_builder/audit_dataset.py data/processed/all.jsonl --markdown > data/processed/audit_report.md
```

This is useful, but keep it optional.

**Step 4: Keep it deterministic and local**

No notebook output, no plotting library, no web UI. Plain text or markdown only.

**Step 5: Verify**

Run:
```bash
uv run pytest tests/test_audit_dataset.py -v
uv run python dataset_builder/build_trajad_dataset.py --seed 42
uv run python dataset_builder/audit_dataset.py data/processed/all.jsonl
```
Expected: stable readable report with no crashes.

**Step 6: Commit**

```bash
git add dataset_builder/audit_dataset.py tests/test_audit_dataset.py README.md dataset_builder/build_trajad_dataset.py
git commit -m "feat: add lightweight dataset audit report"
```

---

## Task 6: Document the storage contract and bronze/silver/gold mapping without renaming anything

**Status:** Done (2026-04-24)
**Verification:** doc review against `README.md`, `docs/data-pipeline-walkthrough.md`, and `docs/dataset-builder-data-contract.md`
**Implementation infographic:** `infographic/phase-1-readiness-improvements/infographic.png`

**Objective:** Make the dataset stages easier to explain while preserving the current simple code and paths.

**Files:**
- Create: `docs/dataset-builder-data-contract.md`
- Modify: `README.md`
- Optionally modify: `docs/learning-materials/dataset-builder/phase-0/0.3-environment-setup/dataset-builder-environment-setup/answers.md`

**Step 1: Write the contract doc**

Document:
- `data/raw` = downloaded immutable source snapshots
- `data/interim` = normalized and still mostly source-shaped records
- `data/processed` = split-ready training/eval artifacts and manifests

**Step 2: Add the conceptual alias only in prose**

Include a short note:
- raw ≈ bronze
- interim ≈ silver
- processed ≈ gold

And immediately explain that these are conceptual aliases only; the codebase will keep `raw/interim/processed`.

**Step 3: Link from README**

Add one short section pointing to the contract doc.

**Step 4: Verify**

Read the docs end-to-end and make sure there is no contradictory guidance that suggests actual directory renames.

**Step 5: Commit**

```bash
git add docs/dataset-builder-data-contract.md README.md docs/learning-materials/dataset-builder/phase-0/0.3-environment-setup/dataset-builder-environment-setup/answers.md
git commit -m "docs: clarify dataset-builder storage contract"
```

---

## Recommended execution order

Execute in this order:
1. Task 1 — `uv` canonicalization
2. Task 2 — bootstrap script
3. Task 3 — richer inspection
4. Task 6 — storage contract doc
5. Task 4 — `invalid_tool_json`
6. Task 5 — audit report

Why this order:
- first make setup boring
- then improve visibility
- then clarify the storage model
- then add one new perturbation capability
- then add a compact audit loop for routine builds

---

## Validation checklist for the full plan

After all tasks are complete, run:

```bash
./scripts/bootstrap_dataset_builder.sh
uv run pytest -q
uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --schema-report
uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --eligibility-report
uv run python dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized.jsonl
uv run python dataset_builder/build_trajad_dataset.py --seed 42
uv run python dataset_builder/validate_labels.py data/processed/all.jsonl --strict
uv run python dataset_builder/audit_dataset.py data/processed/all.jsonl
```

Expected outcomes:
- setup is one-command and uses `uv`
- tests pass
- inspection reports are useful for Phase 1 analysis
- build completes successfully
- strict validation passes
- audit report gives a quick quality summary

---

## Risks and tradeoffs

### Risk 1: `uv.lock` introduces dependency churn
Mitigation: accept this as the cost of a reproducible local workflow; keep the lockfile committed and reviewed.

### Risk 2: `invalid_tool_json` may be too synthetic
Mitigation: start with `ALL_RULES` only, not `MVP_RULES`.

### Risk 3: `inspect_traces.py` becomes a kitchen-sink script
Mitigation: only add modes that directly support Phase 1 decisions; do not turn it into a framework.

### Risk 4: bronze/silver/gold language leaks into code and creates churn
Mitigation: keep it doc-only.

---

## Definition of done

This plan is complete when:
- the repo uses `uv` as its documented default workflow
- a one-command bootstrap exists
- `inspect_traces.py` can report schema, tool stats, and rule-eligibility signals
- `invalid_tool_json` exists as a tested non-MVP rule
- a lightweight dataset audit report exists
- the storage contract is documented clearly
- no part of the implementation was renamed to bronze/silver/gold

---

## Follow-on plan after this one

If these tasks work well, the next plan should probably be a true Phase 1 execution plan covering:
- dataset download and empirical EDA
- normalization spot-check workflow
- perturbation eligibility measurement
- first manual review loop
- HF publication readiness
