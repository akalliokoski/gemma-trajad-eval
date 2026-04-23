# Dataset Builder Phase-0 Overnight Run Handoff

Date: 2026-04-23
Repo: `/home/hermes/gemma-trajad-eval`
Primary plan: `docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md`

## Goal
Finish the remaining plan items:
- Task 6: deepen validation for first-error localization
- Task 7: add build manifests and perturbation diagnostics

Do the work in a durable Hermes tmux session on the VPS, using the repo as the control plane and keeping the handoff file as the external source of truth.

## Current state
- Tasks 1-5 are already completed in the main plan and in the wiki.
- Working tree was clean when this handoff was created.
- Relevant implementation files already in play:
  - `dataset_builder/validate_labels.py`
  - `dataset_builder/build_trajad_dataset.py`
  - `dataset_builder/perturbations.py`
  - `dataset_builder/coherence.py`
  - `tests/test_validate_labels.py`
  - `tests/test_build_trajad_dataset.py`
- There is not yet a `tests/test_build_manifest.py` file.

## Required workflow rules
1. Load and follow these skills first:
   - `dataset-builder-phase0-overnight-run`
   - `plan-task-execution-loop`
   - `resource-safe-vps-delegation`
2. Treat `docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md` as the implementation contract.
3. Prefer coordinator-local execution for Tasks 6 and 7; do not delegate unless a bounded validation/review subtask clearly reduces risk.
4. After each task, do the full completion loop:
   - implement
   - verify
   - create/update infographic PNG artifact
   - update the plan status block with date + verification + infographic path
   - update the wiki
   - commit
   - push
5. Do not batch both tasks into one commit unless forced by a blocker. Prefer one clean commit per task.
6. If a task fails verification, debug and retry before moving on.
7. If the run is blocked by something that cannot be resolved locally, stop and leave a concise blocker note appended to this file.

## Task 6 execution guidance
Objective: make validation enforce first-bad-step semantics, not just type/range checks.

Suggested starting reads:
- `dataset_builder/validate_labels.py`
- `tests/test_validate_labels.py`
- `dataset_builder/perturbations.py`
- `docs/labeling-guidelines.md`

Expected verification:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py -v`
- `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`

Expected deliverables:
- code + tests
- `infographic/task-6-rule-aware-bad-step-validation/infographic.png`
- wiki transcript/query updates for Task 6
- plan file updated with Task 6 status block
- commit + push

## Task 7 execution guidance
Objective: make builds reproducible and inspectable via saved manifest + better diagnostics.

Suggested starting reads:
- `dataset_builder/build_trajad_dataset.py`
- `tests/test_build_trajad_dataset.py`
- `dataset_builder/coherence.py`
- the Task 7 section in the primary plan

Expected verification:
- `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_build_manifest.py -v`
- `python3 dataset_builder/build_trajad_dataset.py --seed 42`
- `python3 -m json.tool data/processed/build_manifest.json > /tmp/build_manifest.pretty.json`
- `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`

Expected deliverables:
- manifest-writing implementation
- `tests/test_build_manifest.py`
- `data/processed/build_manifest.json`
- `infographic/task-7-build-manifest-and-diagnostics/infographic.png`
- wiki transcript/query updates for Task 7
- plan file updated with Task 7 status block
- commit + push

## Stop conditions
Stop only when one of these is true:
- both Task 6 and Task 7 are complete and pushed, or
- there is a concrete blocker that prevents safe completion

## If fully complete
Final report should include:
- completed tasks
- verification commands and exact pass results
- infographic paths
- wiki files updated
- commit hashes
- push results

## Re-entry policy
The overnight run uses bounded Hermes passes, not one immortal conversation.

If a pass stops because of iteration budget, idle prompt, or a dead session, the correct recovery is to start a fresh Hermes pass from repo state.

Re-entry rules:
- treat this handoff file, the main plan, git state, and wiki state as the durable source of truth
- reuse the tmux session name `dataset-phase0-overnight` for the active pass
- it is acceptable to kill and recreate the tmux session when the previous Hermes pass is exhausted or stale
- prefer a fresh Hermes process over trying to preserve a bloated old conversation
- the first objective after re-entry is to inspect the current repo state and finish any incomplete task tail before starting new work

## Re-entry prompt
Use this prompt when relaunching a fresh pass:

`Continue the overnight dataset-builder Phase 0 run in /home/hermes/gemma-trajad-eval. Read and follow AGENTS.md, docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md, docs/plans/2026-04-23-dataset-builder-phase-0-overnight-run.md, docs/plans/2026-04-23-dataset-builder-phase-0-single-task-guide.md, wiki/SCHEMA.md, wiki/index.md, and wiki/log.md. Inspect git status first, then finish any incomplete task tail before starting anything new. Complete the remaining undone or unfinished work from the main plan. For each task do the full loop: implement, verify, create the required infographic PNG, update the plan, update the wiki, commit, and push. Prefer direct local execution on the VPS and avoid delegation unless it is tightly bounded and clearly useful. Stop only when both tasks are complete and pushed, or when you hit a concrete blocker that cannot be resolved locally; if blocked, append a concise blocker note to the overnight handoff file.`

## Monitoring notes
Primary session name: `dataset-phase0-overnight`
Useful checks from another shell:
- `tmux capture-pane -t dataset-phase0-overnight -p | tail -100`
- `tmux list-sessions`
- `git -C /home/hermes/gemma-trajad-eval log --oneline -5`
