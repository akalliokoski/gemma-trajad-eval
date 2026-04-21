# Hermes-First Roadmap Implementation Plan

> For Hermes: use subagent-driven-development when executing this plan task-by-task.

**Goal:** Turn the repository into a functioning Hermes-first build-and-learn system while advancing the original trajectory-anomaly, data engineering, and Gemma fine-tuning goals.

**Architecture:** Keep the existing repo as the implementation surface and add process scaffolding around it: a repo-local wiki, roadmap docs, reusable skills, and study artifacts. Treat the VPS as the control plane, the Apple Silicon MacBook Pro as the preferred small/medium compute worker, and Modal as a future heavy-GPU tier. Execute work in narrow vertical slices so each slice produces code, verification, and human-readable learning material.

**Tech Stack:** Hermes Agent, project skills, Python, Gemma, Unsloth, Apple Silicon, markdown docs, repo-local LLM Wiki.

---

### Task 1: Establish project operating scaffolding

**Objective:** Make the Hermes-first workflow explicit and reusable before deeper implementation work.

**Files:**
- Existing: `AGENTS.md`
- Existing: `README.md`
- Existing: `docs/execution-topology.md`
- Existing: `wiki/SCHEMA.md`
- Existing: `wiki/index.md`
- Existing: `wiki/log.md`
- Existing: `docs/plans/2026-04-17-hermes-pivot.md`

**Step 1: Verify project instructions exist**
Run: read the files above.
Expected: AGENTS, README, execution-topology docs, and wiki scaffolding all reflect the Hermes-first scope.

**Step 2: Fill any missing operating gaps**
Add missing conventions for planning, verification, wiki maintenance, study-material expectations, workload placement, and approval gates for Mac dispatch.

**Step 3: Verify consistency**
Run: inspect file contents and git diff.
Expected: no contradictions between top-level docs.

---

### Task 2: Audit the current codebase as a starting baseline

**Objective:** Build a grounded understanding of what already exists in dataset building, training, prompts, and integrations.

**Files:**
- Inspect: `dataset_builder/*.py`
- Inspect: `training/*.py`
- Inspect: `integrations/*.py`
- Create: `docs/codebase-baseline.md`
- Update: `wiki/index.md`
- Create/Update: relevant wiki pages under `wiki/entities/`, `wiki/concepts/`, or `wiki/queries/`

**Step 1: Read the current code paths**
Run: inspect scripts in dataset_builder, training, and integrations.
Expected: clear picture of implemented, partial, and missing pieces.

**Step 2: Write a baseline note**
Create `docs/codebase-baseline.md` summarizing:
- what exists
- what looks runnable
- obvious gaps
- likely next implementation slice
- likely execution tier for the next slice (VPS, Mac, or later Modal)

**Step 3: Capture durable knowledge in the wiki**
Create or update pages for key entities/concepts discovered during the audit.

**Step 4: Verify**
Run: re-read the new note and confirm linked wiki updates exist.

---

### Task 3: Make the data pipeline runnable end-to-end on a tiny slice

**Objective:** Get the existing data-engineering path working on a small, inspectable subset before scaling or redesigning anything.

**Files:**
- Inspect/modify as needed: `dataset_builder/download_hermes.py`
- Inspect/modify as needed: `dataset_builder/inspect_traces.py`
- Inspect/modify as needed: `dataset_builder/normalize_trajectory.py`
- Inspect/modify as needed: `dataset_builder/perturbations.py`
- Inspect/modify as needed: `dataset_builder/build_trajad_dataset.py`
- Inspect/modify as needed: `dataset_builder/validate_labels.py`
- Create: `docs/data-pipeline-walkthrough.md`
- Update wiki pages and log

**Step 1: Run the smallest viable pipeline commands**
Expected: either a tiny output artifact or concrete failure modes.

Constraint: keep this initial slice on the VPS unless Apple-Silicon-specific execution is clearly needed. Do not schedule high-RAM Mac work without user approval.

**Step 2: Fix blockers one by one**
Prefer small, verified edits over broad rewrites.

**Step 3: Save a walkthrough**
Document inputs, commands, outputs, and checks in `docs/data-pipeline-walkthrough.md`.

**Step 4: Capture reusable procedure knowledge**
If a non-trivial workflow stabilizes, create or patch a relevant Hermes skill.

**Step 5: Verify**
Run: the tiny pipeline again from scratch.
Expected: reproducible success on a sample slice.

---

### Task 4: Make training prep and one local experiment runnable

**Objective:** Convert the dataset output into training-ready examples and execute one local-first Gemma experiment path.

**Files:**
- Inspect/modify as needed: `training/prepare_sft_data.py`
- Inspect/modify as needed: `training/train_e2b.py`
- Inspect/modify as needed: `training/inference.py`
- Inspect/modify as needed: `training/evaluate.py`
- Create: `docs/local-training-playbook.md`
- Update wiki pages and log

**Step 1: Validate training data formatting**
Expected: a small, inspectable SFT sample artifact.

**Step 2: Run the smallest practical local experiment**
Expected: either a successful smoke test or concrete environment/model blocker details.

Constraint: choose the least disruptive execution tier first. If the experiment would create meaningful RAM pressure on the Mac, stop and ask the user before dispatching it there.

**Step 3: Document the path**
Write a local training playbook with commands, assumptions, fallback paths, and verification steps.

**Step 4: Verify**
Run: the documented smoke-test command sequence again.
Expected: repeatable behavior.

---

### Task 5: Add evaluation and demo evidence

**Objective:** Ensure the project produces interpretable evidence instead of isolated scripts.

**Files:**
- Inspect/modify as needed: `training/evaluate.py`
- Inspect/modify as needed: `integrations/*.py`
- Create: `docs/first-demo-report.md`
- Update wiki pages and log

**Step 1: Define the first demo target**
Pick one narrow demo, such as small-slice anomaly scoring or trace inspection.

**Step 2: Run the demo path**
Expected: concrete outputs, logs, or screenshots/artifacts.

**Step 3: Write the report**
Summarize what was demonstrated, limitations, and the next technical question.

**Step 4: Verify**
Re-run the smallest demo command and confirm the report matches the observed result.

---

### Task 6: Turn the repo into a better study system

**Objective:** Make sure knowledge compounds as the project grows.

**Files:**
- Create as needed: `docs/tutorials/*.md`
- Update: `wiki/index.md`
- Update: `wiki/log.md`
- Create or patch relevant Hermes skills

**Step 1: Promote good artifacts**
Convert recurring explanations into short tutorials or glossary pages.

**Step 2: Promote good workflows**
Turn stable procedures into Hermes skills.

**Step 3: Keep the wiki healthy**
Regularly orient, ingest, update, and later lint the wiki.

**Step 4: Verify**
Confirm that a newcomer could find the key docs and understand the current state of the project.

---

### Task 7: Add distributed-execution workflows when they become necessary

**Objective:** Make cross-machine work repeatable once the project starts using the Mac or Modal in earnest.

**Files:**
- Update/create: `docs/execution-topology.md`
- Update: `wiki/index.md`
- Update: `wiki/log.md`
- Create or patch relevant Hermes skills

**Step 1: Capture the real workflow**
Document how code, data, artifacts, and commands move between VPS, Mac, and later Modal.

**Step 2: Stabilize the procedure**
Turn repeated coordination steps into a reusable Hermes skill.

**Step 3: Verify**
Confirm that the workflow is understandable and safe, including approval gates for disruptive Mac tasks.

---

## Recommended execution order

1. Task 2 — codebase baseline
2. Task 3 — tiny end-to-end data pipeline
3. Task 4 — local training prep and smoke test
4. Task 5 — first demo evidence
5. Task 6 — tutorial/skill consolidation
6. Task 7 — distributed-execution workflow hardening

## Verification checklist

- [ ] Top-level docs match the Hermes-first scope
- [ ] Wiki exists and is navigable
- [ ] At least one codebase-baseline document exists
- [ ] At least one tiny data pipeline run is documented
- [ ] At least one local training experiment path is documented
- [ ] At least one demo/report exists
- [ ] New durable workflows are saved as skills when warranted
